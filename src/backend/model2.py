import cvxpy as cp
import numpy as np
import pandas as pd
import time
import json
import os

# Abrir json
with open('src/backend/data/datosm2.json', 'r') as file:
    data = json.load(file)

name = "ej50"

for i in data:
    if i['id'] == name:
        n, m = i['DISP']['shape'] # n (numero de grupos), m (numero de horarios)
        DISP = np.array(i['DISP']['data'])

print("INICIO")
# Medir el tiempo de ejecución
start_time_ex = time.time()  # Inicia el temporizador

# Variables de decisión: asignación de grupos a días
ASIG = cp.Variable((n, m), boolean=True)

# Función objetivo cuadrática
def objective_function():
    sumas = [cp.sum(ASIG[:, j]) for j in range(m)]
    return  cp.sum([(sumas[0] - sumas[j])**2 for j in range(1, m-1)]) + \
            cp.sum([(sumas[j1] - sumas[j2])**2 for j1 in range(m-1) for j2 in range(j1+1, m-1)]) + \
            cp.sum([(sumas[j] - sumas[m-1])**2 for j in range(m-1)])

objective = cp.Minimize(objective_function())

# Restricciones
constraints = [
    # Restricción de número de horarios (sesiones) asignados por día
    cp.sum(ASIG[i, :]) == 1 for i in range(n)
]

# Restriccion de disponibilidad de horarios por grupo
constraints += [
    ASIG[i, j] <= DISP[i, j] for i in range(n) for j in range(m)
]


# Crear el modelo
model = cp.Problem(objective, constraints)

# Resolver el problema
model.solve(solver=cp.GUROBI, verbose=True)

end_time_ex = time.time() # Detiene el temporizador

# Imprimir los resultados
print("Asignación de grupos a horarios:")
# Imprimir matriz de solución binaria
solution_matrix = np.zeros((n, m))
for i in range(n):
    for j in range(m):
        if ASIG.value[i, j] > 0.5:
            solution_matrix[i, j] = 1

print(solution_matrix)

print(f"tiempo de ejecucion: {end_time_ex - start_time_ex}")


# Exportar en csv
hora_inicio = 7 #numerico 00:00 - 24:00

df_solution = pd.DataFrame(solution_matrix, columns=[f'Horario: {hora_inicio + 2 * j}:00 - {hora_inicio + 2 * (j + 1)}:00' for j in range(m)])
df_solution.to_csv('solucion_binaria.csv', index=False)