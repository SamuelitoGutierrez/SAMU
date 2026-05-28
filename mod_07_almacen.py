from flask import Blueprint, render_template_string, session, url_for

from navbar import obtener_navbar


ALMACEN_HTML = """
<style>
    #step7 { border-radius: 24px; padding: 18px; border: 1px solid #dbeafe; transition: 0.25s ease; }
    #step7.m7-materiales { background: linear-gradient(180deg, #eff6ff 0%, #ffffff 44%); border-color: #bfdbfe; }
    #step7.m7-combustible { background: linear-gradient(180deg, #fff7ed 0%, #ffffff 44%); border-color: #fed7aa; }
    .m7-toolbar { display: grid; grid-template-columns: 1.2fr 0.9fr auto; gap: 12px; align-items: stretch; margin-bottom: 14px; }
    .m7-tabs { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
    .m7-tab { border: 1px solid #cbd5e1; background: #fff; color: #334155; border-radius: 18px; padding: 13px 16px; font-size: 12px; font-weight: 800; transition: 0.2s; box-shadow: 0 10px 24px rgba(15,23,42,0.06); text-align: left; }
    .m7-tab i { font-size: 16px; }
    .m7-tab small { display: block; margin-top: 2px; font-size: 10px; font-weight: 700; opacity: 0.72; }
    .m7-tab.active { color: #fff; transform: translateY(-1px); box-shadow: 0 14px 30px rgba(15,23,42,0.18); }
    .m7-tab.materiales { border-color: #bfdbfe; color: #075985; }
    .m7-tab.materiales.active { background: linear-gradient(135deg, #075985, #0ea5e9); border-color: #0ea5e9; color: #fff; }
    .m7-tab.combustible { border-color: #fed7aa; color: #92400e; }
    .m7-tab.combustible.active { background: linear-gradient(135deg, #92400e, #f59e0b); border-color: #f59e0b; color: #fff; }
    .m7-tab.mov-ingreso.active { background: linear-gradient(135deg, #047857, #10b981); border-color: #10b981; }
    .m7-tab.mov-salida.active { background: linear-gradient(135deg, #be123c, #fb7185); border-color: #fb7185; }
    .m7-btn { border: none; border-radius: 18px; padding: 12px 18px; font-size: 12px; font-weight: 800; color: #fff; background: linear-gradient(135deg, #0263a0, #0ea5e9); box-shadow: 0 12px 28px rgba(2,99,160,0.18); min-width: 170px; }
    #step7.m7-combustible .m7-btn { background: linear-gradient(135deg, #92400e, #f59e0b); box-shadow: 0 12px 28px rgba(180,83,9,0.20); }
    .m7-paste-zone { border: 2px dashed #cbd5e1; border-radius: 18px; background: rgba(255,255,255,0.78); padding: 12px; color: #64748b; text-align: center; font-size: 12px; font-weight: 700; margin-bottom: 12px; }
    #step7.m7-materiales .m7-paste-zone:focus-within, #step7.m7-materiales .m7-paste-zone:hover { border-color: #0284c7; background: #f0f9ff; color: #0263a0; }
    #step7.m7-combustible .m7-paste-zone:focus-within, #step7.m7-combustible .m7-paste-zone:hover { border-color: #f59e0b; background: #fff7ed; color: #92400e; }
    .m7-paste-zone textarea { width: 100%; height: 44px; border: 0; outline: 0; resize: none; background: transparent; text-align: center; font-size: 12px; color: #334155; }
    .m7-table-wrap { border: 1px solid #dbeafe; border-radius: 18px; overflow: hidden; background: #fff; box-shadow: 0 12px 30px rgba(15,23,42,0.05); }
    #step7.m7-combustible .m7-table-wrap { border-color: #fed7aa; }
    .m7-table { width: 100%; border-collapse: collapse; font-size: 12px; }
    .m7-table th { background: #f1f5f9; color: #475569; padding: 9px 8px; text-transform: uppercase; letter-spacing: 0.4px; font-size: 10px; border-bottom: 1px solid #cbd5e1; }
    .m7-table td { padding: 6px; border-bottom: 1px solid #eef2ff; vertical-align: middle; }
    .m7-table input { width: 100%; border: 1px solid transparent; border-radius: 9px; padding: 7px 8px; font-size: 12px; background: #f8fafc; outline: none; }
    .m7-table input:focus { border-color: #0ea5e9; background: #fff; box-shadow: 0 0 0 3px rgba(14,165,233,0.10); }
    #step7.m7-combustible .m7-table input:focus { border-color: #f59e0b; box-shadow: 0 0 0 3px rgba(245,158,11,0.14); }
    .m7-preview { border-radius: 16px; min-height: 86px; resize: vertical; font-size: 12px; background: #f8fafc; }
    .m7-empty { padding: 18px; text-align: center; color: #94a3b8; font-weight: 700; font-size: 12px; }
    .m7-fuel-quick { display: none; border: 1px solid #fed7aa; background: #fff7ed; border-radius: 16px; padding: 12px; margin-bottom: 12px; }
    .m7-fuel-quick.active { display: block; }
    .m7-fuel-grid { display: grid; grid-template-columns: repeat(2, 1fr) auto; gap: 10px; align-items: end; }
    .m7-fuel-grid label { font-size: 11px; font-weight: 800; color: #92400e; text-transform: uppercase; }
    .m7-fuel-grid input { border: 1px solid #fed7aa; border-radius: 12px; padding: 9px 10px; font-weight: 800; outline: none; }
    .m7-fuel-grid input:focus { border-color: #f59e0b; box-shadow: 0 0 0 3px rgba(245,158,11,0.15); }
    .m7-btn-fuel { border: none; border-radius: 14px; padding: 10px 14px; color: #fff; background: #b45309; font-size: 12px; font-weight: 800; }
    @media (max-width: 992px) { .m7-toolbar { grid-template-columns: 1fr; } .m7-btn { width: 100%; } }
    @media (max-width: 768px) { .m7-fuel-grid { grid-template-columns: 1fr; } .m7-tabs { grid-template-columns: 1fr; } }
    @media (max-width: 768px) { .m7-table { min-width: 760px; } .m7-table-wrap { overflow-x: auto; } }
</style>

<div class="step-view m7-materiales" id="step7">
    <div class="step-title">7.- Movimientos de Almacen</div>
    <p class="text-muted small mb-3">Registre movimientos de materiales o combustible. Puede pegar desde Excel en el orden: # | Documento | Material/Combustible | Unidad | Cantidad.</p>

    <div class="m7-toolbar">
        <div class="m7-tabs">
            <button type="button" class="m7-tab materiales active" id="m7_cat_materiales" onclick="m7_cambiar_categoria('materiales')"><i class="bi bi-bricks me-1"></i> Materiales de construcción<small>Ingreso y salida de almacén</small></button>
            <button type="button" class="m7-tab combustible" id="m7_cat_combustible" onclick="m7_cambiar_categoria('combustible')"><i class="bi bi-fuel-pump-fill me-1"></i> Combustible<small>Diésel, gasohol y lubricantes</small></button>
        </div>
        <div class="m7-tabs">
            <button type="button" class="m7-tab mov-ingreso active" id="m7_tab_ingreso" onclick="m7_cambiar_tipo('ingreso')"><i class="bi bi-box-arrow-in-down me-1"></i> Ingreso<small>Entradas al almacén</small></button>
            <button type="button" class="m7-tab mov-salida" id="m7_tab_salida" onclick="m7_cambiar_tipo('salida')"><i class="bi bi-box-arrow-up me-1"></i> Salida<small>Consumo o despacho</small></button>
        </div>
        <button type="button" class="m7-btn" onclick="m7_agregar_fila()"><i class="bi bi-plus-lg me-1"></i> Agregar material</button>
    </div>

    <div class="m7-paste-zone">
        <div><i class="bi bi-clipboard-check me-1"></i> Pegue aquí desde Excel con Ctrl + V</div>
        <textarea id="m7_paste_input" placeholder="# | Contrato / Servicio / Orden de compra | Material o combustible | Unidad | Cantidad"></textarea>
    </div>

    <div class="m7-fuel-quick" id="m7_fuel_quick">
        <div class="small fw-bold mb-2" style="color:#92400e;"><i class="bi bi-lightning-charge-fill me-1"></i>Salida rápida de combustible</div>
        <div class="m7-fuel-grid">
            <div>
                <label>Diesel B5 S-50 (GLN)</label>
                <input type="number" step="0.01" id="m7_diesel_qty" placeholder="0.00">
            </div>
            <div>
                <label>Gasohol regular (GLN)</label>
                <input type="number" step="0.01" id="m7_gasohol_qty" placeholder="0.00">
            </div>
            <button type="button" class="m7-btn-fuel" onclick="m7_agregar_salida_combustible()">Agregar salida</button>
        </div>
    </div>

    <div class="m7-table-wrap mb-3">
        <table class="m7-table">
            <thead>
                <tr>
                    <th style="width:50px;">#</th>
                    <th style="width:190px;">Documento</th>
                    <th id="m7_th_material">Material</th>
                    <th style="width:120px;">Unidad</th>
                    <th style="width:100px;">Cantidad</th>
                    <th style="width:46px;"></th>
                </tr>
            </thead>
            <tbody id="m7_tbody"></tbody>
        </table>
    </div>

    <label class="form-label small fw-bold text-muted">Texto que pasará al cuaderno</label>
    <textarea class="form-control req-step7 m7-preview" id="v_almacen" rows="4" readonly placeholder="Aquí se generará el movimiento de almacén..."></textarea>
</div>

<script>
    window.m7_movimientos = window.m7_movimientos || {
        materiales: { ingreso: [], salida: [] },
        combustible: { ingreso: [], salida: [] }
    };
    let m7_categoria_actual = 'materiales';
    let m7_tipo_actual = 'ingreso';

    function m7_cambiar_categoria(categoria) {
        m7_categoria_actual = categoria;
        const panel = document.getElementById('step7');
        if(panel) {
            panel.classList.toggle('m7-materiales', categoria === 'materiales');
            panel.classList.toggle('m7-combustible', categoria === 'combustible');
        }
        document.getElementById('m7_cat_materiales').classList.toggle('active', categoria === 'materiales');
        document.getElementById('m7_cat_combustible').classList.toggle('active', categoria === 'combustible');
        document.getElementById('m7_th_material').innerText = categoria === 'combustible' ? 'Combustible' : 'Material';
        document.querySelector('.m7-btn').innerHTML = categoria === 'combustible'
            ? '<i class="bi bi-plus-lg me-1"></i> Agregar combustible'
            : '<i class="bi bi-plus-lg me-1"></i> Agregar material';
        m7_render();
    }

    function m7_cambiar_tipo(tipo) {
        m7_tipo_actual = tipo;
        document.getElementById('m7_tab_ingreso').classList.toggle('active', tipo === 'ingreso');
        document.getElementById('m7_tab_salida').classList.toggle('active', tipo === 'salida');
        m7_render();
    }

    function m7_movs() {
        return window.m7_movimientos[m7_categoria_actual][m7_tipo_actual];
    }

    function m7_agregar_fila(data = {}) {
        m7_movs().push({
            numero: data.numero || (m7_movs().length + 1).toString(),
            documento: data.documento || '',
            material: data.material || '',
            unidad: data.unidad || (m7_categoria_actual === 'combustible' ? 'GLN' : ''),
            cantidad: data.cantidad || ''
        });
        m7_render();
    }

    function m7_actualizar(idx, campo, valor) {
        m7_movs()[idx][campo] = valor;
        m7_sincronizar();
    }

    function m7_eliminar(idx) {
        m7_movs().splice(idx, 1);
        m7_render();
    }

    function m7_parse_row(cols) {
        const clean = cols.map(c => (c || '').trim());
        if(clean.length >= 5) {
            return { numero: clean[0], documento: clean[1], material: clean[2], unidad: clean[3], cantidad: clean[4] };
        }
        if(clean.length >= 4) {
            return { numero: clean[0], material: clean[1], unidad: clean[2], cantidad: clean[3] };
        }
        if(clean.length >= 3) {
            return { material: clean[0], unidad: clean[1], cantidad: clean[2] };
        }
        return null;
    }

    function m7_texto_oracion(valor) {
        return String(valor || '').replace(/\s+/g, ' ').trim().toLocaleLowerCase('es-PE');
    }

    function m7_formato_item(m) {
        if(!m.material || !m.unidad || !m.cantidad) return '';
        const cantidad = Number(m.cantidad);
        const cantidadTxt = Number.isFinite(cantidad) ? cantidad.toFixed(2) : m.cantidad;
        return `${cantidadTxt} ${m7_texto_oracion(m.unidad)} ${m7_texto_oracion(m.material)}`;
    }

    function m7_titulo_categoria(categoria) {
        return categoria === 'combustible' ? '7.2 Movimiento de combustible.' : '7.1 Movimiento de materiales de construcción';
    }

    function m7_numero_movimiento(categoria, tipo) {
        if(categoria === 'combustible') return tipo === 'ingreso' ? '7.2.1 Ingreso:' : '7.2.2 Salida:';
        return tipo === 'ingreso' ? '7.1.1 Ingreso:' : '7.1.2 Salida:';
    }

    function m7_agregar_salida_combustible() {
        const diesel = document.getElementById('m7_diesel_qty').value;
        const gasohol = document.getElementById('m7_gasohol_qty').value;
        const categoriaAnterior = m7_categoria_actual;
        const tipoAnterior = m7_tipo_actual;
        m7_categoria_actual = 'combustible';
        m7_tipo_actual = 'salida';
        if(diesel) m7_agregar_fila({ material: 'DIESEL B5 S-50', unidad: 'GLN', cantidad: diesel });
        if(gasohol) m7_agregar_fila({ material: 'GASOHOL REGULAR', unidad: 'GLN', cantidad: gasohol });
        document.getElementById('m7_diesel_qty').value = '';
        document.getElementById('m7_gasohol_qty').value = '';
        m7_categoria_actual = categoriaAnterior;
        m7_tipo_actual = tipoAnterior;
        m7_cambiar_categoria('combustible');
        m7_cambiar_tipo('salida');
    }

    function m7_escape_attr(value) {
        return String(value || '')
            .replace(/&/g, '&amp;')
            .replace(/"/g, '&quot;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
    }

    function m7_sincronizar() {
        const partes = [];
        ['materiales', 'combustible'].forEach(cat => {
            const ingreso = window.m7_movimientos[cat].ingreso.map(m7_formato_item).filter(Boolean);
            const salida = window.m7_movimientos[cat].salida.map(m7_formato_item).filter(Boolean);
            if(ingreso.length > 0 || salida.length > 0) {
                const bloque = [m7_titulo_categoria(cat)];
                bloque.push(`${m7_numero_movimiento(cat, 'ingreso')} ${ingreso.join('; ')}`);
                bloque.push(`${m7_numero_movimiento(cat, 'salida')} ${salida.join('; ')}`);
                partes.push(bloque.join('\\n'));
            }
        });

        document.getElementById('v_almacen').value = partes.join('\\n');
        if (typeof sincronizarDatos === 'function') sincronizarDatos();
    }

    function m7_render() {
        const tbody = document.getElementById('m7_tbody');
        const lista = m7_movs();
        const quick = document.getElementById('m7_fuel_quick');
        if(quick) quick.classList.toggle('active', m7_categoria_actual === 'combustible' && m7_tipo_actual === 'salida');
        if(lista.length === 0) {
            tbody.innerHTML = `<tr><td colspan="6"><div class="m7-empty">No hay ${m7_categoria_actual === 'combustible' ? 'combustible' : 'materiales'} registrados en ${m7_tipo_actual}.</div></td></tr>`;
            m7_sincronizar();
            return;
        }

        tbody.innerHTML = lista.map((m, idx) => `
            <tr>
                <td><input value="${m7_escape_attr(m.numero)}" oninput="m7_actualizar(${idx}, 'numero', this.value)"></td>
                <td><input value="${m7_escape_attr(m.documento)}" placeholder="Contrato / Servicio / O.C." oninput="m7_actualizar(${idx}, 'documento', this.value)"></td>
                <td><input value="${m7_escape_attr(m.material)}" placeholder="${m7_categoria_actual === 'combustible' ? 'Combustible' : 'Material'}" oninput="m7_actualizar(${idx}, 'material', this.value)"></td>
                <td><input value="${m7_escape_attr(m.unidad)}" placeholder="UND" oninput="m7_actualizar(${idx}, 'unidad', this.value)"></td>
                <td><input value="${m7_escape_attr(m.cantidad)}" placeholder="0.00" oninput="m7_actualizar(${idx}, 'cantidad', this.value)"></td>
                <td class="text-center"><button type="button" class="btn btn-sm text-danger border-0" onclick="m7_eliminar(${idx})"><i class="bi bi-trash"></i></button></td>
            </tr>
        `).join('');
        m7_sincronizar();
    }

    setTimeout(() => {
        const paste = document.getElementById('m7_paste_input');
        if(!paste) return;
        paste.addEventListener('paste', function(e) {
            e.preventDefault();
            const data = (e.clipboardData || window.clipboardData).getData('text');
            if(!data.trim()) return;
            let count = 0;
            data.split('\\n').forEach(row => {
                if(!row.trim()) return;
                const parsed = m7_parse_row(row.split('\\t'));
                if(parsed && parsed.material) {
                    m7_agregar_fila(parsed);
                    count++;
                }
            });
            paste.value = count > 0 ? `Se pegaron ${count} materiales.` : '';
            setTimeout(() => paste.value = '', 1200);
        });
        m7_render();
    }, 300);
</script>
"""


mod_07_bp = Blueprint("almacen", __name__)


@mod_07_bp.route("/almacen")
def panel_almacen():
    es_admin = session.get("rol") == "Admin"
    nombre_usuario = session.get("nombre", "Visitante")
    menu_superior = obtener_navbar(es_admin, nombre_usuario)

    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>SAMU - Movimientos de Almacén</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
            <style>
                :root {
                    --samu-text: #1d1d1f;
                    --samu-gray: #6b7280;
                    --samu-border: rgba(15, 23, 42, 0.08);
                    --samu-panel: rgba(255, 255, 255, 0.78);
                }

                body {
                    min-height: 100vh;
                    margin: 0;
                    font-family: 'Inter', Arial, sans-serif;
                    color: var(--samu-text);
                    background: #f8fafc;
                    overflow-x: hidden;
                }

                .almacen-bg {
                    position: fixed;
                    inset: 0;
                    z-index: -2;
                    background:
                        radial-gradient(circle at 15% 15%, rgba(14, 165, 233, 0.18), transparent 34%),
                        radial-gradient(circle at 85% 8%, rgba(245, 158, 11, 0.16), transparent 28%),
                        linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
                }

                .almacen-bg::after {
                    content: "";
                    position: absolute;
                    inset: 0;
                    background-image:
                        linear-gradient(rgba(15, 23, 42, 0.035) 1px, transparent 1px),
                        linear-gradient(90deg, rgba(15, 23, 42, 0.035) 1px, transparent 1px);
                    background-size: 42px 42px;
                    mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 0.85), transparent);
                }

                .almacen-shell {
                    width: 100%;
                    min-height: 100vh;
                    padding: 110px 20px 46px;
                }

                .almacen-container {
                    max-width: 1100px;
                    margin: 0 auto;
                }

                .almacen-hero {
                    display: grid;
                    grid-template-columns: 1.4fr 0.6fr;
                    gap: 24px;
                    align-items: stretch;
                    margin-bottom: 28px;
                }

                .hero-card,
                .status-card,
                .movement-card {
                    background: var(--samu-panel);
                    border: 1px solid rgba(255, 255, 255, 0.9);
                    border-radius: 28px;
                    box-shadow: 0 24px 70px rgba(15, 23, 42, 0.08);
                    backdrop-filter: blur(22px);
                    -webkit-backdrop-filter: blur(22px);
                }

                .hero-card {
                    padding: 34px;
                }

                .module-kicker {
                    display: inline-flex;
                    align-items: center;
                    gap: 8px;
                    padding: 8px 13px;
                    border-radius: 999px;
                    background: #0f172a;
                    color: #ffffff;
                    font-size: 12px;
                    font-weight: 800;
                    letter-spacing: 0.08em;
                    text-transform: uppercase;
                    margin-bottom: 18px;
                }

                .hero-card h1 {
                    margin: 0;
                    font-size: clamp(34px, 5vw, 58px);
                    font-weight: 800;
                    letter-spacing: -2px;
                    line-height: 0.98;
                }

                .hero-card p {
                    max-width: 660px;
                    margin: 18px 0 0;
                    color: var(--samu-gray);
                    font-size: 17px;
                    line-height: 1.7;
                }

                .status-card {
                    padding: 28px;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                    min-height: 250px;
                }

                .status-icon {
                    width: 62px;
                    height: 62px;
                    display: grid;
                    place-items: center;
                    border-radius: 20px;
                    color: #ffffff;
                    background: linear-gradient(135deg, #0f172a, #334155);
                    box-shadow: 0 18px 38px rgba(15, 23, 42, 0.2);
                    font-size: 28px;
                }

                .status-card span {
                    color: var(--samu-gray);
                    font-size: 12px;
                    font-weight: 800;
                    letter-spacing: 0.08em;
                    text-transform: uppercase;
                }

                .status-card strong {
                    display: block;
                    margin-top: 6px;
                    font-size: 24px;
                    letter-spacing: -0.5px;
                }

                .movement-grid {
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 24px;
                }

                .movement-card {
                    position: relative;
                    min-height: 310px;
                    padding: 30px;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                    text-decoration: none;
                    color: inherit;
                    overflow: hidden;
                    transition: transform 0.28s ease, box-shadow 0.28s ease, border-color 0.28s ease;
                }

                .movement-card:hover {
                    transform: translateY(-6px);
                    color: inherit;
                    border-color: rgba(15, 23, 42, 0.16);
                    box-shadow: 0 32px 85px rgba(15, 23, 42, 0.14);
                }

                .movement-card::before {
                    content: "";
                    position: absolute;
                    inset: auto -15% -32% auto;
                    width: 260px;
                    height: 260px;
                    border-radius: 50%;
                    opacity: 0.16;
                    transition: transform 0.28s ease;
                }

                .movement-card:hover::before {
                    transform: scale(1.08);
                }

                .movement-card.materiales::before {
                    background: #0284c7;
                }

                .movement-card.combustible::before {
                    background: #f59e0b;
                }

                .movement-icon {
                    width: 76px;
                    height: 76px;
                    display: grid;
                    place-items: center;
                    border-radius: 24px;
                    color: #ffffff;
                    font-size: 34px;
                    box-shadow: 0 18px 40px rgba(15, 23, 42, 0.16);
                }

                .materiales .movement-icon {
                    background: linear-gradient(135deg, #0369a1, #0ea5e9);
                }

                .combustible .movement-icon {
                    background: linear-gradient(135deg, #b45309, #f59e0b);
                }

                .movement-content {
                    position: relative;
                    z-index: 1;
                }

                .movement-content h2 {
                    max-width: 420px;
                    margin: 26px 0 12px;
                    font-size: clamp(25px, 3vw, 34px);
                    font-weight: 800;
                    letter-spacing: -1.1px;
                    line-height: 1.05;
                }

                .movement-content p {
                    margin: 0;
                    color: var(--samu-gray);
                    font-size: 15px;
                    line-height: 1.6;
                }

                .movement-action {
                    position: relative;
                    z-index: 1;
                    display: inline-flex;
                    align-items: center;
                    gap: 10px;
                    width: fit-content;
                    margin-top: 30px;
                    padding: 13px 18px;
                    border-radius: 999px;
                    background: #0f172a;
                    color: #ffffff;
                    font-weight: 800;
                    font-size: 13px;
                    letter-spacing: 0.02em;
                }

                .combustible .movement-action {
                    background: #92400e;
                }

                @media (max-width: 860px) {
                    .almacen-shell { padding-top: 88px; }
                    .almacen-hero,
                    .movement-grid {
                        grid-template-columns: 1fr;
                    }
                    .status-card {
                        min-height: auto;
                        gap: 24px;
                    }
                }

                @media (max-width: 560px) {
                    .almacen-shell {
                        padding-left: 14px;
                        padding-right: 14px;
                    }
                    .hero-card,
                    .status-card,
                    .movement-card {
                        border-radius: 22px;
                        padding: 24px;
                    }
                    .movement-card {
                        min-height: 285px;
                    }
                }
            </style>
        </head>
        <body>
            {{ menu_superior | safe }}
            <div class="almacen-bg"></div>

            <main class="almacen-shell">
                <section class="almacen-container">
                    <div class="almacen-hero">
                        <div class="hero-card">
                            <div class="module-kicker">
                                <i class="bi bi-box-seam"></i>
                                Modulo 7
                            </div>
                            <h1>Movimientos de Almacen</h1>
                            <p>
                                Centro operativo para registrar salidas, ingresos y control de recursos
                                criticos de obra, manteniendo trazabilidad para residencia, almacen y maquinaria.
                            </p>
                        </div>

                        <aside class="status-card">
                            <div class="status-icon">
                                <i class="bi bi-clipboard-data"></i>
                            </div>
                            <div>
                                <span>SAMU Ingenieria</span>
                                <strong>Control logistico listo</strong>
                            </div>
                        </aside>
                    </div>

                    <div class="movement-grid">
                        <a class="movement-card materiales" href="{{ url_for('almacen.movimiento_materiales') }}">
                            <div class="movement-content">
                                <div class="movement-icon">
                                    <i class="bi bi-bricks"></i>
                                </div>
                                <h2>Movimiento de Materiales de Construccion</h2>
                                <p>
                                    Flujo preparado para gestionar agregados, cemento, acero, tuberias,
                                    geosinteticos y consumibles de obra.
                                </p>
                            </div>
                            <div class="movement-action">
                                Abrir movimiento
                                <i class="bi bi-arrow-right"></i>
                            </div>
                        </a>

                        <a class="movement-card combustible" href="{{ url_for('almacen.movimiento_combustible') }}">
                            <div class="movement-content">
                                <div class="movement-icon">
                                    <i class="bi bi-fuel-pump-fill"></i>
                                </div>
                                <h2>Movimiento de Combustible</h2>
                                <p>
                                    Ruta lista para el control de despacho, consumo y trazabilidad de
                                    combustible asociado a maquinaria y frentes de trabajo.
                                </p>
                            </div>
                            <div class="movement-action">
                                Abrir control
                                <i class="bi bi-arrow-right"></i>
                            </div>
                        </a>
                    </div>
                </section>
            </main>
        </body>
        </html>
        """,
        menu_superior=menu_superior,
    )


@mod_07_bp.route("/almacen/materiales")
def movimiento_materiales():
    return render_template_string(
        _PANTALLA_MOVIMIENTO_HTML,
        menu_superior=obtener_navbar(session.get("rol") == "Admin", session.get("nombre", "Visitante")),
        titulo="Movimiento de Materiales de Construccion",
        subtitulo="Registro operativo para entradas, salidas y control de materiales de obra.",
        icono="bi-box-seam-fill",
        color="#0284c7",
        etiqueta="Almacen / Obra",
        campos=[
            "Fecha del movimiento",
            "Material",
            "Unidad",
            "Cantidad",
            "Frente de trabajo",
            "Responsable",
        ],
    )


@mod_07_bp.route("/almacen/combustible")
def movimiento_combustible():
    return render_template_string(
        _PANTALLA_MOVIMIENTO_HTML,
        menu_superior=obtener_navbar(session.get("rol") == "Admin", session.get("nombre", "Visitante")),
        titulo="Movimiento de Combustible",
        subtitulo="Control de despacho, consumo y trazabilidad para maquinaria y frentes.",
        icono="bi-fuel-pump-fill",
        color="#d97706",
        etiqueta="Combustible / Maquinaria",
        campos=[
            "Fecha del despacho",
            "Equipo o maquinaria",
            "Tipo de combustible",
            "Galones",
            "Horometro / kilometraje",
            "Operador responsable",
        ],
    )


_PANTALLA_MOVIMIENTO_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>SAMU - {{ titulo }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {
            min-height: 100vh;
            margin: 0;
            font-family: 'Inter', Arial, sans-serif;
            background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
            color: #1d1d1f;
        }

        .mov-shell {
            min-height: 100vh;
            padding: 100px 20px 44px;
        }

        .mov-container {
            max-width: 980px;
            margin: 0 auto;
        }

        .mov-card {
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid rgba(255, 255, 255, 0.92);
            border-radius: 28px;
            box-shadow: 0 26px 80px rgba(15, 23, 42, 0.1);
            backdrop-filter: blur(22px);
            -webkit-backdrop-filter: blur(22px);
            overflow: hidden;
        }

        .mov-header {
            padding: 34px;
            border-bottom: 1px solid rgba(15, 23, 42, 0.07);
            display: flex;
            gap: 22px;
            align-items: center;
        }

        .mov-icon {
            width: 76px;
            height: 76px;
            flex: 0 0 76px;
            display: grid;
            place-items: center;
            border-radius: 24px;
            background: {{ color }};
            color: #fff;
            font-size: 34px;
            box-shadow: 0 18px 42px color-mix(in srgb, {{ color }} 35%, transparent);
        }

        .mov-kicker {
            display: inline-flex;
            padding: 7px 12px;
            margin-bottom: 8px;
            border-radius: 999px;
            background: rgba(15, 23, 42, 0.08);
            color: #334155;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        h1 {
            margin: 0;
            font-size: clamp(30px, 4vw, 46px);
            font-weight: 800;
            letter-spacing: -1.5px;
            line-height: 1.02;
        }

        .mov-header p {
            margin: 10px 0 0;
            color: #64748b;
            font-size: 16px;
            line-height: 1.6;
        }

        .mov-body {
            padding: 34px;
        }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 18px;
        }

        .field-box {
            background: #fff;
            border: 1px solid rgba(15, 23, 42, 0.08);
            border-radius: 18px;
            padding: 16px;
        }

        .field-box label {
            display: block;
            margin-bottom: 8px;
            color: #64748b;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .field-box input {
            width: 100%;
            border: 0;
            outline: 0;
            color: #0f172a;
            font-size: 16px;
            font-weight: 600;
        }

        .mov-actions {
            display: flex;
            justify-content: space-between;
            gap: 14px;
            margin-top: 28px;
            flex-wrap: wrap;
        }

        .btn-back,
        .btn-save {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            border: 0;
            border-radius: 999px;
            padding: 14px 20px;
            font-weight: 800;
            text-decoration: none;
        }

        .btn-back {
            background: #e2e8f0;
            color: #334155;
        }

        .btn-save {
            background: #0f172a;
            color: #fff;
        }

        @media (max-width: 720px) {
            .mov-header {
                flex-direction: column;
                align-items: flex-start;
            }

            .form-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    {{ menu_superior | safe }}
    <main class="mov-shell">
        <section class="mov-container">
            <div class="mov-card">
                <div class="mov-header">
                    <div class="mov-icon">
                        <i class="bi {{ icono }}"></i>
                    </div>
                    <div>
                        <span class="mov-kicker">{{ etiqueta }}</span>
                        <h1>{{ titulo }}</h1>
                        <p>{{ subtitulo }}</p>
                    </div>
                </div>

                <div class="mov-body">
                    <form>
                        <div class="form-grid">
                            {% for campo in campos %}
                            <div class="field-box">
                                <label>{{ campo }}</label>
                                <input type="text" placeholder="Ingrese {{ campo | lower }}">
                            </div>
                            {% endfor %}
                        </div>

                        <div class="mov-actions">
                            <a class="btn-back" href="{{ url_for('almacen.panel_almacen') }}">
                                <i class="bi bi-arrow-left"></i>
                                Volver a Almacen
                            </a>
                            <button class="btn-save" type="button">
                                <i class="bi bi-check2-circle"></i>
                                Guardar movimiento
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </section>
    </main>
</body>
</html>
"""
