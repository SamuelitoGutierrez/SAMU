from contextlib import suppress
from datetime import date, datetime, timedelta
import json

from database import get_connection, release_connection


ESTADOS_BORRADOR = {"borrador", "en redacción", "en redaccion", "draft"}
ESTADOS_CERRADO = {"cerrado", "firmado", "closed", "vista previa y firmar"}
ESTADOS_ENVIADO_INSPECTOR = {"enviado_inspector", "enviado inspector", "enviar a inspector", "enviado al inspector"}


def normalizar_estado(estado):
    valor = str(estado or "").strip().lower()
    if valor in ESTADOS_ENVIADO_INSPECTOR:
        return "Enviado Inspector"
    if valor in ESTADOS_CERRADO:
        return "Cerrado"
    if valor in ESTADOS_BORRADOR:
        return "Borrador"
    return "Borrador"


def normalizar_tipo(tipo):
    valor = str(tipo or "").strip().lower()
    if "inspector" in valor:
        return "Inspector"
    if "super" in valor:
        return "Inspector"
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
        cur.execute("ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS estado VARCHAR(40) NOT NULL DEFAULT 'Borrador'")
        cur.execute("ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS avance INTEGER NOT NULL DEFAULT 0")
        cur.execute("ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS bloqueado BOOLEAN NOT NULL DEFAULT FALSE")
        cur.execute("ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS firmado_por VARCHAR(160)")
        cur.execute("ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS firmado_en TIMESTAMP")
        cur.execute("ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS contenido TEXT")
        cur.execute("ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS observaciones TEXT")
        cur.execute("ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS personal_gastos_generales JSONB NOT NULL DEFAULT '[]'::jsonb")
        cur.execute("ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT NOW()")
        cur.execute("ALTER TABLE cuaderno_asientos ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NOT NULL DEFAULT NOW()")
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
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS cuaderno_inspector_asientos (
                id SERIAL PRIMARY KEY,
                numero INTEGER,
                residencia_numero INTEGER,
                fecha DATE NOT NULL,
                estado VARCHAR(40) NOT NULL DEFAULT 'borrador_inspector',
                contenido TEXT,
                firmado_por VARCHAR(160),
                firmado_en TIMESTAMP,
                created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
                UNIQUE (fecha)
            )
            """
        )
        cur.execute("ALTER TABLE cuaderno_inspector_asientos ADD COLUMN IF NOT EXISTS numero INTEGER")
        cur.execute("ALTER TABLE cuaderno_inspector_asientos ADD COLUMN IF NOT EXISTS residencia_numero INTEGER")
        cur.execute("ALTER TABLE cuaderno_inspector_asientos ALTER COLUMN residencia_numero DROP NOT NULL")
        cur.execute("ALTER TABLE cuaderno_inspector_asientos ADD COLUMN IF NOT EXISTS personal_supervision JSONB NOT NULL DEFAULT '[]'::jsonb")
        cur.execute("ALTER TABLE cuaderno_inspector_asientos ADD COLUMN IF NOT EXISTS partidas_ejecutadas TEXT")
        cur.execute("ALTER TABLE cuaderno_inspector_asientos ADD COLUMN IF NOT EXISTS almacen_ingreso TEXT")
        cur.execute("ALTER TABLE cuaderno_inspector_asientos ADD COLUMN IF NOT EXISTS almacen_salida TEXT")
        cur.execute("ALTER TABLE cuaderno_inspector_asientos ADD COLUMN IF NOT EXISTS maquinaria TEXT")
        cur.execute("ALTER TABLE cuaderno_inspector_asientos ADD COLUMN IF NOT EXISTS ocurrencias TEXT")
        cur.execute("ALTER TABLE cuaderno_inspector_asientos ALTER COLUMN estado SET DEFAULT 'borrador_inspector'")
        cur.execute(
            """
            DO $$
            DECLARE r RECORD;
            BEGIN
                FOR r IN
                    SELECT conname
                    FROM pg_constraint
                    WHERE conrelid = 'cuaderno_inspector_asientos'::regclass
                      AND contype IN ('f', 'u')
                      AND pg_get_constraintdef(oid) ILIKE '%residencia_numero%'
                LOOP
                    EXECUTE 'ALTER TABLE cuaderno_inspector_asientos DROP CONSTRAINT IF EXISTS ' || quote_ident(r.conname);
                END LOOP;
            END $$;
            """
        )
        cur.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_cuaderno_inspector_fecha
            ON cuaderno_inspector_asientos (fecha)
            """
        )
        conn.commit()
        cur.close()
        return True
    except Exception as exc:
        if conn:
            with suppress(Exception):
                conn.rollback()
        print("[CUADERNO][DB] No se pudieron asegurar las tablas:", exc)
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


def _normalizar_lista_texto(valor):
    if isinstance(valor, list):
        return [str(item).strip() for item in valor if str(item or "").strip()]
    if isinstance(valor, str):
        try:
            parsed = json.loads(valor)
            if isinstance(parsed, list):
                return [str(item).strip() for item in parsed if str(item or "").strip()]
        except Exception:
            return [item.strip() for item in valor.split(",") if item.strip()]
    return []


def _extraer_personal_gastos_generales(contenido):
    if not isinstance(contenido, dict):
        return []
    candidatos = [
        contenido.get("personal_gastos_generales"),
        contenido.get("datos", {}).get("personal_gastos_generales") if isinstance(contenido.get("datos"), dict) else None,
        contenido.get("estado_local", {}).get("listas", {}).get("m2_gastos_generales") if isinstance(contenido.get("estado_local"), dict) else None,
    ]
    for candidato in candidatos:
        lista = _normalizar_lista_texto(candidato)
        if lista:
            return lista
    return []


def _fecha_anterior_iso(fecha):
    try:
        return (datetime.strptime(str(fecha), "%Y-%m-%d").date() - timedelta(days=1)).isoformat()
    except Exception:
        return (date.today() - timedelta(days=1)).isoformat()


def _registrar_log(cur, numero, usuario, accion, detalle=""):
    cur.execute(
        """
        INSERT INTO cuaderno_logs (asiento_numero, usuario, accion, detalle)
        VALUES (%s, %s, %s, %s)
        """,
        (numero, usuario or "Sistema", accion, detalle or ""),
    )


def _correlacionar_inspector_por_fecha(cur, fecha, numero_residencia):
    """Asigna al Inspector pendiente de la misma fecha el correlativo siguiente."""
    try:
        numero_inspector = int(numero_residencia) + 1
    except (TypeError, ValueError):
        return
    cur.execute(
        """
        UPDATE cuaderno_inspector_asientos
        SET residencia_numero = %s,
            numero = COALESCE(numero, %s),
            updated_at = NOW()
        WHERE fecha = %s
          AND (residencia_numero IS NULL OR residencia_numero = %s)
        """,
        (numero_residencia, numero_inspector, fecha, numero_residencia),
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
        print("[CUADERNO][DB] Panel sin conexión: asegurar_tablas_cuaderno() devolvió False")
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
                COUNT(*) FILTER (WHERE estado IN ('Cerrado', 'Firmado', 'Enviado Inspector', 'firmado_inspector')) AS cerrados,
                COUNT(*) FILTER (WHERE estado IN ('Borrador', 'borrador_inspector')) AS borradores,
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
              AND (o.tipo = 'observacion-tecnica' OR LOWER(o.autor) LIKE '%inspector%' OR LOWER(o.autor) LIKE '%supervisor%')
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

        datos_mes = obtener_datos_mes_cuaderno(date.today().year, date.today().month)
        if datos_mes.get("ok"):
            asientos = datos_mes.get("asientos") or asientos

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
                "tiene_residencia": bool(a.get("tiene_residencia", str(a.get("tipo") or "").lower() != "inspector")),
                "tiene_inspector": bool(a.get("tiene_inspector")),
                "residencia_numero": a.get("residencia_numero") or (a["numero"] if str(a.get("tipo") or "").lower() != "inspector" else None),
                "inspector_numero": a.get("inspector_numero"),
                "inspector_estado": a.get("inspector_estado"),
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
        if datos_mes.get("ok"):
            datos["mes_actual"] = datos_mes.get("estadisticas") or datos["mes_actual"]
        else:
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
    except Exception as exc:
        print("[CUADERNO][DB] Error cargando panel principal:", exc)
        datos["conectado"] = False
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
        personal_gastos = _extraer_personal_gastos_generales(contenido)
        bloqueado = estado_normalizado == "Cerrado"
        firmado_por = usuario if estado_normalizado == "Cerrado" else None
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
            return {"ok": False, "error": "El asiento está firmado y bloqueado. Solo Admin puede editarlo."}

        cur.execute(
            """
            INSERT INTO cuaderno_asientos (numero, fecha, tipo, estado, avance, bloqueado, firmado_por, firmado_en, contenido, observaciones, personal_gastos_generales, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, CASE WHEN %s = 'Cerrado' THEN NOW() ELSE NULL END, %s, %s, %s::jsonb, NOW())
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
                personal_gastos_generales = EXCLUDED.personal_gastos_generales,
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
                json.dumps(personal_gastos, ensure_ascii=False),
            ),
        )
        row = cur.fetchone()
        accion = "envió a Inspector" if estado_normalizado == "Enviado Inspector" else ("cerró y bloqueó" if estado_normalizado == "Cerrado" else "guardó borrador")
        _registrar_log(
            cur,
            numero,
            usuario,
            accion,
            f"{tipo_normalizado} {accion} el asiento N° {str(numero).zfill(3)}.",
        )
        if tipo_normalizado == "Inspector" and observaciones:
            cur.execute(
                """
                INSERT INTO cuaderno_observaciones (asiento_numero, autor, texto, tipo, resuelto)
                VALUES (%s, %s, %s, 'observacion-tecnica', FALSE)
                """,
                (numero, usuario or "Inspector", observaciones),
            )
        if tipo_normalizado == "Residente":
            _correlacionar_inspector_por_fecha(cur, fecha, numero)
        conn.commit()
        cur.close()
        return {
            "ok": True,
            "status": "success",
            "numero": row[0],
            "fecha": str(fecha),
            "estado": row[1],
            "estado_slug": str(row[1] or "").lower().replace(" ", "_"),
            "avance": row[2],
            "tipo": row[3],
            "bloqueado": row[4],
        }
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
        fechas_residencia = {a.get("fecha") for a in asientos}
        cur.execute(
            """
            SELECT COALESCE(numero, residencia_numero) AS numero,
                   residencia_numero,
                   fecha::TEXT AS fecha,
                   EXTRACT(DAY FROM fecha)::INTEGER AS dia,
                   estado,
                   CASE WHEN estado = 'firmado_inspector' THEN 100 ELSE 50 END AS avance,
                   COALESCE(firmado_por, 'Inspector') AS supervisor,
                   updated_at::TEXT AS updated_at,
                   'Inspector' AS tipo,
                   estado = 'firmado_inspector' AS bloqueado,
                   '' AS observaciones
            FROM cuaderno_inspector_asientos
            WHERE EXTRACT(YEAR FROM fecha)::INTEGER = %s
              AND EXTRACT(MONTH FROM fecha)::INTEGER = %s
            ORDER BY fecha ASC
            """,
            (year, month),
        )
        inspector_rows = _fetchall_dict(cur)
        inspector_por_fecha = {item.get("fecha"): item for item in inspector_rows if item.get("fecha")}
        for asiento in asientos:
            inspector = inspector_por_fecha.get(asiento.get("fecha"))
            asiento["tiene_residencia"] = True
            asiento["tiene_inspector"] = bool(inspector)
            asiento["inspector_numero"] = inspector.get("numero") if inspector else None
            asiento["inspector_estado"] = inspector.get("estado") if inspector else None
            asiento["residencia_numero"] = asiento.get("numero")
        inspector_asientos = []
        for item in inspector_rows:
            if item.get("fecha") in fechas_residencia:
                continue
            item["tiene_residencia"] = False
            item["tiene_inspector"] = True
            item["inspector_numero"] = item.get("numero")
            item["inspector_estado"] = item.get("estado")
            inspector_asientos.append(item)
        asientos.extend(inspector_asientos)
        cur.execute(
            """
            SELECT
                COUNT(*) FILTER (WHERE estado IN ('Cerrado', 'Firmado', 'Enviado Inspector', 'firmado_inspector')) AS cerrados,
                COUNT(*) FILTER (WHERE estado IN ('Borrador', 'borrador_inspector')) AS borradores,
                EXTRACT(DAY FROM ((DATE_TRUNC('month', MAKE_DATE(%s, %s, 1)) + INTERVAL '1 month - 1 day')))::INTEGER AS dias_mes
            FROM (
                SELECT fecha, estado FROM cuaderno_asientos
                WHERE EXTRACT(YEAR FROM fecha)::INTEGER = %s
                  AND EXTRACT(MONTH FROM fecha)::INTEGER = %s
                UNION ALL
                SELECT fecha, estado FROM cuaderno_inspector_asientos i
                WHERE EXTRACT(YEAR FROM fecha)::INTEGER = %s
                  AND EXTRACT(MONTH FROM fecha)::INTEGER = %s
                  AND NOT EXISTS (SELECT 1 FROM cuaderno_asientos a WHERE a.fecha = i.fecha)
            ) estados_mes
            """,
            (year, month, year, month, year, month),
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
                    "tiene_residencia": bool(a.get("tiene_residencia", str(a.get("tipo") or "").lower() != "inspector")),
                    "tiene_inspector": bool(a.get("tiene_inspector")),
                    "residencia_numero": a.get("residencia_numero") or (a["numero"] if str(a.get("tipo") or "").lower() != "inspector" else None),
                    "inspector_numero": a.get("inspector_numero"),
                    "inspector_estado": a.get("inspector_estado"),
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
                   contenido, COALESCE(observaciones, '') AS observaciones,
                   COALESCE(firmado_por, '') AS firmado_por, firmado_en::TEXT AS firmado_en
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
            "firmado_por": row[8],
            "firmado_en": row[9],
        }
    except Exception:
        return None
    finally:
        if conn:
            release_connection(conn)


def obtener_asiento_por_fecha(fecha):
    if not asegurar_tablas_cuaderno():
        return None
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT numero, fecha::TEXT AS fecha, tipo, estado, avance, bloqueado,
                   contenido, COALESCE(observaciones, '') AS observaciones,
                   COALESCE(firmado_por, '') AS firmado_por, firmado_en::TEXT AS firmado_en
            FROM cuaderno_asientos
            WHERE fecha = %s
            ORDER BY numero DESC
            LIMIT 1
            """,
            (fecha,),
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
            "firmado_por": row[8],
            "firmado_en": row[9],
        }
    except Exception:
        return None
    finally:
        if conn:
            release_connection(conn)


def obtener_personal_gastos_anterior(fecha):
    if not asegurar_tablas_cuaderno():
        return []
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT COALESCE(personal_gastos_generales, '[]'::jsonb)::TEXT
            FROM cuaderno_asientos
            WHERE fecha = %s
            ORDER BY numero DESC
            LIMIT 1
            """,
            (_fecha_anterior_iso(fecha),),
        )
        row = cur.fetchone()
        cur.close()
        return _normalizar_lista_texto(row[0] if row else [])
    except Exception:
        return []
    finally:
        if conn:
            release_connection(conn)


def obtener_catalogo_personal_gastos():
    if not asegurar_tablas_cuaderno():
        return []
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT DISTINCT jsonb_array_elements_text(personal_gastos_generales) AS nombre
            FROM cuaderno_asientos
            WHERE jsonb_typeof(personal_gastos_generales) = 'array'
            ORDER BY nombre
            """
        )
        filas = [row[0] for row in cur.fetchall()]
        cur.close()
        return _normalizar_lista_texto(filas)
    except Exception:
        return []
    finally:
        if conn:
            release_connection(conn)


def obtener_personal_supervision_anterior(fecha):
    if not asegurar_tablas_cuaderno():
        return []
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT COALESCE(personal_supervision, '[]'::jsonb)::TEXT
            FROM cuaderno_inspector_asientos
            WHERE fecha = %s
            LIMIT 1
            """,
            (_fecha_anterior_iso(fecha),),
        )
        row = cur.fetchone()
        cur.close()
        return _normalizar_lista_texto(row[0] if row else [])
    except Exception:
        return []
    finally:
        if conn:
            release_connection(conn)


def contenido_asiento_dict(asiento):
    if not asiento:
        return {}
    contenido = asiento.get("contenido")
    if isinstance(contenido, dict):
        return contenido
    try:
        return json.loads(contenido or "{}")
    except Exception:
        return {}


def extraer_ocurrencias_residencia(asiento):
    contenido = contenido_asiento_dict(asiento)
    for modulo in contenido.get("modulos") or []:
        if not isinstance(modulo, dict):
            continue
        titulo = str(modulo.get("titulo") or "").lower()
        if titulo.startswith("10.") or "ocurrencia" in titulo or "conocimiento" in titulo:
            return str(modulo.get("contenido") or "").strip()
    return str(contenido.get("observaciones") or asiento.get("observaciones") or "").strip()


def obtener_inspector_asiento(numero=None, fecha=None):
    if not asegurar_tablas_cuaderno():
        return None
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        if fecha:
            cur.execute(
                """
                SELECT numero, residencia_numero, fecha::TEXT AS fecha, estado, contenido,
                       COALESCE(personal_supervision, '[]'::jsonb)::TEXT AS personal_supervision,
                       COALESCE(partidas_ejecutadas, '') AS partidas_ejecutadas,
                       COALESCE(almacen_ingreso, '') AS almacen_ingreso,
                       COALESCE(almacen_salida, '') AS almacen_salida,
                       COALESCE(maquinaria, '') AS maquinaria,
                       COALESCE(ocurrencias, '') AS ocurrencias,
                       COALESCE(firmado_por, '') AS firmado_por, firmado_en::TEXT AS firmado_en,
                       updated_at::TEXT AS updated_at
                FROM cuaderno_inspector_asientos
                WHERE fecha = %s
                """,
                (fecha,),
            )
        else:
            cur.execute(
                """
                SELECT numero, residencia_numero, fecha::TEXT AS fecha, estado, contenido,
                       COALESCE(personal_supervision, '[]'::jsonb)::TEXT AS personal_supervision,
                       COALESCE(partidas_ejecutadas, '') AS partidas_ejecutadas,
                       COALESCE(almacen_ingreso, '') AS almacen_ingreso,
                       COALESCE(almacen_salida, '') AS almacen_salida,
                       COALESCE(maquinaria, '') AS maquinaria,
                       COALESCE(ocurrencias, '') AS ocurrencias,
                       COALESCE(firmado_por, '') AS firmado_por, firmado_en::TEXT AS firmado_en,
                       updated_at::TEXT AS updated_at
                FROM cuaderno_inspector_asientos
                WHERE numero = %s OR residencia_numero = %s
                ORDER BY CASE WHEN numero = %s THEN 0 ELSE 1 END
                LIMIT 1
                """,
                (numero, numero, numero),
            )
        row = cur.fetchone()
        cur.close()
        if not row:
            return None
        return {
            "numero": row[0],
            "residencia_numero": row[1],
            "fecha": row[2],
            "estado": row[3],
            "contenido": row[4],
            "personal_supervision": _normalizar_lista_texto(row[5]),
            "partidas_ejecutadas": row[6],
            "almacen_ingreso": row[7],
            "almacen_salida": row[8],
            "maquinaria": row[9],
            "ocurrencias": row[10],
            "firmado_por": row[11],
            "firmado_en": row[12],
            "updated_at": row[13],
        }
    except Exception:
        return None
    finally:
        if conn:
            release_connection(conn)


def guardar_asiento_inspector(numero=None, fecha=None, estado="Borrador", contenido=None, usuario=None):
    conectado = asegurar_tablas_cuaderno()
    if not conectado:
        return {"ok": False, "error": "Base de datos no conectada"}
    estado_normalizado = "firmado_inspector" if str(estado or "").strip().lower() in ("firmado", "firmar", "definitivo", "firmado_inspector") else "borrador_inspector"
    contenido = contenido or {}
    contenido_texto = contenido if isinstance(contenido, str) else json.dumps(contenido, ensure_ascii=False)
    contenido_dict = contenido if isinstance(contenido, dict) else {}
    personal_supervision = _normalizar_lista_texto(contenido_dict.get("personal_supervision"))
    partidas_ejecutadas = str(contenido_dict.get("partidas_ejecutadas") or contenido_dict.get("partidas") or "")
    almacen_ingreso = str(contenido_dict.get("almacen_ingreso") or "")
    almacen_salida = str(contenido_dict.get("almacen_salida") or "")
    maquinaria = str(contenido_dict.get("maquinaria") or "")
    ocurrencias = str(contenido_dict.get("ocurrencias") or contenido_dict.get("texto") or "")
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        residencia_numero = None
        numero_inspector = None
        if numero:
            try:
                residencia_numero = int(numero)
                numero_inspector = residencia_numero + 1
            except (TypeError, ValueError):
                residencia_numero = None
                numero_inspector = None
        cur.execute(
            """
            INSERT INTO cuaderno_inspector_asientos
                (numero, residencia_numero, fecha, estado, contenido, personal_supervision, partidas_ejecutadas, almacen_ingreso, almacen_salida, maquinaria, ocurrencias, firmado_por, firmado_en, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s::jsonb, %s, %s, %s, %s, %s, %s, CASE WHEN %s = 'firmado_inspector' THEN NOW() ELSE NULL END, NOW())
            ON CONFLICT (fecha) DO UPDATE SET
                numero = COALESCE(EXCLUDED.numero, cuaderno_inspector_asientos.numero),
                residencia_numero = COALESCE(EXCLUDED.residencia_numero, cuaderno_inspector_asientos.residencia_numero),
                fecha = EXCLUDED.fecha,
                estado = EXCLUDED.estado,
                contenido = EXCLUDED.contenido,
                personal_supervision = EXCLUDED.personal_supervision,
                partidas_ejecutadas = EXCLUDED.partidas_ejecutadas,
                almacen_ingreso = EXCLUDED.almacen_ingreso,
                almacen_salida = EXCLUDED.almacen_salida,
                maquinaria = EXCLUDED.maquinaria,
                ocurrencias = EXCLUDED.ocurrencias,
                firmado_por = CASE
                    WHEN EXCLUDED.estado = 'firmado_inspector' THEN EXCLUDED.firmado_por
                    ELSE cuaderno_inspector_asientos.firmado_por
                END,
                firmado_en = CASE
                    WHEN EXCLUDED.estado = 'firmado_inspector' THEN NOW()
                    ELSE cuaderno_inspector_asientos.firmado_en
                END,
                updated_at = NOW()
            RETURNING numero, residencia_numero, fecha::TEXT, estado
            """,
            (
                numero_inspector,
                residencia_numero,
                fecha,
                estado_normalizado,
                contenido_texto,
                json.dumps(personal_supervision, ensure_ascii=False),
                partidas_ejecutadas,
                almacen_ingreso,
                almacen_salida,
                maquinaria,
                ocurrencias,
                usuario if estado_normalizado == "firmado_inspector" else None,
                estado_normalizado,
            ),
        )
        row = cur.fetchone()
        if estado_normalizado == "firmado_inspector" and row[1]:
            cur.execute(
                """
                UPDATE cuaderno_asientos
                SET estado = 'Cerrado', bloqueado = TRUE, firmado_por = %s, firmado_en = NOW(), updated_at = NOW()
                WHERE numero = %s
                """,
                (usuario or "Inspector", row[1]),
            )
        _registrar_log(
            cur,
            row[0] or row[1],
            usuario or "Inspector",
            "firmó asiento" if estado_normalizado == "firmado_inspector" else "guardó borrador de Inspector",
            f"Inspector de Obra {('firmó definitivamente' if estado_normalizado == 'firmado_inspector' else 'guardó borrador del')} asiento de fecha {row[2]}.",
        )
        conn.commit()
        cur.close()
        return {"ok": True, "status": "success", "numero": row[0], "residencia_numero": row[1], "fecha": row[2], "estado": row[3]}
    except Exception as exc:
        if conn:
            with suppress(Exception):
                conn.rollback()
        return {"ok": False, "error": str(exc)}
    finally:
        if conn:
            release_connection(conn)


def anular_firma_asiento(numero, usuario=None):
    if not asegurar_tablas_cuaderno():
        return {"ok": False, "error": "Base de datos no conectada"}
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT numero, estado
            FROM cuaderno_asientos
            WHERE numero = %s
            """,
            (numero,),
        )
        row = cur.fetchone()
        if not row:
            cur.close()
            return {"ok": False, "error": "Asiento no encontrado"}
        nuevo_estado = "Enviado Inspector" if row[1] in ("Cerrado", "Firmado") else "Borrador"
        cur.execute(
            """
            UPDATE cuaderno_asientos
            SET estado = %s,
                bloqueado = FALSE,
                firmado_por = NULL,
                firmado_en = NULL,
                updated_at = NOW()
            WHERE numero = %s
            """,
            (nuevo_estado, numero),
        )
        cur.execute(
            """
            UPDATE cuaderno_inspector_asientos
            SET estado = 'borrador_inspector',
                firmado_por = NULL,
                firmado_en = NULL,
                updated_at = NOW()
            WHERE residencia_numero = %s OR numero = %s
            """,
            (numero, numero + 1),
        )
        _registrar_log(
            cur,
            numero,
            usuario or "Admin",
            "anuló firma",
            f"Se anuló la firma y se desbloqueó el asiento N° {str(numero).zfill(3)}.",
        )
        conn.commit()
        cur.close()
        return {"ok": True, "status": "success", "numero": numero, "estado": nuevo_estado}
    except Exception as exc:
        if conn:
            with suppress(Exception):
                conn.rollback()
        return {"ok": False, "error": str(exc)}
    finally:
        if conn:
            release_connection(conn)
