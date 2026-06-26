#!/bin/sh
# Arranque SAMU-GLOBAL KITS — respeta PORT de Coolify
set -e

PORT="${PORT:-3000}"
WORKERS="${GUNICORN_WORKERS:-2}"

echo "=============================================="
echo " SAMU-GLOBAL KITS"
echo " Escuchando en 0.0.0.0:${PORT}"
echo "=============================================="

exec gunicorn \
  --workers "${WORKERS}" \
  --bind "0.0.0.0:${PORT}" \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  --capture-output \
  main:app
