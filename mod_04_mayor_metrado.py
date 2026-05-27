# =========================================================
# mod_04_mayor_metrado.py
# Módulo: 4.- Mayor Metrado (Doble Enter + Metrado Opcional)
# =========================================================

from flask import Blueprint

mod_04_bp = Blueprint('mod_04_mayor_metrado', __name__)

MAYOR_METRADO_HTML = """
<style>
    /* Estilos del buscador predictivo heredados (aislados al contenedor) */
    .dropdown-partidas { position: absolute; top: 100%; left: 0; right: 0; background: white; border: 1px solid #cbd5e1; border-radius: 0 0 12px 12px; max-height: 200px; overflow-y: auto; z-index: 1000; box-shadow: 0 10px 25px rgba(0,0,0,0.1); display: none; }
    .dropdown-item-p { padding: 10px 15px; cursor: pointer; border-bottom: 1px solid #f1f5f9; font-size: 13px; display: flex; gap: 10px; align-items: center; }
    .dropdown-item-p:hover, .dropdown-item-p.selected { background: #f0f9ff; color: #0263a0; font-weight: 600; }
    .badge-item { background: #1e293b; color: white; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; white-space: nowrap; }
    .badge-unidad { background: #e2e8f0; color: #475569; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; white-space: nowrap; margin-left: auto;}
</style>

<div class="step-view" id="step4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <div class="step-title mb-0">4.- Mayor Metrado</div>
        <button type="button" class="btn btn-sm btn-outline-success rounded-pill fw-bold shadow-sm" onclick="abrirCatalogoGlobal()">
            <i class="bi bi-journal-text"></i> Base Global de Partidas
        </button>
    </div>
    
    <p class="text-muted small mb-3">Busque la partida ejecutada como mayor metrado y presione <b>Enter</b>. Digite el metrado y presione <b>Enter</b> nuevamente. <span class="text-primary fw-bold">(El metrado es opcional).</span></p>
    
    <div class="position-relative mb-4">
        <div class="input-group shadow-sm">
            <span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-primary"></i></span>
            <input type="text" class="form-control border-start-0 ps-0" id="m4_buscador" placeholder="Ej: 07.01 o Transporte..." autocomplete="off" onkeyup="m4_teclas(event)" onfocus="m4_filtrar()" oninput="m4_filtrar()">
        </div>
        <div class="dropdown-partidas" id="m4_dropdown"></div>
    </div>
    
    <div id="m4_lista_ui" class="d-flex flex-column gap-2 mb-3"></div>
    <input type="hidden" id="v_mayor_m_status" class="req-step4" value="">
</div>

<div class="modal fade" id="m4_modal" data-bs-backdrop="static" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-sm">
        <div class="modal-content" style="border-radius: 20px; border: 2px solid #0263a0; box-shadow: 0 20px 40px rgba(2,99,160,0.15);">
            <div class="modal-body p-4 text-center">
                <div class="badge-item mb-2" id="m4_lbl_item">00.00</div>
                <h6 class="fw-bold text-dark mb-3" id="m4_lbl_desc" style="line-height: 1.3;">Descripción de la Partida</h6>
                
                <div class="input-group input-group-lg mb-2 shadow-sm">
                    <input type="number" step="0.01" class="form-control text-center fw-bold" id="m4_input" placeholder="Opcional" onkeydown="if(event.key==='Enter'){event.preventDefault(); m4_guardar();}">
                    <span class="input-group-text bg-white fw-bold text-primary" id="m4_lbl_und">UND</span>
                </div>
                <p class="small text-muted mb-0">Presione <b>Enter</b> para guardar.</p>
            </div>
        </div>
    </div>
</div>

<script>
    // Enganche al DOM para mover el modal y forzar Auto-Focus
    setTimeout(() => {
        const mMet4 = document.getElementById('m4_modal');
        if(mMet4 && mMet4.parentNode !== document.body) {
            document.body.appendChild(mMet4);
            
            // Evento oficial de Bootstrap para enfocar el cursor sin dar click
            mMet4.addEventListener('shown.bs.modal', function () {
                document.getElementById('m4_input').focus();
            });
        }
    }, 500);

    // Variables aisladas para el Módulo 4
    window.m4_lista = window.m4_lista || [];
    let m4_temp = null;
    let m4_idx = -1;
    let m4_modal_inst = null;

    // Buscador y Filtro M4
    function m4_filtrar() {
        const val = document.getElementById('m4_buscador').value.toLowerCase();
        const drop = document.getElementById('m4_dropdown');
        
        if(val === '' || !window.catalogoMaestro || window.catalogoMaestro.length === 0) {
            drop.style.display = 'none';
            return;
        }

        const filt = window.catalogoMaestro.filter(p => p.item.toLowerCase().includes(val) || p.descripcion.toLowerCase().includes(val)).slice(0, 8);
        
        if(filt.length > 0) {
            drop.innerHTML = filt.map((p, i) => `
                <div class="dropdown-item-p ${i === 0 ? 'selected' : ''}" onclick="m4_abrir(${i})">
                    <span class="badge-item">${p.item}</span>
                    <span class="text-truncate">${p.descripcion}</span>
                    <span class="badge-unidad">${p.unidad}</span>
                </div>
            `).join('');
            drop.style.display = 'block';
            m4_idx = 0;
            drop.dataset.filt = JSON.stringify(filt);
        } else {
            drop.style.display = 'none';
        }
    }

    // Navegación por teclado (Flechas y Enter) M4
    function m4_teclas(e) {
        const drop = document.getElementById('m4_dropdown');
        if(drop.style.display === 'none') return;
        
        const items = drop.getElementsByClassName('dropdown-item-p');
        
        if (e.key === 'ArrowDown') {
            if (m4_idx < items.length - 1) m4_idx++;
            m4_select(items);
        } else if (e.key === 'ArrowUp') {
            if (m4_idx > 0) m4_idx--;
            m4_select(items);
        } else if (e.key === 'Enter') {
            e.preventDefault();
            m4_abrir(m4_idx);
        }
    }

    function m4_select(items) {
        for(let i=0; i<items.length; i++) { items[i].classList.remove('selected'); }
        if(items[m4_idx]) {
            items[m4_idx].classList.add('selected');
            items[m4_idx].scrollIntoView({block: 'nearest'});
        }
    }

    // Abrir Modal de Metrado M4
    function m4_abrir(idx) {
        const f = JSON.parse(document.getElementById('m4_dropdown').dataset.filt);
        m4_temp = f[idx];
        
        document.getElementById('m4_buscador').value = '';
        document.getElementById('m4_dropdown').style.display = 'none';

        document.getElementById('m4_lbl_item').innerText = m4_temp.item;
        document.getElementById('m4_lbl_desc').innerText = m4_temp.descripcion;
        document.getElementById('m4_lbl_und').innerText = m4_temp.unidad;
        document.getElementById('m4_input').value = '';

        if(!m4_modal_inst) m4_modal_inst = new bootstrap.Modal(document.getElementById('m4_modal'));
        m4_modal_inst.show();
    }

    // Guardar (Soporta metrado vacío) M4
    function m4_guardar() {
        const val = document.getElementById('m4_input').value;
        
        if (!window.m4_lista) window.m4_lista = [];
        
        window.m4_lista.push({
            item: m4_temp.item,
            descripcion: m4_temp.descripcion,
            unidad: m4_temp.unidad,
            metrado: val !== '' ? parseFloat(val).toFixed(2) : ''
        });

        m4_modal_inst.hide();
        m4_render();
        document.getElementById('v_mayor_m_status').value = "lleno"; 
        
        // Sincronizar con Cuaderno Físico
        if (typeof sincronizarDatos === "function") sincronizarDatos();
        
        // Retornar foco al buscador
        setTimeout(() => { document.getElementById('m4_buscador').focus(); }, 300);
    }

    function m4_del(idx) { 
        window.m4_lista.splice(idx, 1); 
        if(window.m4_lista.length === 0) document.getElementById('v_mayor_m_status').value = "";
        m4_render(); 
        if (typeof sincronizarDatos === "function") sincronizarDatos(); 
    }

    // Dibujar tarjetas en pantalla M4
    function m4_render() {
        const container = document.getElementById('m4_lista_ui');
        container.innerHTML = window.m4_lista.map((p, index) => `
            <div class="bg-white border rounded-3 p-2 d-flex justify-content-between align-items-center shadow-sm" style="border-left: 4px solid #0263a0 !important;">
                <div class="d-flex align-items-center gap-2 text-truncate" style="max-width: 350px;">
                    <span class="badge-item">${p.item}</span>
                    <span class="small fw-semibold text-truncate" title="${p.descripcion}">${p.descripcion}</span>
                </div>
                <div class="d-flex align-items-center gap-2">
                    <span class="fw-bold text-dark fs-6">${p.metrado ? p.metrado : '-'} <small class="text-muted" style="font-size:10px;">${p.metrado ? p.unidad : ''}</small></span>
                    <button type="button" class="btn btn-sm text-danger border-0 ms-2" onclick="m4_del(${index})"><i class="bi bi-trash"></i></button>
                </div>
            </div>
        `).join('');
    }
</script>
"""
