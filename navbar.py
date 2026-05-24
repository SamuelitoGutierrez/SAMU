# Módulo: navbar.py
# Encargado de renderizar el Mega-Menú superior para cualquier vista de SAMU

def obtener_navbar(es_admin, nombre_usuario):
    admin_js = 'true' if es_admin else 'false'
    
    html = """
    <style>
        :root {
            --apple-bg: #fbfbfd;
            --apple-text: #1d1d1f;
            --apple-gray: #86868b;
            --nav-height: 48px;
        }

        /* --- NAVBAR APPLE (GLASS PRINCIPAL) --- */
        .apple-nav {
            position: fixed; top: 0; width: 100%; height: var(--nav-height);
            background: rgba(255, 255, 255, 0.8); backdrop-filter: saturate(180%) blur(20px);
            -webkit-backdrop-filter: saturate(180%) blur(20px);
            z-index: 1000; border-bottom: 1px solid rgba(0,0,0,0.05);
            display: flex; justify-content: center;
        }
        .nav-content { width: 100%; max-width: 1024px; display: flex; justify-content: space-between; align-items: center; height: 100%; padding: 0 20px; }
        .nav-brand { font-family: 'Bauhaus 93'; font-size: 1.3rem; text-decoration: none; color: #000; letter-spacing: 1px;}
        .nav-links { display: flex; gap: 30px; height: 100%; align-items: center; }
        .nav-link-item { font-size: 12px; color: rgba(0,0,0,0.8); cursor: pointer; text-decoration: none; transition: opacity 0.2s; height: 100%; display: flex; align-items: center; font-weight: 500; }
        .nav-link-item:hover { opacity: 0.6; }

        /* --- MEGA MENU DESPLEGABLE --- */
        .mega-menu {
            position: fixed; top: var(--nav-height); left: 0; width: 100%;
            background: rgba(255,255,255,0.98); backdrop-filter: blur(30px);
            -webkit-backdrop-filter: blur(30px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.04);
            display: grid; grid-template-rows: 0fr; opacity: 0;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); z-index: 999;
        }
        
        /* ---> DEGRADADO GRIS CLARO TRANSPARENTE EN LA PARTE INFERIOR <--- */
        .mega-menu::after {
            content: "";
            position: absolute;
            bottom: 0; left: 0; width: 100%; 
            height: 50px; /* Altura del degradado */
            /* Inicia 100% transparente y termina en un gris claro al 60% de opacidad */
            background: linear-gradient(to bottom, rgba(255,255,255,0) 0%, rgba(210, 210, 215, 0.6) 100%);
            border-bottom: 1px solid rgba(200, 200, 205, 0.4);
            pointer-events: none; 
        }

        .mega-menu.active { grid-template-rows: 1fr; opacity: 1; }
        .mega-content { overflow: hidden; max-width: 1024px; margin: 0 auto; width: 100%; padding: 0 20px; }
        .mega-grid { display: flex; gap: 80px; padding: 40px 0 60px 0; }
        
        .mega-col h5 { font-size: 12px; color: var(--apple-gray); font-weight: 500; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 0.5px;}
        .mega-col a { display: block; font-size: 24px; font-weight: 600; color: #1d1d1f; text-decoration: none; margin-bottom: 10px; transition: color 0.2s; }
        .mega-col a:hover { color: #0066cc; }
        .mega-sub-col a { font-size: 14px; font-weight: 500; margin-bottom: 8px; color: #1d1d1f; }
        .mega-sub-col a:hover { color: #0066cc; }

        /* TOAST LOCK */
        #lockToast {
            position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%) translateY(100px);
            background: #1d1d1f; color: #fff; padding: 12px 25px; border-radius: 50px;
            font-size: 13px; transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1); opacity: 0; z-index: 2000;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        #lockToast.show { transform: translateX(-50%) translateY(0); opacity: 1; }
    </style>

    <nav class="apple-nav">
        <div class="nav-content">
            <a href="/panel" class="nav-brand">SAMU</a>
            <div class="nav-links">
                <span class="nav-link-item" onmouseover="openMenu('cuaderno')">Cuaderno de Obra</span>
                <span class="nav-link-item" onmouseover="openMenu('personal')">Control del Personal</span>
                <span class="nav-link-item" onmouseover="openMenu('equipo')">Equipo Mecánico</span>
                <span class="nav-link-item" onmouseover="openMenu('almacen')">Almacén</span>
                <span class="nav-link-item" onmouseover="openMenu('avance')">Avance de Obra</span>
                <span class="nav-link-item" onmouseover="openMenu('sistema')">Sistema</span>
            </div>
            <div style="font-size: 12px; color: #86868b; display: flex; align-items: center; font-weight: 500;">
                {NOMBRE_USUARIO} <i class="bi bi-person-circle ms-2" style="font-size: 1.3rem; color: #1d1d1f;"></i>
            </div>
        </div>
    </nav>

    <div class="mega-menu" id="megaMenu" onmouseleave="closeMenu()">
        <div class="mega-content">
            <div class="mega-grid" id="menuGrid">
                </div>
        </div>
    </div>

    <div id="lockToast"><i class="bi bi-lock-fill me-2"></i> Acceso restringido.</div>

    <script>
        const esAdmin = {ADMIN_JS};
        const menuData = {
            cuaderno: {
                title: "Módulos de Registro",
                main: ["Residencia", "Supervisión"],
                sub: ["Análisis de Residencia", "Análisis de Supervisión", "Exportar Partes Diarios"]
            },
            personal: {
                title: "Gestión Humana",
                main: ["Registro de Personal", "Personal en Obra", "Asistencias"],
                sub: ["Sistema de Papeletas", "Análisis de Asistencias", "Reporte de Tareos"]
            },
            equipo: {
                title: "Control de Flota",
                main: ["Maquinaria y Vehículos", "Operativos", "Horas Máquina"],
                sub: ["Combustible a Equipo", "Análisis Horas Máquina", "Rendimiento por KM"]
            },
            almacen: {
                title: "Inventario",
                main: ["Materiales Generales", "Combustible Principal"],
                sub: ["Análisis de Stock", "Ingresos y Salidas"]
            },
            avance: {
                title: "Ejecución Técnica",
                main: ["Partidas y Metrados", "Actividades Diarias", "Topografía"],
                sub: ["Análisis de Metrados", "Curva S del Proyecto"]
            },
            sistema: {
                title: "Administración",
                main: ["Gestión de Usuarios", "Roles y Permisos"],
                sub: ["Actividad del Sistema", "Configuración Global"]
            }
        };

        let timeoutMenu;

        function openMenu(cat) {
            clearTimeout(timeoutMenu);
            const data = menuData[cat];
            const grid = document.getElementById('menuGrid');
            grid.innerHTML = `
                <div class="mega-col" style="width: 320px;">
                    <h5>${data.title}</h5>
                    ${data.main.map(m => `<a href="#" onclick="checkAcceso(event)">${m}</a>`).join('')}
                </div>
                <div class="mega-col mega-sub-col">
                    <h5>Herramientas Analíticas</h5>
                    ${data.sub.map(s => `<a href="#" onclick="checkAcceso(event)">${s}</a>`).join('')}
                </div>
            `;
            document.getElementById('megaMenu').classList.add('active');
        }

        function closeMenu() {
            timeoutMenu = setTimeout(() => {
                document.getElementById('megaMenu').classList.remove('active');
            }, 150);
        }

        document.querySelector('.apple-nav').addEventListener('mouseleave', closeMenu);
        document.querySelector('.apple-nav').addEventListener('mouseenter', () => clearTimeout(timeoutMenu));

        function checkAcceso(e) {
            e.preventDefault();
            if (!esAdmin) {
                const toast = document.getElementById('lockToast');
                toast.classList.add('show');
                setTimeout(() => toast.classList.remove('show'), 3000);
            } else {
                alert("Redirigiendo al módulo de SAMU...");
            }
        }
    </script>
    """
    
    html = html.replace("{NOMBRE_USUARIO}", nombre_usuario).replace("{ADMIN_JS}", admin_js)
    return html
