# workout_api/main.py

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from workout_api.routers import api_router

# --- INÍCIO DO CÓDIGO ADICIONADO ---
# Importações necessárias para criar as tabelas
from workout_api.contrib.models import BaseModel
from workout_api.configs.database import engine

# Função assíncrona para criar as tabelas
async def create_tables():
    print("INFO:     Criando tabelas no banco de dados...")
    async with engine.begin() as conn:
        # O comando 'create_all' cria as tabelas se elas não existirem.
        await conn.run_sync(BaseModel.metadata.create_all)
    print("INFO:     Tabelas criadas com sucesso.")

app = FastAPI(title='WorkoutApi')

# Evento de inicialização: roda a função create_tables quando a API inicia.
@app.on_event("startup")
async def on_startup():
    await create_tables()
# --- FIM DO CÓDIGO ADICIONADO ---

# Inclui os routers da sua API
app.include_router(api_router)

# Adiciona o suporte para paginação
add_pagination(app)
