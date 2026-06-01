from contextlib import suppress
import json

from database import get_connection, release_connection


def _fetchall_dict(cursor):
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def asegurar_tablas_cuaderno():
    """Prepara tablas persistentes para que Coolify redeploy no borre datos."""
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS cuaderno_asientos (
                id SERIAL PRIMARY KEY,
                numero INTEGER NOT NULL UNIQUE,
                fecha DATE NOT NULL,
                estado VARCHAR(40) NOT NULL DEFAULT 'En redacción',
                avance INTEGER NOT NULL DEFAULT 0,
                firmado_por VARCHAR(160),
                firmado_en TIMESTAMP,
                contenido TEXT,
                created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMP NOT NULL DEFAULT NOW()
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS cuaderno_observaciones (
                id SERIAL PRIMARY KEY,
                asiento_numero INTEGER NOT NULL REFERENCES cuaderno_asientos(numero) ON DELETE CASCADE,
                autor VARCHAR(160) NOT NULL,
                texto TEXT NOT NULL,
                tipo VARCHAR(40) NOT NULL DEFAULT 'post-it',
                resuelto BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            )
            """
        )
        conn.commit()
        cur.close()
        return True
    except Exception:
        if conn:
            with suppress(Exception):
                conn.rollback()
        return False
    finally:
        if conn:
            release_connection(conn)


def obtener_panel_cuaderno():
    conectado = asegurar_tablas_cuaderno()
    datos = {
        "conectado": conectado,
        "estadisticas": {
            "total_asientos": 0,
            "dias_lluvia": 0,
            "consultas_pendientes": 0,
            "avance_porcentaje": 0,
            "ultimo_asiento": "-",
            "llenado_ultimo": 0,
            "firmados": 0,
            "observaciones": 0,
        },
        "asientos": [],
        "observaciones": [],
    }
    if not conectado:
        return datos

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                COUNT(*) AS total_asientos,
                COALESCE(ROUND(AVG(avance))::INTEGER, 0) AS avance_porcentaje,
                COALESCE(MAX(numero), 0) AS ultimo_asiento,
                COUNT(*) FILTER (WHERE estado = 'Firmado') AS firmados
            FROM cuaderno_asientos
            """
        )
        row = cur.fetchone()
        cur.execute("SELECT COUNT(*) FROM cuaderno_observaciones WHERE resuelto = FALSE")
        observaciones = cur.fetchone()[0]
        cur.execute(
            """
            SELECT numero, fecha::TEXT AS fecha, EXTRACT(DAY FROM fecha)::INTEGER AS dia,
                   estado, avance, COALESCE(firmado_por, '-') AS supervisor,
                   updated_at::TEXT AS updated_at
            FROM cuaderno_asientos
            ORDER BY fecha DESC, numero DESC
            LIMIT 31
            """
        )
        asientos = _fetchall_dict(cur)
        cur.execute(
            """
            SELECT o.asiento_numero AS numero, o.autor, o.texto, o.tipo, o.created_at
            FROM cuaderno_observaciones o
            WHERE o.resuelto = FALSE
            ORDER BY o.created_at DESC
            LIMIT 10
            """
        )
        obs = _fetchall_dict(cur)
        cur.close()

        ultimo = row[2] or 0
        llenado_ultimo = 0
        if ultimo:
            for asiento in asientos:
                if asiento["numero"] == ultimo:
                    llenado_ultimo = asiento["avance"]
                    break

        datos["estadisticas"] = {
            "total_asientos": row[0] or 0,
            "dias_lluvia": 0,
            "consultas_pendientes": observaciones or 0,
            "avance_porcentaje": row[1] or 0,
            "ultimo_asiento": ultimo or "-",
            "llenado_ultimo": llenado_ultimo or 0,
            "firmados": row[3] or 0,
            "observaciones": observaciones or 0,
        }
        datos["asientos"] = [
            {
                "dia": a["dia"],
                "fecha": a.get("fecha"),
                "numero": a["numero"],
                "estado": a["estado"],
                "avance": a["avance"],
                "supervisor": a["supervisor"],
                "updated_at": a.get("updated_at"),
                "observacion": "Con observaciones" if any(o["numero"] == a["numero"] for o in obs) else "Sin observaciones activas.",
            }
            for a in asientos
        ]
        datos["observaciones"] = obs
        return datos
    except Exception:
        return datos
    finally:
        if conn:
            release_connection(conn)


def guardar_asiento(numero, fecha, estado, avance, contenido, usuario=None):
    conectado = asegurar_tablas_cuaderno()
    if not conectado:
        return {"ok": False, "error": "Base de datos no conectada"}

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        contenido_texto = contenido if isinstance(contenido, str) else json.dumps(contenido, ensure_ascii=False)
        firmado_por = usuario if estado in ("Cerrado", "Firmado") else None
        cur.execute(
            """
            INSERT INTO cuaderno_asientos (numero, fecha, estado, avance, firmado_por, firmado_en, contenido, updated_at)
            VALUES (%s, %s, %s, %s, %s, CASE WHEN %s IN ('Cerrado', 'Firmado') THEN NOW() ELSE NULL END, %s, NOW())
            ON CONFLICT (numero) DO UPDATE SET
                fecha = EXCLUDED.fecha,
                estado = EXCLUDED.estado,
                avance = EXCLUDED.avance,
                firmado_por = COALESCE(EXCLUDED.firmado_por, cuaderno_asientos.firmado_por),
                firmado_en = CASE
                    WHEN EXCLUDED.estado IN ('Cerrado', 'Firmado') THEN NOW()
                    ELSE cuaderno_asientos.firmado_en
                END,
                contenido = EXCLUDED.contenido,
                updated_at = NOW()
            RETURNING numero, estado, avance
            """,
            (numero, fecha, estado, avance, firmado_por, estado, contenido_texto),
        )
        row = cur.fetchone()
        conn.commit()
        cur.close()
        return {"ok": True, "numero": row[0], "estado": row[1], "avance": row[2]}
    except Exception as exc:
        if conn:
            with suppress(Exception):
                conn.rollback()
        return {"ok": False, "error": str(exc)}
    finally:
        if conn:
            release_connection(conn)


def obtener_asiento(numero):
    if not asegurar_tablas_cuaderno():
        return None
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT numero, fecha::TEXT AS fecha, estado, avance, contenido
            FROM cuaderno_asientos
            WHERE numero = %s
            """,
            (numero,),
        )
        row = cur.fetchone()
        cur.close()
        if not row:
            return None
        return {"numero": row[0], "fecha": row[1], "estado": row[2], "avance": row[3], "contenido": row[4]}
    except Exception:
        return None
    finally:
        if conn:
            release_connection(conn)
