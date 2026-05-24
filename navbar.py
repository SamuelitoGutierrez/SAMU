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
        .nav-link-item { font-size: 12px; color: rgba(0,0,0,0.8); cursor: pointer; text-decoration: none; transition: opacity 0.2s; height: 100%; display: flex; align-items: center; }
        .nav-link-item:hover { opacity: 0.6; }

        /* --- MEGA MENU DESPLEGABLE --- */
        .mega-menu {
            position: fixed; top: var(--nav-height); left: 0; width: 100%;
            background: rgba(255,255,255,0.95); backdrop-filter: blur(30px);
            -webkit-backdrop-filter: blur(30px);
            border-bottom: 1px solid rgba(0,0,0,0.1);
            display: grid; grid-template-rows: 0fr; opacity: 0;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); z-index: 999;
        }
        
        /* ---> DEGRADADO GRIS TRANSPARENTE EN LA PARTE INFERIOR <--- */
        .mega-menu::after {
            content: "";
            position: absolute;
            bottom: 0; left: 0; width: 100%; height: 60px;
            background: linear-gradient(to bottom, rgba(255,255,255,0) 0%, rgba(180,180,190,0.25) 100%);
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
            background: #000; color: #fff; padding: 12px 25px; border-radius: 50px;
            font-size: 13px; transition: 0.4s; opacity: 0; z-index: 2000;
        }
        #lockToast.show { transform: translateX(-50%) translateY(0); opacity: 1; }
    </style>

    <nav class="apple-nav">
        <div class="nav-content">
            <a href="/panel" class="nav-brand">SAMU</a>
            <div class="nav-links">
                <span class="nav-link-item" onmouseover="openMenu('cuaderno')">Cuaderno</span>
                <span class="nav-link-item" onmouseover="openMenu('personal')">Personal</span>
                <span class="nav-link-item" onmouseover="openMenu('equipo')">Equipo</span>
                <span class="nav-link-item" onmouseover="openMenu('almacen')">Almacén</span>
                <span class="nav-link-item" onmouseover="openMenu('avance')">Avance</span>
            </div>
            <div style="font-size: 12px; color: #86868b; display: flex; align-items: center;">
                {NOMBRE_USUARIO} <i class="bi bi-person-circle ms-2" style="font-size: 1.2rem;"></i>
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
                title: "Cuaderno de Obra",
                main: ["Residencia", "Supervisión"],
                sub: ["Análisis de Residencia", "Análisis de Supervisión", "Exportar Partes"]
            },
            personal: {
                title: "Control de Personal",
                main: ["Registro", "Asistencias", "Papeletas"],
                sub: ["Análisis de Personal", "Tareos Diarios", "Seguros SCTR"]
            },
            equipo: {
                title: "Equipo Mecánico",
                main: ["Flota", "Horas Máquina", "Combustible"],
                sub: ["Mantenimiento", "Análisis de Equipo", "México Chico"]
            },
            almacen: {
                title: "Almacén",
                main: ["Materiales", "Stock Combustible"],
                sub: ["Ingresos", "Salidas", "Análisis de Stock"]
            },
            avance: {
                title: "Avance de Obra",
                main: ["Partidas", "Metrados", "Topografía"],
                sub: ["Curva S", "Análisis de Metrados", "Actividades"]
            }
        };

        let timeoutMenu;

        function openMenu(cat) {
            clearTimeout(timeoutMenu);
            const data = menuData[cat];
            const grid = document.getElementById('menuGrid');
            grid.innerHTML = `
                <div class="mega-col" style="width: 300px;">
                    <h5>${data.title}</h5>
                    ${data.main.map(m => `<a href="#" onclick="checkAcceso(event)">${m}</a>`).join('')}
                </div>
                <div class="mega-col mega-sub-col">
                    <h5>Herramientas</h5>
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
    
    # Inyectamos los datos dinámicos de forma segura
    html = html.replace("{NOMBRE_USUARIO}", nombre_usuario).replace("{ADMIN_JS}", admin_js)
    return html
