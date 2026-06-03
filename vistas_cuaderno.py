# =========================================================
# vistas_cuaderno.py
# Módulo: Cuaderno de Obra Digital - Lobby Central (Responsivo)
# =========================================================

import json

from flask import Blueprint, render_template_string, session, redirect, url_for, request, jsonify
from navbar import obtener_navbar
from cuaderno_store import anular_firma_asiento, obtener_inspector_asiento, obtener_panel_cuaderno, obtener_asiento, obtener_asiento_por_fecha, obtener_datos_mes_cuaderno

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


@cuaderno_bp.route('/cuaderno/asiento/<int:numero>/anular_firma', methods=['POST'])
def api_anular_firma_asiento(numero):
    if 'usuario_id' not in session:
        return jsonify({"ok": False, "error": "No autorizado"}), 401
    if not (session.get('es_admin') or session.get('rol') == 'Admin'):
        return jsonify({"ok": False, "error": "Solo Dueño/Admin puede anular firma."}), 403
    resultado = anular_firma_asiento(numero, session.get('nombre_usuario') or session.get('nombre') or 'Admin')
    return jsonify(resultado), 200 if resultado.get("ok") else 500


@cuaderno_bp.route('/cuaderno/asiento/<int:numero>/completo')
def ver_asiento_completo(numero):
    if 'usuario_id' not in session:
        return redirect(url_for('login.mostrar_login'))
    asiento = obtener_asiento(numero)
    if not asiento:
        return redirect(url_for('cuaderno.panel_cuaderno'))
    inspector = obtener_inspector_asiento(numero=numero, fecha=asiento.get("fecha"))
    try:
        contenido = json.loads(asiento.get("contenido") or "{}")
    except Exception:
        contenido = {}
    residencia_html = contenido.get("texto_html") or "<div class='text-slate-500'>Sin contenido de Residencia.</div>"
    inspector_texto = ""
    if inspector:
        inspector_texto = "\n\n".join([
            "1. Personal de Supervisión: " + ", ".join(f"(1) {x}" for x in inspector.get("personal_supervision") or []),
            "2. Partidas Ejecutadas:\n" + (inspector.get("partidas_ejecutadas") or "-"),
            "3. Movimiento de Almacén:\nINGRESO: " + (inspector.get("almacen_ingreso") or "-") + "\nSALIDA: " + (inspector.get("almacen_salida") or "-"),
            "4. Maquinaria y/o Equipos:\n" + (inspector.get("maquinaria") or "-"),
            "5. Ocurrencias y/o Obs:\n" + (inspector.get("ocurrencias") or "-"),
        ])
    else:
        inspector_texto = "Inspector/Supervisión aún no registró asiento para esta fecha."
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Asiento completo</title>
        <script>window.tailwind = window.tailwind || {}; window.tailwind.config = { corePlugins: { preflight: false } };</script>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-100 text-slate-900">
        {{ menu_superior | safe }}
        <main class="mx-auto max-w-6xl px-4 py-24">
            <div class="mb-5 flex flex-wrap items-center justify-between gap-3">
                <div>
                    <h1 class="m-0 text-3xl font-black">Hoja completa del Asiento N° {{ numero }}</h1>
                    <p class="m-0 mt-1 text-sm font-bold text-slate-500">Residencia + Supervisión/Inspector en una sola vista</p>
                </div>
                <a href="/cuaderno" class="rounded-full bg-slate-900 px-4 py-3 text-sm font-black text-white no-underline">Volver</a>
            </div>
            <section class="grid gap-4 lg:grid-cols-2">
                <article class="rounded-3xl bg-white p-5 shadow-xl">
                    <h2 class="text-xl font-black text-blue-700">Residencia</h2>
                    <div class="mt-3 overflow-auto">{{ residencia_html | safe }}</div>
                </article>
                <article class="rounded-3xl bg-white p-5 shadow-xl">
                    <h2 class="text-xl font-black text-emerald-700">Supervisión / Inspector</h2>
                    <pre class="mt-3 whitespace-pre-wrap font-[Candara] text-[17px] italic leading-7 text-sky-700">{{ inspector_texto }}</pre>
                </article>
            </section>
        </main>
    </body>
    </html>
    """, menu_superior=obtener_navbar(session.get('rol') == 'Admin', session.get('nombre', 'Visitante')), numero=numero, residencia_html=residencia_html, inspector_texto=inspector_texto)


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
    estado_actual = str(asiento.get("estado") or "").lower()
    editable_resumen = (request.args.get("editar") == "1" or request.path.startswith("/resumen_asiento/")) and estado_actual in ("borrador", "enviado inspector")
    puede_anular_firma = bool(session.get("es_admin") or session.get("rol") == "Admin") and (estado_actual in ("cerrado", "firmado") or asiento.get("bloqueado"))

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Asiento {{ asiento.numero }} — Cuaderno de Obra</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <script>
            window.tailwind = window.tailwind || {};
            window.tailwind.config = { corePlugins: { preflight: false } };
        </script>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body { margin: 0; min-height: 100vh; font-family: Inter, Arial, sans-serif; background: linear-gradient(135deg,#f8fafc,#eff6ff); color: #0f172a; }
            .asiento-view { max-width: 980px; margin: 0 auto; padding: 96px 18px 42px; }
            .asiento-head { display: flex; justify-content: space-between; gap: 12px; align-items: center; flex-wrap: wrap; margin-bottom: 18px; }
            .asiento-head h1 { margin: 0; font-size: 28px; font-weight: 900; letter-spacing: -.8px; }
            .asiento-actions { display: flex; gap: 8px; flex-wrap: wrap; }
            .asiento-btn { border: 0; border-radius: 999px; padding: 10px 14px; font-size: 12px; font-weight: 900; text-decoration: none; color: #fff; background: #0f172a; }
            .asiento-btn.pdf { background: linear-gradient(135deg,#991b1b,#ef4444); }
            .asiento-paper { background: #fff; border-radius: 28px; padding: 20px; box-shadow: 0 24px 60px rgba(15,23,42,.12); overflow-x: auto; }
            .papel-fisico { position: relative; width: 100%; height: 1123px; min-height: 1123px; max-height: 1123px; padding: 30px 46px 34px; box-sizing: border-box; display: flex; flex-direction: column; overflow: hidden; background: #fdfdfa; border: 1px solid #e2e8f0; box-shadow: 0 18px 45px rgba(15,23,42,0.10); font-family: Arial, sans-serif; color: #000; }
            .pagina-cuaderno { background-image: repeating-linear-gradient(to bottom, transparent 0, transparent 25px, #cbd5e1 25px, #cbd5e1 26px); background-size: 100% 26px; background-position: top left; line-height: 26px; height: 780px; min-height: 780px; max-height: 780px; padding-top: 0; position: relative; overflow: hidden; display: flex; flex-direction: column; }
            .lapicero { flex: 1 1 auto; min-height: 0; overflow: hidden; display: flex; flex-direction: column; font-family: Candara, Calibri, Arial, sans-serif; font-style: italic; color: #0263a0; font-size: 17px; line-height: 26px; padding-left: 2px; font-weight: 400; text-align: justify; word-wrap: break-word; overflow-wrap: anywhere; word-break: break-word; }
            .encabezado-asiento { position: relative; margin: 0 0 3px; min-height: 26px; font-weight: 700; }
            .titulo-asiento { width: 100%; text-align: center; text-transform: uppercase; font-weight: 800; padding: 0 128px 0 8px; white-space: nowrap; }
            .fecha-asiento { position: absolute; top: 0; right: 0; text-align: right; white-space: nowrap; }
            .encabezado-asiento.continuacion .titulo-asiento { padding: 0 128px 0 8px; text-align: center; text-transform: none; }
            .modulo-titulo { display: block; font-weight: 700; color: #075985; }
            .modulo-contenido { display: block; padding-left: 22px; white-space: pre-wrap; overflow-wrap: anywhere; word-break: break-word; }
            .personal-bloque { display: block; padding-left: 22px; }
            .personal-subtitulo { display: block; padding-left: 18px; font-weight: 700; line-height: 26px; }
            .personal-gastos-linea { display: block; padding-left: 48px; line-height: 26px; text-align: justify; }
            .personal-costo-fila { display: block; padding-left: 0; line-height: 26px; text-align: center; white-space: pre-wrap; }
            .van-final { margin-top: auto; display: block; text-align: right; padding-right: 8px; font-weight: 800; color: #075985; }
            .page-counter { position: absolute; right: 14mm; bottom: 5mm; font-size: 9px; font-weight: 600; color: #94a3b8; }
            .p-header-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 4px; }
            .p-header-side { width: 86px; flex: 0 0 86px; }
            .p-qr-link { width: 62px; display: block; margin-left: auto; text-decoration: none; }
            .p-qr-link img { width: 62px; height: 62px; display: block; object-fit: contain; border: 0; border-radius: 0; padding: 0; background: transparent; }
            .p-title-box { text-align: center; flex: 1; margin-left: 0; }
            .p-title-box h1 { font-size: 28px; font-weight: bold; text-decoration: underline; letter-spacing: 1.5px; margin: 0; }
            .p-num { font-size: 24px; font-weight: bold; }
            .p-meta { margin-bottom: 3px; padding-bottom: 4px; border-bottom: 3px solid #000; }
            .p-meta-row { display: flex; align-items: flex-end; gap: 15px; width: 100%; margin-bottom: 2px; }
            .p-meta-field { display: flex; align-items: flex-end; min-width: 0; }
            .p-meta-field.fecha { flex: 0 0 46%; }
            .p-meta-field.modalidad { flex: 1 1 auto; }
            .p-row { display: flex; align-items: flex-end; margin-bottom: 2px; }
            .p-label { font-size: 14px; font-weight: bold; margin-right: 8px; }
            .p-line { flex: 1; border-bottom: 1px solid #000; position: relative; height: 17px; }
            .lapicero-meta { position: absolute; bottom: -1px; left: 10px; font-family: Candara, Calibri, Arial, sans-serif; font-style: italic; color: #0263a0; font-size: 16px; font-weight: 500; white-space: nowrap; }
            .p-footer { display: flex; justify-content: space-between; margin-top: auto; padding-top: 18px; padding-bottom: 8px; font-size: 12px; font-weight: bold; color: #000; }
            .p-sig { border-top: 1px solid #000; width: 28%; text-align: center; padding-top: 5px; }
            .modulo-editable { position: relative; border-radius: 14px; padding-right: 42px; }
            .edit-module-btn { position: absolute; top: 0; right: 4px; width: 30px; height: 30px; border: 0; border-radius: 999px; background: #2563eb; color: #fff; display: grid; place-items: center; box-shadow: 0 10px 22px rgba(37,99,235,.22); }
            .edit-module-btn:hover { transform: scale(1.06); }
            @media print {
                body { background: #fff; }
                body * { visibility: hidden !important; }
                #asientoPaper, #asientoPaper * { visibility: visible !important; }
                @page { size: A4; margin: 0; }
                #asientoPaper { position: absolute; left: 0; top: 0; width: 210mm; box-shadow: none; border-radius: 0; padding: 0; background: #fff; }
                #asientoPaper .papel-fisico { position: relative; width: 210mm !important; height: 297mm !important; min-height: 297mm !important; max-height: 297mm !important; box-sizing: border-box !important; padding: 8mm 12mm 9mm !important; margin: 0 !important; box-shadow: none !important; border: none !important; page-break-after: always; break-after: page; display: flex; flex-direction: column; overflow: hidden; background: #fdfdfa !important; }
                #asientoPaper .papel-fisico:last-child { page-break-after: auto; break-after: auto; }
                #asientoPaper .p-header-top { flex: 0 0 auto; margin-bottom: 2mm !important; }
                #asientoPaper .p-meta { flex: 0 0 auto; margin-bottom: 1mm !important; padding-bottom: 1mm !important; }
                #asientoPaper .p-body-lines { flex: 0 0 780px !important; min-height: 780px !important; max-height: 780px !important; margin-top: 1px !important; margin-bottom: 2mm !important; overflow: hidden; display: flex; flex-direction: column; }
                #asientoPaper .pagina-cuaderno { flex: 0 0 780px !important; height: 780px !important; min-height: 780px !important; max-height: 780px !important; overflow: hidden; background-size: 100% 26px !important; background-position: top left !important; background-image: repeating-linear-gradient(to bottom, transparent 0, transparent 25px, #cbd5e1 25px, #cbd5e1 26px) !important; display: flex; flex-direction: column; }
                #asientoPaper .lapicero { flex: 1 1 auto; min-height: 0; overflow: hidden; display: flex; flex-direction: column; font-size: 17px; line-height: 26px; overflow-wrap: anywhere; word-break: break-word; }
                #asientoPaper .modulo-contenido, #asientoPaper .almacen-detalle, #asientoPaper .maquinaria-bloque { overflow-wrap: anywhere !important; word-break: break-word !important; }
                #asientoPaper .van-final { margin-top: auto !important; text-align: right !important; padding-right: 8px !important; }
                #asientoPaper .encabezado-asiento.continuacion .titulo-asiento { padding: 0 128px 0 8px !important; text-align: center !important; text-transform: none !important; }
                #asientoPaper .encabezado-asiento.continuacion .fecha-asiento { display: block !important; }
                #asientoPaper .p-footer { flex: 0 0 auto; margin-top: auto !important; padding-top: 5mm !important; padding-bottom: 2mm !important; page-break-inside: avoid; break-inside: avoid; }
                #asientoPaper .p-sig { page-break-inside: avoid; break-inside: avoid; }
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
                    {% if editable_resumen %}
                    <div class="relative inline-block text-left">
                        <button type="button" class="asiento-btn bg-blue-600" onclick="toggleMenuEditarModulos()">
                            <i class="bi bi-pencil-square"></i> Editar Módulos
                        </button>
                        <div id="menuEditarModulos" class="hidden absolute right-0 z-50 mt-2 w-64 origin-top-right rounded-2xl bg-white p-2 shadow-2xl ring-1 ring-slate-200">
                            {% for i in range(1, 11) %}
                            <button type="button" class="w-full rounded-xl px-3 py-2 text-left text-sm font-black text-slate-700 transition hover:bg-blue-50 hover:text-blue-700" onclick="editarModuloResumen({{ i }})">
                                Módulo {{ i }}
                            </button>
                            {% endfor %}
                        </div>
                    </div>
                    {% endif %}
                    {% if puede_anular_firma %}
                    <button class="asiento-btn bg-red-700" onclick="anularFirmaAsiento()"><i class="bi bi-unlock-fill"></i> Anular Firma / Desbloquear</button>
                    {% endif %}
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
            const resumenEditable = {{ editable_resumen | tojson }};
            const puedeAnularFirma = {{ puede_anular_firma | tojson }};
            const asientoFechaRaw = {{ asiento.fecha | tojson }};
            const asientoHtmlNormal = document.getElementById('asientoPaper')?.innerHTML || '';

            function esc(v) {
                return String(v || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
            }

            function htmlModuloVista(modulo) {
                const tituloHtml = modulo.continuacionModulo ? '' : `<span class="modulo-titulo">${esc(modulo.titulo)}</span>`;
                if (String(modulo.titulo || '').startsWith('2.')) {
                    return `<div class="modulo-redaccion">${tituloHtml}<div class="personal-bloque">${htmlPersonalObraVista(modulo.contenido)}</div></div>`;
                }
                return `<div class="modulo-redaccion">${tituloHtml}<span class="modulo-contenido">${esc(modulo.contenido || '-').replace(/\\n/g, '<br>')}</span></div>`;
            }

            function htmlPersonalObraVista(texto) {
                let enCosto = false;
                return String(texto || '-').split('\\n').map(linea => {
                    const limpia = String(linea || '').trim();
                    if (!limpia) return '';
                    if (limpia.startsWith('*')) {
                        enCosto = /costo\\s+directo/i.test(limpia);
                        return `<div class="personal-subtitulo">${esc(limpia)}</div>`;
                    }
                    if (enCosto && limpia !== '-') return `<div class="personal-costo-fila">${esc(limpia)}</div>`;
                    return `<div class="personal-gastos-linea">${esc(limpia)}</div>`;
                }).filter(Boolean).join('');
            }

            function numeroModuloDesdeTitulo(titulo) {
                const match = String(titulo || '').match(/^(\\d+)/);
                return match ? Number(match[1]) : 1;
            }

            function htmlModuloEditable(modulo) {
                const step = numeroModuloDesdeTitulo(modulo.titulo);
                const contenido = String(modulo.titulo || '').startsWith('2.')
                    ? `<div class="personal-bloque">${htmlPersonalObraVista(modulo.contenido)}</div>`
                    : `<span class="modulo-contenido">${esc(modulo.contenido || '-').replace(/\\n/g, '<br>')}</span>`;
                const tituloHtml = modulo.continuacionModulo ? '' : `<span class="modulo-titulo">${esc(modulo.titulo)}</span>`;
                return `<div class="modulo-redaccion modulo-editable">
                    <button type="button" class="edit-module-btn" title="Editar módulo ${step}" onclick="editarModuloResumen(${step})"><i class="bi bi-pencil-fill"></i></button>
                    ${tituloHtml}
                    ${contenido}
                </div>`;
            }

            function editarModuloResumen(step) {
                const params = new URLSearchParams({
                    fecha: asientoFechaRaw,
                    asiento: String(Number(asientoNumero)),
                    modo: 'continuar',
                    modulo: String(step),
                    paso: String(step),
                    volver: `/resumen_asiento/${encodeURIComponent(asientoFechaRaw)}`
                });
                window.location.href = `/residencia?${params.toString()}`;
            }

            function toggleMenuEditarModulos() {
                document.getElementById('menuEditarModulos')?.classList.toggle('hidden');
            }

            function mostrarMensajeResumen(mensaje, error=false) {
                let box = document.getElementById('resumenMensajeFlotante');
                if (!box) {
                    box = document.createElement('div');
                    box.id = 'resumenMensajeFlotante';
                    box.className = 'fixed right-5 top-24 z-[3000] rounded-2xl px-4 py-3 text-sm font-black text-white shadow-2xl transition';
                    document.body.appendChild(box);
                }
                box.classList.toggle('bg-red-600', error);
                box.classList.toggle('bg-green-600', !error);
                box.textContent = mensaje;
                box.style.opacity = '1';
                setTimeout(() => { box.style.opacity = '0'; }, 2600);
            }

            async function anularFirmaAsiento() {
                if (!puedeAnularFirma) return;
                const resp = await fetch(`/cuaderno/asiento/${Number(asientoNumero)}/anular_firma`, { method: 'POST' });
                const data = await resp.json().catch(() => ({ ok: false, error: 'Respuesta inválida' }));
                if (!resp.ok || !data.ok) {
                    mostrarMensajeResumen(data.error || 'No se pudo anular la firma.', true);
                    return;
                }
                mostrarMensajeResumen('Firma anulada. El asiento vuelve a estar editable.');
                window.location.href = `/resumen_asiento/${encodeURIComponent(asientoFechaRaw)}`;
            }

            function activarEdicionModularResumen() {
                if (!resumenEditable || !Array.isArray(asientoModulos) || asientoModulos.length === 0) return;
                renderAsientoPaginado(true);
            }

            const PDF_LINE_HEIGHT_PX = 26;

            function obtenerMedidorVistaPDF() {
                let medidor = document.getElementById('__samuVistaPdfMeasure');
                if (!medidor) {
                    medidor = document.createElement('div');
                    medidor.id = '__samuVistaPdfMeasure';
                    medidor.style.cssText = [
                        'position:absolute',
                        'left:-99999px',
                        'top:0',
                        'visibility:hidden',
                        'pointer-events:none',
                        'width:650px',
                        'font-family:Candara, Calibri, Arial, sans-serif',
                        'font-style:italic',
                        'font-size:17px',
                        'line-height:26px',
                        'font-weight:400',
                        'text-align:justify',
                        'color:#0263a0',
                        'word-wrap:break-word'
                    ].join(';');
                    document.body.appendChild(medidor);
                }
                return medidor;
            }

            function anchoLineaCuadernoVista() {
                const hoja = document.querySelector('#asientoPaper .pagina-cuaderno') || document.querySelector('.pagina-cuaderno');
                const ancho = hoja?.clientWidth || 836;
                return Math.max(760, Math.floor(ancho - 28));
            }

            function contextoLineasCuadernoVista() {
                if (!window.__samuVistaLineMeasureCanvas) {
                    window.__samuVistaLineMeasureCanvas = document.createElement('canvas');
                }
                const ctx = window.__samuVistaLineMeasureCanvas.getContext('2d');
                ctx.font = 'italic 17px Candara, Calibri, Arial, sans-serif';
                return ctx;
            }

            function contarLineasTextoVista(texto) {
                const ctx = contextoLineasCuadernoVista();
                const anchoMaximo = anchoLineaCuadernoVista();
                const parrafos = String(texto || '-').split('\\n');
                let total = 0;

                parrafos.forEach(parrafo => {
                    const limpio = String(parrafo || '').trim();
                    if (!limpio) {
                        total += 1;
                        return;
                    }

                    let lineaActual = '';
                    limpio.split(/\\s+/).filter(Boolean).forEach(palabra => {
                        const candidata = lineaActual ? `${lineaActual} ${palabra}` : palabra;
                        if (lineaActual && ctx.measureText(candidata).width > anchoMaximo) {
                            total += 1;
                            lineaActual = palabra;
                        } else {
                            lineaActual = candidata;
                        }
                    });
                    total += 1;
                });

                return Math.max(1, total);
            }

            function lineasModuloVista(modulo, incluirVan=false) {
                const titulo = modulo.continuacionModulo ? 0 : 1;
                const html = htmlModuloVista(modulo);
                const bloques = Math.max(0, (html.match(/<div\b/gi) || []).length - 1);
                const saltos = (html.match(/<br\s*\/?\s*>/gi) || []).length;
                const estimadoHtml = bloques + saltos;
                return Math.max(1, titulo + Math.max(contarLineasTextoVista(modulo.contenido || '-'), estimadoHtml) + (incluirVan ? 1 : 0));
            }

            function htmlPaginaVistaTemporal(modulos, continuacion=false, van=false) {
                return `
                    <div class="pagina-cuaderno" style="height:auto;min-height:0;max-height:none;overflow:visible;background:none;display:block;">
                        <div class="lapicero" style="display:block;min-height:0;overflow:visible;">
                            ${encabezadoVista(continuacion)}
                            ${modulos.map(htmlModuloVista).join('')}
                            ${van ? '<span class="van-final">van . . .</span>' : ''}
                        </div>
                    </div>
                `;
            }

            function medirPaginaVista(modulos, continuacion=false, van=false) {
                const medidor = obtenerMedidorVistaPDF();
                medidor.style.width = '650px';
                medidor.innerHTML = htmlPaginaVistaTemporal(modulos, continuacion, van);
                const contenido = medidor.querySelector('.lapicero');
                return contenido ? contenido.scrollHeight : (medidor.scrollHeight || 0);
            }

            function estimarLineasTextoVista(texto) {
                return contarLineasTextoVista(texto);
            }

            function dividirModuloVista(modulo, maxLineas) {
                const texto = String(modulo.contenido || '-').trim();
                const lineasDisponibles = Math.max(1, maxLineas);
                const partes = texto.split(/\\s+/).filter(Boolean);
                if (partes.length <= 1) return [{...modulo, contenido: texto || '-'}, {...modulo, contenido: ''}];

                let bajo = 1;
                let alto = partes.length;
                let mejor = 0;
                while (bajo <= alto) {
                    const medio = Math.floor((bajo + alto) / 2);
                    const candidato = partes.slice(0, medio).join(' ').trim();
                    if (lineasModuloVista({...modulo, contenido: candidato}, false) <= lineasDisponibles) {
                        mejor = medio;
                        bajo = medio + 1;
                    } else {
                        alto = medio - 1;
                    }
                }
                if (mejor <= 0) {
                    return [
                        {...modulo, contenido: '', continuacionModulo: modulo.continuacionModulo},
                        {...modulo, contenido: texto || '-', continuacionModulo: true}
                    ];
                }
                if (mejor >= partes.length) mejor = Math.max(1, partes.length - 1);
                return [
                    {...modulo, contenido: partes.slice(0, mejor).join(' ').trim() || '-'},
                    {...modulo, contenido: partes.slice(mejor).join(' ').trim(), continuacionModulo: true}
                ];
            }

            function dividirModuloVistaPorAltura(modulo, modulosPrevios, continuacion, maxAltura) {
                const texto = String(modulo.contenido || '-').trim();
                const partes = texto.split(/\s+/).filter(Boolean);
                if (partes.length <= 1) return [{...modulo, contenido: texto || '-'}, {...modulo, contenido: ''}];

                let bajo = 1;
                let alto = partes.length;
                let mejor = 0;
                while (bajo <= alto) {
                    const medio = Math.floor((bajo + alto) / 2);
                    const candidato = {...modulo, contenido: partes.slice(0, medio).join(' ').trim()};
                    const altura = medirPaginaVista([...modulosPrevios, candidato], continuacion, false);
                    if (altura <= maxAltura) {
                        mejor = medio;
                        bajo = medio + 1;
                    } else {
                        alto = medio - 1;
                    }
                }
                if (mejor >= partes.length) mejor = Math.max(1, partes.length - 1);
                return [
                    {...modulo, contenido: partes.slice(0, mejor).join(' ').trim()},
                    {...modulo, contenido: partes.slice(mejor).join(' ').trim(), continuacionModulo: true}
                ];
            }

            function paginarVista(modulos) {
                const paginas = [];
                let actual = [];
                let usadas = 1;
                let continuacion = false;
                const maxLineasContenido = () => 29;
                const maxAlturaContenido = () => PDF_LINE_HEIGHT_PX * maxLineasContenido();
                modulos.forEach(original => {
                    let pendiente = {...original};
                    while (pendiente && String(pendiente.contenido || '').trim()) {
                        const lineasPendiente = lineasModuloVista(pendiente);
                        const lineasDisponibles = maxLineasContenido() - usadas;

                        if (lineasPendiente <= lineasDisponibles) {
                            actual.push(pendiente);
                            usadas += lineasPendiente;
                            pendiente = null;
                            continue;
                        }

                        if (lineasDisponibles >= 1) {
                            const partes = dividirModuloVista(pendiente, lineasDisponibles);
                            const resto = String(partes[1].contenido || '').trim();
                            if (String(partes[0].contenido || '').trim()) {
                                actual.push(partes[0]);
                            }
                            if (resto) {
                                paginas.push({modulos: actual, continuacion, van: true});
                                actual = [];
                                usadas = 1;
                                continuacion = true;
                                pendiente = {...partes[1], contenido: resto};
                            } else {
                                pendiente = null;
                            }
                            continue;
                        }

                        if (actual.length > 0) {
                            paginas.push({modulos: actual, continuacion, van: true});
                            actual = [];
                            usadas = 1;
                            continuacion = true;
                            continue;
                        }

                        const forzado = dividirModuloVista(pendiente, Math.max(2, maxLineasContenido() - usadas));
                        const restoForzado = String(forzado[1].contenido || '').trim();
                        actual.push(forzado[0]);
                        if (restoForzado) {
                            paginas.push({modulos: actual, continuacion, van: true});
                            actual = [];
                            usadas = 1;
                            continuacion = true;
                            pendiente = {...forzado[1], contenido: restoForzado};
                        } else {
                            pendiente = null;
                        }
                    }
                });
                if (actual.length > 0 || paginas.length === 0) {
                    paginas.push({modulos: actual, continuacion, van: false});
                }
                return paginas;
            }

            function encabezadoVista(continuacion) {
                const titulo = continuacion ? `. . . viene del ASIENTO N° ${asientoNumero} DEL RESIDENTE DE OBRA` : `ASIENTO N° ${asientoNumero} DEL RESIDENTE DE OBRA`;
                return `<div class="encabezado-asiento ${continuacion ? 'continuacion' : ''}"><div class="titulo-asiento">${esc(titulo)}</div><div class="fecha-asiento">${esc(asientoFechaTexto)}</div></div>`;
            }

            function renderAsientoPaginado(editable=false) {
                if (!Array.isArray(asientoModulos) || asientoModulos.length === 0) return;
                const paginas = paginarVista(asientoModulos);
                const renderModulo = editable ? htmlModuloEditable : htmlModuloVista;
                document.getElementById('asientoPaper').innerHTML = paginas.map((p, idx) => `
                    <div class="papel-fisico hoja-pdf">
                        ${encabezadoGeneralVista()}
                        <div class="p-body-lines">
                            <div class="pagina-cuaderno"><div class="lapicero">
                                ${encabezadoVista(p.continuacion)}
                                ${p.modulos.map(renderModulo).join('')}
                                ${p.van ? '<span class="van-final">van . . .</span>' : ''}
                            </div></div>
                        </div>
                        ${firmasVista()}
                        <div class="page-counter">${idx + 1} de ${paginas.length}</div>
                    </div>
                `).join('');
            }

            function prepararAsientoPDF() {
                renderAsientoPaginado(false);
            }

            function encabezadoGeneralVista() {
                const destino = `${window.location.origin}/resumen_asiento/${encodeURIComponent(asientoFechaRaw || '')}`;
                const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=120x120&margin=0&data=${encodeURIComponent(destino)}`;
                return `
                    <div class="p-header-top">
                        <div class="p-header-side"></div>
                        <div class="p-title-box"><h1>CUADERNO DE OBRA</h1></div>
                        <div class="p-header-side">
                            <a class="p-qr-link" href="${destino}" target="_blank" rel="noopener">
                                <img alt="QR para ver PDF del asiento" src="${qrUrl}">
                            </a>
                        </div>
                    </div>
                    <div class="p-meta">
                        <div class="p-meta-row">
                            <div class="p-meta-field fecha"><span class="p-label">Fecha:</span><div class="p-line"><span class="lapicero-meta">${esc(asientoFechaTexto)}</span></div></div>
                            <div class="p-meta-field modalidad"><span class="p-label">Modalidad:</span><div class="p-line"><span class="lapicero-meta">Administracion Directa</span></div></div>
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
                setTimeout(() => { renderAsientoPaginado(resumenEditable); }, 700);
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
                            .papel-fisico { position: relative; width: 210mm; height: 297mm; min-height: 297mm; max-height: 297mm; box-sizing: border-box; padding: 8mm 12mm 9mm; margin: 0; page-break-after: always; break-after: page; display: flex; flex-direction: column; overflow: hidden; background: #fdfdfa; border: none; box-shadow: none; font-family: Arial, sans-serif; color: #000; }
                            .papel-fisico:last-child { page-break-after: auto; break-after: auto; }
                            .p-header-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 2mm; flex: 0 0 auto; }
                            .p-header-side { width: 86px; flex: 0 0 86px; }
                            .p-qr-link { width: 62px; display: block; margin-left: auto; text-decoration: none; }
                            .p-qr-link img { width: 62px; height: 62px; display: block; object-fit: contain; border: 0; border-radius: 0; padding: 0; background: transparent; }
                            .p-title-box { text-align: center; flex: 1; margin-left: 0; }
                            .p-title-box h1 { font-size: 28px; font-weight: bold; text-decoration: underline; letter-spacing: 1.5px; margin: 0; }
                            .p-num { font-size: 24px; font-weight: bold; }
                            .p-meta { flex: 0 0 auto; margin-bottom: 1mm; padding-bottom: 1mm; border-bottom: 3px solid #000; }
                            .p-meta-row { display: flex; align-items: flex-end; gap: 15px; width: 100%; margin-bottom: 2px; }
                            .p-meta-field { display: flex; align-items: flex-end; min-width: 0; }
                            .p-meta-field.fecha { flex: 0 0 46%; }
                            .p-meta-field.modalidad { flex: 1 1 auto; }
                            .p-row { display: flex; align-items: flex-end; margin-bottom: 2px; }
                            .p-label { font-size: 14px; font-weight: bold; margin-right: 8px; }
                            .p-line { flex: 1; border-bottom: 1px solid #000; position: relative; height: 17px; }
                            .lapicero-meta { position: absolute; bottom: -1px; left: 10px; font-family: Candara, Calibri, Arial, sans-serif; font-style: italic; color: #0263a0; font-size: 16px; font-weight: 500; white-space: nowrap; }
                            .p-body-lines { flex: 0 0 780px; min-height: 780px; max-height: 780px; margin-top: 1px; margin-bottom: 2mm; overflow: hidden; display: flex; flex-direction: column; }
                            .pagina-cuaderno { flex: 0 0 780px; height: 780px; min-height: 780px; max-height: 780px; overflow: hidden; background-image: repeating-linear-gradient(to bottom, transparent 0, transparent 25px, #cbd5e1 25px, #cbd5e1 26px); background-size: 100% 26px; background-position: top left; line-height: 26px; display: flex; flex-direction: column; }
                            .lapicero { flex: 1 1 auto; min-height: 0; overflow: hidden; display: flex; flex-direction: column; font-family: Candara, Calibri, Arial, sans-serif; font-style: italic; color: #0263a0; font-size: 17px; line-height: 26px; padding-left: 2px; font-weight: 400; text-align: justify; word-wrap: break-word; overflow-wrap: anywhere; word-break: break-word; }
                            .encabezado-asiento { position: relative; margin: 0 0 3px; min-height: 26px; font-weight: 700; }
                            .titulo-asiento { width: 100%; text-align: center; text-transform: uppercase; font-weight: 800; padding: 0 128px 0 8px; white-space: nowrap; }
                            .fecha-asiento { position: absolute; top: 0; right: 0; text-align: right; white-space: nowrap; }
                            .encabezado-asiento.continuacion .titulo-asiento { padding: 0 128px 0 8px; text-align: center; text-transform: none; }
                            .encabezado-asiento.continuacion .fecha-asiento { display: block; }
                            .modulo-titulo { display: block; font-weight: 700; color: #075985; }
                            .modulo-contenido { display: block; padding-left: 22px; text-indent: 0; white-space: pre-wrap; overflow-wrap: anywhere; word-break: break-word; }
                            .personal-bloque { display: block; padding-left: 22px; }
                            .personal-subtitulo { display: block; padding-left: 18px; font-weight: 700; line-height: 26px; }
                            .personal-gastos-linea { display: block; padding-left: 48px; line-height: 26px; text-align: justify; }
                            .personal-costo-fila { display: block; padding-left: 0; line-height: 26px; text-align: center; white-space: pre-wrap; }
                            .van-final { margin-top: auto; display: block; text-align: right; padding-right: 8px; font-weight: 800; color: #075985; }
                            .p-footer { flex: 0 0 auto; display: flex; justify-content: space-between; margin-top: auto; padding-top: 5mm; padding-bottom: 2mm; font-size: 12px; font-weight: bold; color: #000; page-break-inside: avoid; break-inside: avoid; }
                            .p-sig { border-top: 1px solid #000; width: 28%; text-align: center; padding-top: 5px; }
                            .page-counter { position: absolute; right: 14mm; bottom: 5mm; font-size: 9px; font-weight: 600; color: #94a3b8; }
                        </style>
                    </head>
                    <body>${contenido.innerHTML}</body>
                    </html>
                `);
                ventana.document.close();
                ventana.focus();
                setTimeout(() => ventana.print(), 350);
            }
            document.addEventListener('DOMContentLoaded', () => {
                if (Array.isArray(asientoModulos) && asientoModulos.length > 0) {
                    renderAsientoPaginado(resumenEditable);
                }
            });
        </script>
    </body>
    </html>
    """, asiento=asiento, html_cuaderno=html_cuaderno, modulos_json=modulos_json, fecha_texto=fecha_texto, menu_superior=menu_superior, editable_resumen=editable_resumen, puede_anular_firma=puede_anular_firma)


@cuaderno_bp.route('/resumen_asiento/<fecha>')
def resumen_asiento_fecha(fecha):
    if 'usuario_id' not in session:
        return redirect(url_for('login.mostrar_login'))
    asiento = obtener_asiento_por_fecha(fecha)
    if not asiento:
        return redirect(url_for('cuaderno.panel_cuaderno'))
    return ver_asiento_cuaderno(asiento["numero"])


@cuaderno_bp.route('/cuaderno/resumen')
def resumen_cuaderno():
    if 'usuario_id' not in session:
        return redirect(url_for('login.mostrar_login'))

    fecha = (request.args.get("fecha") or "").strip()
    numero = (request.args.get("asiento") or request.args.get("numero") or "").strip()
    asiento = None
    if numero:
        try:
            asiento = obtener_asiento(int(numero))
        except (TypeError, ValueError):
            asiento = None
    if not asiento and fecha:
        asiento = obtener_asiento_por_fecha(fecha)
    if not asiento:
        return redirect(url_for('cuaderno.panel_cuaderno'))

    try:
        contenido = json.loads(asiento.get("contenido") or "{}")
    except Exception:
        contenido = {}

    modulos_guardados = contenido.get("modulos") or []
    inspector = obtener_inspector_asiento(numero=asiento.get("numero"), fecha=asiento.get("fecha"))
    try:
        contenido_inspector = json.loads(inspector.get("contenido") or "{}") if inspector else {}
    except Exception:
        contenido_inspector = {}

    volver = f"/cuaderno/resumen?fecha={asiento.get('fecha')}&asiento={asiento.get('numero')}"
    continuar_url = url_for(
        "residencia.redaccion_asiento_residente",
        asiento=asiento.get("numero"),
        fecha=asiento.get("fecha"),
        modo="continuar",
        modulo=1,
        paso=1,
        volver=volver,
    )
    modulos = [
        {"origen": "Residencia", "paso": 1, "nombre": "Jornal de trabajo", "contenido": "", "edit_url": url_for("residencia.redaccion_asiento_residente", asiento=asiento.get("numero"), fecha=asiento.get("fecha"), modo="continuar", modulo=1, paso=1, volver=volver)},
        {"origen": "Residencia", "paso": 2, "nombre": "Personal de obra", "contenido": "", "edit_url": url_for("residencia.redaccion_asiento_residente", asiento=asiento.get("numero"), fecha=asiento.get("fecha"), modo="continuar", modulo=2, paso=2, volver=volver)},
        {"origen": "Residencia", "paso": 3, "nombre": "Partidas ejecutadas", "contenido": "", "edit_url": url_for("residencia.redaccion_asiento_residente", asiento=asiento.get("numero"), fecha=asiento.get("fecha"), modo="continuar", modulo=3, paso=3, volver=volver)},
        {"origen": "Residencia", "paso": 4, "nombre": "Partidas de mayor metrado", "contenido": "", "edit_url": url_for("residencia.redaccion_asiento_residente", asiento=asiento.get("numero"), fecha=asiento.get("fecha"), modo="continuar", modulo=4, paso=4, volver=volver)},
        {"origen": "Residencia", "paso": 5, "nombre": "Sub partidas ejecutadas", "contenido": "", "edit_url": url_for("residencia.redaccion_asiento_residente", asiento=asiento.get("numero"), fecha=asiento.get("fecha"), modo="continuar", modulo=5, paso=5, volver=volver)},
        {"origen": "Residencia", "paso": 6, "nombre": "Actividades ejecutadas", "contenido": "", "edit_url": url_for("residencia.redaccion_asiento_residente", asiento=asiento.get("numero"), fecha=asiento.get("fecha"), modo="continuar", modulo=6, paso=6, volver=volver)},
        {"origen": "Residencia", "paso": 7, "nombre": "Movimiento de almacén", "contenido": "", "edit_url": url_for("residencia.redaccion_asiento_residente", asiento=asiento.get("numero"), fecha=asiento.get("fecha"), modo="continuar", modulo=7, paso=7, volver=volver)},
        {"origen": "Residencia", "paso": 8, "nombre": "Equipo mecánico / Maquinarias", "contenido": "", "edit_url": url_for("residencia.redaccion_asiento_residente", asiento=asiento.get("numero"), fecha=asiento.get("fecha"), modo="continuar", modulo=8, paso=8, volver=volver)},
        {"origen": "Residencia", "paso": 9, "nombre": "Herramientas manuales", "contenido": "", "edit_url": url_for("residencia.redaccion_asiento_residente", asiento=asiento.get("numero"), fecha=asiento.get("fecha"), modo="continuar", modulo=9, paso=9, volver=volver)},
        {"origen": "Residencia", "paso": 10, "nombre": "Ocurrencias y otros", "contenido": "", "edit_url": url_for("residencia.redaccion_asiento_residente", asiento=asiento.get("numero"), fecha=asiento.get("fecha"), modo="continuar", modulo=10, paso=10, volver=volver)},
    ]
    for modulo in modulos:
        modulo["titulo_guardado"] = ""
        for guardado in modulos_guardados:
            titulo = str((guardado or {}).get("titulo") or "")
            if titulo.startswith(f"{modulo['paso']}."):
                modulo["titulo_guardado"] = titulo
                modulo["contenido"] = str((guardado or {}).get("contenido") or "").strip()
                break
        modulo["tiene_contenido"] = modulo["contenido"] not in ("", "-")

    if inspector:
        inspector_modulos = [
            (1, "Personal de Supervisión", ", ".join(f"(1) {nombre}" for nombre in (contenido_inspector.get("personal_supervision") or inspector.get("personal_supervision") or []))),
            (2, "Partidas ejecutadas", contenido_inspector.get("partidas_ejecutadas") or inspector.get("partidas_ejecutadas") or ""),
            (3, "Movimiento de almacén", "\n".join([
                "INGRESO: " + (contenido_inspector.get("almacen_ingreso") or inspector.get("almacen_ingreso") or "-"),
                "SALIDA: " + (contenido_inspector.get("almacen_salida") or inspector.get("almacen_salida") or "-"),
            ])),
            (4, "Equipo mecánico / Maquinaria", contenido_inspector.get("maquinaria") or inspector.get("maquinaria") or ""),
            (5, "Ocurrencias y observaciones", contenido_inspector.get("ocurrencias") or inspector.get("ocurrencias") or ""),
        ]
        for paso, nombre, texto in inspector_modulos:
            contenido_modulo = str(texto or "").strip()
            modulos.append({
                "origen": "Supervisión",
                "paso": paso,
                "nombre": nombre,
                "titulo_guardado": f"{paso}. {nombre}",
                "contenido": contenido_modulo,
                "tiene_contenido": contenido_modulo not in ("", "-"),
                "edit_url": url_for("inspector.redactar_asiento_inspector", asiento=asiento.get("numero"), fecha=asiento.get("fecha"), modulo=paso, paso=paso, volver=volver),
            })

    menu_superior = obtener_navbar(session.get('rol') == 'Admin', session.get('nombre', 'Visitante'))
    calendario_url = url_for("cuaderno.panel_cuaderno")

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Resumen del asiento</title>
        <script>window.tailwind = window.tailwind || {}; window.tailwind.config = { corePlugins: { preflight: false } };</script>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    </head>
    <body class="min-h-screen bg-slate-100 text-slate-900">
        {{ menu_superior | safe }}
        <main class="mx-auto max-w-5xl px-4 py-24">
            <section class="mb-6 rounded-[30px] border border-white/80 bg-white/90 p-6 shadow-2xl shadow-slate-200/70">
                <p class="mb-2 text-xs font-black uppercase tracking-[.22em] text-sky-700">Cuaderno de Obra</p>
                <div class="flex flex-wrap items-end justify-between gap-4">
                    <div>
                        <h1 class="m-0 text-3xl font-black tracking-tight text-slate-950">Resumen del Asiento N° {{ asiento.numero }}</h1>
                        <p class="m-0 mt-2 text-sm font-bold text-slate-500">Fecha: {{ asiento.fecha }} · Estado: {{ asiento.estado }}</p>
                    </div>
                    <a href="/resumen_asiento/{{ asiento.fecha }}" class="rounded-full bg-slate-950 px-5 py-3 text-xs font-black uppercase tracking-wide text-white no-underline shadow-lg shadow-slate-300">
                        Ver hoja completa
                    </a>
                </div>
            </section>

            <section class="rounded-[30px] border border-white/80 bg-white/90 p-4 shadow-2xl shadow-slate-200/70">
                <div class="mb-4 flex flex-wrap items-center justify-between gap-3 px-2">
                    <div>
                        <h2 class="m-0 text-xl font-black text-slate-950">Módulos registrados</h2>
                        <p class="m-0 mt-1 text-sm font-semibold text-slate-500">Despliegue un módulo para revisar el contenido y corregirlo en su ventana original.</p>
                    </div>
                    <div class="flex flex-wrap gap-2">
                        <button type="button" id="btnDesglosarModulos" onclick="alternarDesgloseModulos()" class="rounded-full bg-sky-100 px-6 py-3 text-xs font-black uppercase tracking-wide text-sky-800 shadow-lg shadow-sky-100">
                            Desglosar módulos
                        </button>
                        <button type="button" onclick="abrirDecisionCierre()" class="rounded-full bg-gradient-to-r from-emerald-600 to-slate-950 px-6 py-3 text-xs font-black uppercase tracking-wide text-white shadow-lg shadow-emerald-200">
                            Cerrar Asiento
                        </button>
                    </div>
                </div>
                <div class="grid gap-3" id="listaModulosResumen">
                    {% for modulo in modulos %}
                    <details class="group rounded-3xl border border-slate-200 bg-slate-50/80 p-2 open:bg-white open:shadow-lg">
                        <summary class="flex cursor-pointer list-none flex-wrap items-center justify-between gap-3 rounded-2xl p-3">
                            <div class="flex items-center gap-4">
                                <div class="grid h-12 w-12 place-items-center rounded-2xl {% if modulo.origen == 'Supervisión' %}bg-blue-100 text-blue-800{% else %}bg-emerald-100 text-emerald-800{% endif %} text-lg font-black">{{ modulo.paso }}</div>
                                <div>
                                    <div class="mb-1 inline-flex rounded-full {% if modulo.origen == 'Supervisión' %}bg-blue-50 text-blue-700{% else %}bg-emerald-50 text-emerald-700{% endif %} px-2 py-1 text-[10px] font-black uppercase tracking-wide">{{ modulo.origen }}</div>
                                    <h3 class="m-0 text-base font-black text-slate-900">Módulo {{ modulo.paso }}: {{ modulo.nombre }}</h3>
                                    <p class="m-0 mt-1 text-xs font-bold {% if modulo.tiene_contenido %}text-emerald-600{% else %}text-slate-400{% endif %}">
                                        {% if modulo.tiene_contenido %}Con información registrada{% else %}Sin información registrada{% endif %}
                                    </p>
                                </div>
                            </div>
                            <i class="bi bi-chevron-down text-xl text-slate-400 transition group-open:rotate-180"></i>
                        </summary>
                        <div class="px-4 pb-4">
                            <pre class="mb-4 max-h-72 overflow-auto whitespace-pre-wrap rounded-2xl border border-slate-200 bg-white p-4 font-[Candara] text-[16px] italic leading-7 text-sky-700">{{ modulo.contenido or 'Sin información registrada.' }}</pre>
                            <a href="{{ modulo.edit_url }}" class="inline-flex rounded-full bg-gradient-to-r from-sky-700 to-slate-950 px-5 py-3 text-xs font-black uppercase tracking-wide text-white no-underline shadow-lg shadow-sky-200">
                                <i class="bi bi-pencil-square mr-2"></i> Corregir/Editar
                            </a>
                        </div>
                    </details>
                    {% endfor %}
                </div>
            </section>
        </main>

        <div id="decisionCierreModal" class="fixed inset-0 z-[2500] hidden place-items-center bg-slate-950/70 p-4 backdrop-blur-md">
            <div id="decisionCierreCard" class="w-full max-w-md scale-95 rounded-3xl bg-white p-6 opacity-0 shadow-2xl transition">
                <div class="mb-4 grid h-14 w-14 place-items-center rounded-2xl bg-emerald-50 text-3xl text-emerald-600">
                    <i class="bi bi-check2-circle"></i>
                </div>
                <h3 class="m-0 text-2xl font-black text-slate-950">Decisión del asiento</h3>
                <p class="mb-5 mt-2 text-sm font-bold leading-6 text-slate-600">¿Desea seguir asentando el cuaderno o cerrar?</p>
                <div class="flex flex-wrap justify-end gap-2">
                    <button type="button" onclick="window.location.href='{{ continuar_url }}'" class="rounded-2xl bg-sky-100 px-4 py-3 text-sm font-black text-sky-800">Seguir asentando</button>
                    <button type="button" onclick="window.location.href='{{ calendario_url }}'" class="rounded-2xl bg-slate-950 px-4 py-3 text-sm font-black text-white">Cerrar</button>
                    <button type="button" onclick="cerrarDecisionCierre()" class="rounded-2xl bg-slate-100 px-4 py-3 text-sm font-black text-slate-600">Cancelar</button>
                </div>
            </div>
        </div>

        <script>
            let modulosResumenAbiertos = false;
            function alternarDesgloseModulos() {
                modulosResumenAbiertos = !modulosResumenAbiertos;
                document.querySelectorAll('#listaModulosResumen details').forEach(item => {
                    item.open = modulosResumenAbiertos;
                });
                const boton = document.getElementById('btnDesglosarModulos');
                if (boton) boton.textContent = modulosResumenAbiertos ? 'Contraer módulos' : 'Desglosar módulos';
            }
            function abrirDecisionCierre() {
                const overlay = document.getElementById('decisionCierreModal');
                const card = document.getElementById('decisionCierreCard');
                overlay.classList.remove('hidden');
                overlay.classList.add('grid');
                requestAnimationFrame(() => card.classList.remove('scale-95', 'opacity-0'));
            }
            function cerrarDecisionCierre() {
                const overlay = document.getElementById('decisionCierreModal');
                const card = document.getElementById('decisionCierreCard');
                card.classList.add('scale-95', 'opacity-0');
                setTimeout(() => {
                    overlay.classList.add('hidden');
                    overlay.classList.remove('grid');
                }, 150);
            }
        </script>
    </body>
    </html>
    """, menu_superior=menu_superior, asiento=asiento, modulos=modulos, volver=volver, continuar_url=continuar_url, calendario_url=calendario_url)

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
        <title>Cuaderno de Obra</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
            window.tailwind = window.tailwind || {};
            window.tailwind.config = { corePlugins: { preflight: false } };
        </script>
        <script src="https://cdn.tailwindcss.com"></script>
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
            .calendar-day.future {
                border-color: #e2e8f0;
                background: linear-gradient(135deg, #ffffff, #f8fafc);
                color: #94a3b8;
                cursor: default;
            }
            .calendar-day.future .day-number { background: #e2e8f0; color: #64748b; }
            .calendar-day.future:hover {
                transform: none;
                box-shadow: none;
            }
            .calendar-day.observed {
                border-color: #fdba74;
                background: linear-gradient(135deg, #fff7ed, #ffedd5);
            }
            .calendar-day.observed .day-number { background: #f97316; color: #fff; }
            .calendar-day.residencia {
                border-color: #86efac;
                background: linear-gradient(135deg, #f0fdf4, #dcfce7);
            }
            .calendar-day.residencia .day-number { background: #16a34a; color: #fff; }
            .calendar-day.supervision {
                border-color: #93c5fd;
                background: linear-gradient(135deg, #eff6ff, #dbeafe);
            }
            .calendar-day.supervision .day-number { background: #2563eb; color: #fff; }
            .calendar-day.mixto {
                border-color: #7dd3fc;
                background: linear-gradient(135deg, #dcfce7 0%, #dcfce7 49%, #dbeafe 50%, #dbeafe 100%);
            }
            .calendar-day.mixto .day-number { background: linear-gradient(135deg, #16a34a, #2563eb); color: #fff; }
            .calendar-day.pending,
            .calendar-day.pending.residencia,
            .calendar-day.pending.supervision,
            .calendar-day.pending.mixto {
                border-color: #fecaca;
                background: linear-gradient(135deg, #fff1f2, #fee2e2);
            }
            .calendar-day.pending .day-number { background: #ef4444; color: #fff; }
            .calendar-day.draft,
            .calendar-day.draft.residencia,
            .calendar-day.draft.supervision,
            .calendar-day.draft.mixto,
            .calendar-day.observed,
            .calendar-day.observed.residencia,
            .calendar-day.observed.supervision,
            .calendar-day.observed.mixto {
                border-color: #fde68a;
                background: linear-gradient(135deg, #fefce8, #fef3c7);
            }
            .calendar-day.draft .day-number,
            .calendar-day.observed .day-number { background: #facc15; color: #713f12; }
            .calendar-day.sent,
            .calendar-day.sent.residencia,
            .calendar-day.sent.supervision,
            .calendar-day.sent.mixto {
                border-color: #86efac;
                background: linear-gradient(135deg, #f0fdf4, #dcfce7);
            }
            .calendar-day.sent .day-number { background: #22c55e; color: #fff; }
            .calendar-day.signed,
            .calendar-day.signed.residencia,
            .calendar-day.signed.supervision,
            .calendar-day.signed.mixto {
                border-color: #93c5fd;
                background: linear-gradient(135deg, #eff6ff, #dbeafe);
            }
            .calendar-day.signed .day-number { background: #2563eb; color: #fff; }

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
                width: min(100%, 920px);
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

            .mini-seat-calendar {
                display: grid;
                grid-template-columns: repeat(7, minmax(0, 1fr));
                gap: 7px;
                min-height: 344px;
                grid-template-rows: repeat(6, minmax(52px, 1fr));
            }

            .mini-seat-day {
                min-height: 52px;
                border: 1px solid #e2e8f0;
                border-radius: 14px;
                background: #fff;
                color: #334155;
                font-size: 12px;
                font-weight: 900;
                transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
            }

            .mini-seat-day:hover {
                transform: scale(1.08);
                box-shadow: 0 14px 30px rgba(15,23,42,.14);
                z-index: 2;
            }

            .mini-seat-day.empty {
                opacity: .25;
                pointer-events: none;
                background: transparent;
            }

            .mini-seat-day.pending {
                border-color: #fecaca;
                background: linear-gradient(135deg, #fff1f2, #fee2e2);
                color: #991b1b;
            }

            .mini-seat-day.future {
                border-color: #e2e8f0;
                background: linear-gradient(135deg, #ffffff, #f8fafc);
                color: #94a3b8;
                cursor: default;
            }

            .mini-seat-day.future:hover {
                transform: none;
                box-shadow: none;
            }

            .mini-seat-day.draft {
                border-color: #fde68a;
                background: linear-gradient(135deg, #fefce8, #fef3c7);
                color: #713f12;
            }

            .mini-seat-day.closed {
                border-color: #bbf7d0;
                background: linear-gradient(135deg, #f0fdf4, #dcfce7);
                color: #166534;
            }

            .mini-seat-day.observed {
                border-color: #fdba74;
                background: linear-gradient(135deg, #fff7ed, #ffedd5);
                color: #9a3412;
            }
            .mini-seat-day.residencia {
                border-color: #86efac;
                background: linear-gradient(135deg, #f0fdf4, #dcfce7);
                color: #166534;
            }
            .mini-seat-day.supervision {
                border-color: #93c5fd;
                background: linear-gradient(135deg, #eff6ff, #dbeafe);
                color: #1d4ed8;
            }
            .mini-seat-day.mixto {
                border-color: #7dd3fc;
                background: linear-gradient(135deg, #dcfce7 0%, #dcfce7 49%, #dbeafe 50%, #dbeafe 100%);
                color: #0f172a;
            }
            .mini-seat-day.draft,
            .mini-seat-day.draft.residencia,
            .mini-seat-day.draft.supervision,
            .mini-seat-day.draft.mixto,
            .mini-seat-day.observed,
            .mini-seat-day.observed.residencia,
            .mini-seat-day.observed.supervision,
            .mini-seat-day.observed.mixto {
                border-color: #fde68a;
                background: linear-gradient(135deg, #fefce8, #fef3c7);
                color: #713f12;
            }
            .mini-seat-day.sent,
            .mini-seat-day.sent.residencia,
            .mini-seat-day.sent.supervision,
            .mini-seat-day.sent.mixto {
                border-color: #86efac;
                background: linear-gradient(135deg, #f0fdf4, #dcfce7);
                color: #166534;
            }
            .mini-seat-day.signed,
            .mini-seat-day.signed.residencia,
            .mini-seat-day.signed.supervision,
            .mini-seat-day.signed.mixto {
                border-color: #93c5fd;
                background: linear-gradient(135deg, #eff6ff, #dbeafe);
                color: #1d4ed8;
            }

            .mini-seat-day.selected {
                outline: 3px solid rgba(2,99,160,.26);
                transform: scale(1.04);
                box-shadow: 0 16px 34px rgba(2,99,160,.18);
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

            .flotar-adentro {
                opacity: 0;
                transform: translateY(22px);
                transition: opacity .65s cubic-bezier(.16,.84,.24,1), transform .65s cubic-bezier(.16,.84,.24,1);
                will-change: opacity, transform;
            }

            .flotar-adentro.visible {
                opacity: 1;
                transform: translateY(0);
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
                        <h1>Cuaderno de Obra</h1>
                        <p>Panel principal para redactar asientos, revisar estados del mes, atender observaciones del Inspector y exportar rangos del cuaderno.</p>
                    </div>
                    <span class="connection-pill">
                        <i class="bi bi-journal-check"></i>
                        Listo para registrar
                    </span>
                </div>

                <div class="action-topbar">
                    <a class="primary-action residencia" href="/residencia" onclick="abrirModalAsientoResidencia(event)">
                        <span class="action-icon"><i class="bi bi-journal-richtext"></i></span>
                        <span>
                            <small>Permiso residencia</small>
                            <strong>ASENTAR ASIENTO DE RESIDENCIA</strong>
                        </span>
                    </a>
                    <a class="primary-action supervision" href="/inspector" onclick="abrirModalAsientoInspector(event)">
                        <span class="action-icon"><i class="bi bi-shield-check"></i></span>
                        <span>
                            <small>Permiso supervisión</small>
                            <strong>ASENTAR ASIENTO DE SUPERVISIÓN</strong>
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
                <div class="mini-stat"><span>Firmados Inspector</span><strong>{{ estadisticas.firmados }}</strong></div>
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
                                <div><span><span class="dot" style="background:#2563eb;"></span> Firmados Inspector</span><b id="signedCount">0</b></div>
                                <div><span><span class="dot" style="background:#22c55e;"></span> Enviados a Inspector</span><b id="sentCount">0</b></div>
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
                                    <p class="alert-copy"><b>Sin observaciones críticas activas.</b><br>Cuando el Inspector registre un post-it pendiente, aparecerá aquí para Residencia.</p>
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

        <div id="seatEntryModal" class="seat-modal-overlay hidden transition-opacity duration-200" role="dialog" aria-modal="true" aria-labelledby="seatEntryTitle">
            <div class="seat-modal-card">
                <div class="seat-modal-head">
                    <div>
                        <h3 id="seatEntryTitle">Redactar Asiento</h3>
                        <p id="seatEntrySubtitle">Seleccione una fecha. Rojo sin registro, amarillo borrador, verde enviado al Inspector y azul firmado.</p>
                    </div>
                    <button type="button" class="seat-modal-close" onclick="cerrarModalAsiento()" aria-label="Cerrar">&times;</button>
                </div>
                <div class="grid gap-3">
                    <div class="flex flex-wrap items-center justify-between gap-3 rounded-2xl bg-slate-50 px-3 py-2">
                        <div class="inline-flex items-center gap-2 rounded-full bg-white p-1 shadow-sm">
                            <button type="button" class="rounded-full bg-slate-100 px-3 py-2 text-xs font-black text-slate-700 transition hover:bg-slate-200" onclick="cambiarMesModal(-1)">
                                <i class="bi bi-chevron-left"></i>
                            </button>
                            <span id="miniMonthLabel" class="min-w-[150px] text-center text-xs font-black uppercase tracking-wide text-slate-700">Mes actual</span>
                            <button type="button" class="rounded-full bg-slate-100 px-3 py-2 text-xs font-black text-slate-700 transition hover:bg-slate-200" onclick="cambiarMesModal(1)">
                                <i class="bi bi-chevron-right"></i>
                            </button>
                        </div>
                        <span class="inline-flex items-center gap-2 text-[11px] font-black text-slate-500">
                            <span class="inline-block h-2.5 w-2.5 rounded-full bg-red-500"></span>Nuevo
                            <span class="inline-block h-2.5 w-2.5 rounded-full bg-yellow-400"></span>Borrador
                            <span class="inline-block h-2.5 w-2.5 rounded-full bg-green-500"></span>Enviado
                            <span class="inline-block h-2.5 w-2.5 rounded-full bg-blue-600"></span>Firmado
                        </span>
                    </div>
                    <div class="grid grid-cols-7 gap-1 text-center text-[10px] font-black uppercase text-slate-400">
                        <span>Lun</span><span>Mar</span><span>Mié</span><span>Jue</span><span>Vie</span><span>Sáb</span><span>Dom</span>
                    </div>
                    <div id="miniSeatCalendar" class="mini-seat-calendar"></div>
                </div>
            </div>
        </div>

        <div id="samuGlobalModal" class="hidden fixed inset-0 z-[2100] grid place-items-center bg-slate-950/70 p-4 backdrop-blur-md transition-opacity duration-150" role="dialog" aria-modal="true">
            <div id="samuGlobalModalCard" class="w-full max-w-md rounded-2xl bg-white p-6 opacity-0 shadow-2xl ring-1 ring-slate-200 transition-all duration-150 scale-95">
                <div class="mb-4">
                    <div id="samuGlobalModalIcon" class="mb-3 grid h-12 w-12 place-items-center rounded-2xl bg-blue-50 text-2xl text-blue-600">
                        <i class="bi bi-info-circle-fill"></i>
                    </div>
                    <h3 id="samuGlobalModalTitle" class="m-0 text-xl font-black tracking-tight text-slate-900">Mensaje</h3>
                    <p id="samuGlobalModalMessage" class="mb-0 mt-2 text-sm font-semibold leading-6 text-slate-600"></p>
                </div>
                <div id="samuGlobalModalInputWrap" class="mb-4 hidden">
                    <label id="samuGlobalModalInputLabel" class="mb-2 block text-xs font-black uppercase tracking-wide text-slate-500">Número de asiento</label>
                    <input id="samuGlobalModalInput" type="text" class="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-lg font-black text-slate-900 outline-none transition focus:ring-2 focus:ring-blue-500" placeholder="Ingrese Número de Asiento">
                </div>
                <div class="flex justify-end gap-2">
                    <button id="samuGlobalModalCancel" type="button" class="rounded-2xl bg-slate-100 px-4 py-3 text-sm font-black text-slate-700 transition hover:bg-slate-200">Cancelar</button>
                    <button id="samuGlobalModalOk" type="button" class="rounded-2xl bg-blue-600 px-4 py-3 text-sm font-black text-white shadow-lg shadow-blue-600/20 transition hover:scale-[1.02] hover:bg-blue-700">Aceptar</button>
                </div>
            </div>
        </div>

        <div id="selectorAsientoHistorico" class="hidden fixed inset-0 z-[2200] place-items-center bg-slate-950/70 p-4 backdrop-blur-md" role="dialog" aria-modal="true">
            <div id="selectorAsientoHistoricoCard" class="w-full max-w-md scale-95 rounded-3xl bg-white p-6 opacity-0 shadow-2xl transition">
                <div class="mb-3 grid h-12 w-12 place-items-center rounded-2xl bg-blue-50 text-2xl text-blue-600">
                    <i class="bi bi-journals"></i>
                </div>
                <h3 class="m-0 text-xl font-black text-slate-950">Abrir asiento registrado</h3>
                <p id="selectorAsientoHistoricoTexto" class="mb-5 mt-2 text-sm font-bold leading-6 text-slate-600">Este día tiene registros de Residencia y Supervisión. Elija cuál desea abrir.</p>
                <div class="flex flex-wrap justify-end gap-2">
                    <button type="button" onclick="cerrarSelectorAsientoHistorico()" class="rounded-2xl bg-slate-100 px-4 py-3 text-sm font-black text-slate-700">Cancelar</button>
                    <button type="button" onclick="abrirHistoricoSeleccionado('residencia')" class="rounded-2xl bg-emerald-100 px-4 py-3 text-sm font-black text-emerald-800">Residencia</button>
                    <button type="button" onclick="abrirHistoricoSeleccionado('supervision')" class="rounded-2xl bg-blue-600 px-4 py-3 text-sm font-black text-white">Supervisión</button>
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
            const rolUsuarioActual = {{ rol_usuario | tojson }};

            const estadoColor = {
                cerrado: '#22c55e',
                firmado: '#22c55e',
                borrador: '#facc15',
                pendiente: '#ef4444',
                observado: '#f97316'
            };

            const paramsInicialesPanel = new URLSearchParams(window.location.search || '');
            let mesActivo = new Date();
            const yearInicial = parseInt(paramsInicialesPanel.get('anio') || paramsInicialesPanel.get('year') || '', 10);
            const monthInicial = parseInt(paramsInicialesPanel.get('mes') || paramsInicialesPanel.get('month') || '', 10);
            if (!Number.isNaN(yearInicial) && !Number.isNaN(monthInicial) && monthInicial >= 1 && monthInicial <= 12) {
                mesActivo = new Date(yearInicial, monthInicial - 1, 1);
            }
            mesActivo.setDate(1);
            let doughnutChart = null;
            let asientosMesActivo = new Map();
            let modalMesActivo = new Date(mesActivo.getFullYear(), mesActivo.getMonth(), 1);
            let modalAsientosMes = new Map();
            let asientoModalActual = null;
            let fechaModalSeleccionada = null;
            let modoModalAsiento = 'residencia';
            let asientoHistoricoPendiente = null;

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
                if (estado.includes('firmado_inspector')) return 'firmado_inspector';
                if (estado.includes('borrador') || estado.includes('redacción') || estado.includes('redaccion')) return 'borrador';
                if (estado.includes('observ')) return 'observado';
                if (estado.includes('enviado') && estado.includes('inspector')) return 'enviado_inspector';
                if (estado.includes('cerrado') || estado.includes('firmado')) return 'firmado_inspector';
                return 'pendiente';
            }

            function estadoCalendarioAsiento(asiento) {
                if (!asiento) return 'pendiente';
                const estadoInspector = normalizarEstado(asiento.inspector_estado || '');
                const estado = normalizarEstado(asiento.estado || '');
                if (estadoInspector === 'firmado_inspector' || estado === 'firmado_inspector') return 'signed';
                if (estado === 'enviado_inspector' || estadoInspector === 'enviado_inspector') return 'sent';
                if (estado === 'borrador' || estadoInspector === 'borrador' || estado === 'observado') return 'draft';
                return estado === 'future' ? 'future' : 'pending';
            }

            function parseFechaLocal(fechaISO) {
                const partes = String(fechaISO || '').split('-').map(Number);
                if (partes.length !== 3 || partes.some(Number.isNaN)) return null;
                return { year: partes[0], monthIndex: partes[1] - 1, day: partes[2] };
            }

            function fechaAsiento(asiento, year, month) {
                const partes = parseFechaLocal(asiento.fecha);
                if (partes) return partes;
                return { year, monthIndex: month, day: Number(asiento.dia || 1) };
            }

            function fechaHoraLocal(fechaISO, hora=18, minuto=30) {
                const partes = parseFechaLocal(fechaISO);
                if (!partes) return new Date();
                return new Date(partes.year, partes.monthIndex, partes.day, hora, minuto);
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
                    return fecha.year === year && fecha.monthIndex === month;
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
                    porDia.set(fecha.day, asiento);
                });
                asientosMesActivo = porDia;

                document.getElementById('monthLabel').textContent = nombreMes(mesActivo);

                const totalDias = datos.estadisticas?.dias_mes || diasEnMes(year, month);
                let firmados = 0;
                let enviados = 0;
                let borradores = 0;
                for (const asiento of porDia.values()) {
                    const estado = estadoCalendarioAsiento(asiento);
                    if (estado === 'signed') firmados += 1;
                    if (estado === 'sent') enviados += 1;
                    if (estado === 'draft') borradores += 1;
                }
                const sinRegistro = contarPendientesVencidos(year, month, totalDias, porDia);
                const avance = totalDias > 0 ? Math.round(((firmados + enviados) / totalDias) * 100) : 0;

                renderChart(firmados, enviados, borradores, sinRegistro, avance);
                renderCalendar(year, month, totalDias, porDia);
            }

            function renderChart(firmados, enviados, borradores, sinRegistro, avance) {
                document.getElementById('monthPercent').textContent = `${avance}%`;
                document.getElementById('signedCount').textContent = firmados;
                document.getElementById('sentCount').textContent = enviados;
                document.getElementById('draftCount').textContent = borradores;
                document.getElementById('pendingCount').textContent = sinRegistro;

                const ctx = document.getElementById('monthlyDoughnut');
                const data = [firmados, enviados, borradores, sinRegistro];
                if (doughnutChart) {
                    doughnutChart.destroy();
                    doughnutChart = null;
                }
                doughnutChart = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Días firmados por Inspector', 'Días enviados al Inspector', 'Días en borrador', 'Días sin registro'],
                        datasets: [{
                            data,
                            backgroundColor: ['#2563eb', '#22c55e', '#facc15', '#ef4444'],
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
                    const fechaISO = fechaISODesdePartes(year, month, dia);
                    const estado = asiento ? estadoCalendarioAsiento(asiento) : (esFechaFutura(fechaISO) ? 'future' : 'pending');
                    const estadoVisual = estado;
                    const tipoVisual = asiento ? claseOrigenAsiento(asiento) : '';
                    const item = document.createElement('button');
                    item.type = 'button';
                    item.className = `calendar-day ${estadoVisual} ${tipoVisual}`.trim();
                    item.innerHTML = `
                        <span class="day-number">${dia}</span>
                        <span class="day-caption">${textoEstado(asiento, estado)}${asiento ? `<br>${textoOrigenAsiento(asiento)}` : ''}</span>
                        <span class="calendar-tooltip">
                            ${asiento ? `
                                <b>Asiento N° ${escapeHtml(String(asiento.numero).padStart(3, '0'))}</b><br>
                                Estado: ${escapeHtml(asiento.estado || '-')}<br>
                                Registro: ${escapeHtml(textoOrigenAsiento(asiento))}<br>
                                Avance: ${escapeHtml(asiento.avance || 0)}%<br>
                                Inspector: ${escapeHtml(asiento.supervisor || '-')}<br>
                                ${escapeHtml(asiento.observacion || 'Sin observaciones activas.')}
                            ` : `
                                <b>Día ${dia}</b><br>
                                ${estado === 'future' ? 'Fecha futura. Aún no requiere registro.' : 'Sin asiento registrado para este día.'}
                            `}
                        </span>
                    `;
                    item.dataset.fecha = fechaISO;
                    if (asiento && (asiento.numero || asiento.residencia_numero || asiento.inspector_numero)) {
                        item.addEventListener('click', () => abrirAsientoHistorico(asiento, fechaISO));
                    } else if (!asiento && estado === 'pending') {
                        item.addEventListener('click', () => abrirModalAsientoResidencia(null, fechaISO));
                    }
                    grid.appendChild(item);
                }
            }

            function fechaISODesdePartes(year, month, day) {
                return `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            }

            function hoyISOLocal() {
                const hoy = new Date();
                return fechaISODesdePartes(hoy.getFullYear(), hoy.getMonth(), hoy.getDate());
            }

            function esFechaFutura(fechaISO) {
                return String(fechaISO || '') > hoyISOLocal();
            }

            function contarPendientesVencidos(year, month, totalDias, porDia) {
                let pendientes = 0;
                for (let dia = 1; dia <= totalDias; dia += 1) {
                    const fechaISO = fechaISODesdePartes(year, month, dia);
                    if (!porDia.has(dia) && !esFechaFutura(fechaISO)) pendientes += 1;
                }
                return pendientes;
            }

            function repintarDashboardDesdeMapa(year, month, porDia) {
                const totalDias = diasEnMes(year, month);
                let firmados = 0;
                let enviados = 0;
                let borradores = 0;
                for (const asiento of porDia.values()) {
                    const estado = estadoCalendarioAsiento(asiento);
                    if (estado === 'signed') firmados += 1;
                    if (estado === 'sent') enviados += 1;
                    if (estado === 'draft') borradores += 1;
                }
                const pendientes = contarPendientesVencidos(year, month, totalDias, porDia);
                const avance = totalDias > 0 ? Math.round(((firmados + enviados) / totalDias) * 100) : 0;
                asientosMesActivo = porDia;
                document.getElementById('monthLabel').textContent = nombreMes(mesActivo);
                renderChart(firmados, enviados, borradores, pendientes, avance);
                renderCalendar(year, month, totalDias, porDia);
            }

            function aplicarCambioDashboardLocal(cambio) {
                const partes = parseFechaLocal(cambio?.fecha);
                if (!partes) return;
                const year = partes.year;
                const month = partes.monthIndex;
                const dia = partes.day;
                if (mesActivo.getFullYear() !== year || mesActivo.getMonth() !== month) {
                    mesActivo = new Date(year, month, 1);
                }
                const mapa = new Map(asientosMesActivo);
                mapa.set(dia, {
                    numero: cambio.numero,
                    fecha: cambio.fecha,
                    estado: cambio.estado || 'Borrador',
                    avance: /cerrado|firmado|inspector/i.test(String(cambio.estado || '')) ? 100 : 60,
                    supervisor: '-',
                    observacion: 'Sin observaciones activas.',
                    tipo: /inspector|super/i.test(String(cambio.tipo || '')) ? 'Inspector' : 'Residente',
                    tiene_residencia: !/inspector|super/i.test(String(cambio.tipo || '')),
                    tiene_inspector: /inspector|super/i.test(String(cambio.tipo || '')),
                    residencia_numero: !/inspector|super/i.test(String(cambio.tipo || '')) ? cambio.numero : null,
                    inspector_numero: /inspector|super/i.test(String(cambio.tipo || '')) ? cambio.numero : null,
                    updated_at: cambio.updated_at || new Date().toISOString()
                });
                dashboardSeed.asientos = [
                    ...dashboardSeed.asientos.filter(asiento => asiento.fecha !== cambio.fecha && String(asiento.numero) !== String(cambio.numero)),
                    mapa.get(dia)
                ];
                repintarDashboardDesdeMapa(year, month, mapa);
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

            function buscarAsientoPorFecha(fechaISO, mapa=asientosMesActivo, year=mesActivo.getFullYear(), month=mesActivo.getMonth()) {
                if (!fechaISO) return null;
                const fecha = parseFechaLocal(fechaISO);
                if (!fecha) return null;
                if (fecha.year !== year || fecha.monthIndex !== month) return null;
                return mapa.get(fecha.day) || null;
            }

            function tieneResidencia(asiento) {
                return Boolean(asiento?.tiene_residencia || asiento?.residencia_numero || String(asiento?.tipo || '').toLowerCase() !== 'inspector');
            }

            function tieneSupervision(asiento) {
                return Boolean(asiento?.tiene_inspector || asiento?.inspector_numero || String(asiento?.tipo || '').toLowerCase() === 'inspector');
            }

            function claseOrigenAsiento(asiento) {
                const residencia = tieneResidencia(asiento);
                const supervision = tieneSupervision(asiento);
                if (residencia && supervision) return 'mixto';
                if (supervision) return 'supervision';
                if (residencia) return 'residencia';
                return '';
            }

            function textoOrigenAsiento(asiento) {
                const residencia = tieneResidencia(asiento);
                const supervision = tieneSupervision(asiento);
                if (residencia && supervision) return 'Residencia + Supervisión';
                if (supervision) return 'Supervisión';
                if (residencia) return 'Residencia';
                return 'Sin origen';
            }

            function usuarioEsSupervision() {
                return /inspector|super/i.test(String(rolUsuarioActual || ''));
            }

            function abrirModalAsientoResidencia(event, fechaISO=null) {
                if (event) event.preventDefault();
                modoModalAsiento = 'residencia';
                const modal = document.getElementById('seatEntryModal');
                document.getElementById('seatEntryTitle').textContent = 'Redactar Asiento de Residencia';
                document.getElementById('seatEntrySubtitle').textContent = 'Seleccione una fecha. Rojo sin registro, amarillo continúa borrador, verde enviado al Inspector y azul firmado.';
                const fecha = parseFechaLocal(fechaISO || fechaPorDefectoModal());
                if (fecha) modalMesActivo = new Date(fecha.year, fecha.monthIndex, 1);
                modal.classList.remove('hidden');
                renderCalendarioModalAsiento();
            }

            function abrirModalAsientoInspector(event, fechaISO=null) {
                if (event) event.preventDefault();
                modoModalAsiento = 'inspector';
                const modal = document.getElementById('seatEntryModal');
                document.getElementById('seatEntryTitle').textContent = 'Redactar Asiento de Inspector de Obra';
                document.getElementById('seatEntrySubtitle').textContent = 'Seleccione el día con asiento de Residencia enviado para redactar o firmar como Inspector.';
                const fecha = parseFechaLocal(fechaISO || fechaPorDefectoModal());
                if (fecha) modalMesActivo = new Date(fecha.year, fecha.monthIndex, 1);
                modal.classList.remove('hidden');
                renderCalendarioModalAsiento();
            }

            function cerrarModalAsiento() {
                document.getElementById('seatEntryModal')?.classList.add('hidden');
            }

            async function cambiarMesModal(delta) {
                modalMesActivo.setMonth(modalMesActivo.getMonth() + delta);
                await renderCalendarioModalAsiento();
            }

            async function renderCalendarioModalAsiento() {
                const year = modalMesActivo.getFullYear();
                const month = modalMesActivo.getMonth();
                const grid = document.getElementById('miniSeatCalendar');
                const label = document.getElementById('miniMonthLabel');
                if (!grid || !label) return;
                label.textContent = nombreMes(modalMesActivo);
                grid.innerHTML = '';

                const datos = await cargarDatosMes(year, month);
                modalAsientosMes = new Map();
                datos.asientos.forEach(asiento => {
                    const fecha = fechaAsiento(asiento, year, month);
                    modalAsientosMes.set(fecha.day, asiento);
                });

                const espacios = primerDiaLunes(year, month);
                for (let i = 0; i < espacios; i += 1) {
                    const empty = document.createElement('div');
                    empty.className = 'mini-seat-day empty';
                    grid.appendChild(empty);
                }

                const totalDias = diasEnMes(year, month);
                for (let dia = 1; dia <= totalDias; dia += 1) {
                    const fechaISO = fechaISODesdePartes(year, month, dia);
                    const asiento = buscarAsientoPorFecha(fechaISO, modalAsientosMes, year, month);
                    const estado = asiento ? estadoCalendarioAsiento(asiento) : (esFechaFutura(fechaISO) ? 'future' : 'pending');
                    const estadoVisual = estado;
                    const tipoVisual = asiento ? claseOrigenAsiento(asiento) : '';
                    const day = document.createElement('button');
                    day.type = 'button';
                    day.className = `mini-seat-day ${estadoVisual} ${tipoVisual}`.trim();
                    day.title = asiento ? textoOrigenAsiento(asiento) : 'Sin registro';
                    day.textContent = dia;
                    if (estado !== 'future') {
                        day.addEventListener('click', () => gestionarClickDiaRedaccion(fechaISO, asiento));
                    }
                    grid.appendChild(day);
                }
            }

            function gestionarClickDiaRedaccion(fechaISO, asiento) {
                if (modoModalAsiento === 'inspector') {
                    const params = new URLSearchParams({ fecha: fechaISO });
                    if (asiento?.residencia_numero || asiento?.numero) params.set('asiento', asiento.residencia_numero || asiento.numero);
                    window.location.href = `/inspector?${params.toString()}`;
                    return;
                }
                if (asiento) {
                    abrirAsientoHistorico(asiento, fechaISO);
                    return;
                }
                pedirNumeroAsientoElegante(fechaISO).then(numero => {
                    if (!numero || !String(numero).trim()) return;
                    iniciarNuevoAsientoSeguro(fechaISO, String(numero).trim());
                });
            }

            function abrirModalGlobal({ title, message, icon='bi-info-circle-fill', type='info', input=false, inputLabel='Número de asiento', inputPlaceholder='Ingrese Número de Asiento', okText='Aceptar', cancelText='Cancelar' }) {
                return new Promise(resolve => {
                    const overlay = document.getElementById('samuGlobalModal');
                    const card = document.getElementById('samuGlobalModalCard');
                    const titleEl = document.getElementById('samuGlobalModalTitle');
                    const msgEl = document.getElementById('samuGlobalModalMessage');
                    const iconEl = document.getElementById('samuGlobalModalIcon');
                    const inputWrap = document.getElementById('samuGlobalModalInputWrap');
                    const inputEl = document.getElementById('samuGlobalModalInput');
                    const inputLabelEl = document.getElementById('samuGlobalModalInputLabel');
                    const okBtn = document.getElementById('samuGlobalModalOk');
                    const cancelBtn = document.getElementById('samuGlobalModalCancel');
                    const iconClasses = {
                        success: 'mb-3 grid h-12 w-12 place-items-center rounded-2xl bg-green-50 text-2xl text-green-600',
                        error: 'mb-3 grid h-12 w-12 place-items-center rounded-2xl bg-red-50 text-2xl text-red-600',
                        warning: 'mb-3 grid h-12 w-12 place-items-center rounded-2xl bg-amber-50 text-2xl text-amber-600',
                        info: 'mb-3 grid h-12 w-12 place-items-center rounded-2xl bg-blue-50 text-2xl text-blue-600'
                    };
                    titleEl.textContent = title || 'Mensaje';
                    msgEl.textContent = message || '';
                    iconEl.className = iconClasses[type] || iconClasses.info;
                    iconEl.innerHTML = `<i class="bi ${icon}"></i>`;
                    inputWrap.classList.toggle('hidden', !input);
                    inputLabelEl.textContent = inputLabel;
                    inputEl.value = '';
                    inputEl.placeholder = inputPlaceholder;
                    okBtn.textContent = okText;
                    cancelBtn.textContent = cancelText;
                    cancelBtn.classList.toggle('hidden', !input);

                    const cerrar = valor => {
                        card.classList.add('opacity-0', 'scale-95');
                        setTimeout(() => {
                            overlay.classList.add('hidden');
                            okBtn.onclick = null;
                            cancelBtn.onclick = null;
                            inputEl.onkeydown = null;
                            resolve(valor);
                        }, 150);
                    };

                    okBtn.onclick = () => cerrar(input ? inputEl.value.trim() : true);
                    cancelBtn.onclick = () => cerrar(null);
                    inputEl.onkeydown = event => {
                        if (event.key === 'Enter') cerrar(inputEl.value.trim());
                        if (event.key === 'Escape') cerrar(null);
                    };
                    overlay.classList.remove('hidden');
                    requestAnimationFrame(() => card.classList.remove('opacity-0', 'scale-95'));
                    if (input) setTimeout(() => inputEl.focus(), 180);
                });
            }

            function mostrarModalElegante(title, message, type='info') {
                const icon = type === 'success' ? 'bi-check-circle-fill' : (type === 'error' ? 'bi-exclamation-circle-fill' : 'bi-info-circle-fill');
                return abrirModalGlobal({ title, message, type, icon, input: false, okText: 'Entendido' });
            }

            function pedirNumeroAsientoElegante(fechaISO) {
                return abrirModalGlobal({
                    title: 'Iniciar nuevo registro',
                    message: `Fecha seleccionada: ${fechaISO}. Ingrese el número de asiento para empezar la redacción.`,
                    type: 'info',
                    icon: 'bi-journal-plus',
                    input: true,
                    inputLabel: 'Número de Asiento',
                    inputPlaceholder: 'Ingrese Número de Asiento',
                    okText: 'Iniciar Redacción',
                    cancelText: 'Cancelar'
                });
            }

            function iniciarNuevoAsientoSeguro(fechaISO, numero) {
                const params = new URLSearchParams({
                    fecha: fechaISO,
                    asiento: numero,
                    modo: 'nuevo'
                });
                window.location.href = `/residencia?${params.toString()}`;
            }

            function continuarBorradorSeguro(fechaISO, numero) {
                if (!fechaISO || !numero) {
                    mostrarModalElegante('Borrador no identificado', 'No se pudo identificar el borrador seleccionado.', 'error');
                    return;
                }
                const params = new URLSearchParams({
                    fecha: fechaISO,
                    asiento: numero,
                    modo: 'continuar'
                });
                window.location.href = `/residencia?${params.toString()}`;
            }

            function textoEstado(asiento, estado) {
                if (estado === 'future') return 'Futuro';
                if (!asiento) return 'Sin registro';
                if (estado === 'sent') return 'Enviado Inspector';
                if (estado === 'signed') return 'Firmado Inspector';
                if (estado === 'draft') return 'Borrador';
                if (estado === 'observed') return 'Observado';
                return 'Pendiente';
            }

            function cambiarMes(delta) {
                mesActivo.setMonth(mesActivo.getMonth() + delta);
                renderDashboardMes();
            }

            function abrirAsientoHistorico(asiento, fechaISO) {
                if (!asiento) return;
                const fecha = fechaISO || asiento.fecha || '';
                if (tieneResidencia(asiento) && tieneSupervision(asiento)) {
                    mostrarSelectorAsientoHistorico(asiento, fecha);
                    return;
                }
                if (tieneSupervision(asiento)) {
                    abrirHistoricoSupervision(asiento, fecha);
                    return;
                }
                abrirHistoricoResidencia(asiento, fecha);
            }

            function abrirHistoricoResidencia(asiento, fecha) {
                const numeroResidencia = asiento.residencia_numero || (tieneResidencia(asiento) ? asiento.numero : '');
                if (numeroResidencia) {
                    continuarBorradorSeguro(fecha, numeroResidencia);
                }
            }

            function abrirHistoricoSupervision(asiento, fecha) {
                const params = new URLSearchParams({ fecha });
                const numeroBase = asiento.residencia_numero || asiento.numero;
                if (numeroBase) params.set('asiento', numeroBase);
                params.set('modo', 'continuar');
                window.location.href = `/inspector?${params.toString()}`;
            }

            function mostrarSelectorAsientoHistorico(asiento, fecha) {
                asientoHistoricoPendiente = { asiento, fecha };
                const texto = document.getElementById('selectorAsientoHistoricoTexto');
                if (texto) texto.textContent = `El día ${fecha} tiene asiento de Residencia y Supervisión. Elija cuál desea abrir para revisar o corregir.`;
                const overlay = document.getElementById('selectorAsientoHistorico');
                const card = document.getElementById('selectorAsientoHistoricoCard');
                overlay.classList.remove('hidden');
                overlay.classList.add('grid');
                requestAnimationFrame(() => card.classList.remove('scale-95', 'opacity-0'));
            }

            function cerrarSelectorAsientoHistorico() {
                const overlay = document.getElementById('selectorAsientoHistorico');
                const card = document.getElementById('selectorAsientoHistoricoCard');
                card.classList.add('scale-95', 'opacity-0');
                setTimeout(() => {
                    overlay.classList.add('hidden');
                    overlay.classList.remove('grid');
                }, 150);
            }

            function abrirHistoricoSeleccionado(tipo) {
                const pendiente = asientoHistoricoPendiente;
                if (!pendiente) return;
                cerrarSelectorAsientoHistorico();
                if (tipo === 'supervision') {
                    abrirHistoricoSupervision(pendiente.asiento, pendiente.fecha);
                    return;
                }
                abrirHistoricoResidencia(pendiente.asiento, pendiente.fecha);
            }

            function irAAsiento(numero, fecha=null) {
                if (fecha) {
                    continuarBorradorSeguro(fecha, numero);
                    return;
                }
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
                const estadoAsiento = normalizarEstado(asiento.estado);
                const actor = estadoAsiento === 'borrador'
                    ? 'Residencia guardó'
                    : (estadoAsiento === 'enviado_inspector' ? 'Residencia envió al Inspector' : 'Inspector firmó');
                    acciones.push({
                        hora: asiento.updated_at ? new Date(asiento.updated_at) : (asiento.fecha ? fechaHoraLocal(asiento.fecha, 18, 30) : new Date()),
                        titulo: `${actor} el Asiento N° ${String(asiento.numero || '').padStart(3, '0')}`,
                        detalle: `Estado actual: ${asiento.estado || '-'} · Avance ${asiento.avance || 0}%`
                    });
                });
                dashboardSeed.observaciones.slice(0, 2).forEach(obs => {
                    acciones.push({
                        hora: obs.created_at ? new Date(obs.created_at) : new Date(),
                        titulo: `Inspector observó el Asiento N° ${String(obs.numero || '').padStart(3, '0')}`,
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

            function prepararAnimacionFlotarAdentro() {
                const elementos = document.querySelectorAll(
                    '.hero-card, .mini-stat, .command-card, .export-card, .primary-action, .timeline-box, .alert-supervision'
                );
                const animables = Array.from(elementos).filter(el =>
                    !el.closest('.chart-wrap') &&
                    !el.classList.contains('chart-wrap') &&
                    !el.querySelector('.chart-wrap')
                );
                animables.forEach(el => el.classList.add('flotar-adentro'));
                const observer = new IntersectionObserver(entries => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            entry.target.classList.add('visible');
                            observer.unobserve(entry.target);
                        }
                    });
                }, { threshold: 0.12 });
                animables.forEach(el => observer.observe(el));
            }

            function exportarRangoPDF() {
                const desde = document.getElementById('exportDesde').value;
                const hasta = document.getElementById('exportHasta').value;
                if (!desde || !hasta) {
                    mostrarModalElegante('Rango incompleto', 'Seleccione fecha Desde y Hasta para exportar el rango.', 'warning');
                    return;
                }
                // Endpoint sugerido para conectar luego:
                // window.location.href = `/cuaderno/export/pdf?desde=${desde}&hasta=${hasta}`;
                mostrarModalElegante('Exportación preparada', `Rango seleccionado: ${desde} al ${hasta}. Falta conectar el endpoint PDF real.`, 'success');
            }

            async function refrescarDashboardSiHayCambios() {
                let cambio = null;
                try {
                    cambio = JSON.parse(localStorage.getItem('samu_dashboard_refresh') || 'null');
                } catch (e) {
                    cambio = null;
                }
                if (!cambio) return;
                const partes = parseFechaLocal(cambio.fecha);
                if (partes) {
                    mesActivo = new Date(partes.year, partes.monthIndex, 1);
                }
                aplicarCambioDashboardLocal(cambio);
                await renderDashboardMes();
                const asientoActual = buscarAsientoPorFecha(cambio.fecha);
                const estadoActual = normalizarEstado(asientoActual?.estado);
                const estadoEsperado = normalizarEstado(cambio.estado);
                if (!asientoActual || estadoActual !== estadoEsperado) {
                    aplicarCambioDashboardLocal(cambio);
                }
                try { localStorage.removeItem('samu_dashboard_refresh'); } catch (e) {}
                const estadoCambio = String(cambio.estado || '').toLowerCase();
                const estado = estadoCambio.includes('firmado') || estadoCambio.includes('cerrado')
                    ? 'Asiento firmado exitosamente'
                    : (estadoCambio.includes('inspector') ? 'Asiento enviado al Inspector' : 'Borrador guardado exitosamente');
                mostrarModalElegante(estado, `El Asiento N° ${String(cambio.numero || '').padStart(3, '0')} ya fue sincronizado en el calendario.`, 'success');
            }

            document.addEventListener('DOMContentLoaded', () => {
                renderDashboardMes();
                renderTimeline();
                prepararAnimacionFlotarAdentro();
                refrescarDashboardSiHayCambios();
                const accionInicial = paramsInicialesPanel.get('abrir');
                if (accionInicial === 'residencia') {
                    setTimeout(() => abrirModalAsientoResidencia(null), 250);
                }
                if (accionInicial === 'inspector') {
                    setTimeout(() => abrirModalAsientoInspector(null), 250);
                }
                document.getElementById('seatEntryModal')?.addEventListener('click', event => {
                    if (event.target.id === 'seatEntryModal') cerrarModalAsiento();
                });
                document.addEventListener('keydown', event => {
                    if (event.key === 'Escape') cerrarModalAsiento();
                });
                window.addEventListener('focus', refrescarDashboardSiHayCambios);
                window.addEventListener('storage', event => {
                    if (event.key === 'samu_dashboard_refresh') refrescarDashboardSiHayCambios();
                });
            });
        </script>
    </body>
    </html>
    """, estadisticas=estadisticas, asientos=asientos, observaciones=observaciones, ultima_observacion=ultima_observacion, conectado=conectado, rol_usuario=rol_usuario, menu_superior=menu_superior, asientos_json=asientos_json, observaciones_json=observaciones_json, historial_json=historial_json, mes_actual_json=mes_actual_json)
