import cvxpy as cp
import numpy as np
import pandas as pd
import time
import json
import os
import sys
import io

class Model2:
    def __init__(self):
        self.token = None
        self.data = None
        self.n = 0
        self.m = 0
        self.num_profesores = 0
        self.disp = None
        self.gp = None
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
                disponibilidad_horario = dat["input"][0]["data"]["Disponibilidad Horario"]
                self.data = disponibilidad_horario

        if data is not None:
            self.data = data

    # Paso 1
    def setVariables(self):
        # Obtén el valor de "DISP"
        self.n, self.m = self.data["DISP"]["shape"]
        self.disp = np.array(self.data["DISP"]["data"])

        # Obtén el valor de "GP"
        self.num_profesores = self.data["GP"]["shape"][1]
        self.gp = np.array(self.data["GP"]["data"])

        # Variables de decisión: asignación de grupos a días
        self.asig = cp.Variable((self.n, self.m), boolean=True)

        # Configura el objetivo
        self.objective = cp.Minimize(self.objective_function())

    # Paso 2
    def setConstraints(self):
        self.constraints = [
            # Restricción de número de horarios (sesiones) asignados por día
            cp.sum(self.asig[i, :]) == 1 for i in range(self.n)
        ]

        # Restricción para asegurar que un profesor no esté asignado a más de un grupo por horario
        for prof in range(self.num_profesores):
            grupos_profesor = [grupo for grupo in range(self.n) if self.gp[grupo, prof] == 1]
            for hora in range(self.m):
                self.constraints.append(
                    cp.sum([self.asig[grupo, hora] for grupo in grupos_profesor]) <= 1
                )

        # Restricción de disponibilidad de horarios por grupo
        self.constraints += [
            self.asig[i, j] <= self.disp[i, j] for i in range(self.n) for j in range(self.m)
        ]

    # Paso 3
    def setModel(self):
        # Crear el modelo
        self.model = cp.Problem(self.objective, self.constraints)

    # Paso 4
    def solveModel(self):
        # Redirigir stdout a un buffer
        old_stdout = sys.stdout  # Guarda la salida estándar original
        buffer = io.StringIO()  # Crea un buffer en memoria
        sys.stdout = buffer  # Redirige stdout al buffer

        try:
            # Resolver el problema
            self.model.solve(solver=cp.GUROBI, verbose=True)
            self.valOfSol = self.model.value
        finally:
            # Restaurar stdout
            sys.stdout = old_stdout
        
        # Guardar el verbose capturado en un archivo
        with open(f"src/backend/res/{self.token}", "w") as f:
            f.write(buffer.getvalue())

    # Función objetivo cuadrática
    def objective_function(self):
        sumas = [cp.sum(self.asig[:, j]) for j in range(self.m)]
        return  cp.sum([(sumas[0] - sumas[j])**2 for j in range(1, self.m-1)]) + \
                cp.sum([(sumas[j1] - sumas[j2])**2 for j1 in range(self.m-1) for j2 in range(j1+1, self.m-1)]) + \
                cp.sum([(sumas[j] - sumas[self.m-1])**2 for j in range(self.m-1)])

    def get_solution(self):
        print("Asignación de grupos a horarios:")
        # Imprimir matriz de solución binaria
        solution_matrix = np.zeros((self.n, self.m))
        for i in range(self.n):
            for j in range(self.m):
                if self.asig.value[i, j] > 0.5:
                    solution_matrix[i, j] = 1

        return solution_matrix


if __name__ == "__main__":
    with open('src/backend/data/datosm2.json', 'r') as file:
        data = json.load(file)

    name = "ej10-5"

    for i in data:
        if i['id'] == name:
            data = i

    model = Model2()
    model.start_solution(data=data)
    model.setVariables()
    model.setConstraints()
    model.setModel()
    model.solveModel()

    solution = model.get_solution()

    print(solution)

    # Exportar en csv
    hora_inicio = 7 #numerico 00:00 - 24:00

    df_solution = pd.DataFrame(solution, columns=[f'Horario: {hora_inicio + 2 * j}:00 - {hora_inicio + 2 * (j + 1)}:00' for j in range(model.m)])
    df_solution.to_csv('src/backend/res/solucion_binaria.csv', index=False)
