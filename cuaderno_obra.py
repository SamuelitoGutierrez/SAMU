CUADERNO_OBRA_CSS = """
            /* ==========================================
               CUADERNO FISICO / PREVISUALIZACION
               ========================================== */
            .papel-fisico { background: #fdfdfa; width: 100%; min-height: 980px; padding: 30px 46px 34px; box-shadow: 0 18px 45px rgba(15,23,42,0.10); border: 1px solid #e2e8f0; font-family: Arial, sans-serif; color: #000; position: relative; overflow: hidden; display: flex; flex-direction: column; }
            .p-header-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; margin-bottom: 4px; }
            .p-header-side { width: 86px; flex: 0 0 86px; }
            .p-qr-link { width: 62px; display: block; margin-left: auto; text-decoration: none; }
            .p-qr-link img { width: 62px; height: 62px; display: block; object-fit: contain; border: 0; border-radius: 0; padding: 0; background: transparent; }
            .p-title-box { text-align: center; flex: 1; margin-left: 0;}
            .p-title-box h1 { font-size: 28px; font-weight: bold; text-decoration: underline; letter-spacing: 1.5px; margin: 0;}
            .p-num { font-size: 24px; font-weight: bold; }
            .cuaderno-preview-pages { width: 100%; display: grid; gap: 24px; }
            .papel-fisico.hoja-vista-a4 { height: 1123px; min-height: 1123px; max-height: 1123px; }
            .papel-fisico.hoja-vista-a4 .p-body-lines { flex: 0 0 780px; min-height: 780px; max-height: 780px; }
            .papel-fisico.hoja-vista-a4 .pagina-cuaderno { height: 780px; min-height: 780px; max-height: 780px; }
            .p-meta { margin-bottom: 3px; padding-bottom: 4px; border-bottom: 3px solid #000; }
            .p-meta-row { display: flex; align-items: flex-end; gap: 15px; width: 100%; margin-bottom: 2px; }
            .p-meta-field { display: flex; align-items: flex-end; min-width: 0; }
            .p-meta-field.fecha { flex: 0 0 46%; }
            .p-meta-field.modalidad { flex: 1 1 auto; }
            .p-row { display: flex; align-items: flex-end; margin-bottom: 2px; }
            .p-label { font-size: 14px; font-weight: bold; margin-right: 8px; }
            .p-line { flex: 1; border-bottom: 1px solid #000; position: relative; height: 17px; }
            .lapicero-meta { position: absolute; bottom: -1px; left: 10px; font-family: Candara, Calibri, Arial, sans-serif; font-style: italic; color: var(--celeste-obra); font-size: 16px; font-weight: 500; white-space: nowrap; }
            .p-body-lines { position: relative; margin-top: 1px; margin-bottom: 8px; flex: 0 0 780px; min-height: 780px; max-height: 780px; overflow: hidden; }
            .pagina-cuaderno { background-image: repeating-linear-gradient(to bottom, transparent 0, transparent 25px, #cbd5e1 25px, #cbd5e1 26px); background-size: 100% 26px; background-position: top left; line-height: 26px; height: 780px; min-height: 780px; max-height: 780px; padding-top: 0; position: relative; overflow: hidden; display: flex; flex-direction: column; }
            .lapicero { flex: 1 1 auto; min-height: 0; overflow: hidden; display: flex; flex-direction: column; font-family: Candara, Calibri, Arial, sans-serif; font-style: italic; color: var(--celeste-obra); font-size: 17px; line-height: 26px; padding-left: 2px; font-weight: 400; text-align: justify; word-wrap: break-word; overflow-wrap: anywhere; word-break: break-word; }
            .encabezado-asiento { position: relative; margin: 0 0 3px; min-height: 26px; font-family: Candara, Calibri, Arial, sans-serif; font-style: italic; color: var(--celeste-obra); font-size: 16px; line-height: 26px; font-weight: 700; }
            .encabezado-asiento .titulo-asiento { width: 100%; text-align: center; text-transform: uppercase; color: var(--celeste-obra); font-family: Candara, Calibri, Arial, sans-serif; font-style: italic; font-size: 16px; letter-spacing: 0.1px; font-weight: 800; padding: 0 128px 0 8px; white-space: nowrap; }
            .encabezado-asiento.continuacion .titulo-asiento { padding: 0 128px 0 8px; text-align: center; text-transform: none; color: var(--celeste-obra); font-family: Candara, Calibri, Arial, sans-serif; font-style: italic; font-size: 16px; font-weight: 800; }
            .encabezado-asiento .fecha-asiento { position: absolute; top: 0; right: 0; text-align: right; white-space: nowrap; color: var(--celeste-obra); }
            .modulo-redaccion { margin: 0 0 0; }
            .modulo-titulo { display: block; font-weight: 700; color: #075985; }
            .modulo-contenido { display: block; padding-left: 22px; text-indent: 0; white-space: pre-wrap; overflow-wrap: anywhere; word-break: break-word; }
            .personal-bloque { display: block; padding-left: 22px; }
            .personal-subtitulo { display: block; padding-left: 18px; font-weight: 700; line-height: 26px; }
            .personal-gastos-linea { display: block; padding-left: 48px; line-height: 26px; text-align: justify; }
            .personal-costo-fila { display: block; padding-left: 0; line-height: 26px; text-align: center; white-space: pre-wrap; }
            .almacen-bloque { display: block; padding-left: 22px; }
            .almacen-principal { display: block; padding-left: 18px; font-weight: 600; line-height: 26px; }
            .almacen-sub { display: block; padding-left: 48px; line-height: 26px; }
            .almacen-label { color: var(--celeste-obra); font-weight: 800; }
            .almacen-detalle { color: var(--celeste-obra); font-weight: 400; }
            .almacen-espacio { display: block; height: 26px; }
            .maquinaria-bloque { display: block; padding-left: 22px; white-space: normal; }
            .maquinaria-principal { display: block; padding-left: 18px; font-weight: 800; line-height: 26px; }
            .maquinaria-sub { display: block; padding-left: 44px; line-height: 26px; }
            .maquinaria-fila { display: grid; grid-template-columns: 30% 20% 20% 15% 15%; column-gap: 0; padding-left: 44px; line-height: 26px; font-size: 16px; white-space: nowrap; }
            .maquinaria-fila span { min-width: 0; white-space: nowrap; overflow: visible; }
            .van-final { margin-top: auto; display: block; text-align: right; padding-right: 8px; font-weight: 800; color: #075985; }
            .p-footer { display: flex; justify-content: space-between; margin-top: auto; padding-top: 18px; padding-bottom: 8px; font-size: 12px; font-weight: bold; color: #000;}
            .p-sig { border-top: 1px solid #000; width: 28%; text-align: center; padding-top: 5px; }
            .page-counter { position: absolute; right: 14mm; bottom: 5mm; font-size: 9px; font-weight: 600; color: #94a3b8; }
"""

def obtener_cuaderno_obra_html(numero_hoja):
    return f"""
                <div class="cuaderno-preview-pages" id="papelOficial">
                <div class="papel-fisico hoja-vista-a4">
                    <div class="p-header-top">
                        <div class="p-header-side"></div>
                        <div class="p-title-box"><h1>CUADERNO DE OBRA</h1></div>
                        <div class="p-header-side">
                            <a class="p-qr-link" id="qrCuadernoLink" href="/cuaderno" target="_blank" rel="noopener">
                                <img id="qrCuadernoImg" alt="QR para ver PDF del asiento" src="https://api.qrserver.com/v1/create-qr-code/?size=120x120&amp;margin=0&amp;data=/cuaderno" />
                            </a>
                        </div>
                    </div>
                    <div class="p-meta">
                        <div class="p-meta-row">
                            <div class="p-meta-field fecha"><span class="p-label">Fecha:</span><div class="p-line"><span class="lapicero-meta" id="lbl_hoja_fecha">--</span></div></div>
                            <div class="p-meta-field modalidad"><span class="p-label">Modalidad:</span><div class="p-line"><span class="lapicero-meta">Administracion Directa</span></div></div>
                        </div>
                        <div class="p-row"><span class="p-label">Obra:</span><div class="p-line"><span class="lapicero-meta">Mejoramiento de la Carretera Asiruni - Rosaspata</span></div></div>
                        <div class="p-row"><span class="p-label">Proyecto:</span><div class="p-line"><span class="lapicero-meta">Tramo I</span></div></div>
                        <div class="p-row"><span class="p-label">Programa:</span><div class="p-line"><span class="lapicero-meta">-</span></div></div>
                        <div class="p-row"><span class="p-label">Entidad Ejecutora:</span><div class="p-line"><span class="lapicero-meta">Gobierno Regional Puno</span></div></div>
                    </div>

                    <div class="p-body-lines" id="contenedorLineasCuaderno"></div>
                    <div class="p-footer">
                        <div class="p-sig">ING. INSPECTOR</div><div class="p-sig">ING. RESIDENTE</div><div class="p-sig">ING. SUPERVISOR</div>
                    </div>
                </div>
                </div>
"""


CUADERNO_OBRA_JS = """
            // =====================================================================
            // MOTOR DEL CUADERNO DE OBRA POR MODULOS
            // =====================================================================
            function normalizarOracion(texto) {
                return String(texto || '')
                    .replace(/\\s+/g, ' ')
                    .trim();
            }

            function textoMinuscula(texto) {
                return normalizarOracion(texto).toLocaleLowerCase('es-PE');
            }

            function escaparHtml(texto) {
                return String(texto || '')
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;')
                    .replace(/"/g, '&quot;')
                    .replace(/'/g, '&#039;');
            }

            function escaparHtmlConSaltos(texto) {
                return escaparHtml(texto).replace(/\\n/g, '<br>');
            }

            function valor(id) {
                const el = document.getElementById(id);
                return el ? normalizarOracion(el.value) : '';
            }

            function valorConSaltos(id) {
                const el = document.getElementById(id);
                return el ? String(el.value || '').trim() : '';
            }

            function formatoItem(p) {
                const item = p.item && p.item !== '-' ? `${p.item} ` : '';
                const progresiva = p.prog ? ` - ${p.prog}` : '';
                const metrado = p.metrado ? ` = ${p.metrado} ${p.unidad || ''}` : '';
                return normalizarOracion(`${item}${p.descripcion || ''}${progresiva}${metrado}`);
            }

            function listaModulo(nombre) {
                const lista = window[nombre];
                return Array.isArray(lista) ? lista : [];
            }

            function agregarModulo(modulos, titulo, contenido) {
                const texto = String(contenido || '')
                    .split('\\n')
                    .map(linea => normalizarOracion(linea))
                    .filter(Boolean)
                    .join('\\n');
                modulos.push({ titulo, contenido: texto || '-' });
            }

            function agregarModuloConFormato(modulos, titulo, contenido) {
                const texto = String(contenido || '')
                    .split('\\n')
                    .map(linea => String(linea || '').trimEnd())
                    .filter(linea => linea.trim())
                    .join('\\n');
                modulos.push({ titulo, contenido: texto || '-' });
            }

            function cantidadPersonal(cantidad, nombre) {
                return `(${cantidad.toString().padStart(2, '0')}) ${nombre}`;
            }

            function redactarModulosCuaderno() {
                const modulos = [];

                const vJ1 = valor('v_jornal_m');
                const vJ2 = valor('v_jornal_t');
                const vClima = valor('v_clima');
                if (vJ1 || vJ2) {
                    let partes = [];
                    if (vJ1) partes.push(`Mañana: ${vJ1}`);
                    if (vJ2) partes.push(`Tarde: ${vJ2}`);
                    if (vClima) partes.push(`Clima: ${vClima}`);
                    agregarModulo(modulos, '1. Jornal de trabajo', partes.join(', '));
                } else {
                    agregarModulo(modulos, '1. Jornal de trabajo', '');
                }

                const personal = [
                    {k: 'Operario', v: parseInt(valor('v_oper') || 0)},
                    {k: 'Oficiales', v: parseInt(valor('v_ofic') || 0)},
                    {k: 'Peones', v: parseInt(valor('v_peon') || 0)},
                    {k: 'Mecánicos', v: parseInt(valor('v_meca') || 0)},
                    {k: 'Controladores de maquinaria', v: parseInt(valor('v_ctrl') || 0)},
                    {k: 'Operadores de maquinaria', v: parseInt(valor('v_ope_maq') || 0)}
                ].filter(x => x.v > 0);

                const primeraLinea = personal.slice(0, 4).map(x => cantidadPersonal(x.v, x.k)).join('    ');
                const segundaLinea = personal.slice(4).map(x => cantidadPersonal(x.v, x.k)).join('    ');
                const gastos = (window.m2_gastos_generales || []).map(nombre => `(1) ${nombre}`).join(', ');
                agregarModulo(modulos, '2. Personal de obra', [
                    '* Personal de Gastos Generales',
                    gastos || '-',
                    '* Personal de Costo Directo',
                    [primeraLinea, segundaLinea].filter(Boolean).join('\\n') || '-'
                ].join('\\n'));

                const m3 = listaModulo('m3_lista');
                if (m3.length > 0) {
                    agregarModulo(modulos, '3. Partidas ejecutadas', m3.map(formatoItem).join('\\n'));
                } else {
                    agregarModulo(modulos, '3. Partidas ejecutadas', '');
                }

                const m4 = listaModulo('m4_lista');
                if (m4.length > 0) {
                    agregarModulo(modulos, '4. Partidas de mayor metrado', m4.map(formatoItem).join('\\n'));
                } else {
                    agregarModulo(modulos, '4. Partidas de mayor metrado', '');
                }

                const m5 = listaModulo('m5_lista');
                if (m5.length > 0) {
                    agregarModulo(modulos, '5. Sub partidas ejecutadas', m5.map(formatoItem).join('\\n'));
                } else {
                    agregarModulo(modulos, '5. Sub partidas ejecutadas', '');
                }

                const m6 = listaModulo('m6_lista');
                if (m6.length > 0) {
                    agregarModulo(modulos, '6. Actividades ejecutadas', m6.map(formatoItem).join('\\n'));
                } else {
                    agregarModulo(modulos, '6. Actividades ejecutadas', '');
                }

                agregarModulo(modulos, '7. Movimiento de almacén', valorConSaltos('v_almacen'));
                agregarModuloConFormato(modulos, '8. Maquinarias y equipos', valorConSaltos('v_maquina'));
                agregarModulo(modulos, '9. Herramientas manuales', valor('v_herram'));
                agregarModuloConFormato(modulos, '10. Ocurrencias y otros', valorConSaltos('v_ocurrencia'));

                return modulos;
            }

            function encabezadoPagina(asiento, fecha, continuacion=false) {
                const titulo = continuacion
                    ? `. . . viene del ASIENTO N° ${asiento} DEL RESIDENTE DE OBRA`
                    : `ASIENTO N° ${asiento} DEL RESIDENTE DE OBRA`;
                return `
                    <div class="encabezado-asiento ${continuacion ? 'continuacion' : ''}">
                        <div class="titulo-asiento">${escaparHtml(titulo)}</div>
                        <div class="fecha-asiento">${escaparHtml(fecha)}</div>
                    </div>
                `;
            }

            function htmlModulo(modulo) {
                if (modulo.titulo.startsWith('2.')) {
                    return `
                        <div class="modulo-redaccion">
                            <span class="modulo-titulo">${escaparHtml(modulo.titulo)}</span>
                            <div class="personal-bloque">${htmlPersonalObra(modulo.contenido)}</div>
                        </div>
                    `;
                }
                if (modulo.titulo.startsWith('7.')) {
                    return `
                        <div class="modulo-redaccion">
                            <span class="modulo-titulo">${escaparHtml(modulo.titulo)}</span>
                            <div class="almacen-bloque">${htmlAlmacen(modulo.contenido)}</div>
                        </div>
                    `;
                }
                if (modulo.titulo.startsWith('8.')) {
                    return `
                        <div class="modulo-redaccion">
                            <span class="modulo-titulo">${escaparHtml(modulo.titulo)}</span>
                            <div class="maquinaria-bloque">${htmlMaquinaria(modulo.contenido)}</div>
                        </div>
                    `;
                }
                return `
                    <div class="modulo-redaccion">
                        <span class="modulo-titulo">${escaparHtml(modulo.titulo)}</span>
                        <span class="modulo-contenido">${escaparHtmlConSaltos(modulo.contenido)}</span>
                    </div>
                `;
            }

            function htmlAlmacen(texto) {
                if (!texto || texto === '-') return '<span class="modulo-contenido">-</span>';
                
                let categoriaActual = 'materiales';
                const textoConCortes = String(texto)
                    .replace(/\\s+(?=7\\.[12]\\s+Movimiento)/gi, '\\n')
                    .replace(/\\s+(?=7\\.[12]\\.\\d+\\s+(?:Ingreso|Salida):)/gi, '\\n')
                    .replace(/\\s+(?=\\*\\s*Movimiento)/gi, '\\n')
                    .replace(/\\s+(?=-\\s*(?:Ingreso|Salida):)/gi, '\\n');
                const lineas = textoConCortes.split('\\n').map(linea => {
                    const limpia = normalizarOracion(linea);
                    const mayuscula = limpia.toLocaleUpperCase('es-PE');

                    if ((limpia.startsWith('*') || /^7\\.1\\s+/i.test(limpia)) && mayuscula.includes('MATERIALES')) {
                        categoriaActual = 'materiales';
                        return '* Movimiento de materiales de construcción';
                    }

                    if ((limpia.startsWith('*') || /^7\\.2\\s+/i.test(limpia)) && mayuscula.includes('COMBUSTIBLE')) {
                        categoriaActual = 'combustible';
                        return '* Movimiento de combustible.';
                    }

                    const sub = limpia.match(/^(?:-\\s*)?(?:7\\.\\d+\\.\\d+\\s*)?(INGRESO|SALIDA):\\s*(.*)$/i);
                    if (sub) {
                        const etiqueta = sub[1].toLocaleUpperCase('es-PE') === 'INGRESO' ? 'Ingreso' : 'Salida';
                        return `- ${etiqueta}: ${textoMinuscula(sub[2])}`;
                    }

                    return limpia;
                }).filter(Boolean);
                
                return lineas.map((limpia, index) => {
                    const siguiente = lineas[index + 1] || '';
                    const esUltimaLinea = index === lineas.length - 1;
                    
                    const esSubMovimiento = /^-\\s*(Ingreso|Salida):/i.test(limpia);
                    const esCategoria = limpia.startsWith('*');
                    const siguienteEsCategoria = siguiente.startsWith('*');
                    const llevaEspacio = esSubMovimiento ||
                                         (esCategoria && siguienteEsCategoria) ||
                                         esUltimaLinea;
                                         
                    const espacio = llevaEspacio ? '<span class="almacen-espacio"></span>' : '';
                    
                    if (limpia.startsWith('*')) {
                        return `<div class="almacen-principal">${escaparHtml(limpia)}</div>${espacio}`;
                    }

                    const sub = limpia.match(/^(-\\s*(Ingreso|Salida):)(.*)$/i);
                    if (sub) {
                        return `<div class="almacen-sub"><span class="almacen-label">${escaparHtml(sub[1])}</span><span class="almacen-detalle">${escaparHtml(sub[3])}</span></div>${espacio}`;
                    }

                    return `<div class="almacen-sub">${escaparHtml(limpia)}</div>${espacio}`;
                }).join('');
            }

            function htmlPersonalObra(texto) {
                let enCosto = false;
                return String(texto || '-').split('\\n').map(linea => {
                    const limpia = String(linea || '').trim();
                    if (!limpia) return '';
                    if (limpia.startsWith('*')) {
                        enCosto = /costo\\s+directo/i.test(limpia);
                        return `<div class="personal-subtitulo">${escaparHtml(limpia)}</div>`;
                    }
                    if (enCosto && limpia !== '-') return `<div class="personal-costo-fila">${escaparHtml(limpia)}</div>`;
                    return `<div class="personal-gastos-linea">${escaparHtml(limpia)}</div>`;
                }).filter(Boolean).join('');
            }

            function htmlMaquinaria(texto) {
                if (!texto || texto === '-') return '<span class="modulo-contenido">-</span>';

                return String(texto).split('\\n').map(linea => {
                    const cruda = String(linea || '').trimEnd();
                    if (!cruda.trim()) return '';
                    const limpia = cruda.trimStart();

                    if (limpia.startsWith('*')) {
                        return `<div class="maquinaria-principal">${escaparHtml(limpia)}</div>`;
                    }

                    if (limpia.startsWith('-')) {
                        return `<div class="maquinaria-sub">${escaparHtml(limpia)}</div>`;
                    }

                    if (cruda.includes('\\t')) {
                        const cols = cruda.split('\\t').map(col => escaparHtml(col.trim()));
                        while (cols.length < 5) cols.push('');
                        return `<div class="maquinaria-fila"><span>${cols[0]}</span><span>${cols[1]}</span><span>${cols[2]}</span><span>${cols[3]}</span><span>${cols[4]}</span></div>`;
                    }

                    return `<div class="maquinaria-sub">${escaparHtml(cruda)}</div>`;
                }).filter(Boolean).join('');
            }

            function paginaHtml(asiento, fecha, modulos, continuacion=false, van=false) {
                return `
                    <div class="pagina-cuaderno">
                        <div class="lapicero">
                            ${encabezadoPagina(asiento, fecha, continuacion)}
                            ${modulos.map(htmlModulo).join('')}
                            ${van ? '<span class="van-final">van . . .</span>' : ''}
                        </div>
                    </div>
                `;
            }

            function medirPagina(asiento, fecha, modulos, continuacion=false, van=false) {
                const contenedor = document.getElementById('contenedorLineasCuaderno');
                contenedor.innerHTML = paginaHtml(asiento, fecha, modulos, continuacion, van);
                const pagina = contenedor.querySelector('.pagina-cuaderno');
                return pagina ? pagina.scrollHeight : 0;
            }

            function dividirModulo(asiento, fecha, modulo, continuacion, maxHeight) {
                const palabras = modulo.contenido.split(' ');
                let low = 0;
                let high = palabras.length;
                let best = 0;

                while (low <= high) {
                    const mid = Math.floor((low + high) / 2);
                    const parte = { titulo: modulo.titulo, contenido: palabras.slice(0, mid).join(' ') };
                    if (medirPagina(asiento, fecha, [parte], continuacion, true) <= maxHeight) {
                        best = mid;
                        low = mid + 1;
                    } else {
                        high = mid - 1;
                    }
                }

                if (best <= 0) best = Math.min(1, palabras.length);

                return [
                    { titulo: modulo.titulo, contenido: palabras.slice(0, best).join(' ') },
                    { titulo: modulo.titulo, contenido: palabras.slice(best).join(' ') }
                ];
            }

            function construirPaginas(asiento, fecha, modulos) {
                const maxHeight = 780;
                const paginas = [];
                let actual = [];
                let continuacion = false;

                modulos.forEach((moduloOriginal) => {
                    let pendiente = { ...moduloOriginal };

                    while (pendiente && pendiente.contenido) {
                        const prueba = [...actual, pendiente];
                        if (medirPagina(asiento, fecha, prueba, continuacion, false) <= maxHeight) {
                            actual.push(pendiente);
                            pendiente = null;
                            continue;
                        }

                        if (actual.length > 0) {
                            paginas.push({ modulos: actual, continuacion, van: true });
                            actual = [];
                            continuacion = true;
                            continue;
                        }

                        const partes = dividirModulo(asiento, fecha, pendiente, continuacion, maxHeight);
                        paginas.push({ modulos: [partes[0]], continuacion, van: true });
                        pendiente = partes[1].contenido ? partes[1] : null;
                        continuacion = true;
                    }
                });

                paginas.push({ modulos: actual, continuacion, van: false });
                return paginas;
            }

            function sincronizarDatos() {
                if (typeof actualizarStepper === 'function') actualizarStepper();
                const numeroGlobal = typeof g_numAsiento !== 'undefined' ? g_numAsiento : '';
                const fechaGlobal = typeof g_fechaAsiento !== 'undefined' ? g_fechaAsiento : '';
                const numeroActivo = String(numeroGlobal || window.g_numAsiento || '').trim();
                const fechaActiva = String(fechaGlobal || window.g_fechaAsiento || document.getElementById('lbl_hoja_fecha')?.innerText || '').trim();
                if (typeof window.samuCurrentStep === 'number') currentStep = window.samuCurrentStep;
                if (!numeroActivo) return;

                const asiento = numeroActivo.padStart(4, '0');
                const modulos = redactarModulosCuaderno();
                const contenedor = document.getElementById('contenedorLineasCuaderno');
                if (!contenedor) return;

                if (modulos.length === 0) {
                    contenedor.innerHTML = paginaHtml(asiento, fechaActiva, [], false, false);
                    return;
                }

                contenedor.innerHTML = paginaHtml(asiento, fechaActiva, modulos, false, false);
            }

            if (!window.__samuCuadernoAutoSync) {
                window.__samuCuadernoAutoSync = true;
                document.addEventListener('DOMContentLoaded', () => {
                    const form = document.getElementById('formResidencia');
                    if (form) {
                        const sincronizarConPausa = () => {
                            const numeroGlobal = typeof g_numAsiento !== 'undefined' ? g_numAsiento : '';
                            if (!window.g_numAsiento && !numeroGlobal) return;
                            clearTimeout(window.__samuCuadernoTimer);
                            window.__samuCuadernoTimer = setTimeout(sincronizarDatos, 160);
                        };
                        ['input', 'change', 'click'].forEach(evento => {
                            form.addEventListener(evento, sincronizarConPausa);
                        });
                    }
                });
            }
"""