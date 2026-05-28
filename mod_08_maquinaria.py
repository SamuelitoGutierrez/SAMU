MAQUINARIA_HTML = """
<style>
    #step8 { border-radius: 24px; padding: 18px; border: 1px solid #cbd5e1; background: linear-gradient(180deg, #f8fafc 0%, #ffffff 46%); }
    .m8-layout { display: grid; gap: 14px; }
    .m8-panel { border: 1px solid #e2e8f0; border-radius: 22px; background: rgba(255,255,255,0.88); padding: 14px; box-shadow: 0 16px 34px rgba(15,23,42,0.06); }
    .m8-titlebar { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 12px; }
    .m8-titlebar h6 { margin: 0; font-size: 12px; font-weight: 900; color: #334155; text-transform: uppercase; letter-spacing: 0.45px; }
    .m8-category-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
    .m8-cat { border: 1px solid #cbd5e1; background: #fff; border-radius: 18px; padding: 12px 13px 12px 44px; min-height: 62px; position: relative; text-align: left; color: #475569; font-size: 12px; font-weight: 900; box-shadow: 0 10px 24px rgba(15,23,42,0.05); transition: 0.2s ease; }
    .m8-cat i { position: absolute; top: 14px; left: 13px; width: 24px; height: 24px; display: grid; place-items: center; border-radius: 12px; background: #f1f5f9; font-size: 14px; }
    .m8-cat small { display: block; margin-top: 2px; font-size: 10px; line-height: 1.2; font-weight: 700; opacity: 0.72; }
    .m8-cat.active { color: #fff; transform: translateY(-1px); box-shadow: 0 16px 32px rgba(15,23,42,0.16); }
    .m8-cat.active i { background: rgba(255,255,255,0.18); }
    .m8-cat.gov.active { background: linear-gradient(135deg, #075985, #0ea5e9); border-color: #0ea5e9; }
    .m8-cat.srv.active { background: linear-gradient(135deg, #7c3aed, #a78bfa); border-color: #a78bfa; }
    .m8-form-grid { display: grid; grid-template-columns: 1.4fr 1fr 1fr 0.7fr 0.9fr auto; gap: 9px; align-items: end; }
    .m8-contract-grid { display: none; grid-template-columns: 1.2fr 1fr 1fr 0.8fr; gap: 9px; margin-bottom: 12px; }
    .m8-contract-grid.active { display: grid; }
    .m8-field label { display: block; margin-bottom: 4px; font-size: 10px; font-weight: 900; color: #64748b; text-transform: uppercase; letter-spacing: 0.35px; }
    .m8-field input { width: 100%; border: 1px solid #cbd5e1; border-radius: 13px; padding: 9px 10px; outline: none; font-size: 12px; font-weight: 700; background: #f8fafc; }
    .m8-field input:focus { border-color: #0284c7; background: #fff; box-shadow: 0 0 0 3px rgba(2,132,199,0.11); }
    .m8-btn { border: none; border-radius: 14px; padding: 10px 13px; color: #fff; background: linear-gradient(135deg, #075985, #0ea5e9); font-size: 12px; font-weight: 900; white-space: nowrap; box-shadow: 0 12px 26px rgba(2,132,199,0.16); }
    .m8-btn.secondary { background: linear-gradient(135deg, #475569, #94a3b8); }
    .m8-paste { border: 2px dashed #cbd5e1; background: #f8fafc; border-radius: 18px; padding: 12px; text-align: center; color: #64748b; font-size: 12px; font-weight: 800; }
    .m8-paste textarea { width: 100%; height: 44px; margin-top: 4px; border: 0; background: transparent; outline: none; resize: none; text-align: center; font-size: 12px; }
    .m8-table-wrap { border: 1px solid #e2e8f0; border-radius: 18px; overflow: hidden; background: #fff; }
    .m8-table { width: 100%; border-collapse: collapse; font-size: 12px; }
    .m8-table th { background: #f1f5f9; color: #475569; padding: 9px 8px; font-size: 10px; font-weight: 900; text-transform: uppercase; border-bottom: 1px solid #cbd5e1; }
    .m8-table td { padding: 8px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; }
    .m8-empty { padding: 18px; color: #94a3b8; text-align: center; font-weight: 800; }
    .m8-preview { border-radius: 16px; min-height: 118px; resize: vertical; font-size: 12px; background: #f8fafc; }
    .m8-suggest { position: relative; }
    .m8-suggest-list { position: absolute; z-index: 20; left: 0; right: 0; top: calc(100% + 4px); background: #fff; border: 1px solid #dbeafe; border-radius: 14px; box-shadow: 0 18px 35px rgba(15,23,42,0.14); max-height: 210px; overflow-y: auto; display: none; }
    .m8-suggest-list.active { display: block; }
    .m8-suggest-item { padding: 9px 11px; cursor: pointer; font-size: 12px; border-bottom: 1px solid #f1f5f9; }
    .m8-suggest-item:hover { background: #f0f9ff; }
    @media (max-width: 992px) { .m8-category-grid, .m8-form-grid, .m8-contract-grid { grid-template-columns: 1fr; } }
</style>

<div class="step-view" id="step8">
    <div class="step-title">8.- Maquinarias, vehículos y equipos</div>
    <div class="m8-layout">
        <div class="m8-panel">
            <div class="m8-titlebar">
                <h6><i class="bi bi-truck-front-fill me-1"></i> Clasificación para el cuaderno</h6>
                <button type="button" class="m8-btn secondary" onclick="m8_limpiar_categoria()"><i class="bi bi-eraser me-1"></i> Limpiar categoría</button>
            </div>
            <div class="m8-category-grid">
                <button type="button" class="m8-cat gov active" id="m8_cat_maq_gore" onclick="m8_cambiar_categoria('maq_gore')"><i class="bi bi-truck"></i> Maquinarias<small>Gobierno Regional Puno</small></button>
                <button type="button" class="m8-cat srv" id="m8_cat_maq_serv" onclick="m8_cambiar_categoria('maq_serv')"><i class="bi bi-file-earmark-text"></i> Maquinarias<small>Servicio y/o contrato</small></button>
                <button type="button" class="m8-cat gov" id="m8_cat_mov_gore" onclick="m8_cambiar_categoria('mov_gore')"><i class="bi bi-car-front"></i> Movilidades<small>Gobierno Regional Puno</small></button>
                <button type="button" class="m8-cat srv" id="m8_cat_mov_serv" onclick="m8_cambiar_categoria('mov_serv')"><i class="bi bi-file-earmark-check"></i> Movilidades<small>Servicio y/o contrato</small></button>
                <button type="button" class="m8-cat gov" id="m8_cat_eq_gore" onclick="m8_cambiar_categoria('eq_gore')"><i class="bi bi-tools"></i> Equipo liviano<small>Gobierno Regional Puno</small></button>
                <button type="button" class="m8-cat srv" id="m8_cat_eq_serv" onclick="m8_cambiar_categoria('eq_serv')"><i class="bi bi-clipboard2-check"></i> Equipo liviano<small>Servicio y/o contrato</small></button>
            </div>
        </div>

        <div class="m8-panel">
            <div class="m8-titlebar"><h6><i class="bi bi-pencil-square me-1"></i> Registro diario</h6></div>
            <div class="m8-contract-grid" id="m8_contrato_box">
                <div class="m8-field"><label>Entidad / contratista</label><input id="m8_entidad" placeholder="Ej. Consorcio, proveedor o empresa" oninput="m8_sincronizar()"></div>
                <div class="m8-field"><label>Contrato / servicio</label><input id="m8_contrato" placeholder="N° de contrato u orden" oninput="m8_sincronizar()"></div>
                <div class="m8-field"><label>Inicio / fin</label><input id="m8_plazo" placeholder="Desde - hasta" oninput="m8_sincronizar()"></div>
                <div class="m8-field"><label>Días</label><input id="m8_dias" placeholder="N° días" oninput="m8_sincronizar()"></div>
            </div>
            <div class="m8-form-grid">
                <div class="m8-field m8-suggest">
                    <label>Maquinaria / vehículo / equipo</label>
                    <input id="m8_nombre" placeholder="Buscar o escribir..." oninput="m8_buscar()" onkeydown="m8_enter(event, 'm8_marca')">
                    <div class="m8-suggest-list" id="m8_sugerencias"></div>
                </div>
                <div class="m8-field"><label>Marca</label><input id="m8_marca" placeholder="Marca" onkeydown="m8_enter(event, 'm8_modelo')"></div>
                <div class="m8-field"><label>Modelo, placa o serie</label><input id="m8_modelo" placeholder="Modelo / placa / serie" onkeydown="m8_enter(event, 'm8_hm')"></div>
                <div class="m8-field"><label>HM</label><input id="m8_hm" placeholder="Horas" onkeydown="m8_enter(event, 'm8_combustible')"></div>
                <div class="m8-field"><label>Combustible</label><input id="m8_combustible" placeholder="Galones / tipo" onkeydown="m8_enter_guardar(event)"></div>
                <button type="button" class="m8-btn" onclick="m8_agregar_actual()"><i class="bi bi-plus-lg me-1"></i> Agregar</button>
            </div>
        </div>

        <div class="m8-paste">
            <div><i class="bi bi-clipboard-check me-1"></i> Pegue desde Excel: maquinaria | marca | modelo/placa/serie | HM | combustible</div>
            <textarea id="m8_paste" placeholder="Pegar aquí..." onpaste="m8_pegar(event)"></textarea>
        </div>

        <div class="m8-table-wrap">
            <table class="m8-table">
                <thead>
                    <tr>
                        <th>Maquinaria</th>
                        <th>Marca</th>
                        <th>Modelo, placa o serie</th>
                        <th>HM</th>
                        <th>Combustible</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody id="m8_tbody"></tbody>
            </table>
        </div>

        <label class="form-label small fw-bold text-muted">Texto que pasará al cuaderno</label>
        <textarea class="form-control req-step8 m8-preview" id="v_maquina" rows="6" readonly placeholder="Aquí se generará la maquinaria del día..."></textarea>
    </div>
</div>

<script>
    window.m8_catalogo = window.m8_catalogo || [];
    window.m8_registros = window.m8_registros || {
        maq_gore: [], maq_serv: [], mov_gore: [], mov_serv: [], eq_gore: [], eq_serv: []
    };
    window.m8_contratos = window.m8_contratos || {
        maq_serv: {}, mov_serv: {}, eq_serv: {}
    };
    let m8_categoria_actual = 'maq_gore';

    const m8_titulos = {
        maq_gore: '* Maquinarias del Gobierno Regional Puno',
        maq_serv: '* Maquinarias por servicio y/o contrato',
        mov_gore: '* Movilidades del Gobierno Regional Puno',
        mov_serv: '* Movilidades por servicio y/o contrato',
        eq_gore: '* Equipo liviano del Gobierno Regional Puno',
        eq_serv: '* Equipo liviano por servicio y/o contrato'
    };

    function m8_es_servicio(cat = m8_categoria_actual) {
        return cat.endsWith('_serv');
    }

    function m8_texto(valor) {
        return String(valor || '').replace(/\\s+/g, ' ').trim();
    }

    function m8_oracion(valor) {
        return m8_texto(valor).toLocaleLowerCase('es-PE');
    }

    function m8_escape(valor) {
        return m8_texto(valor)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    function m8_item(item) {
        return {
            nombre: m8_texto(item.nombre),
            marca: m8_texto(item.marca),
            modelo: m8_texto(item.modelo),
            hm: m8_texto(item.hm),
            combustible: m8_texto(item.combustible)
        };
    }

    function m8_cambiar_categoria(cat) {
        m8_guardar_contrato();
        m8_categoria_actual = cat;
        Object.keys(m8_titulos).forEach(k => {
            const btn = document.getElementById(`m8_cat_${k}`);
            if(btn) btn.classList.toggle('active', k === cat);
        });
        document.getElementById('m8_contrato_box').classList.toggle('active', m8_es_servicio(cat));
        const contrato = window.m8_contratos[cat] || {};
        document.getElementById('m8_entidad').value = contrato.entidad || '';
        document.getElementById('m8_contrato').value = contrato.contrato || '';
        document.getElementById('m8_plazo').value = contrato.plazo || '';
        document.getElementById('m8_dias').value = contrato.dias || '';
        m8_render();
    }

    function m8_guardar_contrato() {
        if(!m8_es_servicio()) return;
        window.m8_contratos[m8_categoria_actual] = {
            entidad: m8_texto(document.getElementById('m8_entidad').value),
            contrato: m8_texto(document.getElementById('m8_contrato').value),
            plazo: m8_texto(document.getElementById('m8_plazo').value),
            dias: m8_texto(document.getElementById('m8_dias').value)
        };
    }

    function m8_formatear(item) {
        const partes = [
            m8_oracion(item.nombre),
            m8_oracion(item.marca),
            m8_oracion(item.modelo),
            item.hm ? `${m8_oracion(item.hm)} hm` : '',
            item.combustible ? m8_oracion(item.combustible) : ''
        ].filter(Boolean);
        return partes.join(' / ');
    }

    function m8_sincronizar() {
        m8_guardar_contrato();
        const bloques = [];
        Object.keys(m8_titulos).forEach(cat => {
            const lista = window.m8_registros[cat] || [];
            if(lista.length === 0) return;
            const bloque = [m8_titulos[cat]];
            if(m8_es_servicio(cat)) {
                const c = window.m8_contratos[cat] || {};
                const datosContrato = [
                    c.entidad ? m8_oracion(c.entidad) : '',
                    c.contrato ? m8_oracion(c.contrato) : '',
                    c.plazo ? m8_oracion(c.plazo) : '',
                    c.dias ? `${m8_oracion(c.dias)} días` : ''
                ].filter(Boolean).join(' / ');
                bloque.push(`- ${datosContrato || 'servicio y/o contrato'}`);
            }
            lista.forEach(item => bloque.push(`   ${m8_formatear(item)}`));
            bloques.push(bloque.join('\\n'));
        });
        document.getElementById('v_maquina').value = bloques.join('\\n');
        if(typeof sincronizarDatos === 'function') sincronizarDatos();
    }

    function m8_limpiar_inputs() {
        ['m8_nombre', 'm8_marca', 'm8_modelo', 'm8_hm', 'm8_combustible'].forEach(id => document.getElementById(id).value = '');
        document.getElementById('m8_nombre').focus();
    }

    function m8_agregar_actual(data = null) {
        const item = data ? m8_item(data) : m8_item({
            nombre: document.getElementById('m8_nombre').value,
            marca: document.getElementById('m8_marca').value,
            modelo: document.getElementById('m8_modelo').value,
            hm: document.getElementById('m8_hm').value,
            combustible: document.getElementById('m8_combustible').value
        });
        if(!item.nombre) return;
        window.m8_registros[m8_categoria_actual].push(item);
        if(!window.m8_catalogo.some(x => [x.nombre, x.marca, x.modelo].join('|').toLowerCase() === [item.nombre, item.marca, item.modelo].join('|').toLowerCase())) {
            window.m8_catalogo.push({ nombre: item.nombre, marca: item.marca, modelo: item.modelo });
        }
        if(!data) m8_limpiar_inputs();
        m8_render();
    }

    function m8_render() {
        const lista = window.m8_registros[m8_categoria_actual] || [];
        const tbody = document.getElementById('m8_tbody');
        if(lista.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6"><div class="m8-empty">No hay registros en esta clasificación.</div></td></tr>';
            m8_sincronizar();
            return;
        }
        tbody.innerHTML = lista.map((item, idx) => `
            <tr>
                <td>${m8_escape(item.nombre)}</td>
                <td>${m8_escape(item.marca)}</td>
                <td>${m8_escape(item.modelo)}</td>
                <td>${m8_escape(item.hm)}</td>
                <td>${m8_escape(item.combustible)}</td>
                <td class="text-end"><button type="button" class="btn btn-sm text-danger border-0" onclick="m8_eliminar(${idx})"><i class="bi bi-trash"></i></button></td>
            </tr>
        `).join('');
        m8_sincronizar();
    }

    function m8_eliminar(idx) {
        window.m8_registros[m8_categoria_actual].splice(idx, 1);
        m8_render();
    }

    function m8_limpiar_categoria() {
        window.m8_registros[m8_categoria_actual] = [];
        m8_render();
    }

    function m8_enter(event, nextId) {
        if(event.key !== 'Enter') return;
        event.preventDefault();
        document.getElementById(nextId).focus();
    }

    function m8_enter_guardar(event) {
        if(event.key !== 'Enter') return;
        event.preventDefault();
        m8_agregar_actual();
    }

    function m8_buscar() {
        const q = m8_texto(document.getElementById('m8_nombre').value).toLowerCase();
        const box = document.getElementById('m8_sugerencias');
        if(!q) {
            box.classList.remove('active');
            box.innerHTML = '';
            return;
        }
        const resultados = window.m8_catalogo.filter(x => [x.nombre, x.marca, x.modelo].join(' ').toLowerCase().includes(q)).slice(0, 8);
        box.innerHTML = resultados.map((x, idx) => `<div class="m8-suggest-item" onclick="m8_usar_sugerencia(${idx})"><b>${m8_escape(x.nombre)}</b><br><small>${m8_escape(x.marca)} / ${m8_escape(x.modelo)}</small></div>`).join('');
        box.dataset.items = JSON.stringify(resultados);
        box.classList.toggle('active', resultados.length > 0);
    }

    function m8_usar_sugerencia(idx) {
        const box = document.getElementById('m8_sugerencias');
        const items = JSON.parse(box.dataset.items || '[]');
        const item = items[idx];
        if(!item) return;
        document.getElementById('m8_nombre').value = item.nombre || '';
        document.getElementById('m8_marca').value = item.marca || '';
        document.getElementById('m8_modelo').value = item.modelo || '';
        box.classList.remove('active');
        document.getElementById('m8_hm').focus();
    }

    function m8_pegar(event) {
        event.preventDefault();
        const data = (event.clipboardData || window.clipboardData).getData('text');
        if(!data.trim()) return;
        let count = 0;
        data.split('\\n').forEach(row => {
            if(!row.trim()) return;
            const cols = row.split('\\t').map(x => m8_texto(x));
            const item = {
                nombre: cols[0] || '',
                marca: cols[1] || '',
                modelo: cols[2] || '',
                hm: cols[3] || '',
                combustible: cols[4] || ''
            };
            if(item.nombre) {
                m8_agregar_actual(item);
                count++;
            }
        });
        const paste = document.getElementById('m8_paste');
        paste.value = count > 0 ? `Se pegaron ${count} registros.` : '';
        setTimeout(() => paste.value = '', 1200);
    }

    setTimeout(() => m8_cambiar_categoria('maq_gore'), 300);
</script>
"""
