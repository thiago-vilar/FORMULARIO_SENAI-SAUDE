#!/bin/sh
set -e

# ===== 0) Echo rápido p/ debug =====
echo "[entrypoint] Iniciando..."

# ===== 1) Monta a DATABASE_URL para Alembic e app =====
: "${POSTGRES_HOST:=db}"
: "${POSTGRES_PORT:=5432}"
: "${POSTGRES_USER:=postgres}"
: "${POSTGRES_PASSWORD:=postgres}"
: "${POSTGRES_DB:=formulariosenai}"

export DATABASE_URL="postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
echo "[entrypoint] DATABASE_URL=${DATABASE_URL}"

# ===== 2) Espera Postgres responder =====
echo "[entrypoint] Aguardando Postgres em ${POSTGRES_HOST}:${POSTGRES_PORT} ..."
python - <<'PY'
import os, time, psycopg2
host=os.environ["POSTGRES_HOST"]
port=int(os.environ["POSTGRES_PORT"])
user=os.environ["POSTGRES_USER"]
pwd=os.environ["POSTGRES_PASSWORD"]
db=os.environ["POSTGRES_DB"]

for i in range(60):
    try:
        conn = psycopg2.connect(host=host, port=port, user=user, password=pwd, dbname=db)
        conn.close()
        print("[entrypoint] Postgres OK")
        break
    except Exception:
        time.sleep(1)
else:
    raise SystemExit("[entrypoint] Postgres não respondeu em 60s")
PY

# ===== 3) Rodar migrations Alembic =====
cd /app/backend
if [ -f "alembic.ini" ]; then
  echo "[entrypoint] Rodando alembic upgrade head..."
  alembic upgrade head || { echo "[entrypoint] Alembic falhou"; exit 1; }
else
  echo "[entrypoint] ATENÇÃO: backend/alembic.ini não encontrado; pulando migrations."
fi

# ===== 4) Sobe a API =====
cd /app
echo "[entrypoint] Subindo API em 0.0.0.0:8000 (uvicorn backend.app.main:app)"
exec uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
