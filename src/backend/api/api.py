from typing import Union, Annotated
from fastapi import FastAPI, File, UploadFile
import os
import shutil
import tempfile

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Lista de dominios permitidos, ajusta según necesites
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"Asignacion" : "Salones"}

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Crear un archivo temporal
        temp_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_dir, file.filename)

        with open(temp_file_path, "wb") as temp_file:
            data = await file.read()  # Leer todo el contenido del archivo
            temp_file.write(data)  # Escribir los datos al archivo temporal
            print(f"Se escribieron {len(data)} bytes al archivo {file.filename}")


        # Mover el archivo temporal a un directorio permanente
        shutil.move(temp_file_path, os.path.join("../data", file.filename))


        return {"filename": file.filename, "path": temp_file_path}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)