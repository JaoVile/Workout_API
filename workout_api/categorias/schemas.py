# workout_api/categorias/schemas.py
from typing import Annotated
from pydantic import Field
from workout_api.contrib.schemas import BaseSchema, OutMixin

class Categoria(BaseSchema):
    # CORREÇÃO: Aumentamos o tamanho máximo do nome para 50
    nome: Annotated[str, Field(description='Nome da categoria', example='Scale', max_length=50)]

class CategoriaIn(Categoria):
    pass

class CategoriaOut(Categoria, OutMixin):
    pass