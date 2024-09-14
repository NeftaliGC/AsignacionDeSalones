import pandas as pd
import json
import os


    # Obtiene el directorio actual
current_dir = os.getcwd()
    
dir = os.path.join(current_dir, 'src/backend/data')

def read_excel(file_name: str) -> pd.DataFrame:
    """
    Lee un archivo Excel y retorna un DataFrame de pandas
    """
    return pd.read_excel(os.path.join(dir, file_name), sheet_name=0, header=None)


def get_data(data: pd.DataFrame) -> dict:
    """
    Convierte un DataFrame en un diccionario
    """

    POSITION = 8

    # Extraer el nombre del archivo
    id = data.iloc[1, 0]

    # Extraer las dimensiones de DISP y GS
    n = data.iloc[4, 0]

    # Extraer DISP
    DISP = data.iloc[POSITION:POSITION+n, 0:6].values.tolist()
    print(type(DISP))
    # Extraer GS
    GS = data.iloc[POSITION+n+3:POSITION+n+n+3, 0:3].values.tolist()

    data_dict = {
        "id": id,
        "DISP": {
            "shape": (n, 6),
            "data": DISP
        },
        "GS": {
            "shape": (n, 3),
            "data": GS
        }
    }

    return data_dict


def write_json(data: dict, file_name: str):
    """
    Escribe un diccionario en un archivo JSON
    """
    with open(os.path.join(dir, file_name), 'w') as file:
        json.dump(data, file)


if __name__ == '__main__':
    # Prueba de la función get_data
    data = read_excel('DATOS BALANCEO DIAS 120 GRUPOS.xlsx')
    data_dict = get_data(data)
    print(data_dict)
    # Prueba de la función write_json
    write_json(data_dict, 'datos120.json')