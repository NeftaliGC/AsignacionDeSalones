import cvxpy as cp
import numpy as np
import pandas as pd
import time
import json
import os

# Abrir datos.json
with open('src/backend/data/datos120.json', 'r') as file:
    data = json.load(file)


name = "ex120"

# Medir el tiempo de ejecución
start_time_ex = time.time()  # Inicia el temporizador

for i in data:
    if i['id'] == name:
        # Parámetros de ejemplo 
        n, m = i["DISP"]['shape']
        # Disponibilidad
        DISP = np.array(i['DISP']['data'])
        # Sesiones por semana: cada grupo tiene un número específico de sesiones
        GS = np.array(i['GS']['data'])


# Variables de decisión: asignación de grupos a días
ASIG = cp.Variable((n, m), boolean=True)

# Función objetivo cuadrática
def objective_function():
    sumas = [cp.sum(ASIG[:, j]) for j in range(m)]
    return  cp.sum([(sumas[0] - sumas[j])**2 for j in range(1, m-1)]) + \
            cp.sum([(sumas[j1] - sumas[j2])**2 for j1 in range(m-1) for j2 in range(j1+1, m-1)]) + \
            cp.sum([(sumas[j] - 2 * sumas[m-1])**2 for j in range(m-1)])

objective = cp.Minimize(objective_function())


# Restricciones
constraints = [
    # Restricción de sesiones por semana
    cp.sum(ASIG, axis=1) == GS[:, 0] + 2 * GS[:, 1] + 3 * GS[:, 2],

    # Restricción de disponibilidad
    *[ASIG[i, j] <= DISP[i, j] for i in range(n) for j in range(m)]
]

# Evitar grupos con clases en días consecutivos
for i in range(n):
    # Grupos con 1 sesión por semana no necesitan restricciones adicionales
    if GS[i, 1] == 1:  # Grupos con 2 sesiones por semana
        for j in range(m - 1):
            constraints.append(ASIG[i, j] + ASIG[i, j+1] <= 1)
    if GS[i, 2] == 1:  # Grupos con 3 sesiones por semana
        for j in range(m - 2):
            constraints.append(ASIG[i, j] + ASIG[i, j+1] + ASIG[i, j+2] <= 2)
        # Además, aseguramos que no se asignen clases en días consecutivos
        for j in range(m - 1):
            constraints.append(ASIG[i, j] + ASIG[i, j+1] <= 1)

# Crear el modelo
model = cp.Problem(objective, constraints)

# Medir el tiempo de solucion
start_time_solv = time.time()  # Inicia el temporizador
# Resolver el problema
model.solve(solver=cp.GUROBI, verbose=True)

val = model.value

end_time_solv = time.time() # Detiene el temporizador

end_time_ex = time.time() # Detiene el temporizador


# Mostrar resultados
print("Estado de la solución:", model.status)
for i in range(n):
    for j in range(m):
        if ASIG.value[i, j] > 0.5:
            print(f"Grupo {i+1} tiene clase en el Día {j+1}")


# Imprimir matriz de solución binaria
solution_matrix = np.zeros((n, m))
for i in range(n):
    for j in range(m):
        if ASIG.value[i, j] > 0.5:
            solution_matrix[i, j] = 1

print("Matriz de solución binaria (6 x m):")
print(solution_matrix)

# Exportar la matriz de solución binaria a un archivo CSV
df_solution = pd.DataFrame(solution_matrix, columns=[f'Dia {j+1}' for j in range(m)])
df_solution.to_csv('solucion_binaria.csv', index=False)

print("La matriz de solución binaria se ha exportado a 'solucion_binaria.csv'")

# Imprimir el tiempo de ejecución
execution_time = end_time_ex - start_time_ex
print(f"Tiempo de ejecución: {execution_time:.4f} segundos")

# Imprimir el tiempo de solución
solv_time = end_time_solv - start_time_solv
print(f"Tiempo de solución: {solv_time:.4f} segundos")
print(f"Valor de la función objetivo: {val:.4f}")