# =========================================================
# mod_03_partidas.py
# Módulo: 3.- Partidas Ejecutadas (Motor Doble Enter + Excel)
# =========================================================

from flask import Blueprint

mod_03_bp = Blueprint('mod_03_partidas', __name__)

PARTIDAS_HTML = """
<style>
    /* Estilos locales para el buscador predictivo */
    .dropdown-partidas { position: absolute; top: 100%; left: 0; right: 0; background: white; border: 1px solid #cbd5e1; border-radius: 0 0 12px 12px; max-height: 200px; overflow-y: auto; z-index: 1000; box-shadow: 0 10px 25px rgba(0,0,0,0.1); display: none; }
    .dropdown-item-p { padding: 10px 15px; cursor: pointer; border-bottom: 1px solid #f1f5f9; font-size: 13px; display: flex; gap: 10px; align-items: center; }
    .dropdown-item-p:hover, .dropdown-item-p.selected { background: #f0f9ff; color: #0263a0; font-weight: 600; }
    .badge-item { background: #1e293b; color: white; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; white-space: nowrap; }
    .badge-unidad { background: #e2e8f0; color: #475569; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; white-space: nowrap; margin-left: auto;}
</style>

<div class="step-view" id="step3">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <div class="step-title mb-0">3.- Partidas Ejecutadas</div>
        <button type="button" class="btn btn-sm btn-outline-success rounded-pill fw-bold shadow-sm" onclick="abrirModalCatalogo()">
            <i class="bi bi-file-earmark-excel"></i> Cargar Catálogo (Excel)
        </button>
    </div>
    
    <p class="text-muted small mb-3">Busque la partida y presione <b>Enter</b>. Digite el metrado y presione <b>Enter</b> nuevamente.</p>
    
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

<div class="modal fade" id="modalCatalogo" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content" style="border-radius: 20px;">
            <div class="modal-header border-0 pb-0">
                <h5 class="modal-title fw-bold text-success"><i class="bi bi-table"></i> Importar Catálogo Base</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <p class="small text-muted mb-2">Copie las 3 columnas de su Excel (<b>1. Ítem | 2. Partida | 3. Unidad</b>) y pegue aquí:</p>
                <textarea id="textoCatalogoExcel" class="form-control bg-light" rows="10" placeholder="07.01    TRANSPORTE DE MATERIAL GRANULAR PARA D<=1KM    M3-KM"></textarea>
            </div>
            <div class="modal-footer border-0 pt-0">
                <button type="button" class="btn btn-light rounded-pill px-4" data-bs-dismiss="modal">Cancelar</button>
                <button type="button" class="btn btn-success rounded-pill px-4 fw-bold" onclick="procesarCatalogo()">Guardar Catálogo</button>
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
                    <input type="number" step="0.01" class="form-control text-center fw-bold" id="inputMetrado" placeholder="0.00" onkeydown="if(event.key==='Enter'){event.preventDefault(); confirmarMetrado();}">
                    <span class="input-group-text bg-white fw-bold text-primary" id="lbl_m_und">UND</span>
                </div>
                <p class="small text-muted mb-0">Presione <b>Enter</b> para guardar.</p>
            </div>
        </div>
    </div>
</div>

<script>
    // Variables Globales del Módulo 3
    let catalogoMaestro = []; 
    let partidasEjecutadas = []; 
    let partidaSeleccionadaTemporal = null;
    let indexSeleccionadoDropdown = -1;

    // 1. Lógica del Catálogo Excel
    function abrirModalCatalogo() { 
        document.getElementById('textoCatalogoExcel').value = ''; 
        new bootstrap.Modal(document.getElementById('modalCatalogo')).show(); 
    }

    function procesarCatalogo() {
        const rawData = document.getElementById('textoCatalogoExcel').value;
        if(!rawData.trim()) { mostrarAlerta("No hay datos para procesar", "error"); return; }
        
        const rows = rawData.split('\\n'); 
        let count = 0;
        catalogoMaestro = []; // Limpiamos el catálogo anterior

        rows.forEach(row => {
            if(!row.trim()) return;
            const cols = row.split('\\t'); // Separación por tabulaciones de Excel
            if(cols.length >= 3) {
                catalogoMaestro.push({ item: cols[0].trim(), descripcion: cols[1].trim(), unidad: cols[2].trim() });
                count++;
            } else if (cols.length === 2) {
                catalogoMaestro.push({ item: cols[0].trim(), descripcion: cols[1].trim(), unidad: 'GLB' });
                count++;
            }
        });
        
        if(count > 0) { 
            mostrarAlerta(`Se importaron ${count} partidas al catálogo.`, "success");
        } else {
            mostrarAlerta("Formato incorrecto. Asegúrese de copiar las 3 columnas.", "error");
        }
        bootstrap.Modal.getInstance(document.getElementById('modalCatalogo')).hide();
    }

    // 2. Lógica del Buscador Predictivo
    function filtrarCatalogo() {
        const input = document.getElementById('buscadorPartidas').value.toLowerCase();
        const dropdown = document.getElementById('dropdownPartidas');
        
        if(input === '' || catalogoMaestro.length === 0) {
            dropdown.style.display = 'none';
            return;
        }

        const filtrados = catalogoMaestro.filter(p => p.item.toLowerCase().includes(input) || p.descripcion.toLowerCase().includes(input)).slice(0, 10);
        
        if(filtrados.length > 0) {
            dropdown.innerHTML = filtrados.map((p, idx) => `
                <div class="dropdown-item-p ${idx === 0 ? 'selected' : ''}" onclick="abrirMiniModal(${idx})" id="drop_item_${idx}">
                    <span class="badge-item">${p.item}</span>
                    <span class="text-truncate">${p.descripcion}</span>
                    <span class="badge-unidad">${p.unidad}</span>
                </div>
            `).join('');
            dropdown.style.display = 'block';
            indexSeleccionadoDropdown = 0; // Por defecto el primero
            
            // Guardamos temporalmente la lista filtrada para usarla con Enter
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
        for(let i=0; i<items.length; i++) {
            items[i].classList.remove('selected');
        }
        if(items[indexSeleccionadoDropdown]) {
            items[indexSeleccionadoDropdown].classList.add('selected');
            items[indexSeleccionadoDropdown].scrollIntoView({block: 'nearest'});
        }
    }

    // 3. Lógica del Mini Modal (Doble Enter)
    let miniModalInstance = null;

    function abrirMiniModal(indexFiltrado) {
        const dropdown = document.getElementById('dropdownPartidas');
        const filtrados = JSON.parse(dropdown.dataset.filtrados);
        partidaSeleccionadaTemporal = filtrados[indexFiltrado];
        
        // Limpiamos buscador y cerramos dropdown
        document.getElementById('buscadorPartidas').value = '';
        dropdown.style.display = 'none';

        // Llenamos el Mini Modal
        document.getElementById('lbl_m_item').innerText = partidaSeleccionadaTemporal.item;
        document.getElementById('lbl_m_desc').innerText = partidaSeleccionadaTemporal.descripcion;
        document.getElementById('lbl_m_und').innerText = partidaSeleccionadaTemporal.unidad;
        document.getElementById('inputMetrado').value = '';

        // Mostramos Modal y Auto-Foco
        if(!miniModalInstance) miniModalInstance = new bootstrap.Modal(document.getElementById('modalMetrado'));
        miniModalInstance.show();
        
        setTimeout(() => { document.getElementById('inputMetrado').focus(); }, 400);
    }

    function confirmarMetrado() {
        const metradoVal = document.getElementById('inputMetrado').value;
        if(metradoVal === '') { mostrarAlerta("Ingrese un metrado válido.", "error"); return; }
        
        partidasEjecutadas.push({
            item: partidaSeleccionadaTemporal.item,
            descripcion: partidaSeleccionadaTemporal.descripcion,
            unidad: partidaSeleccionadaTemporal.unidad,
            metrado: parseFloat(metradoVal).toFixed(2)
        });

        miniModalInstance.hide();
        renderizarPartidasEjecutadas();
        document.getElementById('v_partidas').value = "lleno"; 
        
        if (typeof sincronizarDatos === "function") sincronizarDatos();
        
        // Regresa el foco al buscador para seguir tecleando
        setTimeout(() => { document.getElementById('buscadorPartidas').focus(); }, 300);
    }

    function eliminarPartidaEjecutada(index) { 
        partidasEjecutadas.splice(index, 1); 
        if(partidasEjecutadas.length === 0) document.getElementById('v_partidas').value = ""; 
        renderizarPartidasEjecutadas(); 
        if (typeof sincronizarDatos === "function") sincronizarDatos(); 
    }

    function renderizarPartidasEjecutadas() {
        const container = document.getElementById('listaPartidasAgregadas');
        container.innerHTML = partidasEjecutadas.map((p, index) => `
            <div class="bg-white border rounded-3 p-2 d-flex justify-content-between align-items-center shadow-sm">
                <div class="d-flex align-items-center gap-2 text-truncate" style="max-width: 350px;">
                    <span class="badge-item">${p.item}</span>
                    <span class="small fw-semibold text-truncate">${p.descripcion}</span>
                </div>
                <div class="d-flex align-items-center gap-2">
                    <span class="fw-bold text-dark">${p.metrado} <small class="text-muted">${p.unidad}</small></span>
                    <button type="button" class="btn btn-sm text-danger border-0" onclick="eliminarPartidaEjecutada(${index})"><i class="bi bi-trash"></i></button>
                </div>
            </div>
        `).join('');
    }
</script>
"""
