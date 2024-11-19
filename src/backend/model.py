import cvxpy as cp
import numpy as np
import pandas as pd
import time
import json
import os
import sys
import io

class Model:

    def __init__(self):
        self.token = None
        self.data = None
        self.n = 0
        self.m = 0
        self.disp = None
        self.gs = None
        self.asig = None
        self.objective = None
        self.constraints = None
        self.model = None
        self.solution = None
        self.valOfSol = 0

    def start_solution(self, token = None, data = None):

        if token is not None:
            self.token = token
            # Abrir datos.json
            with open(f"src/backend/data/{token}.json", "r") as f:
                # Cargar el contenido completo del archivo JSON
                dat = json.load(f)
                
                # Acceder a la parte específica de "Disponibilidad Dias"
                disponibilidad_dias = dat["input"][0]["data"]["Disponibilidad Dias"]
                self.data = disponibilidad_dias

        if data is not None:
            self.data = data

    # Paso 1
    def setVariables(self):
        # Obtén el valor de "DISP"
        self.n = self.data["DISP"]["shape"][0]
        self.m = self.data["DISP"]["shape"][1]
        self.disp = np.array(self.data["DISP"]["data"])

        # Obtén el valor de "GS"
        self.gs = np.array(self.data["GS"]["data"])

        # Variables de decisión: asignación de grupos a días
        self.asig = cp.Variable((self.n, self.m), boolean=True)

        # Configura el objetivo
        self.objective = cp.Minimize(self.objective_function())


    # Función objetivo cuadrática
    def objective_function(self):
        sumas = [cp.sum(self.asig[:, j]) for j in range(self.m)]
        return  cp.sum([(sumas[0] - sumas[j])**2 for j in range(1, self.m - 1)]) + \
                cp.sum([(sumas[j1] - sumas[j2])**2 for j1 in range(self.m - 1) for j2 in range(j1 + 1, self.m - 1)]) + \
                cp.sum([(sumas[j] - 2 * sumas[self.m - 1])**2 for j in range(self.m - 1)])


    # Paso 2
    def setConstraints(self):
        # Restricciones
        self.constraints = [
            # Restricción de sesiones por semana
            cp.sum(self.asig, axis=1) == self.gs[:, 0] + 2 * self.gs[:, 1] + 3 * self.gs[:, 2],

            # Restricción de disponibilidad
            *[self.asig[i, j] <= self.disp[i, j] for i in range(self.n) for j in range(self.m)]
        ]

        # Evitar grupos con clases en días consecutivos
        for i in range(self.n):
            # Grupos con 1 sesión por semana no necesitan restricciones adicionales
            if self.gs[i, 1] == 1:  # Grupos con 2 sesiones por semana
                for j in range(self.m - 1):
                    self.constraints.append(self.asig[i, j] + self.asig[i, j+1] <= 1)
            if self.gs[i, 2] == 1:  # Grupos con 3 sesiones por semana
                for j in range(self.m - 2):
                    self.constraints.append(self.asig[i, j] + self.asig[i, j+1] + self.asig[i, j+2] <= 2)
                # Además, aseguramos que no se asignen clases en días consecutivos
                for j in range(self.m - 1):
                    self.constraints.append(self.asig[i, j] + self.asig[i, j+1] <= 1)

    # Paso 3
    def setModel(self):
        # Crear el modelo
        self.model = cp.Problem(self.objective, self.constraints)

    # Paso 4
    def solvModel(self, verbose=True):
        # Redirigir stdout a un buffer
        old_stdout = sys.stdout  # Guarda la salida estándar original
        buffer = io.StringIO()  # Crea un buffer en memoria
        sys.stdout = buffer  # Redirige stdout al buffer

        try:
            # Resolver el problema con el verbose activado
            self.model.solve(solver=cp.GUROBI, verbose=verbose)
            self.valOfSol = self.model.value
        finally:
            # Restaurar stdout a su valor original
            sys.stdout = old_stdout

        # Guardar el verbose capturado en un archivo
        with open(f"{self.token}", "w") as f:
            f.write(buffer.getvalue())



if __name__ == '__main__':

    newModel = Model()

    newModel.start_solution(token="cb04ec72-7a3d-4919-b28c-e02792e987e9")
    
    newModel.setVariables()

    newModel.setConstraints()

    newModel.setModel()

    newModel.solvModel()

    n = newModel.n
    m = newModel.m

    # Mostrar resultados
    print("Estado de la solución:", newModel.model.status)
    for i in range(n):
        for j in range(m):
            if newModel.asig.value[i, j] > 0.5:
                print(f"Grupo {i+1} tiene clase en el Día {j+1}")


    # Imprimir matriz de solución binaria
    solution_matrix = np.zeros((n, m))
    for i in range(n):
        for j in range(m):
            if newModel.asig.value[i, j] > 0.5:
                solution_matrix[i, j] = 1

    print("Matriz de solución binaria (6 x m):")
    print(solution_matrix)
