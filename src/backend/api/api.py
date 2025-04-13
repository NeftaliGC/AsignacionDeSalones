from typing import Union, Annotated
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import Response
import json
import uuid
import time
from pathlib import Path
from threading import Timer

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

sessions = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Lista de dominios permitidos, ajusta según necesites
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return FileResponse(str(frontend_path / "index.html"))

# Endpoint para servir archivos CSS y JS sin caché
@app.get("/static/{filename}")
async def get_static(filename: str):
    file_extension = filename.split(".")[-1]
    media_types = {
        "css": "text/css",
        "js": "application/javascript"
        
    }
    
    media_type = media_types.get(file_extension, "application/octet-stream")  # Si no es CSS/JS, usa octet-stream
    
    try:
        with open(f"../../frontend/{filename}", "rb") as file:
            content = file.read()
        return Response(content, media_type=media_type, headers={"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"})
    except FileNotFoundError:
        return Response("File not found", status_code=404)

@app.get("/start-session/")
def start_session():
    session_id = str(uuid.uuid4())
    sessions[session_id] = {'last_active': time.time(), 'input': []}
    return {"session_id": session_id}

@app.get("/get-sessions/")
def get_sessions():
    return sessions

@app.get("/end-session/")
def end_session(token: str = Header(None)):
    if token not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    del sessions[token]
    return {"message": "Session ended"}

@app.post("/add-data/")
def add_data(token: str = Header(...), data: dict = None):
    if token not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Revisar funcionalidad
    
    sessions[token]['input'].append(data)
    #sessions[token]['input'][0]['data'].append(data)
    sessions[token]['last_active'] = time.time()
    return {"message": "Data added"}

@app.post("/save-data/")
def save_data(token: str = Header(None)):
    if token not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    data = sessions[token]
    json_data = json.dumps(data)


    with open(f"../data/{token}.json", "w") as f:
        f.write(str(json_data))
        
    return {"message": "Data saved"}

@app.get("/solution/")
def solution(token: str = Header(None)):
    if token not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    sessions[token]['last_active'] = time.time()
    data = sessions[token]['input']

    # Aquí va el código de la solución


#########################################################
# Función para limpiar sesiones inactivas
def clear_inactive_sessions():
    current_time = time.time()
    inactive_sessions = [sid for sid, details in sessions.items()
                         if current_time - details['last_active'] > 30 * 60]  # 30 minutos

    for sid in inactive_sessions:
        del sessions[sid]
    
    # Configura el temporizador para que se ejecute cada 5 minutos
    Timer(5 * 60, clear_inactive_sessions).start()

# Inicia el temporizador de limpieza
clear_inactive_sessions()


#########################################################
# Obtener la ruta absoluta del directorio frontend
frontend_path = Path(__file__).resolve().parent.parent.parent / "frontend"

# Montar la carpeta frontend como estática
app.mount("/static", StaticFiles(directory=str(frontend_path)), name="frontend")