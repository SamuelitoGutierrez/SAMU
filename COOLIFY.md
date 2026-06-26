# SAMU-GLOBAL KITS — Despliegue Coolify (VPS 85.31.62.90)

## Error `ERR_CONNECTION_TIMED_OUT` — solución

Ese error significa que **nada responde en el puerto 3000**. Sigue estos pasos en Coolify:

### Paso 1 — Puerto expuesto en Coolify

En tu aplicación → **General** → **Ports**:

| Campo | Valor |
|-------|-------|
| **Ports Exposes** | `3000` |
| **Port Mappings** | `3000:3000` |

Guarda y haz **Redeploy**.

### Paso 2 — Comando de inicio (Build Pack / Docker)

Usa el **Dockerfile** del repo (incluye `start.sh` que lee `$PORT`):

```
# No cambies el CMD — el Dockerfile ya usa start.sh
```

Si usas **Custom Start Command**, pon:

```
/app/start.sh
```

**No uses** `python main.py` en producción.

### Paso 3 — Variables de entorno obligatorias

En Coolify → **Environment Variables**:

```
ENTORNO=produccion
PORT=3000
SECRET_KEY=pon_aqui_una_clave_larga_aleatoria_de_32_caracteres_minimo
DB_HOST=<nombre-interno-postgres-coolify>
DB_NAME=samu
DB_USER=postgres
DB_PASSWORD=tu_clave_postgres
DB_PORT=5432
PUBLIC_URL=http://85.31.62.90:3000
STORAGE_DOCUMENTS=/app/storage/documents
LOGIN_USER=admin
LOGIN_PASSWORD=tu_clave_admin
```

**`DB_HOST`**: en Coolify copia el **Internal URL / hostname** del servicio PostgreSQL (NO uses `localhost`).

### Paso 4 — Volúmenes persistentes

| Ruta en VPS | Montar en contenedor |
|-------------|----------------------|
| `/data/postgres_data` | `/var/lib/postgresql/data` (servicio Postgres) |
| `/data/storage/documents` | `/app/storage/documents` (app Flask) |

En el VPS (SSH):

```bash
sudo mkdir -p /data/postgres_data /data/storage/documents
```

### Paso 5 — Firewall del VPS

Abre el puerto 3000 si accedes por IP directa:

```bash
sudo ufw allow 3000/tcp
sudo ufw reload
```

### Paso 6 — Verificar logs en Coolify

Tras Redeploy, en **Logs** debe aparecer:

```
SAMU-GLOBAL KITS
Escuchando en 0.0.0.0:3000
```

Si ves error de Python al importar, revisa variables de entorno.

### Paso 7 — Probar

1. http://85.31.62.90:3000/ping → `{"ok": true}`
2. http://85.31.62.90:3000/health → `"db": true`
3. http://85.31.62.90:3000/login → pantalla de login

---

## Alternativa: URL de Coolify (sin puerto 3000)

Coolify puede dar una URL tipo `https://samu.tudominio.com` por proxy (puertos 80/443).
En ese caso usa esa URL en lugar de `:3000`.

Configura `PUBLIC_URL` con la URL real que uses.
