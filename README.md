# 🏋️ WorkoutAPI

[![CI](https://github.com/JaoVile/Workout_API/actions/workflows/ci.yml/badge.svg)](https://github.com/JaoVile/Workout_API/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.12-3776ab?logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-async-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

API REST **assíncrona** de gestão de competição de crossfit — atletas, categorias e centros de treinamento. Construída com **FastAPI + SQLAlchemy async + PostgreSQL**, com migrations versionadas (Alembic), paginação, query params de busca e tratamento de exceções de integridade.

> Projeto originalmente proposto pela [Digital Innovation One](https://dio.me) e estendido com filtros, paginação, customização de respostas e uma suíte de testes com CI.

## Modelagem de entidade e relacionamento - MER
![MER](/mer.jpg "Modelagem de entidade e relacionamento")

## Stack da API

A API foi desenvolvida utilizando o `fastapi` (async), junto das seguintes libs: `alembic`, `SQLAlchemy`, `pydantic`. Para salvar os dados está sendo utilizando o `postgres`, por meio do `docker`.

## Execução da API

Para executar o projeto, utilizei a [pyenv](https://github.com/pyenv/pyenv), com a versão 3.11.4 do `python` para o ambiente virtual.

Caso opte por usar pyenv, após instalar, execute:

```bash
pyenv virtualenv 3.11.4 workoutapi
pyenv activate workoutapi
pip install -r requirements.txt
```
Para subir o banco de dados, caso não tenha o [docker-compose](https://docs.docker.com/compose/install/linux/) instalado, faça a instalação e logo em seguida, execute:

```bash
make run-docker
```
Para criar uma migration nova, execute:

```bash
make create-migrations d="nome_da_migration"
```

Para criar o banco de dados, execute:

```bash
make run-migrations
```

## API

Para subir a API, execute:
```bash
make run
```
e acesse: http://127.0.0.1:8000/docs

# Desafio Final
    - adicionar query parameters nos endpoints
        - atleta
            - nome
            - cpf
    - customizar response de retorno de endpoints
        - get all
            - atleta
                - nome
                - centro_treinamento
                - categoria
    - Manipular exceção de integridade dos dados em cada módulo/tabela
        - sqlalchemy.exc.IntegrityError e devolver a seguinte mensagem: “Já existe um atleta cadastrado com o cpf: x”
        - status_code: 303
    - Adicionar paginação utilizando a lib: fastapi-pagination
        - limit e offset
## Testes

Os testes de schema validam o contrato dos modelos Pydantic (tamanho de campo,
valores positivos, campos obrigatórios e proibição de campos extras) sem precisar
de banco — rápidos e determinísticos. Rodam automaticamente no CI a cada push.

```bash
pip install -r requirements-dev.txt
pytest
```

# Referências

FastAPI: https://fastapi.tiangolo.com/

Pydantic: https://docs.pydantic.dev/latest/

SQLAlchemy: https://docs.sqlalchemy.org/en/20/

Alembic: https://alembic.sqlalchemy.org/en/latest/

Fastapi-pagination: https://uriyyo-fastapi-pagination.netlify.app/