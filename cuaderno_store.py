from contextlib import suppress
from datetime import date
import json

from database import get_connection, release_connection


ESTADOS_BORRADOR = {"borrador", "en redacción", "en redaccion", "draft"}
ESTADOS_CERRADO = {"cerrado", "firmado", "closed", "vista previa y firmar"}


def normalizar_estado(estado):
    valor = str(estado or "").strip().lower()
    if valor in ESTADOS_CERRADO:
        return "Cerrado"
    if valor in ESTADOS_BORRADOR:
        return "Borrador"
    return "Borrador"


def normalizar_tipo(tipo):
    valor = str(tipo or "").strip().lower()
    if "super" in valor:
        return "Supervisor"
    return "Residente"


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
                tipo VARCHAR(40) NOT NULL DEFAULT 'Residente',
                estado VARCHAR(40) NOT NULL DEFAULT 'En redacción',
                avance INTEGER NOT NULL DEFAULT 0,
                bloqueado BOOLEAN NOT NULL DEFAULT FALSE,
                firmado_por VARCHAR(160),
                firmado_en TIMESTAMP,
                contenido TEXT,
                observaciones TEXT,
                created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMP NOT NULL DEFAULT NOW()
            )
            """
        )
        cur.execute("ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS tipo VARCHAR(40) NOT NULL DEFAULT 'Residente'")
        cur.execute("ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS bloqueado BOOLEAN NOT NULL DEFAULT FALSE")
        cur.execute("ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS observaciones TEXT")
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
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS cuaderno_logs (
                id SERIAL PRIMARY KEY,
                asiento_numero INTEGER,
                usuario VARCHAR(160) NOT NULL DEFAULT 'Sistema',
                accion VARCHAR(80) NOT NULL,
                detalle TEXT,
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


def _extraer_observaciones(contenido):
    if not isinstance(contenido, dict):
        return ""
    candidatos = [
        contenido.get("observaciones"),
        contenido.get("observacion"),
        contenido.get("ultima_observacion"),
    ]
    for modulo in contenido.get("modulos") or []:
        titulo = str(modulo.get("titulo", "")).lower() if isinstance(modulo, dict) else ""
        texto = modulo.get("contenido") if isinstance(modulo, dict) else ""
        if "ocurrencia" in titulo or "observ" in titulo or "supervisi" in titulo:
            candidatos.append(texto)
    return "\n".join(str(item).strip() for item in candidatos if str(item or "").strip())


def _registrar_log(cur, numero, usuario, accion, detalle=""):
    cur.execute(
        """
        INSERT INTO cuaderno_logs (asiento_numero, usuario, accion, detalle)
        VALUES (%s, %s, %s, %s)
        """,
        (numero, usuario or "Sistema", accion, detalle or ""),
    )


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
        "ultima_observacion": None,
        "historial": [],
        "mes_actual": {
            "cerrados": 0,
            "borradores": 0,
            "sin_registro": 0,
            "avance": 0,
        },
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
                COUNT(*) FILTER (WHERE estado IN ('Cerrado', 'Firmado')) AS firmados
            FROM cuaderno_asientos
            """
        )
        row = cur.fetchone()
        cur.execute("SELECT COUNT(*) FROM cuaderno_observaciones WHERE resuelto = FALSE")
        observaciones = cur.fetchone()[0]
        cur.execute(
            """
            SELECT
                COUNT(*) FILTER (WHERE estado IN ('Cerrado', 'Firmado')) AS cerrados,
                COUNT(*) FILTER (WHERE estado = 'Borrador') AS borradores,
                EXTRACT(DAY FROM (DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month - 1 day'))::INTEGER AS dias_mes
            FROM cuaderno_asientos
            WHERE fecha >= DATE_TRUNC('month', CURRENT_DATE)::DATE
              AND fecha < (DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month')::DATE
            """
        )
        mes_row = cur.fetchone()
        cur.execute(
            """
            SELECT numero, fecha::TEXT AS fecha, EXTRACT(DAY FROM fecha)::INTEGER AS dia,
                   estado, avance, COALESCE(firmado_por, '-') AS supervisor,
                   updated_at::TEXT AS updated_at, tipo, bloqueado,
                   COALESCE(observaciones, '') AS observaciones
            FROM cuaderno_asientos
            ORDER BY fecha DESC, numero DESC
            LIMIT 180
            """
        )
        asientos = _fetchall_dict(cur)
        cur.execute(
            """
            SELECT o.asiento_numero AS numero, o.autor, o.texto, o.tipo, o.created_at::TEXT AS created_at
            FROM cuaderno_observaciones o
            WHERE o.resuelto = FALSE
            ORDER BY o.created_at DESC
            LIMIT 10
            """
        )
        obs = _fetchall_dict(cur)
        cur.execute(
            """
            SELECT o.asiento_numero AS numero, o.autor, o.texto, o.tipo, o.created_at::TEXT AS created_at
            FROM cuaderno_observaciones o
            WHERE o.resuelto = FALSE
              AND (o.tipo = 'observacion-tecnica' OR LOWER(o.autor) LIKE '%supervisor%')
            ORDER BY o.created_at DESC
            LIMIT 1
            """
        )
        ultima_obs = cur.fetchone()
        cur.execute(
            """
            SELECT asiento_numero AS numero, usuario, accion, detalle, created_at::TEXT AS created_at
            FROM cuaderno_logs
            ORDER BY created_at DESC
            LIMIT 5
            """
        )
        historial = _fetchall_dict(cur)
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
                "tipo": a.get("tipo"),
                "bloqueado": a.get("bloqueado"),
                "observacion": "Con observaciones" if any(o["numero"] == a["numero"] for o in obs) else "Sin observaciones activas.",
            }
            for a in asientos
        ]
        datos["observaciones"] = obs
        if ultima_obs:
            datos["ultima_observacion"] = {
                "numero": ultima_obs[0],
                "autor": ultima_obs[1],
                "texto": ultima_obs[2],
                "tipo": ultima_obs[3],
                "created_at": ultima_obs[4],
            }
        datos["historial"] = historial
        cerrados_mes = mes_row[0] or 0
        borradores_mes = mes_row[1] or 0
        dias_mes = mes_row[2] or 30
        sin_registro = max(0, dias_mes - cerrados_mes - borradores_mes)
        datos["mes_actual"] = {
            "cerrados": cerrados_mes,
            "borradores": borradores_mes,
            "sin_registro": sin_registro,
            "avance": round((cerrados_mes / dias_mes) * 100) if dias_mes else 0,
        }
        return datos
    except Exception:
        return datos
    finally:
        if conn:
            release_connection(conn)


def guardar_asiento(numero, fecha, estado, avance, contenido, usuario=None, tipo="Residente", puede_editar_cerrado=False):
    conectado = asegurar_tablas_cuaderno()
    if not conectado:
        return {"ok": False, "error": "Base de datos no conectada"}

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        estado_normalizado = normalizar_estado(estado)
        tipo_normalizado = normalizar_tipo(tipo)
        contenido_texto = contenido if isinstance(contenido, str) else json.dumps(contenido, ensure_ascii=False)
        observaciones = _extraer_observaciones(contenido)
        bloqueado = estado_normalizado == "Cerrado"
        firmado_por = usuario if bloqueado else None
        cur.execute(
            """
            SELECT estado, bloqueado
            FROM cuaderno_asientos
            WHERE numero = %s
            """,
            (numero,),
        )
        existente = cur.fetchone()
        if existente and (existente[0] in ("Cerrado", "Firmado") or existente[1]) and not puede_editar_cerrado:
            cur.close()
            conn.rollback()
            return {"ok": False, "error": "El asiento está cerrado y bloqueado. Solo Admin puede editarlo."}

        cur.execute(
            """
            INSERT INTO cuaderno_asientos (numero, fecha, tipo, estado, avance, bloqueado, firmado_por, firmado_en, contenido, observaciones, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, CASE WHEN %s = 'Cerrado' THEN NOW() ELSE NULL END, %s, %s, NOW())
            ON CONFLICT (numero) DO UPDATE SET
                fecha = EXCLUDED.fecha,
                tipo = EXCLUDED.tipo,
                estado = EXCLUDED.estado,
                avance = EXCLUDED.avance,
                bloqueado = EXCLUDED.bloqueado,
                firmado_por = COALESCE(EXCLUDED.firmado_por, cuaderno_asientos.firmado_por),
                firmado_en = CASE
                    WHEN EXCLUDED.estado = 'Cerrado' THEN NOW()
                    ELSE cuaderno_asientos.firmado_en
                END,
                contenido = EXCLUDED.contenido,
                observaciones = EXCLUDED.observaciones,
                updated_at = NOW()
            RETURNING numero, estado, avance, tipo, bloqueado
            """,
            (
                numero,
                fecha,
                tipo_normalizado,
                estado_normalizado,
                avance,
                bloqueado,
                firmado_por,
                estado_normalizado,
                contenido_texto,
                observaciones,
            ),
        )
        row = cur.fetchone()
        accion = "cerró y bloqueó" if estado_normalizado == "Cerrado" else "guardó borrador"
        _registrar_log(
            cur,
            numero,
            usuario,
            accion,
            f"{tipo_normalizado} {accion} el asiento N° {str(numero).zfill(3)}.",
        )
        if tipo_normalizado == "Supervisor" and observaciones:
            cur.execute(
                """
                INSERT INTO cuaderno_observaciones (asiento_numero, autor, texto, tipo, resuelto)
                VALUES (%s, %s, %s, 'observacion-tecnica', FALSE)
                """,
                (numero, usuario or "Supervisor", observaciones),
            )
        conn.commit()
        cur.close()
        return {"ok": True, "numero": row[0], "estado": row[1], "avance": row[2], "tipo": row[3], "bloqueado": row[4]}
    except Exception as exc:
        if conn:
            with suppress(Exception):
                conn.rollback()
        return {"ok": False, "error": str(exc)}
    finally:
        if conn:
            release_connection(conn)


def obtener_datos_mes_cuaderno(year=None, month=None):
    conectado = asegurar_tablas_cuaderno()
    if not conectado:
        return {"ok": False, "error": "Base de datos no conectada", "asientos": [], "estadisticas": {}}

    hoy = date.today()
    year = int(year or hoy.year)
    month = int(month or hoy.month)
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT numero, fecha::TEXT AS fecha, EXTRACT(DAY FROM fecha)::INTEGER AS dia,
                   estado, avance, COALESCE(firmado_por, '-') AS supervisor,
                   updated_at::TEXT AS updated_at, tipo, bloqueado,
                   COALESCE(observaciones, '') AS observaciones
            FROM cuaderno_asientos
            WHERE EXTRACT(YEAR FROM fecha)::INTEGER = %s
              AND EXTRACT(MONTH FROM fecha)::INTEGER = %s
            ORDER BY fecha ASC, numero ASC
            """,
            (year, month),
        )
        asientos = _fetchall_dict(cur)
        cur.execute(
            """
            SELECT
                COUNT(*) FILTER (WHERE estado IN ('Cerrado', 'Firmado')) AS cerrados,
                COUNT(*) FILTER (WHERE estado = 'Borrador') AS borradores,
                EXTRACT(DAY FROM ((DATE_TRUNC('month', MAKE_DATE(%s, %s, 1)) + INTERVAL '1 month - 1 day')))::INTEGER AS dias_mes
            FROM cuaderno_asientos
            WHERE EXTRACT(YEAR FROM fecha)::INTEGER = %s
              AND EXTRACT(MONTH FROM fecha)::INTEGER = %s
            """,
            (year, month, year, month),
        )
        row = cur.fetchone()
        cur.close()
        cerrados = row[0] or 0
        borradores = row[1] or 0
        dias_mes = row[2] or 30
        sin_registro = max(0, dias_mes - cerrados - borradores)
        return {
            "ok": True,
            "asientos": [
                {
                    "dia": a["dia"],
                    "fecha": a.get("fecha"),
                    "numero": a["numero"],
                    "estado": a["estado"],
                    "avance": a["avance"],
                    "supervisor": a["supervisor"],
                    "updated_at": a.get("updated_at"),
                    "tipo": a.get("tipo"),
                    "bloqueado": a.get("bloqueado"),
                    "observacion": a.get("observaciones") or "Sin observaciones activas.",
                }
                for a in asientos
            ],
            "estadisticas": {
                "cerrados": cerrados,
                "borradores": borradores,
                "sin_registro": sin_registro,
                "avance": round((cerrados / dias_mes) * 100) if dias_mes else 0,
                "dias_mes": dias_mes,
            },
        }
    except Exception as exc:
        return {"ok": False, "error": str(exc), "asientos": [], "estadisticas": {}}
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
            SELECT numero, fecha::TEXT AS fecha, tipo, estado, avance, bloqueado,
                   contenido, COALESCE(observaciones, '') AS observaciones
            FROM cuaderno_asientos
            WHERE numero = %s
            """,
            (numero,),
        )
        row = cur.fetchone()
        cur.close()
        if not row:
            return None
        return {
            "numero": row[0],
            "fecha": row[1],
            "tipo": row[2],
            "estado": row[3],
            "avance": row[4],
            "bloqueado": row[5],
            "contenido": row[6],
            "observaciones": row[7],
        }
    except Exception:
        return None
    finally:
        if conn:
            release_connection(conn)
