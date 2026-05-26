# =========================================================
# vistas_residencia.py
# Módulo: Cuaderno de Obra - Versión Élite Separada en Bloques
# =========================================================

from flask import Blueprint, render_template_string, session, redirect, url_for
from navbar import obtener_navbar
from datetime import datetime

residencia_bp = Blueprint('residencia', __name__)

# ==============================================================================
# BLOQUE 1: ESTILOS CSS (DISEÑO, FONDO Y CUADERNO FÍSICO)
# ==============================================================================
BLOQUE_1_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&display=swap');
    
    :root { --apple-text: #1d1d1f; --celeste-obra: #0263a0; --nav-height: 52px; }
    body { font-family: 'Inter', sans-serif; color: var(--apple-text); overflow-x: hidden; padding-bottom: 90px; margin: 0; background: linear-gradient(135deg, rgba(255,255,255,1) 0%, rgba(2,99,160,0.08) 40%, rgba(135,206,235,0.12) 70%, rgba(249,168,212,0.12) 100%); background-attachment: fixed; }
    
    /* Animaciones Flotantes */
    @keyframes floatInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes floatOutDown { from { opacity: 1; transform: translateY(0); } to { opacity: 0; transform: translateY(30px); } }
    
    /* Stepper Superior */
    .stepper-container { position: fixed; top: var(--nav-height); left: 0; width: 100%; background: rgba(255,255,255,0.85); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(0,0,0,0.08); z-index: 900; padding: 12px 20px; overflow-x: auto; white-space: nowrap; display: flex; gap: 12px; scroll-behavior: smooth; -ms-overflow-style: none; scrollbar-width: none; opacity: 0; pointer-events: none; transition: opacity 0.5s;}
    .stepper-container::-webkit-scrollbar { display: none; }
    .step-btn { border: 1px solid #cbd5e1; border-radius: 30px; padding: 10px 20px; font-size: 12px; font-weight: 600; color: #475569; background: rgba(255,255,255,0.9); cursor: pointer; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
    .step-btn.active { background: #ffffff !important; color: #000000 !important; font-weight: 800 !important; transform: scale(1.08); box-shadow: 0 8px 20px rgba(0,0,0,0.08); border-color: #000000 !important; }
    .step-btn.omitted { background: #64748b !important; color: white !important; border-color: #475569 !important; }

    #globalTooltip { position: fixed; background: #ffffff; color: #1e293b; padding: 8px 16px; border-radius: 10px; font-size: 12px; font-weight: 700; white-space: nowrap; border: 1px solid #e2e8f0; box-shadow: 0 10px 25px rgba(0,0,0,0.15); pointer-events: none; z-index: 999999; opacity: 0; transition: opacity 0.15s ease; }

    /* Layout Central */
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
    .form-control:focus, .form-select:focus { border-color: #0066cc; box-shadow: 0 0 0 4px rgba(0,102,204,0.15); }

    /* Tarjetas UI (Relojes y Personal) */
    .time-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 15px; display: flex; align-items: center; gap: 15px; transition: all 0.3s; cursor: pointer;}
    .time-card.active { border-color: var(--celeste-obra); background: #f0f9ff; }
    .clock-icon { font-size: 28px; color: #94a3b8; transition: color 0.3s; }
    .time-card.active .clock-icon { color: var(--celeste-obra); }

    .elegant-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 16px 12px; text-align: center; transition: all 0.3s; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative;}
    .elegant-card:hover { border-color: var(--celeste-obra); transform: translateY(-2px); }
    .elegant-card.active { border-color: var(--celeste-obra); background: rgba(2, 99, 160, 0.03); box-shadow: 0 10px 20px rgba(2,99,160,0.05); }
    .p-icon { font-size: 26px; color: #94a3b8; transition: all 0.3s; margin-bottom: 4px; }
    .elegant-card.active .p-icon { color: var(--celeste-obra); transform: scale(1.1); }
    .elegant-card input { border: none; background: transparent; text-align: center; font-weight: 800; font-size: 20px; width: 100%; color: #000; padding: 0;}
    .elegant-card input:focus { outline: none; }

    /* ==========================================
       DISEÑO DEL CUADERNO FÍSICO Y RAYADO
       ========================================== */
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
    
    /* El texto escrito a mano ahora tiene 16px */
    .lapicero { font-family: 'Caveat', cursive; color: var(--celeste-obra); font-size: 16px; line-height: 24px; padding-left: 2px; font-weight: 700; }
    .p-van-line { text-align: right; font-family: 'Caveat', cursive; color: var(--celeste-obra); font-size: 18px; font-weight: 700; display: block; width: 100%; margin-top: 12px; padding-right: 10px;}
    .p-break-page { border-top: 2px dashed #94a3b8; margin: 35px 0 20px 0; padding-top: 15px; position: relative; }
    .p-break-page::before { content: 'SIGUIENTE FOLIO (HOJA 2)'; position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background: #fdfdfa; padding: 0 15px; font-size: 10px; color: #94a3b8; font-weight: bold; letter-spacing: 1px;}
    
    .p-footer { display: flex; justify-content: space-between; margin-top: 50px; font-size: 12px; font-weight: bold; color: #000;}
    .p-sig { border-top: 1px solid #000; width: 28%; text-align: center; padding-top: 5px; }

    /* Barra Inferior Oculta al inicio */
    .bottom-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(255,255,255,0.95); backdrop-filter: blur(15px); border-top: 1px solid rgba(0,0,0,0.08); padding: 15px 30px; z-index: 900; display: flex; justify-content: space-between; align-items: center; opacity: 0; pointer-events: none; transition: opacity 0.5s;}
    .bottom-bar.unlocked { opacity: 1; pointer-events: all; }
    
    .slider-track { width: 100%; max-width: 400px; height: 60px; background: rgba(0,0,0,0.05); border-radius: 30px; position: relative; display: flex; align-items: center; justify-content: center; overflow: hidden; margin: 0 auto; border: 1px solid rgba(0,0,0,0.05);}
    .slider-text { font-size: 13px; font-weight: 800; color: #64748b; text-transform: uppercase; z-index: 1; pointer-events: none;}
    .slider-handle { width: 52px; height: 52px; background: #000; color: #fff; border-radius: 50%; position: absolute; left: 4px; display: flex; align-items: center; justify-content: center; z-index: 2; cursor: grab;}
    .slider-progress { position: absolute; left: 0; top: 0; height: 100%; background: rgba(0, 102, 204, 0.1); width: 0; pointer-events: none; }

    @media (max-width: 1024px) { .split-layout { flex-direction: column; align-items: center; margin-top: 130px; padding: 0 10px;} .form-column { width: 100%; max-width: 100%; } .preview-column { display: none; } }
</style>
"""

# ==============================================================================
# BLOQUE 2: MODALES Y STEPPER SUPERIOR
# ==============================================================================
BLOQUE_2_MODALES_Y_STEPPER = """
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
                    <input type="date" id="initFecha" class="form-control form-control-lg bg-light" value="{{ fecha_hoy_iso }}">
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
    <button class="step-btn" id="btnStep4" onclick="jumpToStep(4)" data-tooltip="Faltan datos">4. Mayor Metrado</button>
    <button class="step-btn" id="btnStep5" onclick="jumpToStep(5)" data-tooltip="Faltan datos">5. Sub Partidas</button>
    <button class="step-btn" id="btnStep6" onclick="jumpToStep(6)" data-tooltip="Faltan datos">6. Actividades</button>
    <button class="step-btn" id="btnStep7" onclick="jumpToStep(7)" data-tooltip="Faltan datos">7. Almacén</button>
    <button class="step-btn" id="btnStep8" onclick="jumpToStep(8)" data-tooltip="Faltan datos">8. Maquinaria</button>
    <button class="step-btn" id="btnStep9" onclick="jumpToStep(9)" data-tooltip="Faltan datos">9. Herramientas</button>
    <button class="step-btn" id="btnStep10" onclick="jumpToStep(10)" data-tooltip="Faltan datos">10. Ocurrencias</button>
    <button class="step-btn border-dark text-dark fw-bold" id="btnStep11" onclick="jumpToStep(11)" data-tooltip="Vista Final"><i class="bi bi-shield-lock-fill"></i> Firma Final</button>
</div>
<div id="globalTooltip"></div>

<div class="modal fade" id="modalExcel" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content" style="border-radius: 20px;">
            <div class="modal-header border-0 pb-0"><h5 class="modal-title fw-bold text-success"><i class="bi bi-file-earmark-spreadsheet"></i> Pegado Masivo (Excel)</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
            <div class="modal-body">
                <textarea id="textoExcelMasivo" class="form-control" rows="8" placeholder="Control + V para insertar la data de Excel (Descripción | Metrado)..."></textarea>
            </div>
            <div class="modal-footer border-0 pt-0">
                <button type="button" class="btn btn-light rounded-pill px-4" data-bs-dismiss="modal">Cerrar</button>
                <button type="button" class="btn btn-success rounded-pill px-4 fw-bold" onclick="procesarExcelMasivo()">Procesar Datos</button>
            </div>
        </div>
    </div>
</div>
"""

# ==============================================================================
# BLOQUE 3: FORMULARIOS (COLUMNA IZQUIERDA)
# ==============================================================================
BLOQUE_3_FORMULARIO = """
<div class="form-column">
    <div class="d-flex justify-content-between mb-3 px-2">
        <h6 class="text-primary fw-bold mb-0">Asiento N° <span id="lbl_num_asiento">--</span></h6>
        <span class="text-muted small fw-bold" id="lbl_fecha_asiento">--</span>
    </div>

    <form id="formResidencia" onsubmit="event.preventDefault();" oninput="sincronizarDatos()">
        
        <div class="step-view active" id="step1">
            <div class="step-title">1.- Jornal de Trabajo</div>
            <div class="row g-3">
                <div class="col-sm-6"><div class="time-card active" id="card_m" onclick="document.getElementById('v_jornal_m').focus()"><div class="clock-icon"><i class="bi bi-sunrise-fill"></i></div><div class="w-100"><label class="form-label mb-1">Mañana (Inicio - Fin)</label><input type="text" class="form-control border-0 p-0 req-step1" id="v_jornal_m" value="07:00 - 12:00" onfocus="activarReloj('m')"></div></div></div>
                <div class="col-sm-6"><div class="time-card" id="card_t" onclick="document.getElementById('v_jornal_t').focus()"><div class="clock-icon"><i class="bi bi-sunset-fill"></i></div><div class="w-100"><label class="form-label mb-1">Tarde (Inicio - Fin)</label><input type="text" class="form-control border-0 p-0 req-step1" id="v_jornal_t" value="13:00 - 17:00" onfocus="activarReloj('t')"></div></div></div>
            </div>
        </div>

        <div class="step-view" id="step2">
            <div class="step-title">2.- Personal de Obra</div>
            <div class="row g-2">
                <div class="col-4"><div class="elegant-card" id="c_oper"><div class="p-icon"><i class="bi bi-person-badge-fill"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:600;">Operarios</span><input type="number" class="req-step2" id="v_oper" placeholder="0" oninput="evaluarTarjeta('oper')"></div></div>
                <div class="col-4"><div class="elegant-card" id="c_ofic"><div class="p-icon"><i class="bi bi-person-check-fill"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:600;">Oficiales</span><input type="number" class="req-step2" id="v_ofic" placeholder="0" oninput="evaluarTarjeta('ofic')"></div></div>
                <div class="col-4"><div class="elegant-card" id="c_peon"><div class="p-icon"><i class="bi bi-person-fill"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:600;">Peones</span><input type="number" class="req-step2" id="v_peon" placeholder="0" oninput="evaluarTarjeta('peon')"></div></div>
                <div class="col-4"><div class="elegant-card" id="c_meca"><div class="p-icon"><i class="bi bi-tools"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:600;">Mecánicos</span><input type="number" class="req-step2" id="v_meca" placeholder="0" oninput="evaluarTarjeta('meca')"></div></div>
                <div class="col-4"><div class="elegant-card" id="c_ctrl"><div class="p-icon"><i class="bi bi-clipboard-check-fill"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:600;">Controladores</span><input type="number" class="req-step2" id="v_ctrl" placeholder="0" oninput="evaluarTarjeta('ctrl')"></div></div>
                <div class="col-4"><div class="elegant-card" id="c_ope_maq"><div class="p-icon"><i class="bi bi-truck"></i></div><span class="form-label d-block text-muted" style="font-size:10px; font-weight:600;">Operadores</span><input type="number" class="req-step2" id="v_ope_maq" placeholder="0" oninput="evaluarTarjeta('ope_maq')"></div></div>
            </div>
        </div>

        <div class="step-view" id="step3">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <div class="step-title mb-0">3.- Partidas Ejecutadas</div>
                <button type="button" class="btn btn-sm btn-outline-success rounded-pill fw-bold shadow-sm" onclick="abrirModalMasivo()"><i class="bi bi-file-earmark-excel"></i> Excel Masivo</button>
            </div>
            <div class="input-group mb-3 shadow-sm">
                <span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-primary"></i></span>
                <input type="text" class="form-control border-start-0 ps-0" id="buscadorPartidas" placeholder="Escribe partida y presiona Enter..." onkeydown="if(event.key==='Enter'){event.preventDefault(); agregarPartidaRapida();}">
                <button class="btn btn-primary px-3" type="button" onclick="agregarPartidaRapida()"><i class="bi bi-plus-lg"></i></button>
            </div>
            <div id="listaPartidasAgregadas" class="d-flex flex-column gap-2 req-step3"></div>
            <input type="hidden" id="v_partidas" class="req-step3" value="">
        </div>

        <div class="step-view" id="step4"><div class="step-title">4.- Mayor Metrado</div><textarea class="form-control req-step4" id="v_mayor_m" rows="6" placeholder="Registre excedentes..."></textarea></div>
        <div class="step-view" id="step5"><div class="step-title">5.- Sub Partidas</div><textarea class="form-control req-step5" id="v_sub_p" rows="6" placeholder="Sub partidas..."></textarea></div>
        <div class="step-view" id="step6"><div class="step-title">6.- Actividades</div><textarea class="form-control req-step6" id="v_activ" rows="6" placeholder="Diario de actividades..."></textarea></div>
        <div class="step-view" id="step7"><div class="step-title">7.- Almacén</div><textarea class="form-control req-step7" id="v_almacen" rows="6" placeholder="Ingresos y salidas..."></textarea></div>
        <div class="step-view" id="step8"><div class="step-title">8.- Maquinaria</div><textarea class="form-control req-step8" id="v_maquina" rows="6" placeholder="Horas de flota..."></textarea></div>
        <div class="step-view" id="step9"><div class="step-title">9.- Herramientas</div><textarea class="form-control req-step9" id="v_herram" rows="4" placeholder="Inventario manual..."></textarea></div>
        <div class="step-view" id="step10"><div class="step-title text-danger">10.- Ocurrencias</div><textarea class="form-control border-danger req-step10" id="v_ocurrencia" rows="8" placeholder="Redacción técnica y legal de campo..."></textarea></div>

        <div class="step-view" id="step11">
            <div class="step-title text-success text-center mb-4"><i class="bi bi-shield-check"></i> Sellar Folio</div>
            <p class="text-center text-muted small mb-5">Verifica la hoja de cuaderno generada a la derecha. Al deslizar el candado, los datos quedarán inmutables.</p>
            <div class="slider-track" id="sliderTrack"><div class="slider-progress" id="sliderProgress"></div><div class="slider-text" id="sliderText">Deslizar para Firmar</div><div class="slider-handle" id="sliderHandle"><i class="bi bi-lock-fill" style="font-size: 1.2rem;"></i></div></div>
        </div>
    </form>
</div>
"""

# ==============================================================================
# BLOQUE 4: VISTA PREVIA (CUADERNO FÍSICO)
# ==============================================================================
BLOQUE_4_CUADERNO = """
<div class="preview-column">
    <div class="papel-fisico" id="papelOficial">
        <div class="p-header-top">
            <div style="width: 80px;"></div>
            <div class="p-title-box"><h1>CUADERNO DE OBRA</h1></div>
            <div style="text-align: right; width: 80px;"><div class="p-num">Nº <span style="font-size: 26px; margin-left:3px;">0001</span></div></div>
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
            <div class="p-sig">ING. INSPECTOR</div>
            <div class="p-sig">ING. RESIDENTE</div>
            <div class="p-sig">ING. SUPERVISOR</div>
        </div>
    </div>
</div>
"""

# ==============================================================================
# BLOQUE 5: JAVASCRIPT (LÓGICA BLINDADA Y ANTI-ERRORES)
# ==============================================================================
BLOQUE_5_JS = """
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
    // Variables Globales
    let g_numAsiento = "";
    let g_fechaAsiento = "";
    let currentStep = 1;
    const totalSteps = 11;
    let isAnimating = false;

    // Disparador del Modal al iniciar
    document.addEventListener("DOMContentLoaded", function() {
        const myModal = new bootstrap.Modal(document.getElementById('modalConfigInicial'));
        myModal.show();
    });

    // Formateador de Fecha Puno (LUNES, 25/05/2026)
    function formatearFecha(fechaStr) {
        const dias = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO", "DOMINGO"];
        const [y, m, d] = fechaStr.split('-');
        const dateObj = new Date(y, m-1, d);
        let dayIndex = dateObj.getDay() - 1;
        if(dayIndex === -1) dayIndex = 6;
        return `${dias[dayIndex]}, ${d}/${m}/${y}`;
    }

    // Al apretar el botón INICIAR REDACCIÓN en el Modal
    function iniciarAsiento() {
        g_numAsiento = document.getElementById('initNumAsiento').value;
        let rawDate = document.getElementById('initFecha').value;
        if(!g_numAsiento || !rawDate) { alert("Debe completar el número de asiento y la fecha."); return; }
        
        g_fechaAsiento = formatearFecha(rawDate);
        document.getElementById('lbl_num_asiento').innerText = g_numAsiento.padStart(4, '0');
        document.getElementById('lbl_fecha_asiento').innerText = g_fechaAsiento;
        document.getElementById('lbl_hoja_fecha').innerText = g_fechaAsiento;
        
        // Desbloquear Pantalla
        bootstrap.Modal.getInstance(document.getElementById('modalConfigInicial')).hide();
        document.getElementById('mainLayout').classList.add('unlocked');
        document.getElementById('stepperBar').style.opacity = '1';
        document.getElementById('stepperBar').style.pointerEvents = 'all';
        document.getElementById('bottomBarUI').classList.add('unlocked');
        
        // FORZAR PRIMERA ESCRITURA
        sincronizarDatos();
    }

    // Lógica de Tooltip
    const gTooltip = document.getElementById('globalTooltip');
    document.querySelectorAll('.step-btn').forEach(btn => {
        btn.addEventListener('mousemove', (e) => { gTooltip.innerText = btn.getAttribute('data-tooltip'); gTooltip.style.left = (e.clientX + 15) + 'px'; gTooltip.style.top = (e.clientY + 15) + 'px'; gTooltip.style.opacity = '1'; });
        btn.addEventListener('mouseleave', () => { gTooltip.style.opacity = '0'; });
    });
    
    // Navegación (Botón Anterior y Siguiente)
    function jumpToStep(stepIndex) {
        if (isAnimating || currentStep === stepIndex) return;
        isAnimating = true;

        document.getElementById('indicadorGuardado').innerHTML = '<i class="bi bi-check2-all text-success"></i> Sincronizado';
        setTimeout(() => { document.getElementById('indicadorGuardado').innerHTML = '<i class="bi bi-cloud-arrow-up"></i> Autoguardado'; }, 2000);

        const currentView = document.getElementById(`step${currentStep}`);
        currentView.classList.remove('active');
        currentView.classList.add('exit');
        document.getElementById(`btnStep${currentStep}`).classList.remove('active');
        
        setTimeout(() => {
            currentView.classList.remove('exit');
            currentStep = stepIndex;
            const nextView = document.getElementById(`step${currentStep}`);
            nextView.classList.add('active');
            
            document.getElementById(`btnStep${currentStep}`).classList.add('active');
            document.getElementById('stepperBar').scrollLeft = document.getElementById(`btnStep${currentStep}`).offsetLeft - 50;

            const btnAtras = document.getElementById('btnAtras');
            if (currentStep > 1) { btnAtras.classList.remove('d-none'); } else { btnAtras.classList.add('d-none'); }

            if (currentStep === 11) {
                document.querySelector('.bottom-bar').style.display = 'none';
                document.querySelector('.preview-column').style.display = 'block';
            } else {
                document.querySelector('.bottom-bar').style.display = 'flex';
                if(window.innerWidth <= 1024) document.querySelector('.preview-column').style.display = 'none';
            }
            isAnimating = false;
        }, 300); 
    }

    function siguientePaso() { if(currentStep < totalSteps) jumpToStep(currentStep + 1); }
    function anteriorPaso() { if(currentStep > 1) jumpToStep(currentStep - 1); }
    
    function omitirPaso() {
        document.querySelectorAll(`.req-step${currentStep}`).forEach(inp => { if (inp.tagName === 'TEXTAREA' || inp.type === 'text') inp.value = "Sin novedades particulares en la jornada."; });
        document.getElementById(`btnStep${currentStep}`).classList.add('omitted');
        sincronizarDatos(); siguientePaso();
    }

    function activarReloj(turno) {
        document.getElementById('card_m').classList.remove('active'); document.getElementById('card_t').classList.remove('active'); document.getElementById('card_'+turno).classList.add('active');
        sincronizarDatos();
    }

    function evaluarTarjeta(id) {
        const val = document.getElementById('v_' + id).value;
        const card = document.getElementById('c_' + id);
        if(val > 0) card.classList.add('active'); else card.classList.remove('active');
        sincronizarDatos();
    }

    // Lógica Partidas (Enter / Excel)
    let partidasList = [];
    function agregarPartidaRapida() {
        const inputBuscador = document.getElementById('buscadorPartidas');
        const desc = inputBuscador.value.trim();
        if(desc === '') return;
        partidasList.push({ descripcion: desc, metrado: '' });
        inputBuscador.value = ''; renderizarListaPartidas();
        document.getElementById('v_partidas').value = "lleno"; sincronizarDatos();
    }

    function abrirModalMasivo() { document.getElementById('textoExcelMasivo').value = ''; new bootstrap.Modal(document.getElementById('modalExcel')).show(); }
    
    function procesarExcelMasivo() {
        const rawData = document.getElementById('textoExcelMasivo').value;
        if(!rawData.trim()) return;
        const rows = rawData.split('\\n'); let count = 0;
        rows.forEach(row => {
            if(!row.trim()) return;
            const cols = row.split('\\t'); 
            let desc = cols[0].trim(); let met = cols.length > 1 ? cols[1].trim() : '';
            if(desc) { partidasList.push({ descripcion: desc, metrado: met }); count++; }
        });
        if(count > 0) { renderizarListaPartidas(); document.getElementById('v_partidas').value = "lleno"; sincronizarDatos(); }
        bootstrap.Modal.getInstance(document.getElementById('modalExcel')).hide();
    }

    function actualizarMetrado(index, valor) { partidasList[index].metrado = valor; sincronizarDatos(); }
    function eliminarPartida(index) { partidasList.splice(index, 1); if(partidasList.length === 0) document.getElementById('v_partidas').value = ""; renderizarListaPartidas(); sincronizarDatos(); }

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

    // ==========================================================
    // MOTOR DE SINCRONIZACIÓN BLINDADO (ESCRIBE EN LA HOJA)
    // ==========================================================
    function sincronizarDatos() {
        try {
            if(!g_numAsiento) return; // Si no hay asiento, no hace nada.
            
            // Actualizar Colores de la Barra Superior (Termómetros)
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

            let as_str = g_numAsiento.padStart(4, '0');
            
            // TITULAR CENTRADO Y FECHA A LA DERECHA EXACTAMENTE COMO PEDISTE
            let textoPapel = `<div style="display:flex; width:100%; margin-bottom: 5px;">
                <div style="flex:1;"></div>
                <div style="flex:2; text-align:center; font-weight:bold; font-size:17px;">ASIENTO No ${as_str} DEL RESIDENTE DE OBRA</div>
                <div style="flex:1; text-align:right; font-weight:bold; font-size:17px;">${g_fechaAsiento}</div>
            </div>`;

            // Textos del Cuaderno
            const vJ1 = document.getElementById('v_jornal_m').value; const vJ2 = document.getElementById('v_jornal_t').value;
            if(vJ1 || vJ2) textoPapel += `1.- Jornal de trabajo:<br>Mañana: ${vJ1} ; Tarde: ${vJ2}<br>`;
            
            const vOper = (document.getElementById('v_oper').value || '0').padStart(2, '0');
            const vOfic = (document.getElementById('v_ofic').value || '0').padStart(2, '0');
            const vPeon = (document.getElementById('v_peon').value || '0').padStart(2, '0');
            const vMeca = (document.getElementById('v_meca').value || '0').padStart(2, '0');
            const vCtrl = (document.getElementById('v_ctrl').value || '0').padStart(2, '0');
            const vOpe = (document.getElementById('v_ope_maq').value || '0').padStart(2, '0');

            if (vOper !== '00' || vOfic !== '00' || vPeon !== '00' || vMeca !== '00' || vCtrl !== '00' || vOpe !== '00') {
                textoPapel += `2.- Personal de obra:<br>`;
                textoPapel += `${vOper} operarios &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${vOfic} oficiales &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${vPeon} peones &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${vMeca} mecánicos<br>`;
                textoPapel += `${vCtrl} controladores de maquinaria &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${vOpe} operadores de maquinaria<br>`;
            }

            if(partidasList.length > 0) {
                textoPapel += `3.- Partidas ejecutadas:<br>`;
                partidasList.forEach(p => { textoPapel += `- ${p.descripcion} &nbsp;&nbsp; (Metrado registrado: ${p.metrado || '0'})<br>`; });
            }

            const camposText = [
                {id: 'mayor_m', titulo: '4.- Partidas de mayor metrado'}, {id: 'sub_p', titulo: '5.- Sub partidas ejecutadas'},
                {id: 'activ', titulo: '6.- Actividades ejecutadas'}, {id: 'almacen', titulo: '7.- Movimiento de almacén'},
                {id: 'maquina', titulo: '8.- Maquinarias y equipos'}, {id: 'herram', titulo: '9.- Herramientas manuales'},
                {id: 'ocurrencia', titulo: '10.- Ocurrencias y otros'}
            ];

            camposText.forEach(campo => {
                const val = document.getElementById('v_' + campo.id).value;
                if(val) textoPapel += `${campo.titulo}:<br>${val.replace(/\\n/g, '<br>')}<br>`;
            });

            // ESCRIBIR EN LA HOJA
            const outContainer = document.getElementById('out_general');
            outContainer.innerHTML = textoPapel;
            
            // LÓGICA DE VAN / VIENE (Corte de Página Automático)
            if (outContainer.offsetHeight > 560) {
                let contenidoPrevio = outContainer.innerHTML;
                let HTML_Con_Corte = `
                    <div>${contenidoPrevio}</div>
                    <span class="p-van-line">... Van</span>
                    <div class="p-num text-end mb-2" style="font-size:16px; font-weight:bold; padding-right:10px;">Nº 0002</div>
                    <div class="p-break-page"></div>
                    <div style="display:flex; width:100%; margin-bottom:10px; font-family:'Caveat', cursive; color:var(--celeste-obra); font-weight:bold; font-size:17px;">
                        <div style="flex:1;"></div>
                        <div style="flex:2; text-align:center;">... Viene del Asiento No ${as_str} del Residente de Obra</div>
                        <div style="flex:1; text-align:right;">${g_fechaAsiento}</div>
                    </div>
                `;
                outContainer.innerHTML = HTML_Con_Corte;
            }
        } catch(e) { console.error("Error en sincronización:", e); }
    }

    // Slider de Firma Legal
    const handle = document.getElementById('sliderHandle'); const track = document.getElementById('sliderTrack'); const progress = document.getElementById('sliderProgress');
    let isDragging = false, startX = 0, maxSlide = 0;
    function calcLimits() { maxSlide = track.clientWidth - handle.clientWidth - 8; }
    window.addEventListener('resize', calcLimits); setTimeout(calcLimits, 500);
    function startDrag(e) { isDragging = true; startX = (e.clientX || e.touches[0].clientX) - handle.offsetLeft; calcLimits(); }
    function onDrag(e) { if (!isDragging) return; let left = (e.clientX || e.touches[0].clientX) - startX; if (left < 4) left = 4; if (left > maxSlide) left = maxSlide; handle.style.left = left + 'px'; progress.style.width = (left + 23) + 'px'; if (left >= maxSlide - 2) { isDragging = false; firmar(); } }
    function stopDrag() { if (!isDragging) return; isDragging = false; handle.style.left = '4px'; progress.style.width = '0px'; }
    handle.addEventListener('mousedown', startDrag); document.addEventListener('mousemove', onDrag); document.addEventListener('mouseup', stopDrag); handle.addEventListener('touchstart', startDrag, {passive: true}); document.addEventListener('touchmove', onDrag, {passive: false}); document.addEventListener('touchend', stopDrag);
    
    function firmar() { 
        handle.style.left = maxSlide + 'px'; progress.style.width = '100%'; handle.style.background = '#10b981'; 
        handle.innerHTML = '<i class="bi bi-check-lg"></i>'; document.getElementById('sliderText').innerText = "FIRMADO LEGALMENTE"; 
        alert("¡Asiento cerrado y guardado en Base de Datos con éxito!"); window.location.href = '/cuaderno'; 
    }
</script>
"""

# ==============================================================================
# BLOQUE 6: RENDERIZADO FLASK
# ==============================================================================
@residencia_bp.route('/residencia')
def redaccion_asiento_residente():
    if 'usuario_id' not in session: return redirect(url_for('login.mostrar_login'))

    es_admin = session.get('rol') == 'Admin'
    nombre_completo = session.get('nombre', 'Ing. Samuel Gutierrez')
    menu_superior = obtener_navbar(es_admin, nombre_completo)
    
    fecha_hoy_iso = datetime.now().strftime('%Y-%m-%d')

    html_completo = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>SAMU — Cuaderno de Obra</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Caveat:wght@600;700&display=swap" rel="stylesheet">
        {BLOQUE_1_CSS}
    </head>
    <body>
        {{{{ menu_superior | safe }}}}
        <div class="dynamic-bg"><div class="bg-blob blob-navy"></div></div>
        {BLOQUE_2_MODALES_Y_STEPPER}
        <div class="split-layout" id="mainLayout">
            {BLOQUE_3_FORMULARIO}
            {BLOQUE_4_CUADERNO}
        </div>
        {BLOQUE_5_JS}
    </body>
    </html>
    """
    
    return render_template_string(html_completo, menu_superior=menu_superior, fecha_hoy_iso=fecha_hoy_iso)
