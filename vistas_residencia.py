# =========================================================
# vistas_residencia.py
# Módulo: Llenado por Pasos (Stepper Dinámico y Termómetros)
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
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        
        <style>
            :root { --apple-text: #1d1d1f; --bg-color: #fbfbfd; --nav-height: 52px; }
            body { font-family: 'Inter', sans-serif; background-color: var(--bg-color); color: var(--apple-text); overflow-x: hidden; padding-bottom: 90px;}
            
            /* Contenedor del Stepper Superior Fijo */
            .stepper-container {
                position: fixed; top: var(--nav-height); left: 0; width: 100%;
                background: rgba(255,255,255,0.95); backdrop-filter: blur(10px);
                border-bottom: 1px solid rgba(0,0,0,0.1); z-index: 900;
                padding: 10px 15px; overflow-x: auto; white-space: nowrap;
                display: flex; gap: 10px; scroll-behavior: smooth;
                -ms-overflow-style: none; scrollbar-width: none; /* Ocultar scrollbar */
            }
            .stepper-container::-webkit-scrollbar { display: none; }
            
            /* Botones Termómetro */
            .step-btn {
                border: 1px solid #cbd5e1; border-radius: 20px; padding: 8px 16px;
                font-size: 12px; font-weight: 600; color: #475569; background: #f8fafc;
                cursor: pointer; transition: transform 0.2s; position: relative; overflow: hidden;
            }
            .step-btn.active { border-color: #0f172a; color: #fff; transform: scale(1.05); box-shadow: 0 4px 10px rgba(0,0,0,0.1);}
            .step-btn.omitted { background: #64748b !important; color: white !important; border-color: #475569; }
            
            /* Contenido Central */
            .main-workspace { max-width: 800px; margin: 130px auto 0 auto; padding: 0 15px; }
            .step-view { display: none; animation: fadeIn 0.4s ease; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid rgba(0,0,0,0.05);}
            .step-view.active { display: block; }
            @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

            /* Títulos y Formularios */
            .step-title { font-size: 20px; font-weight: 700; margin-bottom: 20px; color: #1d1d1f; border-bottom: 2px solid rgba(0,102,204,0.1); padding-bottom: 10px;}
            .form-label { font-size: 12px; font-weight: 600; color: #64748b; text-transform: uppercase; }
            .form-control, .form-select { border-radius: 12px; border: 1px solid #cbd5e1; padding: 12px; font-size: 14px; background: #f8fafc;}
            .form-control:focus, .form-select:focus { background: #fff; border-color: #0066cc; box-shadow: 0 0 0 3px rgba(0,102,204,0.1); }

            /* Barra Fija Inferior */
            .bottom-bar {
                position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(255,255,255,0.9);
                backdrop-filter: blur(10px); border-top: 1px solid rgba(0,0,0,0.1);
                padding: 15px 20px; z-index: 900; display: flex; justify-content: space-between; align-items: center;
            }

            /* Slider Final (Paso 11) */
            .slider-track { width: 100%; max-width: 350px; height: 56px; background: #f1f5f9; border-radius: 30px; position: relative; display: flex; align-items: center; justify-content: center; overflow: hidden; margin: 0 auto;}
            .slider-text { font-size: 12px; font-weight: 700; color: #64748b; text-transform: uppercase; z-index: 1; pointer-events: none;}
            .slider-handle { width: 48px; height: 48px; background: #0f172a; color: #fff; border-radius: 50%; position: absolute; left: 4px; display: flex; align-items: center; justify-content: center; z-index: 2; cursor: grab;}
            .slider-progress { position: absolute; left: 0; top: 0; height: 100%; background: rgba(0, 102, 204, 0.1); width: 0; pointer-events: none; }
        </style>
    </head>
    <body>

        {{ menu_superior | safe }}

        <div class="stepper-container" id="stepperBar">
            <button class="step-btn active" id="btnStep1" onclick="jumpToStep(1)" title="Faltan datos">1. Clima</button>
            <button class="step-btn" id="btnStep2" onclick="jumpToStep(2)" title="Faltan datos">2. Personal</button>
            <button class="step-btn" id="btnStep3" onclick="jumpToStep(3)" title="Faltan datos">3. Partidas</button>
            <button class="step-btn" id="btnStep4" onclick="jumpToStep(4)" title="Faltan datos">4. Mayor Metrado</button>
            <button class="step-btn" id="btnStep5" onclick="jumpToStep(5)" title="Faltan datos">5. Sub Partidas</button>
            <button class="step-btn" id="btnStep6" onclick="jumpToStep(6)" title="Faltan datos">6. Actividades</button>
            <button class="step-btn" id="btnStep7" onclick="jumpToStep(7)" title="Faltan datos">7. Almacén</button>
            <button class="step-btn" id="btnStep8" onclick="jumpToStep(8)" title="Faltan datos">8. Maquinaria</button>
            <button class="step-btn" id="btnStep9" onclick="jumpToStep(9)" title="Faltan datos">9. Herramientas</button>
            <button class="step-btn" id="btnStep10" onclick="jumpToStep(10)" title="Faltan datos">10. Ocurrencias</button>
            <button class="step-btn text-primary border-primary" id="btnStep11" onclick="jumpToStep(11)"><i class="bi bi-eye-fill"></i> Resumen Final</button>
        </div>

        <div class="main-workspace">
            <div class="d-flex justify-content-between mb-3 px-2">
                <h6 class="text-primary fw-bold mb-0">Asiento N° {{ numero_asiento }}</h6>
                <span class="text-muted small">{{ fecha_hoy }}</span>
            </div>

            <form id="formResidencia" oninput="calculateProgress()">
                
                <div class="step-view active" id="step1">
                    <div class="step-title">1. Condiciones del Entorno (Clima)</div>
                    <div class="row g-3">
                        <div class="col-sm-6">
                            <label class="form-label">Mañana (07:00 - 12:00)</label>
                            <select class="form-select req-step1"><option value="">Seleccione...</option><option value="Soleado">Soleado</option><option value="Lluvia">Lluvia</option></select>
                        </div>
                        <div class="col-sm-6">
                            <label class="form-label">Tarde (13:00 - 18:00)</label>
                            <select class="form-select req-step1"><option value="">Seleccione...</option><option value="Soleado">Soleado</option><option value="Lluvia">Lluvia</option></select>
                        </div>
                        <div class="col-12">
                            <label class="form-label">Impacto en la Obra</label>
                            <select class="form-select req-step1"><option value="">Seleccione...</option><option value="100%">Trabajo al 100%</option><option value="Parcial">Restricción Parcial</option></select>
                        </div>
                    </div>
                </div>

                <div class="step-view" id="step2">
                    <div class="step-title">2. Personal de Obra</div>
                    <div class="row g-3">
                        <div class="col-4"><label class="form-label">Operarios</label><input type="number" class="form-control req-step2" placeholder="0"></div>
                        <div class="col-4"><label class="form-label">Oficiales</label><input type="number" class="form-control req-step2" placeholder="0"></div>
                        <div class="col-4"><label class="form-label">Peones</label><input type="number" class="form-control req-step2" placeholder="0"></div>
                        <div class="col-6"><label class="form-label">Mecánicos</label><input type="number" class="form-control req-step2" placeholder="0"></div>
                        <div class="col-6"><label class="form-label">Controladores</label><input type="number" class="form-control req-step2" placeholder="0"></div>
                        <div class="col-12"><label class="form-label">Personal Clave (G.G.)</label><input type="text" class="form-control req-step2" placeholder="Ej: Residente, Especialista..."></div>
                    </div>
                </div>

                <div class="step-view" id="step3"><div class="step-title">3. Partidas Ejecutadas</div><textarea class="form-control req-step3" rows="5" placeholder="Registre las partidas y metrados..."></textarea></div>
                <div class="step-view" id="step4"><div class="step-title">4. Partidas Mayor Metrado</div><textarea class="form-control req-step4" rows="5" placeholder="Registre excesos de metrado..."></textarea></div>
                <div class="step-view" id="step5"><div class="step-title">5. Sub Partidas Ejecutadas</div><textarea class="form-control req-step5" rows="5" placeholder="Sub partidas..."></textarea></div>
                <div class="step-view" id="step6"><div class="step-title">6. Actividades Ejecutadas</div><textarea class="form-control req-step6" rows="5" placeholder="Diario de actividades operativas..."></textarea></div>

                <div class="step-view" id="step7">
                    <div class="step-title">7. Movimiento de Almacén</div>
                    <label class="form-label">Ingresos y Salidas de Materiales</label>
                    <textarea class="form-control req-step7 mb-3" rows="3" placeholder="Ej: Ingreso 500 bolsas cemento. Salida: 200 bolsas..."></textarea>
                    <label class="form-label">Combustible</label>
                    <textarea class="form-control req-step7" rows="2" placeholder="Ej: Ingreso 0, Salida 150 Gln Diesel B5..."></textarea>
                </div>

                <div class="step-view" id="step8">
                    <div class="step-title">8. Maquinarias, Vehículos y Equipos</div>
                    <textarea class="form-control req-step8" rows="6" placeholder="Detalle maquinaria del GORE Puno y maquinaria alquilada con sus respectivas Horas Máquina..."></textarea>
                </div>

                <div class="step-view" id="step9">
                    <div class="step-title">9. Herramientas Manuales</div>
                    <div class="form-check mb-2"><input class="form-check-input req-step9" type="checkbox" id="h1" value="Palas" checked><label class="form-check-label" for="h1">Palas de acero</label></div>
                    <div class="form-check mb-2"><input class="form-check-input req-step9" type="checkbox" id="h2" value="Picos" checked><label class="form-check-label" for="h2">Picos</label></div>
                    <div class="form-check mb-2"><input class="form-check-input req-step9" type="checkbox" id="h3" value="Buguies" checked><label class="form-check-label" for="h3">Buguies / Carretillas</label></div>
                </div>

                <div class="step-view" id="step10">
                    <div class="step-title text-danger">10. Ocurrencias, Conocimientos y Otros</div>
                    <textarea class="form-control border-danger req-step10" rows="6" placeholder="Redacción libre legal..."></textarea>
                </div>

                <div class="step-view" id="step11">
                    <div class="step-title text-success"><i class="bi bi-check-circle-fill"></i> 11. Resumen y Firma</div>
                    <div class="bg-light p-3 rounded-3 mb-4 border" style="font-size:13px; max-height: 250px; overflow-y: auto;" id="resumenVista">
                        <p class="text-muted text-center mt-3">Al llegar a este paso, aquí se mostrará el texto completo generado.</p>
                    </div>
                    
                    <div class="slider-track" id="sliderTrack">
                        <div class="slider-progress" id="sliderProgress"></div>
                        <div class="slider-text" id="sliderText">Deslizar para Firmar</div>
                        <div class="slider-handle" id="sliderHandle"><i class="bi bi-lock-fill"></i></div>
                    </div>
                </div>

            </form>
        </div>

        <div class="bottom-bar">
            <button type="button" class="btn btn-light border text-muted fw-bold" id="btnOmitir" onclick="omitirPaso()">
                <i class="bi bi-skip-forward-fill"></i> Omitir
            </button>
            <div id="indicadorGuardado" class="small text-muted fw-semibold d-none d-sm-block"><i class="bi bi-cloud-arrow-up"></i> Autoguardado</div>
            <button type="button" class="btn btn-dark fw-bold px-4" id="btnSiguiente" onclick="siguientePaso()">
                Guardar y Continuar <i class="bi bi-arrow-right"></i>
            </button>
        </div>

        <script>
            let currentStep = 1;
            const totalSteps = 11;
            
            // Función para cambiar de vista suavemente y hacer Guardado Silencioso
            function jumpToStep(stepIndex) {
                // Guardado Silencioso en memoria local (simulado)
                document.getElementById('indicadorGuardado').innerHTML = '<i class="bi bi-check2-all text-success"></i> Guardado';
                setTimeout(() => { document.getElementById('indicadorGuardado').innerHTML = '<i class="bi bi-cloud-arrow-up"></i> Autoguardado'; }, 2000);

                // Ocultar actual
                document.getElementById(`step${currentStep}`).classList.remove('active');
                document.getElementById(`btnStep${currentStep}`).classList.remove('active');
                if(currentStep !== 11) document.getElementById(`btnStep${currentStep}`).style.color = "#475569"; // Retorna al color base si no es 100%
                
                // Mostrar nuevo
                currentStep = stepIndex;
                document.getElementById(`step${currentStep}`).classList.add('active');
                document.getElementById(`btnStep${currentStep}`).classList.add('active');
                document.getElementById(`btnStep${currentStep}`).style.color = "#fff";
                
                // Centrar el botón superior en el celular (Scroll automático del navbar)
                const btnObj = document.getElementById(`btnStep${currentStep}`);
                document.getElementById('stepperBar').scrollLeft = btnObj.offsetLeft - 50;

                // Lógica de botones inferiores
                if (currentStep === 11) {
                    document.querySelector('.bottom-bar').style.display = 'none'; // Oculta controles inferiores en la firma
                    generarResumen();
                } else {
                    document.querySelector('.bottom-bar').style.display = 'flex';
                }

                calculateProgress(); // Refrescar colores
            }

            function siguientePaso() {
                if(currentStep < totalSteps) jumpToStep(currentStep + 1);
            }

            function omitirPaso() {
                // Rellenar automáticamente con la frase de omisión
                const inputsText = document.querySelectorAll(`.req-step${currentStep}`);
                inputsText.forEach(inp => {
                    if (inp.tagName === 'TEXTAREA' || inp.type === 'text') inp.value = "SIN NOVEDAD EN LA JORNADA";
                });
                
                // Marcar botón superior como Omitido (Gris)
                document.getElementById(`btnStep${currentStep}`).classList.add('omitted');
                document.getElementById(`btnStep${currentStep}`).title = "Paso Omitido";
                
                siguientePaso();
            }

            // --- LÓGICA DEL TERMÓMETRO EN LOS BOTONES ---
            function calculateProgress() {
                // Iteramos por los 10 pasos para medir qué porcentaje están llenos
                for (let i = 1; i <= 10; i++) {
                    const inputs = document.querySelectorAll(`.req-step${i}`);
                    if (inputs.length === 0) continue;

                    let llenos = 0;
                    inputs.forEach(inp => {
                        if ((inp.type === 'checkbox' && inp.checked) || (inp.value.trim() !== '' && inp.value.trim() !== '0')) {
                            llenos++;
                        }
                    });

                    let porcentaje = Math.round((llenos / inputs.length) * 100);
                    let btn = document.getElementById(`btnStep${i}`);
                    
                    // Si no está omitido, aplicamos el fondo degradado (Termómetro)
                    if (!btn.classList.contains('omitted')) {
                        // El color se pinta de Izquierda a Derecha. Azul si hay datos, gris si está vacío.
                        btn.style.background = `linear-gradient(to right, #bfdbfe ${porcentaje}%, #f8fafc ${porcentaje}%)`;
                        
                        // Tooltip dinámico al poner el mouse
                        btn.title = porcentaje === 100 ? "Completado ✅" : `Progreso: ${porcentaje}%`;
                        
                        // Si está al 100%, borde verde
                        if(porcentaje === 100 && !btn.classList.contains('active')) {
                            btn.style.borderColor = '#10b981'; // Verde
                        } else {
                            btn.style.borderColor = '#cbd5e1'; // Gris normal
                        }
                    }
                }
            }

            function generarResumen() {
                document.getElementById('resumenVista').innerHTML = `
                    <b>1. Clima:</b> ${document.querySelectorAll('.req-step1')[0].value || 'No registrado'} <br>
                    <b>3. Partidas:</b> ${document.querySelectorAll('.req-step3')[0].value || 'No registrado'} <br>
                    <b>10. Ocurrencias:</b> ${document.querySelectorAll('.req-step10')[0].value || 'No registrado'} <br>
                    <i>(Nota: El resumen capturará toda la data ingresada para auditoría final).</i>
                `;
            }

            // --- LÓGICA DEL SLIDER FINAL (PASO 11) ---
            const handle = document.getElementById('sliderHandle');
            const track = document.getElementById('sliderTrack');
            const progress = document.getElementById('sliderProgress');
            let isDragging = false, startX = 0, maxSlide = 0;

            function calcLimits() { maxSlide = track.clientWidth - handle.clientWidth - 8; }
            window.addEventListener('resize', calcLimits);
            setTimeout(calcLimits, 500);

            function startDrag(e) { isDragging = true; startX = (e.clientX || e.touches[0].clientX) - handle.offsetLeft; calcLimits(); }
            function onDrag(e) {
                if (!isDragging) return;
                let clientX = e.clientX || e.touches[0].clientX;
                let left = clientX - startX;
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
                handle.innerHTML = '<i class="bi bi-check-lg"></i>'; document.getElementById('sliderText').innerText = "FIRMADO LEGALMENTE";
                alert("¡Asiento N° 88 firmado con éxito!");
                window.location.href = '/cuaderno';
            }
            
            // Inicializar el porcentaje al cargar
            calculateProgress();
        </script>
    </body>
    </html>
    """, numero_asiento=numero_asiento, fecha_hoy=fecha_hoy, menu_superior=menu_superior)
