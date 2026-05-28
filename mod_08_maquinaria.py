MAQUINARIA_HTML = """
<style>
    #step8 { border-radius: 24px; padding: 18px; border: 1px solid #cbd5e1; background: linear-gradient(180deg, #f8fafc 0%, #ffffff 46%); }
    .m8-layout { display: grid; gap: 14px; }
    .m8-panel { border: 1px solid #e2e8f0; border-radius: 22px; background: rgba(255,255,255,0.9); padding: 14px; box-shadow: 0 16px 34px rgba(15,23,42,0.06); }
    .m8-titlebar { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 12px; }
    .m8-titlebar h6 { margin: 0; font-size: 12px; font-weight: 900; color: #334155; text-transform: uppercase; letter-spacing: 0.45px; }
    .m8-actions { display: flex; gap: 9px; flex-wrap: wrap; }
    .m8-btn { border: none; border-radius: 14px; padding: 10px 13px; color: #fff; background: linear-gradient(135deg, #075985, #0ea5e9); font-size: 12px; font-weight: 900; white-space: nowrap; box-shadow: 0 12px 26px rgba(2,132,199,0.16); }
    .m8-btn.secondary { background: linear-gradient(135deg, #475569, #94a3b8); }
    .m8-btn.purple { background: linear-gradient(135deg, #6d28d9, #a78bfa); }
    .m8-category-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
    .m8-cat { border: 1px solid #cbd5e1; background: #fff; border-radius: 18px; padding: 12px 13px 12px 44px; min-height: 62px; position: relative; text-align: left; color: #475569; font-size: 12px; font-weight: 900; box-shadow: 0 10px 24px rgba(15,23,42,0.05); transition: 0.2s ease; }
    .m8-cat i { position: absolute; top: 14px; left: 13px; width: 24px; height: 24px; display: grid; place-items: center; border-radius: 12px; background: #f1f5f9; font-size: 14px; }
    .m8-cat small { display: block; margin-top: 2px; font-size: 10px; line-height: 1.2; font-weight: 700; opacity: 0.72; }
    .m8-cat.active { color: #fff; transform: translateY(-1px); box-shadow: 0 16px 32px rgba(15,23,42,0.16); }
    .m8-cat.active i { background: rgba(255,255,255,0.18); }
    .m8-cat.gov.active { background: linear-gradient(135deg, #075985, #0ea5e9); border-color: #0ea5e9; }
    .m8-cat.srv.active { background: linear-gradient(135deg, #7c3aed, #a78bfa); border-color: #a78bfa; }
    .m8-form-grid { display: grid; grid-template-columns: 1.25fr 1fr 1fr 1fr 0.65fr 0.95fr auto; gap: 9px; align-items: end; }
    .m8-base-grid { display: grid; grid-template-columns: 1fr 1fr 1fr 1.1fr auto; gap: 9px; align-items: end; }
    .m8-contract-grid { display: none; grid-template-columns: 1.25fr 1fr; gap: 9px; margin-bottom: 12px; }
    .m8-contract-grid.active { display: grid; }
    .m8-field label { display: block; margin-bottom: 4px; font-size: 10px; font-weight: 900; color: #64748b; text-transform: uppercase; letter-spacing: 0.35px; }
    .m8-field input, .m8-field select { width: 100%; border: 1px solid #cbd5e1; border-radius: 13px; padding: 9px 10px; outline: none; font-size: 12px; font-weight: 700; background: #f8fafc; }
    .m8-field input:focus, .m8-field select:focus { border-color: #0284c7; background: #fff; box-shadow: 0 0 0 3px rgba(2,132,199,0.11); }
    .m8-paste { border: 2px dashed #cbd5e1; background: #f8fafc; border-radius: 18px; padding: 12px; text-align: center; color: #64748b; font-size: 12px; font-weight: 800; }
    .m8-paste textarea { width: 100%; height: 44px; margin-top: 4px; border: 0; background: transparent; outline: none; resize: none; text-align: center; font-size: 12px; }
    .m8-table-wrap { border: 1px solid #e2e8f0; border-radius: 18px; overflow: hidden; background: #fff; }
    .m8-table { width: 100%; border-collapse: collapse; font-size: 12px; }
    .m8-table th { background: #f1f5f9; color: #475569; padding: 9px 8px; font-size: 10px; font-weight: 900; text-transform: uppercase; border-bottom: 1px solid #cbd5e1; }
    .m8-table td { padding: 8px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; }
    .m8-empty { padding: 18px; color: #94a3b8; text-align: center; font-weight: 800; }
    .m8-preview { border-radius: 16px; min-height: 118px; resize: vertical; font-size: 12px; background: #f8fafc; }
    @media (max-width: 992px) { .m8-category-grid, .m8-form-grid, .m8-base-grid, .m8-contract-grid { grid-template-columns: 1fr; } }
</style>

<div class="step-view" id="step8">
    <div class="step-title">8.- Maquinarias, vehículos y equipos</div>
    <div class="m8-layout">
        <div class="m8-panel">
            <div class="m8-titlebar">
                <h6><i class="bi bi-bookmark-plus-fill me-1"></i> Base de maquinarias, vehículos y equipos</h6>
                <button type="button" class="m8-btn secondary" onclick="m8_limpiar_base_categoria()"><i class="bi bi-eraser me-1"></i> Limpiar base seleccionada</button>
            </div>
            <div class="m8-base-grid">
                <div class="m8-field"><label>Clasificación</label><select id="m8_base_cat" onchange="m8_render_base(); m8_refrescar_select();"><option value="maq_gore">Maquinarias del Gobierno Regional Puno</option><option value="maq_serv">Maquinarias por servicio y/o contrato</option><option value="mov_gore">Movilidades del Gobierno Regional Puno</option><option value="mov_serv">Movilidades por servicio y/o contrato</option><option value="eq_gore">Equipo liviano del Gobierno Regional Puno</option><option value="eq_serv">Equipo liviano por servicio y/o contrato</option></select></div>
                <div class="m8-field"><label>Maquinaria / vehículo / equipo</label><input id="m8_base_nombre" placeholder="Camión volquete" onkeydown="m8_enter(event, 'm8_base_marca')"></div>
                <div class="m8-field"><label>Marca</label><input id="m8_base_marca" placeholder="Volvo" onkeydown="m8_enter(event, 'm8_base_modelo')"></div>
                <div class="m8-field"><label>Modelo, placa o serie</label><input id="m8_base_modelo" placeholder="FMX 6X4 R / EGK-176" onkeydown="m8_enter_guardar_base(event)"></div>
                <button type="button" class="m8-btn purple" onclick="m8_agregar_base()"><i class="bi bi-plus-lg me-1"></i> Registrar base</button>
            </div>
            <div class="m8-paste mt-3">
                <div><i class="bi bi-clipboard-check me-1"></i> Pegado masivo para la base: maquinaria | marca | modelo, placa o serie</div>
                <textarea id="m8_base_paste" placeholder="Pegar aquí..." onpaste="m8_pegar_base(event)"></textarea>
            </div>
        </div>

        <div class="m8-panel">
            <div class="m8-titlebar">
                <h6><i class="bi bi-list-check me-1"></i> Seleccione la clasificación para el registro diario</h6>
                <button type="button" class="m8-btn secondary" onclick="m8_limpiar_categoria()"><i class="bi bi-eraser me-1"></i> Limpiar diario</button>
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
            <div class="m8-titlebar"><h6><i class="bi bi-pencil-square me-1"></i> Registro diario de trabajo</h6></div>
            <div class="m8-contract-grid" id="m8_contrato_box">
                <div class="m8-field"><label>Entidad / contratista</label><input id="m8_entidad" placeholder="Nombre de la entidad o empresa" oninput="m8_sincronizar()"></div>
                <div class="m8-field"><label>Número de contrato</label><input id="m8_contrato" placeholder="Contrato, servicio u orden" oninput="m8_sincronizar()"></div>
            </div>
            <div class="m8-form-grid">
                <div class="m8-field"><label>Seleccionar equipo registrado</label><select id="m8_equipo_select" onchange="m8_usar_equipo()"></select></div>
                <div class="m8-field"><label>Maquinaria</label><input id="m8_nombre" placeholder="Nombre" onkeydown="m8_enter(event, 'm8_marca')"></div>
                <div class="m8-field"><label>Marca</label><input id="m8_marca" placeholder="Marca" onkeydown="m8_enter(event, 'm8_modelo')"></div>
                <div class="m8-field"><label>Placa/serie</label><input id="m8_modelo" placeholder="Modelo / placa / serie" onkeydown="m8_enter(event, 'm8_hm')"></div>
                <div class="m8-field"><label>HM</label><input id="m8_hm" placeholder="08:00 HM" onkeydown="m8_enter(event, 'm8_combustible')"></div>
                <div class="m8-field"><label>Combustible</label><input id="m8_combustible" placeholder="20 GLN Diesel" onkeydown="m8_enter_guardar(event)"></div>
                <button type="button" class="m8-btn" onclick="m8_agregar_actual()"><i class="bi bi-plus-lg me-1"></i> Agregar</button>
            </div>
            <div class="m8-paste mt-3">
                <div><i class="bi bi-clipboard-check me-1"></i> Pegado masivo diario: maquinaria | marca | placa/serie | HM | combustible</div>
                <textarea id="m8_paste" placeholder="Pegar aquí..." onpaste="m8_pegar_diario(event)"></textarea>
            </div>
        </div>

        <div class="m8-table-wrap">
            <table class="m8-table">
                <thead>
                    <tr><th>Maquinaria</th><th>Marca</th><th>Modelo, placa o serie</th><th>HM</th><th>Combustible</th><th></th></tr>
                </thead>
                <tbody id="m8_tbody"></tbody>
            </table>
        </div>

        <div class="m8-table-wrap">
            <table class="m8-table">
                <thead>
                    <tr><th colspan="4">Base registrada de la clasificación seleccionada</th></tr>
                    <tr><th>Maquinaria</th><th>Marca</th><th>Modelo, placa o serie</th><th></th></tr>
                </thead>
                <tbody id="m8_base_tbody"></tbody>
            </table>
        </div>

        <label class="form-label small fw-bold text-muted">Texto que pasará al cuaderno</label>
        <textarea class="form-control req-step8 m8-preview" id="v_maquina" rows="7" readonly placeholder="Aquí se generará la maquinaria del día..."></textarea>
    </div>
</div>

<script>
    window.m8_base = window.m8_base || { maq_gore: [], maq_serv: [], mov_gore: [], mov_serv: [], eq_gore: [], eq_serv: [] };
    window.m8_registros = window.m8_registros || { maq_gore: [], maq_serv: [], mov_gore: [], mov_serv: [], eq_gore: [], eq_serv: [] };
    window.m8_contratos = window.m8_contratos || { maq_serv: {}, mov_serv: {}, eq_serv: {} };
    let m8_categoria_actual = 'maq_gore';

    const m8_titulos = {
        maq_gore: '* Maquinarias del Gobierno Regional Puno',
        maq_serv: '* Maquinarias por servicio y/o contrato',
        mov_gore: '* Movilidades del Gobierno Regional Puno',
        mov_serv: '* Movilidades por servicio y/o contrato',
        eq_gore: '* Equipo liviano del Gobierno Regional Puno',
        eq_serv: '* Equipo liviano por servicio y/o contrato'
    };

    function m8_es_servicio(cat = m8_categoria_actual) { return cat.endsWith('_serv'); }
    function m8_texto(valor) { return String(valor || '').replace(/\\s+/g, ' ').trim(); }
    function m8_escape(valor) {
        return m8_texto(valor).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
    }
    function m8_item(data) {
        return {
            nombre: m8_texto(data.nombre),
            marca: m8_texto(data.marca),
            modelo: m8_texto(data.modelo),
            hm: m8_texto(data.hm),
            combustible: m8_texto(data.combustible)
        };
    }
    function m8_hm(texto) {
        const t = m8_texto(texto);
        if(!t) return '';
        return /\\bhm\\b/i.test(t) ? t : `${t} HM`;
    }
    function m8_combustible(texto) {
        return m8_texto(texto);
    }

    function m8_cambiar_categoria(cat) {
        m8_guardar_contrato();
        m8_categoria_actual = cat;
        document.getElementById('m8_base_cat').value = cat;
        Object.keys(m8_titulos).forEach(k => {
            const btn = document.getElementById(`m8_cat_${k}`);
            if(btn) btn.classList.toggle('active', k === cat);
        });
        document.getElementById('m8_contrato_box').classList.toggle('active', m8_es_servicio(cat));
        const contrato = window.m8_contratos[cat] || {};
        document.getElementById('m8_entidad').value = contrato.entidad || '';
        document.getElementById('m8_contrato').value = contrato.contrato || '';
        m8_refrescar_select();
        m8_render_base();
        m8_render();
    }

    function m8_guardar_contrato() {
        if(!m8_es_servicio()) return;
        window.m8_contratos[m8_categoria_actual] = {
            entidad: m8_texto(document.getElementById('m8_entidad').value),
            contrato: m8_texto(document.getElementById('m8_contrato').value)
        };
    }

    function m8_agregar_base(data = null) {
        const cat = document.getElementById('m8_base_cat').value;
        const item = data ? m8_item(data) : m8_item({
            nombre: document.getElementById('m8_base_nombre').value,
            marca: document.getElementById('m8_base_marca').value,
            modelo: document.getElementById('m8_base_modelo').value
        });
        if(!item.nombre) return;
        window.m8_base[cat].push({ nombre: item.nombre, marca: item.marca, modelo: item.modelo });
        if(!data) {
            document.getElementById('m8_base_nombre').value = '';
            document.getElementById('m8_base_marca').value = '';
            document.getElementById('m8_base_modelo').value = '';
            document.getElementById('m8_base_nombre').focus();
        }
        m8_refrescar_select();
        m8_render_base();
    }

    function m8_pegar_base(event) {
        event.preventDefault();
        const data = (event.clipboardData || window.clipboardData).getData('text');
        let count = 0;
        data.split('\\n').forEach(row => {
            const cols = row.split('\\t').map(m8_texto);
            if(cols[0]) {
                m8_agregar_base({ nombre: cols[0], marca: cols[1], modelo: cols[2] });
                count++;
            }
        });
        const paste = document.getElementById('m8_base_paste');
        paste.value = count ? `Se registraron ${count} equipos en la base.` : '';
        setTimeout(() => paste.value = '', 1200);
    }

    function m8_refrescar_select() {
        const select = document.getElementById('m8_equipo_select');
        const lista = window.m8_base[m8_categoria_actual] || [];
        select.innerHTML = '<option value="">Seleccione o escriba manualmente...</option>' + lista.map((item, idx) => `<option value="${idx}">${m8_escape(item.nombre)} | ${m8_escape(item.marca)} | ${m8_escape(item.modelo)}</option>`).join('');
    }

    function m8_usar_equipo() {
        const idx = document.getElementById('m8_equipo_select').value;
        const item = (window.m8_base[m8_categoria_actual] || [])[idx];
        if(!item) return;
        document.getElementById('m8_nombre').value = item.nombre || '';
        document.getElementById('m8_marca').value = item.marca || '';
        document.getElementById('m8_modelo').value = item.modelo || '';
        document.getElementById('m8_hm').focus();
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
        if(!data) {
            ['m8_nombre', 'm8_marca', 'm8_modelo', 'm8_hm', 'm8_combustible'].forEach(id => document.getElementById(id).value = '');
            document.getElementById('m8_equipo_select').value = '';
            document.getElementById('m8_equipo_select').focus();
        }
        m8_render();
    }

    function m8_pegar_diario(event) {
        event.preventDefault();
        const data = (event.clipboardData || window.clipboardData).getData('text');
        let count = 0;
        data.split('\\n').forEach(row => {
            const cols = row.split('\\t').map(m8_texto);
            if(cols[0]) {
                m8_agregar_actual({ nombre: cols[0], marca: cols[1], modelo: cols[2], hm: cols[3], combustible: cols[4] });
                count++;
            }
        });
        const paste = document.getElementById('m8_paste');
        paste.value = count ? `Se agregaron ${count} registros al día.` : '';
        setTimeout(() => paste.value = '', 1200);
    }

    function m8_formatear(item) {
        return [item.nombre, item.marca, item.modelo, m8_hm(item.hm), m8_combustible(item.combustible)].map(m8_texto).join('\\t');
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
                const contrato = [c.entidad, c.contrato].map(m8_texto).filter(Boolean).join(' - ');
                bloque.push(`- ${contrato || 'servicio y/o contrato'}`);
            }
            lista.forEach(item => bloque.push(`   ${m8_formatear(item)}`));
            bloques.push(bloque.join('\\n'));
        });
        document.getElementById('v_maquina').value = bloques.join('\\n');
        if(typeof sincronizarDatos === 'function') sincronizarDatos();
    }

    function m8_render() {
        const lista = window.m8_registros[m8_categoria_actual] || [];
        const tbody = document.getElementById('m8_tbody');
        if(lista.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6"><div class="m8-empty">No hay registros diarios en esta clasificación.</div></td></tr>';
            m8_sincronizar();
            return;
        }
        tbody.innerHTML = lista.map((item, idx) => `
            <tr><td>${m8_escape(item.nombre)}</td><td>${m8_escape(item.marca)}</td><td>${m8_escape(item.modelo)}</td><td>${m8_escape(m8_hm(item.hm))}</td><td>${m8_escape(item.combustible)}</td><td class="text-end"><button type="button" class="btn btn-sm text-danger border-0" onclick="m8_eliminar(${idx})"><i class="bi bi-trash"></i></button></td></tr>
        `).join('');
        m8_sincronizar();
    }

    function m8_render_base() {
        const cat = document.getElementById('m8_base_cat').value;
        const lista = window.m8_base[cat] || [];
        const tbody = document.getElementById('m8_base_tbody');
        if(lista.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4"><div class="m8-empty">No hay equipos en la base de esta clasificación.</div></td></tr>';
            return;
        }
        tbody.innerHTML = lista.map((item, idx) => `
            <tr><td>${m8_escape(item.nombre)}</td><td>${m8_escape(item.marca)}</td><td>${m8_escape(item.modelo)}</td><td class="text-end"><button type="button" class="btn btn-sm text-danger border-0" onclick="m8_eliminar_base(${idx})"><i class="bi bi-trash"></i></button></td></tr>
        `).join('');
    }

    function m8_eliminar(idx) {
        window.m8_registros[m8_categoria_actual].splice(idx, 1);
        m8_render();
    }

    function m8_eliminar_base(idx) {
        const cat = document.getElementById('m8_base_cat').value;
        window.m8_base[cat].splice(idx, 1);
        m8_refrescar_select();
        m8_render_base();
    }

    function m8_limpiar_categoria() {
        window.m8_registros[m8_categoria_actual] = [];
        m8_render();
    }

    function m8_limpiar_base_categoria() {
        const cat = document.getElementById('m8_base_cat').value;
        window.m8_base[cat] = [];
        m8_refrescar_select();
        m8_render_base();
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
    function m8_enter_guardar_base(event) {
        if(event.key !== 'Enter') return;
        event.preventDefault();
        m8_agregar_base();
    }

    setTimeout(() => m8_cambiar_categoria('maq_gore'), 300);
</script>
"""
