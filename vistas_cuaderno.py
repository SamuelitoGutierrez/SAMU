# =========================================================
# vistas_cuaderno.py
# Módulo: Cuaderno de Obra Digital - Lobby Central (Responsivo)
# =========================================================

import json

from flask import Blueprint, render_template_string, session, redirect, url_for, request, jsonify
from navbar import obtener_navbar
from cuaderno_store import obtener_panel_cuaderno, obtener_asiento, obtener_datos_mes_cuaderno

cuaderno_bp = Blueprint('cuaderno', __name__)


@cuaderno_bp.route('/cuaderno/api/dashboard')
def api_dashboard_cuaderno():
    if 'usuario_id' not in session:
        return jsonify({"ok": False, "error": "No autorizado"}), 401
    try:
        year = int(request.args.get("year"))
        month = int(request.args.get("month"))
    except (TypeError, ValueError):
        return jsonify({"ok": False, "error": "Mes o año inválido"}), 400
    if month < 1 or month > 12:
        return jsonify({"ok": False, "error": "Mes fuera de rango"}), 400
    return jsonify(obtener_datos_mes_cuaderno(year, month))


@cuaderno_bp.route('/cuaderno/asiento/<int:numero>')
def ver_asiento_cuaderno(numero):
    if 'usuario_id' not in session:
        return redirect(url_for('login.mostrar_login'))

    asiento = obtener_asiento(numero)
    if not asiento:
        return redirect(url_for('cuaderno.panel_cuaderno'))

    import json
    contenido = asiento.get("contenido") or "{}"
    try:
        contenido = json.loads(contenido) if isinstance(contenido, str) else contenido
    except Exception:
        contenido = {}

    html_cuaderno = (contenido or {}).get("texto_html") or "<div class='empty-state'>No hay contenido guardado para este asiento.</div>"
    modulos_json = json.dumps((contenido or {}).get("modulos") or [], ensure_ascii=False)
    fecha_texto = (contenido or {}).get("fecha_texto") or asiento.get("fecha") or ""
    menu_superior = obtener_navbar(session.get('rol') == 'Admin', session.get('nombre', 'Visitante'))

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Asiento {{ asiento.numero }} — Cuaderno de Obra</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <style>
            body { margin: 0; min-height: 100vh; font-family: Inter, Arial, sans-serif; background: linear-gradient(135deg,#f8fafc,#eff6ff); color: #0f172a; }
            .asiento-view { max-width: 980px; margin: 0 auto; padding: 96px 18px 42px; }
            .asiento-head { display: flex; justify-content: space-between; gap: 12px; align-items: center; flex-wrap: wrap; margin-bottom: 18px; }
            .asiento-head h1 { margin: 0; font-size: 28px; font-weight: 900; letter-spacing: -.8px; }
            .asiento-actions { display: flex; gap: 8px; flex-wrap: wrap; }
            .asiento-btn { border: 0; border-radius: 999px; padding: 10px 14px; font-size: 12px; font-weight: 900; text-decoration: none; color: #fff; background: #0f172a; }
            .asiento-btn.pdf { background: linear-gradient(135deg,#991b1b,#ef4444); }
            .asiento-paper { background: #fff; border-radius: 28px; padding: 20px; box-shadow: 0 24px 60px rgba(15,23,42,.12); overflow-x: auto; }
            .pagina-cuaderno { background-image: repeating-linear-gradient(transparent, transparent 25px, #cbd5e1 26px); line-height: 26px; min-height: 760px; padding-top: 0; position: relative; }
            .lapicero { font-family: Candara, Calibri, Arial, sans-serif; font-style: italic; color: #0263a0; font-size: 17px; line-height: 26px; padding-left: 2px; font-weight: 400; text-align: justify; word-wrap: break-word; }
            .encabezado-asiento { position: relative; margin: 0 0 3px; min-height: 26px; font-weight: 700; }
            .titulo-asiento { width: 100%; text-align: center; text-transform: uppercase; font-weight: 800; padding: 0 128px 0 8px; white-space: nowrap; }
            .fecha-asiento { position: absolute; top: 0; right: 0; text-align: right; white-space: nowrap; }
            .modulo-titulo { display: block; font-weight: 700; color: #075985; }
            .modulo-contenido { display: block; padding-left: 22px; white-space: pre-wrap; }
            .van-final { display: block; text-align: right; padding-right: 8px; font-weight: 800; color: #075985; }
            .p-header-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 18px; }
            .p-title-box { text-align: center; flex: 1; margin-left: 60px; }
            .p-title-box h1 { font-size: 28px; font-weight: bold; text-decoration: underline; letter-spacing: 1.5px; margin: 0; }
            .p-num { font-size: 24px; font-weight: bold; }
            .p-meta { margin-bottom: 6px; padding-bottom: 7px; border-bottom: 3px solid #000; }
            .p-row { display: flex; align-items: flex-end; margin-bottom: 4px; }
            .p-label { font-size: 14px; font-weight: bold; margin-right: 8px; }
            .p-line { flex: 1; border-bottom: 1px solid #000; position: relative; height: 20px; }
            .lapicero-meta { position: absolute; bottom: -1px; left: 10px; font-family: Candara, Calibri, Arial, sans-serif; font-style: italic; color: #0263a0; font-size: 17px; font-weight: 500; white-space: nowrap; }
            .p-footer { display: flex; justify-content: space-between; margin-top: 46px; font-size: 12px; font-weight: bold; color: #000; }
            .p-sig { border-top: 1px solid #000; width: 28%; text-align: center; padding-top: 5px; }
            @media print {
                body { background: #fff; }
                body * { visibility: hidden !important; }
                #asientoPaper, #asientoPaper * { visibility: visible !important; }
                @page { size: A4; margin: 0; }
                #asientoPaper { position: absolute; left: 0; top: 0; width: 210mm; box-shadow: none; border-radius: 0; padding: 0; background: #fff; }
                #asientoPaper .papel-fisico { width: 210mm !important; height: 297mm !important; min-height: 297mm !important; box-sizing: border-box !important; padding: 12mm 14mm 14mm !important; margin: 0 !important; box-shadow: none !important; border: none !important; page-break-after: always; break-after: page; display: flex; flex-direction: column; overflow: hidden; background: #fdfdfa !important; }
                #asientoPaper .papel-fisico:last-child { page-break-after: auto; break-after: auto; }
                #asientoPaper .p-header-top { flex: 0 0 auto; margin-bottom: 7mm !important; }
                #asientoPaper .p-meta { flex: 0 0 auto; margin-bottom: 3mm !important; padding-bottom: 2mm !important; }
                #asientoPaper .p-body-lines { flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; }
                #asientoPaper .pagina-cuaderno { flex: 1 1 auto; min-height: 0 !important; background-size: auto 26px; background-image: repeating-linear-gradient(transparent, transparent 25px, #cbd5e1 26px) !important; display: flex; flex-direction: column; }
                #asientoPaper .lapicero { flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; font-size: 17px; line-height: 26px; }
                #asientoPaper .van-final { margin-top: auto !important; text-align: right !important; padding-right: 8px !important; }
                #asientoPaper .p-footer { flex: 0 0 auto; margin-top: 10mm !important; padding-top: 0 !important; }
            }
        </style>
    </head>
    <body>
        {{ menu_superior | safe }}
        <main class="asiento-view">
            <div class="asiento-head">
                <div>
                    <h1>Asiento N° {{ asiento.numero }}</h1>
                    <div class="text-muted fw-bold small">{{ asiento.fecha }} · {{ asiento.estado }} · Avance {{ asiento.avance }}%</div>
                </div>
                <div class="asiento-actions">
                    <a class="asiento-btn" href="/cuaderno"><i class="bi bi-arrow-left"></i> Volver al calendario</a>
                    <button class="asiento-btn pdf" onclick="exportarAsientoPDF()"><i class="bi bi-filetype-pdf"></i> Exportar PDF</button>
                </div>
            </div>
            <section class="asiento-paper" id="asientoPaper">
                {{ html_cuaderno | safe }}
            </section>
        </main>
        <script>
            const asientoModulos = {{ modulos_json | safe }};
            const asientoNumero = "{{ asiento.numero }}".padStart(4, "0");
            const asientoFechaTexto = {{ fecha_texto | tojson }};
            const asientoHtmlNormal = document.getElementById('asientoPaper')?.innerHTML || '';

            function esc(v) {
                return String(v || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
            }

            function htmlModuloVista(modulo) {
                return `<div class="modulo-redaccion"><span class="modulo-titulo">${esc(modulo.titulo)}</span><span class="modulo-contenido">${esc(modulo.contenido || '-').replace(/\\n/g, '<br>')}</span></div>`;
            }

            function lineasModuloVista(modulo) {
                return 1 + String(modulo.contenido || '-').split('\\n').reduce((sum, linea) => sum + Math.max(1, Math.ceil(String(linea || '').length / 82)), 0);
            }

            function dividirModuloVista(modulo, maxLineas) {
                const lineas = String(modulo.contenido || '-').split('\\n');
                const primera = [];
                const segunda = [];
                let usadas = 1;
                lineas.forEach(linea => {
                    const peso = Math.max(1, Math.ceil(String(linea || '').length / 82));
                    if (usadas + peso <= maxLineas || primera.length === 0) {
                        primera.push(linea);
                        usadas += peso;
                    } else {
                        segunda.push(linea);
                    }
                });
                return [{...modulo, contenido: primera.join('\\n') || '-'}, {...modulo, contenido: segunda.join('\\n')}];
            }

            function paginarVista(modulos) {
                const paginas = [];
                let actual = [];
                let usadas = 1;
                let continuacion = false;
                const maxLineasPagina = () => continuacion ? 32 : 24;
                modulos.forEach(original => {
                    let pendiente = {...original};
                    while (pendiente && String(pendiente.contenido || '').trim()) {
                        const lineas = lineasModuloVista(pendiente);
                        if (usadas + lineas <= maxLineasPagina()) {
                            actual.push(pendiente);
                            usadas += lineas;
                            pendiente = null;
                        } else {
                            const espacioRestante = maxLineasPagina() - usadas;
                            if (actual.length > 0 && espacioRestante > 1) {
                                const partes = dividirModuloVista(pendiente, espacioRestante);
                                actual.push(partes[0]);
                                paginas.push({modulos: actual, continuacion, van: true});
                                actual = [];
                                usadas = 1;
                                continuacion = true;
                                pendiente = partes[1].contenido.trim() ? partes[1] : null;
                                continue;
                            }

                            if (actual.length > 0) {
                                paginas.push({modulos: actual, continuacion, van: true});
                                actual = [];
                                usadas = 1;
                                continuacion = true;
                                continue;
                            }

                            const partes = dividirModuloVista(pendiente, maxLineasPagina() - usadas);
                            actual.push(partes[0]);
                            paginas.push({modulos: actual, continuacion, van: true});
                            actual = [];
                            usadas = 1;
                            continuacion = true;
                            pendiente = partes[1].contenido.trim() ? partes[1] : null;
                        }
                    }
                });
                paginas.push({modulos: actual, continuacion, van: false});
                return paginas;
            }

            function encabezadoVista(continuacion) {
                const titulo = continuacion ? `... viene del ASIENTO N° ${asientoNumero} DEL RESIDENTE DE OBRA` : `ASIENTO N° ${asientoNumero} DEL RESIDENTE DE OBRA`;
                return `<div class="encabezado-asiento"><div class="titulo-asiento">${esc(titulo)}</div><div class="fecha-asiento">${esc(asientoFechaTexto)}</div></div>`;
            }

            function prepararAsientoPDF() {
                if (!Array.isArray(asientoModulos) || asientoModulos.length === 0) return;
                document.getElementById('asientoPaper').innerHTML = paginarVista(asientoModulos).map((p, idx) => `
                    <div class="papel-fisico hoja-pdf">
                        ${idx === 0 ? encabezadoGeneralVista() : ''}
                        <div class="p-body-lines">
                            <div class="pagina-cuaderno"><div class="lapicero">
                                ${encabezadoVista(p.continuacion)}
                                ${p.modulos.map(htmlModuloVista).join('')}
                                ${p.van ? '<span class="van-final">Van ...</span>' : ''}
                            </div></div>
                        </div>
                        ${firmasVista()}
                    </div>
                `).join('');
            }

            function encabezadoGeneralVista() {
                return `
                    <div class="p-header-top">
                        <div style="width: 80px;"></div>
                        <div class="p-title-box"><h1>CUADERNO DE OBRA</h1></div>
                        <div style="text-align: right; width: 80px;"><div class="p-num">No <span style="font-size: 26px; margin-left:3px;">${asientoNumero}</span></div></div>
                    </div>
                    <div class="p-meta">
                        <div class="d-flex w-100 mb-1">
                            <div class="d-flex" style="flex: 0.5;"><span class="p-label">Fecha:</span><div class="p-line"><span class="lapicero-meta">${esc(asientoFechaTexto)}</span></div></div>
                            <div class="d-flex" style="flex: 0.5; margin-left: 15px;"><span class="p-label">Modalidad:</span><div class="p-line"><span class="lapicero-meta">Administracion Directa</span></div></div>
                        </div>
                        <div class="p-row"><span class="p-label">Obra:</span><div class="p-line"><span class="lapicero-meta">Mejoramiento de la Carretera Asiruni - Rosaspata</span></div></div>
                        <div class="p-row"><span class="p-label">Proyecto:</span><div class="p-line"><span class="lapicero-meta">Tramo I</span></div></div>
                        <div class="p-row"><span class="p-label">Programa:</span><div class="p-line"><span class="lapicero-meta">-</span></div></div>
                        <div class="p-row"><span class="p-label">Entidad Ejecutora:</span><div class="p-line"><span class="lapicero-meta">Gobierno Regional Puno</span></div></div>
                    </div>
                `;
            }

            function firmasVista() {
                return '<div class="p-footer"><div class="p-sig">ING. INSPECTOR</div><div class="p-sig">ING. RESIDENTE</div><div class="p-sig">ING. SUPERVISOR</div></div>';
            }

            function exportarAsientoPDF() {
                prepararAsientoPDF();
                imprimirAsientoEnVentana();
                setTimeout(() => { document.getElementById('asientoPaper').innerHTML = asientoHtmlNormal; }, 700);
            }

            function imprimirAsientoEnVentana() {
                const contenido = document.getElementById('asientoPaper');
                if (!contenido || !contenido.innerHTML.trim()) return;
                const ventana = window.open('', '_blank', 'width=980,height=720');
                if (!ventana) {
                    window.print();
                    return;
                }
                ventana.document.open();
                ventana.document.write(`
                    <!DOCTYPE html>
                    <html lang="es">
                    <head>
                        <meta charset="UTF-8">
                        <title>cuaderno_obra_${asientoNumero}.pdf</title>
                        <style>
                            @page { size: A4; margin: 0; }
                            html, body { margin: 0; padding: 0; background: #fff; }
                            body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
                            .papel-fisico { width: 210mm; height: 297mm; min-height: 297mm; box-sizing: border-box; padding: 12mm 14mm 14mm; margin: 0; page-break-after: always; break-after: page; display: flex; flex-direction: column; overflow: hidden; background: #fdfdfa; border: none; box-shadow: none; font-family: Arial, sans-serif; color: #000; }
                            .papel-fisico:last-child { page-break-after: auto; break-after: auto; }
                            .p-header-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 7mm; flex: 0 0 auto; }
                            .p-title-box { text-align: center; flex: 1; margin-left: 60px; }
                            .p-title-box h1 { font-size: 28px; font-weight: bold; text-decoration: underline; letter-spacing: 1.5px; margin: 0; }
                            .p-num { font-size: 24px; font-weight: bold; }
                            .p-meta { flex: 0 0 auto; margin-bottom: 3mm; padding-bottom: 2mm; border-bottom: 3px solid #000; }
                            .p-row { display: flex; align-items: flex-end; margin-bottom: 4px; }
                            .p-label { font-size: 14px; font-weight: bold; margin-right: 8px; }
                            .p-line { flex: 1; border-bottom: 1px solid #000; position: relative; height: 20px; }
                            .lapicero-meta { position: absolute; bottom: -1px; left: 10px; font-family: Candara, Calibri, Arial, sans-serif; font-style: italic; color: #0263a0; font-size: 17px; font-weight: 500; white-space: nowrap; }
                            .p-body-lines { flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; }
                            .pagina-cuaderno { flex: 1 1 auto; min-height: 0; background-image: repeating-linear-gradient(transparent, transparent 25px, #cbd5e1 26px); background-size: auto 26px; line-height: 26px; display: flex; flex-direction: column; }
                            .lapicero { flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; font-family: Candara, Calibri, Arial, sans-serif; font-style: italic; color: #0263a0; font-size: 17px; line-height: 26px; padding-left: 2px; font-weight: 400; text-align: justify; word-wrap: break-word; }
                            .encabezado-asiento { position: relative; margin: 0 0 3px; min-height: 26px; font-weight: 700; }
                            .titulo-asiento { width: 100%; text-align: center; text-transform: uppercase; font-weight: 800; padding: 0 128px 0 8px; white-space: nowrap; }
                            .fecha-asiento { position: absolute; top: 0; right: 0; text-align: right; white-space: nowrap; }
                            .modulo-titulo { display: block; font-weight: 700; color: #075985; }
                            .modulo-contenido { display: block; padding-left: 22px; text-indent: 0; white-space: pre-wrap; }
                            .van-final { margin-top: auto; display: block; text-align: right; padding-right: 8px; font-weight: 800; color: #075985; }
                            .p-footer { flex: 0 0 auto; display: flex; justify-content: space-between; margin-top: 10mm; font-size: 12px; font-weight: bold; color: #000; }
                            .p-sig { border-top: 1px solid #000; width: 28%; text-align: center; padding-top: 5px; }
                        </style>
                    </head>
                    <body>${contenido.innerHTML}</body>
                    </html>
                `);
                ventana.document.close();
                ventana.focus();
                setTimeout(() => ventana.print(), 350);
            }
        </script>
    </body>
    </html>
    """, asiento=asiento, html_cuaderno=html_cuaderno, modulos_json=modulos_json, fecha_texto=fecha_texto, menu_superior=menu_superior)

# NOTA IMPORTANTE: Ahora SOLO maneja la ruta /cuaderno. 
# Esto permite que vistas_residencia.py funcione correctamente sin interferencias.
@cuaderno_bp.route('/cuaderno')
def panel_cuaderno():
    if 'usuario_id' not in session: 
        return redirect(url_for('login.mostrar_login'))

    es_admin = session.get('rol') == 'Admin'
    nombre_completo = session.get('nombre', 'Visitante')
    menu_superior = obtener_navbar(es_admin, nombre_completo)

    rol_usuario = session.get('rol', '')
    panel = obtener_panel_cuaderno()
    estadisticas = panel["estadisticas"]
    asientos = panel["asientos"]
    observaciones = panel["observaciones"]
    ultima_observacion = panel.get("ultima_observacion")
    historial = panel.get("historial", [])
    mes_actual = panel.get("mes_actual", {})
    conectado = panel["conectado"]
    asientos_json = json.dumps(asientos, ensure_ascii=False, default=str)
    observaciones_json = json.dumps(observaciones, ensure_ascii=False, default=str)
    historial_json = json.dumps(historial, ensure_ascii=False, default=str)
    mes_actual_json = json.dumps(mes_actual, ensure_ascii=False, default=str)

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>SAMU — Centro de Mando del Cuaderno de Obra</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root {
                --samu-blue: #0263a0;
                --samu-navy: #0f172a;
                --samu-green: #22c55e;
                --samu-yellow: #facc15;
                --samu-red: #ef4444;
                --samu-muted: #64748b;
                --card-bg: rgba(255,255,255,.86);
                --card-border: rgba(226,232,240,.9);
            }

            * { box-sizing: border-box; }
            body {
                margin: 0;
                min-height: 100vh;
                font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                color: var(--samu-navy);
                background:
                    radial-gradient(circle at 6% 8%, rgba(2,99,160,.18), transparent 30%),
                    radial-gradient(circle at 92% 12%, rgba(34,197,94,.14), transparent 28%),
                    linear-gradient(135deg, #f8fafc 0%, #eff6ff 48%, #f8fafc 100%);
                overflow-x: hidden;
            }

            .command-shell {
                width: min(1480px, calc(100% - 40px));
                margin: 0 auto;
                padding: 96px 0 42px;
            }

            .hero-card,
            .command-card {
                border: 1px solid var(--card-border);
                background: var(--card-bg);
                border-radius: 30px;
                box-shadow: 0 24px 70px rgba(15,23,42,.08);
                backdrop-filter: blur(22px);
                -webkit-backdrop-filter: blur(22px);
            }

            .hero-card {
                padding: 24px;
                margin-bottom: 22px;
            }

            .dashboard-title {
                display: flex;
                align-items: flex-start;
                justify-content: space-between;
                gap: 18px;
                margin-bottom: 22px;
            }

            .dashboard-title h1 {
                margin: 0;
                font-size: clamp(32px, 4vw, 58px);
                line-height: .96;
                font-weight: 900;
                letter-spacing: -2.2px;
            }

            .dashboard-title p {
                margin: 12px 0 0;
                max-width: 760px;
                color: var(--samu-muted);
                font-weight: 600;
                font-size: 14px;
                line-height: 1.55;
            }

            .connection-pill {
                flex: 0 0 auto;
                display: inline-flex;
                align-items: center;
                gap: 8px;
                border-radius: 999px;
                padding: 10px 13px;
                background: #dcfce7;
                color: #166534;
                font-size: 12px;
                font-weight: 900;
                white-space: nowrap;
            }

            .connection-pill.offline {
                background: #fee2e2;
                color: #991b1b;
            }

            .action-topbar {
                display: grid;
                grid-template-columns: repeat(2, minmax(230px, 1fr)) minmax(320px, .9fr);
                gap: 14px;
                align-items: stretch;
            }

            .primary-action {
                position: relative;
                min-height: 112px;
                display: flex;
                align-items: center;
                gap: 16px;
                overflow: hidden;
                border-radius: 26px;
                padding: 20px;
                color: #fff;
                text-decoration: none;
                box-shadow: 0 18px 42px rgba(15,23,42,.16);
                transition: transform .22s ease, box-shadow .22s ease;
            }

            .primary-action:hover {
                color: #fff;
                transform: translateY(-4px);
                box-shadow: 0 26px 54px rgba(15,23,42,.22);
            }

            .primary-action.residencia {
                background: linear-gradient(135deg, #0263a0, #0f172a);
            }

            .primary-action.supervision {
                background: linear-gradient(135deg, #7c3aed, #312e81);
            }

            .primary-action::after {
                content: "";
                position: absolute;
                width: 190px;
                height: 190px;
                right: -70px;
                top: -70px;
                border-radius: 50%;
                background: rgba(255,255,255,.16);
            }

            .action-icon {
                width: 64px;
                height: 64px;
                flex: 0 0 auto;
                display: grid;
                place-items: center;
                border-radius: 22px;
                background: rgba(255,255,255,.16);
                font-size: 30px;
            }

            .primary-action small {
                display: block;
                margin-bottom: 5px;
                font-size: 11px;
                font-weight: 900;
                text-transform: uppercase;
                letter-spacing: .8px;
                opacity: .78;
            }

            .primary-action strong {
                display: block;
                font-size: 17px;
                line-height: 1.15;
                font-weight: 900;
            }

            .export-card {
                display: grid;
                gap: 11px;
                align-content: center;
                border: 1px solid #e2e8f0;
                border-radius: 26px;
                padding: 17px;
                background: rgba(248,250,252,.9);
            }

            .export-title {
                display: flex;
                align-items: center;
                gap: 9px;
                font-size: 13px;
                font-weight: 900;
            }

            .range-row {
                display: flex;
                gap: 8px;
                align-items: center;
            }

            .range-row input {
                min-width: 0;
                width: 100%;
                border: 1px solid #cbd5e1;
                border-radius: 13px;
                padding: 10px;
                background: #fff;
                font-size: 12px;
                font-weight: 800;
                outline: none;
            }

            .export-btn {
                border: 0;
                border-radius: 15px;
                padding: 11px 13px;
                background: linear-gradient(135deg, #dc2626, #991b1b);
                color: #fff;
                font-size: 12px;
                font-weight: 900;
                white-space: nowrap;
                box-shadow: 0 14px 28px rgba(220,38,38,.18);
            }

            .stats-strip {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 14px;
                margin: 22px 0;
            }

            .mini-stat {
                border: 1px solid #e2e8f0;
                border-radius: 22px;
                padding: 17px;
                background: rgba(255,255,255,.82);
                box-shadow: 0 14px 34px rgba(15,23,42,.05);
            }

            .mini-stat span {
                display: block;
                color: var(--samu-muted);
                font-size: 11px;
                font-weight: 900;
                text-transform: uppercase;
                letter-spacing: .6px;
            }

            .mini-stat strong {
                display: block;
                margin-top: 8px;
                font-size: 26px;
                font-weight: 900;
                letter-spacing: -1px;
            }

            .main-grid {
                display: grid;
                grid-template-columns: minmax(0, 1.4fr) minmax(360px, .75fr);
                gap: 22px;
            }

            .analytics-grid {
                display: grid;
                grid-template-columns: minmax(280px, .75fr) minmax(0, 1.25fr);
                gap: 18px;
            }

            .command-card {
                padding: 22px;
            }

            .card-head {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                margin-bottom: 18px;
            }

            .card-head h2 {
                margin: 0;
                font-size: 17px;
                font-weight: 900;
                letter-spacing: -.4px;
            }

            .month-controls {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                border: 1px solid #e2e8f0;
                border-radius: 999px;
                padding: 6px;
                background: #fff;
            }

            .month-controls button {
                width: 30px;
                height: 30px;
                border: 0;
                border-radius: 999px;
                background: #f1f5f9;
                color: #0f172a;
                font-weight: 900;
            }

            #monthLabel {
                min-width: 132px;
                text-align: center;
                font-size: 12px;
                font-weight: 900;
                text-transform: uppercase;
                color: #334155;
            }

            .chart-card {
                min-height: 430px;
                display: flex;
                flex-direction: column;
                align-items: center;
            }

            .chart-wrap {
                position: relative;
                width: 350px;
                height: 350px;
                flex: 0 0 350px;
                flex-shrink: 0;
                display: grid;
                place-items: center;
            }

            .chart-wrap canvas {
                width: 350px !important;
                height: 350px !important;
                max-width: 100% !important;
                max-height: 100% !important;
            }

            .chart-center {
                position: absolute;
                inset: 0;
                display: grid;
                place-items: center;
                pointer-events: none;
                text-align: center;
            }

            .chart-center strong {
                display: block;
                font-size: 42px;
                font-weight: 900;
                letter-spacing: -1.8px;
            }

            .chart-center span {
                color: var(--samu-muted);
                font-size: 11px;
                font-weight: 900;
                text-transform: uppercase;
            }

            .legend-dashboard {
                display: grid;
                gap: 9px;
                margin-top: 16px;
            }

            .legend-dashboard div {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 10px;
                border-radius: 999px;
                padding: 9px 12px;
                background: #f8fafc;
                color: #475569;
                font-size: 12px;
                font-weight: 800;
            }

            .dot {
                width: 12px;
                height: 12px;
                border-radius: 999px;
                display: inline-block;
            }

            .calendar-weekdays,
            .calendar-grid {
                display: grid;
                grid-template-columns: repeat(7, 1fr);
                gap: 8px;
            }

            .calendar-grid {
                min-height: 508px;
                grid-template-rows: repeat(6, minmax(78px, 1fr));
                align-content: start;
                padding: 4px;
            }

            .calendar-weekdays {
                margin-bottom: 8px;
                color: #94a3b8;
                font-size: 11px;
                font-weight: 900;
                text-align: center;
                text-transform: uppercase;
            }

            .calendar-day {
                position: relative;
                min-height: 78px;
                border: 1px solid #e2e8f0;
                border-radius: 20px;
                padding: 10px;
                background: #fff;
                color: #334155;
                cursor: pointer;
                transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease, background .2s ease;
                transform-origin: center;
            }

            .calendar-day:hover {
                transform: scale(1.1);
                box-shadow: 0 20px 42px rgba(15,23,42,.16);
                z-index: 6;
            }

            .calendar-day.empty {
                opacity: .35;
                cursor: default;
                background: transparent;
                box-shadow: none;
            }

            .calendar-day.empty:hover {
                transform: none;
                box-shadow: none;
            }

            .calendar-day .day-number {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 28px;
                height: 28px;
                border-radius: 999px;
                font-size: 12px;
                font-weight: 900;
            }

            .calendar-day .day-caption {
                display: block;
                margin-top: 10px;
                color: #64748b;
                font-size: 10px;
                font-weight: 900;
                line-height: 1.25;
            }

            .calendar-day.closed {
                border-color: #bbf7d0;
                background: linear-gradient(135deg, #f0fdf4, #dcfce7);
            }

            .calendar-day.closed .day-number { background: var(--samu-green); color: #fff; }
            .calendar-day.draft {
                border-color: #fde68a;
                background: linear-gradient(135deg, #fefce8, #fef3c7);
            }
            .calendar-day.draft .day-number { background: var(--samu-yellow); color: #713f12; }
            .calendar-day.pending {
                border-color: #fecaca;
                background: linear-gradient(135deg, #fff1f2, #fee2e2);
            }
            .calendar-day.pending .day-number { background: var(--samu-red); color: #fff; }
            .calendar-day.observed {
                border-color: #fdba74;
                background: linear-gradient(135deg, #fff7ed, #ffedd5);
            }
            .calendar-day.observed .day-number { background: #f97316; color: #fff; }

            .calendar-tooltip {
                position: absolute;
                left: 50%;
                bottom: calc(100% + 10px);
                width: 240px;
                transform: translateX(-50%) translateY(8px);
                border-radius: 18px;
                padding: 12px;
                opacity: 0;
                pointer-events: none;
                background: rgba(15,23,42,.96);
                color: #fff;
                box-shadow: 0 22px 45px rgba(15,23,42,.22);
                transition: .18s ease;
                font-size: 11px;
                font-weight: 700;
            }

            .calendar-day:hover .calendar-tooltip {
                opacity: 1;
                transform: translateX(-50%) translateY(0);
            }

            .side-stack {
                display: grid;
                gap: 18px;
                align-content: start;
            }

            .alert-supervision {
                border: 1px solid #fca5a5;
                background: linear-gradient(135deg, #fff7ed, #fee2e2);
                box-shadow: 0 24px 50px rgba(220,38,38,.10);
            }

            .alert-supervision .alert-icon {
                width: 52px;
                height: 52px;
                display: grid;
                place-items: center;
                border-radius: 18px;
                color: #fff;
                background: linear-gradient(135deg, #f97316, #dc2626);
                font-size: 24px;
                box-shadow: 0 14px 28px rgba(220,38,38,.18);
            }

            .alert-copy {
                margin: 0;
                color: #7f1d1d;
                font-size: 13px;
                font-weight: 700;
                line-height: 1.55;
            }

            .timeline {
                position: relative;
                display: grid;
                gap: 0;
            }

            .timeline::before {
                content: "";
                position: absolute;
                left: 14px;
                top: 9px;
                bottom: 12px;
                width: 2px;
                background: #e2e8f0;
            }

            .timeline-item {
                position: relative;
                display: grid;
                grid-template-columns: 34px 1fr;
                gap: 10px;
                padding: 0 0 18px;
            }

            .timeline-item:last-child { padding-bottom: 0; }

            .timeline-dot {
                position: relative;
                z-index: 2;
                width: 30px;
                height: 30px;
                border: 4px solid #fff;
                border-radius: 999px;
                background: var(--samu-blue);
                box-shadow: 0 8px 18px rgba(2,99,160,.18);
            }

            .timeline-box {
                border: 1px solid #e2e8f0;
                border-radius: 18px;
                padding: 12px;
                background: #f8fafc;
            }

            .timeline-box strong {
                display: block;
                margin-bottom: 3px;
                font-size: 12px;
                font-weight: 900;
            }

            .timeline-box span {
                display: block;
                color: #64748b;
                font-size: 12px;
                font-weight: 700;
            }

            .empty-box {
                border: 1px dashed #cbd5e1;
                border-radius: 22px;
                padding: 20px;
                background: #f8fafc;
                color: #64748b;
                font-size: 13px;
                font-weight: 700;
                text-align: center;
            }

            .hidden { display: none !important; }

            .seat-modal-overlay {
                position: fixed;
                inset: 0;
                z-index: 2000;
                display: grid;
                place-items: center;
                padding: 20px;
                background: rgba(15, 23, 42, .68);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
            }

            .seat-modal-card {
                width: min(100%, 460px);
                border: 1px solid rgba(255,255,255,.72);
                border-radius: 30px;
                padding: 24px;
                background: linear-gradient(145deg, rgba(255,255,255,.98), rgba(248,250,252,.94));
                box-shadow: 0 30px 90px rgba(15,23,42,.32);
                animation: modalSeatIn .24s ease both;
            }

            @keyframes modalSeatIn {
                from { opacity: 0; transform: translateY(18px) scale(.96); }
                to { opacity: 1; transform: translateY(0) scale(1); }
            }

            .seat-modal-head {
                display: flex;
                align-items: flex-start;
                justify-content: space-between;
                gap: 14px;
                margin-bottom: 18px;
            }

            .seat-modal-head h3 {
                margin: 0;
                font-size: 22px;
                font-weight: 900;
                letter-spacing: -.8px;
            }

            .seat-modal-head p {
                margin: 6px 0 0;
                color: #64748b;
                font-size: 13px;
                font-weight: 700;
            }

            .seat-modal-close {
                width: 36px;
                height: 36px;
                border: 0;
                border-radius: 999px;
                background: #e2e8f0;
                color: #0f172a;
                font-size: 20px;
                font-weight: 900;
            }

            .seat-modal-form {
                display: grid;
                gap: 14px;
            }

            .seat-field label {
                display: block;
                margin-bottom: 7px;
                color: #334155;
                font-size: 12px;
                font-weight: 900;
                text-transform: uppercase;
                letter-spacing: .5px;
            }

            .seat-field input {
                width: 100%;
                border: 1px solid #cbd5e1;
                border-radius: 18px;
                padding: 13px 14px;
                background: #fff;
                color: #0f172a;
                font-size: 14px;
                font-weight: 800;
                outline: none;
                transition: border-color .2s ease, box-shadow .2s ease;
            }

            .seat-field input:focus {
                border-color: var(--samu-blue);
                box-shadow: 0 0 0 4px rgba(2,99,160,.12);
            }

            .seat-field input[readonly] {
                background: #fef3c7;
                border-color: #facc15;
                color: #713f12;
                cursor: not-allowed;
            }

            .seat-modal-state {
                border-radius: 18px;
                padding: 12px 14px;
                background: #fee2e2;
                color: #991b1b;
                font-size: 13px;
                font-weight: 800;
            }

            .seat-modal-state.draft {
                background: #fef3c7;
                color: #713f12;
            }

            .seat-modal-submit {
                border: 0;
                border-radius: 18px;
                padding: 14px 16px;
                background: linear-gradient(135deg, #0263a0, #0f172a);
                color: #fff;
                font-size: 13px;
                font-weight: 900;
                box-shadow: 0 18px 36px rgba(2,99,160,.22);
            }

            .fade-up {
                animation: fadeUp .55s cubic-bezier(.16,.84,.24,1) both;
            }

            @keyframes fadeUp {
                from { opacity: 0; transform: translateY(18px); }
                to { opacity: 1; transform: translateY(0); }
            }

            @media (max-width: 1180px) {
                .action-topbar { grid-template-columns: 1fr 1fr; }
                .export-card { grid-column: 1 / -1; }
                .main-grid { grid-template-columns: 1fr; }
            }

            @media (max-width: 860px) {
                .command-shell { width: min(100% - 24px, 1480px); padding-top: 86px; }
                .dashboard-title { flex-direction: column; }
                .action-topbar,
                .analytics-grid,
                .stats-strip { grid-template-columns: 1fr; }
                .primary-action { min-height: 96px; }
                .chart-wrap {
                    width: 320px;
                    height: 320px;
                    flex-basis: 320px;
                }
                .chart-wrap canvas {
                    width: 320px !important;
                    height: 320px !important;
                }
                .calendar-grid {
                    min-height: 418px;
                    grid-template-rows: repeat(6, minmax(62px, 1fr));
                }
                .calendar-day { min-height: 62px; border-radius: 16px; padding: 7px; }
                .calendar-day .day-caption { display: none; }
                .card-head { align-items: flex-start; flex-direction: column; }
            }

            @media (max-width: 560px) {
                .hero-card,
                .command-card { border-radius: 22px; padding: 16px; }
                .range-row { flex-direction: column; align-items: stretch; }
                .export-btn { width: 100%; }
                .calendar-weekdays,
                .calendar-grid { gap: 5px; }
                .chart-wrap {
                    width: 260px;
                    height: 260px;
                    flex-basis: 260px;
                }
                .chart-wrap canvas {
                    width: 260px !important;
                    height: 260px !important;
                }
                .calendar-grid {
                    min-height: 318px;
                    grid-template-rows: repeat(6, minmax(48px, 1fr));
                }
                .calendar-day { min-height: 48px; border-radius: 13px; }
                .calendar-tooltip { display: none; }
                .dashboard-title h1 { letter-spacing: -1.2px; }
                .action-icon { width: 54px; height: 54px; }
                .primary-action strong { font-size: 15px; }
                .chart-center strong { font-size: 34px; }
            }
        </style>
    </head>
    <body>
        {{ menu_superior | safe }}

        <main class="command-shell">
            <section class="hero-card fade-up">
                <div class="dashboard-title">
                    <div>
                        <h1>Centro de Mando<br>Cuaderno de Obra</h1>
                        <p>Panel principal para redactar asientos, revisar estados del mes, atender observaciones de supervisión y exportar rangos del cuaderno.</p>
                    </div>
                    <span class="connection-pill {% if not conectado %}offline{% endif %}">
                        <i class="bi {% if conectado %}bi-database-check{% else %}bi-database-exclamation{% endif %}"></i>
                        {% if conectado %}PostgreSQL conectado{% else %}PostgreSQL pendiente{% endif %}
                    </span>
                </div>

                <div class="action-topbar">
                    <a class="primary-action residencia" href="/residencia" onclick="abrirModalAsientoResidencia(event)">
                        <span class="action-icon"><i class="bi bi-journal-richtext"></i></span>
                        <span>
                            <small>Permiso residencia</small>
                            <strong>REDACTAR ASIENTO DE RESIDENCIA</strong>
                        </span>
                    </a>
                    <a class="primary-action supervision" href="/supervision">
                        <span class="action-icon"><i class="bi bi-shield-check"></i></span>
                        <span>
                            <small>Permiso supervisión</small>
                            <strong>REDACTAR ASIENTO DE SUPERVISIÓN</strong>
                        </span>
                    </a>
                    <div class="export-card">
                        <div class="export-title"><i class="bi bi-cloud-arrow-down-fill text-danger"></i> Exportar Rango a PDF</div>
                        <div class="range-row">
                            <input type="date" id="exportDesde" aria-label="Desde">
                            <input type="date" id="exportHasta" aria-label="Hasta">
                            <button class="export-btn" type="button" onclick="exportarRangoPDF()">
                                <i class="bi bi-download me-1"></i>PDF
                            </button>
                        </div>
                    </div>
                </div>
            </section>

            <section class="stats-strip fade-up">
                <div class="mini-stat"><span>Total asientos</span><strong>{{ estadisticas.total_asientos }}</strong></div>
                <div class="mini-stat"><span>Último asiento</span><strong>{{ estadisticas.ultimo_asiento }}</strong></div>
                <div class="mini-stat"><span>Firmados</span><strong>{{ estadisticas.firmados }}</strong></div>
                <div class="mini-stat"><span>Observaciones</span><strong style="color:#dc2626;">{{ estadisticas.observaciones }}</strong></div>
            </section>

            <section class="main-grid">
                <div class="command-card fade-up">
                    <div class="card-head">
                        <h2><i class="bi bi-bar-chart-steps me-2"></i>Estadísticas y calendario mensual</h2>
                        <div class="month-controls">
                            <button type="button" onclick="cambiarMes(-1)" aria-label="Mes anterior"><i class="bi bi-chevron-left"></i></button>
                            <span id="monthLabel">Mes actual</span>
                            <button type="button" onclick="cambiarMes(1)" aria-label="Mes siguiente"><i class="bi bi-chevron-right"></i></button>
                        </div>
                    </div>

                    <div class="analytics-grid">
                        <div class="chart-card">
                            <div class="chart-wrap">
                                <canvas id="monthlyDoughnut"></canvas>
                                <div class="chart-center">
                                    <div>
                                        <strong id="monthPercent">0%</strong>
                                        <span>avance del mes</span>
                                    </div>
                                </div>
                            </div>
                            <div class="legend-dashboard">
                                <div><span><span class="dot" style="background:#22c55e;"></span> Cerrados</span><b id="closedCount">0</b></div>
                                <div><span><span class="dot" style="background:#facc15;"></span> Borradores</span><b id="draftCount">0</b></div>
                                <div><span><span class="dot" style="background:#ef4444;"></span> Sin registro</span><b id="pendingCount">0</b></div>
                            </div>
                        </div>

                        <div>
                            <div class="calendar-weekdays">
                                <span>Lun</span><span>Mar</span><span>Mié</span><span>Jue</span><span>Vie</span><span>Sáb</span><span>Dom</span>
                            </div>
                            <div class="calendar-grid" id="calendarGrid"></div>
                        </div>
                    </div>
                </div>

                <aside class="side-stack">
                    <div class="command-card alert-supervision fade-up">
                        <div class="card-head">
                            <h2><i class="bi bi-exclamation-triangle-fill me-2"></i>Observación crítica</h2>
                            <span class="connection-pill offline">Atención</span>
                        </div>
                        <div class="d-flex gap-3 align-items-start">
                            <div class="alert-icon"><i class="bi bi-stickies-fill"></i></div>
                            <div>
                                {% if ultima_observacion %}
                                    {% set obs = ultima_observacion %}
                                    <p class="alert-copy"><b>Asiento N° {{ obs.numero }}</b> · {{ obs.autor }}<br>{{ obs.texto }}</p>
                                {% else %}
                                    <p class="alert-copy"><b>Sin observaciones críticas activas.</b><br>Cuando supervisión registre un post-it pendiente, aparecerá aquí para residencia.</p>
                                {% endif %}
                            </div>
                        </div>
                    </div>

                    <div class="command-card fade-up">
                        <div class="card-head">
                            <h2><i class="bi bi-clock-history me-2"></i>Historial reciente</h2>
                            <span class="connection-pill">Últimas acciones</span>
                        </div>
                        <div class="timeline" id="recentTimeline"></div>
                    </div>
                </aside>
            </section>
        </main>

        <div id="seatEntryModal" class="seat-modal-overlay hidden" role="dialog" aria-modal="true" aria-labelledby="seatEntryTitle">
            <div class="seat-modal-card">
                <div class="seat-modal-head">
                    <div>
                        <h3 id="seatEntryTitle">Nuevo Asiento / Continuar</h3>
                        <p>Seleccione la fecha y confirme el número de asiento para ingresar al cuaderno.</p>
                    </div>
                    <button type="button" class="seat-modal-close" onclick="cerrarModalAsiento()" aria-label="Cerrar">&times;</button>
                </div>
                <div class="seat-modal-form">
                    <div class="seat-field">
                        <label for="seatModalDate">Fecha del asiento</label>
                        <input type="date" id="seatModalDate" onchange="evaluarFechaAsientoModal()">
                    </div>
                    <div class="seat-field">
                        <label for="seatModalNumber">Número de asiento</label>
                        <input type="text" id="seatModalNumber" placeholder="Ingrese el número de asiento">
                    </div>
                    <div id="seatModalState" class="seat-modal-state">
                        Día sin registro. Ingrese manualmente el número de asiento.
                    </div>
                    <button type="button" id="seatModalSubmit" class="seat-modal-submit" onclick="ingresarAlCuadernoResidencia()">
                        <i class="bi bi-journal-arrow-up me-1"></i> Ingresar al Cuaderno
                    </button>
                </div>
            </div>
        </div>

        <script>
            // Datos iniciales Jinja2. Luego se pueden reemplazar por Fetch/AJAX desde PostgreSQL.
            const dashboardSeed = {
                estadisticas: {
                    totalAsientos: Number({{ estadisticas.total_asientos | default(0) }}),
                    ultimoAsiento: {{ estadisticas.ultimo_asiento | tojson }},
                    firmados: Number({{ estadisticas.firmados | default(0) }}),
                    observaciones: Number({{ estadisticas.observaciones | default(0) }})
                },
                asientos: {{ asientos_json | safe }},
                observaciones: {{ observaciones_json | safe }},
                historial: {{ historial_json | safe }},
                mesActual: {{ mes_actual_json | safe }}
            };

            const estadoColor = {
                cerrado: '#22c55e',
                firmado: '#22c55e',
                borrador: '#facc15',
                pendiente: '#ef4444',
                observado: '#f97316'
            };

            let mesActivo = new Date();
            mesActivo.setDate(1);
            let doughnutChart = null;
            let asientosMesActivo = new Map();
            let asientoModalActual = null;

            function escapeHtml(valor) {
                return String(valor ?? '')
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;')
                    .replace(/"/g, '&quot;')
                    .replace(/'/g, '&#039;');
            }

            function normalizarEstado(valor) {
                const estado = String(valor || '').trim().toLowerCase();
                if (estado.includes('borrador') || estado.includes('redacción') || estado.includes('redaccion')) return 'borrador';
                if (estado.includes('observ')) return 'observado';
                if (estado.includes('cerrado') || estado.includes('firmado')) return 'cerrado';
                return 'pendiente';
            }

            function fechaAsiento(asiento, year, month) {
                if (asiento.fecha) {
                    const fecha = new Date(`${asiento.fecha}T00:00:00`);
                    if (!Number.isNaN(fecha.getTime())) return fecha;
                }
                return new Date(year, month, Number(asiento.dia || 1));
            }

            async function cargarDatosMes(year, month) {
                try {
                    const resp = await fetch(`/cuaderno/api/dashboard?year=${year}&month=${month + 1}`);
                    const data = await resp.json();
                    if (resp.ok && data.ok) return data;
                } catch (error) {
                    console.warn('No se pudo consultar el dashboard mensual. Usando datos iniciales.', error);
                }
                const asientos = dashboardSeed.asientos.filter(asiento => {
                    const fecha = fechaAsiento(asiento, year, month);
                    return fecha.getFullYear() === year && fecha.getMonth() === month;
                });
                return { asientos, observaciones: dashboardSeed.observaciones, estadisticas: null };
            }

            function diasEnMes(year, month) {
                return new Date(year, month + 1, 0).getDate();
            }

            function primerDiaLunes(year, month) {
                const day = new Date(year, month, 1).getDay();
                return day === 0 ? 6 : day - 1;
            }

            function nombreMes(fecha) {
                return fecha.toLocaleDateString('es-PE', { month: 'long', year: 'numeric' });
            }

            async function renderDashboardMes() {
                const year = mesActivo.getFullYear();
                const month = mesActivo.getMonth();
                const datos = await cargarDatosMes(year, month);
                const porDia = new Map();
                datos.asientos.forEach(asiento => {
                    const fecha = fechaAsiento(asiento, year, month);
                    porDia.set(fecha.getDate(), asiento);
                });
                asientosMesActivo = porDia;

                document.getElementById('monthLabel').textContent = nombreMes(mesActivo);

                const totalDias = datos.estadisticas?.dias_mes || diasEnMes(year, month);
                let cerrados = Number(datos.estadisticas?.cerrados || 0);
                let borradores = Number(datos.estadisticas?.borradores || 0);
                let sinRegistro = Number(datos.estadisticas?.sin_registro || 0);
                let avance = Number(datos.estadisticas?.avance || 0);
                if (!datos.estadisticas) {
                    let observados = 0;
                    for (const asiento of porDia.values()) {
                        const estado = normalizarEstado(asiento.estado);
                        if (estado === 'cerrado') cerrados += 1;
                        if (estado === 'borrador') borradores += 1;
                        if (estado === 'observado') observados += 1;
                    }
                    sinRegistro = Math.max(0, totalDias - cerrados - borradores - observados);
                    avance = Math.round((cerrados / totalDias) * 100);
                }

                renderChart(cerrados, borradores, sinRegistro, avance);
                renderCalendar(year, month, totalDias, porDia);
            }

            function renderChart(cerrados, borradores, sinRegistro, avance) {
                document.getElementById('monthPercent').textContent = `${avance}%`;
                document.getElementById('closedCount').textContent = cerrados;
                document.getElementById('draftCount').textContent = borradores;
                document.getElementById('pendingCount').textContent = sinRegistro;

                const ctx = document.getElementById('monthlyDoughnut');
                const data = [cerrados, borradores, sinRegistro];
                if (doughnutChart) {
                    doughnutChart.destroy();
                    doughnutChart = null;
                }
                doughnutChart = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Días con asientos cerrados', 'Días en borrador', 'Días sin registro'],
                        datasets: [{
                            data,
                            backgroundColor: ['#22c55e', '#facc15', '#ef4444'],
                            borderColor: '#ffffff',
                            borderWidth: 6,
                            hoverOffset: 8
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        cutout: '72%',
                        animation: {
                            animateRotate: true,
                            animateScale: false,
                            duration: 2000,
                            easing: 'easeOutQuart'
                        },
                        plugins: {
                            legend: { display: false },
                            tooltip: {
                                callbacks: {
                                    label: ctx => `${ctx.label}: ${ctx.raw} día(s)`
                                }
                            }
                        }
                    }
                });
            }

            function renderCalendar(year, month, totalDias, porDia) {
                const grid = document.getElementById('calendarGrid');
                grid.innerHTML = '';
                const espacios = primerDiaLunes(year, month);
                for (let i = 0; i < espacios; i += 1) {
                    const empty = document.createElement('div');
                    empty.className = 'calendar-day empty';
                    grid.appendChild(empty);
                }

                for (let dia = 1; dia <= totalDias; dia += 1) {
                    const asiento = porDia.get(dia);
                    const estado = asiento ? normalizarEstado(asiento.estado) : 'pendiente';
                    const item = document.createElement('button');
                    item.type = 'button';
                    item.className = `calendar-day ${estado}`;
                    item.innerHTML = `
                        <span class="day-number">${dia}</span>
                        <span class="day-caption">${textoEstado(asiento, estado)}</span>
                        <span class="calendar-tooltip">
                            ${asiento ? `
                                <b>Asiento N° ${escapeHtml(String(asiento.numero).padStart(3, '0'))}</b><br>
                                Estado: ${escapeHtml(asiento.estado || '-')}<br>
                                Avance: ${escapeHtml(asiento.avance || 0)}%<br>
                                Supervisor: ${escapeHtml(asiento.supervisor || '-')}<br>
                                ${escapeHtml(asiento.observacion || 'Sin observaciones activas.')}
                            ` : `
                                <b>Día ${dia}</b><br>
                                Sin asiento registrado para este día.
                            `}
                        </span>
                    `;
                    const fechaISO = fechaISODesdePartes(year, month, dia);
                    item.dataset.fecha = fechaISO;
                    if (asiento && asiento.numero && estado === 'borrador') {
                        item.addEventListener('click', () => abrirModalAsientoResidencia(null, fechaISO));
                    } else if (!asiento) {
                        item.addEventListener('click', () => abrirModalAsientoResidencia(null, fechaISO));
                    } else if (asiento && asiento.numero) {
                        item.addEventListener('click', () => irAAsiento(asiento.numero));
                    }
                    grid.appendChild(item);
                }
            }

            function fechaISODesdePartes(year, month, day) {
                return `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            }

            function fechaPorDefectoModal() {
                const hoy = new Date();
                const year = mesActivo.getFullYear();
                const month = mesActivo.getMonth();
                const dia = hoy.getFullYear() === year && hoy.getMonth() === month
                    ? hoy.getDate()
                    : 1;
                return fechaISODesdePartes(year, month, Math.min(dia, diasEnMes(year, month)));
            }

            function buscarAsientoPorFecha(fechaISO) {
                if (!fechaISO) return null;
                const fecha = new Date(`${fechaISO}T00:00:00`);
                if (Number.isNaN(fecha.getTime())) return null;
                if (fecha.getFullYear() !== mesActivo.getFullYear() || fecha.getMonth() !== mesActivo.getMonth()) return null;
                return asientosMesActivo.get(fecha.getDate()) || null;
            }

            function abrirModalAsientoResidencia(event, fechaISO=null) {
                if (event) event.preventDefault();
                const modal = document.getElementById('seatEntryModal');
                const fechaInput = document.getElementById('seatModalDate');
                const fechaBase = fechaISO || fechaPorDefectoModal();
                fechaInput.value = fechaBase;
                modal.classList.remove('hidden');
                evaluarFechaAsientoModal();
                setTimeout(() => fechaInput.focus(), 80);
            }

            function cerrarModalAsiento() {
                document.getElementById('seatEntryModal')?.classList.add('hidden');
            }

            function evaluarFechaAsientoModal() {
                const fechaInput = document.getElementById('seatModalDate');
                const numeroInput = document.getElementById('seatModalNumber');
                const estadoBox = document.getElementById('seatModalState');
                const boton = document.getElementById('seatModalSubmit');
                const fechaISO = fechaInput.value;
                const asiento = buscarAsientoPorFecha(fechaISO);
                asientoModalActual = asiento || null;

                if (asiento && normalizarEstado(asiento.estado) === 'borrador') {
                    numeroInput.value = `Continuando Asiento N° ${String(asiento.numero).padStart(3, '0')}`;
                    numeroInput.dataset.numero = asiento.numero;
                    numeroInput.readOnly = true;
                    estadoBox.classList.add('draft');
                    estadoBox.innerHTML = '<i class="bi bi-pencil-square me-1"></i> Día amarillo: existe un borrador. Continuará el asiento registrado.';
                    boton.innerHTML = '<i class="bi bi-journal-arrow-up me-1"></i> Continuar Borrador';
                    return;
                }

                numeroInput.value = '';
                numeroInput.dataset.numero = '';
                numeroInput.readOnly = false;
                estadoBox.classList.remove('draft');
                if (asiento) {
                    numeroInput.value = `Asiento cerrado N° ${String(asiento.numero).padStart(3, '0')}`;
                    numeroInput.dataset.numero = asiento.numero;
                    numeroInput.readOnly = true;
                    estadoBox.innerHTML = '<i class="bi bi-lock-fill me-1"></i> Esta fecha ya tiene un asiento cerrado. Puede revisarlo desde el calendario.';
                    boton.innerHTML = '<i class="bi bi-eye-fill me-1"></i> Ver Asiento';
                } else {
                    estadoBox.innerHTML = '<i class="bi bi-plus-circle-fill me-1"></i> Día rojo: sin registro. Ingrese manualmente el número de asiento.';
                    boton.innerHTML = '<i class="bi bi-journal-arrow-up me-1"></i> Ingresar al Cuaderno';
                }
            }

            function ingresarAlCuadernoResidencia() {
                const fecha = document.getElementById('seatModalDate').value;
                const numeroInput = document.getElementById('seatModalNumber');
                const asientoExistente = asientoModalActual;
                if (asientoExistente && normalizarEstado(asientoExistente.estado) === 'cerrado') {
                    irAAsiento(asientoExistente.numero);
                    return;
                }
                const numero = asientoExistente && normalizarEstado(asientoExistente.estado) === 'borrador'
                    ? asientoExistente.numero
                    : String(numeroInput.value || '').trim();
                if (!fecha || !numero || String(numero).includes('Continuando')) {
                    alert('Seleccione la fecha e ingrese un número de asiento válido.');
                    return;
                }
                const params = new URLSearchParams({
                    fecha,
                    asiento: numero,
                    modo: asientoExistente ? 'continuar' : 'nuevo'
                });
                window.location.href = `/residencia?${params.toString()}`;
            }

            function textoEstado(asiento, estado) {
                if (!asiento) return 'Sin registro';
                if (estado === 'cerrado') return 'Cerrado';
                if (estado === 'borrador') return 'Borrador';
                if (estado === 'observado') return 'Observado';
                return 'Pendiente';
            }

            function cambiarMes(delta) {
                mesActivo.setMonth(mesActivo.getMonth() + delta);
                renderDashboardMes();
            }

            function irAAsiento(numero) {
                window.location.href = `/cuaderno/asiento/${numero}`;
            }

            function renderTimeline() {
                const timeline = document.getElementById('recentTimeline');
                const acciones = [];
                dashboardSeed.historial.slice(0, 5).forEach(log => {
                    acciones.push({
                        hora: log.created_at ? new Date(log.created_at) : new Date(),
                        titulo: `${log.usuario || 'Sistema'} ${log.accion || 'registró actividad'}${log.numero ? ` el Asiento N° ${String(log.numero).padStart(3, '0')}` : ''}`,
                        detalle: log.detalle || 'Movimiento registrado en el cuaderno de obra.'
                    });
                });
                if (acciones.length > 0) {
                    acciones.sort((a, b) => b.hora - a.hora);
                    timeline.innerHTML = acciones.slice(0, 5).map((accion, idx) => `
                        <div class="timeline-item">
                            <span class="timeline-dot" style="background:${idx === 0 ? '#ef4444' : '#0263a0'};"></span>
                            <div class="timeline-box">
                                <strong>${escapeHtml(formatoRelativo(accion.hora))} - ${escapeHtml(accion.titulo)}</strong>
                                <span>${escapeHtml(accion.detalle)}</span>
                            </div>
                        </div>
                    `).join('');
                    return;
                }
                dashboardSeed.asientos.slice(0, 5).forEach(asiento => {
                    const actor = normalizarEstado(asiento.estado) === 'borrador' ? 'Supervisión guardó' : 'Residencia cerró';
                    acciones.push({
                        hora: asiento.updated_at ? new Date(asiento.updated_at) : (asiento.fecha ? new Date(`${asiento.fecha}T18:30:00`) : new Date()),
                        titulo: `${actor} el Asiento N° ${String(asiento.numero || '').padStart(3, '0')}`,
                        detalle: `Estado actual: ${asiento.estado || '-'} · Avance ${asiento.avance || 0}%`
                    });
                });
                dashboardSeed.observaciones.slice(0, 2).forEach(obs => {
                    acciones.push({
                        hora: obs.created_at ? new Date(obs.created_at) : new Date(),
                        titulo: `Supervisión observó el Asiento N° ${String(obs.numero || '').padStart(3, '0')}`,
                        detalle: obs.texto || 'Observación pendiente de atención.'
                    });
                });
                acciones.sort((a, b) => b.hora - a.hora);

                if (acciones.length === 0) {
                    timeline.innerHTML = '<div class="empty-box">Aún no hay acciones registradas. El historial se llenará al guardar borradores, cerrar asientos o registrar observaciones.</div>';
                    return;
                }

                timeline.innerHTML = acciones.slice(0, 5).map((accion, idx) => `
                    <div class="timeline-item">
                        <span class="timeline-dot" style="background:${idx === 0 ? '#ef4444' : '#0263a0'};"></span>
                        <div class="timeline-box">
                            <strong>${escapeHtml(formatoRelativo(accion.hora))} - ${escapeHtml(accion.titulo)}</strong>
                            <span>${escapeHtml(accion.detalle)}</span>
                        </div>
                    </div>
                `).join('');
            }

            function formatoRelativo(fecha) {
                if (!(fecha instanceof Date) || Number.isNaN(fecha.getTime())) return 'Reciente';
                const hoy = new Date();
                const ayer = new Date();
                ayer.setDate(hoy.getDate() - 1);
                const hora = fecha.toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' });
                if (fecha.toDateString() === hoy.toDateString()) return `Hoy ${hora}`;
                if (fecha.toDateString() === ayer.toDateString()) return `Ayer ${hora}`;
                return `${fecha.toLocaleDateString('es-PE', { day: '2-digit', month: 'short' })} ${hora}`;
            }

            function exportarRangoPDF() {
                const desde = document.getElementById('exportDesde').value;
                const hasta = document.getElementById('exportHasta').value;
                if (!desde || !hasta) {
                    alert('Seleccione fecha Desde y Hasta para exportar el rango.');
                    return;
                }
                // Endpoint sugerido para conectar luego:
                // window.location.href = `/cuaderno/export/pdf?desde=${desde}&hasta=${hasta}`;
                alert(`Exportación preparada: ${desde} al ${hasta}. Falta conectar el endpoint PDF real.`);
            }

            document.addEventListener('DOMContentLoaded', () => {
                renderDashboardMes();
                renderTimeline();
                document.getElementById('seatEntryModal')?.addEventListener('click', event => {
                    if (event.target.id === 'seatEntryModal') cerrarModalAsiento();
                });
                document.addEventListener('keydown', event => {
                    if (event.key === 'Escape') cerrarModalAsiento();
                });
            });
        </script>
    </body>
    </html>
    """, estadisticas=estadisticas, asientos=asientos, observaciones=observaciones, ultima_observacion=ultima_observacion, conectado=conectado, rol_usuario=rol_usuario, menu_superior=menu_superior, asientos_json=asientos_json, observaciones_json=observaciones_json, historial_json=historial_json, mes_actual_json=mes_actual_json)
