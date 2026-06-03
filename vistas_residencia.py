# =========================================================
# vistas_residencia.py
# Módulo Maestro: Ensamblador Final del Cuaderno de Obra
# =========================================================

from flask import Blueprint, render_template_string, session, redirect, url_for, request, jsonify
from navbar import obtener_navbar
from datetime import datetime, timedelta
import traceback
from cuaderno_obra import CUADERNO_OBRA_CSS, CUADERNO_OBRA_JS, obtener_cuaderno_obra_html
from resumen_asiento import RESUMEN_ASIENTO_HTML
from cuaderno_store import (
    extraer_ocurrencias_residencia,
    guardar_asiento,
    obtener_asiento,
    obtener_asiento_por_fecha,
    obtener_inspector_asiento,
    obtener_personal_gastos_anterior,
)

# ==============================================================================
# IMPORTACIÓN DINÁMICA
# ==============================================================================
try: from mod_01_jornal import JORNAL_HTML
except: JORNAL_HTML = "<div class='step-view active' id='step1'><p>Error: mod_01_jornal.py</p></div>"

try: from mod_02_personal import PERSONAL_HTML
except: PERSONAL_HTML = "<div class='step-view' id='step2'><p>Error: mod_02_personal.py</p></div>"

try: from mod_03_partidas import PARTIDAS_HTML
except: PARTIDAS_HTML = "<div class='step-view' id='step3'><p>Error: mod_03_partidas.py</p></div>"

try: from mod_04_mayor_metrado import MAYOR_METRADO_HTML
except: MAYOR_METRADO_HTML = "<div class='step-view' id='step4'><p>En construcción...</p></div>"

try: from mod_05_sub_partidas import SUB_PARTIDAS_HTML
except: SUB_PARTIDAS_HTML = "<div class='step-view' id='step5'><p>En construcción...</p></div>"

try: from mod_06_actividades import ACTIVIDADES_HTML
except: ACTIVIDADES_HTML = "<div class='step-view' id='step6'><p>En construcción...</p></div>"

try: from mod_07_almacen import ALMACEN_HTML
except: ALMACEN_HTML = "<div class='step-view' id='step7'><p>En construcción...</p></div>"

try: from mod_08_maquinaria import MAQUINARIA_HTML
except: MAQUINARIA_HTML = "<div class='step-view' id='step8'><p>En construcción...</p></div>"

try: from mod_09_herramientas import HERRAMIENTAS_HTML
except: HERRAMIENTAS_HTML = "<div class='step-view' id='step9'><p>En construcción...</p></div>"

try: from mod_10_ocurrencias import OCURRENCIAS_HTML
except: OCURRENCIAS_HTML = "<div class='step-view' id='step10'><p>En construcción...</p></div>"

residencia_bp = Blueprint('residencia', __name__)


@residencia_bp.route('/residencia/api/asiento/<int:numero>')
def api_obtener_asiento(numero):
    if 'usuario_id' not in session:
        return jsonify({"ok": False, "error": "No autorizado"}), 401
    asiento = obtener_asiento(numero)
    return jsonify({"ok": True, "asiento": asiento})


@residencia_bp.route('/residencia/api/carryover')
def api_carryover_residencia():
    if 'usuario_id' not in session:
        return jsonify({"ok": False, "error": "No autorizado"}), 401
    fecha = request.args.get("fecha") or datetime.now().strftime('%Y-%m-%d')
    return jsonify({
        "ok": True,
        "fecha": fecha,
        "personal_gastos_generales": obtener_personal_gastos_anterior(fecha),
    })


@residencia_bp.route('/residencia/api/ocurrencias-previas')
def api_ocurrencias_previas_residencia():
    if 'usuario_id' not in session:
        return jsonify({"ok": False, "error": "No autorizado"}), 401
    fecha_raw = request.args.get("fecha") or datetime.now().strftime('%Y-%m-%d')
    try:
        fecha_actual = datetime.strptime(fecha_raw, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"ok": False, "error": "Fecha inválida"}), 400

    dias_retroceso = 2 if fecha_actual.weekday() == 0 else 1
    fecha_anterior = fecha_actual - timedelta(days=dias_retroceso)
    fecha_anterior_iso = fecha_anterior.strftime("%Y-%m-%d")

    asiento_residencia = obtener_asiento_por_fecha(fecha_anterior_iso)
    asiento_supervision = obtener_inspector_asiento(fecha=fecha_anterior_iso)
    ocurrencia_residencia = extraer_ocurrencias_residencia(asiento_residencia) if asiento_residencia else ""
    ocurrencia_supervision = (asiento_supervision or {}).get("ocurrencias") or ""

    return jsonify({
        "ok": True,
        "fecha": fecha_raw,
        "fecha_anterior": fecha_anterior_iso,
        "residencia": {
            "numero": asiento_residencia.get("numero") if asiento_residencia else None,
            "texto": ocurrencia_residencia,
        },
        "supervision": {
            "numero": asiento_supervision.get("numero") if asiento_supervision else None,
            "residencia_numero": asiento_supervision.get("residencia_numero") if asiento_supervision else None,
            "texto": ocurrencia_supervision,
        },
    })


@residencia_bp.route('/residencia/api/asiento', methods=['POST'])
@residencia_bp.route('/guardar_asiento', methods=['POST'])
def api_guardar_asiento():
    try:
        if 'usuario_id' not in session:
            return jsonify({"ok": False, "status": "error", "message": "No autorizado", "error": "No autorizado"}), 401

        data = request.get_json(silent=True) or {}
        numero = int(data.get("numero"))
        avance = max(0, min(100, int(data.get("avance", 0))))
    except (TypeError, ValueError):
        return jsonify({"ok": False, "status": "error", "message": "Número de asiento o avance inválido", "error": "Número de asiento o avance inválido"}), 400
    except Exception as e:
        traceback.print_exc()
        return jsonify({"ok": False, "status": "error", "message": str(e), "error": str(e)}), 500

    try:
        estado_raw = str(data.get("estado") or "Borrador").strip().lower()
        estado = "Enviado Inspector" if estado_raw in ("enviado_inspector", "enviado inspector", "enviar a inspector", "cerrado", "firmado", "vista previa y firmar", "closed") else "Borrador"
        tipo_raw = data.get("tipo") or data.get("autor_tipo") or session.get("rol") or "Residente"
        tipo = "Inspector" if ("inspector" in str(tipo_raw).lower() or "super" in str(tipo_raw).lower()) else "Residente"

        existente = obtener_asiento(numero)
        if existente and (existente.get("estado") in ("Cerrado", "Firmado") or (existente.get("bloqueado") and existente.get("estado") != "Enviado Inspector")) and session.get("rol") != "Admin":
            mensaje = "El asiento ya fue firmado o cerrado. Solo el dueño/Admin puede editarlo."
            return jsonify({"ok": False, "status": "error", "message": mensaje, "error": mensaje}), 403

        contenido = data.get("contenido")
        if not contenido:
            contenido = {
                "numero": numero,
                "fecha": data.get("fecha") or datetime.now().strftime('%Y-%m-%d'),
                "modulos": data.get("modulos") or [],
                "observaciones": data.get("observaciones") or data.get("observacion") or "",
            }

        resultado = guardar_asiento(
            numero=numero,
            fecha=data.get("fecha") or datetime.now().strftime('%Y-%m-%d'),
            estado=estado,
            avance=avance,
            contenido=contenido,
            usuario=session.get("nombre", "Sistema"),
            tipo=tipo,
            puede_editar_cerrado=session.get("rol") == "Admin",
        )
        if resultado.get("ok"):
            status = 200
        elif "cerrado" in str(resultado.get("error", "")).lower() or "bloqueado" in str(resultado.get("error", "")).lower():
            status = 403
        else:
            print("[CUADERNO][ERROR] No se pudo guardar asiento:", resultado.get("error"))
            status = 500

        if resultado.get("ok"):
            estado_api = str(resultado.get("estado") or estado).strip().lower().replace(" ", "_")
            fecha_guardada = data.get("fecha") or resultado.get("fecha") or datetime.now().strftime('%Y-%m-%d')
            redirect_url = "" if estado_api == "borrador" else f"/resumen_asiento/{fecha_guardada}"
            modulo_activo = data.get("modulo_activo")
            if not modulo_activo and isinstance(contenido, dict):
                modulo_activo = (contenido.get("estado_local") or {}).get("step")
            resultado = {
                **resultado,
                "status": "success",
                "fecha": fecha_guardada,
                "estado": estado_api,
                "estado_label": resultado.get("estado"),
                "redirect_url": redirect_url,
                "modulo_activo": modulo_activo,
            }
        else:
            mensaje = str(resultado.get("error") or "No se pudo guardar el asiento.")
            resultado = {
                **resultado,
                "ok": False,
                "status": "error",
                "message": mensaje,
                "error": mensaje,
            }
        return jsonify(resultado), status
    except Exception as e:
        traceback.print_exc()
        return jsonify({"ok": False, "status": "error", "message": str(e), "error": str(e)}), 500

@residencia_bp.route('/residencia')
def redaccion_asiento_residente():
    if 'usuario_id' not in session: return redirect(url_for('login.mostrar_login'))

    es_admin = session.get('rol') == 'Admin'
    nombre_completo = session.get('nombre', 'Ing. Samuel Gutierrez')
    menu_superior = obtener_navbar(es_admin, nombre_completo)
    fecha_hoy_iso = datetime.now().strftime('%Y-%m-%d')
    numero_hoja = "0001"
    cuaderno_obra_html = obtener_cuaderno_obra_html(numero_hoja)

    html_completo = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>SAMU — Residencia</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <script>
            window.tailwind = window.tailwind || {{}};
            window.tailwind.config = {{ corePlugins: {{ preflight: false }} }};
            (function() {{
                try {{
                    const params = new URLSearchParams(window.location.search || '');
                    const pasoURL = parseInt(params.get('paso') || params.get('modulo') || '', 10);
                    const estado = JSON.parse(localStorage.getItem('samu_residencia_asiento_en_edicion') || sessionStorage.getItem('samu_residencia_asiento_en_edicion') || 'null');
                    const pasoLocal = parseInt(localStorage.getItem('samu_residencia_modulo_activo') || sessionStorage.getItem('samu_residencia_modulo_activo') || estado?.step || '', 10);
                    window.__samuModuloInicial = Math.max(1, Math.min(10, pasoURL || pasoLocal || 1));
                    document.documentElement.classList.add('samu-restoring');
                }} catch (e) {{
                    window.__samuModuloInicial = 1;
                }}
            }})();
        </script>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Caveat:wght@600;700&display=swap');
            :root {{ --apple-text: #1d1d1f; --celeste-obra: #0263a0; --nav-height: 52px; }}
            body {{ font-family: 'Inter', sans-serif; color: var(--apple-text); overflow-x: hidden; padding-bottom: 90px; margin: 0; background: linear-gradient(135deg, rgba(255,255,255,1) 0%, rgba(2,99,160,0.08) 40%, rgba(135,206,235,0.12) 70%, rgba(249,168,212,0.12) 100%); background-attachment: fixed; }}
            
            @keyframes floatInUp {{ from {{ opacity: 0; transform: translateY(30px); }} to {{ opacity: 1; transform: translateY(0); }} }}
            @keyframes floatOutDown {{ from {{ opacity: 1; transform: translateY(0); }} to {{ opacity: 0; transform: translateY(30px); }} }}
            
            .stepper-container {{ position: fixed; top: calc(var(--nav-height) + 16px); bottom: 92px; left: 18px; width: 218px; background: transparent; backdrop-filter: none; border: 0; border-radius: 0; z-index: 900; padding: 4px 34px 4px 0; overflow-y: auto; overflow-x: visible; white-space: normal; display: flex; flex-direction: column; align-items: stretch; justify-content: space-between; gap: 8px; opacity: 0; pointer-events: none; transition: opacity 0.5s; box-shadow: none; }}
            .stepper-container::before {{ content: none; display: none; }}
            .stepper-container::-webkit-scrollbar {{ width: 0; height: 0; display: none; }}
            .step-btn {{ position: relative; width: 100%; min-height: 48px; border: 0; border-radius: 18px; padding: 12px 12px 12px 46px; min-width: 0; max-width: none; font-size: 10.5px; line-height: 1.12; letter-spacing: .045em; text-transform: uppercase; font-weight: 950; color: #475569; background: rgba(255,255,255,0.62); cursor: pointer; transition: transform .36s cubic-bezier(.16,1,.3,1), color .24s ease, background .24s ease, box-shadow .36s cubic-bezier(.16,1,.3,1); transform-origin: left center; box-shadow: none; overflow: visible; text-align: left; will-change: transform; }}
            .step-label-short, .step-label-full {{ position: absolute; left: 46px; right: 14px; top: 50%; display: block; transform: translateY(-50%); transition: opacity .22s ease; will-change: opacity; }}
            .step-label-short {{ opacity: 1; }}
            .step-label-full {{ opacity: 0; font-size: 9.5px; line-height: 1.1; letter-spacing: .025em; white-space: normal; pointer-events: none; }}
            .step-btn::before {{ content: ""; position: absolute; left: 8px; top: 50%; transform: translateY(-50%); width: 28px; height: 28px; border-radius: 12px; display: grid; place-items: center; background: #f1f5f9; color: #64748b; font-size: 13px; font-weight: 900; box-shadow: inset 0 0 0 1px #e2e8f0; }}
            .step-main-icon {{ position: absolute; left: 14px; top: 50%; transform: translateY(-50%); z-index: 2; font-size: 14px; line-height: 1; color: #64748b; pointer-events: none; }}
            .step-btn::after {{ content: ""; position: absolute; left: 46px; right: 14px; bottom: 7px; height: 3px; border-radius: 999px; background: linear-gradient(90deg, #0284c7 var(--pct, 0%), #e2e8f0 0); opacity: .9; }}
            .step-btn:hover {{ transform: translateX(10px) scale(1.03); color: #0f172a; background: rgba(255,255,255,0.92); box-shadow: 0 16px 30px rgba(2,132,199,0.15); z-index: 3; }}
            .step-btn:hover .step-label-short {{ opacity: 0; }}
            .step-btn:hover .step-label-full {{ opacity: 1; }}
            .step-btn.active {{ background: #ffffff !important; color: #020617 !important; font-weight: 950 !important; transform: translateX(6px) scale(1.02); box-shadow: 0 16px 35px rgba(15,23,42,0.13); }}
            .step-btn:hover .step-main-icon, .step-btn.active .step-main-icon {{ color: #0284c7; }}
            .step-btn.completed {{ color: #166534; background: rgba(240,253,244,.72); }}
            .step-btn.completed::before {{ background: #22c55e; color: #fff; box-shadow: 0 6px 14px rgba(34,197,94,.25); }}
            .step-btn.completed .step-main-icon {{ color: #fff; }}
            .step-btn.missing {{ color: #9a3412; background: rgba(255,247,237,.78); }}
            .step-btn.missing::before {{ background: #ffedd5; color: #9a3412; }}
            .step-btn.resumen {{ color: #fff; background: linear-gradient(135deg, #0f172a, #0263a0); }}
            .step-btn.resumen::before {{ background: rgba(255,255,255,.16); color: #fff; box-shadow: none; }}
            .step-btn.resumen .step-main-icon {{ color: #fff; }}
            .step-btn.resumen::after {{ background: linear-gradient(90deg, #38bdf8 100%, #38bdf8 0); }}
            .sidebar-accordion {{ overflow: visible; }}
            .step-btn.accordion-toggle {{ display: flex; align-items: center; justify-content: flex-start; }}
            .step-btn.accordion-toggle .step-label-short, .step-btn.accordion-toggle .step-label-full {{ right: 30px; }}
            .step-btn.accordion-toggle .accordion-caret {{ margin-left: auto; font-size: 12px; transition: transform .3s ease; }}
            .sidebar-accordion.open .accordion-caret {{ transform: rotate(180deg); }}
            .sidebar-submenu {{ max-height: 0; overflow: hidden; padding-left: 18px; transition: max-height .46s cubic-bezier(.16,1,.3,1), opacity .3s ease, transform .46s cubic-bezier(.16,1,.3,1), margin .32s ease; opacity: 0; transform: translateY(-8px); will-change: max-height, opacity, transform; }}
            .sidebar-accordion.open .sidebar-submenu {{ max-height: 112px; margin-top: 6px; opacity: 1; transform: translateY(0); }}
            .sidebar-sub-btn {{ width: calc(100% - 8px); border: 0; border-radius: 14px; margin: 4px 0; padding: 9px 10px 9px 18px; text-align: left; font-size: 10px; line-height: 1.1; letter-spacing: .035em; text-transform: uppercase; font-weight: 900; color: #075985; background: rgba(224,242,254,.72); transition: transform .42s cubic-bezier(.16,1,.3,1), background .25s ease, color .25s ease, box-shadow .42s cubic-bezier(.16,1,.3,1); will-change: transform; }}
            .sidebar-sub-btn:hover {{ transform: translateX(10px) scale(1.03); background: #e0f2fe; color: #0f172a; box-shadow: 0 12px 24px rgba(2,132,199,.14); }}
            
            #globalTooltip {{ position: fixed; background: rgba(15, 23, 42, 0.96); backdrop-filter: blur(10px); color: #ffffff; padding: 11px 15px; border-radius: 14px; font-size: 11px; font-weight: 900; letter-spacing: .04em; text-transform: uppercase; white-space: nowrap; box-shadow: 0 18px 35px rgba(15,23,42,0.25); pointer-events: none; z-index: 999999; opacity: 0; transform: translateX(10px) scale(.96); transition: opacity 0.2s ease, transform 0.2s ease; border: 1px solid rgba(255,255,255,.12); }}
            #globalTooltip.visible {{ opacity: 1; transform: translateX(0) scale(1); }}

            .elegant-alert {{ position: fixed; top: 20px; left: 50%; transform: translateX(-50%) translateY(-100px); background: rgba(255,255,255,0.95); backdrop-filter: blur(20px); border-radius: 50px; padding: 12px 25px; display: flex; align-items: center; gap: 12px; box-shadow: 0 15px 35px rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,1); z-index: 9999999; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); opacity: 0; pointer-events: none; }}
            .elegant-alert.show {{ transform: translateX(-50%) translateY(0); opacity: 1; }}

            .split-layout {{ display: grid; grid-template-columns: minmax(500px, .92fr) minmax(680px, 1.08fr); gap: 24px; max-width: none; margin: calc(var(--nav-height) + 18px) 24px 0 260px; padding: 0; align-items: flex-start; filter: blur(5px); pointer-events: none; transition: filter 0.5s; }}
            .split-layout.unlocked {{ filter: blur(0); pointer-events: all; }}
            .form-column {{ min-width: 0; width: 100%; max-width: none; }}
            .preview-column {{ min-width: 0; position: sticky; top: calc(var(--nav-height) + 18px); height: calc(100vh - 154px); overflow-y: auto; display: flex; justify-content: center; }}
            .preview-column .cuaderno-preview-pages {{ width: min(100%, 840px); }}
            .preview-column .papel-fisico {{ width: 100%; }}
            .mobile-preview-btn {{ position: fixed; right: 18px; bottom: 88px; z-index: 920; border: none; border-radius: 999px; padding: 13px 16px; color: #fff; background: linear-gradient(135deg, #0f172a, #0263a0); box-shadow: 0 18px 38px rgba(15,23,42,.26); font-size: 12px; font-weight: 900; display: none; align-items: center; gap: 8px; opacity: 0; pointer-events: none; transform: translateY(12px); transition: .25s ease; }}
            .mobile-preview-btn.unlocked {{ opacity: 1; pointer-events: all; transform: translateY(0); }}
            
            .step-view {{ display: none; opacity: 0; background: rgba(255,255,255,0.85); backdrop-filter: blur(25px); padding: 30px; border-radius: 20px; box-shadow: 0 4px 25px rgba(0,0,0,0.03); border: 1px solid rgba(255,255,255,1);}}
            .step-view.active {{ display: block; animation: floatInUp 0.35s forwards; }}
            .samu-restoring .step-view.active {{ animation: none !important; opacity: 1; transform: none; }}
            .step-view.exit {{ display: block; animation: floatOutDown 0.3s forwards; }}
            .step-title {{ font-size: 22px; font-weight: 800; margin-bottom: 25px; color: #0f172a; letter-spacing: -0.5px;}}

            /* Tarjetas M1 y M2 */
            .time-card {{ background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 15px; display: flex; align-items: center; gap: 15px; cursor: pointer; transition: all 0.3s;}}
            .time-card.active {{ border-color: var(--celeste-obra); background: #f0f9ff; }}
            .time-card .clock-icon {{ font-size: 28px; color: #94a3b8; }}
            .time-card.active .clock-icon {{ color: var(--celeste-obra); }}

            .elegant-card {{ background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 16px 12px; text-align: center; transition: all 0.3s; display: flex; flex-direction: column; align-items: center; }}
            .elegant-card.active {{ border-color: var(--celeste-obra); background: rgba(2, 99, 160, 0.03); }}
            .elegant-card .p-icon {{ font-size: 26px; color: #94a3b8; transition: all 0.3s; margin-bottom: 4px; }}
            .elegant-card.active .p-icon {{ color: var(--celeste-obra); transform: scale(1.1); }}
            .elegant-card input {{ border: none; background: transparent; text-align: center; font-weight: 800; font-size: 20px; width: 100%; outline: none; }}

            {CUADERNO_OBRA_CSS}
            
            .bottom-bar {{ position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(255,255,255,0.95); backdrop-filter: blur(15px); border-top: 1px solid rgba(0,0,0,0.08); padding: 15px 30px; z-index: 900; display: flex; justify-content: space-between; align-items: center; opacity: 0; pointer-events: none; transition: opacity 0.5s;}}
            .bottom-bar.unlocked {{ opacity: 1; pointer-events: all; }}
            .asiento-actions {{ display: none; gap: 8px; flex-wrap: wrap; align-items: center; margin-left: auto; }}
            .asiento-actions.visible {{ display: flex; }}
            .save-inline-status {{ display: inline-flex; align-items: center; gap: 7px; min-width: 148px; min-height: 34px; padding: 7px 12px; border-radius: 999px; font-size: 11px; font-weight: 900; color: #64748b; background: rgba(248,250,252,.9); border: 1px solid rgba(226,232,240,.9); opacity: 0; transform: translateY(4px); pointer-events: none; transition: opacity .22s ease, transform .22s ease, color .22s ease, background .22s ease; }}
            .save-inline-status.visible {{ opacity: 1; transform: translateY(0); }}
            .save-inline-status.saving {{ color: #075985; background: #e0f2fe; border-color: #bae6fd; }}
            .save-inline-status.saved {{ color: #166534; background: #dcfce7; border-color: #bbf7d0; }}
            .save-inline-status.error {{ color: #991b1b; background: #fee2e2; border-color: #fecaca; }}
            .asiento-lock-banner {{ display: none; position: fixed; left: 50%; bottom: 76px; transform: translateX(-50%); z-index: 930; border-radius: 999px; padding: 10px 16px; background: #0f172a; color: #fff; font-size: 12px; font-weight: 800; box-shadow: 0 18px 34px rgba(15,23,42,.22); }}
            .asiento-lock-banner.visible {{ display: inline-flex; gap: 8px; align-items: center; }}
            .confirm-seat-overlay {{ position: fixed; inset: 0; z-index: 999999; display: none; align-items: center; justify-content: center; padding: 18px; background: rgba(15,23,42,.48); backdrop-filter: blur(14px); }}
            .confirm-seat-overlay.active {{ display: flex; animation: floatInUp .22s ease both; }}
            .confirm-seat-card {{ width: min(460px, 94vw); border: 1px solid rgba(255,255,255,.84); border-radius: 30px; background: rgba(255,255,255,.96); box-shadow: 0 35px 90px rgba(15,23,42,.32); overflow: hidden; }}
            .confirm-seat-hero {{ padding: 26px 26px 20px; color: #fff; background: linear-gradient(135deg, #0f172a, #166534); text-align: center; }}
            .confirm-seat-hero.draft {{ background: linear-gradient(135deg, #78350f, #f59e0b); }}
            .confirm-seat-hero .icon {{ width: 62px; height: 62px; border-radius: 22px; display: grid; place-items: center; margin: 0 auto 12px; background: rgba(255,255,255,.14); font-size: 30px; }}
            .confirm-seat-hero h5 {{ margin: 0; font-weight: 900; letter-spacing: -.25px; }}
            .confirm-seat-hero p {{ margin: 8px 0 0; font-size: 12px; color: rgba(255,255,255,.76); }}
            .confirm-seat-body {{ padding: 22px 24px 24px; }}
            .confirm-seat-warning {{ border: 1px solid #fde68a; border-radius: 18px; padding: 13px; background: #fef9c3; color: #854d0e; font-size: 12px; font-weight: 800; line-height: 1.45; }}
            .confirm-seat-actions {{ display: flex; gap: 10px; justify-content: flex-end; margin-top: 18px; flex-wrap: wrap; }}
            .confirm-seat-btn {{ border: 0; border-radius: 999px; padding: 11px 16px; font-size: 12px; font-weight: 900; }}
            .confirm-seat-btn.cancel {{ color: #334155; background: #f1f5f9; }}
            .confirm-seat-btn.primary {{ color: #fff; background: linear-gradient(135deg, #166534, #22c55e); box-shadow: 0 14px 28px rgba(34,197,94,.22); }}
            .confirm-seat-btn.primary.draft {{ background: linear-gradient(135deg, #b45309, #f59e0b); box-shadow: 0 14px 28px rgba(245,158,11,.22); }}
            .save-success-toast {{ position: fixed; top: 28px; right: 28px; z-index: 1000000; min-width: 280px; max-width: calc(100vw - 32px); display: none; align-items: center; gap: 12px; padding: 14px 16px; border-radius: 22px; background: rgba(255,255,255,.96); border: 1px solid rgba(255,255,255,.9); box-shadow: 0 24px 54px rgba(15,23,42,.22); backdrop-filter: blur(18px); }}
            .save-success-toast.show {{ display: flex; animation: floatInUp .28s ease both; }}
            .save-success-icon {{ width: 42px; height: 42px; border-radius: 16px; display: grid; place-items: center; color: #fff; background: linear-gradient(135deg, #16a34a, #22c55e); font-size: 22px; box-shadow: 0 12px 24px rgba(34,197,94,.24); }}
            .save-success-title {{ margin: 0; font-size: 13px; font-weight: 900; color: #0f172a; }}
            .save-success-text {{ margin: 2px 0 0; font-size: 11px; font-weight: 700; color: #64748b; }}
            .form-column.asiento-cerrado input,
            .form-column.asiento-cerrado textarea,
            .form-column.asiento-cerrado select {{ pointer-events: none; background-color: #f8fafc !important; opacity: .72; }}
            .form-column.asiento-cerrado button:not(#btnEditarComoDueno):not(#btnResumenCuaderno):not(.step-btn) {{ pointer-events: none; opacity: .55; }}

            /* Estilos del Panel de Pegado Inteligente */
            .col-header {{ background: #f8fafc; border: 1px solid #cbd5e1; border-bottom: none; border-radius: 8px 8px 0 0; padding: 8px; text-align: center; font-size: 11px; font-weight: 800; color: #475569; letter-spacing: 0.5px; }}
            .col-textarea {{ border-radius: 0 0 8px 8px; border: 1px solid #cbd5e1; font-size: 12px; line-height: 1.8; padding: 10px; resize: none; overflow-x: hidden; white-space: pre; background: #fff;}}
            .col-textarea:focus {{ border-color: #0263a0; box-shadow: 0 0 0 3px rgba(2,99,160,0.1); outline: none; }}
            .inicio-asiento-card {{ border: none; border-radius: 30px; overflow: hidden; box-shadow: 0 30px 80px rgba(15,23,42,0.28); background: rgba(255,255,255,0.96); backdrop-filter: blur(24px); }}
            .inicio-asiento-hero {{ background: linear-gradient(135deg, #0f172a, #0263a0); color: #fff; padding: 28px 34px; text-align: center; }}
            .inicio-asiento-icon {{ width: 62px; height: 62px; border-radius: 22px; display: grid; place-items: center; margin: 0 auto 14px; background: rgba(255,255,255,0.14); font-size: 30px; }}
            .inicio-asiento-hero h4 {{ margin: 0; font-weight: 800; letter-spacing: -0.4px; }}
            .inicio-asiento-hero p {{ margin: 8px 0 0; color: rgba(255,255,255,0.76); font-size: 13px; }}
            .inicio-asiento-body {{ padding: 30px 34px 34px; }}
            .inicio-input {{ border-radius: 16px !important; border: 1px solid #dbeafe !important; background: #f8fafc !important; font-weight: 800; }}
            .inicio-input:focus {{ border-color: #0263a0 !important; box-shadow: 0 0 0 4px rgba(2,99,160,0.12) !important; background: #fff !important; }}
            @media (max-width: 1200px) {{
                .stepper-container {{ left: 12px; width: 190px; padding-right: 26px; }}
                .split-layout {{ grid-template-columns: minmax(430px, .95fr) minmax(500px, 1.05fr); gap: 18px; margin-left: 214px; margin-right: 14px; }}
                .step-btn {{ min-height: 46px; padding-left: 44px; font-size: 9.8px; }}
                .step-label-short, .step-label-full {{ left: 44px; }}
            }}
            @media (min-width: 993px) and (max-width: 1180px) {{
                .preview-column .cuaderno-preview-pages {{ width: min(100%, 760px); }}
                .step-view {{ padding: 24px; }}
            }}
            @media (max-width: 992px) {{
                body {{ padding-bottom: 156px; overflow-x: hidden; }}
                .stepper-container {{ top: var(--nav-height); left: 0; width: 100%; max-height: none; border-radius: 0; border-left: 0; border-right: 0; padding: 12px 12px 15px; display: flex; flex-direction: row; gap: 8px; overflow-x: auto; overflow-y: hidden; white-space: nowrap; scroll-snap-type: x proximity; -webkit-overflow-scrolling: touch; background: rgba(255,255,255,.86); backdrop-filter: blur(18px); }}
                .stepper-container::before {{ display: none; }}
                .step-btn {{ flex: 0 0 auto; min-width: 132px; max-width: 174px; padding-right: 16px; scroll-snap-align: start; }}
                .step-btn::after {{ left: 12px; right: 12px; top: auto; bottom: -7px; width: auto; height: 3px; background: linear-gradient(90deg, #0284c7 var(--pct, 0%), #e2e8f0 0); }}
                .step-btn:hover {{ transform: translateX(6px) scale(1.02); }}
                .step-btn.active {{ transform: scale(1.02); margin: 0 2px; }}
                .sidebar-accordion {{ flex: 0 0 auto; }}
                .sidebar-accordion.open .sidebar-submenu {{ position: fixed; left: 12px; right: 12px; top: calc(var(--nav-height) + 58px); z-index: 950; display: flex; gap: 8px; max-height: 62px; padding: 8px; border-radius: 18px; background: rgba(255,255,255,.96); box-shadow: 0 18px 40px rgba(15,23,42,.14); }}
                .sidebar-sub-btn {{ flex: 1 1 0; width: auto; margin: 0; white-space: normal; }}
                .split-layout {{ display: block; max-width: 820px; margin: 132px auto 0 auto; padding: 0 14px; }}
                .form-column {{ max-width: none; width: 100%; }}
                #formResidencia input, #formResidencia textarea, #formResidencia select {{ font-size: 16px; }}
                .preview-column {{ display: none; }}
                .mobile-preview-btn {{ display: inline-flex; }}
                .step-view {{ padding: 22px; border-radius: 22px; }}
                .bottom-bar {{ padding: 10px 12px; gap: 8px; flex-wrap: wrap; align-items: center; }}
                .bottom-bar .btn {{ padding: 10px 14px !important; font-size: 12px; }}
                .asiento-actions {{ width: 100%; order: 3; justify-content: center; margin-left: 0; }}
                #moduloNavActions {{ flex: 1 1 auto; justify-content: flex-end; min-width: 0; }}
                .save-inline-status {{ order: 2; min-width: auto; flex: 1 1 160px; justify-content: center; }}
                .asiento-lock-banner {{ bottom: 90px; max-width: calc(100vw - 24px); border-radius: 18px; }}
            }}
            @media (max-width: 576px) {{
                body {{ padding-bottom: 182px; }}
                .stepper-container {{ padding: 10px 10px 13px; gap: 7px; }}
                .step-btn {{ min-width: 116px; max-width: 144px; min-height: 46px; font-size: 9.3px; border-radius: 15px; }}
                .step-label-full {{ font-size: 8.7px; }}
                .split-layout {{ margin: 124px auto 0 auto; padding: 0 10px; }}
                .step-view {{ padding: 18px 14px; border-radius: 20px; }}
                .step-title {{ font-size: 18px; margin-bottom: 18px; }}
                .bottom-bar {{ padding: 9px 10px; }}
                .bottom-bar .btn {{ flex: 1 1 auto; padding: 10px 11px !important; }}
                #btnAtras {{ flex: 0 0 auto; }}
                #moduloNavActions {{ width: 100%; order: 4; }}
                #moduloNavActions .btn {{ min-width: 0; }}
                .save-inline-status {{ width: 100%; order: 2; }}
                .mobile-preview-btn {{ right: 12px; bottom: 114px; padding: 11px 13px; }}
                .bottom-bar {{ align-items: stretch; justify-content: center; }}
                .bottom-bar .d-flex {{ gap: 6px !important; }}
                #btnAtras {{ flex: 1 1 100px; }}
                #moduloNavActions {{ width: 100%; order: 2; display: grid !important; grid-template-columns: 1fr 1.3fr; gap: 8px !important; }}
                #moduloNavActions.d-none {{ display: none !important; }}
                #moduloNavActions .btn {{ width: 100%; margin: 0; }}
                .asiento-actions .btn {{ flex: 1 1 100%; width: 100%; }}
            }}
        </style>
    </head>
    <body>
        {{{{ menu_superior | safe }}}}

        <div id="elegantAlert" class="elegant-alert"><div class="alert-icon" id="alertIcon"></div><div class="alert-text" id="alertText">Mensaje</div></div>
        <div class="save-success-toast" id="saveSuccessToast">
            <div class="save-success-icon"><i class="bi bi-check-lg"></i></div>
            <div>
                <p class="save-success-title" id="saveSuccessTitle">Guardado exitosamente</p>
                <p class="save-success-text" id="saveSuccessText">Abriendo resumen del cuaderno...</p>
            </div>
        </div>

        <div id="residenciaGlobalModal" class="hidden fixed inset-0 z-[2200] grid place-items-center bg-slate-950/70 p-4 backdrop-blur-md transition-opacity duration-150" role="dialog" aria-modal="true">
            <div id="residenciaGlobalModalCard" class="w-full max-w-md rounded-2xl bg-white p-6 opacity-0 shadow-2xl ring-1 ring-slate-200 transition-all duration-150 scale-95">
                <div id="residenciaGlobalModalIcon" class="mb-3 grid h-12 w-12 place-items-center rounded-2xl bg-green-50 text-2xl text-green-600">
                    <i class="bi bi-check-circle-fill"></i>
                </div>
                <h3 id="residenciaGlobalModalTitle" class="m-0 text-xl font-black tracking-tight text-slate-900">Guardado exitosamente</h3>
                <p id="residenciaGlobalModalMessage" class="mb-5 mt-2 text-sm font-semibold leading-6 text-slate-600">Abriendo resumen del cuaderno...</p>
                <div class="flex justify-end">
                    <button id="residenciaGlobalModalOk" type="button" class="rounded-2xl bg-blue-600 px-4 py-3 text-sm font-black text-white shadow-lg shadow-blue-600/20 transition hover:scale-[1.02] hover:bg-blue-700">Continuar</button>
                </div>
            </div>
        </div>

        <input type="hidden" id="initNumAsiento" value="">
        <input type="hidden" id="initFecha" value="{fecha_hoy_iso}">

        <div class="modal fade" id="modalPegadoInteligente" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-xl">
                <div class="modal-content" style="border-radius: 20px; border: none; box-shadow: 0 25px 50px rgba(0,0,0,0.2);">
                    <div class="modal-header border-0 bg-light pb-3">
                        <h5 class="modal-title fw-bold text-dark"><i class="bi bi-layout-three-columns text-success me-2"></i> Catálogo Maestro de Partidas</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body p-4 bg-white">
                        <p class="small text-muted mb-3 text-center">
                            <i class="bi bi-info-circle-fill text-primary"></i> 
                            Pegue las columnas desde el Expediente Técnico. <b>Esto SOLO alimentará el buscador, NO se escribirá en el cuaderno de hoy.</b>
                        </p>
                        <div class="row g-2">
                            <div class="col-2">
                                <div class="col-header">1. ÍTEMS</div>
                                <textarea id="p_items" class="form-control col-textarea text-center fw-bold" rows="12" placeholder="Pegar..." onpaste="handleSmartPaste(event, 'p_items')" onscroll="sincronizarScroll('p_items')"></textarea>
                            </div>
                            <div class="col-6">
                                <div class="col-header">2. DESCRIPCIÓN DE PARTIDAS</div>
                                <textarea id="p_descs" class="form-control col-textarea fw-semibold text-dark" rows="12" placeholder="Pegar..." onpaste="handleSmartPaste(event, 'p_descs')" onscroll="sincronizarScroll('p_descs')"></textarea>
                            </div>
                            <div class="col-2">
                                <div class="col-header">3. UNIDADES</div>
                                <textarea id="p_unds" class="form-control col-textarea text-center" rows="12" placeholder="Pegar..." onpaste="handleSmartPaste(event, 'p_unds')" onscroll="sincronizarScroll('p_unds')"></textarea>
                            </div>
                            <div class="col-2">
                                <div class="col-header text-primary">4. METRADO TOTAL (Opcional)</div>
                                <textarea id="p_mets" class="form-control col-textarea text-center fw-bold text-primary" rows="12" placeholder="Pegar..." onpaste="handleSmartPaste(event, 'p_mets')" onscroll="sincronizarScroll('p_mets')"></textarea>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer border-0 pt-0 bg-white d-flex justify-content-between">
                        <button type="button" class="btn btn-light rounded-pill px-4 fw-bold" onclick="limpiarGrilla()">Limpiar Cuadros</button>
                        <div>
                            <span class="text-muted small fw-semibold me-3">En memoria: <span id="lbl_total_cat" class="text-primary">0</span></span>
                            <button type="button" class="btn btn-primary rounded-pill px-5 fw-bold shadow-sm" onclick="procesarCatalogoGlobal()">Guardar en Memoria</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="stepper-container" id="stepperBar">
            <button type="button" class="step-btn active" id="btnStep1" data-step="1" data-percent="0%" onclick="window.irModulo(1)"><i class="bi bi-calendar-check step-main-icon"></i><span class="step-label-short">JORNAL</span><span class="step-label-full">JORNAL DE TRABAJO</span></button>
            <div class="sidebar-accordion" id="sidebarM2Accordion">
                <button type="button" class="step-btn accordion-toggle" id="btnStep2" data-step="2" data-percent="0%" onclick="toggleModulo2Sidebar(event)">
                    <i class="bi bi-people-fill step-main-icon"></i>
                    <span class="step-label-short">PERSONAL</span>
                    <span class="step-label-full">PERSONAL DE OBRA</span>
                    <i class="bi bi-chevron-down accordion-caret"></i>
                </button>
                <div class="sidebar-submenu" id="sidebarM2Submenu">
                    <button type="button" class="sidebar-sub-btn" onclick="abrirSubModuloPersonal('m2_panel_gastos')">Gastos Generales</button>
                    <button type="button" class="sidebar-sub-btn" onclick="abrirSubModuloPersonal('m2_panel_directo')">Costo Directo</button>
                </div>
            </div>
            <button type="button" class="step-btn" id="btnStep3" data-step="3" data-percent="0%" onclick="window.irModulo(3)"><i class="bi bi-list-check step-main-icon"></i><span class="step-label-short">PARTIDAS</span><span class="step-label-full">PARTIDAS EJECUTADAS</span></button>
            <button type="button" class="step-btn" id="btnStep4" data-step="4" data-percent="0%" onclick="window.irModulo(4)"><i class="bi bi-rulers step-main-icon"></i><span class="step-label-short">METRADO</span><span class="step-label-full">MAYOR METRADO</span></button>
            <button type="button" class="step-btn" id="btnStep5" data-step="5" data-percent="0%" onclick="window.irModulo(5)"><i class="bi bi-diagram-3 step-main-icon"></i><span class="step-label-short">SUB PART.</span><span class="step-label-full">SUB PARTIDAS</span></button>
            <button type="button" class="step-btn" id="btnStep6" data-step="6" data-percent="0%" onclick="window.irModulo(6)"><i class="bi bi-clipboard2-check step-main-icon"></i><span class="step-label-short">ACTIVID.</span><span class="step-label-full">ACTIVIDADES</span></button>
            <button type="button" class="step-btn" id="btnStep7" data-step="7" data-percent="0%" onclick="window.irModulo(7)"><i class="bi bi-box-seam step-main-icon"></i><span class="step-label-short">ALMACEN</span><span class="step-label-full">ALMACEN</span></button>
            <button type="button" class="step-btn" id="btnStep8" data-step="8" data-percent="0%" onclick="window.irModulo(8)"><i class="bi bi-truck step-main-icon"></i><span class="step-label-short">MAQUIN.</span><span class="step-label-full">EQUIPO MECANICO</span></button>
            <button type="button" class="step-btn" id="btnStep9" data-step="9" data-percent="0%" onclick="window.irModulo(9)"><i class="bi bi-tools step-main-icon"></i><span class="step-label-short">HERRAM.</span><span class="step-label-full">HERRAMIENTAS</span></button>
            <button type="button" class="step-btn" id="btnStep10" data-step="10" data-percent="0%" onclick="window.irModulo(10)"><i class="bi bi-chat-square-text step-main-icon"></i><span class="step-label-short">OCURRENC.</span><span class="step-label-full">OCURRENCIAS</span></button>
            <button type="button" class="step-btn resumen" id="btnResumenCuaderno" data-percent="Ver" onclick="abrirResumenCuaderno()"><i class="bi bi-journal-text step-main-icon"></i><span class="step-label-short">RESUMEN</span><span class="step-label-full">RESUMEN DEL CUADERNO</span></button>
        </div>
        <div id="globalTooltip"></div>

        <div class="split-layout" id="mainLayout">
            <div class="form-column">
                <form id="formResidencia" onsubmit="event.preventDefault();">
                    {JORNAL_HTML}
                    {PERSONAL_HTML}
                    {PARTIDAS_HTML}
                    {MAYOR_METRADO_HTML}
                    {SUB_PARTIDAS_HTML}
                    {ACTIVIDADES_HTML}
                    {ALMACEN_HTML}
                    {MAQUINARIA_HTML}
                    {HERRAMIENTAS_HTML}
                    {OCURRENCIAS_HTML}
                </form>
            </div>

            <div class="preview-column">
                {cuaderno_obra_html}
            </div>
        </div>

        <div class="bottom-bar shadow-lg" id="bottomBarUI">
            <button type="button" id="btnAtras" class="btn btn-light border fw-bold rounded-pill px-4 text-dark shadow-sm d-none" onclick="window.anteriorModulo()"><i class="bi bi-arrow-left"></i> Anterior</button>
            <div class="asiento-actions" id="asientoActions">
                <button type="button" class="btn btn-warning fw-bold rounded-pill px-4 shadow-sm" onclick="window.mostrarConfirmarGuardarBorrador()"><i class="bi bi-save2"></i> Guardar como Borrador</button>
                <button type="button" class="btn btn-success fw-bold rounded-pill px-4 shadow-sm" id="btnEnviarInspector" onclick="window.mostrarConfirmarCerrarAsiento()"><i class="bi bi-send-check-fill"></i> Enviar a Inspector</button>
                <button type="button" class="btn btn-dark fw-bold rounded-pill px-4 shadow-sm d-none" id="btnEditarComoDueno" onclick="habilitarEdicionComoDueno()"><i class="bi bi-unlock-fill"></i> Editar como dueño</button>
            </div>
            <div class="save-inline-status" id="saveInlineStatus" aria-live="polite"><i class="bi bi-check2-circle"></i><span>Guardado local</span></div>
            <div class="d-flex gap-2 align-items-center ms-auto" id="moduloNavActions">
                <button type="button" class="btn btn-outline-secondary fw-bold rounded-pill px-4" onclick="window.omitirModulo()">Omitir</button>
                <button type="button" class="btn btn-dark fw-bold rounded-pill px-4" id="btnGuardarContinuar" onclick="window.guardarYContinuarModulo()">Guardar y Continuar <i class="bi bi-arrow-right"></i></button>
            </div>
        </div>
        <div class="asiento-lock-banner" id="asientoLockBanner"><i class="bi bi-lock-fill"></i> Asiento firmado. La edición de Residencia está bloqueada.</div>

        <div class="confirm-seat-overlay" id="confirmAccionAsiento">
            <div class="confirm-seat-card">
                <div class="confirm-seat-hero" id="confirmAccionHero">
                    <div class="icon" id="confirmAccionIcon"><i class="bi bi-shield-lock-fill"></i></div>
                    <h5 id="confirmAccionTitulo">Enviar asiento al Inspector</h5>
                    <p id="confirmAccionSubtitulo">Antes de enviar, revise que la información registrada sea correcta.</p>
                </div>
                <div class="confirm-seat-body">
                    <div class="confirm-seat-warning" id="confirmAccionMensaje">
                        <i class="bi bi-exclamation-triangle-fill me-1"></i>
                        Al enviar el asiento quedará listo para firma del Inspector. Podrá corregirse desde el resumen hasta que la firma sea estampada.
                    </div>
                    <div class="confirm-seat-actions">
                        <button type="button" class="confirm-seat-btn cancel" id="confirmAccionCancelar" onclick="window.ocultarConfirmarAccionAsiento()">Cancelar</button>
                        <button type="button" class="confirm-seat-btn primary" id="confirmAccionBoton" onclick="window.confirmarAccionAsiento()">Sí, enviar a firma</button>
                    </div>
                </div>
            </div>
        </div>

        <div class="confirm-seat-overlay" id="modalBorradorGuardado">
            <div class="confirm-seat-card">
                <div class="confirm-seat-hero draft">
                    <div class="icon"><i class="bi bi-check-circle-fill"></i></div>
                    <h5>Borrador guardado correctamente</h5>
                    <p>El asiento fue guardado en la base de datos.</p>
                </div>
                <div class="confirm-seat-body">
                    <div class="confirm-seat-actions">
                        <button type="button" class="confirm-seat-btn primary draft" onclick="window.seguirAsentandoOtroDia()">Seguir asentando otro día</button>
                        <button type="button" class="confirm-seat-btn cancel" onclick="window.cerrarModalBorradorGuardado()">Cerrar</button>
                    </div>
                </div>
            </div>
        </div>

        <button type="button" class="mobile-preview-btn" id="mobilePreviewBtn" onclick="abrirResumenCuaderno()">
            <i class="bi bi-journal-text"></i> Ver cuaderno
        </button>

        {RESUMEN_ASIENTO_HTML}

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            function samuTieneParametrosAsiento() {{
                const params = new URLSearchParams(window.location.search || '');
                return !!(params.get('fecha') && params.get('asiento'));
            }}
            function abrirModalInicialSeguro() {{
                if (samuTieneParametrosAsiento()) return;
                window.location.href = '/cuaderno';
            }}
            function cerrarModalInicialSeguro() {{
                document.body.classList.remove('modal-open');
                document.body.style.removeProperty('overflow');
                document.body.style.removeProperty('padding-right');
                document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
            }}
            window.iniciarAsiento = function() {{
                const inputNumero = document.getElementById('initNumAsiento');
                const inputFecha = document.getElementById('initFecha');
                const numero = (inputNumero && inputNumero.value ? inputNumero.value : '').trim();
                const fecha = inputFecha ? inputFecha.value : '';
                if (!numero || !fecha) {{
                    const alerta = document.getElementById('elegantAlert');
                    const texto = document.getElementById('alertText');
                    const icono = document.getElementById('alertIcon');
                    if (texto) texto.innerText = 'Complete los datos para iniciar.';
                    if (icono) icono.innerHTML = '<i class="bi bi-exclamation-circle-fill text-danger"></i>';
                    if (alerta) {{
                        alerta.classList.add('show');
                        setTimeout(() => alerta.classList.remove('show'), 3000);
                    }}
                    return;
                }}

                const dias = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO", "DOMINGO"];
                const partes = fecha.split('-');
                const fechaObj = new Date(partes[0], partes[1] - 1, partes[2]);
                let diaIndex = fechaObj.getDay() - 1;
                if (diaIndex === -1) diaIndex = 6;

                window.g_numAsiento = numero;
                window.g_fechaRaw = fecha;
                window.g_fechaAsiento = `${{dias[diaIndex]}}, ${{partes[2]}}/${{partes[1]}}/${{partes[0]}}`;

                const fechaCuaderno = document.getElementById('lbl_hoja_fecha');
                if (fechaCuaderno) fechaCuaderno.innerText = window.g_fechaAsiento;
                document.dispatchEvent(new CustomEvent('asiento:init', {{
                    detail: {{
                        numero: window.g_numAsiento,
                        fechaRaw: window.g_fechaRaw,
                        fechaTexto: window.g_fechaAsiento
                    }}
                }}));

                cerrarModalInicialSeguro();

                const activarRegistro = () => {{
                    document.getElementById('mainLayout')?.classList.add('unlocked');
                    const stepper = document.getElementById('stepperBar');
                    if (stepper) {{
                        stepper.style.opacity = '1';
                        stepper.style.pointerEvents = 'all';
                    }}
                    document.getElementById('bottomBarUI')?.classList.add('unlocked');
                    document.getElementById('mobilePreviewBtn')?.classList.add('unlocked');
                    document.getElementById('step1')?.classList.add('active');
                    document.getElementById('btnStep1')?.classList.add('active');
                    if (typeof sincronizarDatos === 'function') sincronizarDatos();
                    if (typeof actualizarAccionesAsiento === 'function') actualizarAccionesAsiento();
                    if (typeof verificarEstadoAsientoGuardado === 'function') verificarEstadoAsientoGuardado();
                }};
                requestAnimationFrame(activarRegistro);
                setTimeout(activarRegistro, 80);
            }};
            window.iniciarAsientoSeguro = window.iniciarAsiento;
            window.samuCurrentStep = 1;
            window.irModulo = function(stepIndex) {{
                const step = Math.max(1, Math.min(10, parseInt(stepIndex, 10) || 1));
                window.samuCurrentStep = step;
                document.querySelectorAll('.step-view').forEach(view => view.classList.remove('active', 'exit'));
                document.querySelectorAll('.step-btn').forEach(btn => btn.classList.remove('active'));
                document.getElementById(`step${{step}}`)?.classList.add('active');
                document.getElementById(`btnStep${{step}}`)?.classList.add('active');
                const btnAtras = document.getElementById('btnAtras');
                if (btnAtras) btnAtras.classList.toggle('d-none', step <= 1);
                document.dispatchEvent(new CustomEvent('modulo:cambio', {{ detail: {{ step }} }}));
                if (typeof sincronizarDatos === 'function') sincronizarDatos();
                if (typeof actualizarAccionesAsiento === 'function') actualizarAccionesAsiento();
            }};
            window.siguienteModulo = function() {{
                if (window.g_numAsiento && typeof autoGuardarBorrador === 'function') {{
                    try {{ autoGuardarBorrador(); }} catch (e) {{}}
                }}
                window.irModulo((window.samuCurrentStep || 1) + 1);
            }};
            window.anteriorModulo = function() {{
                window.irModulo((window.samuCurrentStep || 1) - 1);
            }};
            window.toggleModulo2Sidebar = function(event) {{
                if (event) event.preventDefault();
                const accordion = document.getElementById('sidebarM2Accordion');
                const wasOpen = accordion?.classList.contains('open');
                window.irModulo(2);
                accordion?.classList.toggle('open', !wasOpen);
            }};
            window.abrirSubModuloPersonal = function(panelId) {{
                window.irModulo(2);
                document.getElementById('sidebarM2Accordion')?.classList.add('open');
                setTimeout(() => {{
                    const panel = document.getElementById(panelId);
                    if (!panel) return;
                    panel.classList.remove('closed');
                    panel.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                }}, 120);
            }};
            document.addEventListener('DOMContentLoaded', function() {{
                document.getElementById('formResidencia')?.addEventListener('input', function() {{
                    if (typeof sincronizarDatos === 'function') sincronizarDatos();
                }});
                document.getElementById('formResidencia')?.addEventListener('change', function() {{
                    if (typeof sincronizarDatos === 'function') sincronizarDatos();
                }});
            }});
            abrirModalInicialSeguro();
        </script>
        
        <script>
            // CONFIGURACIÓN GLOBAL
            let g_numAsiento = ""; let g_fechaAsiento = ""; let g_fechaRaw = "";
            let currentStep = 1; const totalSteps = 10; let isAnimating = false;
            const rolUsuario = "{session.get('rol', '')}";
            let asientoCerrado = false;
            let edicionDuenoActiva = false;
            document.addEventListener('asiento:init', function(event) {{
                const detalle = event.detail || {{}};
                g_numAsiento = detalle.numero || "";
                g_fechaRaw = detalle.fechaRaw || "";
                g_fechaAsiento = detalle.fechaTexto || "";
                currentStep = 1;
            }});
            document.addEventListener('modulo:cambio', function(event) {{
                currentStep = (event.detail && event.detail.step) ? event.detail.step : 1;
                isAnimating = false;
            }});
            const stepLabels = {{
                1: 'Jornal de trabajo', 2: 'Personal de obra', 3: 'Partidas ejecutadas',
                4: 'Mayor metrado', 5: 'Sub partidas', 6: 'Actividades',
                7: 'Almacén', 8: 'Maquinaria', 9: 'Herramientas', 10: 'Ocurrencias'
            }};
            
            // EL CATÁLOGO MAESTRO (Accesible para todos) Y LAS LISTAS DIARIAS
            window.catalogoMaestro = [];
            window.m3_lista = []; window.m4_lista = []; window.m5_lista = []; window.m6_lista = [];

            function mostrarAlerta(mensaje, tipo="error") {{
                const alerta = document.getElementById('elegantAlert'); const icono = document.getElementById('alertIcon');
                document.getElementById('alertText').innerText = mensaje;
                if(tipo === "error") {{ icono.innerHTML = '<i class="bi bi-exclamation-circle-fill text-danger"></i>'; }} 
                else {{ icono.innerHTML = '<i class="bi bi-check-circle-fill text-success"></i>'; }}
                alerta.classList.add('show'); setTimeout(() => {{ alerta.classList.remove('show'); }}, 3500);
            }}

            function mostrarModalResidencia(title, message, type="success", autoCloseMs=900) {{
                return new Promise(resolve => {{
                    const overlay = document.getElementById('residenciaGlobalModal');
                    const card = document.getElementById('residenciaGlobalModalCard');
                    const icon = document.getElementById('residenciaGlobalModalIcon');
                    const titleEl = document.getElementById('residenciaGlobalModalTitle');
                    const messageEl = document.getElementById('residenciaGlobalModalMessage');
                    const okBtn = document.getElementById('residenciaGlobalModalOk');
                    const classes = {{
                        success: 'mb-3 grid h-12 w-12 place-items-center rounded-2xl bg-green-50 text-2xl text-green-600',
                        error: 'mb-3 grid h-12 w-12 place-items-center rounded-2xl bg-red-50 text-2xl text-red-600',
                        warning: 'mb-3 grid h-12 w-12 place-items-center rounded-2xl bg-amber-50 text-2xl text-amber-600'
                    }};
                    icon.className = classes[type] || classes.success;
                    icon.innerHTML = type === "error" ? '<i class="bi bi-exclamation-circle-fill"></i>' : '<i class="bi bi-check-circle-fill"></i>';
                    titleEl.textContent = title;
                    messageEl.textContent = message;
                    const cerrar = () => {{
                        card.classList.add('opacity-0', 'scale-95');
                        setTimeout(() => {{
                            overlay.classList.add('hidden');
                            okBtn.onclick = null;
                            resolve(true);
                        }}, 150);
                    }};
                    okBtn.onclick = cerrar;
                    overlay.classList.remove('hidden');
                    requestAnimationFrame(() => card.classList.remove('opacity-0', 'scale-95'));
                    if (autoCloseMs) setTimeout(cerrar, autoCloseMs);
                }});
            }}

            document.addEventListener("DOMContentLoaded", function() {{
                abrirModalInicialSeguro();
                instalarTooltipStepper();
                actualizarStepper();
            }});
            function formatearFecha(fechaStr) {{ const dias = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO", "DOMINGO"]; const [y, m, d] = fechaStr.split('-'); const dateObj = new Date(y, m-1, d); let dayIndex = dateObj.getDay() - 1; if(dayIndex === -1) dayIndex = 6; return `${{dias[dayIndex]}}, ${{d}}/${{m}}/${{y}}`; }}
            
            function iniciarAsiento() {{ window.iniciarAsientoSeguro(); }}

            function porcentajePaso(step) {{
                const scope = document.getElementById(`step${{step}}`);
                if(!scope) return 0;
                const reqs = Array.from(scope.querySelectorAll(`[class*="req-step${{step}}"]`));
                if(reqs.length === 0) return step < currentStep ? 100 : 0;
                const llenos = reqs.filter(el => String(el.value || '').trim().length > 0).length;
                return Math.round((llenos / reqs.length) * 100);
            }}

            function actualizarStepper() {{
                for(let i = 1; i <= totalSteps; i++) {{
                    const btn = document.getElementById(`btnStep${{i}}`);
                    if(!btn) continue;
                    const pct = porcentajePaso(i);
                    btn.dataset.percent = `${{pct}}%`;
                    btn.style.setProperty('--pct', `${{pct}}%`);
                    btn.classList.toggle('completed', pct >= 100);
                    btn.classList.toggle('missing', pct > 0 && pct < 100);
                    const estado = pct >= 100 ? 'Completo' : (pct > 0 ? `Falta ${{100 - pct}}%` : 'Sin registrar');
                    btn.dataset.tooltip = `${{stepLabels[i]}} · ${{estado}} · Avance ${{pct}}%`;
                }}
            }}

            function instalarTooltipStepper() {{
                const tooltip = document.getElementById('globalTooltip');
                document.querySelectorAll('.step-btn').forEach(btn => {{
                    btn.addEventListener('mouseenter', () => {{
                        const text = btn.dataset.tooltip || '';
                        if (!text) return;
                        tooltip.innerText = text;
                        const rect = btn.getBoundingClientRect();
                        tooltip.style.left = `${{rect.right + 14}}px`;
                        tooltip.style.top = `${{rect.top + rect.height / 2 - tooltip.offsetHeight / 2}}px`;
                        tooltip.classList.add('visible');
                    }});
                    btn.addEventListener('mousemove', () => {{
                        const rect = btn.getBoundingClientRect();
                        tooltip.style.left = `${{rect.right + 14}}px`;
                        tooltip.style.top = `${{rect.top + rect.height / 2 - tooltip.offsetHeight / 2}}px`;
                    }});
                    btn.addEventListener('mouseleave', () => {{
                        tooltip.classList.remove('visible');
                    }});
                }});
            }}

            // LÓGICA DEL CATÁLOGO GLOBAL (PEGADO DE 4 COLUMNAS)
            function abrirModalPegadoInteligente() {{ new bootstrap.Modal(document.getElementById('modalPegadoInteligente')).show(); }}
            function sincronizarScroll(sourceId) {{ const source = document.getElementById(sourceId); const textareas = ['p_items', 'p_descs', 'p_unds', 'p_mets']; textareas.forEach(id => {{ if(id !== sourceId) document.getElementById(id).scrollTop = source.scrollTop; }}); }}
            function limpiarGrilla() {{ document.getElementById('p_items').value = ''; document.getElementById('p_descs').value = ''; document.getElementById('p_unds').value = ''; document.getElementById('p_mets').value = ''; }}
            
            function handleSmartPaste(e, targetId) {{
                let pasteData = (e.clipboardData || window.clipboardData).getData('text');
                if(pasteData.includes('\\t')) {{
                    e.preventDefault(); const rows = pasteData.split('\\n');
                    let i_arr=[], d_arr=[], u_arr=[], m_arr=[];
                    rows.forEach(row => {{
                        if(!row.trim()) return; const cols = row.split('\\t');
                        if (targetId === 'p_items') {{ i_arr.push(cols[0]||''); d_arr.push(cols[1]||''); u_arr.push(cols[2]||''); m_arr.push(cols[3]||''); }} 
                        else if (targetId === 'p_descs') {{ d_arr.push(cols[0]||''); u_arr.push(cols[1]||''); m_arr.push(cols[2]||''); }}
                    }});
                    if (targetId === 'p_items') {{
                        if(i_arr.length) document.getElementById('p_items').value += (document.getElementById('p_items').value ? '\\n' : '') + i_arr.join('\\n');
                        if(d_arr.length) document.getElementById('p_descs').value += (document.getElementById('p_descs').value ? '\\n' : '') + d_arr.join('\\n');
                        if(u_arr.length) document.getElementById('p_unds').value += (document.getElementById('p_unds').value ? '\\n' : '') + u_arr.join('\\n');
                        if(m_arr.length) document.getElementById('p_mets').value += (document.getElementById('p_mets').value ? '\\n' : '') + m_arr.join('\\n');
                    }} else if (targetId === 'p_descs') {{
                        if(d_arr.length) document.getElementById('p_descs').value += (document.getElementById('p_descs').value ? '\\n' : '') + d_arr.join('\\n');
                        if(u_arr.length) document.getElementById('p_unds').value += (document.getElementById('p_unds').value ? '\\n' : '') + u_arr.join('\\n');
                        if(m_arr.length) document.getElementById('p_mets').value += (document.getElementById('p_mets').value ? '\\n' : '') + m_arr.join('\\n');
                    }}
                }}
            }}

            // ESTO SOLO ALIMENTA LA BASE DE DATOS (NO EL CUADERNO)
            function procesarCatalogoGlobal() {{
                const items = document.getElementById('p_items').value.split('\\n');
                const descs = document.getElementById('p_descs').value.split('\\n');
                const unds = document.getElementById('p_unds').value.split('\\n');
                const mets = document.getElementById('p_mets').value.split('\\n');
                let maxRows = Math.max(items.length, descs.length, unds.length, mets.length);
                let count = 0;
                for(let i = 0; i < maxRows; i++) {{
                    let desc = (descs[i] || '').trim();
                    if(!desc) continue; 
                    let item = (items[i] || '').trim() || '-';
                    let und = (unds[i] || '').trim().toUpperCase() || 'GLB';
                    let met = (mets[i] || '').trim();
                    window.catalogoMaestro.push({{ item: item, descripcion: desc, unidad: und, metrado_total: met }});
                    count++;
                }}
                if(count > 0) {{
                    limpiarGrilla();
                    document.getElementById('lbl_total_cat').innerText = window.catalogoMaestro.length;
                    bootstrap.Modal.getInstance(document.getElementById('modalPegadoInteligente')).hide();
                    mostrarAlerta(`Se guardaron ${{count}} partidas en la memoria del proyecto.`, "success");
                }}
            }}

            // NAVEGACIÓN Y UX
            function jumpToStep(stepIndex) {{ if (isAnimating || currentStep === stepIndex) return; isAnimating = true; const currentView = document.getElementById(`step${{currentStep}}`); currentView.classList.remove('active'); currentView.classList.add('exit'); document.getElementById(`btnStep${{currentStep}}`).classList.remove('active'); setTimeout(() => {{ currentView.classList.remove('exit'); currentStep = stepIndex; window.samuCurrentStep = stepIndex; document.getElementById(`step${{currentStep}}`).classList.add('active'); document.getElementById(`btnStep${{currentStep}}`).classList.add('active'); const btnAtras = document.getElementById('btnAtras'); if (currentStep > 1) btnAtras.classList.remove('d-none'); else btnAtras.classList.add('d-none'); actualizarAccionesAsiento(); if (typeof sincronizarDatos === "function") sincronizarDatos(); if (typeof guardarEstadoLocal === "function") guardarEstadoLocal(); isAnimating = false; }}, 300); }}
            function siguientePaso() {{ if (g_numAsiento && !asientoCerrado) autoGuardarBorrador(); if(currentStep < totalSteps) jumpToStep(currentStep + 1); }} function anteriorPaso() {{ if(currentStep > 1) jumpToStep(currentStep - 1); }} function omitirPaso() {{ siguientePaso(); }}

            function actualizarAccionesAsiento() {{
                const acciones = document.getElementById('asientoActions');
                if (acciones) acciones.classList.toggle('visible', currentStep > 1);
                document.getElementById('btnEnviarInspector')?.classList.toggle('d-none', currentStep !== 10);
                const navegacion = document.getElementById('moduloNavActions');
                if (navegacion) navegacion.classList.toggle('d-none', currentStep === 10);
                const btnAtras = document.getElementById('btnAtras');
                if (btnAtras) btnAtras.classList.toggle('d-none', currentStep <= 1);
                const btnDueno = document.getElementById('btnEditarComoDueno');
                if (btnDueno) btnDueno.classList.toggle('d-none', !(asientoCerrado && rolUsuario === 'Admin'));
            }}

            function avanceAsiento() {{
                let suma = 0;
                for (let i = 1; i <= totalSteps; i++) suma += porcentajePaso(i);
                return Math.round(suma / totalSteps);
            }}

            function contenidoAsiento() {{
                const modulos = typeof redactarModulosCuaderno === 'function' ? redactarModulosCuaderno() : [];
                return {{
                    numero: g_numAsiento,
                    fecha: g_fechaRaw,
                    fecha_texto: g_fechaAsiento,
                    avance: avanceAsiento(),
                    modulos: modulos,
                    texto_html: document.getElementById('papelOficial')?.innerHTML || '',
                    datos: {{
                        jornal_m: document.getElementById('v_jornal_m')?.value || '',
                        jornal_t: document.getElementById('v_jornal_t')?.value || '',
                        clima: document.getElementById('v_clima')?.value || '',
                        personal: {{
                            operario: document.getElementById('v_oper')?.value || '',
                            oficiales: document.getElementById('v_ofic')?.value || '',
                            peones: document.getElementById('v_peon')?.value || '',
                            mecanicos: document.getElementById('v_meca')?.value || '',
                            controladores: document.getElementById('v_ctrl')?.value || '',
                            operadores: document.getElementById('v_ope_maq')?.value || ''
                        }},
                        personal_gastos_generales: window.m2_gastos_generales || [],
                        m3: window.m3_lista || [],
                        m4: window.m4_lista || [],
                        m5: window.m5_lista || [],
                        m6: window.m6_lista || [],
                        almacen: document.getElementById('v_almacen')?.value || '',
                        maquinaria: document.getElementById('v_maquina')?.value || '',
                        herramientas: document.getElementById('v_herram')?.value || '',
                        ocurrencia: document.getElementById('v_ocurrencia')?.value || ''
                    }}
                }};
            }}

            function mensajeErrorServidor(resp, data=null) {{
                const detalle = data?.message || data?.error || data?.detail;
                if (detalle) return `Error: ${{detalle}}`;
                if (!resp || !resp.ok) return `Error en el servidor (${{resp?.status || 500}})`;
                return 'No se pudo guardar el asiento.';
            }}

            function esErrorDeRed(error) {{
                const mensaje = String(error?.message || error || '');
                return error instanceof TypeError || /Failed to fetch|NetworkError|Load failed|fetch/i.test(mensaje);
            }}

            function mensajeErrorFetch(error) {{
                return esErrorDeRed(error) ? 'Sin conexión' : (error?.message || 'Error inesperado al guardar.');
            }}

            async function leerJsonSeguro(resp) {{
                return await resp.json().catch(() => ({{ ok: false, error: 'Respuesta inválida del servidor' }}));
            }}

            async function enviarAsiento(estado, silencioso=false) {{
                if (!g_numAsiento || !g_fechaRaw) {{
                    if (!silencioso) mostrarAlerta("Primero inicie el asiento con número y fecha.", "error");
                    return null;
                }}
                if (asientoCerrado && !edicionDuenoActiva && rolUsuario !== 'Admin') {{
                    if (!silencioso) mostrarAlerta("Este asiento ya fue enviado o cerrado y no puede modificarse.", "error");
                    return null;
                }}
                if (typeof sincronizarDatos === "function") sincronizarDatos();
                const payload = {{
                    numero: g_numAsiento,
                    fecha: g_fechaRaw,
                    estado: estado,
                    avance: avanceAsiento(),
                    modulo_activo: window.samuCurrentStep || 1,
                    contenido: contenidoAsiento()
                }};
                try {{
                    const resp = await fetch('/residencia/api/asiento', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(payload)
                    }});
                    const data = await leerJsonSeguro(resp);
                    if (!resp.ok || !data.ok) {{
                        if (!silencioso) mostrarAlerta(mensajeErrorServidor(resp, data), "error");
                        return null;
                    }}
                    return data;
                }} catch (error) {{
                    if (!silencioso) mostrarAlerta(mensajeErrorFetch(error), "error");
                    return null;
                }}
            }}

            async function autoGuardarBorrador() {{
                try {{ await enviarAsiento('Borrador', true); }} catch (e) {{ /* El guardado manual mostrará cualquier problema de conexión. */ }}
            }}

            async function guardarBorradorAsiento() {{
                const data = await enviarAsiento('Borrador');
                if (!data) return;
                asientoCerrado = false;
                mostrarAlerta(`Borrador guardado. Avance ${{data.avance}}%.`, "success");
            }}
            window.guardarBorradorAsiento = guardarBorradorAsiento;

            async function cerrarAsiento() {{
                if (typeof window.mostrarConfirmarCerrarAsiento === 'function') {{
                    window.mostrarConfirmarCerrarAsiento();
                }}
            }}
            window.cerrarAsiento = cerrarAsiento;

            function bloquearEdicionAsiento() {{
                document.querySelector('.form-column')?.classList.add('asiento-cerrado');
                document.getElementById('asientoLockBanner')?.classList.add('visible');
                actualizarAccionesAsiento();
            }}

            function habilitarEdicionComoDueno() {{
                if (rolUsuario !== 'Admin') return;
                edicionDuenoActiva = true;
                asientoCerrado = false;
                document.querySelector('.form-column')?.classList.remove('asiento-cerrado');
                document.getElementById('asientoLockBanner')?.classList.remove('visible');
                actualizarAccionesAsiento();
                mostrarAlerta("Edición de dueño habilitada para este asiento.", "success");
            }}

            async function verificarEstadoAsientoGuardado() {{
                if (!g_numAsiento) return;
                const resp = await fetch(`/residencia/api/asiento/${{encodeURIComponent(g_numAsiento)}}`);
                const data = await resp.json().catch(() => null);
                const asiento = data && data.ok ? data.asiento : null;
                if (!asiento) return;
                if (['Cerrado', 'Firmado'].includes(asiento.estado) || (asiento.bloqueado && asiento.estado !== 'Enviado Inspector')) {{
                    asientoCerrado = true;
                    bloquearEdicionAsiento();
                    mostrarAlerta("Este asiento ya fue enviado o cerrado. Se abrió en modo solo lectura.", "success");
                }} else {{
                    mostrarAlerta(`Borrador existente encontrado. Avance guardado ${{asiento.avance || 0}}%.`, "success");
                }}
            }}

            let t_m = true; let t_t = true;
            function toggleTurno(turno) {{ if(turno === 'm') {{ t_m = !t_m; document.getElementById('card_m').classList.toggle('active', t_m); document.getElementById('hora_jornal_m').style.opacity = t_m ? "1" : "0.3"; }} else {{ t_t = !t_t; document.getElementById('card_t').classList.toggle('active', t_t); document.getElementById('hora_jornal_t').style.opacity = t_t ? "1" : "0.3"; }} if (typeof m1_actualizar_jornal === "function") m1_actualizar_jornal(); else sincronizarDatos(); }}
            function evaluarTarjeta(id) {{ const val = document.getElementById('v_' + id).value; document.getElementById('c_' + id).classList.toggle('active', val > 0); sincronizarDatos(); }}

            {CUADERNO_OBRA_JS}

            function samuListaModulo(nombre) {{
                const lista = window[nombre];
                return Array.isArray(lista) ? lista : [];
            }}

            function samuValor(id, saltos=false) {{
                const el = document.getElementById(id);
                if (!el) return '';
                const texto = String(el.value || '').trim();
                return saltos ? texto : texto.replace(/\\s+/g, ' ');
            }}

            function samuFormatoItem(p) {{
                const item = p && p.item && p.item !== '-' ? `${{p.item}} ` : '';
                const descripcion = p && p.descripcion ? p.descripcion : '';
                const prog = p && p.prog ? ` - ${{p.prog}}` : '';
                const metrado = p && p.metrado ? ` = ${{p.metrado}} ${{p.unidad || ''}}` : '';
                return `${{item}}${{descripcion}}${{prog}}${{metrado}}`.replace(/\\s+/g, ' ').trim();
            }}

            function samuAgregarModulo(lista, titulo, contenido, conservarSaltos=false) {{
                const texto = String(contenido || '')
                    .split('\\n')
                    .map(linea => conservarSaltos ? String(linea || '').trimEnd() : String(linea || '').replace(/\\s+/g, ' ').trim())
                    .filter(linea => linea.trim())
                    .join('\\n');
                lista.push({{ titulo, contenido: texto || '-' }});
            }}

            function samuRedactarCuadernoCompleto() {{
                const modulos = [];

                const jornal = [];
                if (samuValor('v_jornal_m')) jornal.push(`Mañana: ${{samuValor('v_jornal_m')}}`);
                if (samuValor('v_jornal_t')) jornal.push(`Tarde: ${{samuValor('v_jornal_t')}}`);
                if (samuValor('v_clima')) jornal.push(`Clima: ${{samuValor('v_clima')}}`);
                samuAgregarModulo(modulos, '1. Jornal de trabajo', jornal.join(', '));

                const personalItems = [
                    ['Operario', samuValor('v_oper')],
                    ['Oficiales', samuValor('v_ofic')],
                    ['Peones', samuValor('v_peon')],
                    ['Mecánicos', samuValor('v_meca')],
                    ['Controladores de maquinaria', samuValor('v_ctrl')],
                    ['Operadores de maquinaria', samuValor('v_ope_maq')]
                ].filter(([_, cantidad]) => parseInt(cantidad || 0) > 0)
                 .map(([nombre, cantidad]) => `(${{String(parseInt(cantidad || 0)).padStart(2, '0')}}) ${{nombre}}`);
                const gastosGenerales = (window.m2_gastos_generales || []).map(nombre => `(1) ${{nombre}}`).join(', ');
                const costoDirecto = [
                    personalItems.slice(0, 4).join('    '),
                    personalItems.slice(4).join('    ')
                ].filter(Boolean).join('\\n');
                samuAgregarModulo(modulos, '2. Personal de obra', [
                    '* Personal de Gastos Generales',
                    gastosGenerales || '-',
                    '* Personal de Costo Directo',
                    costoDirecto || '-'
                ].join('\\n'), true);

                samuAgregarModulo(modulos, '3. Partidas ejecutadas', samuListaModulo('m3_lista').map(samuFormatoItem).join('\\n'));
                samuAgregarModulo(modulos, '4. Partidas de mayor metrado', samuListaModulo('m4_lista').map(samuFormatoItem).join('\\n'));
                samuAgregarModulo(modulos, '5. Sub partidas ejecutadas', samuListaModulo('m5_lista').map(samuFormatoItem).join('\\n'));
                samuAgregarModulo(modulos, '6. Actividades ejecutadas', samuListaModulo('m6_lista').map(samuFormatoItem).join('\\n'));
                samuAgregarModulo(modulos, '7. Movimiento de almacén', samuValor('v_almacen', true), true);
                samuAgregarModulo(modulos, '8. Maquinarias y equipos', samuValor('v_maquina', true), true);
                samuAgregarModulo(modulos, '9. Herramientas manuales', samuValor('v_herram', true), true);
                samuAgregarModulo(modulos, '10. Ocurrencias y otros', samuValor('v_ocurrencia', true), true);

                return modulos;
            }}

            window.samuSincronizarCuaderno = function() {{
                try {{
                    if (typeof actualizarStepper === 'function') actualizarStepper();
                    const numeroGlobal = typeof g_numAsiento !== 'undefined' ? g_numAsiento : '';
                    const fechaGlobal = typeof g_fechaAsiento !== 'undefined' ? g_fechaAsiento : '';
                    const numero = String(numeroGlobal || window.g_numAsiento || '').trim();
                    const fecha = String(fechaGlobal || window.g_fechaAsiento || document.getElementById('lbl_hoja_fecha')?.innerText || '').trim();
                    const contenedor = document.getElementById('contenedorLineasCuaderno');
                    if (!contenedor || !numero) return;
                    const asiento = numero.padStart(4, '0');
                    const maxStep = Math.max(1, Math.min(10, parseInt(window.samuMaxStepReached || window.samuCurrentStep || 1, 10) || 1));
                    const modulos = samuRedactarCuadernoCompleto().filter((_, index) => index + 1 <= maxStep);
                    contenedor.innerHTML = paginaHtml(asiento, fecha, modulos, false, false);
                }} catch (error) {{
                    console.error('No se pudo sincronizar el cuaderno:', error);
                }}
            }};

            sincronizarDatos = window.samuSincronizarCuaderno;

            document.addEventListener('DOMContentLoaded', function() {{
                const refrescar = () => {{
                    clearTimeout(window.__samuSyncLigeroTimer);
                    window.__samuSyncLigeroTimer = setTimeout(() => {{
                        const fn = window.samuActualizarCuaderno || window.samuSincronizarCuaderno;
                        if (typeof fn === 'function') fn();
                    }}, 35);
                }};
                document.getElementById('formResidencia')?.addEventListener('input', refrescar);
                document.getElementById('formResidencia')?.addEventListener('change', refrescar);
                document.getElementById('formResidencia')?.addEventListener('click', refrescar);
            }});
        </script>

        <script>
            // Motor de seguridad independiente: si un script anterior falla, este mantiene vivo el cuaderno.
            (function() {{
                const totalModulos = 10;
                const estadoKey = 'samu_residencia_asiento_en_edicion';
                const moduloActivoKey = 'samu_residencia_modulo_activo';
                const draftAsientoKey = 'samu_draft_asiento';
                window.samuCurrentStep = window.samuCurrentStep || 1;
                window.samuMaxStepReached = window.samuMaxStepReached || window.samuCurrentStep || 1;

                function texto(id, saltos=false) {{
                    const el = document.getElementById(id);
                    const valor = el ? String(el.value || '').trim() : '';
                    return saltos ? valor : valor.replace(/\\s+/g, ' ');
                }}

                function escapar(valor) {{
                    return String(valor || '')
                        .replace(/&/g, '&amp;')
                        .replace(/</g, '&lt;')
                        .replace(/>/g, '&gt;')
                        .replace(/"/g, '&quot;')
                        .replace(/'/g, '&#039;');
                }}

                function lista(nombre) {{
                    return Array.isArray(window[nombre]) ? window[nombre] : [];
                }}

                function itemPartida(p) {{
                    const item = p && p.item && p.item !== '-' ? `${{p.item}} ` : '';
                    const descripcion = p && p.descripcion ? p.descripcion : '';
                    const prog = p && p.prog ? ` - ${{p.prog}}` : '';
                    const metrado = p && p.metrado ? ` = ${{p.metrado}} ${{p.unidad || ''}}` : '';
                    return `${{item}}${{descripcion}}${{prog}}${{metrado}}`.replace(/\\s+/g, ' ').trim();
                }}

                function agregar(modulos, titulo, contenido) {{
                    const limpio = String(contenido || '')
                        .split('\\n')
                        .map(linea => String(linea || '').trimEnd())
                        .filter(linea => linea.trim())
                        .join('\\n');
                    modulos.push({{ titulo, contenido: limpio || '-' }});
                }}

                function modulosCuadernoCompleto() {{
                    const modulos = [];
                    const jornal = [];
                    if (texto('v_jornal_m')) jornal.push(`Mañana: ${{texto('v_jornal_m')}}`);
                    if (texto('v_jornal_t')) jornal.push(`Tarde: ${{texto('v_jornal_t')}}`);
                    if (texto('v_clima')) jornal.push(`Clima: ${{texto('v_clima')}}`);
                    agregar(modulos, '1. Jornal de trabajo', jornal.join(', '));

                    const personalItems = [
                        ['Operario', texto('v_oper')],
                        ['Oficiales', texto('v_ofic')],
                        ['Peones', texto('v_peon')],
                        ['Mecánicos', texto('v_meca')],
                        ['Controladores de maquinaria', texto('v_ctrl')],
                        ['Operadores de maquinaria', texto('v_ope_maq')]
                    ].filter(([_, cantidad]) => parseInt(cantidad || 0) > 0)
                     .map(([nombre, cantidad]) => `(${{String(parseInt(cantidad || 0)).padStart(2, '0')}}) ${{nombre}}`);
                    const gastosGenerales = (window.m2_gastos_generales || []).map(nombre => `(1) ${{nombre}}`).join(', ');
                    const costoDirecto = [
                        personalItems.slice(0, 4).join('    '),
                        personalItems.slice(4).join('    ')
                    ].filter(Boolean).join('\\n');
                    agregar(modulos, '2. Personal de obra', [
                        '* Personal de Gastos Generales',
                        gastosGenerales || '-',
                        '* Personal de Costo Directo',
                        costoDirecto || '-'
                    ].join('\\n'));

                    agregar(modulos, '3. Partidas ejecutadas', lista('m3_lista').map(itemPartida).join('\\n'));
                    agregar(modulos, '4. Partidas de mayor metrado', lista('m4_lista').map(itemPartida).join('\\n'));
                    agregar(modulos, '5. Sub partidas ejecutadas', lista('m5_lista').map(itemPartida).join('\\n'));
                    agregar(modulos, '6. Actividades ejecutadas', lista('m6_lista').map(itemPartida).join('\\n'));
                    agregar(modulos, '7. Movimiento de almacén', texto('v_almacen', true));
                    agregar(modulos, '8. Maquinarias y equipos', texto('v_maquina', true));
                    agregar(modulos, '9. Herramientas manuales', texto('v_herram', true));
                    agregar(modulos, '10. Ocurrencias y otros', texto('v_ocurrencia', true));
                    return modulos;
                }}

                function modulosCuaderno() {{
                    const maxStep = Math.max(1, Math.min(totalModulos, parseInt(window.samuMaxStepReached || window.samuCurrentStep || 1, 10) || 1));
                    return modulosCuadernoCompleto().filter((_, index) => index + 1 <= maxStep);
                }}

                function camposFormulario() {{
                    const datos = {{}};
                    document.querySelectorAll('#formResidencia input[id], #formResidencia textarea[id], #formResidencia select[id]').forEach(el => {{
                        if (el.type === 'checkbox' || el.type === 'radio') {{
                            datos[el.id] = {{ tipo: el.type, checked: el.checked, value: el.value }};
                        }} else {{
                            datos[el.id] = {{ tipo: el.type || el.tagName.toLowerCase(), value: el.value }};
                        }}
                    }});
                    return datos;
                }}

                function aplicarCamposFormulario(datos) {{
                    Object.entries(datos || {{}}).forEach(([id, info]) => {{
                        const el = document.getElementById(id);
                        if (!el) return;
                        if (info && (info.tipo === 'checkbox' || info.tipo === 'radio')) {{
                            el.checked = !!info.checked;
                        }} else {{
                            el.value = info && typeof info.value !== 'undefined' ? info.value : '';
                        }}
                    }});
                }}

                function estadoActualAsiento() {{
                    return {{
                        numero: window.g_numAsiento || '',
                        fechaRaw: window.g_fechaRaw || '',
                        fechaTexto: window.g_fechaAsiento || '',
                        step: window.samuCurrentStep || 1,
                        maxStepReached: window.samuMaxStepReached || window.samuCurrentStep || 1,
                        campos: camposFormulario(),
                        listas: {{
                            catalogoMaestro: window.catalogoMaestro || [],
                            m2_gastos_base: window.m2_gastos_base || [],
                            m2_gastos_generales: window.m2_gastos_generales || [],
                            m3_lista: window.m3_lista || [],
                            m4_lista: window.m4_lista || [],
                            m5_lista: window.m5_lista || [],
                            m6_lista: window.m6_lista || [],
                            m8_base: window.m8_base || null,
                            m8_registros: window.m8_registros || null,
                            m8_entidad_actual: window.m8_entidad_actual || null,
                            m8_entidades_registradas: window.m8_entidades_registradas || null,
                            m9_herramientas: window.m9_herramientas || null,
                            m9_seleccionadas: window.m9_seleccionadas || null,
                            m10_tipo_actual: window.m10_tipo_actual || null
                        }},
                        guardadoEn: new Date().toISOString()
                    }};
                }}

                function aplicarListasEstado(listas = {{}}) {{
                    if (Array.isArray(listas.catalogoMaestro)) window.catalogoMaestro = listas.catalogoMaestro;
                    if (Array.isArray(listas.m2_gastos_base)) window.m2_gastos_base = listas.m2_gastos_base;
                    if (Array.isArray(listas.m2_gastos_generales)) window.m2_gastos_generales = listas.m2_gastos_generales;
                    if (Array.isArray(listas.m3_lista)) window.m3_lista = listas.m3_lista;
                    if (Array.isArray(listas.m4_lista)) window.m4_lista = listas.m4_lista;
                    if (Array.isArray(listas.m5_lista)) window.m5_lista = listas.m5_lista;
                    if (Array.isArray(listas.m6_lista)) window.m6_lista = listas.m6_lista;
                    if (listas.m8_base) window.m8_base = listas.m8_base;
                    if (listas.m8_registros) window.m8_registros = listas.m8_registros;
                    if (listas.m8_entidad_actual) window.m8_entidad_actual = listas.m8_entidad_actual;
                    if (listas.m8_entidades_registradas) window.m8_entidades_registradas = listas.m8_entidades_registradas;
                    if (Array.isArray(listas.m9_herramientas)) window.m9_herramientas = listas.m9_herramientas;
                    if (Array.isArray(listas.m9_seleccionadas)) window.m9_seleccionadas = listas.m9_seleccionadas;
                    if (listas.m10_tipo_actual) window.m10_tipo_actual = listas.m10_tipo_actual;
                }}

                function guardarDraftAsientoCliente() {{
                    try {{
                        const draft = {{
                            ...estadoActualAsiento(),
                            clave: draftAsientoKey,
                            actualizadoEn: new Date().toISOString()
                        }};
                        localStorage.setItem(draftAsientoKey, JSON.stringify(draft));
                    }} catch (e) {{
                        console.warn('No se pudo guardar el borrador de emergencia.', e);
                    }}
                }}
                window.guardarDraftAsientoCliente = guardarDraftAsientoCliente;

                function limpiarDraftAsientoCliente() {{
                    try {{ localStorage.removeItem(draftAsientoKey); }} catch (e) {{}}
                }}
                window.limpiarDraftAsientoCliente = limpiarDraftAsientoCliente;

                function restaurarDraftAsientoCliente() {{
                    let draft = null;
                    try {{
                        draft = JSON.parse(localStorage.getItem(draftAsientoKey) || 'null');
                    }} catch (e) {{
                        draft = null;
                    }}
                    if (!draft || typeof draft !== 'object') return false;
                    if (window.g_numAsiento && draft.numero && String(window.g_numAsiento) !== String(draft.numero)) return false;

                    if (draft.numero && !window.g_numAsiento) window.g_numAsiento = draft.numero;
                    if (draft.fechaRaw && !window.g_fechaRaw) window.g_fechaRaw = draft.fechaRaw;
                    if (draft.fechaTexto && !window.g_fechaAsiento) window.g_fechaAsiento = draft.fechaTexto;
                    if (typeof g_numAsiento !== 'undefined' && window.g_numAsiento) g_numAsiento = window.g_numAsiento;
                    if (typeof g_fechaRaw !== 'undefined' && window.g_fechaRaw) g_fechaRaw = window.g_fechaRaw;
                    if (typeof g_fechaAsiento !== 'undefined' && window.g_fechaAsiento) g_fechaAsiento = window.g_fechaAsiento;

                    const lblFecha = document.getElementById('lbl_hoja_fecha');
                    if (lblFecha && window.g_fechaAsiento) lblFecha.innerText = window.g_fechaAsiento;
                    aplicarCamposFormulario(draft.campos || {{}});
                    aplicarListasEstado(draft.listas || {{}});
                    window.samuCurrentStep = Math.max(1, Math.min(totalModulos, parseInt(draft.step || window.samuCurrentStep || 1, 10) || 1));
                    window.samuMaxStepReached = Math.max(parseInt(draft.maxStepReached || 1, 10) || 1, window.samuCurrentStep);
                    window.borradorAsiento = draft;
                    restaurarRenderModulos();
                    desbloquearPantallaAsiento();
                    window.irModulo(window.samuCurrentStep);
                    window.samuActualizarCuaderno();
                    return true;
                }}
                window.restaurarDraftAsientoCliente = restaurarDraftAsientoCliente;

                function guardarEstadoLocal() {{
                    if (!window.g_numAsiento) return;
                    try {{
                        window.borradorAsiento = estadoActualAsiento();
                        localStorage.setItem(estadoKey, JSON.stringify(window.borradorAsiento));
                        sessionStorage.setItem(estadoKey, JSON.stringify(window.borradorAsiento));
                        localStorage.setItem(moduloActivoKey, String(window.borradorAsiento.step || 1));
                        sessionStorage.setItem(moduloActivoKey, String(window.borradorAsiento.step || 1));
                        guardarDraftAsientoCliente();
                    }} catch (e) {{
                        console.warn('No se pudo guardar el estado local del asiento.', e);
                    }}
                }}
                window.guardarEstadoLocal = guardarEstadoLocal;

                function guardarEstadoLocalInmediato() {{
                    try {{
                        if (typeof window.samuActualizarCuaderno === 'function') window.samuActualizarCuaderno();
                        guardarEstadoLocal();
                    }} catch (e) {{
                        console.warn('No se pudo guardar el estado inmediato del asiento.', e);
                    }}
                }}
                window.guardarEstadoLocalInmediato = guardarEstadoLocalInmediato;

                function programarAutoGuardadoContinuo() {{
                    if (!window.g_numAsiento || !window.g_fechaRaw || (typeof asientoCerrado !== 'undefined' && asientoCerrado)) return;
                    clearTimeout(window.__samuAutoGuardadoServidorTimer);
                    window.__samuAutoGuardadoServidorTimer = setTimeout(() => {{
                        guardarBorradorSilenciosoServidor();
                    }}, 2600);
                }}
                window.programarAutoGuardadoContinuo = programarAutoGuardadoContinuo;

                function restaurarRenderModulos() {{
                    ['m2_render', 'm3_render', 'm4_render', 'm5_render', 'm6_render', 'm8_render', 'm8_render_base', 'm8_refrescar_select', 'm8_actualizar_cuaderno', 'm9_render', 'm9_sincronizar', 'm10_sincronizar', 'm10_render_historial'].forEach(nombre => {{
                        if (typeof window[nombre] === 'function') {{
                            try {{ window[nombre](); }} catch (e) {{ console.warn(`No se pudo ejecutar ${{nombre}}`, e); }}
                        }}
                    }});
                }}

                function desbloquearPantallaAsiento() {{
                    document.body.classList.remove('modal-open');
                    document.body.style.removeProperty('overflow');
                    document.body.style.removeProperty('padding-right');
                    document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
                    document.getElementById('mainLayout')?.classList.add('unlocked');
                    const stepper = document.getElementById('stepperBar');
                    if (stepper) {{
                        stepper.style.opacity = '1';
                        stepper.style.pointerEvents = 'all';
                    }}
                    document.getElementById('bottomBarUI')?.classList.add('unlocked');
                    document.getElementById('mobilePreviewBtn')?.classList.add('unlocked');
                }}

                function restaurarEstadoLocal() {{
                    let estado = null;
                    try {{
                        estado = JSON.parse(localStorage.getItem(estadoKey) || sessionStorage.getItem(estadoKey) || 'null');
                    }} catch (e) {{
                        estado = null;
                    }}
                    if (!estado || !estado.numero || !estado.fechaRaw) return false;
                    const pasoPersistido = parseInt(localStorage.getItem(moduloActivoKey) || sessionStorage.getItem(moduloActivoKey) || estado.step || '1', 10) || 1;
                    estado.step = Math.max(1, Math.min(totalModulos, pasoPersistido));

                    window.borradorAsiento = estado;
                    window.g_numAsiento = estado.numero;
                    window.g_fechaRaw = estado.fechaRaw;
                    window.g_fechaAsiento = estado.fechaTexto || estado.fechaRaw;
                    window.samuMaxStepReached = Math.max(parseInt(estado.maxStepReached || 1, 10) || 1, parseInt(estado.step || 1, 10) || 1);
                    if (typeof g_numAsiento !== 'undefined') g_numAsiento = window.g_numAsiento;
                    if (typeof g_fechaRaw !== 'undefined') g_fechaRaw = window.g_fechaRaw;
                    if (typeof g_fechaAsiento !== 'undefined') g_fechaAsiento = window.g_fechaAsiento;

                    const lblFecha = document.getElementById('lbl_hoja_fecha');
                    if (lblFecha) lblFecha.innerText = window.g_fechaAsiento;
                    const inputNumero = document.getElementById('initNumAsiento');
                    const inputFecha = document.getElementById('initFecha');
                    if (inputNumero) inputNumero.value = window.g_numAsiento;
                    if (inputFecha) inputFecha.value = window.g_fechaRaw;

                    const listas = estado.listas || {{}};
                    if (Array.isArray(listas.catalogoMaestro)) window.catalogoMaestro = listas.catalogoMaestro;
                    if (Array.isArray(listas.m2_gastos_base)) window.m2_gastos_base = listas.m2_gastos_base;
                    if (Array.isArray(listas.m2_gastos_generales)) window.m2_gastos_generales = listas.m2_gastos_generales;
                    if (Array.isArray(listas.m3_lista)) window.m3_lista = listas.m3_lista;
                    if (Array.isArray(listas.m4_lista)) window.m4_lista = listas.m4_lista;
                    if (Array.isArray(listas.m5_lista)) window.m5_lista = listas.m5_lista;
                    if (Array.isArray(listas.m6_lista)) window.m6_lista = listas.m6_lista;
                    if (listas.m8_base) window.m8_base = listas.m8_base;
                    if (listas.m8_registros) window.m8_registros = listas.m8_registros;
                    if (listas.m8_entidad_actual) window.m8_entidad_actual = listas.m8_entidad_actual;
                    if (listas.m8_entidades_registradas) window.m8_entidades_registradas = listas.m8_entidades_registradas;
                    if (Array.isArray(listas.m9_herramientas)) window.m9_herramientas = listas.m9_herramientas;
                    if (Array.isArray(listas.m9_seleccionadas)) window.m9_seleccionadas = listas.m9_seleccionadas;
                    if (listas.m10_tipo_actual) window.m10_tipo_actual = listas.m10_tipo_actual;

                    aplicarCamposFormulario(estado.campos || {{}});
                    desbloquearPantallaAsiento();
                    restaurarRenderModulos();
                    window.irModulo(estado.step || 1);
                    window.samuActualizarCuaderno();
                    if (typeof mostrarAlerta === 'function') mostrarAlerta(`Se restauró el asiento N° ${{window.g_numAsiento}} donde lo dejaste.`, 'success');
                    return true;
                }}

                function htmlContenidoModulo(modulo) {{
                    if (modulo.titulo.startsWith('2.')) {{
                        return `<div class="personal-bloque">${{htmlPersonalObra(modulo.contenido)}}</div>`;
                    }}
                    if (modulo.titulo.startsWith('7.') && typeof htmlAlmacen === 'function') {{
                        return `<div class="almacen-bloque">${{htmlAlmacen(modulo.contenido)}}</div>`;
                    }}
                    if (modulo.titulo.startsWith('8.') && typeof htmlMaquinaria === 'function') {{
                        return `<div class="maquinaria-bloque">${{htmlMaquinaria(modulo.contenido)}}</div>`;
                    }}
                    return `<span class="modulo-contenido">${{escapar(modulo.contenido).replace(/\\n/g, '<br>')}}</span>`;
                }}

                function htmlPersonalObra(texto) {{
                    const lineas = String(texto || '-').split('\\n').map(linea => String(linea || '').trim()).filter(Boolean);
                    let enCostoDirecto = false;
                    return lineas.map(linea => {{
                        if (linea.startsWith('*')) {{
                            enCostoDirecto = /costo\\s+directo/i.test(linea);
                            return `<div class="personal-subtitulo">${{escapar(linea)}}</div>`;
                        }}
                        if (enCostoDirecto && linea !== '-') {{
                            return `<div class="personal-costo-fila">${{escapar(linea)}}</div>`;
                        }}
                        return `<div class="personal-gastos-linea">${{escapar(linea)}}</div>`;
                    }}).join('');
                }}

                function htmlCuaderno(asiento, fecha, modulos) {{
                    const paginas = paginarModulos(asiento, fecha, modulos);
                    return paginas.map(pagina => `
                        <div class="pagina-cuaderno">
                            <div class="lapicero">
                                ${{htmlEncabezadoPagina(asiento, fecha, pagina.continuacion)}}
                                ${{pagina.modulos.map(modulo => `
                                    <div class="modulo-redaccion">
                                        ${{modulo.continuacionModulo ? '' : `<span class="modulo-titulo">${{escapar(modulo.titulo)}}</span>`}}
                                        ${{htmlContenidoModulo(modulo)}}
                                    </div>
                                `).join('')}}
                                ${{pagina.van ? '<span class="van-final">van . . .</span>' : ''}}
                            </div>
                        </div>
                    `).join('');
                }}

                function htmlEncabezadoPagina(asiento, fecha, continuacion=false) {{
                    const titulo = continuacion
                        ? `. . . viene del ASIENTO N° ${{asiento}} DEL RESIDENTE DE OBRA`
                        : `ASIENTO N° ${{asiento}} DEL RESIDENTE DE OBRA`;
                    return `
                        <div class="encabezado-asiento ${{continuacion ? 'continuacion' : ''}}">
                            <div class="titulo-asiento">${{escapar(titulo)}}</div>
                            <div class="fecha-asiento">${{escapar(fecha)}}</div>
                        </div>
                    `;
                }}

                const PDF_LINE_HEIGHT_PX = 26;

                function obtenerMedidorPDF() {{
                    let medidor = document.getElementById('__samuPdfMeasure');
                    if (!medidor) {{
                        medidor = document.createElement('div');
                        medidor.id = '__samuPdfMeasure';
                        medidor.style.cssText = [
                            'position:absolute',
                            'left:-99999px',
                            'top:0',
                            'visibility:hidden',
                            'pointer-events:none',
                            'width:650px',
                            'font-family:Candara, Calibri, Arial, sans-serif',
                            'font-style:italic',
                            'font-size:17px',
                            'line-height:26px',
                            'font-weight:400',
                            'text-align:justify',
                            'color:#0263a0',
                            'word-wrap:break-word'
                        ].join(';');
                        document.body.appendChild(medidor);
                    }}
                    return medidor;
                }}

                function htmlModuloMedicion(modulo, incluirVan=false) {{
                    return `
                        <div class="modulo-redaccion">
                            ${{modulo.continuacionModulo ? '' : `<span class="modulo-titulo">${{escapar(modulo.titulo)}}</span>`}}
                            ${{htmlContenidoModulo(modulo)}}
                        </div>
                        ${{incluirVan ? '<span class="van-final">van . . .</span>' : ''}}
                    `;
                }}

                function estimarLineasHtmlModulo(modulo) {{
                    const html = htmlContenidoModulo(modulo);
                    const bloques = (html.match(/<div\\b/gi) || []).length;
                    const saltos = (html.match(/<br\\s*\\/?\\s*>/gi) || []).length;
                    return Math.max(0, bloques + saltos);
                }}

                function anchoLineaCuadernoPDF() {{
                    const hoja = document.querySelector('#papelOficial .pagina-cuaderno') || document.querySelector('.pagina-cuaderno');
                    const ancho = hoja?.clientWidth || 836;
                    return Math.max(760, Math.floor(ancho - 28));
                }}

                function contextoLineasCuadernoPDF() {{
                    if (!window.__samuLineMeasureCanvas) {{
                        window.__samuLineMeasureCanvas = document.createElement('canvas');
                    }}
                    const ctx = window.__samuLineMeasureCanvas.getContext('2d');
                    ctx.font = 'italic 17px Candara, Calibri, Arial, sans-serif';
                    return ctx;
                }}

                function contarLineasTextoCuaderno(texto) {{
                    const ctx = contextoLineasCuadernoPDF();
                    const anchoMaximo = anchoLineaCuadernoPDF();
                    const parrafos = String(texto || '-').split('\\n');
                    let total = 0;

                    parrafos.forEach(parrafo => {{
                        const limpio = String(parrafo || '').trim();
                        if (!limpio) {{
                            total += 1;
                            return;
                        }}

                        let lineaActual = '';
                        limpio.split(/\\s+/).filter(Boolean).forEach(palabra => {{
                            const candidata = lineaActual ? `${{lineaActual}} ${{palabra}}` : palabra;
                            if (lineaActual && ctx.measureText(candidata).width > anchoMaximo) {{
                                total += 1;
                                lineaActual = palabra;
                            }} else {{
                                lineaActual = candidata;
                            }}
                        }});
                        total += 1;
                    }});

                    return Math.max(1, total);
                }}

                function estimarLineasModulo(modulo) {{
                    const titulo = modulo.continuacionModulo ? 0 : 1;
                    const texto = contarLineasTextoCuaderno(modulo.contenido || '-');
                    const html = estimarLineasHtmlModulo(modulo);
                    return titulo + Math.max(texto, html);
                }}

                function lineasModulo(modulo, incluirVan=false) {{
                    return Math.max(1, estimarLineasModulo(modulo) + (incluirVan ? 1 : 0));
                }}

                function htmlPaginaMedicionPDF(asiento, fecha, modulos, continuacion=false, van=false) {{
                    return `
                        <div class="pagina-cuaderno" style="height:auto;min-height:0;max-height:none;overflow:visible;background:none;display:block;">
                            <div class="lapicero" style="display:block;min-height:0;overflow:visible;">
                                ${{htmlEncabezadoPagina(asiento, fecha, continuacion)}}
                                ${{modulos.map(modulo => `
                                    <div class="modulo-redaccion">
                                        ${{modulo.continuacionModulo ? '' : `<span class="modulo-titulo">${{escapar(modulo.titulo)}}</span>`}}
                                        ${{htmlContenidoModulo(modulo)}}
                                    </div>
                                `).join('')}}
                                ${{van ? '<span class="van-final">van . . .</span>' : ''}}
                            </div>
                        </div>
                    `;
                }}

                function medirPaginaPDF(asiento, fecha, modulos, continuacion=false, van=false) {{
                    const medidor = obtenerMedidorPDF();
                    medidor.style.width = '650px';
                    medidor.innerHTML = htmlPaginaMedicionPDF(asiento, fecha, modulos, continuacion, van);
                    const contenido = medidor.querySelector('.lapicero');
                    return contenido ? contenido.scrollHeight : (medidor.scrollHeight || 0);
                }}

                function estimarLineasTexto(texto) {{
                    return contarLineasTextoCuaderno(texto);
                }}

                function dividirModuloPorLineas(modulo, maxLineas) {{
                    const texto = String(modulo.contenido || '-').trim();
                    const lineasDisponibles = Math.max(1, maxLineas);
                    const palabras = texto.split(/\\s+/).filter(Boolean);
                    if (palabras.length <= 1) {{
                        return [
                            {{ titulo: modulo.titulo, contenido: texto || '-' }},
                            {{ titulo: modulo.titulo, contenido: '' }}
                        ];
                    }}

                    let bajo = 1;
                    let alto = palabras.length;
                    let mejor = 0;
                    while (bajo <= alto) {{
                        const medio = Math.floor((bajo + alto) / 2);
                        const candidato = palabras.slice(0, medio).join(' ').trim();
                        if (lineasModulo({{ ...modulo, contenido: candidato }}, false) <= lineasDisponibles) {{
                            mejor = medio;
                            bajo = medio + 1;
                        }} else {{
                            alto = medio - 1;
                        }}
                    }}

                    if (mejor <= 0) {{
                        return [
                            {{ titulo: modulo.titulo, contenido: '', continuacionModulo: modulo.continuacionModulo }},
                            {{ titulo: modulo.titulo, contenido: texto || '-', continuacionModulo: true }}
                        ];
                    }}

                    if (mejor >= palabras.length) {{
                        mejor = Math.max(1, palabras.length - 1);
                    }}
                    const primera = palabras.slice(0, mejor).join(' ').trim();
                    const segunda = palabras.slice(mejor).join(' ').trim();
                    return [
                        {{ titulo: modulo.titulo, contenido: primera || '-' }},
                        {{ titulo: modulo.titulo, contenido: segunda, continuacionModulo: true }}
                    ];
                }}

                function dividirModuloPorAltura(asiento, fecha, modulo, modulosPrevios, continuacion, maxAltura) {{
                    const texto = String(modulo.contenido || '-').trim();
                    const palabras = texto.split(/\\s+/).filter(Boolean);
                    if (palabras.length <= 1) {{
                        return [
                            {{ titulo: modulo.titulo, contenido: texto || '-' }},
                            {{ titulo: modulo.titulo, contenido: '' }}
                        ];
                    }}

                    let bajo = 1;
                    let alto = palabras.length;
                    let mejor = 0;
                    while (bajo <= alto) {{
                        const medio = Math.floor((bajo + alto) / 2);
                        const candidato = {{ ...modulo, contenido: palabras.slice(0, medio).join(' ').trim() }};
                        const altura = medirPaginaPDF(asiento, fecha, [...modulosPrevios, candidato], continuacion, false);
                        if (altura <= maxAltura) {{
                            mejor = medio;
                            bajo = medio + 1;
                        }} else {{
                            alto = medio - 1;
                        }}
                    }}

                    if (mejor >= palabras.length) mejor = Math.max(1, palabras.length - 1);
                    return [
                        {{ titulo: modulo.titulo, contenido: palabras.slice(0, mejor).join(' ').trim() }},
                        {{ titulo: modulo.titulo, contenido: palabras.slice(mejor).join(' ').trim(), continuacionModulo: true }}
                    ];
                }}

                function paginarModulos(asiento, fecha, modulos, opciones = {{}}) {{
                    const paginas = [];
                    let actual = [];
                    let usadas = 1;
                    let continuacion = false;
                    const lineasPorPagina = parseInt(opciones.lineasPorPagina || 30, 10) || 30;
                    const maxLineasContenido = () => Math.max(2, lineasPorPagina - 1);
                    const maxAlturaContenido = () => PDF_LINE_HEIGHT_PX * maxLineasContenido();

                    modulos.forEach(moduloOriginal => {{
                        let pendiente = {{ ...moduloOriginal }};
                        while (pendiente && String(pendiente.contenido || '').trim()) {{
                            const lineasPendiente = lineasModulo(pendiente);
                            const lineasDisponibles = maxLineasContenido() - usadas;

                            if (lineasPendiente <= lineasDisponibles) {{
                                actual.push(pendiente);
                                usadas += lineasPendiente;
                                pendiente = null;
                                continue;
                            }}

                            if (lineasDisponibles >= 1) {{
                                const partes = dividirModuloPorLineas(pendiente, lineasDisponibles);
                                const resto = String(partes[1].contenido || '').trim();
                                if (String(partes[0].contenido || '').trim()) {{
                                    actual.push(partes[0]);
                                }}
                                if (resto) {{
                                    paginas.push({{ modulos: actual, continuacion, van: true }});
                                    actual = [];
                                    usadas = 1;
                                    continuacion = true;
                                    pendiente = {{ ...partes[1], contenido: resto }};
                                }} else {{
                                    pendiente = null;
                                }}
                                continue;
                            }}

                            if (actual.length > 0) {{
                                paginas.push({{ modulos: actual, continuacion, van: true }});
                                actual = [];
                                usadas = 1;
                                continuacion = true;
                                continue;
                            }}

                            const forzado = dividirModuloPorLineas(pendiente, Math.max(2, maxLineasContenido() - usadas));
                            const restoForzado = String(forzado[1].contenido || '').trim();
                            actual.push(forzado[0]);
                            if (restoForzado) {{
                                paginas.push({{ modulos: actual, continuacion, van: true }});
                                actual = [];
                                usadas = 1;
                                continuacion = true;
                                pendiente = {{ ...forzado[1], contenido: restoForzado }};
                            }} else {{
                                pendiente = null;
                            }}
                        }}
                    }});

                    if (actual.length > 0 || paginas.length === 0) {{
                        paginas.push({{ modulos: actual, continuacion, van: false }});
                    }}
                    return paginas;
                }}

                function htmlCuadernoVistaA4(asiento, fecha, modulos) {{
                    const paginas = paginarModulos(asiento, fecha, modulos, {{ lineasPorPagina: 30, alturaPagina: 780 }});
                    const firmas = htmlFirmasPDF();
                    const encabezadoGeneral = htmlEncabezadoGeneralPDF();
                    return paginas.map((pagina, idx) => `
                        <div class="papel-fisico hoja-vista-a4">
                            ${{encabezadoGeneral}}
                            <div class="p-body-lines">
                                <div class="pagina-cuaderno">
                                    <div class="lapicero">
                                        ${{htmlEncabezadoPagina(asiento, fecha, pagina.continuacion)}}
                                        ${{pagina.modulos.map(modulo => `
                                            <div class="modulo-redaccion">
                                                ${{modulo.continuacionModulo ? '' : `<span class="modulo-titulo">${{escapar(modulo.titulo)}}</span>`}}
                                                ${{htmlContenidoModulo(modulo)}}
                                            </div>
                                        `).join('')}}
                                        ${{pagina.van ? '<span class="van-final">van . . .</span>' : ''}}
                                    </div>
                                </div>
                            </div>
                            ${{firmas}}
                            <div class="page-counter">${{idx + 1}} de ${{paginas.length}}</div>
                        </div>
                    `).join('');
                }}

                function actualizarQRCuaderno() {{
                    const fechaRaw = String(window.g_fechaRaw || '').trim();
                    const destino = fechaRaw
                        ? `${{window.location.origin}}/resumen_asiento/${{encodeURIComponent(fechaRaw)}}`
                        : `${{window.location.origin}}/cuaderno`;
                    const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=120x120&margin=0&data=${{encodeURIComponent(destino)}}`;
                    document.querySelectorAll('#qrCuadernoLink, .qr-cuaderno-link, .p-qr-link').forEach(link => {{
                        link.href = destino;
                    }});
                    document.querySelectorAll('#qrCuadernoImg, .qr-cuaderno-img').forEach(img => {{
                        if (img.getAttribute('src') !== qrUrl) img.setAttribute('src', qrUrl);
                    }});
                }}
                window.actualizarQRCuaderno = actualizarQRCuaderno;

                window.samuActualizarCuaderno = function() {{
                    const numero = String(window.g_numAsiento || (typeof g_numAsiento !== 'undefined' ? g_numAsiento : '') || '').trim();
                    const fecha = String(window.g_fechaAsiento || (typeof g_fechaAsiento !== 'undefined' ? g_fechaAsiento : '') || document.getElementById('lbl_hoja_fecha')?.innerText || '').trim();
                    const contenedor = document.getElementById('papelOficial');
                    if (!contenedor || !numero) return;
                    contenedor.innerHTML = htmlCuadernoVistaA4(numero.padStart(4, '0'), fecha, modulosCuaderno());
                    actualizarQRCuaderno();
                }};

                window.samuPrepararResumenPDF = function() {{
                    const numero = String(window.g_numAsiento || (typeof g_numAsiento !== 'undefined' ? g_numAsiento : '') || '').trim();
                    const fecha = String(window.g_fechaAsiento || (typeof g_fechaAsiento !== 'undefined' ? g_fechaAsiento : '') || document.getElementById('lbl_hoja_fecha')?.innerText || '').trim();
                    const destino = document.getElementById('resumenCuadernoContenido');
                    if (!destino || !numero) return;
                    destino.innerHTML = htmlCuadernoPDF(numero.padStart(4, '0'), fecha, modulosCuadernoCompleto());
                    if (typeof aplicarZoomResumenCuaderno === 'function') aplicarZoomResumenCuaderno();
                }};

                function htmlFirmasPDF() {{
                    const footer = document.querySelector('#papelOficial .p-footer');
                    return footer ? footer.outerHTML : '<div class="p-footer"><div class="p-sig">ING. INSPECTOR</div><div class="p-sig">ING. RESIDENTE</div><div class="p-sig">ING. SUPERVISOR</div></div>';
                }}

                function htmlEncabezadoGeneralPDF() {{
                    const top = document.querySelector('#papelOficial .p-header-top')?.outerHTML || '';
                    const meta = document.querySelector('#papelOficial .p-meta')?.outerHTML || '';
                    return `${{top}}${{meta}}`
                        .replaceAll(' id="qrCuadernoLink"', '')
                        .replaceAll('class="p-qr-link"', 'class="p-qr-link qr-cuaderno-link"')
                        .replaceAll('id="qrCuadernoImg"', 'class="qr-cuaderno-img"');
                }}

                function htmlCuadernoPDF(asiento, fecha, modulos) {{
                    const paginas = paginarModulos(asiento, fecha, modulos);
                    const firmas = htmlFirmasPDF();
                    const encabezadoGeneral = htmlEncabezadoGeneralPDF();
                    return paginas.map((pagina, idx) => `
                        <div class="papel-fisico hoja-pdf">
                            ${{encabezadoGeneral}}
                            <div class="p-body-lines">
                                <div class="pagina-cuaderno">
                                    <div class="lapicero">
                                        ${{htmlEncabezadoPagina(asiento, fecha, pagina.continuacion)}}
                                        ${{pagina.modulos.map(modulo => `
                                            <div class="modulo-redaccion">
                                                ${{modulo.continuacionModulo ? '' : `<span class="modulo-titulo">${{escapar(modulo.titulo)}}</span>`}}
                                                ${{htmlContenidoModulo(modulo)}}
                                            </div>
                                        `).join('')}}
                                        ${{pagina.van ? '<span class="van-final">van . . .</span>' : ''}}
                                    </div>
                                </div>
                            </div>
                            ${{firmas}}
                            <div class="page-counter">${{idx + 1}} de ${{paginas.length}}</div>
                        </div>
                    `).join('');
                }}

                window.irModulo = function(stepIndex) {{
                    guardarEstadoLocal();
                    const step = Math.max(1, Math.min(totalModulos, parseInt(stepIndex, 10) || 1));
                    window.samuCurrentStep = step;
                    window.samuMaxStepReached = Math.max(parseInt(window.samuMaxStepReached || 1, 10) || 1, step);
                    try {{
                        localStorage.setItem(moduloActivoKey, String(step));
                        sessionStorage.setItem(moduloActivoKey, String(step));
                    }} catch (e) {{}}
                    if (typeof currentStep !== 'undefined') currentStep = step;
                    document.querySelectorAll('.step-view').forEach(vista => vista.classList.remove('active', 'exit'));
                    document.querySelectorAll('.step-btn').forEach(btn => btn.classList.remove('active'));
                    document.getElementById(`step${{step}}`)?.classList.add('active');
                    document.getElementById(`btnStep${{step}}`)?.classList.add('active');
                    document.getElementById('btnAtras')?.classList.toggle('d-none', step <= 1);
                    document.getElementById('asientoActions')?.classList.toggle('visible', step > 1);
                    document.getElementById('btnEnviarInspector')?.classList.toggle('d-none', step !== 10);
                    document.getElementById('moduloNavActions')?.classList.toggle('d-none', step === 10);
                    if (window.borradorAsiento?.campos) aplicarCamposFormulario(window.borradorAsiento.campos);
                    restaurarRenderModulos();
                    setTimeout(window.samuActualizarCuaderno, 30);
                    guardarEstadoLocalInmediato();
                }};

                window.omitirModulo = function() {{
                    guardarEstadoLocalInmediato();
                    window.irModulo((window.samuCurrentStep || 1) + 1);
                }};

                window.guardarYContinuarModulo = async function() {{
                    const btn = document.getElementById('btnGuardarContinuar');
                    if (btn?.disabled) return;
                    if (btn) btn.disabled = true;
                    try {{
                        guardarEstadoLocalInmediato();
                        const data = await guardarAsientoSeguro('Borrador', {{ mostrarModal: false }});
                        if (data) {{
                            window.irModulo((window.samuCurrentStep || 1) + 1);
                            limpiarDraftAsientoCliente();
                        }}
                    }} finally {{
                        if (btn) btn.disabled = false;
                    }}
                }};

                window.siguienteModulo = window.guardarYContinuarModulo;

                window.anteriorModulo = function() {{
                    window.irModulo((window.samuCurrentStep || 1) - 1);
                }};

                window.iniciarAsientoSeguro = function() {{
                    const numero = String(document.getElementById('initNumAsiento')?.value || '').trim();
                    const fecha = String(document.getElementById('initFecha')?.value || '').trim();
                    if (!numero || !fecha) {{
                        if (typeof mostrarAlerta === 'function') mostrarAlerta('Complete los datos para iniciar.', 'error');
                        return;
                    }}

                    const dias = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO", "DOMINGO"];
                    const [y, m, d] = fecha.split('-');
                    const dateObj = new Date(y, m - 1, d);
                    let dayIndex = dateObj.getDay() - 1;
                    if (dayIndex === -1) dayIndex = 6;

                    window.g_numAsiento = numero;
                    window.g_fechaRaw = fecha;
                    window.g_fechaAsiento = `${{dias[dayIndex]}}, ${{d}}/${{m}}/${{y}}`;
                    const pasoInicial = Math.max(1, Math.min(totalModulos, parseInt(window.__samuModuloInicial || localStorage.getItem(moduloActivoKey) || sessionStorage.getItem(moduloActivoKey) || '1', 10) || 1));
                    window.samuMaxStepReached = pasoInicial;
                    if (typeof g_numAsiento !== 'undefined') g_numAsiento = window.g_numAsiento;
                    if (typeof g_fechaRaw !== 'undefined') g_fechaRaw = window.g_fechaRaw;
                    if (typeof g_fechaAsiento !== 'undefined') g_fechaAsiento = window.g_fechaAsiento;

                    const fechaCuaderno = document.getElementById('lbl_hoja_fecha');
                    if (fechaCuaderno) fechaCuaderno.innerText = window.g_fechaAsiento;

                    document.body.classList.remove('modal-open');
                    document.body.style.removeProperty('overflow');
                    document.body.style.removeProperty('padding-right');
                    document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());

                    document.getElementById('mainLayout')?.classList.add('unlocked');
                    const stepper = document.getElementById('stepperBar');
                    if (stepper) {{
                        stepper.style.opacity = '1';
                        stepper.style.pointerEvents = 'all';
                    }}
                    document.getElementById('bottomBarUI')?.classList.add('unlocked');
                    document.getElementById('mobilePreviewBtn')?.classList.add('unlocked');
                    window.irModulo(pasoInicial);
                    window.samuActualizarCuaderno();
                    guardarEstadoLocal();
                }};

                function mensajeErrorServidor(resp, data=null) {{
                    const detalle = data?.message || data?.error || data?.detail;
                    if (detalle) return `Error: ${{detalle}}`;
                    if (!resp || !resp.ok) return `Error en el servidor (${{resp?.status || 500}})`;
                    return 'No se pudo guardar el asiento.';
                }}

                function esErrorDeRed(error) {{
                    const mensaje = String(error?.message || error || '');
                    return error instanceof TypeError || /Failed to fetch|NetworkError|Load failed|fetch/i.test(mensaje);
                }}

                function mensajeErrorFetch(error) {{
                    return esErrorDeRed(error) ? 'Sin conexión' : (error?.message || 'Error inesperado al guardar.');
                }}

                async function leerJsonSeguro(resp) {{
                    return await resp.json().catch(() => ({{ ok: false, error: 'Respuesta inválida del servidor' }}));
                }}

                function mostrarEstadoGuardado(tipo, texto) {{
                    const estadoEl = document.getElementById('saveInlineStatus');
                    if (!estadoEl) return;
                    estadoEl.classList.remove('saving', 'saved', 'error');
                    estadoEl.classList.add('visible', tipo);
                    const icono = tipo === 'saving' ? 'bi-arrow-repeat' : (tipo === 'error' ? 'bi-exclamation-triangle-fill' : 'bi-check2-circle');
                    estadoEl.innerHTML = `<i class="bi ${{icono}}"></i><span>${{texto}}</span>`;
                    clearTimeout(window.__samuSaveStatusTimer);
                    if (tipo !== 'saving') {{
                        window.__samuSaveStatusTimer = setTimeout(() => {{
                            estadoEl.classList.remove('visible', 'saving', 'saved', 'error');
                        }}, 2400);
                    }}
                }}

                async function guardarAsientoSeguro(estado, opciones = {{}}) {{
                    const silencioso = !!opciones.silencioso;
                    const mostrarModal = opciones.mostrarModal !== false;
                    if (!silencioso) mostrarEstadoGuardado('saving', 'Guardando...');
                    window.samuActualizarCuaderno();
                    const numero = String(window.g_numAsiento || '').trim();
                    const fecha = String(window.g_fechaRaw || '').trim();
                    if (!numero || !fecha) {{
                        if (typeof mostrarAlerta === 'function') mostrarAlerta('Primero inicie el asiento.', 'error');
                        if (!silencioso) mostrarEstadoGuardado('error', 'No iniciado');
                        return null;
                    }}
                    const payload = {{
                        numero,
                        fecha,
                            estado,
                        avance: 100,
                        modulo_activo: window.samuCurrentStep || 1,
                        contenido: {{
                            numero,
                            fecha,
                            fecha_texto: window.g_fechaAsiento || '',
                            modulos: modulosCuadernoCompleto(),
                            texto_html: document.getElementById('papelOficial')?.innerHTML || '',
                            estado_local: estadoActualAsiento()
                        }}
                    }};
                    const respaldoKey = `samu_asiento_guardado_${{numero}}`;
                    try {{
                        localStorage.setItem(respaldoKey, JSON.stringify({{
                            ...payload,
                            guardado_local_en: new Date().toISOString()
                        }}));
                        localStorage.setItem('samu_ultimo_asiento_guardado', respaldoKey);
                    }} catch (e) {{
                        console.warn('No se pudo crear respaldo local del asiento.', e);
                    }}

                    let guardadoServidor = false;
                    let respuestaGuardado = null;
                    let mensajeErrorGuardado = '';
                    try {{
                        const resp = await fetch('/residencia/api/asiento', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify(payload)
                        }});
                        const data = await leerJsonSeguro(resp);
                        respuestaGuardado = data;
                        if (!resp.ok || !data.ok) {{
                            mensajeErrorGuardado = mensajeErrorServidor(resp, data);
                            respuestaGuardado = {{ ...data, ok: false, error: mensajeErrorGuardado }};
                            console.warn('No se pudo guardar en servidor:', mensajeErrorGuardado);
                        }} else {{
                            guardadoServidor = true;
                            try {{
                                localStorage.setItem('samu_dashboard_refresh', JSON.stringify({{
                                    numero,
                                    fecha,
                                    estado,
                                    tipo: 'Residente',
                                    updated_at: new Date().toISOString()
                                }}));
                            }} catch (e) {{}}
                        }}
                    }} catch (error) {{
                        mensajeErrorGuardado = mensajeErrorFetch(error);
                        respuestaGuardado = {{ ok: false, error: mensajeErrorGuardado }};
                        console.error('Error guardando asiento:', error);
                    }}
                    if (guardadoServidor) {{
                        mostrarEstadoGuardado('saved', 'Guardado correctamente');
                        if (!silencioso) limpiarDraftAsientoCliente();
                    }} else if (!silencioso) {{
                        mostrarEstadoGuardado('error', mensajeErrorGuardado || 'No se pudo guardar');
                    }}
                    if (guardadoServidor && estado !== 'Borrador') {{
                        try {{ localStorage.removeItem(estadoKey); }} catch (e) {{}}
                    }}
                    if (mostrarModal) {{
                        mostrarVentanaExitoGuardado(estado, guardadoServidor, respuestaGuardado);
                    }}
                    return guardadoServidor ? respuestaGuardado : null;
                }}

                async function guardarBorradorSilenciosoServidor() {{
                    const numero = String(window.g_numAsiento || '').trim();
                    const fecha = String(window.g_fechaRaw || '').trim();
                    if (!numero || !fecha) return;
                    if (window.__samuGuardandoBorradorSilencioso) return;
                    window.__samuGuardandoBorradorSilencioso = true;
                    try {{
                        if (typeof window.samuActualizarCuaderno === 'function') window.samuActualizarCuaderno();
                        guardarEstadoLocal();
                        const payload = {{
                            numero,
                            fecha,
                            estado: 'Borrador',
                            avance: 100,
                            modulo_activo: window.samuCurrentStep || 1,
                            contenido: {{
                                numero,
                                fecha,
                                fecha_texto: window.g_fechaAsiento || '',
                                modulos: modulosCuadernoCompleto(),
                                texto_html: document.getElementById('papelOficial')?.innerHTML || '',
                                estado_local: estadoActualAsiento()
                            }}
                        }};
                        const resp = await fetch('/residencia/api/asiento', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify(payload)
                        }});
                        const data = await resp.json().catch(() => null);
                        if (resp.ok && data?.ok) {{
                            localStorage.setItem('samu_ultimo_autoguardado_residencia', JSON.stringify({{
                                numero,
                                fecha,
                                estado: 'Borrador',
                                updated_at: new Date().toISOString()
                            }}));
                        }}
                    }} catch (error) {{
                        console.warn('Autoguardado silencioso pendiente de sincronizar.', error);
                    }} finally {{
                        window.__samuGuardandoBorradorSilencioso = false;
                    }}
                }}

                function mostrarVentanaExitoGuardado(estado, guardadoServidor=true, respuestaGuardado=null) {{
                    const enviadoInspector = estado === 'Enviado Inspector';
                    const fechaResumen = encodeURIComponent(window.g_fechaRaw || '');
                    const numeroResumen = encodeURIComponent(window.g_numAsiento || '');
                    if (!guardadoServidor) {{
                        mostrarModalResidencia(
                            'No se pudo guardar el borrador',
                            respuestaGuardado?.error || 'El servidor no confirmó el guardado en PostgreSQL. Revise la conexión e intente nuevamente.',
                            'warning',
                            0
                        );
                        return;
                    }}
                    if (!enviadoInspector) {{
                        window.ultimoBorradorGuardadoFecha = String(respuestaGuardado?.fecha || window.g_fechaRaw || '');
                        document.getElementById('modalBorradorGuardado')?.classList.add('active');
                        return;
                    }}
                    const titulo = guardadoServidor
                        ? (enviadoInspector ? 'Asiento enviado al Inspector' : 'Borrador guardado exitosamente')
                        : 'No se pudo sincronizar con el servidor';
                    const texto = guardadoServidor
                        ? (enviadoInspector ? 'La Residencia queda lista para que el Inspector revise y firme.' : 'El asiento se guardó realmente en la base de datos. El calendario lo mostrará en amarillo como borrador.')
                        : 'Se creó un respaldo local para no perder información. Revise la conexión antes de cerrar definitivamente.';
                    const tipo = guardadoServidor ? 'success' : 'warning';
                    mostrarModalResidencia(titulo, texto, tipo, 1100).then(() => {{
                        setTimeout(() => {{
                            if (!enviadoInspector && fechaResumen && numeroResumen) {{
                                window.location.href = `/cuaderno/resumen?fecha=${{fechaResumen}}&asiento=${{numeroResumen}}`;
                                return;
                            }}
                            window.location.href = fechaResumen ? `/resumen_asiento/${{fechaResumen}}` : '/cuaderno';
                        }}, 1500);
                    }});
                }}

                window.accionAsientoPendiente = 'Borrador';
                function configurarConfirmacionAsiento(tipo) {{
                    const esCierre = tipo === 'Enviado Inspector';
                    window.accionAsientoPendiente = tipo;
                    const hero = document.getElementById('confirmAccionHero');
                    const icon = document.getElementById('confirmAccionIcon');
                    const titulo = document.getElementById('confirmAccionTitulo');
                    const subtitulo = document.getElementById('confirmAccionSubtitulo');
                    const mensaje = document.getElementById('confirmAccionMensaje');
                    const cancelar = document.getElementById('confirmAccionCancelar');
                    const boton = document.getElementById('confirmAccionBoton');
                    hero?.classList.toggle('draft', !esCierre);
                    boton?.classList.toggle('draft', !esCierre);
                    if (icon) icon.innerHTML = esCierre ? '<i class="bi bi-shield-lock-fill"></i>' : '<i class="bi bi-save2-fill"></i>';
                    if (titulo) titulo.innerText = esCierre ? 'Enviar asiento al Inspector' : 'Guardar como Borrador';
                    if (subtitulo) subtitulo.innerText = esCierre
                        ? 'Confirme el envío para que el Inspector pueda revisar y firmar.'
                        : '¿Desea guardar el borrador del asiento?';
                    if (mensaje) mensaje.innerHTML = esCierre
                        ? '<i class="bi bi-exclamation-triangle-fill me-1"></i> Al enviar el asiento quedará listo para firma del Inspector. Podrá corregirse desde el resumen mientras no esté firmado.'
                        : '<i class="bi bi-info-circle-fill me-1"></i> Al confirmar, se guardará el avance real en la base de datos y luego podrá seguir asentando otro día o cerrar.';
                    if (cancelar) cancelar.innerText = esCierre ? 'Seguir editando' : 'Cancelar';
                    if (boton) boton.innerText = esCierre ? 'Sí, enviar a firma' : 'Confirmar';
                }}
                window.mostrarConfirmarGuardarBorrador = function() {{
                    guardarAsientoSeguro('Borrador');
                }};
                function urlCalendarioDesdeFechaAsiento(fechaISO) {{
                    const partes = String(fechaISO || '').split('-').map(n => parseInt(n, 10));
                    if (partes.length !== 3 || partes.some(Number.isNaN)) return '/cuaderno';
                    let [anio, mes, dia] = partes;
                    const ultimoDiaMes = new Date(anio, mes, 0).getDate();
                    if (dia === ultimoDiaMes) {{
                        mes += 1;
                        if (mes > 12) {{
                            mes = 1;
                            anio += 1;
                        }}
                    }}
                    return `/cuaderno?mes=${{mes}}&anio=${{anio}}`;
                }}
                window.seguirAsentandoOtroDia = function() {{
                    const fecha = window.ultimoBorradorGuardadoFecha || window.g_fechaRaw || '';
                    window.location.href = urlCalendarioDesdeFechaAsiento(fecha);
                }};
                window.cerrarModalBorradorGuardado = function() {{
                    window.location.href = '/cuaderno';
                }};
                window.mostrarConfirmarCerrarAsiento = function() {{
                    configurarConfirmacionAsiento('Enviado Inspector');
                    document.getElementById('confirmAccionAsiento')?.classList.add('active');
                }};
                window.ocultarConfirmarAccionAsiento = function() {{
                    document.getElementById('confirmAccionAsiento')?.classList.remove('active');
                }};
                window.confirmarAccionAsiento = function() {{
                    window.ocultarConfirmarAccionAsiento();
                    guardarAsientoSeguro(window.accionAsientoPendiente || 'Borrador');
                }};
                window.guardarBorradorAsiento = window.mostrarConfirmarGuardarBorrador;
                window.cerrarAsiento = window.mostrarConfirmarCerrarAsiento;

                function fechaTextoLocal(fechaISO) {{
                    const partes = String(fechaISO || '').split('-');
                    if (partes.length !== 3) return fechaISO || '';
                    const y = parseInt(partes[0], 10);
                    const m = parseInt(partes[1], 10);
                    const d = parseInt(partes[2], 10);
                    const dias = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO", "DOMINGO"];
                    const fecha = new Date(y, m - 1, d);
                    let dayIndex = fecha.getDay() - 1;
                    if (dayIndex === -1) dayIndex = 6;
                    return `${{dias[dayIndex]}}, ${{String(d).padStart(2, '0')}}/${{String(m).padStart(2, '0')}}/${{y}}`;
                }}

                async function cargarCarryoverGastosGenerales(fecha) {{
                    if ((window.m2_gastos_generales || []).length > 0 || !fecha) return;
                    try {{
                        const resp = await fetch(`/residencia/api/carryover?fecha=${{encodeURIComponent(fecha)}}`);
                        const data = await resp.json().catch(() => null);
                        if (resp.ok && data?.ok && Array.isArray(data.personal_gastos_generales) && data.personal_gastos_generales.length) {{
                            window.m2_gastos_generales = data.personal_gastos_generales;
                            if (typeof window.m2_render === 'function') window.m2_render();
                            guardarEstadoLocal();
                        }}
                    }} catch (error) {{
                        console.warn('No se pudo aplicar carry-over de gastos generales.', error);
                    }}
                }}

                function aplicarContenidoGuardado(contenido) {{
                    if (!contenido || typeof contenido !== 'object') return;
                    if (contenido.estado_local?.campos) aplicarCamposFormulario(contenido.estado_local.campos);
                    const listasGuardadas = contenido.estado_local?.listas || {{}};
                    if (Array.isArray(listasGuardadas.catalogoMaestro)) window.catalogoMaestro = listasGuardadas.catalogoMaestro;
                    if (Array.isArray(listasGuardadas.m2_gastos_base)) window.m2_gastos_base = listasGuardadas.m2_gastos_base;
                    if (Array.isArray(listasGuardadas.m2_gastos_generales)) window.m2_gastos_generales = listasGuardadas.m2_gastos_generales;
                    if (Array.isArray(contenido.personal_gastos_generales) && !(window.m2_gastos_generales || []).length) window.m2_gastos_generales = contenido.personal_gastos_generales;
                    if (Array.isArray(listasGuardadas.m3_lista)) window.m3_lista = listasGuardadas.m3_lista;
                    if (Array.isArray(listasGuardadas.m4_lista)) window.m4_lista = listasGuardadas.m4_lista;
                    if (Array.isArray(listasGuardadas.m5_lista)) window.m5_lista = listasGuardadas.m5_lista;
                    if (Array.isArray(listasGuardadas.m6_lista)) window.m6_lista = listasGuardadas.m6_lista;
                    if (listasGuardadas.m8_base) window.m8_base = listasGuardadas.m8_base;
                    if (listasGuardadas.m8_registros) window.m8_registros = listasGuardadas.m8_registros;
                    if (listasGuardadas.m8_entidad_actual) window.m8_entidad_actual = listasGuardadas.m8_entidad_actual;
                    if (listasGuardadas.m8_entidades_registradas) window.m8_entidades_registradas = listasGuardadas.m8_entidades_registradas;
                    if (Array.isArray(listasGuardadas.m9_herramientas)) window.m9_herramientas = listasGuardadas.m9_herramientas;
                    if (Array.isArray(listasGuardadas.m9_seleccionadas)) window.m9_seleccionadas = listasGuardadas.m9_seleccionadas;
                    if (listasGuardadas.m10_tipo_actual) window.m10_tipo_actual = listasGuardadas.m10_tipo_actual;
                    const datos = contenido.datos || {{}};
                    const asignar = (id, valor) => {{
                        const el = document.getElementById(id);
                        if (el && typeof valor !== 'undefined' && valor !== null) el.value = valor;
                    }};
                    asignar('v_jornal_m', datos.jornal_m);
                    asignar('v_jornal_t', datos.jornal_t);
                    asignar('v_clima', datos.clima);
                    asignar('v_oper', datos.personal?.operario);
                    asignar('v_ofic', datos.personal?.oficiales);
                    asignar('v_peon', datos.personal?.peones);
                    asignar('v_meca', datos.personal?.mecanicos);
                    asignar('v_ctrl', datos.personal?.controladores);
                    asignar('v_ope_maq', datos.personal?.operadores);
                    if (Array.isArray(datos.personal_gastos_generales)) window.m2_gastos_generales = datos.personal_gastos_generales;
                    asignar('v_almacen', datos.almacen);
                    asignar('v_maquina', datos.maquinaria);
                    asignar('v_herram', datos.herramientas);
                    asignar('v_ocurrencia', datos.ocurrencia);
                    if (Array.isArray(datos.m3)) window.m3_lista = datos.m3;
                    if (Array.isArray(datos.m4)) window.m4_lista = datos.m4;
                    if (Array.isArray(datos.m5)) window.m5_lista = datos.m5;
                    if (Array.isArray(datos.m6)) window.m6_lista = datos.m6;
                    restaurarRenderModulos();
                    window.samuActualizarCuaderno();
                }}

                async function iniciarAsientoDesdeParametrosURL() {{
                    const params = new URLSearchParams(window.location.search || '');
                    const fecha = params.get('fecha');
                    const numero = params.get('asiento');
                    const modo = params.get('modo') || 'nuevo';
                    const moduloDestino = Math.max(1, Math.min(10, parseInt(params.get('paso') || params.get('modulo') || '1', 10) || 1));
                    if (!fecha || !numero) return false;

                    try {{ localStorage.removeItem(estadoKey); }} catch (e) {{}}
                    window.__samuModuloInicial = moduloDestino;
                    try {{
                        localStorage.setItem(moduloActivoKey, String(moduloDestino));
                        sessionStorage.setItem(moduloActivoKey, String(moduloDestino));
                    }} catch (e) {{}}
                    const inputNumero = document.getElementById('initNumAsiento');
                    const inputFecha = document.getElementById('initFecha');
                    if (inputNumero) inputNumero.value = String(numero).replace(/\\D/g, '');
                    if (inputFecha) inputFecha.value = fecha;
                    window.iniciarAsientoSeguro();
                    if (modo !== 'continuar') await cargarCarryoverGastosGenerales(fecha);

                    if (modo === 'continuar') {{
                        try {{
                            const resp = await fetch(`/residencia/api/asiento/${{encodeURIComponent(numero)}}`);
                            const data = await resp.json().catch(() => null);
                            const asiento = data && data.ok ? data.asiento : null;
                            if (!asiento) return true;
                            if (['Cerrado', 'Firmado'].includes(asiento.estado) || (asiento.bloqueado && asiento.estado !== 'Enviado Inspector')) {{
                                window.location.href = `/cuaderno/asiento/${{encodeURIComponent(numero)}}`;
                                return true;
                            }}
                            let contenido = asiento.contenido || {{}};
                            if (typeof contenido === 'string') {{
                                try {{ contenido = JSON.parse(contenido); }} catch (e) {{ contenido = {{}}; }}
                            }}
                            window.g_numAsiento = String(asiento.numero || numero);
                            window.g_fechaRaw = asiento.fecha || fecha;
                            window.g_fechaAsiento = contenido.fecha_texto || fechaTextoLocal(window.g_fechaRaw);
                            if (typeof g_numAsiento !== 'undefined') g_numAsiento = window.g_numAsiento;
                            if (typeof g_fechaRaw !== 'undefined') g_fechaRaw = window.g_fechaRaw;
                            if (typeof g_fechaAsiento !== 'undefined') g_fechaAsiento = window.g_fechaAsiento;
                            const lblFecha = document.getElementById('lbl_hoja_fecha');
                            if (lblFecha) lblFecha.innerText = window.g_fechaAsiento;
                            aplicarContenidoGuardado(contenido);
                            guardarEstadoLocal();
                            window.irModulo(moduloDestino);
                            if (typeof mostrarAlerta === 'function') mostrarAlerta(`Borrador N° ${{numero}} cargado sin modificar la base de datos.`, 'success');
                        }} catch (error) {{
                            console.error('No se pudo cargar el borrador guardado.', error);
                        }}
                    }}
                    if (modo !== 'continuar') window.irModulo(moduloDestino);
                    return true;
                }}

                document.addEventListener('DOMContentLoaded', function() {{
                    const form = document.getElementById('formResidencia');
                    if (form) {{
                        const refrescarYGuardar = () => {{
                            guardarDraftAsientoCliente();
                            clearTimeout(window.__samuRefrescoTimer);
                            window.__samuRefrescoTimer = setTimeout(() => {{
                                window.samuActualizarCuaderno();
                                guardarEstadoLocal();
                                programarAutoGuardadoContinuo();
                            }}, 35);
                        }};
                        ['input', 'change'].forEach(evento => {{
                            form.addEventListener(evento, refrescarYGuardar);
                        }});
                        form.addEventListener('click', () => {{
                            setTimeout(refrescarYGuardar, 0);
                        }});
                        document.addEventListener('modulo:cambio', guardarDraftAsientoCliente);
                    }}
                    (async () => {{
                        const iniciadoDesdeURL = await iniciarAsientoDesdeParametrosURL();
                        if (!iniciadoDesdeURL) {{
                            if (!restaurarDraftAsientoCliente()) restaurarEstadoLocal();
                        }} else {{
                            restaurarDraftAsientoCliente();
                        }}
                        document.documentElement.classList.remove('samu-restoring');
                    }})();
                    window.addEventListener('beforeunload', guardarEstadoLocalInmediato);
                    window.addEventListener('pagehide', guardarEstadoLocalInmediato);
                    document.addEventListener('visibilitychange', () => {{
                        if (document.visibilityState === 'hidden') guardarEstadoLocalInmediato();
                    }});
                }});
            }})();
        </script>
    </body>
    </html>
    """
    return render_template_string(html_completo, menu_superior=menu_superior, fecha_hoy_iso=fecha_hoy_iso, numero_hoja=numero_hoja)
