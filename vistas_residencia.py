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
    
    :root { --apple-text: #1d1d1f; --bg-color: #fbfbfd; --nav-height: 52px; }
    body { font-family: 'Inter', sans-serif; background-color: var(--bg-color); color: var(--apple-text); overflow-x: hidden; padding-bottom: 90px;}
    
    .dynamic-bg { position: fixed; inset: 0; z-index: -2; background: #fbfbfd; overflow: hidden; }
    .bg-blob { position: absolute; border-radius: 50%; filter: blur(100px); pointer-events: none; }
    .blob-navy { width: 60vw; height: 60vw; background: #0f172a; opacity: 0.08; top: -10%; left: -10%; animation: movAzul 22s infinite alternate; }
    
    /* Stepper Superior */
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
    .step-btn.omitted { background: #64748b !important; color: white !important; border-color: #475569 !important; }

    /* Tooltip Global (Claro y Elegante) */
    #globalTooltip {
        position: fixed; background: #ffffff; color: #1e293b; padding: 8px 16px;
        border-radius: 10px; font-size: 12px; font-weight: 700; white-space: nowrap;
        border: 1px solid #e2e8f0; box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        pointer-events: none; z-index: 999999; opacity: 0; transition: opacity 0.15s ease;
    }

    /* Layout Pantalla Dividida */
    .split-layout { display: flex; gap: 40px; max-width: 1500px; margin: 140px auto 0 auto; padding: 0 20px; align-items: flex-start; }
    .form-column { flex: 1; max-width: 600px; }
    .preview-column { flex: 1; position: sticky; top: 140px; height: calc(100vh - 240px); overflow-y: auto; }
    
    /* Formularios */
    .step-view { display: none; animation: fadeIn 0.4s ease; background: rgba(255,255,255,0.7); backdrop-filter: blur(20px); padding: 30px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.02); border: 1px solid rgba(255,255,255,0.9);}
    .step-view.active { display: block; }
    @keyframes fadeIn { from { opacity: 0; transform: translateX(-10px); } to { opacity: 1; transform: translateX(0); } }
    .step-title { font-size: 22px; font-weight: 800; margin-bottom: 25px; color: #0f172a; letter-spacing: -0.5px;}
    .form-label { font-size: 12px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px;}
    .form-control, .form-select { border-radius: 14px; border: 1px solid #cbd5e1; padding: 14px; font-size: 14px; background: rgba(255,255,255,0.9); font-weight: 500;}
    .form-control:focus, .form-select:focus { border-color: #0066cc; box-shadow: 0 0 0 4px rgba(0,102,204,0.15); }

    /* =========================================================================
       DISEÑO EXACTO DEL CUADERNO DE OBRA FÍSICO (SEGÚN FOTO)
       ========================================================================= */
    .papel-fisico {
        background: #fdfdfa; width: 100%; min-height: 900px; padding: 40px 50px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1); border: 1px solid #e2e8f0;
        font-family: Arial, sans-serif; color: #000; position: relative;
    }
    
    /* Cabecera del Papel */
    .p-header-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; }
    .p-title-box { text-align: center; flex: 1; }
    .p-title-box h1 { font-size: 28px; font-weight: bold; text-decoration: underline; letter-spacing: 1px; margin: 0; color: #000;}
    .p-num { font-size: 24px; font-weight: bold; margin-top: 5px; color: #000;}
    .p-sello { width: 90px; height: 90px; border: 2px dashed #94a3b8; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 11px; color: #94a3b8; text-align: center; padding: 5px; opacity: 0.5; margin-top: -20px;}
    
    /* Datos Meta Alineados (La magia de alinear en la línea) */
    .p-meta { margin-bottom: 20px; }
    .p-row { display: flex; align-items: flex-end; margin-bottom: 12px; }
    .p-label { font-size: 14px; font-weight: bold; margin-right: 8px; color: #000; white-space: nowrap; }
    .p-line { flex: 1; border-bottom: 1px solid #000; position: relative; height: 22px; }
    
    /* Tinta de Lapicero Celeste Oscuro */
    .lapicero-meta { 
        position: absolute; bottom: -2px; left: 15px; 
        font-family: 'Caveat', cursive; color: #0263a0; 
        font-size: 24px; line-height: 0.8; white-space: nowrap; 
    }
    
    /* Cuerpo Rayado (El texto que escribes) */
    .p-body-lines {
        background-image: repeating-linear-gradient(transparent, transparent 27px, #94a3b8 28px);
        line-height: 28px; min-height: 650px; padding-top: 4px; position: relative;
    }
    
    /* Fuente de Lapicero General */
    .lapicero { font-family: 'Caveat', cursive; color: #0263a0; font-size: 22px; padding-left: 10px; margin-top: -4px;}
    .lapicero-muted { font-family: 'Caveat', cursive; color: #64748b; font-size: 20px; padding-left: 20px; }
    
    /* Etiqueta de PAGINACIÓN */
    .p-van { position: absolute; bottom: 0; right: 10px; font-family: 'Caveat', cursive; color: #0263a0; font-size: 20px; }

    /* Firmas Footer */
    .p-footer { display: flex; justify-content: space-between; margin-top: 60px; font-size: 12px; font-weight: bold; color: #000;}
    .p-sig { border-top: 1px solid #000; width: 28%; text-align: center; padding-top: 5px; }

    /* Barra Inferior del Sistema */
    .bottom-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(255,255,255,0.9); backdrop-filter: blur(15px); border-top: 1px solid rgba(0,0,0,0.08); padding: 15px 30px; z-index: 900; display: flex; justify-content: space-between; align-items: center; }
    .slider-track { width: 100%; max-width: 400px; height: 60px; background: rgba(0,0,0,0.05); border-radius: 30px; position: relative; display: flex; align-items: center; justify-content: center; overflow: hidden; margin: 0 auto; }
    .slider-text { font-size: 13px; font-weight: 800; color: #64748b; text-transform: uppercase; z-index: 1; pointer-events: none;}
    .slider-handle { width: 52px; height: 52px; background: #000; color: #fff; border-radius: 50%; position: absolute; left: 4px; display: flex; align-items: center; justify-content: center; z-index: 2; cursor: grab;}
    .slider-progress { position: absolute; left: 0; top: 0; height: 100%; background: rgba(0, 102, 204, 0.1); width: 0; pointer-events: none; }

    @media (max-width: 1024px) {
        .split-layout { flex-direction: column; align-items: center; margin-top: 130px; padding: 0 10px;}
        .form-column { width: 100%; max-width: 100%; }
        .preview-column { display: none; } 
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
            <div class="step-title">1. Jornal de Trabajo</div>
            <div class="row g-3">
                <div class="col-sm-6"><label class="form-label">Mañana</label><input type="text" class="form-control req-step1" id="v_jornal_m" value="07:00 - 12:00"></div>
                <div class="col-sm-6"><label class="form-label">Tarde</label><input type="text" class="form-control req-step1" id="v_jornal_t" value="13:00 - 17:00"></div>
            </div>
        </div>

        <div class="step-view" id="step2">
            <div class="step-title">2. Personal de Obra</div>
            <div class="row g-3">
                <div class="col-4"><label class="form-label">Operarios</label><input type="number" class="form-control req-step2" id="v_oper" placeholder="0"></div>
                <div class="col-4"><label class="form-label">Oficiales</label><input type="number" class="form-control req-step2" id="v_ofic" placeholder="0"></div>
                <div class="col-4"><label class="form-label">Peones</label><input type="number" class="form-control req-step2" id="v_peon" placeholder="0"></div>
                <div class="col-4"><label class="form-label">Mecánicos</label><input type="number" class="form-control req-step2" id="v_meca" placeholder="0"></div>
                <div class="col-4"><label class="form-label">Controladores</label><input type="number" class="form-control req-step2" id="v_ctrl" placeholder="0"></div>
                <div class="col-4"><label class="form-label">Operadores</label><input type="number" class="form-control req-step2" id="v_ope_maq" placeholder="0"></div>
            </div>
        </div>

        <div class="step-view" id="step3"><div class="step-title">3. Partidas Ejecutadas</div><textarea class="form-control req-step3" id="v_partidas" rows="6" placeholder="Detalle partidas..."></textarea></div>
        <div class="step-view" id="step4"><div class="step-title">4. Partidas Mayor Metrado</div><textarea class="form-control req-step4" id="v_mayor_m" rows="6" placeholder="Detalle excedentes..."></textarea></div>
        <div class="step-view" id="step5"><div class="step-title">5. Sub Partidas Ejecutadas</div><textarea class="form-control req-step5" id="v_sub_p" rows="6" placeholder="Sub partidas..."></textarea></div>
        <div class="step-view" id="step6"><div class="step-title">6. Actividades Ejecutadas</div><textarea class="form-control req-step6" id="v_activ" rows="6" placeholder="Diario de actividades..."></textarea></div>
        <div class="step-view" id="step7"><div class="step-title">7. Movimiento de Almacén</div><textarea class="form-control req-step7" id="v_almacen" rows="6" placeholder="Ingresos y salidas..."></textarea></div>
        <div class="step-view" id="step8"><div class="step-title">8. Maquinarias y Equipos</div><textarea class="form-control req-step8" id="v_maquina" rows="6" placeholder="GORE y Alquiladas..."></textarea></div>
        <div class="step-view" id="step9"><div class="step-title">9. Herramientas Manuales</div><textarea class="form-control req-step9" id="v_herram" rows="4" placeholder="Uso de herramientas..."></textarea></div>
        <div class="step-view" id="step10"><div class="step-title text-danger">10. Ocurrencias</div><textarea class="form-control border-danger req-step10" id="v_ocurrencia" rows="8" placeholder="Ocurrencias legales..."></textarea></div>

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
<div class="bottom-bar shadow-lg">
    <button type="button" class="btn btn-outline-secondary fw-bold rounded-pill px-4" onclick="omitirPaso()"><i class="bi bi-skip-forward-fill"></i> Omitir</button>
    <div id="indicadorGuardado" class="small text-muted fw-semibold d-none d-sm-block"><i class="bi bi-cloud-arrow-up"></i> Autoguardado</div>
    <button type="button" class="btn btn-dark fw-bold rounded-pill px-4" onclick="siguientePaso()">Guardar y Continuar <i class="bi bi-arrow-right"></i></button>
</div>

<script>
    let currentStep = 1;
    const totalSteps = 11;

    // 1. Tooltip Flotante Global (Elegante)
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
    
    // 2. Navegación
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
            document.querySelector('.preview-column').style.position = 'relative';
            document.querySelector('.preview-column').style.top = '0';
            document.querySelector('.preview-column').style.height = 'auto';
        } else {
            document.querySelector('.bottom-bar').style.display = 'flex';
            if(window.innerWidth <= 1024) document.querySelector('.preview-column').style.display = 'none';
        }
        sincronizarDatos();
    }

    function siguientePaso() { if(currentStep < totalSteps) jumpToStep(currentStep + 1); }
    function omitirPaso() {
        document.querySelectorAll(`.req-step${currentStep}`).forEach(inp => { if (inp.tagName === 'TEXTAREA') inp.value = "SIN NOVEDAD EN LA JORNADA"; });
        document.getElementById(`btnStep${currentStep}`).classList.add('omitted');
        sincronizarDatos(); siguientePaso();
    }

    // 3. GENERADOR DE TEXTO EXACTO PARA EL CUADERNO
    function sincronizarDatos() {
        // Colores del Stepper
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
            } else {
                btn.setAttribute('data-tooltip', "Paso Omitido");
            }
        }

        // ==========================================
        // ENSAMBLAJE DE TEXTO (FORMATO SOLICITADO)
        // ==========================================
        let numAsiento = "{{ numero_asiento }}";
        let fechaLarga = "{{ fecha_hoy_texto_largo }}";
        
        // Cabecera Principal del Asiento
        let textoPapel = `<div style="display:flex; justify-content:space-between; padding-right:15px; margin-bottom: 5px;">
            <span><b>ASIENTO No ${numAsiento} DEL RESIDENTE DE OBRA</b></span>
            <span><b>${fechaLarga}</b></span>
        </div>`;

        // 1. Jornal
        const vJornalM = document.getElementById('v_jornal_m').value;
        const vJornalT = document.getElementById('v_jornal_t').value;
        if(vJornalM || vJornalT) {
            textoPapel += `<b>1.- JORNAL DE TRABAJO</b><br>`;
            textoPapel += `MAÑANA: ${vJornalM} ; TARDE: ${vJornalT}<br>`;
        }
        
        // 2. Personal (con relleno de ceros a la izquierda para que se vea profesional)
        const vOper = (document.getElementById('v_oper').value || '0').padStart(2, '0');
        const vOfic = (document.getElementById('v_ofic').value || '0').padStart(2, '0');
        const vPeon = (document.getElementById('v_peon').value || '0').padStart(2, '0');
        const vMeca = (document.getElementById('v_meca').value || '0').padStart(2, '0');
        const vCtrl = (document.getElementById('v_ctrl').value || '0').padStart(2, '0');
        const vOpe = (document.getElementById('v_ope_maq').value || '0').padStart(2, '0');

        textoPapel += `<b>2.- PERSONAL DE OBRA:</b><br>`;
        textoPapel += `&nbsp;&nbsp;${vOper} OPERARIOS &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${vOfic} OFICIALES &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${vPeon} PEONES &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${vMeca} MECANICOS<br>`;
        textoPapel += `&nbsp;&nbsp;${vCtrl} CONTROLADORES DE MAQUINARIA &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ${vOpe} OPERADORES DE MAQUINARIA<br>`;

        // Partidas y los demás textos largos
        const vPartidas = document.getElementById('v_partidas').value;
        if(vPartidas) textoPapel += `<b>3.- PARTIDAS EJECUTADAS</b><br>${vPartidas.replace(/\\n/g, '<br>')}<br>`;
        
        const vMayor = document.getElementById('v_mayor_m').value;
        if(vMayor) textoPapel += `<b>4.- PARTIDAS DE MAYOR METRADO</b><br>${vMayor.replace(/\\n/g, '<br>')}<br>`;

        const vOcurrencia = document.getElementById('v_ocurrencia').value;
        if(vOcurrencia) textoPapel += `<b>10.- OCURRENCIAS Y CONOCIMIENTOS</b><br>${vOcurrencia.replace(/\\n/g, '<br>')}<br>`;

        // Insertar en la hoja
        document.getElementById('out_general').innerHTML = textoPapel;
        
        // Lógica visual del "Van..." si el texto es muy largo
        const bodyLines = document.querySelector('.p-body-lines');
        if (bodyLines.scrollHeight > 650) {
            document.getElementById('indicadorVan').style.display = 'block';
        } else {
            document.getElementById('indicadorVan').style.display = 'none';
        }
    }

    // 4. Slider de Firma
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
        alert("¡Asiento N° 88 firmado con éxito!"); window.location.href = '/cuaderno';
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
