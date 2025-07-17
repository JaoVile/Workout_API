## alembic/env.py
from __future__ import annotations

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Importações da nossa aplicação
from workout_api.configs.settings import settings
from workout_api.contrib.models import BaseModel

# Configuração base do Alembic
config = context.config

# --- LÓGICA INTELIGENTE DE HOST ---
# Pega o argumento '-x db_host=db' que passamos no comando 'docker compose run'
db_host_from_cmd = context.get_x_argument(as_dictionary=True).get('db_host')

if db_host_from_cmd:
    # Se o argumento existe, nós o usamos para sobrescrever o host nas configurações.
    # Isso faz com que a DATABASE_URL seja montada com o host 'db',
    # que é o nome correto dentro da rede Docker.
    settings.POSTGRES_HOST = db_host_from_cmd

# Configura a URL final no Alembic
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Configuração de logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Importa todos os modelos da aplicação para que o Alembic os reconheça
import workout_api.atleta.models
import workout_api.categorias.models
import workout_api.centro_treinamento.models

target_metadata = BaseModel.metadata

# Definição das funções de migração (offline e online)
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(
            lambda sync_conn: context.configure(
                connection=sync_conn, target_metadata=target_metadata
            )
        )
        async with connection.begin():
            await connection.run_sync(lambda _: context.run_migrations())

    await connectable.dispose()

# Bloco principal que decide se roda online ou offline
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())