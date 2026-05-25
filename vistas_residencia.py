# =========================================================
# vistas_residencia.py
# Arquitectura Modular: Formularios por Pasos + Live Preview
# =========================================================

from flask import Blueprint, render_template_string, session, redirect, url_for
from navbar import obtener_navbar
from datetime import datetime

residencia_bp = Blueprint('residencia', __name__)

# ==============================================================================
# BLOQUE 1: ESTILOS CSS (DISEÑO, COLORES Y FORMATO DEL CUADERNO FÍSICO)
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
    .form-column { flex: 1; max-width: 650px; }
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
        background: #fdfdfa; width: 100%; min-height: 800px; padding: 40px 50px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1); border: 1px solid #e2e8f0;
        font-family: Arial, sans-serif; color: #000; position: relative;
    }
    
    /* Cabecera del Papel */
    .p-header-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; }
    .p-title-box { text-align: center; flex: 1; }
    .p-title-box h1 { font-size: 26px; font-weight: bold; text-decoration: underline; letter-spacing: 1px; margin: 0; }
    .p-num { font-size: 22px; font-weight: bold; margin-top: 5px;}
    .p-sello { width: 80px; height: 80px; border: 2px dashed #94a3b8; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #94a3b8; text-align: center; padding: 5px; opacity: 0.5;}
    
    /* Datos Meta (Obra, Proyecto, etc) */
    .p-meta { font-size: 13px; font-weight: bold; line-height: 1.8; margin-bottom: 20px; }
    .p-row { display: flex; align-items: flex-end; margin-bottom: 5px; }
    .p-label { white-space: nowrap; margin-right: 5px; }
    .p-line { flex: 1; border-bottom: 1px solid #000; height: 18px; }
    
    /* Cuerpo Rayado (El texto que escribes) */
    .p-body-lines {
        background-image: repeating-linear-gradient(transparent, transparent 27px, #475569 28px);
        line-height: 28px; min-height: 500px; padding-top: 5px;
    }
    
    /* Fuente de Lapicero (Azul, tipo manuscrita) */
    .lapicero { font-family: 'Caveat', cursive; color: #0000CD; font-size: 20px; padding-left: 10px; }
    .lapicero-meta { font-family: 'Caveat', cursive; color: #0000CD; font-size: 18px; font-weight: 500; }
    
    /* Firmas Footer */
    .p-footer { display: flex; justify-content: space-between; margin-top: 60px; font-size: 11px; font-weight: bold; }
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
    <button class="step-btn active" id="btnStep1" onclick="jumpToStep(1)" data-tooltip="Faltan datos">1. Clima</button>
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
        <span class="text-muted small fw-bold">{{ fecha_hoy }}</span>
    </div>

    <form id="formResidencia" oninput="sincronizarDatos()">
        <div class="step-view active" id="step1">
            <div class="step-title">1. Condiciones del Entorno</div>
            <div class="row g-3">
                <div class="col-sm-6"><label class="form-label">Mañana (07:00 - 12:00)</label><select class="form-select req-step1" id="v_clima_m"><option value="">Seleccione...</option><option value="Soleado">Soleado</option><option value="Lluvioso">Lluvioso</option></select></div>
                <div class="col-sm-6"><label class="form-label">Tarde (13:00 - 18:00)</label><select class="form-select req-step1" id="v_clima_t"><option value="">Seleccione...</option><option value="Soleado">Soleado</option><option value="Lluvioso">Lluvioso</option></select></div>
                <div class="col-12"><label class="form-label">Impacto Operativo</label><select class="form-select req-step1" id="v_impacto"><option value="">Seleccione...</option><option value="Trabajo Normal al 100%">Trabajo al 100%</option><option value="Restricción Parcial por Clima">Restricción Parcial</option></select></div>
            </div>
        </div>

        <div class="step-view" id="step2">
            <div class="step-title">2. Personal de Obra</div>
            <div class="row g-3">
                <div class="col-4"><label class="form-label">Operarios</label><input type="number" class="form-control req-step2" id="v_oper" placeholder="0"></div>
                <div class="col-4"><label class="form-label">Oficiales</label><input type="number" class="form-control req-step2" id="v_ofic" placeholder="0"></div>
                <div class="col-4"><label class="form-label">Peones</label><input type="number" class="form-control req-step2" id="v_peon" placeholder="0"></div>
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
            <div style="width: 80px;"></div> <div class="p-title-box">
                <h1>CUADERNO DE OBRA</h1>
            </div>
            <div style="text-align: right; width: 100px;">
                <div class="p-num">Nº {{ numero_asiento }}</div>
                <div class="p-sello">Sello Juzgado</div>
            </div>
        </div>
        
        <div class="p-meta">
            <div class="d-flex w-100 mb-1">
                <div class="d-flex" style="flex: 1;"><span class="p-label">Fecha:</span><div class="p-line"><span class="lapicero-meta">{{ fecha_hoy }}</span></div></div>
                <div class="d-flex" style="flex: 1; margin-left: 15px;"><span class="p-label">Modalidad:</span><div class="p-line"><span class="lapicero-meta">Adm. Directa</span></div></div>
            </div>
            <div class="p-row"><span class="p-label">Obra:</span><div class="p-line"><span class="lapicero-meta">Mejoramiento de la Carretera PU N-110</span></div></div>
            <div class="p-row"><span class="p-label">Proyecto:</span><div class="p-line"><span class="lapicero-meta">Asiruni—Rosaspata—Huayrapata</span></div></div>
            <div class="p-row"><span class="p-label">Programa:</span><div class="p-line"></div></div>
            <div class="p-row"><span class="p-label">Entidad Ejecutora:</span><div class="p-line"><span class="lapicero-meta">Gobierno Regional Puno</span></div></div>
        </div>

        <div class="p-body-lines">
            <div class="lapicero text-muted" style="font-size: 16px;">... viene del ASIENTO Nº 87 DEL RESIDENTE DE OBRA </div>
            
            <div class="lapicero" id="out_general">
                </div>
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
# BLOQUE 5: JAVASCRIPT (LÓGICA DEL TOOLTIP, STEPPER Y LIVE PREVIEW)
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

    // 1. Lógica del Tooltip Global (Nunca se corta)
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
    
    // 2. Navegación entre pasos
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

    // 3. Sincronización Termómetro y Hoja de Papel Física
    function sincronizarDatos() {
        let textoPapel = "";

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

        // Compilar texto para la hoja física
        const vClimaM = document.getElementById('v_clima_m').value;
        if(vClimaM) textoPapel += `<b>1. CLIMA:</b> Mañana: ${vClimaM} | Tarde: ${document.getElementById('v_clima_t').value}<br>`;
        
        const vOper = document.getElementById('v_oper').value;
        if(vOper) textoPapel += `<b>2. PERSONAL:</b> Operarios: ${vOper}, Oficiales: ${document.getElementById('v_ofic').value}, Peones: ${document.getElementById('v_peon').value}<br>`;

        const vPartidas = document.getElementById('v_partidas').value;
        if(vPartidas) textoPapel += `<b>3. PARTIDAS:</b> ${vPartidas.replace(/\\n/g, '<br>')}<br>`;
        
        const vOcurrencia = document.getElementById('v_ocurrencia').value;
        if(vOcurrencia) textoPapel += `<b>10. OCURRENCIAS:</b> ${vOcurrencia.replace(/\\n/g, '<br>')}<br>`;

        document.getElementById('out_general').innerHTML = textoPapel;
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
# RENDERIZADO FINAL (Ensamblaje del ecosistema)
# ==============================================================================
@residencia_bp.route('/residencia')
def redaccion_asiento_residente():
    if 'usuario_id' not in session:
        return redirect(url_for('login.mostrar_login'))

    es_admin = session.get('rol') == 'Admin'
    nombre_completo = session.get('nombre', 'Ing. Samuel Gutierrez')
    menu_superior = obtener_navbar(es_admin, nombre_completo)

    numero_asiento = 88
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")

    html_completo = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>SAMU — Asiento de Residencia N° {numero_asiento}</title>
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
    
    # Renderizamos pasando las variables que Flask necesita inyectar
    return render_template_string(html_completo, 
                                  menu_superior=menu_superior, 
                                  numero_asiento=numero_asiento, 
                                  fecha_hoy=fecha_hoy,
                                  nombre_completo=nombre_completo)
