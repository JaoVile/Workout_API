# workout_api/categorias/controller.py
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut
from workout_api.categorias.models import CategoriaModel
from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post(
    '/',
    summary='Criar uma nova Categoria',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def post(
    db_session: DatabaseDependency, 
    categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:
    try:
        categoria_model = CategoriaModel(**categoria_in.model_dump())
        db_session.add(categoria_model)
        await db_session.commit()
        await db_session.refresh(categoria_model)
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe uma categoria cadastrada com o nome: {categoria_in.nome}"
        )
    
    # CONSTRUÇÃO MANUAL: Garante que o objeto de resposta é criado corretamente.
    return CategoriaOut(
        id=categoria_model.id,
        nome=categoria_model.nome,
        created_at=categoria_model.created_at
    )


@router.get(
    '/', 
    summary='Consultar todas as Categorias',
    status_code=status.HTTP_200_OK,
    response_model=list[CategoriaOut],
)
async def query(db_session: DatabaseDependency) -> list[CategoriaOut]:
    categorias_db: list[CategoriaModel] = (await db_session.execute(select(CategoriaModel))).scalars().all()
    
    # CONSTRUÇÃO MANUAL: Garante que cada item da lista é convertido corretamente.
    return [
        CategoriaOut(id=cat.id, nome=cat.nome, created_at=cat.created_at) 
        for cat in categorias_db
    ]


@router.get(
    '/{id}', 
    summary='Consulta uma Categoria pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> CategoriaOut:
    categoria: CategoriaModel | None = (
        await db_session.execute(select(CategoriaModel).filter_by(id=id))
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Categoria não encontrada no id: {id}'
        )
    
    # CONSTRUÇÃO MANUAL: Garante que o objeto de resposta é criado corretamente.
    return CategoriaOut(
        id=categoria.id,
        nome=categoria.nome,
        created_at=categoria.created_at
    )