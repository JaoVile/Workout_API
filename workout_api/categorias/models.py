from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from workout_api.contrib.models import BaseModel

# --- INÍCIO DA CORREÇÃO ---
# O caminho de importação foi corrigido, removendo a duplicação de "workout_api".
from workout_api.atleta.models import AtletaModel
# --- FIM DA CORREÇÃO ---


class CategoriaModel(BaseModel):
    __tablename__ = 'categorias'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    atleta: Mapped['AtletaModel'] = relationship(back_populates="categoria")
