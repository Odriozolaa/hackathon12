from fastapi import FastAPI
from .database import engine
from .models import Base
from .routers import auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth")

@app.get("/")
def read_root():
    return {"Hello": "World"}