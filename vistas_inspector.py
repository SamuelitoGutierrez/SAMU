from datetime import datetime
import json

from flask import Blueprint, jsonify, redirect, render_template_string, request, session, url_for

from cuaderno_store import (
    extraer_ocurrencias_residencia,
    guardar_asiento_inspector,
    obtener_asiento,
    obtener_asiento_por_fecha,
    obtener_inspector_asiento,
)
from navbar import obtener_navbar


inspector_bp = Blueprint("inspector", __name__)


def _fecha_texto(fecha_iso):
    try:
        fecha = datetime.strptime(str(fecha_iso), "%Y-%m-%d")
    except Exception:
        fecha = datetime.now()
    dias = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO", "DOMINGO"]
    return f"{dias[fecha.weekday()]}, {fecha.strftime('%d/%m/%Y')}"


def _contenido_inspector_dict(asiento_inspector):
    if not asiento_inspector:
        return {}
    try:
        return json.loads(asiento_inspector.get("contenido") or "{}")
    except Exception:
        return {}


@inspector_bp.route("/inspector")
def redactar_asiento_inspector():
    if "usuario_id" not in session:
        return redirect(url_for("login.mostrar_login"))

    fecha_iso = request.args.get("fecha") or datetime.now().strftime("%Y-%m-%d")
    numero = request.args.get("asiento") or request.args.get("numero")
    numero_int = None
    asiento_residencia = None
    if numero:
        try:
            numero_int = int(numero)
            asiento_residencia = obtener_asiento(numero_int)
        except (TypeError, ValueError):
            numero_int = None
    if not asiento_residencia:
        asiento_residencia = obtener_asiento_por_fecha(fecha_iso)
        numero_int = asiento_residencia.get("numero") if asiento_residencia else None

    asiento_inspector = obtener_inspector_asiento(numero=numero_int, fecha=fecha_iso)
    contenido_inspector = _contenido_inspector_dict(asiento_inspector)
    texto_guardado = contenido_inspector.get("texto") or ""
    estado_inspector = asiento_inspector.get("estado") if asiento_inspector else "Borrador"
    numero_inspector = asiento_inspector.get("numero") if asiento_inspector else None
    residencia_numero = numero_int or (asiento_inspector.get("residencia_numero") if asiento_inspector else None)
    ocurrencias = extraer_ocurrencias_residencia(asiento_residencia) if asiento_residencia else ""
    ocurrencias = ocurrencias or "Residencia aún no registró ocurrencias para esta fecha."

    return render_template_string(
        """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Asiento del Inspector de Obra</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">
    <script>
        window.tailwind = window.tailwind || {};
        window.tailwind.config = { corePlugins: { preflight: false } };
    </script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { margin: 0; min-height: 100vh; font-family: Inter, Arial, sans-serif; background: radial-gradient(circle at top left, #e0f2fe, transparent 34%), linear-gradient(135deg, #f8fafc, #eef2ff); color: #0f172a; }
        .inspector-shell { width: min(1180px, calc(100% - 28px)); margin: 28px auto 48px; }
        .float-in { opacity: 0; transform: translateY(18px); animation: floatIn .55s ease forwards; }
        .float-in:nth-child(2) { animation-delay: .08s; }
        .float-in:nth-child(3) { animation-delay: .14s; }
        @keyframes floatIn { to { opacity: 1; transform: translateY(0); } }
        .hero { border-radius: 30px; padding: 26px; background: rgba(255,255,255,.86); box-shadow: 0 24px 70px rgba(15,23,42,.12); border: 1px solid rgba(148,163,184,.24); backdrop-filter: blur(18px); }
        .hero h1 { margin: 0; font-size: clamp(25px, 4vw, 42px); font-weight: 950; letter-spacing: -.04em; }
        .hero p { margin: 8px 0 0; color: #64748b; font-weight: 800; }
        .grid-main { display: grid; grid-template-columns: 380px 1fr; gap: 18px; margin-top: 18px; }
        .card { border-radius: 26px; padding: 22px; background: rgba(255,255,255,.9); border: 1px solid rgba(148,163,184,.24); box-shadow: 0 18px 46px rgba(15,23,42,.1); }
        .card h2 { margin: 0 0 12px; font-size: 16px; font-weight: 950; }
        .ocurrencias { white-space: pre-wrap; color: #075985; font-family: Candara, Calibri, Arial, sans-serif; font-style: italic; font-size: 17px; line-height: 28px; background: #f8fafc; border: 1px dashed #bae6fd; border-radius: 18px; padding: 16px; min-height: 190px; }
        .word-editor { width: 100%; min-height: 470px; resize: vertical; border: 1px solid #cbd5e1; border-radius: 22px; padding: 20px 22px; outline: none; color: #0263a0; background: repeating-linear-gradient(#fff, #fff 27px, #dbeafe 28px); font-family: Candara, Calibri, Arial, sans-serif; font-style: italic; font-size: 17px; line-height: 28px; box-shadow: inset 0 1px 0 rgba(15,23,42,.04); }
        .word-editor:focus { border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37,99,235,.13); }
        .btn-row { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 10px; margin-top: 14px; }
        .btn-modern { border: 0; border-radius: 999px; padding: 13px 18px; font-weight: 950; color: #fff; transition: transform .18s ease, box-shadow .18s ease; }
        .btn-modern:hover { transform: translateY(-1px) scale(1.01); }
        .btn-draft { background: linear-gradient(135deg, #f59e0b, #d97706); box-shadow: 0 12px 24px rgba(217,119,6,.18); }
        .btn-sign { background: linear-gradient(135deg, #16a34a, #047857); box-shadow: 0 12px 24px rgba(4,120,87,.18); }
        .btn-view { display: inline-flex; align-items: center; gap: 8px; text-decoration: none; margin-top: 14px; border-radius: 999px; padding: 12px 16px; color: #fff; font-weight: 950; background: linear-gradient(135deg, #1d4ed8, #312e81); }
        .modal-backdrop-samu { position: fixed; inset: 0; z-index: 2500; display: grid; place-items: center; background: rgba(15,23,42,.72); backdrop-filter: blur(10px); padding: 18px; }
        .modal-card-samu { width: min(440px, 100%); border-radius: 24px; background: #fff; padding: 24px; box-shadow: 0 30px 90px rgba(15,23,42,.28); transform: scale(.95); opacity: 0; transition: all .15s ease; }
        .modal-card-samu.active { transform: scale(1); opacity: 1; }
        @media (max-width: 900px) { .grid-main { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    {{ menu_superior | safe }}
    <main class="inspector-shell">
        <section class="hero float-in">
            <h1>ASIENTO N° {{ numero }} DEL INSPECTOR DE OBRA</h1>
            <p>{{ fecha_texto }} · Estado Inspector: <b id="estadoInspector">{{ estado_inspector }}</b></p>
        </section>

        <section class="grid-main">
            <aside class="card float-in">
                <h2><i class="bi bi-journal-text me-2"></i>Ocurrencias de Residencia del día</h2>
                <div class="ocurrencias">{{ ocurrencias }}</div>
                {% if residencia_numero %}
                <a class="btn-view" href="/cuaderno/asiento/{{ residencia_numero }}" target="_blank" rel="noopener">
                    <i class="bi bi-box-arrow-up-right"></i> Ver asiento completo de Residencia
                </a>
                {% else %}
                <div class="mt-3 rounded-2xl bg-amber-50 p-3 text-sm font-black text-amber-700">
                    Residencia aún no registró asiento para esta fecha. El sistema correlacionará el número automáticamente cuando exista.
                </div>
                {% endif %}
            </aside>

            <section class="card float-in">
                <h2><i class="bi bi-pencil-square me-2"></i>Redacción del Inspector</h2>
                <textarea id="textoInspector" class="word-editor" placeholder="Redacte aquí las observaciones, conformidad, recomendaciones o decisiones del Inspector de Obra...">{{ texto_guardado }}</textarea>
                <div class="btn-row">
                    <button class="btn-modern btn-draft" type="button" onclick="guardarInspector('Borrador')">
                        <i class="bi bi-save2-fill"></i> Guardar Borrador de Inspector
                    </button>
                    <button class="btn-modern btn-sign" type="button" onclick="guardarInspector('Firmado')">
                        <i class="bi bi-pen-fill"></i> Firmar Asiento Definitivo
                    </button>
                </div>
            </section>
        </section>
    </main>

    <div id="samuModal" class="modal-backdrop-samu hidden">
        <div id="samuModalCard" class="modal-card-samu">
            <div id="samuModalIcon" class="mb-3 grid h-12 w-12 place-items-center rounded-2xl bg-blue-50 text-2xl text-blue-600"><i class="bi bi-info-circle-fill"></i></div>
            <h3 id="samuModalTitle" class="m-0 text-xl font-black text-slate-900">Mensaje</h3>
            <p id="samuModalText" class="mb-5 mt-2 text-sm font-bold leading-6 text-slate-600"></p>
            <div class="flex justify-end">
                <button type="button" class="rounded-2xl bg-blue-600 px-4 py-3 text-sm font-black text-white" onclick="cerrarModal()">Continuar</button>
            </div>
        </div>
    </div>

    <script>
        const numeroResidencia = {{ residencia_numero | tojson }};
        const fechaAsiento = {{ fecha_iso | tojson }};

        function abrirModal(titulo, texto, tipo='success') {
            const overlay = document.getElementById('samuModal');
            const card = document.getElementById('samuModalCard');
            const icon = document.getElementById('samuModalIcon');
            document.getElementById('samuModalTitle').textContent = titulo;
            document.getElementById('samuModalText').textContent = texto;
            icon.className = tipo === 'error'
                ? 'mb-3 grid h-12 w-12 place-items-center rounded-2xl bg-red-50 text-2xl text-red-600'
                : 'mb-3 grid h-12 w-12 place-items-center rounded-2xl bg-green-50 text-2xl text-green-600';
            icon.innerHTML = tipo === 'error' ? '<i class="bi bi-exclamation-circle-fill"></i>' : '<i class="bi bi-check-circle-fill"></i>';
            overlay.classList.remove('hidden');
            requestAnimationFrame(() => card.classList.add('active'));
        }

        function cerrarModal() {
            const overlay = document.getElementById('samuModal');
            const card = document.getElementById('samuModalCard');
            card.classList.remove('active');
            setTimeout(() => overlay.classList.add('hidden'), 150);
        }

        async function guardarInspector(estado) {
            const texto = document.getElementById('textoInspector').value.trim();
            if (!texto) {
                abrirModal('Redacción vacía', 'Escriba el asiento del Inspector antes de guardar.', 'error');
                return;
            }
            const resp = await fetch('/inspector/api/asiento', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    numero: numeroResidencia,
                    fecha: fechaAsiento,
                    estado,
                    contenido: { texto }
                })
            });
            const data = await resp.json().catch(() => ({ ok: false, error: 'Respuesta inválida del servidor' }));
            if (!resp.ok || !data.ok) {
                abrirModal('No se pudo guardar', data.error || 'Revise la conexión e intente nuevamente.', 'error');
                return;
            }
            document.getElementById('estadoInspector').textContent = data.estado;
            localStorage.setItem('samu_dashboard_refresh', JSON.stringify({
                numero: data.numero || numeroResidencia,
                fecha: fechaAsiento,
                estado: data.estado === 'Firmado' ? 'Cerrado' : 'Enviado Inspector',
                updated_at: new Date().toISOString()
            }));
            abrirModal(data.estado === 'Firmado' ? 'Asiento firmado definitivamente' : 'Borrador de Inspector guardado', 'El dashboard se actualizará automáticamente.');
            setTimeout(() => { window.location.href = '/cuaderno'; }, 1500);
        }
    </script>
</body>
</html>
        """,
        menu_superior=obtener_navbar(
            es_admin=session.get('es_admin', False),
            nombre_usuario=session.get('nombre_usuario', session.get('nombre', 'Usuario')),
        ),
        numero=f"{int(numero_inspector or (numero_int + 1 if numero_int else 0)):04d}" if (numero_inspector or numero_int) else "PENDIENTE",
        residencia_numero=residencia_numero,
        fecha_iso=fecha_iso,
        fecha_texto=_fecha_texto(fecha_iso),
        ocurrencias=ocurrencias,
        texto_guardado=texto_guardado,
        estado_inspector=estado_inspector,
    )


@inspector_bp.route("/inspector/api/asiento", methods=["POST"])
def api_guardar_inspector():
    if "usuario_id" not in session:
        return jsonify({"ok": False, "error": "No autorizado"}), 401
    data = request.get_json(silent=True) or {}
    numero_raw = data.get("numero")
    numero = None
    if numero_raw not in (None, ""):
        try:
            numero = int(numero_raw)
        except (TypeError, ValueError):
            return jsonify({"ok": False, "error": "Número de asiento inválido"}), 400
    fecha = data.get("fecha") or datetime.now().strftime("%Y-%m-%d")
    contenido = data.get("contenido") or {}
    estado = data.get("estado") or "Borrador"
    resultado = guardar_asiento_inspector(
        numero=numero,
        fecha=fecha,
        estado=estado,
        contenido=contenido,
        usuario=session.get("nombre", "Inspector"),
    )
    return jsonify(resultado), 200 if resultado.get("ok") else 500
