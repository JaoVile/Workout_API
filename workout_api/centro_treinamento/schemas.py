# workout_api/centro_treinamento/schemas.py
from typing import Annotated
from pydantic import Field
from workout_api.contrib.schemas import BaseSchema, OutMixin

class CentroTreinamento(BaseSchema):
    # Aumentando o max_length para consistência
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT King', max_length=50)]
    endereco: Annotated[str, Field(description='Endereço do centro de treinamento', example='Rua X, Qdr 2', max_length=60)]
    proprietario: Annotated[str, Field(description='Proprietário do centro de treinamento', example='Marcos', max_length=30)]

class CentroTreinamentoIn(CentroTreinamento):
    pass

class CentroTreinamentoOut(CentroTreinamento, OutMixin):
    pass

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT King', max_length=50)]