RESUMEN_ASIENTO_HTML = """
<style>
    .resumen-overlay { position: fixed; inset: 0; z-index: 99998; display: none; align-items: center; justify-content: center; padding: 30px; background: rgba(15,23,42,.52); backdrop-filter: blur(14px); }
    .resumen-overlay.active { display: flex; animation: resumenFade .18s ease forwards; }
    .resumen-modal { width: min(1040px, 96vw); max-height: 92vh; overflow: hidden; border-radius: 30px; background: rgba(255,255,255,.96); box-shadow: 0 35px 90px rgba(15,23,42,.34); border: 1px solid rgba(255,255,255,.78); display: grid; grid-template-rows: auto auto 1fr; }
    .resumen-head { display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 18px 22px; background: linear-gradient(135deg, #0f172a, #0263a0); color: #fff; }
    .resumen-head h5 { margin: 0; font-size: 15px; font-weight: 900; letter-spacing: -.2px; }
    .resumen-head small { display: block; margin-top: 3px; color: rgba(255,255,255,.72); font-weight: 700; }
    .resumen-actions { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; justify-content: flex-end; }
    .resumen-btn { border: 0; border-radius: 999px; padding: 9px 14px; font-size: 12px; font-weight: 900; color: #0f172a; background: #fff; }
    .resumen-btn.dark { color: #fff; background: rgba(255,255,255,.14); border: 1px solid rgba(255,255,255,.18); }
    .resumen-btn.pdf { color: #fff; background: linear-gradient(135deg, #991b1b, #ef4444); }
    .resumen-body { overflow: auto; padding: 24px; background: linear-gradient(135deg, #f8fafc, #eff6ff); }
    .resumen-paper { width: min(760px, 100%); margin: 0 auto; transform-origin: top center; }
    .resumen-paper .papel-fisico { margin: 0 auto; }
    .resumen-zoom { display: flex; align-items: center; gap: 6px; padding: 8px 12px; background: rgba(255,255,255,.78); border-bottom: 1px solid #dbeafe; }
    .resumen-zoom button { border: 0; border-radius: 999px; padding: 7px 11px; font-size: 12px; font-weight: 900; color: #0f172a; background: #e0f2fe; }
    .resumen-zoom span { margin-left: auto; font-size: 11px; font-weight: 900; color: #475569; }
    @media print {
        @page { size: A4; margin: 12mm; }
        body * { visibility: hidden !important; }
        #resumenCuadernoContenido, #resumenCuadernoContenido * { visibility: visible !important; }
        #resumenCuadernoContenido { position: absolute; left: 0; top: 0; width: 100% !important; transform: none !important; }
        #resumenCuadernoContenido .papel-fisico { box-shadow: none !important; border: none !important; width: 100% !important; min-height: 270mm !important; padding: 8mm 10mm 10mm !important; page-break-after: always; break-after: page; display: flex; flex-direction: column; }
        #resumenCuadernoContenido .papel-fisico:last-child { page-break-after: auto; break-after: auto; }
        #resumenCuadernoContenido .p-body-lines { flex: 1; }
        #resumenCuadernoContenido .pagina-cuaderno { width: 100%; min-height: 210mm; background-size: auto 26px; }
        #resumenCuadernoContenido .hoja-pdf:not(:first-child) .pagina-cuaderno { min-height: 238mm; }
        #resumenCuadernoContenido .lapicero { font-size: 17px; line-height: 26px; }
        #resumenCuadernoContenido .p-footer { margin-top: auto !important; padding-top: 12mm; }
    }
    @media (max-width: 768px) {
        .resumen-overlay { padding: 8px; align-items: stretch; }
        .resumen-modal { width: 100%; max-height: none; height: 100%; border-radius: 22px; }
        .resumen-head { padding: 14px; align-items: flex-start; flex-direction: column; }
        .resumen-actions { width: 100%; justify-content: flex-end; }
        .resumen-body { padding: 12px; }
        .resumen-paper { width: 100%; overflow-x: auto; }
        .resumen-paper .papel-fisico { min-width: 720px; }
    }
    @keyframes resumenFade { from { opacity: 0; } to { opacity: 1; } }
</style>

<div class="resumen-overlay" id="resumenCuadernoOverlay" onclick="cerrarResumenCuaderno(event)">
    <div class="resumen-modal" onclick="event.stopPropagation()">
        <div class="resumen-head">
            <div>
                <h5><i class="bi bi-journal-text me-2"></i>Resumen final del asiento</h5>
                <small>Vista previa de la hoja asentada, lista para exportar.</small>
            </div>
            <div class="resumen-actions">
                <button type="button" class="resumen-btn dark" onclick="actualizarResumenCuaderno()"><i class="bi bi-arrow-clockwise me-1"></i>Actualizar</button>
                <button type="button" class="resumen-btn pdf" onclick="exportarResumenPDF()"><i class="bi bi-filetype-pdf me-1"></i>PDF</button>
                <button type="button" class="resumen-btn" onclick="cerrarResumenCuaderno()"><i class="bi bi-x-lg me-1"></i>Cerrar</button>
            </div>
        </div>
        <div class="resumen-zoom">
            <button type="button" onclick="zoomResumenCuaderno(-0.1)"><i class="bi bi-zoom-out"></i> Alejar</button>
            <button type="button" onclick="zoomResumenCuaderno(0.1)"><i class="bi bi-zoom-in"></i> Acercar</button>
            <button type="button" onclick="resetZoomResumenCuaderno()">100%</button>
            <span id="resumenZoomLabel">100%</span>
        </div>
        <div class="resumen-body">
            <div class="resumen-paper" id="resumenCuadernoContenido"></div>
        </div>
    </div>
</div>

<script>
    window.resumenCuadernoZoom = window.resumenCuadernoZoom || 1;

    function aplicarZoomResumenCuaderno() {
        const papel = document.getElementById('resumenCuadernoContenido');
        const label = document.getElementById('resumenZoomLabel');
        if (!papel) return;
        papel.style.transform = `scale(${window.resumenCuadernoZoom})`;
        papel.style.width = `${100 / window.resumenCuadernoZoom}%`;
        if (label) label.innerText = `${Math.round(window.resumenCuadernoZoom * 100)}%`;
    }

    function zoomResumenCuaderno(delta) {
        window.resumenCuadernoZoom = Math.max(0.55, Math.min(1.45, window.resumenCuadernoZoom + delta));
        aplicarZoomResumenCuaderno();
    }

    function resetZoomResumenCuaderno() {
        window.resumenCuadernoZoom = 1;
        aplicarZoomResumenCuaderno();
    }

    function actualizarResumenCuaderno() {
        if (typeof window.samuActualizarCuaderno === 'function') window.samuActualizarCuaderno();
        else if (typeof sincronizarDatos === 'function') sincronizarDatos();
        const origen = document.getElementById('papelOficial');
        const destino = document.getElementById('resumenCuadernoContenido');
        if (!origen || !destino) return;
        destino.innerHTML = origen.outerHTML;
        aplicarZoomResumenCuaderno();
    }

    function abrirResumenCuaderno() {
        actualizarResumenCuaderno();
        document.getElementById('resumenCuadernoOverlay').classList.add('active');
    }

    function cerrarResumenCuaderno(event) {
        if (event && event.target && event.target.id !== 'resumenCuadernoOverlay') return;
        document.getElementById('resumenCuadernoOverlay').classList.remove('active');
        if (window.redirigirCuadernoAlCerrarResumen) {
            window.redirigirCuadernoAlCerrarResumen = false;
            window.location.href = '/cuaderno';
        }
    }

    function nombreArchivoResumen(extension) {
        const numero = String(window.g_numAsiento || 'asiento').padStart(4, '0');
        return `cuaderno_obra_${numero}.${extension}`;
    }

    function exportarResumenPDF() {
        if (typeof window.samuPrepararResumenPDF === 'function') window.samuPrepararResumenPDF();
        else actualizarResumenCuaderno();
        window.print();
        setTimeout(actualizarResumenCuaderno, 700);
    }
</script>
"""
