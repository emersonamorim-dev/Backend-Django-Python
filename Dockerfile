# Usar a imagem oficial do Python 3.9 como ponto de partida
FROM python:3.9

# Definir variáveis de ambiente para as chaves do PayPal
ENV PAYPAL_MODE="sandbox"
ENV PAYPAL_CLIENT_ID="sua_client_id"
ENV PAYPAL_CLIENT_SECRET="seu_client_secret"

# Criar um diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar o código-fonte para o diretório de trabalho
COPY . .

# Instalar as dependências do Python
RUN pip install -r requirements.txt

# Expor a porta 8000
EXPOSE 8000

# Definir o comando a ser executado quando o contêiner for iniciado
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
