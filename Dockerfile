FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=3000 \
    STORAGE_DOCUMENTS=/app/storage/documents

RUN mkdir -p /app/storage/documents/cotizaciones \
             /app/storage/documents/boletas \
             /app/storage/documents/anexos

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x /app/start.sh

EXPOSE 3000

# Coolify inyecta PORT — start.sh lo usa automáticamente
CMD ["/app/start.sh"]
