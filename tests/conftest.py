"""
Fixtures e bootstrap dos testes.

As configurações da app (workout_api.configs.settings.Settings) são instanciadas
no import e exigem as variáveis POSTGRES_*. Definimos valores fake aqui — antes
de qualquer import da aplicação — para que os testes de schema e de wiring rodem
sem um banco de verdade. O engine do SQLAlchemy é preguiçoso: criá-lo não abre
conexão; nenhum teste aqui executa query.
"""

import os

os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("POSTGRES_PORT", "5432")
os.environ.setdefault("POSTGRES_USER", "test")
os.environ.setdefault("POSTGRES_PASSWORD", "test")
os.environ.setdefault("POSTGRES_DB", "workout_test")
