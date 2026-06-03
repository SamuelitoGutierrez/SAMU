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
    .resumen-paper { width: min(210mm, 100%); margin: 0 auto; transform-origin: top center; display: grid; gap: 28px; }
    .resumen-paper .papel-fisico { width: 210mm; height: 297mm; min-height: 297mm; max-height: 297mm; box-sizing: border-box; margin: 0 auto; border-radius: 0; }
    .resumen-zoom { display: flex; align-items: center; gap: 6px; padding: 8px 12px; background: rgba(255,255,255,.78); border-bottom: 1px solid #dbeafe; }
    .resumen-zoom button { border: 0; border-radius: 999px; padding: 7px 11px; font-size: 12px; font-weight: 900; color: #0f172a; background: #e0f2fe; }
    .resumen-zoom span { margin-left: auto; font-size: 11px; font-weight: 900; color: #475569; }
    @media print {
        @page { size: A4; margin: 0; }
        body * { visibility: hidden !important; }
        #resumenCuadernoContenido, #resumenCuadernoContenido * { visibility: visible !important; }
        #resumenCuadernoContenido { position: absolute; left: 0; top: 0; width: 210mm !important; transform: none !important; background: #fff !important; }
        #resumenCuadernoContenido .papel-fisico { position: relative; width: 210mm !important; height: 297mm !important; min-height: 297mm !important; max-height: 297mm !important; box-sizing: border-box !important; padding: 8mm 12mm 9mm !important; margin: 0 !important; box-shadow: none !important; border: none !important; page-break-after: always; break-after: page; display: flex; flex-direction: column; overflow: hidden; background: #fdfdfa !important; }
        #resumenCuadernoContenido .papel-fisico:last-child { page-break-after: auto; break-after: auto; }
        #resumenCuadernoContenido .p-header-top { flex: 0 0 auto; margin-bottom: 2mm !important; }
        #resumenCuadernoContenido .p-header-side { width: 86px !important; flex: 0 0 86px !important; }
        #resumenCuadernoContenido .p-qr-link { width: 62px !important; display: block !important; margin-left: auto !important; text-decoration: none !important; }
        #resumenCuadernoContenido .p-qr-link img { width: 62px !important; height: 62px !important; display: block !important; object-fit: contain !important; border: 0 !important; border-radius: 0 !important; padding: 0 !important; background: transparent !important; }
        #resumenCuadernoContenido .p-qr-link span { display: none !important; }
        #resumenCuadernoContenido .p-meta { flex: 0 0 auto; margin-bottom: 1mm !important; padding-bottom: 1mm !important; }
        #resumenCuadernoContenido .p-body-lines { flex: 0 0 780px !important; min-height: 780px !important; max-height: 780px !important; margin-top: 1px !important; margin-bottom: 2mm !important; overflow: hidden; display: flex; flex-direction: column; }
        #resumenCuadernoContenido .pagina-cuaderno { flex: 0 0 780px !important; width: 100%; height: 780px !important; min-height: 780px !important; max-height: 780px !important; overflow: hidden; background-size: 100% 26px !important; background-position: top left !important; background-image: repeating-linear-gradient(to bottom, transparent 0, transparent 25px, #cbd5e1 25px, #cbd5e1 26px) !important; display: flex; flex-direction: column; }
        #resumenCuadernoContenido .encabezado-asiento.continuacion .titulo-asiento { padding: 0 128px 0 8px !important; text-align: center !important; text-transform: none !important; }
        #resumenCuadernoContenido .encabezado-asiento.continuacion .fecha-asiento { display: block !important; }
        #resumenCuadernoContenido .lapicero { flex: 1 1 auto; min-height: 0; overflow: hidden; display: flex; flex-direction: column; font-size: 17px; line-height: 26px; overflow-wrap: anywhere; word-break: break-word; }
        #resumenCuadernoContenido .modulo-contenido, #resumenCuadernoContenido .almacen-detalle, #resumenCuadernoContenido .maquinaria-bloque { overflow-wrap: anywhere !important; word-break: break-word !important; }
        #resumenCuadernoContenido .van-final { margin-top: auto !important; text-align: right !important; padding-right: 8px !important; }
        #resumenCuadernoContenido .p-footer { flex: 0 0 auto; margin-top: auto !important; padding-top: 5mm !important; padding-bottom: 2mm !important; page-break-inside: avoid; break-inside: avoid; }
        #resumenCuadernoContenido .p-sig { page-break-inside: avoid; break-inside: avoid; }
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
                <small>Vista previa A4 paginada, exactamente como saldrá en PDF.</small>
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
        const destino = document.getElementById('resumenCuadernoContenido');
        if (!destino) return;
        if (typeof window.samuPrepararResumenPDF === 'function') {
            window.samuPrepararResumenPDF();
            return;
        }
        const origen = document.getElementById('papelOficial');
        if (!origen) return;
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
        actualizarResumenCuaderno();
        imprimirResumenEnVentana();
    }

    function imprimirResumenEnVentana() {
        const contenido = document.getElementById('resumenCuadernoContenido');
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
                <title>${nombreArchivoResumen('pdf')}</title>
                <style>
                    @page { size: A4; margin: 0; }
                    html, body { margin: 0; padding: 0; background: #fff; }
                    body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
                    .papel-fisico {
                        position: relative;
                        width: 210mm;
                        height: 297mm;
                        min-height: 297mm;
                        max-height: 297mm;
                        box-sizing: border-box;
                        padding: 8mm 12mm 9mm;
                        margin: 0;
                        page-break-after: always;
                        break-after: page;
                        display: flex;
                        flex-direction: column;
                        overflow: hidden;
                        background: #fdfdfa;
                        border: none;
                        box-shadow: none;
                        font-family: Arial, sans-serif;
                        color: #000;
                    }
                    .papel-fisico:last-child { page-break-after: auto; break-after: auto; }
                    .p-header-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 2mm; flex: 0 0 auto; }
                    .p-header-side { width: 86px; flex: 0 0 86px; }
                    .p-qr-link { width: 62px; display: block; margin-left: auto; text-decoration: none; }
                    .p-qr-link img { width: 62px; height: 62px; display: block; object-fit: contain; border: 0; border-radius: 0; padding: 0; background: transparent; }
                    .p-qr-link span { display: none; }
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
                    .pagina-cuaderno {
                        flex: 0 0 780px;
                        height: 780px;
                        min-height: 780px;
                        max-height: 780px;
                        background-image: repeating-linear-gradient(to bottom, transparent 0, transparent 25px, #cbd5e1 25px, #cbd5e1 26px);
                        overflow: hidden;
                        background-size: 100% 26px;
                        background-position: top left;
                        line-height: 26px;
                        display: flex;
                        flex-direction: column;
                    }
                    .lapicero { flex: 1 1 auto; min-height: 0; overflow: hidden; display: flex; flex-direction: column; font-family: Candara, Calibri, Arial, sans-serif; font-style: italic; color: #0263a0; font-size: 17px; line-height: 26px; padding-left: 2px; font-weight: 400; text-align: justify; word-wrap: break-word; overflow-wrap: anywhere; word-break: break-word; }
                    .encabezado-asiento { position: relative; margin: 0 0 3px; min-height: 26px; font-weight: 700; }
                    .titulo-asiento { width: 100%; text-align: center; text-transform: uppercase; font-weight: 800; padding: 0 128px 0 8px; white-space: nowrap; }
                    .fecha-asiento { position: absolute; top: 0; right: 0; text-align: right; white-space: nowrap; }
                    .encabezado-asiento.continuacion .titulo-asiento { padding: 0 128px 0 8px; text-align: center; text-transform: none; }
                    .encabezado-asiento.continuacion .fecha-asiento { display: block; }
                    .modulo-redaccion { margin: 0; }
                    .modulo-titulo { display: block; font-weight: 700; color: #075985; }
                    .modulo-contenido { display: block; padding-left: 22px; text-indent: 0; white-space: pre-wrap; overflow-wrap: anywhere; word-break: break-word; }
                    .almacen-bloque { display: block; padding-left: 22px; }
                    .almacen-principal { display: block; padding-left: 18px; font-weight: 600; line-height: 26px; }
                    .almacen-sub { display: block; padding-left: 48px; line-height: 26px; }
                    .almacen-label { color: #0263a0; font-weight: 800; }
                    .almacen-detalle { color: #0263a0; font-weight: 400; }
                    .almacen-espacio { display: block; height: 26px; }
                    .maquinaria-bloque { display: block; padding-left: 22px; white-space: normal; }
                    .maquinaria-principal { display: block; padding-left: 18px; font-weight: 800; line-height: 26px; }
                    .maquinaria-sub { display: block; padding-left: 44px; line-height: 26px; }
                    .maquinaria-fila { display: grid; grid-template-columns: 30% 20% 20% 15% 15%; column-gap: 0; padding-left: 44px; line-height: 26px; font-size: 16px; white-space: nowrap; }
                    .maquinaria-fila span { min-width: 0; white-space: nowrap; overflow: visible; }
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
        setTimeout(() => {
            ventana.print();
        }, 350);
    }
</script>
"""
