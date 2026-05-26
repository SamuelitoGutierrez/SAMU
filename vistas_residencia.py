# =========================================================
# vistas_residencia.py
# Arquitectura Chasis: Ensamblador de Submódulos del Cuaderno
# =========================================================

from flask import Blueprint, render_template_string, session, redirect, url_for
from navbar import obtener_navbar
from datetime import datetime

residencia_bp = Blueprint('residencia', __name__)

# IMPORTACIÓN ESTRATÉGICA DE SUBMÓDULOS (Evita duplicados)
try:
    from mod_01_jornal import JORNAL_HTML
except ImportError:
    JORNAL_HTML = ""

try:
    from mod_02_personal import PERSONAL_HTML
except ImportError:
    PERSONAL_HTML = ""


@residencia_bp.route('/residencia')
def redaccion_asiento_residente():
    if 'usuario_id' not in session:
        return redirect(url_for('login.mostrar_login'))

    es_admin = session.get('rol') == 'Admin'
    nombre_completo = session.get('nombre', 'Ing. Samuel Gutierrez')
    menu_superior = obtener_navbar(es_admin, nombre_completo)
    
    fecha_hoy_iso = datetime.now().strftime('%Y-%m-%d')
    numero_hoja = "0001"

    # Estilos Base del Chasis
    css_estilos = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Caveat:wght@600;700&display=swap');
        :root { --apple-text: #1d1d1f; --celeste-obra: #0263a0; --nav-height: 52px; }
        body { font-family: 'Inter', sans-serif; color: var(--apple-text); overflow-x: hidden; padding-bottom: 90px; margin: 0; background: linear-gradient(135deg, rgba(255,255,255,1) 0%, rgba(2,99,160,0.08) 40%, rgba(135,206,235,0.12) 70%, rgba(249,168,212,0.12) 100%); background-attachment: fixed; }
        
        /* Animaciones Float */
        @keyframes floatInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes floatOutDown { from { opacity: 1; transform: translateY(0); } to { opacity: 0; transform: translateY(30px); } }
        
        .stepper-container { position: fixed; top: var(--nav-height); left: 0; width: 100%; background: rgba(255,255,255,0.85); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(0,0,0,0.08); z-index: 900; padding: 12px 20px; overflow-x: auto; white-space: nowrap; display: flex; gap: 12px; scroll-behavior: smooth; -ms-overflow-style: none; scrollbar-width: none; opacity: 0; pointer-events: none; transition: opacity 0.5s; }
        .stepper-container::-webkit-scrollbar { display: none; }
        .step-btn { border: 1px solid #cbd5e1; border-radius: 30px; padding: 10px 20px; font-size: 12px; font-weight: 600; color: #475569; background: rgba(255,255,255,0.9); cursor: pointer; transition: all 0.3s; }
        .step-btn.active { background: #ffffff !important; color: #000000 !important; font-weight: 800 !important; transform: scale(1.08); box-shadow: 0 8px 20px rgba(0,0,0,0.08); border-color: #000000 !important; }
        .step-btn.omitted { background: #64748b !important; color: white !important; border-color: #475569 !important; }
        #globalTooltip { position: fixed; background: #ffffff; color: #1e293b; padding: 8px 16px; border-radius: 10px; font-size: 12px; font-weight: 700; white-space: nowrap; border: 1px solid #e2e8f0; box-shadow: 0 10px 25px rgba(0,0,0,0.15); pointer-events: none; z-index: 999999; opacity: 0; transition: opacity 0.15s ease; }

        .split-layout { display: flex; gap: 40px; max-width: 1500px; margin: 140px auto 0 auto; padding: 0 20px; align-items: flex-start; filter: blur(5px); pointer-events: none; transition: filter 0.5s; }
        .split-layout.unlocked { filter: blur(0); pointer-events: all; }
        .form-column { flex: 1; max-width: 600px; }
        .preview-column { flex: 1; position: sticky; top: 140px; height: calc(100vh - 240px); overflow-y: auto; }
        
        .step-view { display: none; opacity: 0; background: rgba(255,255,255,0.85); backdrop-filter: blur(25px); padding: 30px; border-radius: 20px; box-shadow: 0 4px 25px rgba(0,0,0,0.03); border: 1px solid rgba(255,255,255,1);}
        .step-view.active { display: block; animation: floatInUp 0.35s cubic-bezier(0.4, 0, 0.2, 1) forwards; }
        .step-view.exit { display: block; animation: floatOutDown 0.3s cubic-bezier(0.4, 0, 0.2, 1) forwards; }
        
        .step-title { font-size: 22px; font-weight: 800; margin-bottom: 25px; color: #0f172a; letter-spacing: -0.5px;}
        .form-label { font-size: 12px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px;}
        .form-control, .form-select { border-radius: 12px; border: 1px solid #cbd5e1; padding: 12px 14px; font-size: 14px; background: rgba(255,255,255,0.9); font-weight: 500;}

        /* Estilos Tarjetas */
        .time-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 15px; display: flex; align-items: center; gap: 15px; transition: all 0.3s; cursor: pointer;}
        .time-card.active { border-color: var(--celeste-obra); background: #f0f9ff; }
        .clock-icon { font-size: 28px; color: #94a3b8; transition: color 0.3s; }
        .time-card.active .clock-icon { color: var(--celeste-obra); }

        .elegant-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 16px 12px; text-align: center; transition: all 0.3s; display: flex; flex-direction: column; align-items: center; justify-content: center;}
        .elegant-card:hover { border-color: var(--celeste-obra); transform: translateY(-2px); }
        .elegant-card.active { border-color: var(--celeste-obra); background: rgba(2, 99, 160, 0.03); box-shadow: 0 10px 20px rgba(2,99,160,0.05); }
        .p-icon { font-size: 26px; color: #94a3b8; transition: all 0.3s; margin-bottom: 4px; }
        .elegant-card.active .p-icon { color: var(--celeste-obra); transform: scale(1.1); }
        .elegant-card input { border: none; background: transparent; text-align: center; font-weight: 800; font-size: 20px; width: 100%; color: #000; padding: 0;}
        .elegant-card input:focus { outline: none; }

        /* Papel del Cuaderno */
        .papel-fisico { background: #fdfdfa; width: 100%; min-height: 980px; padding: 45px 50px; box-shadow: 0 15px 40px rgba(0,0,0,0.08); border: 1px solid #e2e8f0; font-family: Arial, sans-serif; color: #000; position: relative;}
        .p-header-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 25px; } 
        .p-title-box { text-align: center; flex: 1; margin-left: 60px;}
        .p-title-box h1 { font-size: 28px; font-weight: bold; text-decoration: underline; letter-spacing: 1.5px; margin: 0; color: #000;}
        .p-num { font-size: 24px; font-weight: bold; color: #000;}
        .p-meta { margin-bottom: 12px; padding-bottom: 14px; border-bottom: 3px solid #000; }
        .p-row { display: flex; align-items: flex-end; margin-bottom: 6px; }
        .p-label { font-size: 14px; font-weight: bold; margin-right: 8px; color: #000; white-space: nowrap; }
        .p-line { flex: 1; border-bottom: 1px solid #000; position: relative; height: 20px; }
        .lapicero-meta { position: absolute; bottom: -1px; left: 10px; font-family: 'Caveat', cursive; color: var(--celeste-obra); font-size: 19px; font-weight: 700; white-space: nowrap; }
        
        .p-body-lines { background-image: repeating-linear-gradient(transparent, transparent 23px, #cbd5e1 24px); line-height: 24px; min-height: 650px; padding-top: 5px; position: relative; margin-top: 15px;}
        .lapicero { font-family: 'Caveat', cursive; color: var(--celeste-obra); font-size: 16px; line-height: 24px; padding-left: 2px; font-weight: 700; }
        .p-van-line { text-align: right; font-family: 'Caveat', cursive; color: var(--celeste-obra); font-size: 18px; font-weight: 700; display: block; width: 100%; margin-top: 12px; padding-right: 10px;}
        .p-break-page { border-top: 2px dashed #94a3b8; margin: 35px 0 20px 0; padding-top: 15px; position: relative; }
        .p-break-page::before { content: 'SIGUIENTE FOLIO (PÁGINA 2)'; position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background: #fdfdfa; padding: 0 15px; font-size: 10px; color: #94a3b8; font-weight: bold; letter-spacing: 1px;}
        
        .p-footer { display: flex; justify-content: space-between; margin-top: 50px; font-size: 12px; font-weight: bold; color: #000;}
        .p-sig { border-top: 1px solid #000; width: 28%; text-align: center; padding-top: 5px; }
        .bottom-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(255,255,255,0.95); backdrop-filter: blur(15px); border-top: 1px solid rgba(0,0,0,0.08); padding: 15px 30px; z-index: 900; display: flex; justify-content: space-between; align-items: center; opacity: 0; pointer-events: none; transition: opacity 0.5s;}
        .bottom-bar.unlocked { opacity: 1; pointer-events: all; }
    </style>
    """

    # Ensamblamos la estructura inyectando las variables importadas
    html_completo = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>SAMU — Sistema de Residencia</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        {css_estilos}
    </head>
    <body>
        {{{{ menu_superior | safe }}}}

        <div class="modal fade" id="modalConfigInicial" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content" style="border-radius: 24px; border: none; box-shadow: 0 20px 50px rgba(0,0,0,0.2);">
                    <div class="modal-header border-0 pb-0 justify-content-center mt-3">
                        <h4 class="modal-title fw-bold text-primary"><i class="bi bi-journal-plus"></i> Apertura de Asiento</h4>
                    </div>
                    <div class="modal-body px-5 pb-4">
                        <p class="text-muted small text-center mb-4">Ingrese los datos para aperturar el folio de hoy en el cuaderno.</p>
                        <div class="mb-3">
                            <label class="form-label fw-bold">N° de Asiento</label>
                            <input type="number" id="initNumAsiento" class="form-control form-control-lg bg-light" placeholder="Ej: 88">
                        </div>
                        <div class="mb-4">
                            <label class="form-label fw-bold">Fecha del Asiento</label>
                            <input type="date" id="initFecha" class="form-control form-control-lg bg-light" value="{fecha_hoy_iso}">
                        </div>
                        <button type="button" class="btn btn-primary btn-lg w-100 rounded-pill fw-bold" onclick="iniciarAsiento()">Iniciar Redacción <i class="bi bi-arrow-right ms-2"></i></button>
                    </div>
                </div>
            </div>
        </div>

        <div class="stepper-container" id="stepperBar">
            <button class="step-btn active" id="btnStep1" onclick="jumpToStep(1)" data-tooltip="Faltan datos">1. Jornal</button>
            <button class="step-btn" id="btnStep2" onclick="jumpToStep(2)" data-tooltip="Faltan datos">2. Personal</button>
            <button class="step-btn" id="btnStep3" onclick="jumpToStep(3)" data-tooltip="Faltan datos">3. Partidas</button>
            <button class="step-btn" id="btnStep4" onclick="jumpToStep(4)" data-tooltip="Bloque Pendiente">4. Mayor Metrado</button>
            <button class="step-btn" id="btnStep5" onclick="jumpToStep(5)" data-tooltip="Bloque Pendiente">5. Sub Partidas</button>
            <button class="step-btn" id="btnStep6" onclick="jumpToStep(6)" data-tooltip="Bloque Pendiente">6. Actividades</button>
            <button class="step-btn" id="btnStep7" onclick="jumpToStep(7)" data-tooltip="Bloque Pendiente">7. Almacén</button>
            <button class="step-btn" id="btnStep8" onclick="jumpToStep(8)" data-tooltip="Bloque Pendiente">8. Maquinaria</button>
            <button class="step-btn" id="btnStep9" onclick="jumpToStep(9)" data-tooltip="Bloque Pendiente">9. Herramientas</button>
            <button class="step-btn" id="btnStep10" onclick="jumpToStep(10)" data-tooltip="Bloque Pendiente">10. Ocurrencias</button>
            <button class="step-btn border-dark text-dark fw-bold" id="btnStep11" onclick="jumpToStep(11)" data-tooltip="Cierre Folio"><i class="bi bi-shield-lock-fill"></i> Firma Final</button>
        </div>
        <div id="globalTooltip"></div>

        <div class="split-layout" id="mainLayout">
            <div class="form-column">
                <div class="d-flex justify-content-between mb-3 px-2">
                    <h6 class="text-primary fw-bold mb-0">Asiento N° <span id="lbl_num_asiento">--</span></h6>
                    <span class="text-muted small fw-bold" id="lbl_fecha_asiento">--</span>
                </div>

                <form id="formResidencia" onsubmit="event.preventDefault();" oninput="sincronizarDatos()">
                    {JORNAL_HTML}
                    {PERSONAL_HTML}

                    <div class="step-view" id="step3">
                        <div class="step-title">3.- Partidas Ejecutadas</div>
                        <div class="alert alert-light border border-dashed text-center py-4 text-muted"><i class="bi bi-code-square fs-3 d-block mb-2"></i> El motor de partidas masivas (mod_03_partidas.py) está listo para configurarse de forma independiente en el siguiente paso.</div>
                    </div>
                    <div class="step-view" id="step4"><div class="step-title">4.- Mayor Metrado</div><textarea class="form-control" id="v_mayor_m" rows="5" placeholder="Módulo transitorio..."></textarea></div>
                    <div class="step-view" id="step5"><div class="step-title">5.- Sub Partidas</div><textarea class="form-control" id="v_sub_p" rows="5" placeholder="Módulo transitorio..."></textarea></div>
                    <div class="step-view" id="step6"><div class="step-title">6.- Actividades</div><textarea class="form-control" id="v_activ" rows="5" placeholder="Módulo transitorio..."></textarea></div>
                    <div class="step-view" id="step7"><div class="step-title">7.- Almacén</div><textarea class="form-control" id="v_almacen" rows="5" placeholder="Módulo transitorio..."></textarea></div>
                    <div class="step-view" id="step8"><div class="step-title">8.- Maquinaria</div><textarea class="form-control" id="v_maquina" rows="5" placeholder="Módulo transitorio..."></textarea></div>
                    <div class="step-view" id="step9"><div class="step-title">9.- Herramientas</div><textarea class="form-control" id="v_herram" rows="4" placeholder="Módulo transitorio..."></textarea></div>
                    <div class="step-view" id="step10"><div class="step-title text-danger">10.- Ocurrencias</div><textarea class="form-control border-danger" id="v_ocurrencia" rows="6" placeholder="Módulo transitorio..."></textarea></div>

                    <div class="step-view" id="step11">
                        <div class="step-title text-success text-center mb-4"><i class="bi bi-shield-check"></i> Sellar Folio</div>
                        <p class="text-center text-muted small mb-5">Verifique la hoja de cuaderno. Al deslizar el candado, los datos quedarán inmutables.</p>
                    </div>
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

                    <div class="p-body-lines">
                        <div class="lapicero-muted" style="margin-bottom: 0px;">... viene del asiento nº 0087 del residente de obra </div>
                        <div class="lapicero" id="out_general"></div>
                    </div>

                    <div class="p-footer">
                        <div class="p-sig">ING. INSPECTOR</div><div class="p-sig">ING. RESIDENTE</div><div class="p-sig">ING. SUPERVISOR</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="bottom-bar shadow-lg" id="bottomBarUI">
            <div>
                <button type="button" id="btnAtras" class="btn btn-light border fw-bold rounded-pill px-4 text-dark shadow-sm d-none" onclick="anteriorPaso()"><i class="bi bi-arrow-left"></i> Anterior</button>
            </div>
            <div class="d-flex gap-2 align-items-center">
                <div id="indicadorGuardado" class="small text-muted fw-semibold d-none d-sm-block me-2"><i class="bi bi-cloud-arrow-up"></i> Autoguardado</div>
                <button type="button" class="btn btn-outline-secondary fw-bold rounded-pill px-4 shadow-sm" onclick="omitirPaso()">Omitir</button>
                <button type="button" class="btn btn-dark fw-bold rounded-pill px-4 shadow-sm" onclick="siguientePaso()">Guardar y Continuar <i class="bi bi-arrow-right"></i></button>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        
        <script>
            let g_numAsiento = ""; let g_fechaAsiento = "";
            let currentStep = 1; const totalSteps = 11; let isAnimating = false;
            let t_m = true; let t_t = true;

            document.addEventListener("DOMContentLoaded", function() {{
                const myModal = new bootstrap.Modal(document.getElementById('modalConfigInicial'));
                myModal.show();
            }});

            function formatearFecha(fechaStr) {{
                const dias = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO", "DOMINGO"];
                const [y, m, d] = fechaStr.split('-');
                const dateObj = new Date(y, m-1, d);
                let dayIndex = dateObj.getDay() - 1; if(dayIndex === -1) dayIndex = 6;
                return `${{dias[dayIndex]}}, ${{d}}/${{m}}/${{y}}`;
            }}

            function iniciarAsiento() {{
                g_numAsiento = document.getElementById('initNumAsiento').value;
                let rawDate = document.getElementById('initFecha').value;
                if(!g_numAsiento || !rawDate) {{ alert("Complete los campos para iniciar."); return; }}
                
                g_fechaAsiento = formatearFecha(rawDate);
                document.getElementById('lbl_num_asiento').innerText = g_numAsiento.padStart(4, '0');
                document.getElementById('lbl_fecha_asiento').innerText = g_fechaAsiento;
                document.getElementById('lbl_hoja_fecha').innerText = g_fechaAsiento;
                
                bootstrap.Modal.getInstance(document.getElementById('modalConfigInicial')).hide();
                document.getElementById('mainLayout').classList.add('unlocked');
                document.getElementById('stepperBar').style.opacity = '1';
                document.getElementById('stepperBar').style.pointerEvents = 'all';
                document.getElementById('bottomBarUI').classList.add('unlocked');
                sincronizarDatos();
            }}

            function jumpToStep(stepIndex) {{
                if (isAnimating || currentStep === stepIndex) return;
                isAnimating = true;

                const currentView = document.getElementById(`step${{currentStep}}`);
                currentView.classList.remove('active'); currentView.classList.add('exit');
                document.getElementById(`btnStep${{currentStep}}`).classList.remove('active');
                
                setTimeout(() => {{
                    currentView.classList.remove('exit');
                    currentStep = stepIndex;
                    const nextView = document.getElementById(`step${{currentStep}}`);
                    nextView.classList.add('active');
                    document.getElementById(`btnStep${{currentStep}}`).classList.add('active');

                    const btnAtras = document.getElementById('btnAtras');
                    if (currentStep > 1) btnAtras.classList.remove('d-none'); else btnAtras.classList.add('d-none');
                    isAnimating = false;
                    sincronizarDatos();
                }}, 300); 
            }}

            function siguientePaso() {{ if(currentStep < totalSteps) jumpToStep(currentStep + 1); }}
            function anteriorPaso() {{ if(currentStep > 1) jumpToStep(currentStep - 1); }}
            function omitirPaso() {{ siguientePaso(); }}

            // Lógica de Módulo 1 (Jornal)
            function toggleTurno(turno) {{
                if(turno === 'm') {{
                    t_m = !t_m; document.getElementById('card_m').classList.toggle('active', t_m);
                    document.getElementById('v_jornal_m').value = t_m ? "07:00 - 12:00" : "";
                    document.getElementById('lbl_jornal_m').style.opacity = t_m ? "1" : "0.3";
                }} else {{
                    t_t = !t_t; document.getElementById('card_t').classList.toggle('active', t_t);
                    document.getElementById('v_jornal_t').value = t_t ? "13:00 - 17:00" : "";
                    document.getElementById('lbl_jornal_t').style.opacity = t_t ? "1" : "0.3";
                }}
                sincronizarDatos();
            }}

            // Lógica de Módulo 2 (Personal)
            function evaluarTarjeta(id) {{
                const val = document.getElementById('v_' + id).value;
                const card = document.getElementById('c_' + id);
                if(val > 0) card.classList.add('active'); else card.classList.remove('active');
                sincronizarDatos();
            }}

            // ==========================================================
            // MOTOR DE RENDERIZADO GENERAL (ESCRIBE EN TIEMPO REAL)
            // ==========================================================
            function sincronizarDatos() {{
                if(!g_numAsiento) return;
                let as_str = g_numAsiento.padStart(4, '0');
                
                // Cabecera Centrada y Fecha a la Derecha en una misma línea
                let textoPapel = `
                <div style="display:flex; justify-content:space-between; align-items:center; width:100%; margin-bottom: 5px;">
                    <div style="font-weight:bold; font-size:17px; padding-left:40px;">ASIENTO No ${{as_str}} DEL RESIDENTE DE OBRA</div>
                    <div style="font-weight:bold; font-size:17px; padding-right:10px;">${{g_fechaAsiento}}</div>
                </div>`;

                // Renderizado Paso 1
                const vJ1 = document.getElementById('v_jornal_m').value; const vJ2 = document.getElementById('v_jornal_t').value;
                if(vJ1 || vJ2) {{
                    textoPapel += `1.- Jornal de trabajo:<br>`;
                    if(vJ1) textoPapel += `Mañana: ${{vJ1}} `;
                    if(vJ2) textoPapel += `Tarde: ${{vJ2}}`;
                    textoPapel += `<br>`;
                }}
                
                // Renderizado Paso 2
                const vOper = (document.getElementById('v_oper').value || '0').padStart(2, '0');
                const vOfic = (document.getElementById('v_ofic').value || '0').padStart(2, '0');
                const vPeon = (document.getElementById('v_peon').value || '0').padStart(2, '0');
                const vMeca = (document.getElementById('v_meca').value || '0').padStart(2, '0');
                const vCtrl = (document.getElementById('v_ctrl').value || '0').padStart(2, '0');
                const vOpe = (document.getElementById('v_ope_maq').value || '0').padStart(2, '0');

                if (vOper !== '00' || vOfic !== '00' || vPeon !== '00' || vMeca !== '00' || vCtrl !== '00' || vOpe !== '00') {{
                    textoPapel += `2.- Personal de obra:<br>`;
                    textoPapel += `${{vOper}} operarios &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${{vOfic}} oficiales &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${{vPeon}} peones &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${{vMeca}} mecánicos<br>`;
                    textoPapel += `${{vCtrl}} controladores de maquinaria &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${{vOpe}} operadores de maquinaria<br>`;
                }}

                // Captura transitoria para los demás campos
                const campos = [
                    {{id: 'v_mayor_m', tit: '4.- Partidas de mayor metrado'}}, {{id: 'v_sub_p', tit: '5.- Sub partidas ejecutadas'}},
                    {{id: 'v_activ', tit: '6.- Actividades ejecutadas'}}, {{id: 'v_almacen', tit: '7.- Movimiento de almacén'}},
                    {{id: 'v_maquina', tit: '8.- Maquinarias y equipos'}}, {{id: 'v_herram', tit: '9.- Herramientas manuales'}},
                    {{id: 'v_ocurrencia', tit: '10.- Ocurrencias y otros'}}
                ];
                campos.forEach(c => {{
                    const el = document.getElementById(c.id);
                    if(el && el.value) textoPapel += `${{c.tit}}:<br>${{el.value.replace(/\\n/g, '<br>')}}<br>`;
                }});

                const outContainer = document.getElementById('out_general');
                outContainer.innerHTML = textoPapel;
                
                // LÓGICA DE VAN / VIENE (Corte de Página Automático)
                if (outContainer.offsetHeight > 560) {{
                    let contenidoPrevio = outContainer.innerHTML;
                    outContainer.innerHTML = `
                        <div>${{contenidoPrevio}}</div>
                        <span class="p-van-line">... Van</span>
                        <div class="p-num text-end mb-2" style="font-size:16px; font-weight:bold; padding-right:10px;">Nº 0002</div>
                        <div class="p-break-page"></div>
                        <div style="display:flex; width:100%; margin-bottom:10px; font-family:'Caveat', cursive; color:var(--celeste-obra); font-weight:bold; font-size:17px;">
                            <div style="flex:1;"></div>
                            <div style="flex:2; text-align:center;">... VIENE DEL ASIENTO No ${{as_str}} DEL RESIDENTE DE OBRA</div>
                            <div style="flex:1; text-align:right;">${{g_fechaAsiento}}</div>
                        </div>
                    `;
                }}
            }}
        </script>
    </body>
    </html>
    """
    
    return render_template_string(html_completo, menu_superior=menu_superior)
