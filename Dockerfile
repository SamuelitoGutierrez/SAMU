FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STORAGE_DOCUMENTS=/app/storage/documents

RUN mkdir -p /app/storage/documents/cotizaciones \
             /app/storage/documents/boletas \
             /app/storage/documents/anexos

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:3000", "--timeout", "120", "main:app"]
