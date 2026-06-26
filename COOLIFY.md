# SAMU-GLOBAL KITS — Persistencia en Coolify / VPS

Servidor: **http://85.31.62.90:3000/**

## 1. Volúmenes obligatorios (anti-borrado en Restart / Redeploy)

En el VPS, crea las carpetas **antes** del primer despliegue:

```bash
sudo mkdir -p /data/postgres_data
sudo mkdir -p /data/storage/documents/cotizaciones
sudo mkdir -p /data/storage/documents/boletas
sudo mkdir -p /data/storage/documents/anexos
sudo chown -R 999:999 /data/postgres_data
sudo chown -R 1000:1000 /data/storage/documents
```

### Opción A — docker-compose (recomendado)

```bash
docker compose up -d --build
```

El archivo `docker-compose.yml` ya mapea:

| Host (VPS) | Contenedor | Contenido |
|------------|------------|-----------|
| `/data/postgres_data` | `/var/lib/postgresql/data` | Base de datos PostgreSQL |
| `/data/storage/documents` | `/app/storage/documents` | PDF, cotizaciones, boletas |

### Opción B — Coolify UI (servicio manual)

En **Storages / Volumes** del proyecto:

1. **PostgreSQL**: montar `/data/postgres_data` → `/var/lib/postgresql/data`
2. **App Flask**: montar `/data/storage/documents` → `/app/storage/documents`

Sin estos volúmenes, un Redeploy **borra** usuarios, inventario y archivos.

## 2. Variables de entorno en Coolify

```
ENTORNO=produccion
SECRET_KEY=<mínimo 32 caracteres aleatorios>
DB_HOST=postgres
DB_NAME=samu
DB_USER=postgres
DB_PASSWORD=<tu_clave>
DB_PORT=5432
PUBLIC_URL=http://85.31.62.90:3000
STORAGE_DOCUMENTS=/app/storage/documents
LOGIN_USER=admin
LOGIN_PASSWORD=<clave_segura>
FLASK_DEBUG=0
PORT=3000
```

## 3. Comando de arranque

```
gunicorn -w 2 -b 0.0.0.0:3000 --timeout 120 main:app
```

## 4. Comprobar salud

```
GET http://85.31.62.90:3000/health
```

Respuesta esperada:

```json
{"ok": true, "app": "SAMU-GLOBAL KITS", "db": true, "storage": "/app/storage/documents"}
```

## 5. Seguridad implementada

- CSRF en formularios (Flask-WTF)
- `SECRET_KEY` obligatoria en producción
- Contraseñas con hash **scrypt** (Werkzeug)
- Cookies de sesión `HttpOnly` + `SameSite=Lax`
- Documentos fuera del contenedor en volumen persistente
