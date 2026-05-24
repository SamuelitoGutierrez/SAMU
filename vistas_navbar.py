# vistas_navbar.py
# Aquí va únicamente el HTML/CSS/JS del menú.
# Usará variables como {{ usuario }} para mostrar el nombre.
HTML_NAVBAR = """
<nav class="apple-nav">
    {% for item in menu_items %}
        <a href="{{ item.url }}" class="nav-link">{{ item.label }}</a>
    {% endfor %}
    <span class="user-name">{{ usuario }}</span>
</nav>
"""
