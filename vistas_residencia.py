# =========================================================
# vistas_residencia.py
# Arquitectura Modular: Formularios por Pasos + Live Preview Físico
# =========================================================

from flask import Blueprint, render_template_string, session, redirect, url_for
from navbar import obtener_navbar
from datetime import datetime

residencia_bp = Blueprint('residencia', __name__)

# ==============================================================================
# BLOQUE 1: ESTILOS CSS (DISEÑO, COLORES Y FORMATO EXACTO DEL CUADERNO FÍSICO)
# ==============================================================================
BLOQUE_1_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&display=swap');
    
    :root { --apple-text: #1d1d1f; --bg-color: #fbfbfd; --nav-height: 52px; --celeste-obra: #0263a0; }
    body { font-family: 'Inter', sans-serif; background-color: var(--bg-color); color: var(--apple-text); overflow-x: hidden; padding-bottom: 90px;}
    
    .dynamic-bg { position: fixed; inset: 0; z-index: -2; background: #fbfbfd; overflow: hidden; }
    .bg-blob { position: absolute; border-radius: 50%; filter: blur(100px); pointer-events: none; }
    .blob-navy { width: 60vw; height: 60vw; background: #0f172a; opacity: 0.08; top: -10%; left: -10%; animation: movAzul 22s infinite alternate; }
    
    /* --- STEPPER SUPERIOR --- */
    .stepper-container {
        position: fixed; top: var(--nav-height); left: 0; width: 100%;
        background: rgba(255,255,255,0.95); backdrop-filter: blur(15px);
        border-bottom: 1px solid rgba(0,0,0,0.08); z-index: 900;
        padding: 12px 20px; overflow-x: auto; white-space: nowrap;
        display: flex; gap: 12px; scroll-behavior: smooth;
        -ms-overflow-style: none; scrollbar-width: none; 
    }
    .stepper-container::-webkit-scrollbar { display: none; }
    
    .step-btn {
        border: 1px solid #cbd5e1; border-radius: 30px; padding: 10px 20px;
        font-size: 12px; font-weight: 600; color: #475569; background: #f8fafc;
        cursor: pointer; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); 
    }
    .step-btn.active { 
        background: #ffffff !important; color: #000000 !important; font-weight: 800 !important; 
        transform: scale(1.08); box-shadow: 0 8px 20px rgba(0,0,0,0.08); border-color: #000000 !important;
    }

    /* Tooltip Global */
    #globalTooltip {
        position: fixed; background: #ffffff; color: #1e293b; padding: 8px 16px;
        border-radius: 10px; font-size: 12px; font-weight: 700; white-space: nowrap;
        border: 1px solid #e2e8f0; box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        pointer-events: none; z-index: 999999; opacity: 0; transition: opacity 0.15s ease;
    }

    /* --- FORMULARIOS --- */
    .split-layout { display: flex; gap: 40px; max-width: 1550px; margin: 140px auto 0 auto; padding: 0 20px; align-items: flex-start; }
    .form-column { flex: 1; max-width: 600px; }
    .preview-column { flex: 1; position: sticky; top: 140px; height: calc(100vh - 240px); overflow-y: auto; }
    
    .step-view { display: none; animation: fadeIn 0.4s ease; background: rgba(255,255,255,0.75); backdrop-filter: blur(20px); padding: 30px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.02); border: 1px solid rgba(255,255,255,0.9);}
    .step-view.active { display: block; }
    @keyframes fadeIn { from { opacity: 0; transform: translateX(-10px); } to { opacity: 1; transform: translateX(0); } }

    /* --- COMPONENTES DINÁMICOS: RELOJ Y CASCOS --- */
    .time-card {
        background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 15px;
        display: flex; align-items: center; gap: 15px; transition: all 0.3s;
    }
    .time-card:hover { border-color: var(--celeste-obra); box-shadow: 0 5px 15px rgba(2,99,160,0.1); }
    .clock-icon { font-size: 28px; color: #94a3b8; transition: color 0.3s; }
    .time-card.active .clock-icon { color: var(--celeste-obra); }

    .casco-card {
        background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 12px;
        text-align: center; transition: all 0.3s; position: relative; overflow: hidden;
    }
    .casco-card:hover { border-color: #f59e0b; transform: translateY(-3px); }
    .casco-card.active { border-color: #f59e0b; background: #fffbeb; }
    .casco-icon { font-size: 24px; color: #cbd5e1; transition: all 0.3s; }
    .casco-card.active .casco-icon { color: #f59e0b; transform: scale(1.2); }
    .casco-card input { border: none; background: transparent; text-align: center; font-weight: 800; font-size: 18px; width: 100%; margin-top: 5px; color: #000;}
    .casco-card input:focus { outline: none; }

    /* --- CUADERNO FÍSICO (AJUSTE DE ALINEACIÓN) --- */
    .papel-fisico {
        background: #fdfdfa; width: 100%; min-height: 950px; padding: 40px 50px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1); border: 1px solid #e2e8f0;
        font-family: Arial, sans-serif; color: #000; position: relative;
    }
    .p-meta { margin-bottom: 25px; }
    .p-row { display: flex; align-items: flex-end; margin-bottom: 10px; }
    .p-label { font-size: 13px; font-weight: bold; margin-right: 8px; color: #000; white-space: nowrap; }
    .p-line { flex: 1; border-bottom: 1px solid #000; position: relative; height: 18px; }
    
    .lapicero-meta { 
        position: absolute; bottom: -4px; left: 10px; 
        font-family: 'Caveat', cursive; color: var(--celeste-obra); 
        font-size: 20px; font-weight: 700; white-space: nowrap; 
    }
    
    .p-body-lines {
        background-image: repeating-linear-gradient(transparent, transparent 27px, #94a3b8 28px);
        line-height: 28px; min-height: 650px; padding-top: 2px; position: relative;
    }
    .lapicero { 
        font-family: 'Caveat', cursive; color: var(--celeste-obra); 
        font-size: 19px; /* Tamaño reducido como pediste */
        padding-left: 5px; margin-top: -3px; font-weight: 600;
    }
</style>
"""

# ==============================================================================
# BLOQUE 2: BARRA SUPERIOR (STEPPER TERMÓMETRO)
# ==============================================================================
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

# ==============================================================================
# BLOQUE 3: FORMULARIOS (COLUMNA IZQUIERDA)
# ==============================================================================
BLOQUE_3_FORMULARIO = """
<div class="form-column">
    <div class="d-flex justify-content-between mb-3 px-2">
        <h6 class="text-primary fw-bold mb-0">Asiento N° {{ numero_asiento }}</h6>
        <span class="text-muted small fw-bold">{{ fecha_hoy_texto_largo }}</span>
    </div>

    <form id="formResidencia" oninput="sincronizarDatos()">
        <div class="step-view active" id="step1">
            <div class="step-title">1.- JORNAL DE TRABAJO</div>
            <div class="row g-3">
                <div class="col-sm-6">
                    <div class="time-card" id="card_m">
                        <div class="clock-icon"><i class="bi bi-alarm"></i></div>
                        <div class="w-100">
                            <label class="form-label">Mañana (Inicio - Fin)</label>
                            <input type="text" class="form-control border-0 p-0 req-step1" id="v_jornal_m" value="07:00 - 12:00" onfocus="activarReloj('m')">
                        </div>
                    </div>
                </div>
                <div class="col-sm-6">
                    <div class="time-card" id="card_t">
                        <div class="clock-icon"><i class="bi bi-clock-history"></i></div>
                        <div class="w-100">
                            <label class="form-label">Tarde (Inicio - Fin)</label>
                            <input type="text" class="form-control border-0 p-0 req-step1" id="v_jornal_t" value="13:00 - 17:00" onfocus="activarReloj('t')">
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="step-view" id="step2">
            <div class="step-title">2.- PERSONAL DE OBRA</div>
            <div class="row g-2">
                <div class="col-4">
                    <div class="casco-card" id="c_oper">
                        <div class="casco-icon"><i class="bi bi-person-fill-gear"></i></div>
                        <span class="form-label d-block" style="font-size:9px;">Operarios</span>
                        <input type="number" class="req-step2" id="v_oper" placeholder="0">
                    </div>
                </div>
                <div class="col-4">
                    <div class="casco-card" id="c_ofic">
                        <div class="casco-icon"><i class="bi bi-person-fill-check"></i></div>
                        <span class="form-label d-block" style="font-size:9px;">Oficiales</span>
                        <input type="number" class="req-step2" id="v_ofic" placeholder="0">
                    </div>
                </div>
                <div class="col-4">
                    <div class="casco-card" id="c_peon">
                        <div class="casco-icon"><i class="bi bi-person-fill"></i></div>
                        <span class="form-label d-block" style="font-size:9px;">Peones</span>
                        <input type="number" class="req-step2" id="v_peon" placeholder="0">
                    </div>
                </div>
                <div class="col-4">
                    <div class="casco-card" id="c_meca">
                        <div class="casco-icon"><i class="bi bi-nut-fill"></i></div>
                        <span class="form-label d-block" style="font-size:9px;">Mecánicos</span>
                        <input type="number" class="req-step2" id="v_meca" placeholder="0">
                    </div>
                </div>
                <div class="col-4">
                    <div class="casco-card" id="c_ctrl">
                        <div class="casco-icon"><i class="bi bi-clipboard-data-fill"></i></div>
                        <span class="form-label d-block" style="font-size:9px;">Controladores</span>
                        <input type="number" class="req-step2" id="v_ctrl" placeholder="0">
                    </div>
                </div>
                <div class="col-4">
                    <div class="casco-card" id="c_ope_maq">
                        <div class="casco-icon"><i class="bi bi-truck-front-fill"></i></div>
                        <span class="form-label d-block" style="font-size:9px;">Operadores</span>
                        <input type="number" class="req-step2" id="v_ope_maq" placeholder="0">
                    </div>
                </div>
            </div>
        </div>

        <div class="step-view" id="step3"><div class="step-title">3. Partidas Ejecutadas</div><textarea class="form-control req-step3" id="v_partidas" rows="6" placeholder="Detalle partidas..."></textarea></div>
        <div class="step-view" id="step4"><div class="step-title">4. Partidas Mayor Metrado</div><textarea class="form-control req-step4" id="v_mayor_m" rows="6" placeholder="Detalle excedentes..."></textarea></div>
        <div class="step-view" id="step10"><div class="step-title text-danger">10. Ocurrencias</div><textarea class="form-control border-danger req-step10" id="v_ocurrencia" rows="8" placeholder="Ocurrencias legales..."></textarea></div>
    </form>
</div>
"""
# ==============================================================================
# BLOQUE 4: LIVE PREVIEW (HOJA DE CUADERNO FÍSICO EXACTA A LA FOTO)
# ==============================================================================
BLOQUE_4_CUADERNO_FISICO = """
<div class="preview-column">
    <div class="papel-fisico" id="papelOficial">
        
        <div class="p-header-top">
            <div style="width: 80px;"></div>
            <div class="p-title-box">
                <h1>CUADERNO DE OBRA</h1>
            </div>
            <div style="text-align: right; width: 110px;">
                <div class="p-num">Nº <span style="font-size: 32px; margin-left:5px;">{{ numero_asiento }}</span></div>
                <div class="p-sello">Sello Juzgado<br>Paz Letrado</div>
            </div>
        </div>
        
        <div class="p-meta">
            <div class="d-flex w-100 mb-2">
                <div class="d-flex" style="flex: 0.5;">
                    <span class="p-label">Fecha:</span>
                    <div class="p-line"><span class="lapicero-meta">{{ fecha_hoy_texto_largo }}</span></div>
                </div>
                <div class="d-flex" style="flex: 0.5; margin-left: 20px;">
                    <span class="p-label">Modalidad:</span>
                    <div class="p-line"><span class="lapicero-meta">ADMINISTRACIÓN DIRECTA</span></div>
                </div>
            </div>
            <div class="p-row"><span class="p-label">Obra:</span><div class="p-line"><span class="lapicero-meta">MEJORAMIENTO DE LA CARRETERA ASIRUNI - ROSASPATA</span></div></div>
            <div class="p-row"><span class="p-label">Proyecto:</span><div class="p-line"><span class="lapicero-meta">TRAMO I</span></div></div>
            <div class="p-row"><span class="p-label">Programa:</span><div class="p-line"><span class="lapicero-meta">-</span></div></div>
            <div class="p-row"><span class="p-label">Entidad Ejecutora:</span><div class="p-line"><span class="lapicero-meta">GOBIERNO REGIONAL PUNO</span></div></div>
        </div>

        <div class="p-body-lines">
            <div class="lapicero-muted" style="margin-bottom: 5px;">... Viene del ASIENTO Nº 87 DEL RESIDENTE DE OBRA </div>
            
            <div class="lapicero" id="out_general">
                </div>
            
            <div class="p-van" id="indicadorVan" style="display:none;">... Van</div>
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
# BLOQUE 5: JAVASCRIPT (LÓGICA DEL TEXTO FORMATO EXACTO Y TERMÓMETRO)
# ==============================================================================
BLOQUE_5_JS = """
<script>
    // ... (Mantener lógica de Tooltip y Navegación anterior)

    function activarReloj(turno) {
        document.getElementById('card_m').classList.remove('active');
        document.getElementById('card_t').classList.remove('active');
        document.getElementById('card_'+turno).classList.add('active');
    }

    function sincronizarDatos() {
        // Lógica de Cascos Dinámicos
        const idsCascos = ['oper', 'ofic', 'peon', 'meca', 'ctrl', 'ope_maq'];
        idsCascos.forEach(id => {
            const val = document.getElementById('v_'+id).value;
            const card = document.getElementById('c_'+id);
            if(val > 0) card.classList.add('active');
            else card.classList.remove('active');
        });

        // ==========================================
        // ENSAMBLAJE DE TEXTO (Ajuste de Alineación)
        // ==========================================
        let numAsiento = "{{ numero_asiento }}";
        let fechaLarga = "{{ fecha_hoy_texto_largo }}";
        
        let textoPapel = `<div style="display:flex; justify-content:space-between; margin-bottom: 5px; padding-right:10px;">
            <span><b>ASIENTO No ${numAsiento} DEL RESIDENTE DE OBRA</b></span>
            <span><b>${fechaLarga}</b></span>
        </div>`;

        // 1. Jornal
        const vJ1 = document.getElementById('v_jornal_m').value;
        const vJ2 = document.getElementById('v_jornal_t').value;
        textoPapel += `<b>1.- JORNAL DE TRABAJO</b><br>MAÑANA: ${vJ1} ; TARDE: ${vJ2}<br>`;
        
        // 2. Personal (Formato alineado)
        const vOper = (document.getElementById('v_oper').value || '0').padStart(2, '0');
        const vOfic = (document.getElementById('v_ofic').value || '0').padStart(2, '0');
        const vPeon = (document.getElementById('v_peon').value || '0').padStart(2, '0');
        const vMeca = (document.getElementById('v_meca').value || '0').padStart(2, '0');
        const vCtrl = (document.getElementById('v_ctrl').value || '0').padStart(2, '0');
        const vOpe = (document.getElementById('v_ope_maq').value || '0').padStart(2, '0');

        textoPapel += `<b>2.- PERSONAL DE OBRA:</b><br>`;
        textoPapel += `${vOper} OPERARIOS &nbsp;&nbsp;&nbsp;&nbsp; ${vOfic} OFICIALES &nbsp;&nbsp;&nbsp;&nbsp; ${vPeon} PEONES &nbsp;&nbsp;&nbsp;&nbsp; ${vMeca} MECANICOS<br>`;
        textoPapel += `${vCtrl} CONTROLADORES DE MAQ. &nbsp;&nbsp;&nbsp;&nbsp; ${vOpe} OPERADORES DE MAQ.<br>`;

        document.getElementById('out_general').innerHTML = textoPapel;
    }

    sincronizarDatos();
</script>
"""
# ==============================================================================
# RENDERIZADO FINAL Y LÓGICA DE FECHA
# ==============================================================================
@residencia_bp.route('/residencia')
def redaccion_asiento_residente():
    if 'usuario_id' not in session:
        return redirect(url_for('login.mostrar_login'))

    es_admin = session.get('rol') == 'Admin'
    nombre_completo = session.get('nombre', 'Ing. Samuel Gutierrez')
    menu_superior = obtener_navbar(es_admin, nombre_completo)

    numero_asiento = 88
    
    # Lógica para la fecha con el nombre del día en mayúsculas (Ej: LUNES, 25/05/2026)
    dias_semana = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO", "DOMINGO"]
    fecha_dt = datetime.now()
    nombre_dia = dias_semana[fecha_dt.weekday()]
    fecha_str = fecha_dt.strftime("%d/%m/%Y")
    fecha_hoy_texto_largo = f"{nombre_dia}, {fecha_str}"

    html_completo = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>SAMU — Asiento N° {numero_asiento}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        {BLOQUE_1_CSS}
    </head>
    <body>
        {{{{ menu_superior | safe }}}}
        <div class="dynamic-bg"><div class="bg-blob blob-navy"></div><div class="bg-blob blob-pink"></div></div>
        {BLOQUE_2_STEPPER}
        <div class="split-layout">
            {BLOQUE_3_FORMULARIO}
            {BLOQUE_4_CUADERNO_FISICO}
        </div>
        {BLOQUE_5_JS}
    </body>
    </html>
    """
    
    return render_template_string(html_completo, 
                                  menu_superior=menu_superior, 
                                  numero_asiento=numero_asiento, 
                                  fecha_hoy_texto_largo=fecha_hoy_texto_largo)
