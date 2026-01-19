# Estágio 1: Builder
FROM python:3.14-slim AS builder

WORKDIR /install
COPY requirements.txt .

# A instalação e limpeza em um único comando evita camadas desnecessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt \
    && apt-get purge -y --auto-remove gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Estágio 2: Imagem Final
FROM python:3.14-slim

# Instala o runtime do FFmpeg
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Força a saída de logs em tempo real (resolve seu problema anterior)
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Copia as dependências limpas
COPY --from=builder /install /usr/local

# Copia os arquivos do projeto
COPY src/ ./src/
COPY Modelos/ ./Modelos/

# Configurações de ambiente
ENV PYTHONPATH="/app/src"
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT=7860

EXPOSE 7860

# Garante que não existam arquivos .pyc antigos vindos da cópia
RUN find . -type d -name "__pycache__" -exec rm -rf {} +

CMD ["python", "src/Gradio_Interface.py"]