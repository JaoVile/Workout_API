# workout_api/atleta/controller.py

from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, status, HTTPException, Query
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate, AtletaListOut
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel

from fastapi_pagination import LimitOffsetPage, paginate

router = APIRouter()

@router.post(
    '/',
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(
    db_session: DatabaseDependency,
    atleta_in: AtletaIn = Body(...)
):
    categoria_nome = atleta_in.categoria.nome
    ct_nome = atleta_in.centro_treinamento.nome

    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=categoria_nome))).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'A categoria {categoria_nome} não foi encontrada.')

    centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=ct_nome))).scalars().first()
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'O centro de treinamento {ct_nome} não foi encontrado.')

    try:
        # A lógica correta: cria o modelo, associa as FKs e salva.
        atleta_model = AtletaModel(**atleta_in.model_dump(exclude={'categoria', 'centro_treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        
        db_session.add(atleta_model)
        await db_session.commit()
        await db_session.refresh(atleta_model) # A linha da vitória!
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}")
    
    return atleta_model

@router.get(
    '/',
    summary='Consultar todos os Atletas',
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[AtletaListOut],
)
async def query(
    db_session: DatabaseDependency,
    nome: str = Query(None, description="Filtrar por nome do atleta"),
    cpf: str = Query(None, description="Filtrar por CPF do atleta")
) -> LimitOffsetPage[AtletaListOut]:
    
    # Esta query já estava correta para o desafio
    stmt = select(
        AtletaModel.nome, 
        CategoriaModel.nome.label('categoria'), 
        CentroTreinamentoModel.nome.label('centro_treinamento')
    ).join(CategoriaModel, AtletaModel.categoria_id == CategoriaModel.pk_id
    ).join(CentroTreinamentoModel, AtletaModel.centro_treinamento_id == CentroTreinamentoModel.pk_id)

    if nome:
        stmt = stmt.where(AtletaModel.nome == nome)
    if cpf:
        stmt = stmt.where(AtletaModel.cpf == cpf)

    return await paginate(db_session, stmt)


@router.get(
    '/{id}',
    summary='Consulta um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaModel | None = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id: {id}')

    return atleta


@router.patch(
    '/{id}',
    summary='Editar um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def patch(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaModel | None = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id: {id}')
    
    atleta_update_data = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update_data.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta


@router.delete(
    '/{id}',
    summary='Deletar um Atleta pelo id',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    atleta: AtletaModel | None = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta não encontrado no id: {id}')
    
    await db_session.delete(atleta)
    await db_session.commit()