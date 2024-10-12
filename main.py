from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://pruebahackathon-eng3h2bbghfshwe9.centralus-01.azurewebsites.net/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulación de base de datos en memoria con datos iniciales
database = {
    1: {"id": 1, "name": "John", "lastname": "Doe", "age": 30},
    2: {"id": 2, "name": "Jane", "lastname": "Smith", "age": 25}
}

class User(BaseModel):
    id: int
    name: str
    lastname: str
    age: int = Field(..., gt=0, description="Edad debe ser un número positivo")

@app.post('/user/', response_model=User)
async def add_user(user: User):
    if user.name in [u["name"] for u in database.values()]:
        raise HTTPException(status_code=400, detail="El nombre ya está registrado")
    if user.id in database:
        raise HTTPException(status_code=400, detail="El ID ya está registrado")
    
    database[user.id] = user.dict()
    return user

@app.get('/user/{id}', response_model=User)
async def get_user_by_id(id: int):
    user = database.get(id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return User(**user)

@app.get('/userValidation/{name}/{lastname}', response_model=User)
async def get_user_by_name_lastname(name: str, lastname: str):
    user = next((u for u in database.values() if u["name"] == name and u["lastname"] == lastname), None)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return User(**user)

@app.put('/user/{name}', response_model=User)
async def update_user(name: str, user: User):
    existing_user_id = next((id for id, u in database.items() if u["name"] == name), None)
    if existing_user_id is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    database[existing_user_id] = user.dict()
    return user

@app.delete('/user/{id}', response_model=dict)
async def delete_user(id: int):
    if id not in database:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    del database[id]
    return {"detail": "Usuario eliminado con éxito"}