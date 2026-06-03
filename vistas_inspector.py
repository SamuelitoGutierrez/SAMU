from datetime import datetime
import json

from flask import Blueprint, jsonify, redirect, render_template_string, request, session, url_for

from cuaderno_store import (
    extraer_ocurrencias_residencia,
    guardar_asiento_inspector,
    obtener_catalogo_personal_gastos,
    obtener_asiento,
    obtener_asiento_por_fecha,
    obtener_inspector_asiento,
    obtener_personal_supervision_anterior,
)
from mod_01_personal_sup import PERSONAL_SUP_BASE
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
        contenido = json.loads(asiento_inspector.get("contenido") or "{}")
    except Exception:
        contenido = {}
    contenido.setdefault("personal_supervision", asiento_inspector.get("personal_supervision") or [])
    contenido.setdefault("partidas_ejecutadas", asiento_inspector.get("partidas_ejecutadas") or "")
    contenido.setdefault("almacen_ingreso", asiento_inspector.get("almacen_ingreso") or "")
    contenido.setdefault("almacen_salida", asiento_inspector.get("almacen_salida") or "")
    contenido.setdefault("maquinaria", asiento_inspector.get("maquinaria") or "")
    contenido.setdefault("ocurrencias", asiento_inspector.get("ocurrencias") or "")
    return contenido


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
    contenido = _contenido_inspector_dict(asiento_inspector)
    estado_inspector = asiento_inspector.get("estado") if asiento_inspector else "Borrador"
    numero_inspector = asiento_inspector.get("numero") if asiento_inspector else None
    residencia_numero = numero_int or (asiento_inspector.get("residencia_numero") if asiento_inspector else None)
    catalogo_gastos = obtener_catalogo_personal_gastos()
    personal_carry = contenido.get("personal_supervision") or obtener_personal_supervision_anterior(fecha_iso) or PERSONAL_SUP_BASE
    ocurrencias_residencia = extraer_ocurrencias_residencia(asiento_residencia) if asiento_residencia else ""
    ocurrencias_residencia = ocurrencias_residencia or "Residencia aún no registró ocurrencias para esta fecha."
    ocurrencias_supervision = contenido.get("ocurrencias") or "Supervisión/Inspector aún no registró ocurrencias para esta fecha."

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
        .inspector-shell { width: min(1220px, calc(100% - 28px)); margin: 28px auto 48px; }
        .float-in { opacity: 0; transform: translateY(18px); animation: floatIn .55s ease forwards; }
        @keyframes floatIn { to { opacity: 1; transform: translateY(0); } }
        .hero, .card { border-radius: 30px; padding: 24px; background: rgba(255,255,255,.9); box-shadow: 0 24px 70px rgba(15,23,42,.12); border: 1px solid rgba(148,163,184,.24); backdrop-filter: blur(18px); }
        .hero h1 { margin: 0; font-size: clamp(25px, 4vw, 40px); font-weight: 950; letter-spacing: -.04em; }
        .step-tabs { display: flex; gap: 8px; flex-wrap: wrap; margin: 16px 0; }
        .step-tab { border: 0; border-radius: 999px; padding: 10px 13px; font-size: 12px; font-weight: 950; background: #e2e8f0; color: #334155; }
        .step-tab.active { color: #fff; background: linear-gradient(135deg,#2563eb,#0f766e); box-shadow: 0 12px 24px rgba(37,99,235,.18); }
        .grid-main { display: grid; grid-template-columns: 390px 1fr; gap: 18px; }
        .step-panel { display: none; }
        .step-panel.active { display: block; }
        .word-editor { width: 100%; min-height: 420px; resize: vertical; border: 1px solid #cbd5e1; border-radius: 22px; padding: 18px 20px; outline: none; color: #0263a0; background: repeating-linear-gradient(#fff, #fff 27px, #dbeafe 28px); font-family: Candara, Calibri, Arial, sans-serif; font-style: italic; font-size: 17px; line-height: 28px; }
        .word-editor:focus { border-color: #2563eb; box-shadow: 0 0 0 4px rgba(37,99,235,.13); }
        .check-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
        .check-card { display: flex; gap: 9px; align-items: center; border: 1px solid #dbeafe; border-radius: 16px; background: #fff; padding: 11px; font-size: 13px; font-weight: 900; color: #334155; }
        .check-card:has(input:checked) { border-color: #2563eb; background: #eff6ff; color: #1d4ed8; }
        .paper { background: #fdfdfa; border-radius: 24px; padding: 18px; min-height: 520px; box-shadow: inset 0 0 0 1px #e2e8f0; }
        .lapicero { font-family: Candara, Calibri, Arial, sans-serif; font-style: italic; color: #0263a0; font-size: 17px; line-height: 28px; white-space: pre-wrap; }
        .paper-title { text-align: center; font-weight: 950; color: #075985; margin-bottom: 10px; }
        .btn-modern { border: 0; border-radius: 999px; padding: 13px 18px; font-weight: 950; color: #fff; transition: transform .18s ease; }
        .btn-modern:hover { transform: translateY(-1px) scale(1.01); }
        .btn-draft { background: linear-gradient(135deg, #f59e0b, #d97706); }
        .btn-sign { background: linear-gradient(135deg, #16a34a, #047857); }
        .modal-backdrop-samu { position: fixed; inset: 0; z-index: 2500; display: grid; place-items: center; background: rgba(15,23,42,.72); backdrop-filter: blur(10px); padding: 18px; }
        .modal-card-samu { width: min(440px, 100%); border-radius: 24px; background: #fff; padding: 24px; box-shadow: 0 30px 90px rgba(15,23,42,.28); transform: scale(.95); opacity: 0; transition: all .15s ease; }
        .modal-card-samu.active { transform: scale(1); opacity: 1; }
        @media (max-width: 980px) { .grid-main { grid-template-columns: 1fr; } .check-grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    {{ menu_superior | safe }}
    <main class="inspector-shell">
        <section class="hero float-in">
            <h1>ASIENTO N° {{ numero }} DEL INSPECTOR DE OBRA</h1>
            <p class="m-0 mt-2 font-extrabold text-slate-500">{{ fecha_texto }} · Estado: <b id="estadoInspector">{{ estado_inspector }}</b></p>
        </section>

        <div class="step-tabs">
            <button class="step-tab active" data-step="1" onclick="irModuloInspector(1)">1. Personal</button>
            <button class="step-tab" data-step="2" onclick="irModuloInspector(2)">2. Partidas</button>
            <button class="step-tab" data-step="3" onclick="irModuloInspector(3)">3. Almacén</button>
            <button class="step-tab" data-step="4" onclick="irModuloInspector(4)">4. Maquinaria</button>
            <button class="step-tab" data-step="5" onclick="irModuloInspector(5)">5. Ocurrencias</button>
        </div>

        <section class="grid-main">
            <aside class="card float-in">
                <h2 class="m-0 mb-3 text-base font-black"><i class="bi bi-journal-text me-2"></i>Ocurrencias / Observaciones</h2>
                <div class="mb-2 rounded-2xl border border-sky-100 bg-sky-50 p-3 text-sm font-bold text-sky-800 whitespace-pre-wrap">
                    <b>Residencia:</b><br>{{ ocurrencias_residencia }}
                </div>
                <div class="rounded-2xl border border-emerald-100 bg-emerald-50 p-3 text-sm font-bold text-emerald-800 whitespace-pre-wrap">
                    <b>Supervisión / Inspector:</b><br>{{ ocurrencias_supervision }}
                </div>
                {% if residencia_numero %}
                <a class="mt-3 inline-flex rounded-full bg-blue-700 px-4 py-3 text-sm font-black text-white no-underline" href="/cuaderno/asiento/{{ residencia_numero }}" target="_blank" rel="noopener">
                    <i class="bi bi-box-arrow-up-right me-2"></i> Ver asiento completo de Residencia
                </a>
                <a class="mt-3 inline-flex rounded-full bg-slate-900 px-4 py-3 text-sm font-black text-white no-underline" href="/cuaderno/asiento/{{ residencia_numero }}/completo" target="_blank" rel="noopener">
                    <i class="bi bi-journals me-2"></i> Ver hoja completa Residencia + Supervisión
                </a>
                {% endif %}
                <div class="paper mt-4">
                    <div class="paper-title">ASIENTO N° {{ numero }} DEL INSPECTOR DE OBRA</div>
                    <div id="previewInspector" class="lapicero"></div>
                </div>
            </aside>

            <section class="card float-in">
                <div class="step-panel active" id="inspectorStep1">
                    <h2 class="text-lg font-black">1. Personal de Supervisión</h2>
                    <div id="personalSupGrid" class="check-grid"></div>
                </div>
                <div class="step-panel" id="inspectorStep2">
                    <h2 class="text-lg font-black">2. Partidas Ejecutadas</h2>
                    <textarea id="sup_partidas" class="word-editor" placeholder="Describa las partidas ejecutadas..."></textarea>
                </div>
                <div class="step-panel" id="inspectorStep3">
                    <h2 class="text-lg font-black">3. Movimiento de Almacén</h2>
                    <label class="font-black text-slate-600">INGRESO:</label>
                    <textarea id="sup_almacen_ingreso" class="word-editor" style="min-height:190px" placeholder="Ingreso de almacén..."></textarea>
                    <label class="mt-3 block font-black text-slate-600">SALIDA:</label>
                    <textarea id="sup_almacen_salida" class="word-editor" style="min-height:190px" placeholder="Salida de almacén..."></textarea>
                </div>
                <div class="step-panel" id="inspectorStep4">
                    <h2 class="text-lg font-black">4. Maquinaria y/o Equipos</h2>
                    <textarea id="sup_maquinaria" class="word-editor" placeholder="Maquinaria y/o equipos..."></textarea>
                </div>
                <div class="step-panel" id="inspectorStep5">
                    <h2 class="text-lg font-black">5. Ocurrencias y/o Obs</h2>
                    <textarea id="sup_ocurrencias" class="word-editor" placeholder="Ocurrencias y/o observaciones..."></textarea>
                </div>
                <div class="mt-4 flex flex-wrap justify-end gap-2">
                    <button class="btn-modern btn-draft" type="button" onclick="confirmarGuardarInspector()"><i class="bi bi-save2-fill"></i> Guardar como Borrador</button>
                    <button class="btn-modern btn-sign" type="button" onclick="guardarInspector('Firmado')"><i class="bi bi-pen-fill"></i> Firmar Asiento</button>
                </div>
            </section>
        </section>
    </main>

    <div id="samuModal" class="modal-backdrop-samu hidden">
        <div id="samuModalCard" class="modal-card-samu">
            <div id="samuModalIcon" class="mb-3 grid h-12 w-12 place-items-center rounded-2xl bg-blue-50 text-2xl text-blue-600"><i class="bi bi-info-circle-fill"></i></div>
            <h3 id="samuModalTitle" class="m-0 text-xl font-black text-slate-900">Mensaje</h3>
            <p id="samuModalText" class="mb-5 mt-2 text-sm font-bold leading-6 text-slate-600"></p>
            <div class="flex justify-end"><button type="button" class="rounded-2xl bg-blue-600 px-4 py-3 text-sm font-black text-white" onclick="cerrarModal()">Continuar</button></div>
        </div>
    </div>

    <div id="confirmInspectorModal" class="modal-backdrop-samu hidden">
        <div id="confirmInspectorCard" class="modal-card-samu">
            <div class="mb-3 grid h-12 w-12 place-items-center rounded-2xl bg-amber-50 text-2xl text-amber-600"><i class="bi bi-save2-fill"></i></div>
            <h3 class="m-0 text-xl font-black text-slate-900">Guardar borrador</h3>
            <p class="mb-5 mt-2 text-sm font-bold leading-6 text-slate-600">¿Desea guardar el borrador y pasar al resumen del asiento?</p>
            <div class="flex flex-wrap justify-end gap-2">
                <button type="button" class="rounded-2xl bg-slate-100 px-4 py-3 text-sm font-black text-slate-700" onclick="cerrarConfirmInspector()">Cancelar</button>
                <button type="button" class="rounded-2xl bg-amber-500 px-4 py-3 text-sm font-black text-white" onclick="confirmarGuardarInspectorAhora()">Confirmar</button>
            </div>
        </div>
    </div>

    <script>
        const numeroResidencia = {{ residencia_numero | tojson }};
        const fechaAsiento = {{ fecha_iso | tojson }};
        const personalBase = {{ personal_base | tojson }};
        const personalCarry = {{ personal_carry | tojson }};
        const contenidoInicial = {{ contenido_json | safe }};
        const storagePrefix = `inspector_fecha_${fechaAsiento}`;
        const paramsInspector = new URLSearchParams(window.location.search || '');
        const moduloInicialInspector = Math.max(1, Math.min(5, parseInt(paramsInspector.get('paso') || paramsInspector.get('modulo') || '1', 10) || 1));
        const cargarDesdeBase = paramsInspector.get('modo') === 'continuar' || paramsInspector.has('asiento') || paramsInspector.has('numero');

        function keyModulo(id) { return `${storagePrefix}_${id}`; }
        function guardarLocal(id, valor) { localStorage.setItem(keyModulo(id), JSON.stringify(valor)); }
        function leerLocal(id, fallback) {
            if (cargarDesdeBase) return fallback;
            try {
                const raw = localStorage.getItem(keyModulo(id));
                return raw ? JSON.parse(raw) : fallback;
            } catch (e) { return fallback; }
        }
        function personalSeleccionado() {
            return Array.from(document.querySelectorAll('.sup-personal-check:checked')).map(chk => chk.value);
        }
        function textoPersonal(lista) {
            return (lista || []).map(nombre => `(1) ${nombre}`).join(', ');
        }
        function renderPersonal() {
            const seleccion = leerLocal('mod_1', contenidoInicial.personal_supervision || personalCarry || []);
            const unicos = Array.from(new Set([...(personalBase || []), ...(personalCarry || []), ...(seleccion || [])]));
            document.getElementById('personalSupGrid').innerHTML = unicos.map(nombre => `
                <label class="check-card"><input type="checkbox" class="sup-personal-check" value="${nombre.replace(/"/g, '&quot;')}" ${seleccion.includes(nombre) ? 'checked' : ''} onchange="sincronizarInspector()"> <span>${nombre}</span></label>
            `).join('');
        }
        function hidratarFormulario() {
            renderPersonal();
            document.getElementById('sup_partidas').value = leerLocal('mod_2', contenidoInicial.partidas_ejecutadas || '');
            document.getElementById('sup_almacen_ingreso').value = leerLocal('mod_3_ingreso', contenidoInicial.almacen_ingreso || '');
            document.getElementById('sup_almacen_salida').value = leerLocal('mod_3_salida', contenidoInicial.almacen_salida || '');
            document.getElementById('sup_maquinaria').value = leerLocal('mod_4', contenidoInicial.maquinaria || '');
            document.getElementById('sup_ocurrencias').value = leerLocal('mod_5', contenidoInicial.ocurrencias || contenidoInicial.texto || '');
            sincronizarInspector();
        }
        function estadoInspectorActual() {
            return {
                personal_supervision: personalSeleccionado(),
                partidas_ejecutadas: document.getElementById('sup_partidas').value,
                almacen_ingreso: document.getElementById('sup_almacen_ingreso').value,
                almacen_salida: document.getElementById('sup_almacen_salida').value,
                maquinaria: document.getElementById('sup_maquinaria').value,
                ocurrencias: document.getElementById('sup_ocurrencias').value
            };
        }
        function sincronizarInspector() {
            const estado = estadoInspectorActual();
            guardarLocal('mod_1', estado.personal_supervision);
            guardarLocal('mod_2', estado.partidas_ejecutadas);
            guardarLocal('mod_3_ingreso', estado.almacen_ingreso);
            guardarLocal('mod_3_salida', estado.almacen_salida);
            guardarLocal('mod_4', estado.maquinaria);
            guardarLocal('mod_5', estado.ocurrencias);
            document.getElementById('previewInspector').textContent = [
                `1. Personal de Supervisión: ${textoPersonal(estado.personal_supervision) || '-'}`,
                `2. Partidas Ejecutadas:\\n${estado.partidas_ejecutadas || '-'}`,
                `3. Movimiento de Almacén:\\nINGRESO: ${estado.almacen_ingreso || '-'}\\nSALIDA: ${estado.almacen_salida || '-'}`,
                `4. Maquinaria y/o Equipos:\\n${estado.maquinaria || '-'}`,
                `5. Ocurrencias y/o Obs:\\n${estado.ocurrencias || '-'}`
            ].join('\\n\\n');
        }
        function irModuloInspector(step) {
            document.querySelectorAll('.step-tab').forEach(btn => btn.classList.toggle('active', Number(btn.dataset.step) === step));
            document.querySelectorAll('.step-panel').forEach(panel => panel.classList.remove('active'));
            document.getElementById(`inspectorStep${step}`)?.classList.add('active');
            sincronizarInspector();
        }
        function abrirModal(titulo, texto, tipo='success') {
            const overlay = document.getElementById('samuModal');
            const card = document.getElementById('samuModalCard');
            const icon = document.getElementById('samuModalIcon');
            document.getElementById('samuModalTitle').textContent = titulo;
            document.getElementById('samuModalText').textContent = texto;
            icon.className = tipo === 'error' ? 'mb-3 grid h-12 w-12 place-items-center rounded-2xl bg-red-50 text-2xl text-red-600' : 'mb-3 grid h-12 w-12 place-items-center rounded-2xl bg-green-50 text-2xl text-green-600';
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
        function confirmarGuardarInspector() {
            const overlay = document.getElementById('confirmInspectorModal');
            const card = document.getElementById('confirmInspectorCard');
            overlay.classList.remove('hidden');
            requestAnimationFrame(() => card.classList.add('active'));
        }
        function cerrarConfirmInspector() {
            const overlay = document.getElementById('confirmInspectorModal');
            const card = document.getElementById('confirmInspectorCard');
            card.classList.remove('active');
            setTimeout(() => overlay.classList.add('hidden'), 150);
        }
        function confirmarGuardarInspectorAhora() {
            cerrarConfirmInspector();
            guardarInspector('Borrador');
        }
        async function guardarInspector(estado) {
            sincronizarInspector();
            const payload = estadoInspectorActual();
            const resp = await fetch('/inspector/api/asiento', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ numero: numeroResidencia, fecha: fechaAsiento, estado, contenido: payload })
            });
            const data = await resp.json().catch(() => ({ ok: false, error: 'Respuesta inválida del servidor' }));
            if (!resp.ok || !data.ok) {
                abrirModal('No se pudo guardar', data.error || 'Revise la conexión e intente nuevamente.', 'error');
                return;
            }
            document.getElementById('estadoInspector').textContent = data.estado;
            localStorage.setItem('samu_dashboard_refresh', JSON.stringify({ numero: data.numero || numeroResidencia, fecha: fechaAsiento, estado: data.estado === 'firmado_inspector' ? 'Cerrado' : 'Enviado Inspector', tipo: 'Inspector', updated_at: new Date().toISOString() }));
            abrirModal(data.estado === 'firmado_inspector' ? 'Asiento firmado' : 'Borrador guardado', 'Los datos del Inspector fueron guardados correctamente.');
            setTimeout(() => {
                if (estado === 'Borrador' && numeroResidencia) {
                    window.location.href = `/cuaderno/resumen?fecha=${encodeURIComponent(fechaAsiento)}&asiento=${encodeURIComponent(numeroResidencia)}`;
                    return;
                }
                window.location.href = '/cuaderno';
            }, 1500);
        }
        document.addEventListener('DOMContentLoaded', () => {
            hidratarFormulario();
            irModuloInspector(moduloInicialInspector);
            document.querySelectorAll('textarea').forEach(el => el.addEventListener('input', sincronizarInspector));
        });
    </script>
</body>
</html>
        """,
        menu_superior=obtener_navbar(
            es_admin=session.get("es_admin", False),
            nombre_usuario=session.get("nombre_usuario", "Usuario"),
        ),
        numero=f"{int(numero_inspector or (numero_int + 1 if numero_int else 0)):04d}" if (numero_inspector or numero_int) else "PENDIENTE",
        residencia_numero=residencia_numero,
        fecha_iso=fecha_iso,
        fecha_texto=_fecha_texto(fecha_iso),
        ocurrencias_residencia=ocurrencias_residencia,
        ocurrencias_supervision=ocurrencias_supervision,
        estado_inspector=estado_inspector,
        personal_base=list(dict.fromkeys([*PERSONAL_SUP_BASE, *catalogo_gastos])),
        personal_carry=personal_carry,
        contenido_json=json.dumps(contenido, ensure_ascii=False),
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
    resultado = guardar_asiento_inspector(
        numero=numero,
        fecha=fecha,
        estado=data.get("estado") or "Borrador",
        contenido=data.get("contenido") or {},
        usuario=session.get("nombre", "Inspector"),
    )
    return jsonify(resultado), 200 if resultado.get("ok") else 500
