from typing import Union, Annotated
from fastapi import FastAPI, Header, HTTPException
import json
import uuid
import time
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
def root():
    return {"Asignacion" : "Salones"}

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
