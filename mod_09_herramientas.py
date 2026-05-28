HERRAMIENTAS_HTML = """
<style>
    #step9 { border-radius: 24px; padding: 22px; border: 1px solid #bbf7d0; background: linear-gradient(180deg, #f0fdf4 0%, #ffffff 48%); }
    .m9-panel { border: 1px solid #dcfce7; border-radius: 22px; background: rgba(255,255,255,0.92); padding: 16px; box-shadow: 0 16px 34px rgba(22,101,52,0.08); }
    .m9-header { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 14px; }
    .m9-header h6 { margin: 0; font-size: 12px; font-weight: 900; text-transform: uppercase; letter-spacing: .45px; color: #166534; }
    .m9-actions { display: flex; gap: 8px; flex-wrap: wrap; }
    .m9-btn { border: none; border-radius: 999px; padding: 9px 13px; color: #fff; background: linear-gradient(135deg, #166534, #22c55e); font-size: 12px; font-weight: 900; box-shadow: 0 12px 24px rgba(22,101,52,.16); }
    .m9-btn.secondary { background: linear-gradient(135deg, #475569, #94a3b8); }
    .m9-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; }
    .m9-tool { position: relative; display: flex; align-items: center; gap: 10px; min-height: 56px; border: 1px solid #dcfce7; border-radius: 18px; background: #fff; padding: 11px 12px; cursor: pointer; transition: .2s ease; font-size: 12px; font-weight: 900; color: #334155; }
    .m9-tool:hover { transform: translateY(-1px); box-shadow: 0 12px 26px rgba(15,23,42,.08); }
    .m9-tool input { width: 18px; height: 18px; accent-color: #16a34a; }
    .m9-tool.active { border-color: #22c55e; background: #f0fdf4; color: #166534; }
    .m9-otros { display: grid; grid-template-columns: 1fr auto; gap: 10px; margin-top: 12px; }
    .m9-otros input { border: 1px solid #bbf7d0; border-radius: 14px; padding: 10px 12px; font-size: 12px; font-weight: 700; outline: none; background: #f8fafc; }
    .m9-otros input:focus { border-color: #22c55e; box-shadow: 0 0 0 3px rgba(34,197,94,.12); background: #fff; }
    .m9-preview { margin-top: 14px; border-radius: 16px; min-height: 74px; resize: vertical; background: #f8fafc; font-size: 12px; }
    @media (max-width: 768px) { .m9-grid, .m9-otros { grid-template-columns: 1fr; } }
</style>

<div class="step-view" id="step9">
    <div class="step-title">9.- Herramientas manuales y otros</div>
    <div class="m9-panel">
        <div class="m9-header">
            <h6><i class="bi bi-tools me-1"></i> Herramientas disponibles en obra</h6>
            <div class="m9-actions">
                <button type="button" class="m9-btn" onclick="m9_marcar_todo()">Marcar todo</button>
                <button type="button" class="m9-btn secondary" onclick="m9_desmarcar_todo()">Desmarcar</button>
            </div>
        </div>

        <div class="m9-grid" id="m9_grid"></div>

        <div class="m9-otros">
            <input id="m9_otro" placeholder="Agregar otro: generador, compresora, escalera..." onkeydown="m9_enter_otro(event)">
            <button type="button" class="m9-btn" onclick="m9_agregar_otro()"><i class="bi bi-plus-lg me-1"></i> Agregar otro</button>
        </div>

        <label class="form-label small fw-bold text-muted mt-3">Texto que pasará al cuaderno</label>
        <textarea class="form-control req-step9 m9-preview" id="v_herram" readonly placeholder="Aquí se generarán las herramientas manuales..."></textarea>
    </div>
</div>

<script>
    window.m9_herramientas = window.m9_herramientas || [
        'Palas', 'Picos', 'Buguies', 'Carretillas', 'Barretas', 'Combas',
        'Martillos', 'Cinceles', 'Winchas', 'Niveles de mano', 'Cordeles', 'Plomadas',
        'Badilejos', 'Frotachos', 'Llanas', 'Baldes', 'Cizallas', 'Alicates',
        'Llaves mixtas', 'Destornilladores', 'Arcos de sierra', 'Amoladora',
        'Sierra circular', 'Taladro', 'Extensiones electricas', 'Conos de seguridad', 'Otros'
    ];
    window.m9_seleccionadas = window.m9_seleccionadas || ['Palas', 'Picos', 'Buguies', 'Amoladora', 'Sierra circular', 'Otros'];

    function m9_escape(texto) {
        return String(texto || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
    }

    function m9_render() {
        const grid = document.getElementById('m9_grid');
        grid.innerHTML = window.m9_herramientas.map((herramienta, idx) => {
            const activa = window.m9_seleccionadas.includes(herramienta);
            return `
                <label class="m9-tool ${activa ? 'active' : ''}">
                    <input type="checkbox" ${activa ? 'checked' : ''} onchange="m9_toggle('${m9_escape(herramienta)}', this.checked)">
                    <span>${m9_escape(herramienta)}</span>
                </label>
            `;
        }).join('');
        m9_sincronizar();
    }

    function m9_toggle(herramienta, checked) {
        if (checked && !window.m9_seleccionadas.includes(herramienta)) window.m9_seleccionadas.push(herramienta);
        if (!checked) window.m9_seleccionadas = window.m9_seleccionadas.filter(x => x !== herramienta);
        m9_render();
    }

    function m9_marcar_todo() {
        window.m9_seleccionadas = [...window.m9_herramientas];
        m9_render();
    }

    function m9_desmarcar_todo() {
        window.m9_seleccionadas = [];
        m9_render();
    }

    function m9_agregar_otro() {
        const input = document.getElementById('m9_otro');
        const valor = String(input.value || '').replace(/\\s+/g, ' ').trim();
        if (!valor) return;
        if (!window.m9_herramientas.some(x => x.toLowerCase() === valor.toLowerCase())) window.m9_herramientas.push(valor);
        if (!window.m9_seleccionadas.some(x => x.toLowerCase() === valor.toLowerCase())) window.m9_seleccionadas.push(valor);
        input.value = '';
        m9_render();
    }

    function m9_enter_otro(event) {
        if (event.key !== 'Enter') return;
        event.preventDefault();
        m9_agregar_otro();
    }

    function m9_sincronizar() {
        const texto = window.m9_seleccionadas.length
            ? `* Herramientas manuales: ${window.m9_seleccionadas.join(', ')}.`
            : '* Herramientas manuales: -';
        document.getElementById('v_herram').value = texto;
        if (typeof sincronizarDatos === 'function') sincronizarDatos();
    }

    setTimeout(m9_render, 250);
</script>
"""
