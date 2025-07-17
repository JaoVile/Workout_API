# workout_api/contrib/models.py

import uuid
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

class BaseModel(DeclarativeBase):
    """
    Modelo base do qual todos os outros modelos herdarão.
    Fornece um 'id' UUID e um 'created_at' para todas as tabelas.
    """
    
    # --- CORREÇÃO AQUI ---
    # O 'id' é um identificador único universal, mas não a chave primária da tabela.
    # A chave primária será o 'pk_id' em cada modelo filho.
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid.uuid4, nullable=False, unique=True)
    
    # A coluna de data de criação.
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    # --- FIM DA CORREÇÃO ---