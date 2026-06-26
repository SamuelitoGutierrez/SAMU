# SAMU-GLOBAL KITS

Sistema para comités y administración con persistencia absoluta en VPS/Coolify.

## URLs

- http://85.31.62.90:3000/login
- http://85.31.62.90:3000/panel
- http://85.31.62.90:3000/health

## Documentación de despliegue

Ver **[COOLIFY.md](COOLIFY.md)** para volúmenes persistentes y variables de entorno.

## Stack

- Python 3.12 + Flask + Flask-WTF (CSRF)
- PostgreSQL (volumen `/data/postgres_data`)
- Tailwind CSS (CDN, mobile-first)
- Almacén PDF: `/data/storage/documents`

## Desarrollo local

```bash
pip install -r requirements.txt
# .env con DB_* y SECRET_KEY (mín. 32 chars) o ENTORNO=desarrollo
python main.py
```
