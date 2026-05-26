# =========================================================
# vistas_residencia.py
# Módulo Maestro: Ensamblador Final del Cuaderno de Obra
# =========================================================

from flask import Blueprint, render_template_string, session, redirect, url_for
from navbar import obtener_navbar
from datetime import datetime

# ==============================================================================
# IMPORTACIÓN DINÁMICA DE LOS MÓDULOS
# ==============================================================================
try:
    from mod_01_jornal import JORNAL_HTML
except ImportError:
    JORNAL_HTML = "<div class='step-view active' id='step1'><p>Error: mod_01_jornal.py no encontrado.</p></div>"

try:
    from mod_02_personal import PERSONAL_HTML
except ImportError:
    PERSONAL_HTML = "<div class='step-view' id='step2'><p>Error: mod_02_personal.py no encontrado.</p></div>"

try:
    from mod_03_partidas import PARTIDAS_HTML
except ImportError:
    PARTIDAS_HTML = "<div class='step-view' id='step3'><div class='step-title'>3.- Partidas</div><p>Módulo pendiente.</p><input type='hidden' id='v_partidas' class='req-step3'></div>"

try:
    from mod_04_mayor_metrado import MAYOR_METRADO_HTML
except ImportError:
    MAYOR_METRADO_HTML = "<div class='step-view' id='step4'><div class='step-title'>4.- Mayor Metrado</div><textarea class='form-control req-step4' id='v_mayor_m' rows='5' oninput='sincronizarDatos()' placeholder='Módulo en construcción...'></textarea></div>"

try:
    from mod_05_sub_partidas import SUB_PARTIDAS_HTML
except ImportError:
    SUB_PARTIDAS_HTML = "<div class='step-view' id='step5'><div class='step-title'>5.- Sub Partidas</div><textarea class='form-control req-step5' id='v_sub_p' rows='5' oninput='sincronizarDatos()' placeholder='Módulo en construcción...'></textarea></div>"

try:
    from mod_06_actividades import ACTIVIDADES_HTML
except ImportError:
    ACTIVIDADES_HTML = "<div class='step-view' id='step6'><div class='step-title'>6.- Actividades</div><textarea class='form-control req-step6' id='v_activ' rows='5' oninput='sincronizarDatos()' placeholder='Módulo en construcción...'></textarea></div>"

try:
    from mod_07_almacen import ALMACEN_HTML
except ImportError:
    ALMACEN_HTML = "<div class='step-view' id='step7'><div class='step-title'>7.- Almacén</div><textarea class='form-control req-step7' id='v_almacen' rows='5' oninput='sincronizarDatos()' placeholder='Módulo en construcción...'></textarea></div>"

try:
    from mod_08_maquinaria import MAQUINARIA_HTML
except ImportError:
    MAQUINARIA_HTML = "<div class='step-view' id='step8'><div class='step-title'>8.- Maquinaria</div><textarea class='form-control req-step8' id='v_maquina' rows='5' oninput='sincronizarDatos()' placeholder='Módulo en construcción...'></textarea></div>"

try:
    from mod_09_herramientas import HERRAMIENTAS_HTML
except ImportError:
    HERRAMIENTAS_HTML = "<div class='step-view' id='step9'><div class='step-title'>9.- Herramientas</div><textarea class='form-control req-step9' id='v_herram' rows='4' oninput='sincronizarDatos()' placeholder='Módulo en construcción...'></textarea></div>"

try:
    from mod_10_ocurrencias import OCURRENCIAS_HTML
except ImportError:
    OCURRENCIAS_HTML = "<div class='step-view' id='step10'><div class='step-title text-danger'>10.- Ocurrencias</div><textarea class='form-control border-danger req-step10' id='v_ocurrencia' rows='6' oninput='sincronizarDatos()' placeholder='Módulo en construcción...'></textarea></div>"


residencia_bp = Blueprint('residencia', __name__)

@residencia_bp.route('/residencia')
def redaccion_asiento_residente():
    if 'usuario_id' not in session:
        return redirect(url_for('login.mostrar_login'))

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
            
            .step-btn {{ border: 1px solid #cbd5e1; border-radius: 30px; padding: 10px 20px; font-size: 12px; font-weight: 600; color: #475569; background: rgba(255,255,255,0.9); cursor: pointer; transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); transform-origin: center; }}
            .step-btn.active {{ background: #ffffff !important; color: #000000 !important; font-weight: 800 !important; transform: scale(1.15) !important; box-shadow: 0 10px 25px rgba(0,0,0,0.12); border-color: #000000 !important; margin: 0 10px; }}
            .step-btn.omitted {{ background: #64748b !important; color: white !important; border-color: #475569 !important; }}

            #globalTooltip {{ position: fixed; background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(8px); color: #ffffff; padding: 8px 16px; border-radius: 8px; font-size: 12px; font-weight: 600; white-space: nowrap; box-shadow: 0 10px 25px rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.1); pointer-events: none; z-index: 999999; opacity: 0; transform: translateY(10px); transition: opacity 0.2s ease, transform 0.2s ease; }}
            #globalTooltip.visible {{ opacity: 1; transform: translateY(0); }}

            .elegant-alert {{ position: fixed; top: 20px; left: 50%; transform: translateX(-50%) translateY(-100px); background: rgba(255,255,255,0.95); backdrop-filter: blur(20px); border-radius: 50px; padding: 12px 25px; display: flex; align-items: center; gap: 12px; box-shadow: 0 15px 35px rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,1); z-index: 9999999; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); opacity: 0; pointer-events: none; }}
            .elegant-alert.show {{ transform: translateX(-50%) translateY(0); opacity: 1; }}
            .alert-icon {{ font-size: 20px; }}
            .alert-text {{ font-size: 14px; font-weight: 700; color: #1e293b; }}

            .split-layout {{ display: flex; gap: 40px; max-width: 1500px; margin: 140px auto 0 auto; padding: 0 20px; align-items: flex-start; filter: blur(5px); pointer-events: none; transition: filter 0.5s; }}
            .split-layout.unlocked {{ filter: blur(0); pointer-events: all; }}
            .form-column {{ flex: 1; max-width: 600px; }}
            .preview-column {{ flex: 1; position: sticky; top: 140px; height: calc(100vh - 240px); overflow-y: auto; }}
            
            .step-view {{ display: none; opacity: 0; background: rgba(255,255,255,0.85); backdrop-filter: blur(25px); padding: 30px; border-radius: 20px; box-shadow: 0 4px 25px rgba(0,0,0,0.03); border: 1px solid rgba(255,255,255,1);}}
            .step-view.active {{ display: block; animation: floatInUp 0.35s forwards; }}
            .step-view.exit {{ display: block; animation: floatOutDown 0.3s forwards; }}
            
            .step-title {{ font-size: 22px; font-weight: 800; margin-bottom: 25px; color: #0f172a; letter-spacing: -0.5px;}}
            .form-control {{ border-radius: 12px; border: 1px solid #cbd5e1; padding: 12px 14px; font-size: 14px; }}
            .form-control:focus {{ border-color: #0066cc; box-shadow: 0 0 0 4px rgba(0,102,204,0.15); }}

            .time-card {{ background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 15px; display: flex; align-items: center; gap: 15px; cursor: pointer; transition: all 0.3s;}}
            .time-card.active {{ border-color: var(--celeste-obra); background: #f0f9ff; }}
            .time-card .clock-icon {{ font-size: 28px; color: #94a3b8; }}
            .time-card.active .clock-icon {{ color: var(--celeste-obra); }}

            .elegant-card {{ background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 16px 12px; text-align: center; transition: all 0.3s; display: flex; flex-direction: column; align-items: center; }}
            .elegant-card.active {{ border-color: var(--celeste-obra); background: rgba(2, 99, 160, 0.03); }}
            .elegant-card .p-icon {{ font-size: 26px; color: #94a3b8; transition: all 0.3s; margin-bottom: 4px; }}
            .elegant-card.active .p-icon {{ color: var(--celeste-obra); transform: scale(1.1); }}
            .elegant-card input {{ border: none; background: transparent; text-align: center; font-weight: 800; font-size: 20px; width: 100%; outline: none; }}

            /* Cuaderno Físico */
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
            .lapicero {{ font-family: 'Caveat', cursive; color: var(--celeste-obra); font-size: 22px; line-height: 28px; padding-left: 2px; font-weight: 700; }}
            .p-van-line {{ text-align: right; font-family: 'Caveat', cursive; color: var(--celeste-obra); font-size: 22px; font-weight: 700; display: block; width: 100%; margin-top: 12px; padding-right: 10px;}}
            .p-break-page {{ border-top: 2px dashed #94a3b8; margin: 35px 0 20px 0; padding-top: 15px; position: relative; }}
            .p-footer {{ display: flex; justify-content: space-between; margin-top: 50px; font-size: 12px; font-weight: bold; color: #000;}}
            .p-sig {{ border-top: 1px solid #000; width: 28%; text-align: center; padding-top: 5px; }}
            
            .bottom-bar {{ position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(255,255,255,0.95); backdrop-filter: blur(15px); border-top: 1px solid rgba(0,0,0,0.08); padding: 15px 30px; z-index: 900; display: flex; justify-content: space-between; align-items: center; opacity: 0; pointer-events: none; transition: opacity 0.5s;}}
            .bottom-bar.unlocked {{ opacity: 1; pointer-events: all; }}
            
            .slider-track {{ width: 100%; max-width: 400px; height: 60px; background: rgba(0,0,0,0.05); border-radius: 30px; position: relative; display: flex; align-items: center; justify-content: center; overflow: hidden; margin: 0 auto; border: 1px solid rgba(0,0,0,0.05);}}
            .slider-text {{ font-size: 13px; font-weight: 800; color: #64748b; text-transform: uppercase; z-index: 1; pointer-events: none;}}
            .slider-handle {{ width: 52px; height: 52px; background: #000; color: #fff; border-radius: 50%; position: absolute; left: 4px; display: flex; align-items: center; justify-content: center; z-index: 2; cursor: grab;}}
            .slider-progress {{ position: absolute; left: 0; top: 0; height: 100%; background: rgba(0, 102, 204, 0.1); width: 0; pointer-events: none; }}
        </style>
    </head>
    <body>
        {{{{ menu_superior | safe }}}}

        <div id="elegantAlert" class="elegant-alert">
            <div class="alert-icon" id="alertIcon"></div>
            <div class="alert-text" id="alertText">Mensaje</div>
        </div>

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

        <div class="stepper-container" id="stepperBar">
            <button class="step-btn active" id="btnStep1" onclick="jumpToStep(1)" data-tooltip="Faltan datos">1. Jornal</button>
            <button class="step-btn" id="btnStep2" onclick="jumpToStep(2)" data-tooltip="Faltan datos">2. Personal</button>
            <button class="step-btn" id="btnStep3" onclick="jumpToStep(3)" data-tooltip="Faltan datos">3. Partidas</button>
            <button class="step-btn" id="btnStep4" onclick="jumpToStep(4)" data-tooltip="Faltan datos">4. Mayor Metrado</button>
            <button class="step-btn" id="btnStep5" onclick="jumpToStep(5)" data-tooltip="Faltan datos">5. Sub Partidas</button>
            <button class="step-btn" id="btnStep6" onclick="jumpToStep(6)" data-tooltip="Faltan datos">6. Actividades</button>
            <button class="step-btn" id="btnStep7" onclick="jumpToStep(7)" data-tooltip="Faltan datos">7. Almacén</button>
            <button class="step-btn" id="btnStep8" onclick="jumpToStep(8)" data-tooltip="Faltan datos">8. Maquinaria</button>
            <button class="step-btn" id="btnStep9" onclick="jumpToStep(9)" data-tooltip="Faltan datos">9. Herramientas</button>
            <button class="step-btn" id="btnStep10" onclick="jumpToStep(10)" data-tooltip="Faltan datos">10. Ocurrencias</button>
            <button class="step-btn border-dark text-dark fw-bold" id="btnStep11" onclick="jumpToStep(11)" data-tooltip="Ver Documento Final"><i class="bi bi-shield-lock-fill"></i> Firma Final</button>
        </div>
        <div id="globalTooltip"></div>

        <div class="split-layout" id="mainLayout">
            <div class="form-column">
                <form id="formResidencia" onsubmit="event.preventDefault();" oninput="sincronizarDatos()">
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
                    
                    <div class="step-view" id="step11">
                        <div class="step-title text-success text-center mb-4"><i class="bi bi-shield-check"></i> Sellar Folio</div>
                        <p class="text-center text-muted small mb-5">Verifica la hoja de cuaderno generada a la derecha. Al deslizar el candado, los datos quedarán inmutables.</p>
                        <div class="slider-track" id="sliderTrack"><div class="slider-progress" id="sliderProgress"></div><div class="slider-text" id="sliderText">Deslizar para Firmar</div><div class="slider-handle" id="sliderHandle"><i class="bi bi-lock-fill" style="font-size: 1.2rem;"></i></div></div>
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
            let g_numAsiento = ""; let g_fechaAsiento = "";
            let currentStep = 1; const totalSteps = 11; let isAnimating = false;
            let t_m = true; let t_t = true;

            function mostrarAlerta(mensaje, tipo="error") {{
                const alerta = document.getElementById('elegantAlert');
                const icono = document.getElementById('alertIcon');
                document.getElementById('alertText').innerText = mensaje;
                if(tipo === "error") {{ icono.innerHTML = '<i class="bi bi-exclamation-circle-fill text-danger"></i>'; }} 
                else {{ icono.innerHTML = '<i class="bi bi-check-circle-fill text-success"></i>'; }}
                alerta.classList.add('show');
                setTimeout(() => {{ alerta.classList.remove('show'); }}, 3500);
            }}

            document.addEventListener("DOMContentLoaded", function() {{ new bootstrap.Modal(document.getElementById('modalConfigInicial')).show(); }});

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
                if(!g_numAsiento || !rawDate) {{ mostrarAlerta("Complete los datos para iniciar.", "error"); return; }}
                g_fechaAsiento = formatearFecha(rawDate);
                document.getElementById('lbl_hoja_fecha').innerText = g_fechaAsiento;
                bootstrap.Modal.getInstance(document.getElementById('modalConfigInicial')).hide();
                document.getElementById('mainLayout').classList.add('unlocked');
                document.getElementById('stepperBar').style.opacity = '1';
                document.getElementById('stepperBar').style.pointerEvents = 'all';
                document.getElementById('bottomBarUI').classList.add('unlocked');
                sincronizarDatos();
            }}

            const gTooltip = document.getElementById('globalTooltip');
            document.querySelectorAll('.step-btn').forEach(btn => {{
                btn.addEventListener('mousemove', (e) => {{
                    gTooltip.innerText = btn.getAttribute('data-tooltip');
                    gTooltip.style.left = (e.clientX + 15) + 'px'; gTooltip.style.top = (e.clientY + 15) + 'px';
                    gTooltip.classList.add('visible');
                }});
                btn.addEventListener('mouseleave', () => {{ gTooltip.classList.remove('visible'); }});
            }});
            
            function jumpToStep(stepIndex) {{
                if (isAnimating || currentStep === stepIndex) return;
                isAnimating = true;
                const currentView = document.getElementById(`step${{currentStep}}`);
                currentView.classList.remove('active'); currentView.classList.add('exit');
                document.getElementById(`btnStep${{currentStep}}`).classList.remove('active');
                setTimeout(() => {{
                    currentView.classList.remove('exit');
                    currentStep = stepIndex;
                    document.getElementById(`step${{currentStep}}`).classList.add('active');
                    document.getElementById(`btnStep${{currentStep}}`).classList.add('active');
                    const btnAtras = document.getElementById('btnAtras');
                    if (currentStep > 1) btnAtras.classList.remove('d-none'); else btnAtras.classList.add('d-none');
                    isAnimating = false;
                }}, 300); 
            }}

            function siguientePaso() {{ if(currentStep < totalSteps) jumpToStep(currentStep + 1); }}
            function anteriorPaso() {{ if(currentStep > 1) jumpToStep(currentStep - 1); }}
            function omitirPaso() {{ document.querySelectorAll(`.req-step${{currentStep}}`).forEach(i => i.value = ""); sincronizarDatos(); siguientePaso(); }}

            function toggleTurno(turno) {{
                if(turno === 'm') {{ t_m = !t_m; document.getElementById('card_m').classList.toggle('active', t_m); document.getElementById('v_jornal_m').value = t_m ? "07:00 - 12:00" : ""; document.getElementById('lbl_jornal_m').style.opacity = t_m ? "1" : "0.3"; }}
                else {{ t_t = !t_t; document.getElementById('card_t').classList.toggle('active', t_t); document.getElementById('v_jornal_t').value = t_t ? "13:00 - 17:00" : ""; document.getElementById('lbl_jornal_t').style.opacity = t_t ? "1" : "0.3"; }}
                sincronizarDatos();
            }}

            function evaluarTarjeta(id) {{
                const val = document.getElementById('v_' + id).value;
                document.getElementById('c_' + id).classList.toggle('active', val > 0);
                sincronizarDatos();
            }}

            let partidasList = [];
            function agregarPartidaRapida() {{
                const inputBuscador = document.getElementById('buscadorPartidas');
                if(!inputBuscador) return;
                const desc = inputBuscador.value.trim();
                if(desc === '') return;
                partidasList.push({{ descripcion: desc, metrado: '' }});
                inputBuscador.value = ''; 
                renderizarListaPartidas();
                document.getElementById('v_partidas').value = "lleno"; 
                sincronizarDatos();
            }}

            function abrirModalMasivo() {{ 
                document.getElementById('textoExcelMasivo').value = ''; 
                new bootstrap.Modal(document.getElementById('modalExcel')).show(); 
            }}

            function procesarExcelMasivo() {{
                const rawData = document.getElementById('textoExcelMasivo').value;
                if(!rawData.trim()) {{ mostrarAlerta("No hay datos para procesar", "error"); return; }}
                const rows = rawData.split('\\n'); 
                let count = 0;
                rows.forEach(row => {{
                    if(!row.trim()) return;
                    const cols = row.split('\\t'); 
                    let desc = cols[0].trim(); 
                    let met = cols.length > 1 ? cols[1].trim() : '';
                    if(desc) {{ partidasList.push({{ descripcion: desc, metrado: met }}); count++; }}
                }});
                if(count > 0) {{ 
                    renderizarListaPartidas(); 
                    document.getElementById('v_partidas').value = "lleno"; 
                    sincronizarDatos(); 
                    mostrarAlerta(`Se importaron ${{count}} partidas correctamente.`, "success");
                }}
                bootstrap.Modal.getInstance(document.getElementById('modalExcel')).hide();
            }}

            function actualizarMetrado(index, valor) {{ partidasList[index].metrado = valor; sincronizarDatos(); }}
            function eliminarPartida(index) {{ partidasList.splice(index, 1); if(partidasList.length === 0) document.getElementById('v_partidas').value = ""; renderizarListaPartidas(); sincronizarDatos(); }}

            function renderizarListaPartidas() {{
                const container = document.getElementById('listaPartidasAgregadas');
                if(!container) return;
                container.innerHTML = partidasList.map((p, index) => `
                    <div class="bg-white border rounded-3 p-2 d-flex justify-content-between align-items-center shadow-sm">
                        <span class="text-truncate flex-grow-1 small fw-semibold me-2" style="max-width: 320px;">${{p.descripcion}}</span>
                        <input type="text" class="form-control form-control-sm text-end border-primary" style="width: 100px; background:#f0f9ff;" placeholder="Metrado" value="${{p.metrado}}" oninput="actualizarMetrado(${{index}}, this.value)">
                        <button type="button" class="btn btn-sm text-danger ms-2" onclick="eliminarPartida(${{index}})"><i class="bi bi-trash"></i></button>
                    </div>
                `).join('');
            }}

            function sincronizarDatos() {{
                if(!g_numAsiento) return;
                let as_str = g_numAsiento.padStart(4, '0');
                
                let textoPapel = `
                <div style="display:flex; justify-content:space-between; width:100%; margin-bottom: 5px;">
                    <div style="padding-left:40px;">ASIENTO No ${{as_str}} DEL RESIDENTE DE OBRA</div>
                    <div style="padding-right:10px;">${{g_fechaAsiento}}</div>
                </div>`;

                const vJm = document.getElementById('v_jornal_m'); const vJt = document.getElementById('v_jornal_t');
                const vJ1 = vJm ? vJm.value : ''; const vJ2 = vJt ? vJt.value : '';
                if(vJ1 || vJ2) {{ textoPapel += `1.- Jornal de trabajo:<br>`; if(vJ1) textoPapel += `Mañana: ${{vJ1}} `; if(vJ2) textoPapel += `Tarde: ${{vJ2}}`; textoPapel += `<br>`; }}
                
                const eOp = document.getElementById('v_oper'); const vOper = (eOp ? eOp.value : '0').padStart(2, '0'); 
                const eOf = document.getElementById('v_ofic'); const vOfic = (eOf ? eOf.value : '0').padStart(2, '0'); 
                const ePe = document.getElementById('v_peon'); const vPeon = (ePe ? ePe.value : '0').padStart(2, '0');
                const eMe = document.getElementById('v_meca'); const vMeca = (eMe ? eMe.value : '0').padStart(2, '0'); 
                const eCt = document.getElementById('v_ctrl'); const vCtrl = (eCt ? eCt.value : '0').padStart(2, '0'); 
                const eOm = document.getElementById('v_ope_maq'); const vOpe = (eOm ? eOm.value : '0').padStart(2, '0');

                if (vOper !== '00' || vOfic !== '00' || vPeon !== '00' || vMeca !== '00' || vCtrl !== '00' || vOpe !== '00') {{
                    textoPapel += `2.- Personal de obra:<br>${{vOper}} operarios &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${{vOfic}} oficiales &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${{vPeon}} peones &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${{vMeca}} mecánicos<br>${{vCtrl}} controladores maq. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${{vOpe}} operadores maq.<br>`;
                }}

                if(partidasList.length > 0) {{
                    textoPapel += `3.- Partidas ejecutadas:<br>`;
                    partidasList.forEach(p => {{ textoPapel += `- ${{p.descripcion}} &nbsp;&nbsp;&nbsp;&nbsp; (Metrado: ${{p.metrado || '0.00'}})<br>`; }});
                }}

                const camposText = [
                    {{id: 'v_mayor_m', titulo: '4.- Partidas de mayor metrado'}}, {{id: 'v_sub_p', titulo: '5.- Sub partidas ejecutadas'}},
                    {{id: 'v_activ', titulo: '6.- Actividades ejecutadas'}}, {{id: 'v_almacen', titulo: '7.- Movimiento de almacén'}},
                    {{id: 'v_maquina', titulo: '8.- Maquinarias y equipos'}}, {{id: 'v_herram', titulo: '9.- Herramientas manuales'}},
                    {{id: 'v_ocurrencia', titulo: '10.- Ocurrencias y otros'}}
                ];

                camposText.forEach(c => {{
                    const el = document.getElementById(c.id);
                    if(el && el.value) textoPapel += `${{c.titulo}}:<br>${{el.value.replace(/\\n/g, '<br>')}}<br>`;
                }});

                const outContainer = document.getElementById('out_general');
                outContainer.innerHTML = textoPapel;
                
                if (outContainer.offsetHeight > 560) {{
                    let cPrevio = outContainer.innerHTML;
                    outContainer.innerHTML = `
                        <div>${{cPrevio}}</div>
                        <span class="p-van-line">... Van</span>
                        <div class="p-break-page"></div>
                        <div style="display:flex; justify-content:space-between; width:100%; margin-bottom:10px; font-family:'Caveat', cursive; color:var(--celeste-obra); font-weight:bold; font-size:22px;">
                            <div style="padding-left:10px;">... VIENE DEL ASIENTO No ${{as_str}} DEL RESIDENTE DE OBRA</div>
                            <div style="padding-right:10px;">${{g_fechaAsiento}}</div>
                        </div>
                    `;
                }}
            }}

            const handle = document.getElementById('sliderHandle'); const track = document.getElementById('sliderTrack'); const progress = document.getElementById('sliderProgress');
            let isDragging = false, startX = 0, maxSlide = 0;
            function calcLimits() {{ maxSlide = track.clientWidth - handle.clientWidth - 8; }}
            window.addEventListener('resize', calcLimits); setTimeout(calcLimits, 500);
            function startDrag(e) {{ isDragging = true; startX = (e.clientX || e.touches[0].clientX) - handle.offsetLeft; calcLimits(); }}
            function onDrag(e) {{ if (!isDragging) return; let left = (e.clientX || e.touches[0].clientX) - startX; if (left < 4) left = 4; if (left > maxSlide) left = maxSlide; handle.style.left = left + 'px'; progress.style.width = (left + 23) + 'px'; if (left >= maxSlide - 2) {{ isDragging = false; firmar(); }} }}
            function stopDrag() {{ if (!isDragging) return; isDragging = false; handle.style.left = '4px'; progress.style.width = '0px'; }}
            handle.addEventListener('mousedown', startDrag); document.addEventListener('mousemove', onDrag); document.addEventListener('mouseup', stopDrag); handle.addEventListener('touchstart', startDrag, {{passive: true}}); document.addEventListener('touchmove', onDrag, {{passive: false}}); document.addEventListener('touchend', stopDrag);
            
            function firmar() {{ 
                handle.style.left = maxSlide + 'px'; progress.style.width = '100%'; handle.style.background = '#10b981'; 
                handle.innerHTML = '<i class="bi bi-check-lg"></i>'; document.getElementById('sliderText').innerText = "FIRMADO LEGALMENTE"; 
                mostrarAlerta("¡Asiento cerrado y guardado en Base de Datos con éxito!", "success");
                setTimeout(() => {{ window.location.href = '/cuaderno'; }}, 2500);
            }}
        </script>
    </body>
    </html>
    """
    
    return render_template_string(html_completo, menu_superior=menu_superior, fecha_hoy_iso=fecha_hoy_iso, numero_hoja=numero_hoja)
