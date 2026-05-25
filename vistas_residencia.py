# =========================================================
# vistas_residencia.py
# Módulo: Llenado por Pasos + Live Preview + UI Premium
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

    numero_asiento = 88
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>SAMU — Asiento de Residencia N° {{ numero_asiento }}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        
        <style>
            :root { --apple-text: #1d1d1f; --bg-color: #fbfbfd; --nav-height: 52px; }
            body { font-family: 'Inter', sans-serif; background-color: var(--bg-color); color: var(--apple-text); overflow-x: hidden; padding-bottom: 90px;}
            
            /* Fondos dinámicos */
            .dynamic-bg { position: fixed; inset: 0; z-index: -2; background: #fbfbfd; overflow: hidden; }
            .bg-blob { position: absolute; border-radius: 50%; filter: blur(100px); pointer-events: none; }
            .blob-navy { width: 60vw; height: 60vw; background: #0f172a; opacity: 0.10; top: -10%; left: -10%; animation: movAzul 22s infinite alternate; }
            .blob-pink { width: 60vw; height: 60vw; background: #f9a8d4; opacity: 0.10; bottom: -10%; right: -10%; animation: movRosa 26s infinite alternate; }
            @keyframes movAzul { 100% { transform: translate(10vw,10vh) scale(1.1); } }
            @keyframes movRosa { 100% { transform: translate(-10vw,-10vh) scale(1.1); } }

            /* ===================================================
               STEPPER SUPERIOR Y BOTONES ELEGANTES
               =================================================== */
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
                position: relative; 
            }
            
            /* ESTADO ACTIVO (Zoom, Blanco puro, Letra Negra Negrita) */
            .step-btn.active { 
                background: #ffffff !important; 
                color: #000000 !important; 
                font-weight: 800 !important; 
                transform: scale(1.08); 
                box-shadow: 0 8px 20px rgba(0,0,0,0.08);
                border-color: #000000 !important;
            }
            
            /* ESTADO OMITIDO */
            .step-btn.omitted { background: #64748b !important; color: white !important; border-color: #475569 !important; }

            /* TOOLTIP ELEGANTE ESTILO APPLE (Burbuja Flotante) */
            .step-btn::after {
                content: attr(data-tooltip);
                position: absolute; bottom: -35px; left: 50%; transform: translateX(-50%) translateY(-10px);
                background: rgba(0, 0, 0, 0.85); color: #fff; padding: 6px 14px;
                border-radius: 8px; font-size: 11px; font-weight: 600; white-space: nowrap;
                opacity: 0; visibility: hidden; transition: all 0.3s ease;
                pointer-events: none; backdrop-filter: blur(5px); z-index: 1000;
            }
            .step-btn::before { /* Triangulito del Tooltip */
                content: ''; position: absolute; bottom: -10px; left: 50%; transform: translateX(-50%) translateY(-10px);
                border-width: 0 5px 5px 5px; border-style: solid; border-color: transparent transparent rgba(0,0,0,0.85) transparent;
                opacity: 0; visibility: hidden; transition: all 0.3s ease; pointer-events: none; z-index: 1000;
            }
            .step-btn:hover::after, .step-btn:hover::before { opacity: 1; visibility: visible; transform: translateX(-50%) translateY(0); }
            
            /* ===================================================
               LAYOUT DIVIDIDO (FORMULARIO Y VISTA PREVIA)
               =================================================== */
            .split-layout {
                display: flex; gap: 30px; max-width: 1400px; margin: 140px auto 0 auto; padding: 0 20px; align-items: flex-start;
            }
            
            .form-column { flex: 1; max-width: 700px; }
            
            .preview-column { 
                flex: 1; position: sticky; top: 140px; 
                background: #ffffff; border: 1px solid #cbd5e1; border-radius: 16px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.05); height: calc(100vh - 240px); overflow-y: auto;
            }
            
            /* Diseño de Hoja de Papel para la Vista Previa */
            .paper-sheet {
                padding: 40px; font-family: 'Courier New', Courier, monospace; font-size: 13px; line-height: 1.6; color: #1e293b;
                background-image: linear-gradient(rgba(0, 102, 204, 0.08) 1px, transparent 1px);
                background-size: 100% 28px; /* Líneas de cuaderno */
            }

            .step-view { display: none; animation: fadeIn 0.4s ease; background: rgba(255,255,255,0.7); backdrop-filter: blur(20px); padding: 30px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.02); border: 1px solid rgba(255,255,255,0.9);}
            .step-view.active { display: block; }
            @keyframes fadeIn { from { opacity: 0; transform: translateX(-10px); } to { opacity: 1; transform: translateX(0); } }

            .step-title { font-size: 22px; font-weight: 800; margin-bottom: 25px; color: #0f172a; letter-spacing: -0.5px;}
            .form-label { font-size: 12px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px;}
            .form-control, .form-select { border-radius: 14px; border: 1px solid #cbd5e1; padding: 14px; font-size: 14px; background: rgba(255,255,255,0.9); transition: all 0.2s; font-weight: 500;}
            .form-control:focus, .form-select:focus { background: #fff; border-color: #0066cc; box-shadow: 0 0 0 4px rgba(0,102,204,0.15); }

            /* Barra Fija Inferior */
            .bottom-bar {
                position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(255,255,255,0.9);
                backdrop-filter: blur(15px); border-top: 1px solid rgba(0,0,0,0.08);
                padding: 15px 30px; z-index: 900; display: flex; justify-content: space-between; align-items: center;
            }

            /* Slider Candado (Paso 11) */
            .slider-track { width: 100%; max-width: 400px; height: 60px; background: rgba(0,0,0,0.05); border-radius: 30px; position: relative; display: flex; align-items: center; justify-content: center; overflow: hidden; margin: 0 auto; border: 1px solid rgba(0,0,0,0.05);}
            .slider-text { font-size: 13px; font-weight: 800; color: #64748b; text-transform: uppercase; z-index: 1; pointer-events: none; letter-spacing: 0.5px;}
            .slider-handle { width: 52px; height: 52px; background: #000; color: #fff; border-radius: 50%; position: absolute; left: 4px; display: flex; align-items: center; justify-content: center; z-index: 2; cursor: grab; box-shadow: 0 4px 15px rgba(0,0,0,0.2);}
            .slider-progress { position: absolute; left: 0; top: 0; height: 100%; background: rgba(0, 102, 204, 0.1); width: 0; pointer-events: none; }

            /* RESPONSIVO */
            @media (max-width: 1024px) {
                .split-layout { flex-direction: column; align-items: center; margin-top: 130px; padding: 0 10px;}
                .form-column { width: 100%; max-width: 100%; }
                .preview-column { display: none; } /* Oculta la vista previa en celulares para no saturar */
                .step-view { padding: 20px; }
            }
        </style>
    </head>
    <body>

        {{ menu_superior | safe }}

        <div class="dynamic-bg"><div class="bg-blob blob-navy"></div><div class="bg-blob blob-pink"></div></div>

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
            <button class="step-btn border-dark text-dark fw-bold" id="btnStep11" onclick="jumpToStep(11)" data-tooltip="Ir a firmar"><i class="bi bi-shield-lock-fill"></i> Firma Final</button>
        </div>

        <div class="split-layout">
            
            <div class="form-column">
                <div class="d-flex justify-content-between mb-3 px-2">
                    <h6 class="text-primary fw-bold mb-0">Asiento N° {{ numero_asiento }}</h6>
                    <span class="text-muted small fw-bold">{{ fecha_hoy }}</span>
                </div>

                <form id="formResidencia" oninput="sincronizarDatos()">
                    
                    <div class="step-view active" id="step1">
                        <div class="step-title">1. Condiciones del Entorno (Clima)</div>
                        <div class="row g-3">
                            <div class="col-sm-6"><label class="form-label">Mañana (07:00 - 12:00)</label><select class="form-select req-step1" id="v_clima_m"><option value="">Seleccione...</option><option value="Soleado">Soleado</option><option value="Lluvioso">Lluvia</option></select></div>
                            <div class="col-sm-6"><label class="form-label">Tarde (13:00 - 18:00)</label><select class="form-select req-step1" id="v_clima_t"><option value="">Seleccione...</option><option value="Soleado">Soleado</option><option value="Lluvioso">Lluvia</option></select></div>
                            <div class="col-12"><label class="form-label">Impacto Operativo</label><select class="form-select req-step1" id="v_impacto"><option value="">Seleccione...</option><option value="Trabajo Normal al 100%">Trabajo al 100%</option><option value="Restricción Parcial por Clima">Restricción Parcial</option></select></div>
                        </div>
                    </div>

                    <div class="step-view" id="step2">
                        <div class="step-title">2. Personal de Obra</div>
                        <div class="row g-3">
                            <div class="col-4"><label class="form-label">Operarios</label><input type="number" class="form-control req-step2" id="v_oper" placeholder="0"></div>
                            <div class="col-4"><label class="form-label">Oficiales</label><input type="number" class="form-control req-step2" id="v_ofic" placeholder="0"></div>
                            <div class="col-4"><label class="form-label">Peones</label><input type="number" class="form-control req-step2" id="v_peon" placeholder="0"></div>
                            <div class="col-6"><label class="form-label">Mecánicos</label><input type="number" class="form-control req-step2" id="v_meca" placeholder="0"></div>
                            <div class="col-6"><label class="form-label">Operadores</label><input type="number" class="form-control req-step2" id="v_ope_maq" placeholder="0"></div>
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
                        <p class="text-center text-muted small mb-5">El documento a la derecha (o arriba) representa la versión oficial. Al deslizar el candado, los datos quedarán inmutables.</p>
                        <div class="slider-track" id="sliderTrack">
                            <div class="slider-progress" id="sliderProgress"></div>
                            <div class="slider-text" id="sliderText">Deslizar para Firmar</div>
                            <div class="slider-handle" id="sliderHandle"><i class="bi bi-lock-fill" style="font-size: 1.2rem;"></i></div>
                        </div>
                    </div>
                </form>
            </div>

            <div class="preview-column">
                <div class="bg-light p-3 border-bottom d-flex justify-content-between align-items-center position-sticky top-0 z-1">
                    <h6 class="m-0 fw-bold"><i class="bi bi-file-earmark-text text-primary"></i> Cuaderno de Obra Oficial</h6>
                    <span class="badge bg-warning text-dark border">Pre-visualización</span>
                </div>
                
                <div class="paper-sheet" id="livePaperContent">
                    <p style="text-align:center; font-weight:bold; font-size:16px; margin-bottom:20px;">
                        ASIENTO N° {{ numero_asiento }} DEL RESIDENTE DE OBRA<br>
                        FECHA: {{ fecha_hoy }}
                    </p>
                    <p><b>1. JORNAL Y CLIMA:</b> <br>Mañana: <span id="out_clima_m" class="text-muted">___</span> | Tarde: <span id="out_clima_t" class="text-muted">___</span> | Estado: <span id="out_impacto" class="text-muted">___</span></p>
                    <p><b>2. PERSONAL DE OBRA:</b> <br>Operarios: <span id="out_oper">0</span>, Oficiales: <span id="out_ofic">0</span>, Peones: <span id="out_peon">0</span>, Mecánicos: <span id="out_meca">0</span>, Operadores: <span id="out_ope_maq">0</span>.</p>
                    <p><b>3. PARTIDAS EJECUTADAS:</b> <br><span id="out_partidas" class="text-muted">Sin datos.</span></p>
                    <p><b>4. MAYOR METRADO:</b> <br><span id="out_mayor_m" class="text-muted">Sin datos.</span></p>
                    <p><b>5. SUB PARTIDAS:</b> <br><span id="out_sub_p" class="text-muted">Sin datos.</span></p>
                    <p><b>6. ACTIVIDADES:</b> <br><span id="out_activ" class="text-muted">Sin datos.</span></p>
                    <p><b>7. ALMACÉN:</b> <br><span id="out_almacen" class="text-muted">Sin datos.</span></p>
                    <p><b>8. MAQUINARIA:</b> <br><span id="out_maquina" class="text-muted">Sin datos.</span></p>
                    <p><b>9. HERRAMIENTAS:</b> <br><span id="out_herram" class="text-muted">Sin datos.</span></p>
                    <p><b>10. OCURRENCIAS:</b> <br><span id="out_ocurrencia" class="text-muted">Sin datos.</span></p>
                    <br><br><br>
                    <div style="text-align:center; border-top: 1px solid #000; width: 250px; margin: 0 auto; padding-top: 5px;">
                        <b>{{ nombre_completo }}</b><br>Residente de Obra
                    </div>
                </div>
            </div>

        </div>

        <div class="bottom-bar shadow-lg">
            <button type="button" class="btn btn-outline-secondary fw-bold rounded-pill px-4" id="btnOmitir" onclick="omitirPaso()">
                <i class="bi bi-skip-forward-fill"></i> Omitir
            </button>
            <div id="indicadorGuardado" class="small text-muted fw-semibold d-none d-sm-block"><i class="bi bi-cloud-arrow-up"></i> Autoguardado</div>
            <button type="button" class="btn btn-dark fw-bold rounded-pill px-4 shadow-sm" id="btnSiguiente" onclick="siguientePaso()">
                Guardar y Continuar <i class="bi bi-arrow-right"></i>
            </button>
        </div>

        <script>
            let currentStep = 1;
            const totalSteps = 11;
            
            // --- NAVEGACIÓN Y GUARDADO SILENCIOSO ---
            function jumpToStep(stepIndex) {
                // Indicador de Guardado Silencioso
                document.getElementById('indicadorGuardado').innerHTML = '<i class="bi bi-check2-all text-success"></i> Guardado en la nube';
                setTimeout(() => { document.getElementById('indicadorGuardado').innerHTML = '<i class="bi bi-cloud-arrow-up"></i> Autoguardado'; }, 2000);

                // Quitar clase Active al anterior
                document.getElementById(`step${currentStep}`).classList.remove('active');
                document.getElementById(`btnStep${currentStep}`).classList.remove('active');
                
                // Activar el nuevo
                currentStep = stepIndex;
                document.getElementById(`step${currentStep}`).classList.add('active');
                document.getElementById(`btnStep${currentStep}`).classList.add('active');
                
                // Centrar Scroll en móvil
                const btnObj = document.getElementById(`btnStep${currentStep}`);
                document.getElementById('stepperBar').scrollLeft = btnObj.offsetLeft - 50;

                // Ocultar barra inferior en firma
                if (currentStep === 11) {
                    document.querySelector('.bottom-bar').style.display = 'none';
                    // Si el usuario está en celular, mostramos la Vista Previa (que estaba oculta) moviéndola arriba
                    document.querySelector('.preview-column').style.display = 'block';
                    document.querySelector('.preview-column').style.position = 'relative';
                    document.querySelector('.preview-column').style.top = '0';
                    document.querySelector('.preview-column').style.height = 'auto';
                    document.querySelector('.preview-column').style.marginBottom = '30px';
                } else {
                    document.querySelector('.bottom-bar').style.display = 'flex';
                    if(window.innerWidth <= 1024) document.querySelector('.preview-column').style.display = 'none'; // Re-ocultar en móvil
                }

                sincronizarDatos();
            }

            function siguientePaso() { if(currentStep < totalSteps) jumpToStep(currentStep + 1); }

            function omitirPaso() {
                const inputs = document.querySelectorAll(`.req-step${currentStep}`);
                inputs.forEach(inp => { if (inp.tagName === 'TEXTAREA' || inp.type === 'text') inp.value = "SIN NOVEDAD EN LA JORNADA"; });
                document.getElementById(`btnStep${currentStep}`).classList.add('omitted');
                sincronizarDatos();
                siguientePaso();
            }

            // --- LÓGICA CORE: TERMÓMETROS Y LIVE PREVIEW ---
            function sincronizarDatos() {
                // 1. PINTAR TERMÓMETROS DE LOS BOTONES
                for (let i = 1; i <= 10; i++) {
                    const inputs = document.querySelectorAll(`.req-step${i}`);
                    if (inputs.length === 0) continue;

                    let llenos = 0;
                    inputs.forEach(inp => {
                        if (inp.value.trim() !== '' && inp.value.trim() !== '0') llenos++;
                    });

                    let porcentaje = Math.round((llenos / inputs.length) * 100);
                    let btn = document.getElementById(`btnStep${i}`);
                    
                    if (!btn.classList.contains('omitted')) {
                        // El tooltip elegante de Apple
                        btn.setAttribute('data-tooltip', porcentaje === 100 ? "¡Completado!" : `Progreso: ${porcentaje}%`);
                        
                        // Si el botón NO es el activo, le aplicamos el degradado azul. 
                        // Si es el ACTIVO, el CSS puro lo forzará a BLANCO (!important).
                        btn.style.background = `linear-gradient(to right, #bfdbfe ${porcentaje}%, #f8fafc ${porcentaje}%)`;
                    } else {
                        btn.setAttribute('data-tooltip', "Paso Omitido");
                    }
                }

                // 2. ACTUALIZAR LA HOJA DE PAPEL EN TIEMPO REAL (LIVE PREVIEW)
                const campos = ['clima_m', 'clima_t', 'impacto', 'oper', 'ofic', 'peon', 'meca', 'ope_maq', 'partidas', 'mayor_m', 'sub_p', 'activ', 'almacen', 'maquina', 'herram', 'ocurrencia'];
                
                campos.forEach(campo => {
                    const val = document.getElementById(`v_${campo}`).value;
                    const out = document.getElementById(`out_${campo}`);
                    
                    if (val.trim() === '') {
                        out.innerHTML = '<span style="color:#cbd5e1;">...</span>';
                    } else {
                        // Reemplazar saltos de línea por <br> para que se vea bien en HTML
                        out.innerHTML = val.replace(/\\n/g, '<br>');
                        out.style.color = '#1e293b';
                        out.style.fontWeight = '600';
                    }
                });
            }

            // --- SLIDER FINAL (PASO 11) ---
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
                handle.style.transition = 'left 0.3s ease'; progress.style.transition = 'width 0.3s ease';
                handle.style.left = '4px'; progress.style.width = '0px';
                setTimeout(() => { handle.style.transition = 'none'; progress.style.transition = 'none'; }, 300);
            }

            handle.addEventListener('mousedown', startDrag); document.addEventListener('mousemove', onDrag); document.addEventListener('mouseup', stopDrag);
            handle.addEventListener('touchstart', startDrag, {passive: true}); document.addEventListener('touchmove', onDrag, {passive: false}); document.addEventListener('touchend', stopDrag);

            function firmar() {
                handle.style.left = maxSlide + 'px'; progress.style.width = '100%'; handle.style.background = '#10b981';
                handle.innerHTML = '<i class="bi bi-check-lg"></i>'; document.getElementById('sliderText').innerText = "FIRMADO Y SELLADO";
                alert("Asiento N° 88 firmado con éxito. Queda registrado inmutablemente.");
                window.location.href = '/cuaderno';
            }
            
            sincronizarDatos(); // Carga inicial
        </script>
    </body>
    </html>
    """, numero_asiento=numero_asiento, fecha_hoy=fecha_hoy, menu_superior=menu_superior, nombre_completo=nombre_completo)
