from flask import Blueprint, render_template_string, session, url_for

from navbar import obtener_navbar


ALMACEN_HTML = """
<style>
    .m7-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-bottom: 18px; }
    .m7-card { border: 1px solid #e2e8f0; background: #ffffff; border-radius: 18px; padding: 18px; cursor: pointer; transition: all 0.25s ease; box-shadow: 0 8px 22px rgba(15, 23, 42, 0.04); }
    .m7-card:hover, .m7-card.active { transform: translateY(-3px); border-color: #0263a0; background: #f0f9ff; box-shadow: 0 16px 34px rgba(2, 99, 160, 0.12); }
    .m7-icon { width: 52px; height: 52px; display: grid; place-items: center; border-radius: 16px; color: #ffffff; font-size: 25px; margin-bottom: 12px; }
    .m7-materiales .m7-icon { background: linear-gradient(135deg, #0369a1, #0ea5e9); }
    .m7-combustible .m7-icon { background: linear-gradient(135deg, #b45309, #f59e0b); }
    .m7-title { font-size: 16px; font-weight: 800; color: #0f172a; line-height: 1.2; margin-bottom: 8px; }
    .m7-desc { font-size: 12px; color: #64748b; line-height: 1.5; margin: 0; }
    .m7-textarea { border-radius: 16px; min-height: 130px; resize: vertical; }
    @media (max-width: 576px) { .m7-grid { grid-template-columns: 1fr; } }
</style>

<div class="step-view" id="step7">
    <div class="step-title">7.- Movimientos de Almacen</div>
    <p class="text-muted small mb-3">Seleccione el tipo de movimiento y describa el control realizado en obra.</p>

    <div class="m7-grid">
        <div class="m7-card m7-materiales" id="m7_card_materiales" onclick="m7_seleccionar('materiales')">
            <div class="m7-icon"><i class="bi bi-bricks"></i></div>
            <div class="m7-title">Movimiento de Materiales de Construccion</div>
            <p class="m7-desc">Entradas, salidas, consumos y control de materiales para frentes de trabajo.</p>
        </div>

        <div class="m7-card m7-combustible" id="m7_card_combustible" onclick="m7_seleccionar('combustible')">
            <div class="m7-icon"><i class="bi bi-fuel-pump-fill"></i></div>
            <div class="m7-title">Movimiento de Combustible</div>
            <p class="m7-desc">Despachos, consumo y trazabilidad de combustible para maquinaria.</p>
        </div>
    </div>

    <textarea class="form-control req-step7 m7-textarea" id="v_almacen" rows="5" placeholder="Detalle el movimiento de almacen realizado..." oninput="sincronizarDatos()"></textarea>
</div>

<script>
    function m7_seleccionar(tipo) {
        const materiales = document.getElementById('m7_card_materiales');
        const combustible = document.getElementById('m7_card_combustible');
        const detalle = document.getElementById('v_almacen');

        materiales.classList.toggle('active', tipo === 'materiales');
        combustible.classList.toggle('active', tipo === 'combustible');

        if (tipo === 'materiales') {
            detalle.value = 'Movimiento de materiales de construccion: ';
        } else {
            detalle.value = 'Movimiento de combustible: ';
        }

        detalle.focus();
        if (typeof sincronizarDatos === 'function') sincronizarDatos();
    }
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
