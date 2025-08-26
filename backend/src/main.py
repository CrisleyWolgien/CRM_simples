# src/main.py

from fastapi import FastAPI
from src.routers import users  # Importe o novo router de usuários

app = FastAPI(
    title="CRM para Mecânicas",
    description="API para gerenciamento de clientes, veículos e serviços.",
)


@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao CRM para Mecânicas!"}


# Inclui as rotas na sua aplicação
app.include_router(users.router)  # Adiciona as rotas de usuário
