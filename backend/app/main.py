# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.controllers import formulario_controller, resposta_controller

app = FastAPI(title="SENAI-Saúde API", version="0.1.0")

# ajuste conforme front
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"mensagem": "API SENAI Saúde rodando!"}

# Rotas
app.include_router(formulario_controller.router)
app.include_router(resposta_controller.router)
