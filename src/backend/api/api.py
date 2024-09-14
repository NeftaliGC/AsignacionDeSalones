from typing import Union, Annotated
from fastapi import FastAPI, File, UploadFile
import os
import shutil
import tempfile

app = FastAPI()

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
            shutil.copyfileobj(file.file, temp_file)

        return {"filename": file.filename}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)