# =========================================================
# vistas_residencia.py
# Módulo: Stepper Dinámico, Live Preview y Maniquíes Animados
# =========================================================

from flask import Blueprint, render_template_string, session, redirect, url_for
from navbar import obtener_navbar
from datetime import datetime

residencia_bp = Blueprint('residencia', __name__)

BLOQUE_1_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&display=swap');
    :root { --apple-text: #1d1d1f; --celeste-obra: #0263a0; --nav-height: 52px; }
    
    body { font-family: 'Inter', sans-serif; color: var(--apple-text); overflow-x: hidden; padding-bottom: 90px; margin: 0;
           background: linear-gradient(135deg, rgba(255,255,255,1) 0%, rgba(2,99,160,0.1) 40%, rgba(135,206,235,0.15) 70%, rgba(249,168,212,0.15) 100%);
           background-attachment: fixed; }
    
    /* Animaciones Flotantes (Entrada y Salida) */
    @keyframes floatUp { from { opacity: 0; transform: translateY(40px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes floatDown { from { opacity: 1; transform: translateY(0); } to { opacity: 0; transform: translateY(40px); display: none; } }
    
    .stepper-container { position: fixed; top: var(--nav-height); left: 0; width: 100%; background: rgba(255,255,255,0.85); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(0,0,0,0.08); z-index: 900; padding: 12px 20px; overflow-x: auto; white-space: nowrap; display: flex; gap: 12px; scroll-behavior: smooth; -ms-overflow-style: none; scrollbar-width: none; }
    .stepper-container::-webkit-scrollbar { display: none; }
    
    .step-btn { border: 1px solid #cbd5e1; border-radius: 30px; padding: 10px 20px; font-size: 12px; font-weight: 600; color: #475569; background: rgba(255,255,255,0.9); cursor: pointer; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
    .step-btn.active { background: #ffffff !important; color: #000000 !important; font-weight: 800 !important; transform: scale(1.08); box-shadow: 0 8px 20px rgba(0,0,0,0.08); border-color: #000000 !important; }
    .step-btn.omitted { background: #64748b !important; color: white !important; border-color: #475569 !important; }

    #globalTooltip { position: fixed; background: #ffffff; color: #1e293b; padding: 8px 16px; border-radius: 10px; font-size: 12px; font-weight: 700; white-space: nowrap; border: 1px solid #e2e8f0; box-shadow: 0 10px 25px rgba(0,0,0,0.15); pointer-events: none; z-index: 999999; opacity: 0; transition: opacity 0.15s ease; }

    .split-layout { display: flex; gap: 40px; max-width: 1500px; margin: 140px auto 0 auto; padding: 0 20px; align-items: flex-start; }
    .form-column { flex: 1; max-width: 600px; }
    .preview-column { flex: 1; position: sticky; top: 140px; height: calc(100vh - 240px); overflow-y: auto; }
    
    /* Controladores de Vistas */
    .step-view { display: none; background: rgba(255,255,255,0.85); backdrop-filter: blur(25px); padding: 30px; border-radius: 20px; box-shadow: 0 4px 25px rgba(0,0,0,0.04); border: 1px solid rgba(255,255,255,1);}
    .step-view.active { display: block; animation: floatUp 0.35s cubic-bezier(0.4, 0, 0.2, 1) forwards; }
    .step-view.exit { display: block; animation: floatDown 0.3s cubic-bezier(0.4, 0, 0.2, 1) forwards; }
    
    .step-title { font-size: 22px; font-weight: 800; margin-bottom: 25px; color: #0f172a; letter-spacing: -0.5px;}
    .form-label { font-size: 12px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px;}
    .form-control, .form-select { border-radius: 12px; border: 1px solid #cbd5e1; padding: 12px 14px; font-size: 14px; background: rgba(255,255,255,0.9); font-weight: 500;}
    .form-control:focus, .form-select:focus { border-color: #0066cc; box-shadow: 0 0 0 4px rgba(0,102,204,0.15); }

    .time-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 15px; display: flex; align-items: center; gap: 15px; transition: all 0.3s; cursor: pointer;}
    .time-card.active { border-color: var(--celeste-obra); background: #f0f9ff; }
    .clock-icon { font-size: 28px; color: #94a3b8; transition: color 0.3s; }
    .time-card.active .clock-icon { color: var(--celeste-obra); }

    /* ==========================================
       MANIQUÍES DINÁMICOS CON CASCO (NUEVO)
       ========================================== */
    @keyframes workingBounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
    
    .mannequin-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 15px 10px; text-align: center; transition: all 0.3s; display: flex; flex-direction: column; align-items: center;}
    .mannequin-card.active { border-color: #f59e0b; background: #fffbeb; box-shadow: 0 5px 15px rgba(245,158,11,0.1); }
    .mannequin-card input { border: none; background: transparent; text-align: center; font-weight: 800; font-size: 20px; width: 100%; margin-top: 5px; color: #000; padding: 0;}
    .mannequin-card input:focus { outline: none; }
    
    .m-fig { width: 40px; height: 50px; position: relative; transition: all 0.3s; }
    .m-fig.working { animation: workingBounce 0.8s infinite ease-in-out; } /* Animación al ingresar datos */
    
    .m-head { width: 24px; height: 24px; background: #fcd34d; border-radius: 50%; position: absolute; top: 8px; left: 50%; transform: translateX(-50%); z-index: 1;}
    .m-helmet { width: 28px; height: 16px; border-radius: 14px 14px 0 0; position: absolute; top: 4px; left: 50%; transform: translateX(-50%); z-index: 2; border-bottom: 2px solid rgba(0,0,0,0.1);}
    .m-body { width: 36px; height: 20px; background: #94a3b8; border-radius: 10px 10px 4px 4px; position: absolute; bottom: 0; left: 50%; transform: translateX(-50%); z-index: 0;}
    
    .mannequin-card.active .m-body { background: #0f172a; } /* Cuerpo cambia de color al activar */

    /* Colores Jerárquicos de Cascos */
    .helmet-white { background: #ffffff; border: 1px solid #cbd5e1; }
    .helmet-blue { background: #3b82f6; }
    .helmet-yellow { background: #eab308; }
    .helmet-orange { background: #f97316; }
    .helmet-green { background: #22c55e; }
    .helmet-red { background: #ef4444; }

    /* Cuaderno Físico */
    .papel-fisico { background: #fdfdfa; width: 100%; min-height: 950px; padding: 40px 50px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; font-family: Arial, sans-serif; color: #000; position: relative;}
    .p-header-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 5px; }
    .p-title-box { text-align: center; flex: 1; margin-left: 50px;}
    .p-title-box h1 { font-size: 26px; font-weight: bold; text-decoration: underline; letter-spacing: 1px; margin: 0; color: #000;}
    .p-num { font-size: 22px; font-weight: bold; margin-top: 5px; color: #000;}
    .p-sello { width: 90px; height: 90px; border: 2px dashed #94a3b8; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 11px; color: #94a3b8; text-align: center; padding: 5px; opacity: 0.5; margin-top: -20px;}
    .p-meta { margin-bottom: 10px; padding-bottom: 10px; border-bottom: 3px solid #000; }
    .p-row { display: flex; align-items: flex-end; margin-bottom: 6px; }
    .p-label { font-size: 14px; font-weight: bold; margin-right: 8px; color: #000; white-space: nowrap; }
    .p-line { flex: 1; border-bottom: 1px solid #000; position: relative; height: 20px; }
    .lapicero-meta { position: absolute; bottom: -1px; left: 10px; font-family: 'Caveat', cursive; color: var(--celeste-obra); font-size: 18px; font-weight: 700; white-space: nowrap; }
    .p-body-lines { background-image: repeating-linear-gradient(transparent, transparent 23px, #94a3b8 24px); line-height: 24px; min-height: 650px; padding-top: 5px; position: relative; margin-top: 10px;}
    .lapicero { font-family: 'Caveat', cursive; color: var(--celeste-obra); font-size: 16px; line-height: 24px; padding-left: 5px; font-weight: 700; }
    .lapicero-muted { font-family: 'Caveat', cursive; color: #64748b; font-size: 16px; padding-left: 20px; font-weight: 600;}
    .p-van { position: absolute; bottom: 0; right: 10px; font-family: 'Caveat', cursive; color: var(--celeste-obra); font-size: 18px; font-weight: 700;}
    .p-footer { display: flex; justify-content: space-between; margin-top: 60px; font-size: 12px; font-weight: bold; color: #000;}
    .p-sig { border-top: 1px solid #000; width: 28%; text-align: center; padding-top: 5px; }

    /* Barra Inferior (Reordenada y Animada) */
    .bottom-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(255,255,255,0.95); backdrop-filter: blur(15px); border-top: 1px solid rgba(0,0,0,0.08); padding: 15px 30px; z-index: 900; display: flex; justify-content: space-between; align-items: center; }
    .slider-track { width: 100%; max-width: 400px; height: 60px; background: rgba(0,0,0,0.05); border-radius: 30px; position: relative; display: flex; align-items: center; justify-content: center; overflow: hidden; margin: 0 auto; border: 1px solid rgba(0,0,0,0.05);}
    .slider-text { font-size: 13px; font-weight: 800; color: #64748b; text-transform: uppercase; z-index: 1; pointer-events: none;}
    .slider-handle { width: 52px; height: 52px; background: #000; color: #fff; border-radius: 50%; position: absolute; left: 4px; display: flex; align-items: center; justify-content: center; z-index: 2; cursor: grab;}
    .slider-progress { position: absolute; left: 0; top: 0; height: 100%; background: rgba(0, 102, 204, 0.1); width: 0; pointer-events: none; }

    @media (max-width: 1024px) { .split-layout { flex-direction: column; align-items: center; margin-top: 130px; padding: 0 10px;} .form-column { width: 100%; max-width: 100%; } .preview-column { display: none; } .bottom-bar { padding: 15px; } .bottom-bar .btn { padding-left: 15px !important; padding-right: 15px !important; font-size: 13px; } }
</style>
"""

BLOQUE_2_STEPPER = """
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
"""

BLOQUE_3_FORMULARIO = """
<div class="form-column">
    <div class="d-flex justify-content-between mb-3 px-2">
        <h6 class="text-primary fw-bold mb-0">Asiento N° {{ numero_asiento }}</h6>
        <span class="text-muted small fw-bold">{{ fecha_hoy }}</span>
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
            <p class="text-muted small mb-3">Asigna personal para verlos en acción en la obra.</p>
            <div class="row g-2">
                <div class="col-4"><div class="mannequin-card" id="c_oper"><div class="m-fig" id="fig_oper"><div class="m-helmet helmet-white"></div><div class="m-head"></div><div class="m-body"></div></div><span class="form-label d-block mt-2" style="font-size:10px;">Operarios</span><input type="number" class="req-step2" id="v_oper" placeholder="0" oninput="animarManiqui('oper')"></div></div>
                <div class="col-4"><div class="mannequin-card" id="c_ofic"><div class="m-fig" id="fig_ofic"><div class="m-helmet helmet-blue"></div><div class="m-head"></div><div class="m-body"></div></div><span class="form-label d-block mt-2" style="font-size:10px;">Oficiales</span><input type="number" class="req-step2" id="v_ofic" placeholder="0" oninput="animarManiqui('ofic')"></div></div>
                <div class="col-4"><div class="mannequin-card" id="c_peon"><div class="m-fig" id="fig_peon"><div class="m-helmet helmet-yellow"></div><div class="m-head"></div><div class="m-body"></div></div><span class="form-label d-block mt-2" style="font-size:10px;">Peones</span><input type="number" class="req-step2" id="v_peon" placeholder="0" oninput="animarManiqui('peon')"></div></div>
                <div class="col-4"><div class="mannequin-card" id="c_meca"><div class="m-fig" id="fig_meca"><div class="m-helmet helmet-orange"></div><div class="m-head"></div><div class="m-body"></div></div><span class="form-label d-block mt-2" style="font-size:10px;">Mecánicos</span><input type="number" class="req-step2" id="v_meca" placeholder="0" oninput="animarManiqui('meca')"></div></div>
                <div class="col-4"><div class="mannequin-card" id="c_ctrl"><div class="m-fig" id="fig_ctrl"><div class="m-helmet helmet-green"></div><div class="m-head"></div><div class="m-body"></div></div><span class="form-label d-block mt-2" style="font-size:10px;">Controladores</span><input type="number" class="req-step2" id="v_ctrl" placeholder="0" oninput="animarManiqui('ctrl')"></div></div>
                <div class="col-4"><div class="mannequin-card" id="c_ope_maq"><div class="m-fig" id="fig_ope_maq"><div class="m-helmet helmet-red"></div><div class="m-head"></div><div class="m-body"></div></div><span class="form-label d-block mt-2" style="font-size:10px;">Operadores</span><input type="number" class="req-step2" id="v_ope_maq" placeholder="0" oninput="animarManiqui('ope_maq')"></div></div>
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
        <div class="step-view" id="step8"><div class="step-title">8.- Maquinarias</div><textarea class="form-control req-step8" id="v_maquina" rows="6" placeholder="Maquinarias..."></textarea></div>
        <div class="step-view" id="step9"><div class="step-title">9.- Herramientas</div><textarea class="form-control req-step9" id="v_herram" rows="4" placeholder="Herramientas..."></textarea></div>
        <div class="step-view" id="step10"><div class="step-title text-danger">10.- Ocurrencias</div><textarea class="form-control border-danger req-step10" id="v_ocurrencia" rows="8" placeholder="Ocurrencias legales..."></textarea></div>

        <div class="step-view" id="step11">
            <div class="step-title text-success text-center mb-4"><i class="bi bi-shield-check"></i> Listo para Firmar</div>
            <p class="text-center text-muted small mb-5">Verifica la hoja a la derecha. Al deslizar el candado, los datos quedarán inmutables.</p>
            <div class="slider-track" id="sliderTrack"><div class="slider-progress" id="sliderProgress"></div><div class="slider-text" id="sliderText">Deslizar para Firmar</div><div class="slider-handle" id="sliderHandle"><i class="bi bi-lock-fill" style="font-size: 1.2rem;"></i></div></div>
        </div>
    </form>
</div>
"""

BLOQUE_4_CUADERNO_FISICO = """
<div class="preview-column">
    <div class="papel-fisico" id="papelOficial">
        <div class="p-header-top">
            <div style="width: 90px;"></div>
            <div class="p-title-box"><h1>CUADERNO DE OBRA</h1></div>
            <div style="text-align: right; width: 110px;"><div class="p-num">Nº <span style="font-size: 26px; margin-left:5px;">{{ numero_asiento }}</span></div><div class="p-sello">Sello Juzgado<br>Paz Letrado</div></div>
        </div>
        
        <div class="p-meta">
            <div class="d-flex w-100 mb-1">
                <div class="d-flex" style="flex: 0.5;"><span class="p-label">Fecha:</span><div class="p-line"><span class="lapicero-meta">{{ fecha_hoy }}</span></div></div>
                <div class="d-flex" style="flex: 0.5; margin-left: 15px;"><span class="p-label">Modalidad:</span><div class="p-line"><span class="lapicero-meta">Administración Directa</span></div></div>
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
            <div class="p-sig">ING. INSPECTOR</div><div class="p-sig">ING. RESIDENTE</div><div class="p-sig">ING. SUPERVISOR</div>
        </div>
    </div>
</div>

<div class="modal fade" id="modalExcel" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content" style="border-radius: 20px;">
            <div class="modal-header border-0 pb-0"><h5 class="modal-title fw-bold text-success"><i class="bi bi-file-earmark-spreadsheet"></i> Pegado Masivo (Excel)</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
            <div class="modal-body">
                <p class="small text-muted mb-2">Copia las filas desde tu Excel (<b>Descripción | Metrado</b>) y presiona <code>Ctrl + V</code>:</p>
                <textarea id="textoExcelMasivo" class="form-control" rows="8" placeholder="Pega aquí las filas copiadas..."></textarea>
            </div>
            <div class="modal-footer border-0 pt-0">
                <button type="button" class="btn btn-light rounded-pill px-4" data-bs-dismiss="modal">Cancelar</button>
                <button type="button" class="btn btn-success rounded-pill px-4 fw-bold" onclick="procesarExcelMasivo()">Importar Datos</button>
            </div>
        </div>
    </div>
</div>
"""

BLOQUE_5_JS = """
<div class="bottom-bar shadow-lg">
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
    let currentStep = 1;
    const totalSteps = 11;
    let isAnimating = false; // Bloquea clics dobles mientras flota la pantalla

    const gTooltip = document.getElementById('globalTooltip');
    document.querySelectorAll('.step-btn').forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            gTooltip.innerText = btn.getAttribute('data-tooltip');
            gTooltip.style.left = (e.clientX + 15) + 'px'; gTooltip.style.top = (e.clientY + 15) + 'px';
            gTooltip.style.opacity = '1';
        });
        btn.addEventListener('mouseleave', () => { gTooltip.style.opacity = '0'; });
    });
    
    // NAVEGACIÓN Y FLOAT ANIMATION
    function jumpToStep(stepIndex) {
        if (isAnimating || currentStep === stepIndex) return;
        isAnimating = true;

        document.getElementById('indicadorGuardado').innerHTML = '<i class="bi bi-check2-all text-success"></i> Guardado';
        setTimeout(() => { document.getElementById('indicadorGuardado').innerHTML = '<i class="bi bi-cloud-arrow-up"></i> Autoguardado'; }, 2000);

        const currentView = document.getElementById(`step${currentStep}`);
        currentView.classList.remove('active');
        currentView.classList.add('exit'); // Inicia Float Down
        document.getElementById(`btnStep${currentStep}`).classList.remove('active');
        
        setTimeout(() => {
            currentView.classList.remove('exit'); // Lo oculta de verdad
            currentStep = stepIndex;
            const nextView = document.getElementById(`step${currentStep}`);
            nextView.classList.add('active'); // Inicia Float Up
            
            document.getElementById(`btnStep${currentStep}`).classList.add('active');
            document.getElementById('stepperBar').scrollLeft = document.getElementById(`btnStep${currentStep}`).offsetLeft - 50;

            const btnAtras = document.getElementById('btnAtras');
            if (currentStep > 1) btnAtras.classList.remove('d-none'); else btnAtras.classList.add('d-none');

            if (currentStep === 11) {
                document.querySelector('.bottom-bar').style.display = 'none';
                document.querySelector('.preview-column').style.display = 'block';
            } else {
                document.querySelector('.bottom-bar').style.display = 'flex';
                if(window.innerWidth <= 1024) document.querySelector('.preview-column').style.display = 'none';
            }
            sincronizarDatos();
            isAnimating = false;
        }, 300); // 300ms espera a que termine la salida
    }

    function siguientePaso() { if(currentStep < totalSteps) jumpToStep(currentStep + 1); }
    function anteriorPaso() { if(currentStep > 1) jumpToStep(currentStep - 1); }
    
    function omitirPaso() {
        document.querySelectorAll(`.req-step${currentStep}`).forEach(inp => { if (inp.tagName === 'TEXTAREA' || inp.type === 'text') inp.value = "Sin novedad en la jornada."; });
        document.getElementById(`btnStep${currentStep}`).classList.add('omitted');
        sincronizarDatos(); siguientePaso();
    }

    function activarReloj(turno) {
        document.getElementById('card_m').classList.remove('active'); document.getElementById('card_t').classList.remove('active');
        document.getElementById('card_'+turno).classList.add('active');
    }

    // ANIMACIÓN DE MANIQUÍES (PASO 2)
    function animarManiqui(id) {
        const val = document.getElementById('v_' + id).value;
        const fig = document.getElementById('fig_' + id);
        const card = document.getElementById('c_' + id);
        if(val > 0) {
            fig.classList.add('working');
            card.classList.add('active');
        } else {
            fig.classList.remove('working');
            card.classList.remove('active');
        }
        sincronizarDatos();
    }

    // LISTA DE PARTIDAS
    let partidasList = [];
    function agregarPartidaRapida() {
        const inputBuscador = document.getElementById('buscadorPartidas');
        const desc = inputBuscador.value.trim();
        if(desc === '') return;
        partidasList.push({ descripcion: desc, metrado: '' });
        inputBuscador.value = ''; 
        renderizarListaPartidas();
        document.getElementById('v_partidas').value = "lleno"; 
        sincronizarDatos();
    }

    function abrirModalMasivo() { document.getElementById('textoExcelMasivo').value = ''; new bootstrap.Modal(document.getElementById('modalExcel')).show(); }
    
    function procesarExcelMasivo() {
        const rawData = document.getElementById('textoExcelMasivo').value;
        if(!rawData.trim()) return;
        const rows = rawData.split('\\n');
        let count = 0;
        rows.forEach(row => {
            if(!row.trim()) return;
            const cols = row.split('\\t'); 
            let desc = cols[0].trim();
            let met = cols.length > 1 ? cols[1].trim() : '';
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

        let numAsiento = "{{ numero_asiento }}"; let fechaLarga = "{{ fecha_hoy }}";
        let textoPapel = `&nbsp;&nbsp;Asiento N° ${numAsiento} del Residente de Obra &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${fechaLarga}<br>`;

        const vJ1 = document.getElementById('v_jornal_m').value; const vJ2 = document.getElementById('v_jornal_t').value;
        if(vJ1 || vJ2) textoPapel += `1.- Jornal de trabajo<br>Mañana: ${vJ1} ; Tarde: ${vJ2}<br>`;
        
        const vOper = (document.getElementById('v_oper').value || '0').padStart(2, '0');
        const vOfic = (document.getElementById('v_ofic').value || '0').padStart(2, '0');
        const vPeon = (document.getElementById('v_peon').value || '0').padStart(2, '0');
        const vMeca = (document.getElementById('v_meca').value || '0').padStart(2, '0');
        const vCtrl = (document.getElementById('v_ctrl').value || '0').padStart(2, '0');
        const vOpe = (document.getElementById('v_ope_maq').value || '0').padStart(2, '0');
        textoPapel += `2.- Personal de obra:<br>${vOper} operarios &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${vOfic} oficiales &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${vPeon} peones &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${vMeca} mecánicos<br>${vCtrl} controladores maq. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${vOpe} operadores maq.<br>`;

        if(partidasList.length > 0) {
            textoPapel += `3.- Partidas ejecutadas<br>`;
            partidasList.forEach(p => { textoPapel += `- ${p.descripcion} &nbsp;&nbsp;&nbsp; (Metrado: ${p.metrado || '0'})<br>`; });
        }

        const camposText = [{id: 'mayor_m', titulo: '4.- Partidas de mayor metrado'}, {id: 'sub_p', titulo: '5.- Sub partidas ejecutadas'}, {id: 'activ', titulo: '6.- Actividades ejecutadas'}, {id: 'almacen', titulo: '7.- Movimiento de almacén'}, {id: 'maquina', titulo: '8.- Maquinarias y equipos'}, {id: 'herram', titulo: '9.- Herramientas manuales'}, {id: 'ocurrencia', titulo: '10.- Ocurrencias y otros'}];
        camposText.forEach(campo => { const val = document.getElementById('v_' + campo.id).value; if(val) textoPapel += `${campo.titulo}<br>${val.replace(/\\n/g, '<br>')}<br>`; });
        
        document.getElementById('out_general').innerHTML = textoPapel;
        if (document.querySelector('.p-body-lines').scrollHeight > 650) document.getElementById('indicadorVan').style.display = 'block'; else document.getElementById('indicadorVan').style.display = 'none';
    }

    const handle = document.getElementById('sliderHandle'); const track = document.getElementById('sliderTrack'); const progress = document.getElementById('sliderProgress');
    let isDragging = false, startX = 0, maxSlide = 0;
    function calcLimits() { maxSlide = track.clientWidth - handle.clientWidth - 8; }
    window.addEventListener('resize', calcLimits); setTimeout(calcLimits, 500);
    function startDrag(e) { isDragging = true; startX = (e.clientX || e.touches[0].clientX) - handle.offsetLeft; calcLimits(); }
    function onDrag(e) { if (!isDragging) return; let left = (e.clientX || e.touches[0].clientX) - startX; if (left < 4) left = 4; if (left > maxSlide) left = maxSlide; handle.style.left = left + 'px'; progress.style.width = (left + 23) + 'px'; if (left >= maxSlide - 2) { isDragging = false; firmar(); } }
    function stopDrag() { if (!isDragging) return; isDragging = false; handle.style.left = '4px'; progress.style.width = '0px'; }
    handle.addEventListener('mousedown', startDrag); document.addEventListener('mousemove', onDrag); document.addEventListener('mouseup', stopDrag); handle.addEventListener('touchstart', startDrag, {passive: true}); document.addEventListener('touchmove', onDrag, {passive: false}); document.addEventListener('touchend', stopDrag);
    function firmar() { handle.style.left = maxSlide + 'px'; progress.style.width = '100%'; handle.style.background = '#10b981'; handle.innerHTML = '<i class="bi bi-check-lg"></i>'; document.getElementById('sliderText').innerText = "FIRMADO LEGALMENTE"; alert("¡Asiento N° 0088 firmado con éxito!"); window.location.href = '/cuaderno'; }
    sincronizarDatos();
</script>
"""

# ==============================================================================
# BLOQUE 6: RENDERIZADO FINAL
# ==============================================================================
@residencia_bp.route('/residencia')
def redaccion_asiento_residente():
    if 'usuario_id' not in session: return redirect(url_for('login.mostrar_login'))

    es_admin = session.get('rol') == 'Admin'
    nombre_completo = session.get('nombre', 'Ing. Samuel Gutierrez')
    menu_superior = obtener_navbar(es_admin, nombre_completo)
    numero_asiento = "0088"
    dias = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO", "DOMINGO"]
    fecha_dt = datetime.now()
    fecha_hoy = f"{dias[fecha_dt.weekday()]}, {fecha_dt.strftime('%d/%m/%Y')}"

    html_completo = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>SAMU — Asiento N° {numero_asiento}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Caveat:wght@600;700&display=swap" rel="stylesheet">
        {BLOQUE_1_CSS}
    </head>
    <body>
        {{{{ menu_superior | safe }}}}
        {BLOQUE_2_STEPPER}
        <div class="split-layout">
            {BLOQUE_3_FORMULARIO}
            {BLOQUE_4_CUADERNO_FISICO}
        </div>
        {BLOQUE_5_JS}
    </body>
    </html>
    """
    return render_template_string(html_completo, menu_superior=menu_superior, numero_asiento=numero_asiento, fecha_hoy=fecha_hoy)

