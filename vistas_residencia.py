# =========================================================
# vistas_residencia.py
# Módulo Maestro: Ensamblador Final del Cuaderno de Obra
# =========================================================

from flask import Blueprint, render_template_string, session, redirect, url_for, request, jsonify
from navbar import obtener_navbar
from datetime import datetime
from cuaderno_obra import CUADERNO_OBRA_CSS, CUADERNO_OBRA_JS, obtener_cuaderno_obra_html
from resumen_cuaderno import RESUMEN_CUADERNO_HTML
from cuaderno_store import guardar_asiento, obtener_asiento

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


@residencia_bp.route('/residencia/api/asiento', methods=['POST'])
def api_guardar_asiento():
    if 'usuario_id' not in session:
        return jsonify({"ok": False, "error": "No autorizado"}), 401

    data = request.get_json(silent=True) or {}
    try:
        numero = int(data.get("numero"))
        avance = max(0, min(100, int(data.get("avance", 0))))
    except (TypeError, ValueError):
        return jsonify({"ok": False, "error": "Número de asiento o avance inválido"}), 400

    estado = data.get("estado") or "Borrador"
    if estado not in ("Borrador", "Cerrado"):
        estado = "Borrador"

    if estado == "Borrador":
        existente = obtener_asiento(numero)
        if existente and existente.get("estado") == "Cerrado" and session.get("rol") != "Admin":
            return jsonify({"ok": False, "error": "El asiento está cerrado. Solo el dueño/Admin puede editarlo."}), 403

    resultado = guardar_asiento(
        numero=numero,
        fecha=data.get("fecha") or datetime.now().strftime('%Y-%m-%d'),
        estado=estado,
        avance=avance,
        contenido=data.get("contenido") or {},
        usuario=session.get("nombre", "Sistema"),
    )
    status = 200 if resultado.get("ok") else 500
    return jsonify(resultado), status

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
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Caveat:wght@600;700&display=swap');
            :root {{ --apple-text: #1d1d1f; --celeste-obra: #0263a0; --nav-height: 52px; }}
            body {{ font-family: 'Inter', sans-serif; color: var(--apple-text); overflow-x: hidden; padding-bottom: 90px; margin: 0; background: linear-gradient(135deg, rgba(255,255,255,1) 0%, rgba(2,99,160,0.08) 40%, rgba(135,206,235,0.12) 70%, rgba(249,168,212,0.12) 100%); background-attachment: fixed; }}
            
            @keyframes floatInUp {{ from {{ opacity: 0; transform: translateY(30px); }} to {{ opacity: 1; transform: translateY(0); }} }}
            @keyframes floatOutDown {{ from {{ opacity: 1; transform: translateY(0); }} to {{ opacity: 0; transform: translateY(30px); }} }}
            
            .stepper-container {{ position: fixed; top: var(--nav-height); left: 0; width: 100%; background: rgba(255,255,255,0.84); backdrop-filter: blur(22px); border-bottom: 1px solid rgba(15,23,42,0.08); z-index: 900; padding: 14px 18px 16px; overflow-x: auto; white-space: nowrap; display: grid; grid-template-columns: repeat(11, minmax(106px, 1fr)); align-items: center; gap: 10px; opacity: 0; pointer-events: none; transition: opacity 0.5s; box-shadow: 0 14px 35px rgba(15,23,42,0.05); }}
            .stepper-container::-webkit-scrollbar {{ display: none; }}
            .step-btn {{ position: relative; border: 1px solid #dbeafe; border-radius: 999px; padding: 10px 16px 10px 34px; min-width: 112px; max-width: 175px; font-size: 10.5px; line-height: 1.15; font-weight: 800; color: #475569; background: rgba(255,255,255,0.92); cursor: pointer; transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease, background .22s ease; transform-origin: center; box-shadow: 0 8px 20px rgba(15,23,42,0.04); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
            .step-btn::before {{ content: attr(data-percent); position: absolute; left: 7px; top: 50%; transform: translateY(-50%); width: 22px; height: 22px; border-radius: 50%; display: grid; place-items: center; background: #f1f5f9; color: #64748b; font-size: 8px; font-weight: 900; box-shadow: inset 0 0 0 1px #e2e8f0; }}
            .step-btn::after {{ content: ""; position: absolute; left: 12px; right: 12px; bottom: -7px; height: 3px; border-radius: 999px; background: linear-gradient(90deg, #0284c7 var(--pct, 0%), #e2e8f0 0); opacity: .9; }}
            .step-btn:hover {{ transform: translateY(-2px) scale(1.03); border-color: #0284c7; box-shadow: 0 16px 30px rgba(2,132,199,0.15); z-index: 3; }}
            .step-btn.active {{ background: #ffffff !important; color: #020617 !important; font-weight: 900 !important; transform: scale(1.04); box-shadow: 0 16px 35px rgba(15,23,42,0.15); border-color: #020617 !important; margin: 0 3px; }}
            .step-btn.completed {{ border-color: #22c55e; color: #166534; background: #f0fdf4; }}
            .step-btn.completed::before {{ content: "✓"; background: #22c55e; color: #fff; box-shadow: 0 6px 14px rgba(34,197,94,.25); }}
            .step-btn.missing {{ border-color: #fed7aa; color: #9a3412; background: #fff7ed; }}
            .step-btn.missing::before {{ background: #ffedd5; color: #9a3412; }}
            .step-btn.resumen {{ color: #fff; background: linear-gradient(135deg, #0f172a, #0263a0); border-color: #0263a0; }}
            .step-btn.resumen::before {{ content: "Ver"; width: 24px; background: rgba(255,255,255,.16); color: #fff; box-shadow: none; }}
            .step-btn.resumen::after {{ background: linear-gradient(90deg, #38bdf8 100%, #38bdf8 0); }}
            
            #globalTooltip {{ position: fixed; background: rgba(15, 23, 42, 0.94); backdrop-filter: blur(10px); color: #ffffff; padding: 10px 14px; border-radius: 14px; font-size: 11px; font-weight: 800; white-space: nowrap; box-shadow: 0 18px 35px rgba(15,23,42,0.25); pointer-events: none; z-index: 999999; opacity: 0; transform: translateY(10px) scale(.96); transition: opacity 0.2s ease, transform 0.2s ease; border: 1px solid rgba(255,255,255,.12); }}
            #globalTooltip.visible {{ opacity: 1; transform: translateY(0); }}

            .elegant-alert {{ position: fixed; top: 20px; left: 50%; transform: translateX(-50%) translateY(-100px); background: rgba(255,255,255,0.95); backdrop-filter: blur(20px); border-radius: 50px; padding: 12px 25px; display: flex; align-items: center; gap: 12px; box-shadow: 0 15px 35px rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,1); z-index: 9999999; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); opacity: 0; pointer-events: none; }}
            .elegant-alert.show {{ transform: translateX(-50%) translateY(0); opacity: 1; }}

            .split-layout {{ display: flex; gap: 40px; max-width: 1500px; margin: 140px auto 0 auto; padding: 0 20px; align-items: flex-start; filter: blur(5px); pointer-events: none; transition: filter 0.5s; }}
            .split-layout.unlocked {{ filter: blur(0); pointer-events: all; }}
            .form-column {{ flex: 1; max-width: 600px; }}
            .preview-column {{ flex: 1; position: sticky; top: 140px; height: calc(100vh - 240px); overflow-y: auto; }}
            .mobile-preview-btn {{ position: fixed; right: 18px; bottom: 88px; z-index: 920; border: none; border-radius: 999px; padding: 13px 16px; color: #fff; background: linear-gradient(135deg, #0f172a, #0263a0); box-shadow: 0 18px 38px rgba(15,23,42,.26); font-size: 12px; font-weight: 900; display: none; align-items: center; gap: 8px; opacity: 0; pointer-events: none; transform: translateY(12px); transition: .25s ease; }}
            .mobile-preview-btn.unlocked {{ opacity: 1; pointer-events: all; transform: translateY(0); }}
            
            .step-view {{ display: none; opacity: 0; background: rgba(255,255,255,0.85); backdrop-filter: blur(25px); padding: 30px; border-radius: 20px; box-shadow: 0 4px 25px rgba(0,0,0,0.03); border: 1px solid rgba(255,255,255,1);}}
            .step-view.active {{ display: block; animation: floatInUp 0.35s forwards; }}
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
            .asiento-lock-banner {{ display: none; position: fixed; left: 50%; bottom: 76px; transform: translateX(-50%); z-index: 930; border-radius: 999px; padding: 10px 16px; background: #0f172a; color: #fff; font-size: 12px; font-weight: 800; box-shadow: 0 18px 34px rgba(15,23,42,.22); }}
            .asiento-lock-banner.visible {{ display: inline-flex; gap: 8px; align-items: center; }}
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
                .stepper-container {{ grid-template-columns: repeat(11, minmax(116px, 1fr)); }}
                .split-layout {{ gap: 22px; padding: 0 16px; }}
                .form-column {{ max-width: 560px; }}
            }}
            @media (max-width: 992px) {{
                body {{ padding-bottom: 112px; }}
                .stepper-container {{ padding: 12px 12px 15px; display: flex; gap: 8px; overflow-x: auto; }}
                .step-btn {{ flex: 0 0 auto; min-width: 126px; max-width: 170px; padding-right: 16px; }}
                .step-btn:hover {{ transform: translateY(-2px) scale(1.02); }}
                .step-btn.active {{ transform: scale(1.02); margin: 0 2px; }}
                .split-layout {{ display: block; max-width: 760px; margin-top: 132px; padding: 0 14px; }}
                .form-column {{ max-width: none; width: 100%; }}
                .preview-column {{ display: none; }}
                .mobile-preview-btn {{ display: inline-flex; }}
                .step-view {{ padding: 22px; border-radius: 22px; }}
                .bottom-bar {{ padding: 12px 14px; gap: 10px; }}
                .bottom-bar .btn {{ padding-left: 16px !important; padding-right: 16px !important; font-size: 12px; }}
                .asiento-lock-banner {{ bottom: 90px; max-width: calc(100vw - 24px); border-radius: 18px; }}
            }}
            @media (max-width: 576px) {{
                .split-layout {{ margin-top: 126px; padding: 0 10px; }}
                .step-view {{ padding: 18px 14px; border-radius: 20px; }}
                .step-title {{ font-size: 18px; margin-bottom: 18px; }}
                .mobile-preview-btn {{ right: 12px; bottom: 82px; padding: 12px 14px; }}
                .bottom-bar {{ align-items: center; }}
                .bottom-bar .d-flex {{ gap: 6px !important; }}
            }}
        </style>
    </head>
    <body>
        {{{{ menu_superior | safe }}}}

        <div id="elegantAlert" class="elegant-alert"><div class="alert-icon" id="alertIcon"></div><div class="alert-text" id="alertText">Mensaje</div></div>

        <div class="modal fade" id="modalConfigInicial" data-bs-backdrop="static" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content inicio-asiento-card">
                    <div class="inicio-asiento-hero">
                        <div class="inicio-asiento-icon"><i class="bi bi-journal-richtext"></i></div>
                        <h4>Apertura de Asiento</h4>
                        <p>Ingrese el número y fecha para comenzar la redacción del cuaderno.</p>
                    </div>
                    <div class="inicio-asiento-body">
                        <div class="mb-3">
                            <label class="form-label fw-bold text-muted">N° de Asiento</label>
                            <input type="text" inputmode="numeric" pattern="[0-9]*" id="initNumAsiento" class="form-control form-control-lg inicio-input" placeholder="Ej: XXXX" oninput="this.value=this.value.replace(/\\D/g,'')" onkeydown="if(event.key==='Enter'){{event.preventDefault(); document.getElementById('initFecha').focus();}}">
                        </div>
                        <div class="mb-4">
                            <label class="form-label fw-bold text-muted">Fecha del Asiento</label>
                            <input type="date" id="initFecha" class="form-control form-control-lg inicio-input" value="{fecha_hoy_iso}">
                        </div>
                        <button type="button" id="btnComenzarRegistro" class="btn btn-primary btn-lg w-100 rounded-pill fw-bold shadow-sm">Comenzar registro <i class="bi bi-arrow-right ms-1"></i></button>
                        <div class="text-center text-muted small mt-3">También puede presionar <b>Enter</b> para avanzar.</div>
                    </div>
                </div>
            </div>
        </div>

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
            <button type="button" class="step-btn active" id="btnStep1" data-step="1" data-percent="0%" onclick="window.irModulo(1)">1. Jornal</button>
            <button type="button" class="step-btn" id="btnStep2" data-step="2" data-percent="0%" onclick="window.irModulo(2)">2. Personal</button>
            <button type="button" class="step-btn" id="btnStep3" data-step="3" data-percent="0%" onclick="window.irModulo(3)">3. Partidas</button>
            <button type="button" class="step-btn" id="btnStep4" data-step="4" data-percent="0%" onclick="window.irModulo(4)">4. Mayor Metrado</button>
            <button type="button" class="step-btn" id="btnStep5" data-step="5" data-percent="0%" onclick="window.irModulo(5)">5. Sub Partidas</button>
            <button type="button" class="step-btn" id="btnStep6" data-step="6" data-percent="0%" onclick="window.irModulo(6)">6. Actividades</button>
            <button type="button" class="step-btn" id="btnStep7" data-step="7" data-percent="0%" onclick="window.irModulo(7)">7. Almacén</button>
            <button type="button" class="step-btn" id="btnStep8" data-step="8" data-percent="0%" onclick="window.irModulo(8)">8. Maquinaria</button>
            <button type="button" class="step-btn" id="btnStep9" data-step="9" data-percent="0%" onclick="window.irModulo(9)">9. Herramientas</button>
            <button type="button" class="step-btn" id="btnStep10" data-step="10" data-percent="0%" onclick="window.irModulo(10)">10. Ocurrencias</button>
            <button type="button" class="step-btn resumen" id="btnResumenCuaderno" data-percent="Ver" data-tooltip="Resumen del cuaderno · Vista previa completa" onclick="abrirResumenCuaderno()">Resumen</button>
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
                <button type="button" class="btn btn-warning fw-bold rounded-pill px-4 shadow-sm" onclick="guardarBorradorAsiento()"><i class="bi bi-save2"></i> Guardar borrador</button>
                <button type="button" class="btn btn-success fw-bold rounded-pill px-4 shadow-sm" onclick="cerrarAsiento()"><i class="bi bi-lock-fill"></i> Cerrar asiento</button>
                <button type="button" class="btn btn-dark fw-bold rounded-pill px-4 shadow-sm d-none" id="btnEditarComoDueno" onclick="habilitarEdicionComoDueno()"><i class="bi bi-unlock-fill"></i> Editar como dueño</button>
            </div>
            <div class="d-flex gap-2 align-items-center ms-auto" id="moduloNavActions">
                <button type="button" class="btn btn-outline-secondary fw-bold rounded-pill px-4" onclick="window.siguienteModulo()">Omitir</button>
                <button type="button" class="btn btn-dark fw-bold rounded-pill px-4" onclick="window.siguienteModulo()">Guardar y Continuar <i class="bi bi-arrow-right"></i></button>
            </div>
        </div>
        <div class="asiento-lock-banner" id="asientoLockBanner"><i class="bi bi-lock-fill"></i> Asiento cerrado. La edición está bloqueada.</div>

        <button type="button" class="mobile-preview-btn" id="mobilePreviewBtn" onclick="abrirResumenCuaderno()">
            <i class="bi bi-journal-text"></i> Ver cuaderno
        </button>

        {RESUMEN_CUADERNO_HTML}

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            function abrirModalInicialSeguro() {{
                const modalInicial = document.getElementById('modalConfigInicial');
                if (!modalInicial || modalInicial.dataset.abierto === '1') return;
                modalInicial.dataset.abierto = '1';
                try {{
                    if (window.bootstrap && bootstrap.Modal) {{
                        new bootstrap.Modal(modalInicial).show();
                    }} else {{
                        modalInicial.style.display = 'block';
                        modalInicial.removeAttribute('aria-hidden');
                        modalInicial.setAttribute('aria-modal', 'true');
                        modalInicial.classList.add('show');
                        document.body.classList.add('modal-open');
                        if (!document.querySelector('.modal-backdrop')) {{
                            const fondo = document.createElement('div');
                            fondo.className = 'modal-backdrop fade show';
                            document.body.appendChild(fondo);
                        }}
                    }}
                    setTimeout(() => document.getElementById('initNumAsiento')?.focus(), 250);
                }} catch (e) {{
                    modalInicial.style.display = 'block';
                    modalInicial.classList.add('show');
                }}
            }}
            function cerrarModalInicialSeguro() {{
                const modalInicial = document.getElementById('modalConfigInicial');
                if (!modalInicial) return;
                try {{
                    const instancia = window.bootstrap && bootstrap.Modal
                        ? (bootstrap.Modal.getInstance(modalInicial) || new bootstrap.Modal(modalInicial))
                        : null;
                    if (instancia) {{
                        instancia.hide();
                    }}
                }} catch (e) {{}}
                modalInicial.classList.remove('show');
                modalInicial.style.display = 'none';
                modalInicial.setAttribute('aria-hidden', 'true');
                modalInicial.removeAttribute('aria-modal');
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
                    }} else {{
                        alert('Complete los datos para iniciar.');
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
            document.addEventListener('DOMContentLoaded', function() {{
                document.getElementById('btnComenzarRegistro')?.addEventListener('click', function(event) {{
                    event.preventDefault();
                    window.iniciarAsientoSeguro();
                }});
                document.getElementById('initFecha')?.addEventListener('keydown', function(event) {{
                    if (event.key === 'Enter') {{
                        event.preventDefault();
                        window.iniciarAsientoSeguro();
                    }}
                }});
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

            document.addEventListener("DOMContentLoaded", function() {{
                const modalInicial = document.getElementById('modalConfigInicial');
                modalInicial.addEventListener('shown.bs.modal', function () {{ document.getElementById('initNumAsiento').focus(); }});
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
                        tooltip.innerText = btn.dataset.tooltip || '';
                        const rect = btn.getBoundingClientRect();
                        tooltip.style.left = `${{rect.left + rect.width / 2}}px`;
                        tooltip.style.top = `${{rect.bottom + 12}}px`;
                        tooltip.style.transform = 'translateX(-50%) translateY(0) scale(1)';
                        tooltip.classList.add('visible');
                    }});
                    btn.addEventListener('mousemove', () => {{
                        const rect = btn.getBoundingClientRect();
                        tooltip.style.left = `${{rect.left + rect.width / 2}}px`;
                        tooltip.style.top = `${{rect.bottom + 12}}px`;
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
            function jumpToStep(stepIndex) {{ if (isAnimating || currentStep === stepIndex) return; isAnimating = true; const currentView = document.getElementById(`step${{currentStep}}`); currentView.classList.remove('active'); currentView.classList.add('exit'); document.getElementById(`btnStep${{currentStep}}`).classList.remove('active'); setTimeout(() => {{ currentView.classList.remove('exit'); currentStep = stepIndex; document.getElementById(`step${{currentStep}}`).classList.add('active'); document.getElementById(`btnStep${{currentStep}}`).classList.add('active'); const btnAtras = document.getElementById('btnAtras'); if (currentStep > 1) btnAtras.classList.remove('d-none'); else btnAtras.classList.add('d-none'); actualizarAccionesAsiento(); if (typeof sincronizarDatos === "function") sincronizarDatos(); isAnimating = false; }}, 300); }}
            function siguientePaso() {{ if (g_numAsiento && !asientoCerrado) autoGuardarBorrador(); if(currentStep < totalSteps) jumpToStep(currentStep + 1); }} function anteriorPaso() {{ if(currentStep > 1) jumpToStep(currentStep - 1); }} function omitirPaso() {{ siguientePaso(); }}

            function actualizarAccionesAsiento() {{
                const acciones = document.getElementById('asientoActions');
                if (acciones) acciones.classList.toggle('visible', currentStep === 10 || asientoCerrado);
                const navegacion = document.getElementById('moduloNavActions');
                if (navegacion) navegacion.classList.toggle('d-none', currentStep === 10);
                const btnAtras = document.getElementById('btnAtras');
                if (btnAtras) btnAtras.classList.toggle('d-none', currentStep <= 1 || currentStep === 10);
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
                    texto_html: document.getElementById('contenedorLineasCuaderno')?.innerHTML || '',
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

            async function enviarAsiento(estado, silencioso=false) {{
                if (!g_numAsiento || !g_fechaRaw) {{
                    if (!silencioso) mostrarAlerta("Primero inicie el asiento con número y fecha.", "error");
                    return null;
                }}
                if (asientoCerrado && !edicionDuenoActiva && rolUsuario !== 'Admin') {{
                    if (!silencioso) mostrarAlerta("Este asiento ya está cerrado y no puede modificarse.", "error");
                    return null;
                }}
                if (typeof sincronizarDatos === "function") sincronizarDatos();
                const payload = {{
                    numero: g_numAsiento,
                    fecha: g_fechaRaw,
                    estado: estado,
                    avance: avanceAsiento(),
                    contenido: contenidoAsiento()
                }};
                const resp = await fetch('/residencia/api/asiento', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(payload)
                }});
                const data = await resp.json().catch(() => ({{ ok: false, error: 'Respuesta inválida del servidor' }}));
                if (!resp.ok || !data.ok) {{
                    if (!silencioso) mostrarAlerta(data.error || "No se pudo guardar el asiento.", "error");
                    return null;
                }}
                return data;
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
                if (!confirm("Al cerrar el asiento ya no se podrá modificar. Solo el dueño/Admin podrá editarlo. ¿Desea cerrar el asiento?")) return;
                const data = await enviarAsiento('Cerrado');
                if (!data) return;
                asientoCerrado = true;
                edicionDuenoActiva = false;
                bloquearEdicionAsiento();
                mostrarAlerta("Asiento cerrado y guardado correctamente.", "success");
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
                if (asiento.estado === 'Cerrado') {{
                    asientoCerrado = true;
                    bloquearEdicionAsiento();
                    mostrarAlerta("Este asiento ya fue cerrado. Se abrió en modo solo lectura.", "success");
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

                const personal = [
                    ['Operario', samuValor('v_oper')],
                    ['Oficiales', samuValor('v_ofic')],
                    ['Peones', samuValor('v_peon')],
                    ['Mecánicos', samuValor('v_meca')],
                    ['Controladores de maquinaria', samuValor('v_ctrl')],
                    ['Operadores de maquinaria', samuValor('v_ope_maq')]
                ].filter(([_, cantidad]) => parseInt(cantidad || 0) > 0)
                 .map(([nombre, cantidad]) => `(${{String(parseInt(cantidad || 0)).padStart(2, '0')}}) ${{nombre}}`);
                samuAgregarModulo(modulos, '2. Personal de obra', personal.join('    '));

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
                    const numero = String(g_numAsiento || window.g_numAsiento || '').trim();
                    const fecha = String(g_fechaAsiento || window.g_fechaAsiento || document.getElementById('lbl_hoja_fecha')?.innerText || '').trim();
                    const contenedor = document.getElementById('contenedorLineasCuaderno');
                    if (!contenedor || !numero) return;
                    const asiento = numero.padStart(4, '0');
                    const modulos = samuRedactarCuadernoCompleto();
                    contenedor.innerHTML = paginaHtml(asiento, fecha, modulos, false, false);
                }} catch (error) {{
                    console.error('No se pudo sincronizar el cuaderno:', error);
                }}
            }};

            sincronizarDatos = window.samuSincronizarCuaderno;

            document.addEventListener('DOMContentLoaded', function() {{
                const refrescar = () => setTimeout(window.samuSincronizarCuaderno, 30);
                document.getElementById('formResidencia')?.addEventListener('input', refrescar);
                document.getElementById('formResidencia')?.addEventListener('change', refrescar);
                document.getElementById('formResidencia')?.addEventListener('click', refrescar);
                setInterval(window.samuSincronizarCuaderno, 700);
            }});
        </script>

        <script>
            // Motor de seguridad independiente: si un script anterior falla, este mantiene vivo el cuaderno.
            (function() {{
                const totalModulos = 10;
                window.samuCurrentStep = window.samuCurrentStep || 1;

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

                function modulosCuaderno() {{
                    const modulos = [];
                    const jornal = [];
                    if (texto('v_jornal_m')) jornal.push(`Mañana: ${{texto('v_jornal_m')}}`);
                    if (texto('v_jornal_t')) jornal.push(`Tarde: ${{texto('v_jornal_t')}}`);
                    if (texto('v_clima')) jornal.push(`Clima: ${{texto('v_clima')}}`);
                    agregar(modulos, '1. Jornal de trabajo', jornal.join(', '));

                    const personal = [
                        ['Operario', texto('v_oper')],
                        ['Oficiales', texto('v_ofic')],
                        ['Peones', texto('v_peon')],
                        ['Mecánicos', texto('v_meca')],
                        ['Controladores de maquinaria', texto('v_ctrl')],
                        ['Operadores de maquinaria', texto('v_ope_maq')]
                    ].filter(([_, cantidad]) => parseInt(cantidad || 0) > 0)
                     .map(([nombre, cantidad]) => `(${{String(parseInt(cantidad || 0)).padStart(2, '0')}}) ${{nombre}}`);
                    agregar(modulos, '2. Personal de obra', personal.join('    '));

                    agregar(modulos, '3. Partidas ejecutadas', lista('m3_lista').map(itemPartida).join('\\n'));
                    agregar(modulos, '4. Partidas de mayor metrado', lista('m4_lista').map(itemPartida).join('\\n'));
                    agregar(modulos, '5. Sub partidas ejecutadas', lista('m5_lista').map(itemPartida).join('\\n'));
                    agregar(modulos, '6. Actividades ejecutadas', lista('m6_lista').map(itemPartida).join('\\n'));
                    agregar(modulos, '7. Movimiento de almacén', texto('v_almacen', true));
                    agregar(modulos, '8. Maquinarias y equipos', texto('v_maquina', true));
                    agregar(modulos, '9. Herramientas manuales', texto('v_herram', true));
                    agregar(modulos, '10. Ocurrencias y otros', texto('v_ocurrencia', true));
                    const paso = Math.max(1, Math.min(totalModulos, parseInt(window.samuCurrentStep || 1, 10) || 1));
                    return modulos.slice(0, paso);
                }}

                function htmlContenidoModulo(modulo) {{
                    if (modulo.titulo.startsWith('7.') && typeof htmlAlmacen === 'function') {{
                        return `<div class="almacen-bloque">${{htmlAlmacen(modulo.contenido)}}</div>`;
                    }}
                    if (modulo.titulo.startsWith('8.') && typeof htmlMaquinaria === 'function') {{
                        return `<div class="maquinaria-bloque">${{htmlMaquinaria(modulo.contenido)}}</div>`;
                    }}
                    return `<span class="modulo-contenido">${{escapar(modulo.contenido).replace(/\\n/g, '<br>')}}</span>`;
                }}

                function htmlCuaderno(asiento, fecha, modulos) {{
                    const contenido = modulos.map(modulo => `
                        <div class="modulo-redaccion">
                            <span class="modulo-titulo">${{escapar(modulo.titulo)}}</span>
                            ${{htmlContenidoModulo(modulo)}}
                        </div>
                    `).join('');

                    return `
                        <div class="pagina-cuaderno">
                            <div class="lapicero">
                                <div class="encabezado-asiento">
                                    <div class="titulo-asiento">ASIENTO N° ${{escapar(asiento)}} DEL RESIDENTE DE OBRA</div>
                                    <div class="fecha-asiento">${{escapar(fecha)}}</div>
                                </div>
                                ${{contenido}}
                            </div>
                        </div>
                    `;
                }}

                window.samuActualizarCuaderno = function() {{
                    const numero = String(window.g_numAsiento || (typeof g_numAsiento !== 'undefined' ? g_numAsiento : '') || '').trim();
                    const fecha = String(window.g_fechaAsiento || (typeof g_fechaAsiento !== 'undefined' ? g_fechaAsiento : '') || document.getElementById('lbl_hoja_fecha')?.innerText || '').trim();
                    const contenedor = document.getElementById('contenedorLineasCuaderno');
                    if (!contenedor || !numero) return;
                    contenedor.innerHTML = htmlCuaderno(numero.padStart(4, '0'), fecha, modulosCuaderno());
                }};

                window.irModulo = function(stepIndex) {{
                    const step = Math.max(1, Math.min(totalModulos, parseInt(stepIndex, 10) || 1));
                    window.samuCurrentStep = step;
                    if (typeof currentStep !== 'undefined') currentStep = step;
                    document.querySelectorAll('.step-view').forEach(vista => vista.classList.remove('active', 'exit'));
                    document.querySelectorAll('.step-btn').forEach(btn => btn.classList.remove('active'));
                    document.getElementById(`step${{step}}`)?.classList.add('active');
                    document.getElementById(`btnStep${{step}}`)?.classList.add('active');
                    document.getElementById('btnAtras')?.classList.toggle('d-none', step <= 1 || step === 10);
                    document.getElementById('asientoActions')?.classList.toggle('visible', step === 10);
                    document.getElementById('moduloNavActions')?.classList.toggle('d-none', step === 10);
                    setTimeout(window.samuActualizarCuaderno, 30);
                }};

                window.siguienteModulo = function() {{
                    window.irModulo((window.samuCurrentStep || 1) + 1);
                }};

                window.anteriorModulo = function() {{
                    window.irModulo((window.samuCurrentStep || 1) - 1);
                }};

                window.iniciarAsientoSeguro = function() {{
                    const numero = String(document.getElementById('initNumAsiento')?.value || '').trim();
                    const fecha = String(document.getElementById('initFecha')?.value || '').trim();
                    if (!numero || !fecha) {{
                        if (typeof mostrarAlerta === 'function') mostrarAlerta('Complete los datos para iniciar.', 'error');
                        else alert('Complete los datos para iniciar.');
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
                    if (typeof g_numAsiento !== 'undefined') g_numAsiento = window.g_numAsiento;
                    if (typeof g_fechaRaw !== 'undefined') g_fechaRaw = window.g_fechaRaw;
                    if (typeof g_fechaAsiento !== 'undefined') g_fechaAsiento = window.g_fechaAsiento;

                    const fechaCuaderno = document.getElementById('lbl_hoja_fecha');
                    if (fechaCuaderno) fechaCuaderno.innerText = window.g_fechaAsiento;

                    document.getElementById('modalConfigInicial')?.classList.remove('show');
                    const modal = document.getElementById('modalConfigInicial');
                    if (modal) {{
                        modal.style.display = 'none';
                        modal.setAttribute('aria-hidden', 'true');
                    }}
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
                    window.irModulo(1);
                    window.samuActualizarCuaderno();
                }};

                async function guardarAsientoSeguro(estado) {{
                    window.samuActualizarCuaderno();
                    const numero = String(window.g_numAsiento || '').trim();
                    const fecha = String(window.g_fechaRaw || '').trim();
                    if (!numero || !fecha) {{
                        if (typeof mostrarAlerta === 'function') mostrarAlerta('Primero inicie el asiento.', 'error');
                        return;
                    }}
                    const payload = {{
                        numero,
                        fecha,
                        estado,
                        avance: 100,
                        contenido: {{
                            numero,
                            fecha,
                            fecha_texto: window.g_fechaAsiento || '',
                            modulos: modulosCuaderno(),
                            texto_html: document.getElementById('contenedorLineasCuaderno')?.innerHTML || ''
                        }}
                    }};
                    const resp = await fetch('/residencia/api/asiento', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(payload)
                    }});
                    const data = await resp.json().catch(() => ({{ ok: false, error: 'Respuesta inválida' }}));
                    if (!resp.ok || !data.ok) {{
                        if (typeof mostrarAlerta === 'function') mostrarAlerta(data.error || 'No se pudo guardar.', 'error');
                        return;
                    }}
                    if (typeof mostrarAlerta === 'function') mostrarAlerta(estado === 'Cerrado' ? 'Asiento cerrado correctamente.' : 'Borrador guardado correctamente.', 'success');
                    setTimeout(() => {{
                        window.redirigirCuadernoAlCerrarResumen = true;
                        if (typeof abrirResumenCuaderno === 'function') abrirResumenCuaderno();
                    }}, 450);
                }}

                window.guardarBorradorAsiento = function() {{ guardarAsientoSeguro('Borrador'); }};
                window.cerrarAsiento = function() {{
                    if (confirm('Al cerrar el asiento ya no se podrá modificar. ¿Desea cerrar el asiento?')) guardarAsientoSeguro('Cerrado');
                }};

                document.addEventListener('DOMContentLoaded', function() {{
                    document.getElementById('btnComenzarRegistro')?.addEventListener('click', function(event) {{
                        event.preventDefault();
                        window.iniciarAsientoSeguro();
                    }});
                    document.getElementById('initFecha')?.addEventListener('keydown', function(event) {{
                        if (event.key === 'Enter') {{
                            event.preventDefault();
                            window.iniciarAsientoSeguro();
                        }}
                    }});
                    const form = document.getElementById('formResidencia');
                    if (form) {{
                        ['input', 'change', 'click', 'keyup'].forEach(evento => {{
                            form.addEventListener(evento, () => setTimeout(window.samuActualizarCuaderno, 40));
                        }});
                    }}
                    setInterval(window.samuActualizarCuaderno, 800);
                }});
            }})();
        </script>
    </body>
    </html>
    """
    return render_template_string(html_completo, menu_superior=menu_superior, fecha_hoy_iso=fecha_hoy_iso, numero_hoja=numero_hoja)
