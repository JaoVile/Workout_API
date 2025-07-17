# Etapa 1: Usar uma imagem base oficial do Python
FROM python:3.11-slim

# Etapa 2: Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Etapa 3: Copiar o arquivo de dependências para o contêiner
COPY requirements.txt .

# Etapa 4: Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 5: Copiar todo o código do projeto para o contêiner
COPY . .

# Etapa 6: Expor a porta 8000 para que possamos acessá-la de fora
EXPOSE 8000