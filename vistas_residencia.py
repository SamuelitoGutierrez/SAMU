# =========================================================
# vistas_residencia.py
# Módulo: Llenado de Cuaderno de Obra - Versión Completa y Unificada
# =========================================================

from flask import Blueprint, render_template_string, session, redirect, url_for
from navbar import obtener_navbar
from datetime import datetime

residencia_bp = Blueprint('residencia', __name__)

@residencia_bp.route('/residencia')
def redaccion_asiento_residente():
    if 'usuario_id' not in session:
        return redirect(url_for('login.mostrar_login'))

    es_admin = session.get('rol') == 'Admin'
    nombre_completo = session.get('nombre', 'Ing. Samuel Gutierrez')
    menu_superior = obtener_navbar(es_admin, nombre_completo)

    numero_asiento = "0088"
    
    # Generar fecha en formato: LUNES, 25/05/2026
    dias = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO", "DOMINGO"]
    fecha_dt = datetime.now()
    nombre_dia = dias[fecha_dt.weekday()]
    fecha_hoy = f"{nombre_dia}, {fecha_dt.strftime('%d/%m/%Y')}"

    html_completo = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>SAMU — Asiento N° {{ numero_asiento }}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Caveat:wght@600;700&display=swap" rel="stylesheet">
        
        <style>
            :root { --apple-text: #1d1d1f; --celeste-obra: #0263a0; --nav-height: 52px; }
            
            /* Fondo Degradado 20% (Azul, Celeste, Rosado sobre Blanco) */
            body { 
                font-family: 'Inter', sans-serif; color: var(--apple-text); overflow-x: hidden; padding-bottom: 90px; margin: 0;
                background: linear-gradient(135deg, rgba(255,255,255,1) 0%, rgba(2,99,160,0.1) 40%, rgba(135,206,235,0.15) 70%, rgba(249,168,212,0.15) 100%);
                background-attachment: fixed;
            }
            
            /* Animación Deslizante (Slide) */
            @keyframes slideInRight { 
                from { opacity: 0; transform: translateX(40px); } 
                to { opacity: 1; transform: translateX(0); } 
            }
            
            /* ==========================================
               STEPPER SUPERIOR (BARRA DE NAVEGACIÓN)
               ========================================== */
            .stepper-container { position: fixed; top: var(--nav-height); left: 0; width: 100%; background: rgba(255,255,255,0.85); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(0,0,0,0.08); z-index: 900; padding: 12px 20px; overflow-x: auto; white-space: nowrap; display: flex; gap: 12px; scroll-behavior: smooth; -ms-overflow-style: none; scrollbar-width: none; }
            .stepper-container::-webkit-scrollbar { display: none; }
            
            .step-btn { border: 1px solid #cbd5e1; border-radius: 30px; padding: 10px 20px; font-size: 12px; font-weight: 600; color: #475569; background: rgba(255,255,255,0.9); cursor: pointer; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
            .step-btn.active { background: #ffffff !important; color: #000000 !important; font-weight: 800 !important; transform: scale(1.08); box-shadow: 0 8px 20px rgba(0,0,0,0.08); border-color: #000000 !important; }
            .step-btn.omitted { background: #64748b !important; color: white !important; border-color: #475569 !important; }

            #globalTooltip { position: fixed; background: #ffffff; color: #1e293b; padding: 8px 16px; border-radius: 10px; font-size: 12px; font-weight: 700; white-space: nowrap; border: 1px solid #e2e8f0; box-shadow: 0 10px 25px rgba(0,0,0,0.15); pointer-events: none; z-index: 999999; opacity: 0; transition: opacity 0.15s ease; }

            /* ==========================================
               LAYOUT: FORMULARIO Y VISTA PREVIA
               ========================================== */
            .split-layout { display: flex; gap: 40px; max-width: 1500px; margin: 140px auto 0 auto; padding: 0 20px; align-items: flex-start; }
            .form-column { flex: 1; max-width: 600px; }
            .preview-column { flex: 1; position: sticky; top: 140px; height: calc(100vh - 240px); overflow-y: auto; }
            
            .step-view { display: none; animation: slideInRight 0.4s cubic-bezier(0.4, 0, 0.2, 1) forwards; background: rgba(255,255,255,0.8); backdrop-filter: blur(20px); padding: 30px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid rgba(255,255,255,1);}
            .step-view.active { display: block; }
            
            .step-title { font-size: 22px; font-weight: 800; margin-bottom: 25px; color: #0f172a; letter-spacing: -0.5px;}
            .form-label { font-size: 12px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px;}
            .form-control, .form-select { border-radius: 12px; border: 1px solid #cbd5e1; padding: 12px 14px; font-size: 14px; background: rgba(255,255,255,0.9); font-weight: 500;}
            .form-control:focus, .form-select:focus { border-color: #0066cc; box-shadow: 0 0 0 4px rgba(0,102,204,0.15); }

            .time-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 15px; display: flex; align-items: center; gap: 15px; transition: all 0.3s; cursor: pointer;}
            .time-card.active { border-color: var(--celeste-obra); background: #f0f9ff; }
            .clock-icon { font-size: 28px; color: #94a3b8; transition: color 0.3s; }
            .time-card.active .clock-icon { color: var(--celeste-obra); }

            .casco-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 12px; text-align: center; transition: all 0.3s; }
            .casco-card.active { border-color: #f59e0b; background: #fffbeb; }
            .casco-icon { font-size: 24px; color: #cbd5e1; transition: all 0.3s; }
            .casco-card.active .casco-icon { color: #f59e0b; transform: scale(1.1); }
            .casco-card input { border: none; background: transparent; text-align: center; font-weight: 800; font-size: 18px; width: 100%; margin-top: 5px; color: #000; padding: 0;}
            .casco-card input:focus { outline: none; }

            /* ==========================================
               CUADERNO FÍSICO (Ajustes de Encabezado y Línea)
               ========================================== */
            .papel-fisico { background: #fdfdfa; width: 100%; min-height: 950px; padding: 40px 50px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; font-family: Arial, sans-serif; color: #000; position: relative;}
            
            .p-header-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 5px; }
            .p-title-box { text-align: center; flex: 1; margin-left: 50px;}
            .p-title-box h1 { font-size: 26px; font-weight: bold; text-decoration: underline; letter-spacing: 1px; margin: 0; color: #000;}
            .p-num { font-size: 22px; font-weight: bold; margin-top: 5px; color: #000;}
            .p-sello { width: 90px; height: 90px; border: 2px dashed #94a3b8; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 11px; color: #94a3b8; text-align: center; padding: 5px; opacity: 0.5; margin-top: -20px;}
            
            /* Línea negra gruesa y menos espaciado */
            .p-meta { margin-bottom: 10px; padding-bottom: 10px; border-bottom: 3px solid #000; }
            .p-row { display: flex; align-items: flex-end; margin-bottom: 6px; }
            .p-label { font-size: 14px; font-weight: bold; margin-right: 8px; color: #000; white-space: nowrap; }
            .p-line { flex: 1; border-bottom: 1px solid #000; position: relative; height: 20px; }
            
            .lapicero-meta { position: absolute; bottom: -1px; left: 10px; font-family: 'Caveat', cursive; color: var(--celeste-obra); font-size: 18px; font-weight: 700; white-space: nowrap; }
            
            .p-body-lines { background-image: repeating-linear-gradient(transparent, transparent 23px, #94a3b8 24px); line-height: 24px; min-height: 650px; padding-top: 5px; position: relative; margin-top: 10px;}
            
            /* Tamaño 16px (visual equivale a 14px normal) y texto normal (no mayúsculas forzadas) */
            .lapicero { font-family: 'Caveat', cursive; color: var(--celeste-obra); font-size: 16px; line-height: 24px; padding-left: 5px; font-weight: 700; }
            .lapicero-muted { font-family: 'Caveat', cursive; color: #64748b; font-size: 16px; padding-left: 20px; font-weight: 600;}
            .p-van { position: absolute; bottom: 0; right: 10px; font-family: 'Caveat', cursive; color: var(--celeste-obra); font-size: 18px; font-weight: 700;}
            .p-footer { display: flex; justify-content: space-between; margin-top: 60px; font-size: 12px; font-weight: bold; color: #000;}
            .p-sig { border-top: 1px solid #000; width: 28%; text-align: center; padding-top: 5px; }

            /* ==========================================
               BARRA INFERIOR (Volver izq / Controles der)
               ========================================== */
            .bottom-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(255,255,255,0.9); backdrop-filter: blur(15px); border-top: 1px solid rgba(0,0,0,0.08); padding: 15px 30px; z-index: 900; display: flex; justify-content: space-between; align-items: center; }
            
            .slider-track { width: 100%; max-width: 400px; height: 60px; background: rgba(0,0,0,0.05); border-radius: 30px; position: relative; display: flex; align-items: center; justify-content: center; overflow: hidden; margin: 0 auto; border: 1px solid rgba(0,0,0,0.05);}
            .slider-text { font-size: 13px; font-weight: 800; color: #64748b; text-transform: uppercase; z-index: 1; pointer-events: none;}
            .slider-handle { width: 52px; height: 52px; background: #000; color: #fff; border-radius: 50%; position: absolute; left: 4px; display: flex; align-items: center; justify-content: center; z-index: 2; cursor: grab;}
            .slider-progress { position: absolute; left: 0; top: 0; height: 100%; background: rgba(0, 102, 204, 0.1); width: 0; pointer-events: none; }

            @media (max-width: 1024px) { .split-layout { flex-direction: column; align-items: center; margin-top: 130px; padding: 0 10px;} .form-column { width: 100%; max-width: 100%; } .preview-column { display: none; } .bottom-bar { padding: 15px; } .bottom-bar .btn { padding-left: 15px !important; padding-right: 15px !important; font-size: 13px; } }
        </style>
    </head>
    <body>

        {{ menu_superior | safe }}

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
            <button class="step-btn border-dark text-dark fw-bold" id="btnStep11" onclick="jumpToStep(11)" data-tooltip="Vista Final / Firmar"><i class="bi bi-shield-lock-fill"></i> Firma Final</button>
        </div>
        <div id="globalTooltip"></div>

        <div class="split-layout">
            
            <div class="form-column">
                <div class="d-flex justify-content-between mb-3 px-2">
                    <h6 class="text-primary fw-bold mb-0">Asiento N° {{ numero_asiento }}</h6>
                    <span class="text-muted small fw-bold">{{ fecha_hoy }}</span>
                </div>

                <form id="formResidencia" onsubmit="event.preventDefault();" oninput="sincronizarDatos()">
                    
                    <div class="step-view active" id="step1">
                        <div class="step-title">1.- Jornal de Trabajo</div>
                        <div class="row g-3">
                            <div class="col-sm-6">
                                <div class="time-card active" id="card_m" onclick="document.getElementById('v_jornal_m').focus()">
                                    <div class="clock-icon"><i class="bi bi-sunrise-fill"></i></div>
                                    <div class="w-100">
                                        <label class="form-label mb-1">Mañana (Inicio - Fin)</label>
                                        <input type="text" class="form-control border-0 p-0 req-step1" id="v_jornal_m" value="07:00 - 12:00" onfocus="activarReloj('m')">
                                    </div>
                                </div>
                            </div>
                            <div class="col-sm-6">
                                <div class="time-card" id="card_t" onclick="document.getElementById('v_jornal_t').focus()">
                                    <div class="clock-icon"><i class="bi bi-sunset-fill"></i></div>
                                    <div class="w-100">
                                        <label class="form-label mb-1">Tarde (Inicio - Fin)</label>
                                        <input type="text" class="form-control border-0 p-0 req-step1" id="v_jornal_t" value="13:00 - 17:00" onfocus="activarReloj('t')">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="step-view" id="step2">
                        <div class="step-title">2.- Personal de Obra</div>
                        <div class="row g-2">
                            <div class="col-4"><div class="casco-card" id="c_oper"><div class="casco-icon"><i class="bi bi-person-fill-gear"></i></div><span class="form-label d-block" style="font-size:10px;">Operarios</span><input type="number" class="req-step2" id="v_oper" placeholder="0"></div></div>
                            <div class="col-4"><div class="casco-card" id="c_ofic"><div class="casco-icon"><i class="bi bi-person-fill-check"></i></div><span class="form-label d-block" style="font-size:10px;">Oficiales</span><input type="number" class="req-step2" id="v_ofic" placeholder="0"></div></div>
                            <div class="col-4"><div class="casco-card" id="c_peon"><div class="casco-icon"><i class="bi bi-person-fill"></i></div><span class="form-label d-block" style="font-size:10px;">Peones</span><input type="number" class="req-step2" id="v_peon" placeholder="0"></div></div>
                            <div class="col-4"><div class="casco-card" id="c_meca"><div class="casco-icon"><i class="bi bi-nut-fill"></i></div><span class="form-label d-block" style="font-size:10px;">Mecánicos</span><input type="number" class="req-step2" id="v_meca" placeholder="0"></div></div>
                            <div class="col-4"><div class="casco-card" id="c_ctrl"><div class="casco-icon"><i class="bi bi-sign-stop-fill"></i></div><span class="form-label d-block" style="font-size:10px;">Controladores</span><input type="number" class="req-step2" id="v_ctrl" placeholder="0"></div></div>
                            <div class="col-4"><div class="casco-card" id="c_ope_maq"><div class="casco-icon"><i class="bi bi-truck-front-fill"></i></div><span class="form-label d-block" style="font-size:10px;">Operadores</span><input type="number" class="req-step2" id="v_ope_maq" placeholder="0"></div></div>
                        </div>
                    </div>

                    <div class="step-view" id="step3">
                        <div class="step-title">3.- Partidas Ejecutadas</div>
                        <p class="text-muted small mb-3">Escribe la partida y presiona <b>Enter</b> para agregarla rápido a la lista.</p>
                        <div class="input-group mb-3 shadow-sm">
                            <span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-primary"></i></span>
                            <input type="text" class="form-control border-start-0 ps-0" id="buscadorPartidas" placeholder="Ej: Conformación de base..." onkeydown="if(event.key==='Enter'){event.preventDefault(); agregarPartidaRapida();}">
                            <button class="btn btn-primary px-3" type="button" onclick="agregarPartidaRapida()"><i class="bi bi-plus-lg"></i></button>
                        </div>
                        
                        <div id="listaPartidasAgregadas" class="d-flex flex-column gap-2 req-step3"></div>
                        <input type="hidden" id="v_partidas" class="req-step3" value="">
                    </div>

                    <div class="step-view" id="step4"><div class="step-title">4.- Mayor Metrado</div><textarea class="form-control req-step4" id="v_mayor_m" rows="6" placeholder="Registre excedentes..."></textarea></div>
                    <div class="step-view" id="step5"><div class="step-title">5.- Sub Partidas</div><textarea class="form-control req-step5" id="v_sub_p" rows="6" placeholder="Sub partidas..."></textarea></div>
                    <div class="step-view" id="step6"><div class="step-title">6.- Actividades</div><textarea class="form-control req-step6" id="v_activ" rows="6" placeholder="Diario de actividades..."></textarea></div>
                    <div class="step-view" id="step7"><div class="step-title">7.- Almacén</div><textarea class="form-control req-step7" id="v_almacen" rows="6" placeholder="Ingresos y salidas..."></textarea></div>
                    <div class="step-view" id="step8"><div class="step-title">8.- Maquinarias</div><textarea class="form-control req-step8" id="v_maquina" rows="6" placeholder="Maquinarias..."></textarea></div>
                    <div class="step-view" id="step9"><div class="step-title">9.- Herramientas</div><textarea class="form-control req-step9" id="v_herram" rows="4" placeholder="Herramientas..."></textarea></div>
                    <div class="step-view" id="step10"><div class="step-title text-danger">10.- Ocurrencias</div><textarea class="form-control border-danger req-step10" id="v_ocurrencia" rows="8" placeholder="Ocurrencias legales..."></textarea></div>

                    <div class="step-view" id="step11">
                        <div class="step-title text-success text-center mb-4"><i class="bi bi-shield-check"></i> Listo para Firmar</div>
                        <p class="text-center text-muted small mb-5">Verifica la hoja de cuaderno generada a la derecha. Al deslizar el candado, los datos quedarán inmutables.</p>
                        <div class="slider-track" id="sliderTrack">
                            <div class="slider-progress" id="sliderProgress"></div>
                            <div class="slider-text" id="sliderText">Deslizar para Firmar</div>
                            <div class="slider-handle" id="sliderHandle"><i class="bi bi-lock-fill" style="font-size: 1.2rem;"></i></div>
                        </div>
                    </div>
                </form>
            </div>

            <div class="preview-column">
                <div class="papel-fisico" id="papelOficial">
                    
                    <div class="p-header-top">
                        <div style="width: 90px;"></div>
                        <div class="p-title-box">
                            <h1>CUADERNO DE OBRA</h1>
                        </div>
                        <div style="text-align: right; width: 110px;">
                            <div class="p-num">Nº <span style="font-size: 26px; margin-left:5px;">{{ numero_asiento }}</span></div>
                            <div class="p-sello">Sello Juzgado<br>Paz Letrado</div>
                        </div>
                    </div>
                    
                    <div class="p-meta">
                        <div class="d-flex w-100 mb-1">
                            <div class="d-flex" style="flex: 0.5;">
                                <span class="p-label">Fecha:</span>
                                <div class="p-line"><span class="lapicero-meta">{{ fecha_hoy }}</span></div>
                            </div>
                            <div class="d-flex" style="flex: 0.5; margin-left: 15px;">
                                <span class="p-label">Modalidad:</span>
                                <div class="p-line"><span class="lapicero-meta">Administración Directa</span></div>
                            </div>
                        </div>
                        <div class="p-row"><span class="p-label">Obra:</span><div class="p-line"><span class="lapicero-meta">Mejoramiento de la Carretera Asiruni - Rosaspata</span></div></div>
                        <div class="p-row"><span class="p-label">Proyecto:</span><div class="p-line"><span class="lapicero-meta">Tramo I</span></div></div>
                        <div class="p-row"><span class="p-label">Programa:</span><div class="p-line"><span class="lapicero-meta">-</span></div></div>
                        <div class="p-row"><span class="p-label">Entidad Ejecutora:</span><div class="p-line"><span class="lapicero-meta">Gobierno Regional Puno</span></div></div>
                    </div>

                    <div class="p-body-lines">
                        <div class="lapicero-muted" style="margin-bottom: 0px;">... Viene del ASIENTO Nº 0087 DEL RESIDENTE DE OBRA </div>
                        
                        <div class="lapicero" id="out_general"></div>
                        
                        <div class="p-van" id="indicadorVan" style="display:none;">... Van</div>
                    </div>

                    <div class="p-footer">
                        <div class="p-sig">ING. INSPECTOR</div>
                        <div class="p-sig">ING. RESIDENTE</div>
                        <div class="p-sig">ING. SUPERVISOR</div>
                    </div>

                </div>
            </div>

        </div>

        <div class="bottom-bar shadow-lg">
            <div>
                <a href="/cuaderno" class="btn btn-light border fw-bold rounded-pill px-4 text-dark shadow-sm"><i class="bi bi-arrow-left"></i> Volver al Lobby</a>
            </div>
            <div class="d-flex gap-2 align-items-center">
                <div id="indicadorGuardado" class="small text-muted fw-semibold d-none d-sm-block me-2"><i class="bi bi-cloud-arrow-up"></i> Autoguardado</div>
                <button type="button" class="btn btn-outline-secondary fw-bold rounded-pill px-4 shadow-sm" onclick="omitirPaso()">Omitir</button>
                <button type="button" class="btn btn-dark fw-bold rounded-pill px-4 shadow-sm" onclick="siguientePaso()">Guardar y Continuar <i class="bi bi-arrow-right"></i></button>
            </div>
        </div>

        <script>
            let currentStep = 1;
            const totalSteps = 11;

            // 1. Tooltip Elegante
            const gTooltip = document.getElementById('globalTooltip');
            document.querySelectorAll('.step-btn').forEach(btn => {
                btn.addEventListener('mousemove', (e) => {
                    gTooltip.innerText = btn.getAttribute('data-tooltip');
                    gTooltip.style.left = (e.clientX + 15) + 'px';
                    gTooltip.style.top = (e.clientY + 15) + 'px';
                    gTooltip.style.opacity = '1';
                });
                btn.addEventListener('mouseleave', () => { gTooltip.style.opacity = '0'; });
            });
            
            // 2. Navegación (Animación SlideIn controlada CSS)
            function jumpToStep(stepIndex) {
                document.getElementById('indicadorGuardado').innerHTML = '<i class="bi bi-check2-all text-success"></i> Guardado';
                setTimeout(() => { document.getElementById('indicadorGuardado').innerHTML = '<i class="bi bi-cloud-arrow-up"></i> Autoguardado'; }, 2000);

                document.getElementById(`step${currentStep}`).classList.remove('active');
                document.getElementById(`btnStep${currentStep}`).classList.remove('active');
                
                currentStep = stepIndex;
                document.getElementById(`step${currentStep}`).classList.add('active');
                document.getElementById(`btnStep${currentStep}`).classList.add('active');
                document.getElementById('stepperBar').scrollLeft = document.getElementById(`btnStep${currentStep}`).offsetLeft - 50;

                if (currentStep === 11) {
                    document.querySelector('.bottom-bar').style.display = 'none';
                    document.querySelector('.preview-column').style.display = 'block';
                } else {
                    document.querySelector('.bottom-bar').style.display = 'flex';
                    if(window.innerWidth <= 1024) document.querySelector('.preview-column').style.display = 'none';
                }
                sincronizarDatos();
            }

            function siguientePaso() { if(currentStep < totalSteps) jumpToStep(currentStep + 1); }
            
            function omitirPaso() {
                document.querySelectorAll(`.req-step${currentStep}`).forEach(inp => { if (inp.tagName === 'TEXTAREA' || inp.type === 'text') inp.value = "Sin novedad en la jornada."; });
                document.getElementById(`btnStep${currentStep}`).classList.add('omitted');
                sincronizarDatos(); siguientePaso();
            }

            function activarReloj(turno) {
                document.getElementById('card_m').classList.remove('active');
                document.getElementById('card_t').classList.remove('active');
                document.getElementById('card_'+turno).classList.add('active');
            }

            // ==========================================
            // LÓGICA DE PARTIDAS (MÉTODO ENTER)
            // ==========================================
            let partidasList = [];
            function agregarPartidaRapida() {
                const inputBuscador = document.getElementById('buscadorPartidas');
                const desc = inputBuscador.value.trim();
                if(desc === '') return;

                partidasList.push({ descripcion: desc, metrado: '' });
                inputBuscador.value = ''; // Limpia el input
                renderizarListaPartidas();
                document.getElementById('v_partidas').value = "lleno"; // Para activar termómetro
                sincronizarDatos();
            }

            function actualizarMetrado(index, valor) {
                partidasList[index].metrado = valor;
                sincronizarDatos();
            }

            function eliminarPartida(index) {
                partidasList.splice(index, 1);
                if(partidasList.length === 0) document.getElementById('v_partidas').value = "";
                renderizarListaPartidas();
                sincronizarDatos();
            }

            function renderizarListaPartidas() {
                const container = document.getElementById('listaPartidasAgregadas');
                container.innerHTML = partidasList.map((p, index) => `
                    <div class="bg-white border rounded-3 p-2 d-flex justify-content-between align-items-center shadow-sm">
                        <span class="text-truncate flex-grow-1 small fw-semibold me-2">${p.descripcion}</span>
                        <input type="text" class="form-control form-control-sm text-end border-primary" style="width: 100px; background:#f0f9ff;" placeholder="Metrado" value="${p.metrado}" oninput="actualizarMetrado(${index}, this.value)">
                        <button class="btn btn-sm text-danger ms-2" onclick="eliminarPartida(${index})"><i class="bi bi-trash"></i></button>
                    </div>
                `).join('');
            }

            // ==========================================
            // SINCRONIZACIÓN AL CUADERNO
            // ==========================================
            function sincronizarDatos() {
                for (let i = 1; i <= 10; i++) {
                    const inputs = document.querySelectorAll(`.req-step${i}`);
                    if (inputs.length === 0) continue;
                    let llenos = 0;
                    inputs.forEach(inp => { if (inp.value.trim() !== '' && inp.value.trim() !== '0') llenos++; });
                    let btn = document.getElementById(`btnStep${i}`);
                    let porcentaje = Math.round((llenos / inputs.length) * 100);
                    
                    if (!btn.classList.contains('omitted')) {
                        btn.setAttribute('data-tooltip', porcentaje === 100 ? "¡Completado!" : `Progreso: ${porcentaje}%`);
                        btn.style.background = `linear-gradient(to right, #bfdbfe ${porcentaje}%, #f8fafc ${porcentaje}%)`;
                    }
                }

                const idsCascos = ['oper', 'ofic', 'peon', 'meca', 'ctrl', 'ope_maq'];
                idsCascos.forEach(id => {
                    const val = document.getElementById('v_'+id).value;
                    const card = document.getElementById('c_'+id);
                    if(val > 0) card.classList.add('active');
                    else card.classList.remove('active');
                });

                // Texto Normal (No forzado a mayúsculas) y Alineado
                let numAsiento = "{{ numero_asiento }}";
                let fechaLarga = "{{ fecha_hoy }}";
                let textoPapel = `&nbsp;&nbsp;Asiento N° ${numAsiento} del Residente de Obra &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${fechaLarga}<br>`;

                const vJ1 = document.getElementById('v_jornal_m').value;
                const vJ2 = document.getElementById('v_jornal_t').value;
                if(vJ1 || vJ2) {
                    textoPapel += `1.- Jornal de trabajo<br>Mañana: ${vJ1} ; Tarde: ${vJ2}<br>`;
                }
                
                const vOper = (document.getElementById('v_oper').value || '0').padStart(2, '0');
                const vOfic = (document.getElementById('v_ofic').value || '0').padStart(2, '0');
                const vPeon = (document.getElementById('v_peon').value || '0').padStart(2, '0');
                const vMeca = (document.getElementById('v_meca').value || '0').padStart(2, '0');
                const vCtrl = (document.getElementById('v_ctrl').value || '0').padStart(2, '0');
                const vOpe = (document.getElementById('v_ope_maq').value || '0').padStart(2, '0');

                textoPapel += `2.- Personal de obra:<br>`;
                textoPapel += `${vOper} operarios &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${vOfic} oficiales &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${vPeon} peones &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${vMeca} mecánicos<br>`;
                textoPapel += `${vCtrl} controladores de maq. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${vOpe} operadores de maq.<br>`;

                // Partidas por Enter
                if(partidasList.length > 0) {
                    textoPapel += `3.- Partidas ejecutadas<br>`;
                    partidasList.forEach(p => {
                        textoPapel += `- ${p.descripcion} &nbsp;&nbsp;&nbsp; (Metrado: ${p.metrado || '0'})<br>`;
                    });
                }

                const camposText = [
                    {id: 'mayor_m', titulo: '4.- Partidas de mayor metrado'},
                    {id: 'sub_p', titulo: '5.- Sub partidas ejecutadas'},
                    {id: 'activ', titulo: '6.- Actividades ejecutadas'},
                    {id: 'almacen', titulo: '7.- Movimiento de almacén'},
                    {id: 'maquina', titulo: '8.- Maquinarias y equipos'},
                    {id: 'herram', titulo: '9.- Herramientas manuales'},
                    {id: 'ocurrencia', titulo: '10.- Ocurrencias y otros'}
                ];

                camposText.forEach(campo => {
                    const val = document.getElementById('v_' + campo.id).value;
                    if(val) {
                        textoPapel += `${campo.titulo}<br>${val.replace(/\\n/g, '<br>')}<br>`;
                    }
                });

                document.getElementById('out_general').innerHTML = textoPapel;
                
                const bodyLines = document.querySelector('.p-body-lines');
                if (bodyLines.scrollHeight > 650) document.getElementById('indicadorVan').style.display = 'block';
                else document.getElementById('indicadorVan').style.display = 'none';
            }

            // 5. Slider de Firma
            const handle = document.getElementById('sliderHandle'); const track = document.getElementById('sliderTrack'); const progress = document.getElementById('sliderProgress');
            let isDragging = false, startX = 0, maxSlide = 0;
            function calcLimits() { maxSlide = track.clientWidth - handle.clientWidth - 8; }
            window.addEventListener('resize', calcLimits); setTimeout(calcLimits, 500);

            function startDrag(e) { isDragging = true; startX = (e.clientX || e.touches[0].clientX) - handle.offsetLeft; calcLimits(); }
            function onDrag(e) {
                if (!isDragging) return;
                let left = (e.clientX || e.touches[0].clientX) - startX;
                if (left < 4) left = 4; if (left > maxSlide) left = maxSlide;
                handle.style.left = left + 'px'; progress.style.width = (left + 23) + 'px';
                if (left >= maxSlide - 2) { isDragging = false; firmar(); }
            }
            function stopDrag() {
                if (!isDragging) return; isDragging = false;
                handle.style.left = '4px'; progress.style.width = '0px';
            }

            handle.addEventListener('mousedown', startDrag); document.addEventListener('mousemove', onDrag); document.addEventListener('mouseup', stopDrag);
            handle.addEventListener('touchstart', startDrag, {passive: true}); document.addEventListener('touchmove', onDrag, {passive: false}); document.addEventListener('touchend', stopDrag);

            function firmar() {
                handle.style.left = maxSlide + 'px'; progress.style.width = '100%'; handle.style.background = '#10b981';
                handle.innerHTML = '<i class="bi bi-check-lg"></i>'; document.getElementById('sliderText').innerText = "FIRMADO LEGALMENTE";
                alert("¡Asiento N° 0088 firmado con éxito!"); window.location.href = '/cuaderno';
            }
            
            sincronizarDatos();
        </script>
    </body>
    </html>
    """
    
    return render_template_string(html_completo, menu_superior=menu_superior, numero_asiento=numero_asiento, fecha_hoy=fecha_hoy)
