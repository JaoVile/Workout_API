# workout_api/configs/settings.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Carrega as configurações da aplicação a partir de variáveis de ambiente
    ou de um arquivo .env. A padronização dos nomes é POSTGRES_*.
    """
    
    # Estes campos são obrigatórios. O Pydantic vai procurar por variáveis
    # de ambiente com estes nomes.
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def DATABASE_URL(self) -> str:
        """
        Monta a URL de conexão com o banco de dados dinamicamente a partir
        das outras configurações.
        """
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        # Pede para o pydantic ler o arquivo .env, se ele existir,
        # para carregar as variáveis de ambiente para o desenvolvimento local.
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Cria uma instância única e global das configurações que será
# importada em outras partes da aplicação.
settings = Settings()