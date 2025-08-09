FROM python:3.11-slim

# deps de compilação e postgres + utilitário dos2unix p/ CRLF
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev curl dos2unix \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# deps Python
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# código e entrypoint
COPY backend /app/backend
COPY backend/entrypoint.sh /entrypoint.sh

# remove CRLF e BOM e marca como executável
RUN sed -i 's/\r$//' /entrypoint.sh \
 && sed -i '1s/^\xEF\xBB\xBF//' /entrypoint.sh \
 && chmod +x /entrypoint.sh

# IMPORTANTE: executa via /bin/sh (ignora shebang do arquivo)
ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]
