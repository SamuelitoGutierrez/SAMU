from contextlib import suppress

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
            SELECT numero, EXTRACT(DAY FROM fecha)::INTEGER AS dia, estado, avance,
                   COALESCE(firmado_por, '-') AS supervisor
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
                "numero": a["numero"],
                "estado": a["estado"],
                "avance": a["avance"],
                "supervisor": a["supervisor"],
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
