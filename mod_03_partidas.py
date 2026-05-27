# =========================================================
# mod_03_partidas.py
# Módulo: 3.- Partidas Ejecutadas (Importación 3 Columnas + Auto-foco Inmediato)
# =========================================================

from flask import Blueprint

mod_03_bp = Blueprint('mod_03_partidas', __name__)

PARTIDAS_HTML = """
<style>
    /* Estilos del buscador predictivo */
    .dropdown-partidas { position: absolute; top: 100%; left: 0; right: 0; background: white; border: 1px solid #cbd5e1; border-radius: 0 0 12px 12px; max-height: 200px; overflow-y: auto; z-index: 1000; box-shadow: 0 10px 25px rgba(0,0,0,0.1); display: none; }
    .dropdown-item-p { padding: 10px 15px; cursor: pointer; border-bottom: 1px solid #f1f5f9; font-size: 13px; display: flex; gap: 10px; align-items: center; }
    .dropdown-item-p:hover, .dropdown-item-p.selected { background: #f0f9ff; color: #0263a0; font-weight: 600; }
    .badge-item { background: #1e293b; color: white; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; white-space: nowrap; }
    .badge-unidad { background: #e2e8f0; color: #475569; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; white-space: nowrap; margin-left: auto;}
    
    /* Estilos del Panel de Pegado Inteligente */
    .col-header { background: #f8fafc; border: 1px solid #cbd5e1; border-bottom: none; border-radius: 8px 8px 0 0; padding: 8px; text-align: center; font-size: 11px; font-weight: 800; color: #475569; letter-spacing: 0.5px; }
    .col-textarea { border-radius: 0 0 8px 8px; border: 1px solid #cbd5e1; font-size: 12px; line-height: 1.8; padding: 10px; resize: none; overflow-x: hidden; white-space: pre; background: #fff;}
    .col-textarea:focus { border-color: #0263a0; box-shadow: 0 0 0 3px rgba(2,99,160,0.1); outline: none; }
</style>

<div class="step-view" id="step3">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <div class="step-title mb-0">3.- Partidas Ejecutadas</div>
        <button type="button" class="btn btn-sm btn-outline-success rounded-pill fw-bold shadow-sm" onclick="abrirModalPegadoInteligente()">
            <i class="bi bi-file-earmark-spreadsheet"></i> Catálogo Base (Excel)
        </button>
    </div>
    
    <p class="text-muted small mb-3">Busque la partida y presione <b>Enter</b>, digite el metrado y vuelva a presionar <b>Enter</b>.</p>
    
    <div class="position-relative mb-4">
        <div class="input-group shadow-sm">
            <span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-primary"></i></span>
            <input type="text" class="form-control border-start-0 ps-0" id="buscadorPartidas" placeholder="Ej: 07.01 o Transporte..." autocomplete="off" onkeyup="manejarTeclasBuscador(event)" onfocus="filtrarCatalogo()" oninput="filtrarCatalogo()">
        </div>
        <div class="dropdown-partidas" id="dropdownPartidas"></div>
    </div>
    
    <div id="listaPartidasAgregadas" class="d-flex flex-column gap-2 req-step3 mb-3"></div>
    <input type="hidden" id="v_partidas" class="req-step3" value="">
</div>

<div class="modal fade" id="modalPegadoInteligente" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-xl">
        <div class="modal-content" style="border-radius: 20px; border: none; box-shadow: 0 25px 50px rgba(0,0,0,0.2);">
            <div class="modal-header border-0 bg-light pb-3">
                <h5 class="modal-title fw-bold text-dark"><i class="bi bi-layout-three-columns text-success me-2"></i> Alimentar Base de Partidas</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body p-4 bg-white">
                
                <p class="small text-muted mb-3 text-center">
                    <i class="bi bi-info-circle-fill text-primary"></i> 
                    Pegue las columnas desde el Expediente Técnico. <b>Si pega las 3 columnas juntas en el primer cuadro, el sistema las distribuirá automáticamente.</b>
                </p>

                <div class="row g-2 justify-content-center">
                    <div class="col-2">
                        <div class="col-header">1. ÍTEMS</div>
                        <textarea id="p_items" class="form-control col-textarea text-center fw-bold" rows="12" placeholder="Pegar..." onpaste="handleSmartPaste(event, 'p_items')" onscroll="sincronizarScroll('p_items')"></textarea>
                    </div>
                    <div class="col-7">
                        <div class="col-header">2. DESCRIPCIÓN DE PARTIDAS</div>
                        <textarea id="p_descs" class="form-control col-textarea fw-semibold text-dark" rows="12" placeholder="Pegar..." onpaste="handleSmartPaste(event, 'p_descs')" onscroll="sincronizarScroll('p_descs')"></textarea>
                    </div>
                    <div class="col-2">
                        <div class="col-header">3. UNIDADES</div>
                        <textarea id="p_unds" class="form-control col-textarea text-center" rows="12" placeholder="Pegar..." onpaste="handleSmartPaste(event, 'p_unds')" onscroll="sincronizarScroll('p_unds')"></textarea>
                    </div>
                </div>

            </div>
            <div class="modal-footer border-0 pt-0 bg-white d-flex justify-content-between">
                <button type="button" class="btn btn-light rounded-pill px-4 fw-bold" onclick="limpiarGrilla()">Limpiar Cuadros</button>
                <button type="button" class="btn btn-primary rounded-pill px-5 fw-bold shadow-sm" onclick="procesarGrillaMasiva()">Guardar en Memoria</button>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="modalMetrado" data-bs-backdrop="static" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-sm">
        <div class="modal-content" style="border-radius: 20px; border: 2px solid #0263a0; box-shadow: 0 20px 40px rgba(2,99,160,0.15);">
            <div class="modal-body p-4 text-center">
                <div class="badge-item mb-2" id="lbl_m_item">00.00</div>
                <h6 class="fw-bold text-dark mb-3" id="lbl_m_desc" style="line-height: 1.3;">Descripción de la Partida</h6>
                
                <div class="input-group input-group-lg mb-2 shadow-sm">
                    <input type="number" step="0.01" class="form-control text-center fw-bold" id="inputMetrado" placeholder="Opcional" onkeydown="if(event.key==='Enter'){event.preventDefault(); confirmarMetrado();}">
                    <span class="input-group-text bg-white fw-bold text-primary" id="lbl_m_und">UND</span>
                </div>
                <p class="small text-muted mb-0">Digite el avance y presione <b>Enter</b>.</p>
            </div>
        </div>
    </div>
</div>

<script>
    // ==========================================
    // INICIALIZACIÓN GLOBAL
    // ==========================================
    window.m3_lista = window.m3_lista || [];
    window.catalogoMaestro = window.catalogoMaestro || [];
    
    let partidaSeleccionadaTemporal = null;
    let indexSeleccionadoDropdown = -1;
    let miniModalInstance = null;

    // Corrección para que el Modal del Metrado se enfoque DE INMEDIATO sin la animación lenta de Bootstrap
    setTimeout(() => {
        const mPegado = document.getElementById('modalPegadoInteligente');
        const mMet = document.getElementById('modalMetrado');
        if(mPegado && mPegado.parentNode !== document.body) document.body.appendChild(mPegado);
        if(mMet && mMet.parentNode !== document.body) {
            document.body.appendChild(mMet);
            
            // Cuando se muestra, el foco ya estará ahí
            mMet.addEventListener('shown.bs.modal', function () { 
                document.getElementById('inputMetrado').focus(); 
            });
        }
    }, 500);

    // ==========================================
    // LÓGICA DE PEGADO INTELIGENTE (3 COLUMNAS)
    // ==========================================
    function abrirModalPegadoInteligente() { 
        new bootstrap.Modal(document.getElementById('modalPegadoInteligente')).show(); 
    }

    function sincronizarScroll(sourceId) {
        const source = document.getElementById(sourceId);
        const textareas = ['p_items', 'p_descs', 'p_unds'];
        textareas.forEach(id => {
            if(id !== sourceId) document.getElementById(id).scrollTop = source.scrollTop;
        });
    }

    function limpiarGrilla() {
        document.getElementById('p_items').value = '';
        document.getElementById('p_descs').value = '';
        document.getElementById('p_unds').value = '';
    }

    // El cerebro del pegado: Si pegas varias columnas con TAB, las divide en 3
    function handleSmartPaste(e, targetId) {
        let pasteData = (e.clipboardData || window.clipboardData).getData('text');
        
        if(pasteData.includes('\\t')) {
            e.preventDefault();
            const rows = pasteData.split('\\n');
            let i_arr=[], d_arr=[], u_arr=[];
            
            rows.forEach(row => {
                if(!row.trim()) return;
                const cols = row.split('\\t');
                
                // Si pega en la columna 1, asume que vienen las 3 columnas
                if (targetId === 'p_items') {
                    i_arr.push(cols[0] || ''); 
                    d_arr.push(cols[1] || ''); 
                    u_arr.push(cols[2] || ''); 
                } 
                // Si pega en la columna 2, asume que vienen Desc y Und
                else if (targetId === 'p_descs') {
                    d_arr.push(cols[0] || ''); 
                    u_arr.push(cols[1] || ''); 
                }
            });

            if (targetId === 'p_items') {
                if(i_arr.length) document.getElementById('p_items').value += (document.getElementById('p_items').value ? '\\n' : '') + i_arr.join('\\n');
                if(d_arr.length) document.getElementById('p_descs').value += (document.getElementById('p_descs').value ? '\\n' : '') + d_arr.join('\\n');
                if(u_arr.length) document.getElementById('p_unds').value  += (document.getElementById('p_unds').value ? '\\n' : '') + u_arr.join('\\n');
            } else if (targetId === 'p_descs') {
                if(d_arr.length) document.getElementById('p_descs').value += (document.getElementById('p_descs').value ? '\\n' : '') + d_arr.join('\\n');
                if(u_arr.length) document.getElementById('p_unds').value  += (document.getElementById('p_unds').value ? '\\n' : '') + u_arr.join('\\n');
            }
        }
    }

    function procesarGrillaMasiva() {
        const items = document.getElementById('p_items').value.split('\\n');
        const descs = document.getElementById('p_descs').value.split('\\n');
        const unds = document.getElementById('p_unds').value.split('\\n');
        
        let maxRows = Math.max(items.length, descs.length, unds.length);
        let count = 0;

        for(let i = 0; i < maxRows; i++) {
            let desc = (descs[i] || '').trim();
            if(!desc) continue; // Descripción obligatoria
            
            let item = (items[i] || '').trim() || '-';
            let und = (unds[i] || '').trim().toUpperCase() || 'GLB';

            // Guardar en el catálogo global para futuras búsquedas predictivas
            window.catalogoMaestro.push({ item: item, descripcion: desc, unidad: und });
            count++;
        }

        if(count > 0) {
            limpiarGrilla();
            bootstrap.Modal.getInstance(document.getElementById('modalPegadoInteligente')).hide();
            
            // Usamos la alerta elegante si está disponible
            if(typeof mostrarAlerta === 'function') {
                mostrarAlerta(`Se agregaron ${count} partidas al catálogo.`, 'success');
            }
        }
    }

    // ==========================================
    // BUSCADOR PREDICTIVO Y MINI MODAL (DOBLE ENTER)
    // ==========================================
    function filtrarCatalogo() {
        const input = document.getElementById('buscadorPartidas').value.toLowerCase();
        const dropdown = document.getElementById('dropdownPartidas');
        
        if(input === '' || window.catalogoMaestro.length === 0) {
            dropdown.style.display = 'none'; return;
        }

        const filtrados = window.catalogoMaestro.filter(p => p.item.toLowerCase().includes(input) || p.descripcion.toLowerCase().includes(input)).slice(0, 8);
        
        if(filtrados.length > 0) {
            dropdown.innerHTML = filtrados.map((p, idx) => `
                <div class="dropdown-item-p ${idx === 0 ? 'selected' : ''}" onclick="abrirMiniModal(${idx})" id="drop_item_${idx}">
                    <span class="badge-item">${p.item}</span>
                    <span class="text-truncate">${p.descripcion}</span>
                    <span class="badge-unidad">${p.unidad}</span>
                </div>
            `).join('');
            dropdown.style.display = 'block';
            indexSeleccionadoDropdown = 0;
            dropdown.dataset.filtrados = JSON.stringify(filtrados);
        } else {
            dropdown.style.display = 'none';
        }
    }

    function manejarTeclasBuscador(e) {
        const dropdown = document.getElementById('dropdownPartidas');
        if(dropdown.style.display === 'none') return;
        
        const items = dropdown.getElementsByClassName('dropdown-item-p');
        
        if (e.key === 'ArrowDown') {
            if (indexSeleccionadoDropdown < items.length - 1) indexSeleccionadoDropdown++;
            actualizarSeleccionDropdown(items);
        } else if (e.key === 'ArrowUp') {
            if (indexSeleccionadoDropdown > 0) indexSeleccionadoDropdown--;
            actualizarSeleccionDropdown(items);
        } else if (e.key === 'Enter') {
            e.preventDefault();
            abrirMiniModal(indexSeleccionadoDropdown);
        }
    }

    function actualizarSeleccionDropdown(items) {
        for(let i=0; i<items.length; i++) { items[i].classList.remove('selected'); }
        if(items[indexSeleccionadoDropdown]) {
            items[indexSeleccionadoDropdown].classList.add('selected');
            items[indexSeleccionadoDropdown].scrollIntoView({block: 'nearest'});
        }
    }

    function abrirMiniModal(indexFiltrado) {
        const dropdown = document.getElementById('dropdownPartidas');
        const filtrados = JSON.parse(dropdown.dataset.filtrados);
        partidaSeleccionadaTemporal = filtrados[indexFiltrado];
        
        document.getElementById('buscadorPartidas').value = '';
        dropdown.style.display = 'none';

        document.getElementById('lbl_m_item').innerText = partidaSeleccionadaTemporal.item;
        document.getElementById('lbl_m_desc').innerText = partidaSeleccionadaTemporal.descripcion;
        document.getElementById('lbl_m_und').innerText = partidaSeleccionadaTemporal.unidad;
        
        // Limpiamos el input
        const inputMet = document.getElementById('inputMetrado');
        inputMet.value = '';

        if(!miniModalInstance) miniModalInstance = new bootstrap.Modal(document.getElementById('modalMetrado'));
        miniModalInstance.show();
        
        // Truco para forzar el foco INMEDIATO sin esperar la animación
        setTimeout(() => { inputMet.focus(); }, 50);
    }

    function confirmarMetrado() {
        const metradoVal = document.getElementById('inputMetrado').value;
        
        // Añadimos a la lista del cuaderno
        window.m3_lista.push({
            item: partidaSeleccionadaTemporal.item,
            descripcion: partidaSeleccionadaTemporal.descripcion,
            unidad: partidaSeleccionadaTemporal.unidad,
            metrado: metradoVal !== '' ? parseFloat(metradoVal).toFixed(2) : ''
        });

        miniModalInstance.hide();
        renderizarPartidasEjecutadas();
        document.getElementById('v_partidas').value = "lleno"; 
        
        // Sincronizar el Cuaderno Físico
        if (typeof sincronizarDatos === "function") sincronizarDatos();
        
        // Regresa el foco al buscador inmediatamente
        setTimeout(() => { document.getElementById('buscadorPartidas').focus(); }, 150);
    }

    function eliminarPartidaEjecutada(index) { 
        window.m3_lista.splice(index, 1); 
        if(window.m3_lista.length === 0) document.getElementById('v_partidas').value = ""; 
        renderizarPartidasEjecutadas(); 
        if (typeof sincronizarDatos === "function") sincronizarDatos(); 
    }

    function renderizarPartidasEjecutadas() {
        const container = document.getElementById('listaPartidasAgregadas');
        container.innerHTML = window.m3_lista.map((p, index) => `
            <div class="bg-white border rounded-3 p-2 d-flex justify-content-between align-items-center shadow-sm" style="border-left: 4px solid #0263a0 !important;">
                <div class="d-flex align-items-center gap-2 text-truncate" style="max-width: 350px;">
                    <span class="badge-item">${p.item}</span>
                    <span class="small fw-semibold text-truncate" title="${p.descripcion}">${p.descripcion}</span>
                </div>
                <div class="d-flex align-items-center gap-2">
                    <span class="fw-bold text-dark fs-6">${p.metrado ? p.metrado : '-'} <small class="text-muted" style="font-size:10px;">${p.unidad}</small></span>
                    <button type="button" class="btn btn-sm text-danger border-0 ms-2" onclick="eliminarPartidaEjecutada(${index})"><i class="bi bi-trash"></i></button>
                </div>
            </div>
        `).join('');
    }
</script>
"""
