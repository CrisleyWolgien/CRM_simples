# src/main.py

from fastapi import FastAPI
from src.routers import (
    users,
    login,
    clients,
    vehicles,
    services,
    scheduling,
)  # Importe o router de agendamentos

app = FastAPI(
    title="CRM para Mecânicas",
    description="API para gerenciamento de clientes, veículos e serviços.",
)


@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao CRM para Mecânicas!"}


# Inclui as rotas na sua aplicação
app.include_router(login.router)
app.include_router(users.router)
app.include_router(clients.router)
app.include_router(vehicles.router)
app.include_router(services.router)
app.include_router(scheduling.router)
