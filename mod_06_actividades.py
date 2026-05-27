# =========================================================
# mod_06_actividades.py
# Módulo: 6.- Actividades Ejecutadas (Híbrido + Progresivas)
# =========================================================

from flask import Blueprint

mod_06_bp = Blueprint('mod_06_actividades', __name__)

ACTIVIDADES_HTML = """
<style>
    .dropdown-partidas { position: absolute; top: 100%; left: 0; right: 0; background: white; border: 1px solid #cbd5e1; border-radius: 0 0 12px 12px; max-height: 200px; overflow-y: auto; z-index: 1000; box-shadow: 0 10px 25px rgba(0,0,0,0.1); display: none; }
    .dropdown-item-p { padding: 10px 15px; cursor: pointer; border-bottom: 1px solid #f1f5f9; font-size: 13px; display: flex; gap: 10px; align-items: center; }
    .dropdown-item-p:hover, .dropdown-item-p.selected { background: #f0f9ff; color: #0263a0; font-weight: 600; }
    .badge-item { background: #1e293b; color: white; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; white-space: nowrap; }
    .badge-unidad { background: #e2e8f0; color: #475569; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; white-space: nowrap; margin-left: auto;}
    .excel-paste-zone { border: 2px dashed #cbd5e1; border-radius: 12px; padding: 10px; background: #f8fafc; text-align: center; color: #64748b; font-size: 12px; font-weight: 600; cursor: pointer; transition: 0.3s; margin-bottom: 15px;}
    .excel-paste-zone:hover { border-color: #0263a0; color: #0263a0; background: #f0f9ff;}
    .m6-btn-primary { background: linear-gradient(135deg, #0263a0, #0ea5e9); color: #fff; border: none; }
    .m6-chip { border: 1px solid #cbd5e1; border-radius: 999px; background: #fff; padding: 8px 12px; font-size: 12px; font-weight: 700; color: #334155; cursor: pointer; transition: 0.2s; }
    .m6-chip:hover { border-color: #0263a0; background: #f0f9ff; color: #0263a0; transform: translateY(-1px); }
    .m6-modal-soft { border: none; border-radius: 22px; box-shadow: 0 25px 60px rgba(15,23,42,0.22); overflow: hidden; }
</style>

<div class="step-view" id="step6">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <div class="step-title mb-0">6.- Actividades en Ejecución</div>
        <button type="button" class="btn btn-sm rounded-pill fw-bold shadow-sm px-3 m6-btn-primary" onclick="abrirModalMasivoM6()">
            <i class="bi bi-clipboard-plus me-1"></i> Carga masiva / partidas
        </button>
    </div>
    
    <p class="text-muted small mb-3">Escriba una actividad o selecciónela del catálogo y presione <b>Enter</b>. Luego avance con Enter por progresiva, metrado y unidad.</p>
    
    <div class="position-relative mb-4">
        <div class="input-group shadow-sm">
            <span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-primary"></i></span>
            <input type="text" class="form-control border-start-0 ps-0" id="m6_buscador" placeholder="Ej: Limpieza de cunetas o 07.01..." autocomplete="off" onkeyup="m6_teclas(event)" onfocus="m6_filtrar()" oninput="m6_filtrar()">
        </div>
        <div class="dropdown-partidas" id="m6_dropdown"></div>
    </div>
    
    <div id="m6_lista_ui" class="d-flex flex-column gap-2 mb-3"></div>
    <input type="hidden" id="v_actividades_status" class="req-step6" value="">
</div>

<div class="modal fade" id="m6_modal_masivo" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content m6-modal-soft">
            <div class="modal-header border-0 bg-light pb-3">
                <h5 class="modal-title fw-bold text-dark"><i class="bi bi-card-checklist text-primary me-2"></i> Registrar actividades</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body p-4 bg-white">
                <div class="excel-paste-zone" id="m6_pasteHint">
                    <i class="bi bi-clipboard-check fs-4 d-block mb-1"></i>
                    Copie actividades desde Excel y presione <b>Ctrl + V</b> aquí. <br>
                    <span class="fw-normal text-muted">Formato: Actividad | Progresiva opcional | Metrado opcional | Unidad opcional</span>
                </div>
                <div class="small text-muted fw-bold mb-2">Partidas registradas disponibles</div>
                <div id="m6_partidas_chips" class="d-flex flex-wrap gap-2"></div>
            </div>
            <div class="modal-footer border-0 pt-0 bg-white">
                <button type="button" class="btn btn-primary rounded-pill px-4 fw-bold" data-bs-dismiss="modal">Listo, continuar</button>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="m6_modal" data-bs-backdrop="static" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content" style="border-radius: 20px; border: 2px solid #0263a0; box-shadow: 0 20px 40px rgba(2,99,160,0.15);">
            <div class="modal-body p-4">
                <div class="text-center mb-3">
                    <span class="badge-item mb-2" id="m6_lbl_item">-</span>
                    <h5 class="fw-bold text-dark" style="line-height: 1.3;"><i class="bi bi-tools text-primary me-2"></i>Detalle de Actividad</h5>
                </div>
                
                <div class="mb-3">
                    <label class="form-label small fw-bold text-muted">Descripción de la Actividad</label>
                    <input type="text" class="form-control fw-bold bg-light" id="m6_input_desc" onkeydown="if(event.key==='Enter'){event.preventDefault(); document.getElementById('m6_input_prog').focus();}">
                </div>

                <div class="mb-3">
                    <label class="form-label small fw-bold text-muted">Progresiva / Ubicación <span class="text-primary fw-normal">(Opcional)</span></label>
                    <input type="text" class="form-control fw-semibold" id="m6_input_prog" placeholder="Ej: KM 10+000 a KM 10+500" onkeydown="if(event.key==='Enter'){event.preventDefault(); document.getElementById('m6_input_met').focus();}">
                </div>

                <div class="mb-3">
                    <label class="form-label small fw-bold text-muted">Metrado <span class="text-primary fw-normal">(Opcional)</span></label>
                    <div class="input-group shadow-sm">
                        <input type="number" step="0.01" class="form-control fw-bold" id="m6_input_met" placeholder="Opcional" onkeydown="if(event.key==='Enter'){event.preventDefault(); if(this.value.trim()===''){m6_guardar();}else{document.getElementById('m6_input_und').focus();}}">
                        <input type="text" class="form-control text-center" id="m6_input_und" placeholder="Und" style="max-width: 80px;" onkeydown="if(event.key==='Enter'){event.preventDefault(); m6_guardar();}">
                    </div>
                </div>
                
                <p class="text-center small text-muted mb-3">Enter avanza entre campos. Si el metrado queda vacío, se guarda directamente.</p>
                <button type="button" class="btn btn-dark w-100 rounded-pill fw-bold" onclick="m6_guardar()">Guardar Actividad</button>
            </div>
        </div>
    </div>
</div>

<script>
    // Configuración Z-Index y Auto-Focus
    setTimeout(() => {
        const mMas6 = document.getElementById('m6_modal_masivo');
        const mMet6 = document.getElementById('m6_modal');
        if(mMas6 && mMas6.parentNode !== document.body) document.body.appendChild(mMas6);
        if(mMet6 && mMet6.parentNode !== document.body) {
            document.body.appendChild(mMet6);
            mMet6.addEventListener('shown.bs.modal', function () {
                // Si la descripción está vacía, enfoca ahí, sino, salta a la progresiva.
                const desc = document.getElementById('m6_input_desc');
                if(desc.value.trim() === '') desc.focus();
                else document.getElementById('m6_input_prog').focus();
            });
        }
    }, 500);

    // Variables Módulo 6
    window.m6_lista = window.m6_lista || [];
    let m6_temp_item = "-";
    let m6_idx = -1;
    let m6_modal_inst = null;

    // Lógica Pegado Masivo Excel
    function abrirModalMasivoM6() {
        m6_render_partidas_registradas();
        document.getElementById('m6_pasteHint').innerHTML = `<i class="bi bi-clipboard-check fs-4 d-block mb-1"></i> Copie desde Excel y presione <b>Ctrl + V</b> aquí.`;
        document.getElementById('m6_pasteHint').style.borderColor = '#cbd5e1';
        document.getElementById('m6_pasteHint').style.backgroundColor = '#f8fafc';
        new bootstrap.Modal(document.getElementById('m6_modal_masivo')).show();
    }

    function m6_partidas_base() {
        const desdeM3 = Array.isArray(window.m3_lista) ? window.m3_lista : [];
        const desdeM4 = Array.isArray(window.m4_lista) ? window.m4_lista : [];
        const desdeM5 = Array.isArray(window.m5_lista) ? window.m5_lista : [];
        return [...desdeM3, ...desdeM4, ...desdeM5];
    }

    function m6_render_partidas_registradas() {
        const cont = document.getElementById('m6_partidas_chips');
        const partidas = m6_partidas_base();
        if(!cont) return;
        if(partidas.length === 0) {
            cont.innerHTML = `<div class="text-muted small">Aún no hay partidas registradas en los módulos 3, 4 o 5.</div>`;
            return;
        }
        cont.innerHTML = partidas.map((p, idx) => `
            <button type="button" class="m6-chip" onclick="m6_actividad_desde_partida(${idx})">
                ${p.item && p.item !== '-' ? `<span class="badge-item me-1">${p.item}</span>` : ''}
                ${p.descripcion}
            </button>
        `).join('');
    }

    function m6_actividad_desde_partida(idx) {
        const partida = m6_partidas_base()[idx];
        if(!partida) return;
        const texto = partida.item && partida.item !== '-' ? `${partida.item} ${partida.descripcion}` : partida.descripcion;
        m6_abrir_libre(texto);
        const modalMasivo = bootstrap.Modal.getInstance(document.getElementById('m6_modal_masivo'));
        if(modalMasivo) modalMasivo.hide();
    }

    document.addEventListener('paste', function(e) {
        const modalEl = document.getElementById('m6_modal_masivo');
        if (!modalEl || !modalEl.classList.contains('show')) return; 

        e.preventDefault();
        let pasteData = (e.clipboardData || window.clipboardData).getData('text');
        if(!pasteData.trim()) return;

        const rows = pasteData.split('\\n');
        let count = 0;

        rows.forEach(row => {
            if(!row.trim()) return;
            const cols = row.split('\\t'); 
            
            // Analizador inteligente de columnas
            let desc = cols[0] ? cols[0].trim() : '';
            let prog = cols[1] ? cols[1].trim() : '';
            let met = cols[2] ? cols[2].trim() : '';
            let und = cols[3] ? cols[3].trim() : (met ? 'GLB' : '');

            if(desc) {
                window.m6_lista.push({
                    item: '-',
                    descripcion: desc,
                    prog: prog,
                    metrado: met,
                    unidad: und.toUpperCase()
                });
                count++;
            }
        });

        if(count > 0) {
            m6_render();
            document.getElementById('v_actividades_status').value = "lleno";
            if (typeof sincronizarDatos === "function") sincronizarDatos();
            document.getElementById('m6_pasteHint').innerHTML = `<i class="bi bi-check-circle-fill text-success fs-4 d-block mb-1"></i> ¡Se importaron ${count} actividades con éxito!`;
            document.getElementById('m6_pasteHint').style.borderColor = '#10b981';
            document.getElementById('m6_pasteHint').style.backgroundColor = '#ecfdf5';
        }
    });

    // Buscador Híbrido (Predictivo + Libre)
    function m6_filtrar() {
        const val = document.getElementById('m6_buscador').value.toLowerCase();
        const drop = document.getElementById('m6_dropdown');
        
        if(val === '' || !window.catalogoMaestro || window.catalogoMaestro.length === 0) {
            drop.style.display = 'none';
            return;
        }

        const filt = window.catalogoMaestro.filter(p => p.item.toLowerCase().includes(val) || p.descripcion.toLowerCase().includes(val)).slice(0, 6);
        
        if(filt.length > 0) {
            drop.innerHTML = filt.map((p, i) => `
                <div class="dropdown-item-p ${i === 0 ? 'selected' : ''}" onclick="m6_abrir_desde_catalogo(${i})">
                    <span class="badge-item">${p.item}</span>
                    <span class="text-truncate">${p.descripcion}</span>
                    <span class="badge-unidad">${p.unidad}</span>
                </div>
            `).join('');
            drop.style.display = 'block';
            m6_idx = 0;
            drop.dataset.filt = JSON.stringify(filt);
        } else {
            drop.style.display = 'none';
        }
    }

    function m6_teclas(e) {
        const val = document.getElementById('m6_buscador').value.trim();
        const drop = document.getElementById('m6_dropdown');
        const items = drop.getElementsByClassName('dropdown-item-p');
        
        if (e.key === 'ArrowDown' && drop.style.display === 'block') {
            if (m6_idx < items.length - 1) m6_idx++;
            m6_select(items);
        } else if (e.key === 'ArrowUp' && drop.style.display === 'block') {
            if (m6_idx > 0) m6_idx--;
            m6_select(items);
        } else if (e.key === 'Enter') {
            e.preventDefault();
            // Lógica híbrida: Si hay menú abierto y algo seleccionado, úsalo. Si no, usa el texto libre.
            if(drop.style.display === 'block' && m6_idx >= 0 && items.length > 0) {
                m6_abrir_desde_catalogo(m6_idx);
            } else if (val !== '') {
                m6_abrir_libre(val);
            }
        }
    }

    function m6_select(items) {
        for(let i=0; i<items.length; i++) { items[i].classList.remove('selected'); }
        if(items[m6_idx]) { items[m6_idx].classList.add('selected'); items[m6_idx].scrollIntoView({block: 'nearest'}); }
    }

    // Apertura del modal desde Catálogo
    function m6_abrir_desde_catalogo(idx) {
        const f = JSON.parse(document.getElementById('m6_dropdown').dataset.filt);
        const seleccionado = f[idx];
        
        m6_temp_item = seleccionado.item;
        document.getElementById('m6_lbl_item').innerText = seleccionado.item;
        document.getElementById('m6_input_desc').value = seleccionado.descripcion;
        document.getElementById('m6_input_und').value = seleccionado.unidad;
        
        prepararYMostrarModalM6();
    }

    // Apertura del modal desde Texto Libre
    function m6_abrir_libre(texto) {
        m6_temp_item = '-';
        document.getElementById('m6_lbl_item').innerText = 'LIBRE';
        document.getElementById('m6_input_desc').value = texto;
        document.getElementById('m6_input_und').value = 'GLB'; // Por defecto global
        
        prepararYMostrarModalM6();
    }

    function prepararYMostrarModalM6() {
        document.getElementById('m6_buscador').value = '';
        document.getElementById('m6_dropdown').style.display = 'none';
        
        document.getElementById('m6_input_prog').value = '';
        document.getElementById('m6_input_met').value = '';

        if(!m6_modal_inst) m6_modal_inst = new bootstrap.Modal(document.getElementById('m6_modal'));
        m6_modal_inst.show();
    }

    function m6_guardar() {
        const desc = document.getElementById('m6_input_desc').value.trim();
        const prog = document.getElementById('m6_input_prog').value.trim();
        const met = document.getElementById('m6_input_met').value;
        const und = document.getElementById('m6_input_und').value.trim().toUpperCase();
        
        if(desc === '') { alert("La descripción es obligatoria."); return; }
        
        window.m6_lista.push({
            item: m6_temp_item,
            descripcion: desc,
            prog: prog,
            unidad: und,
            metrado: met !== '' ? parseFloat(met).toFixed(2) : ''
        });

        m6_modal_inst.hide();
        m6_render();
        document.getElementById('v_actividades_status').value = "lleno"; 
        
        if (typeof sincronizarDatos === "function") sincronizarDatos();
        setTimeout(() => { document.getElementById('m6_buscador').focus(); }, 300);
    }

    function m6_del(idx) { 
        window.m6_lista.splice(idx, 1); 
        if(window.m6_lista.length === 0) document.getElementById('v_actividades_status').value = "";
        m6_render(); 
        if (typeof sincronizarDatos === "function") sincronizarDatos(); 
    }

    function m6_render() {
        const container = document.getElementById('m6_lista_ui');
        container.innerHTML = window.m6_lista.map((p, index) => `
            <div class="bg-white border rounded-3 p-3 d-flex justify-content-between align-items-center shadow-sm" style="border-left: 4px solid #0263a0 !important;">
                <div class="d-flex flex-column gap-1">
                    <div class="d-flex align-items-center gap-2">
                        ${p.item !== '-' ? `<span class="badge-item">${p.item}</span>` : ''}
                        <span class="fw-semibold text-dark text-truncate" style="max-width: 300px;" title="${p.descripcion}">${p.descripcion}</span>
                    </div>
                    ${p.prog ? `<div class="small text-muted fw-bold"><i class="bi bi-geo-alt-fill text-danger me-1"></i> ${p.prog}</div>` : ''}
                </div>
                <div class="d-flex align-items-center gap-2">
                    ${p.metrado ? `<span class="fw-bold text-dark fs-6">${p.metrado} <small class="text-muted" style="font-size:10px;">${p.unidad}</small></span>` : ''}
                    <button type="button" class="btn btn-sm text-danger border-0 ms-2" onclick="m6_del(${index})"><i class="bi bi-trash"></i></button>
                </div>
            </div>
        `).join('');
    }
</script>
"""
