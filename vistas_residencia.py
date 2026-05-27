# =========================================================
# vistas_residencia.py
# Módulo Maestro: Ensamblador Final del Cuaderno de Obra
# =========================================================

from flask import Blueprint, render_template_string, session, redirect, url_for
from navbar import obtener_navbar
from datetime import datetime

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

ALMACEN_HTML = "<div class='step-view' id='step7'><div class='step-title'>7.- Almacén</div><textarea class='form-control req-step7' id='v_almacen' rows='5' oninput='sincronizarDatos()'></textarea></div>"
MAQUINARIA_HTML = "<div class='step-view' id='step8'><div class='step-title'>8.- Maquinaria</div><textarea class='form-control req-step8' id='v_maquina' rows='5' oninput='sincronizarDatos()'></textarea></div>"
HERRAMIENTAS_HTML = "<div class='step-view' id='step9'><div class='step-title'>9.- Herramientas</div><textarea class='form-control req-step9' id='v_herram' rows='4' oninput='sincronizarDatos()'></textarea></div>"
OCURRENCIAS_HTML = "<div class='step-view' id='step10'><div class='step-title text-danger'>10.- Ocurrencias</div><textarea class='form-control border-danger req-step10' id='v_ocurrencia' rows='6' oninput='sincronizarDatos()'></textarea></div>"

residencia_bp = Blueprint('residencia', __name__)

@residencia_bp.route('/residencia')
def redaccion_asiento_residente():
    if 'usuario_id' not in session: return redirect(url_for('login.mostrar_login'))

    es_admin = session.get('rol') == 'Admin'
    nombre_completo = session.get('nombre', 'Ing. Samuel Gutierrez')
    menu_superior = obtener_navbar(es_admin, nombre_completo)
    fecha_hoy_iso = datetime.now().strftime('%Y-%m-%d')
    numero_hoja = "0001"

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
            
            .stepper-container {{ position: fixed; top: var(--nav-height); left: 0; width: 100%; background: rgba(255,255,255,0.85); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(0,0,0,0.08); z-index: 900; padding: 15px 20px; overflow-x: auto; white-space: nowrap; display: flex; align-items: center; gap: 8px; opacity: 0; pointer-events: none; transition: opacity 0.5s; }}
            .stepper-container::-webkit-scrollbar {{ display: none; }}
            .step-btn {{ border: 1px solid #cbd5e1; border-radius: 30px; padding: 10px 20px; font-size: 12px; font-weight: 600; color: #475569; background: rgba(255,255,255,0.9); cursor: pointer; transition: all 0.3s; transform-origin: center; }}
            .step-btn.active {{ background: #ffffff !important; color: #000000 !important; font-weight: 800 !important; transform: scale(1.15); box-shadow: 0 10px 25px rgba(0,0,0,0.12); border-color: #000000 !important; margin: 0 10px; }}
            
            #globalTooltip {{ position: fixed; background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(8px); color: #ffffff; padding: 8px 16px; border-radius: 8px; font-size: 12px; font-weight: 600; white-space: nowrap; box-shadow: 0 10px 25px rgba(0,0,0,0.2); pointer-events: none; z-index: 999999; opacity: 0; transform: translateY(10px); transition: opacity 0.2s ease, transform 0.2s ease; }}
            #globalTooltip.visible {{ opacity: 1; transform: translateY(0); }}

            .elegant-alert {{ position: fixed; top: 20px; left: 50%; transform: translateX(-50%) translateY(-100px); background: rgba(255,255,255,0.95); backdrop-filter: blur(20px); border-radius: 50px; padding: 12px 25px; display: flex; align-items: center; gap: 12px; box-shadow: 0 15px 35px rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,1); z-index: 9999999; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); opacity: 0; pointer-events: none; }}
            .elegant-alert.show {{ transform: translateX(-50%) translateY(0); opacity: 1; }}

            .split-layout {{ display: flex; gap: 40px; max-width: 1500px; margin: 140px auto 0 auto; padding: 0 20px; align-items: flex-start; filter: blur(5px); pointer-events: none; transition: filter 0.5s; }}
            .split-layout.unlocked {{ filter: blur(0); pointer-events: all; }}
            .form-column {{ flex: 1; max-width: 600px; }}
            .preview-column {{ flex: 1; position: sticky; top: 140px; height: calc(100vh - 240px); overflow-y: auto; }}
            
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

            /* ==========================================
               CUADERNO FÍSICO CORREGIDO (TEXTO CONTINUO)
               ========================================== */
            .papel-fisico {{ background: #fdfdfa; width: 100%; min-height: 980px; padding: 45px 50px; box-shadow: 0 15px 40px rgba(0,0,0,0.08); border: 1px solid #e2e8f0; font-family: Arial, sans-serif; color: #000; position: relative;}}
            .p-header-top {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 25px; }} 
            .p-title-box {{ text-align: center; flex: 1; margin-left: 60px;}}
            .p-title-box h1 {{ font-size: 28px; font-weight: bold; text-decoration: underline; letter-spacing: 1.5px; margin: 0;}}
            .p-num {{ font-size: 24px; font-weight: bold; }}
            .p-meta {{ margin-bottom: 12px; padding-bottom: 14px; border-bottom: 3px solid #000; }}
            .p-row {{ display: flex; align-items: flex-end; margin-bottom: 6px; }}
            .p-label {{ font-size: 14px; font-weight: bold; margin-right: 8px; }}
            .p-line {{ flex: 1; border-bottom: 1px solid #000; position: relative; height: 20px; }}
            .lapicero-meta {{ position: absolute; bottom: -1px; left: 10px; font-family: 'Caveat', cursive; color: var(--celeste-obra); font-size: 22px; font-weight: 700; white-space: nowrap; }}
            
            .p-body-lines {{ background-image: repeating-linear-gradient(transparent, transparent 27px, #cbd5e1 28px); line-height: 28px; min-height: 650px; padding-top: 2px; position: relative; margin-top: 15px;}}
            
            /* Lapicero ahora está justificado para simular el párrafo continuo */
            .lapicero {{ font-family: 'Caveat', cursive; color: var(--celeste-obra); font-size: 22px; line-height: 28px; padding-left: 2px; font-weight: 700; text-align: justify; word-wrap: break-word; }}
            
            .p-break-page {{ border-top: 2px dashed #94a3b8; margin: 35px 0 20px 0; padding-top: 15px; position: relative; }}
            .p-footer {{ display: flex; justify-content: space-between; margin-top: 50px; font-size: 12px; font-weight: bold; color: #000;}}
            .p-sig {{ border-top: 1px solid #000; width: 28%; text-align: center; padding-top: 5px; }}
            
            .bottom-bar {{ position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(255,255,255,0.95); backdrop-filter: blur(15px); border-top: 1px solid rgba(0,0,0,0.08); padding: 15px 30px; z-index: 900; display: flex; justify-content: space-between; align-items: center; opacity: 0; pointer-events: none; transition: opacity 0.5s;}}
            .bottom-bar.unlocked {{ opacity: 1; pointer-events: all; }}

            /* Estilos del Panel de Pegado Inteligente */
            .col-header {{ background: #f8fafc; border: 1px solid #cbd5e1; border-bottom: none; border-radius: 8px 8px 0 0; padding: 8px; text-align: center; font-size: 11px; font-weight: 800; color: #475569; letter-spacing: 0.5px; }}
            .col-textarea {{ border-radius: 0 0 8px 8px; border: 1px solid #cbd5e1; font-size: 12px; line-height: 1.8; padding: 10px; resize: none; overflow-x: hidden; white-space: pre; background: #fff;}}
            .col-textarea:focus {{ border-color: #0263a0; box-shadow: 0 0 0 3px rgba(2,99,160,0.1); outline: none; }}
        </style>
    </head>
    <body>
        {{{{ menu_superior | safe }}}}

        <div id="elegantAlert" class="elegant-alert"><div class="alert-icon" id="alertIcon"></div><div class="alert-text" id="alertText">Mensaje</div></div>

        <div class="modal fade" id="modalConfigInicial" data-bs-backdrop="static" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content" style="border-radius: 24px; border: none; box-shadow: 0 20px 50px rgba(0,0,0,0.2);">
                    <div class="modal-header border-0 pb-0 justify-content-center mt-3"><h4 class="modal-title fw-bold text-primary"><i class="bi bi-journal-plus"></i> Apertura de Asiento</h4></div>
                    <div class="modal-body px-5 pb-4">
                        <div class="mb-3"><label class="form-label fw-bold">N° de Asiento</label><input type="number" id="initNumAsiento" class="form-control form-control-lg bg-light" placeholder="Ej: 88"></div>
                        <div class="mb-4"><label class="form-label fw-bold">Fecha del Asiento</label><input type="date" id="initFecha" class="form-control form-control-lg bg-light" value="{fecha_hoy_iso}"></div>
                        <button type="button" class="btn btn-primary btn-lg w-100 rounded-pill fw-bold" onclick="iniciarAsiento()">Iniciar Redacción</button>
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
            <button type="button" class="step-btn active" id="btnStep1" onclick="jumpToStep(1)">1. Jornal</button>
            <button type="button" class="step-btn" id="btnStep2" onclick="jumpToStep(2)">2. Personal</button>
            <button type="button" class="step-btn" id="btnStep3" onclick="jumpToStep(3)">3. Partidas</button>
            <button type="button" class="step-btn" id="btnStep4" onclick="jumpToStep(4)">4. Mayor Metrado</button>
            <button type="button" class="step-btn" id="btnStep5" onclick="jumpToStep(5)">5. Sub Partidas</button>
            <button type="button" class="step-btn" id="btnStep6" onclick="jumpToStep(6)">6. Actividades</button>
            <button type="button" class="step-btn" id="btnStep7" onclick="jumpToStep(7)">7. Almacén</button>
            <button type="button" class="step-btn" id="btnStep8" onclick="jumpToStep(8)">8. Maquinaria</button>
            <button type="button" class="step-btn" id="btnStep9" onclick="jumpToStep(9)">9. Herramientas</button>
            <button type="button" class="step-btn" id="btnStep10" onclick="jumpToStep(10)">10. Ocurrencias</button>
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
                <div class="papel-fisico" id="papelOficial">
                    <div class="p-header-top">
                        <div style="width: 80px;"></div>
                        <div class="p-title-box"><h1>CUADERNO DE OBRA</h1></div>
                        <div style="text-align: right; width: 80px;"><div class="p-num">Nº <span style="font-size: 26px; margin-left:3px;">{numero_hoja}</span></div></div>
                    </div>
                    <div class="p-meta">
                        <div class="d-flex w-100 mb-1">
                            <div class="d-flex" style="flex: 0.5;"><span class="p-label">Fecha:</span><div class="p-line"><span class="lapicero-meta" id="lbl_hoja_fecha">--</span></div></div>
                            <div class="d-flex" style="flex: 0.5; margin-left: 15px;"><span class="p-label">Modalidad:</span><div class="p-line"><span class="lapicero-meta">Administración Directa</span></div></div>
                        </div>
                        <div class="p-row"><span class="p-label">Obra:</span><div class="p-line"><span class="lapicero-meta">Mejoramiento de la Carretera Asiruni - Rosaspata</span></div></div>
                        <div class="p-row"><span class="p-label">Proyecto:</span><div class="p-line"><span class="lapicero-meta">Tramo I</span></div></div>
                        <div class="p-row"><span class="p-label">Programa:</span><div class="p-line"><span class="lapicero-meta">-</span></div></div>
                        <div class="p-row"><span class="p-label">Entidad Ejecutora:</span><div class="p-line"><span class="lapicero-meta">Gobierno Regional Puno</span></div></div>
                    </div>

                    <div class="p-body-lines" id="contenedorLineasCuaderno">
                        <div class="lapicero" id="out_general"></div>
                    </div>
                    <div class="p-footer">
                        <div class="p-sig">ING. INSPECTOR</div><div class="p-sig">ING. RESIDENTE</div><div class="p-sig">ING. SUPERVISOR</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="bottom-bar shadow-lg" id="bottomBarUI">
            <button type="button" id="btnAtras" class="btn btn-light border fw-bold rounded-pill px-4 text-dark shadow-sm d-none" onclick="anteriorPaso()"><i class="bi bi-arrow-left"></i> Anterior</button>
            <div class="d-flex gap-2 align-items-center ms-auto">
                <button type="button" class="btn btn-outline-secondary fw-bold rounded-pill px-4" onclick="omitirPaso()">Omitir</button>
                <button type="button" class="btn btn-dark fw-bold rounded-pill px-4" onclick="siguientePaso()">Guardar y Continuar <i class="bi bi-arrow-right"></i></button>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        
        <script>
            // CONFIGURACIÓN GLOBAL
            let g_numAsiento = ""; let g_fechaAsiento = ""; let g_fechaRaw = "";
            let currentStep = 1; const totalSteps = 10; let isAnimating = false;
            
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

            document.addEventListener("DOMContentLoaded", function() {{ new bootstrap.Modal(document.getElementById('modalConfigInicial')).show(); }});
            function formatearFecha(fechaStr) {{ const dias = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO", "DOMINGO"]; const [y, m, d] = fechaStr.split('-'); const dateObj = new Date(y, m-1, d); let dayIndex = dateObj.getDay() - 1; if(dayIndex === -1) dayIndex = 6; return `${{dias[dayIndex]}}, ${{d}}/${{m}}/${{y}}`; }}
            
            function iniciarAsiento() {{ 
                g_numAsiento = document.getElementById('initNumAsiento').value; let rawDate = document.getElementById('initFecha').value; 
                if(!g_numAsiento || !rawDate) {{ mostrarAlerta("Complete los datos para iniciar.", "error"); return; }} 
                g_fechaRaw = rawDate; g_fechaAsiento = formatearFecha(rawDate); document.getElementById('lbl_hoja_fecha').innerText = g_fechaAsiento; 
                bootstrap.Modal.getInstance(document.getElementById('modalConfigInicial')).hide(); 
                document.getElementById('mainLayout').classList.add('unlocked'); document.getElementById('stepperBar').style.opacity = '1'; document.getElementById('stepperBar').style.pointerEvents = 'all'; document.getElementById('bottomBarUI').classList.add('unlocked'); sincronizarDatos(); 
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
            function jumpToStep(stepIndex) {{ if (isAnimating || currentStep === stepIndex) return; isAnimating = true; const currentView = document.getElementById(`step${{currentStep}}`); currentView.classList.remove('active'); currentView.classList.add('exit'); document.getElementById(`btnStep${{currentStep}}`).classList.remove('active'); setTimeout(() => {{ currentView.classList.remove('exit'); currentStep = stepIndex; document.getElementById(`step${{currentStep}}`).classList.add('active'); document.getElementById(`btnStep${{currentStep}}`).classList.add('active'); const btnAtras = document.getElementById('btnAtras'); if (currentStep > 1) btnAtras.classList.remove('d-none'); else btnAtras.classList.add('d-none'); isAnimating = false; }}, 300); }}
            function siguientePaso() {{ if(currentStep < totalSteps) jumpToStep(currentStep + 1); }} function anteriorPaso() {{ if(currentStep > 1) jumpToStep(currentStep - 1); }} function omitirPaso() {{ siguientePaso(); }}

            let t_m = true; let t_t = true;
            function toggleTurno(turno) {{ if(turno === 'm') {{ t_m = !t_m; document.getElementById('card_m').classList.toggle('active', t_m); document.getElementById('v_jornal_m').value = t_m ? "07:00 - 12:00" : ""; document.getElementById('lbl_jornal_m').style.opacity = t_m ? "1" : "0.3"; }} else {{ t_t = !t_t; document.getElementById('card_t').classList.toggle('active', t_t); document.getElementById('v_jornal_t').value = t_t ? "13:00 - 17:00" : ""; document.getElementById('lbl_jornal_t').style.opacity = t_t ? "1" : "0.3"; }} sincronizarDatos(); }}
            function evaluarTarjeta(id) {{ const val = document.getElementById('v_' + id).value; document.getElementById('c_' + id).classList.toggle('active', val > 0); sincronizarDatos(); }}

            // =====================================================================
            // MOTOR DE RENDERIZADO "TIPO ORACIÓN" CON PAGINACIÓN INTELIGENTE
            // =====================================================================
            function paginateText(texto, contenedorId, maxHeight) {{
                const container = document.getElementById(contenedorId);
                container.innerHTML = texto;
                if(container.offsetHeight <= maxHeight) return [texto, ""];
                
                // Búsqueda binaria para encontrar el corte perfecto de página
                let words = texto.split(' ');
                let low = 0, high = words.length;
                let best = 0;
                while(low <= high) {{
                    let mid = Math.floor((low + high) / 2);
                    container.innerHTML = words.slice(0, mid).join(' ') + ' ... Van';
                    if(container.offsetHeight <= maxHeight) {{ best = mid; low = mid + 1; }} 
                    else {{ high = mid - 1; }}
                }}
                return [words.slice(0, best).join(' '), words.slice(best).join(' ')];
            }}

            function sincronizarDatos() {{
                if(!g_numAsiento) return;
                let as_str = g_numAsiento.padStart(4, '0');
                
                let cabecera = `<div style="display:flex; justify-content:space-between; width:100%; margin-bottom: 5px; font-family: Arial, sans-serif;"><div style="padding-left:40px; font-weight:bold; font-size:17px; color:#000;">ASIENTO No ${{as_str}} DEL RESIDENTE DE OBRA</div><div style="padding-right:10px; font-weight:bold; font-size:17px; color:#000;">${{g_fechaAsiento}}</div></div>`;

                let parrafo = ""; // Aquí construiremos la "Oración continua"

                // 1. Jornal
                const vJm = document.getElementById('v_jornal_m'); const vJt = document.getElementById('v_jornal_t');
                const vJ1 = vJm ? vJm.value : ''; const vJ2 = vJt ? vJt.value : '';
                if(vJ1 || vJ2) {{
                    parrafo += "1.- Jornal de trabajo: ";
                    if(vJ1) parrafo += `Mañana: ${{vJ1}}`;
                    if(vJ1 && vJ2) parrafo += ", ";
                    if(vJ2) parrafo += `Tarde: ${{vJ2}}`;
                    parrafo += ". ";
                }}
                
                // 2. Personal (Solo los > 0)
                let p_data = [
                    {{k: 'operarios', v: parseInt(document.getElementById('v_oper')?.value||0)}}, {{k: 'oficiales', v: parseInt(document.getElementById('v_ofic')?.value||0)}},
                    {{k: 'peones', v: parseInt(document.getElementById('v_peon')?.value||0)}}, {{k: 'mecánicos', v: parseInt(document.getElementById('v_meca')?.value||0)}},
                    {{k: 'controladores', v: parseInt(document.getElementById('v_ctrl')?.value||0)}}, {{k: 'operadores', v: parseInt(document.getElementById('v_ope_maq')?.value||0)}}
                ];
                let p_filtrado = p_data.filter(x => x.v > 0);
                if(p_filtrado.length > 0) {{
                    parrafo += "2.- Personal de obra: ";
                    parrafo += p_filtrado.map(x => `${{x.v.toString().padStart(2,'0')}} ${{x.k}}`).join(', ') + ". ";
                }}

                // 3. Partidas M3
                if (typeof window.m3_lista !== 'undefined' && window.m3_lista.length > 0) {{
                    parrafo += "3.- Partidas ejecutadas: ";
                    parrafo += window.m3_lista.map(p => p.metrado ? `${{p.item}} ${{p.descripcion}} = ${{p.metrado}} ${{p.unidad}}` : `${{p.item}} ${{p.descripcion}}`).join('; ') + ". ";
                }}

                // Textos Libres 4, 5, 6, 7, 8, 9, 10
                const cRestantes = [ 
                    {{id: 'v_mayor_m', t: '4.- Partidas de mayor metrado'}}, {{id: 'v_sub_p', t: '5.- Sub partidas ejecutadas'}},
                    {{id: 'v_activ', t: '6.- Actividades ejecutadas'}}, {{id: 'v_almacen', t: '7.- Movimiento de almacén'}}, 
                    {{id: 'v_maquina', t: '8.- Maquinarias y equipos'}}, {{id: 'v_herram', t: '9.- Herramientas manuales'}}, 
                    {{id: 'v_ocurrencia', t: '10.- Ocurrencias y otros'}} 
                ];
                cRestantes.forEach(c => {{ 
                    const el = document.getElementById(c.id); 
                    if(el && el.value) {{ parrafo += `${{c.t}}: ${{el.value.replace(/\\n/g, ' ')}} `; }}
                }});

                const outContainer = document.getElementById('out_general');
                
                // Procesar Paginación Exacta
                const [pagina1, pagina2] = paginateText(parrafo, 'out_general', 560);
                
                if (pagina2 === "") {{
                    // Si cabe en una hoja
                    outContainer.innerHTML = cabecera + pagina1;
                }} else {{
                    // Si sobrepasa, hacemos la página 1 con "Van" pegado al final del texto y creamos la hoja 2
                    let htmlFinal = cabecera + pagina1 + ' <span class="p-van-line d-inline" style="padding-left:15px;">... Van</span>';
                    htmlFinal += `<div class="p-break-page"></div>`;
                    htmlFinal += `<div style="display:flex; justify-content:space-between; width:100%; margin-bottom:10px; font-family:'Caveat', cursive; color:var(--celeste-obra); font-weight:bold; font-size:22px;">
                        <div style="padding-left:10px;">... VIENE DEL ASIENTO No ${{as_str}} DEL RESIDENTE DE OBRA</div>
                        <div style="padding-right:10px;">${{g_fechaAsiento}}</div>
                    </div>`;
                    htmlFinal += pagina2;
                    outContainer.innerHTML = htmlFinal;
                }}
            }}
        </script>
    </body>
    </html>
    """
    return render_template_string(html_completo, menu_superior=menu_superior, fecha_hoy_iso=fecha_hoy_iso, numero_hoja=numero_hoja)
