"""Portfolio personal: la página principal de la web (index.html y proyectos/).

La llama build.py con las mismas fichas de contenido/ y borradores/.
Foto opcional: assets/img/foto.jpg. Si no está, se usa un monograma.
"""
import html
import math
from pathlib import Path

E = html.escape
RAIZ = Path(__file__).resolve().parent
CORREO = "nico.sgandurra@gmail.com"
GITHUB = "https://github.com/NicoSgandurra"
LINKEDIN = "https://www.linkedin.com/in/nicosgandurra"

# Orden de la vitrina y de la grilla. Los borradores van siempre al final.
ORDEN = ["simuladores-electricos", "oswald", "neutro-flotante", "pcscanner", "motor-paso-a-paso", "nexxo"]
EN_VITRINA = 5
ROJO, AZUL, VERDE, AMBAR = "#ff7a7a", "#7cb4ff", "#4ade9b", "#fbbf24"
TONOS = {"Sistemas eléctricos": VERDE, "Ingeniería mecánica y térmica": AMBAR, "Software y automatización": AZUL}
# Proyectos con un dibujo propio: en las tarjetas chicas se ve mejor que una captura
ARTES = {"neutro-flotante", "motor-paso-a-paso", "pcscanner", "nexxo", "picocero",
         "rosca-transportadora", "intercambiador-de-calor"}
FASES = [("r", "R", ROJO, 10), ("t", "T", AZUL, 20), ("s", "S", VERDE, 40)]
INICIAL = {"r": "144,0 V", "t": "249,5 V", "s": "288,0 V", "n": "83,2 V"}  # lo que se ve sin JS
FUENTES = ("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600"
           "&family=JetBrains+Mono:wght@400;500&display=swap")
SECCIONES = [("Inicio", "#inicio"), ("Proyectos", "#trabajo"), ("Sobre mí", "#sobre-mi"),
             ("Laboratorio", "#laboratorio"), ("Trayectoria", "#trayectoria"), ("Contacto", "#contacto")]
LUPA = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">'
        '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>')


# ---------------------------------------------------------------- Dibujos
def trazo(puntos, color, ancho=2.0, extra=""):
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in puntos)
    return (f'<polyline points="{d}" fill="none" stroke="{color}" stroke-width="{ancho}" '
            f'stroke-linecap="round" stroke-linejoin="round" {extra}/>')


def circulo(x, y, r, borde="none", relleno="none", ancho=2.0):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" stroke="{borde}" fill="{relleno}" stroke-width="{ancho}"/>'


def rect(x, y, w, h, relleno="none", borde="none", rx=8):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{relleno}" stroke="{borde}"/>'


def arte(slug):
    """Ilustración vectorial para los proyectos que no tienen captura."""
    cx, cy, p = 320, 200, []
    tenue, gris, claro, panel = "#2a2c31", "#3d4046", "#d4d5d9", "#16171a"

    if slug == "neutro-flotante":
        p += [circulo(cx, cy, r, tenue, ancho=1) for r in (50, 100, 150)]
        fin = [(cx + 150 * math.cos(math.radians(a)), cy - 150 * math.sin(math.radians(a))) for a in (0, 120, 240)]
        p.append(trazo(fin + fin[:1], gris, 1.5, 'stroke-dasharray="5 6"'))
        n = (cx + 57, cy - 16)
        for f, c in zip(fin, (ROJO, AZUL, VERDE)):
            p += [trazo([n, f], c, 3.5), circulo(*f, 6, relleno=c)]
        p.append(circulo(*n, 9, relleno=AMBAR))
    elif slug == "motor-paso-a-paso":
        p.append(circulo(cx, cy, 160, tenue))
        for i in range(8):
            a = math.radians(i * 45)
            c = VERDE if i in (1, 5) else gris
            for d in range(5):
                r, b = 106 + d * 11, 0.16
                p.append(trazo([(cx + r * math.cos(a - b), cy + r * math.sin(a - b)),
                                (cx + r * math.cos(a + b), cy + r * math.sin(a + b))], c, 4))
        rotor = [(cx + (84 if i % 2 else 66) * math.cos(i * math.pi / 18),
                  cy + (84 if i % 2 else 66) * math.sin(i * math.pi / 18)) for i in range(37)]
        p += [trazo(rotor, claro, 1.8), circulo(cx, cy, 18, claro, ancho=1.8)]
    elif slug == "pcscanner":
        for i in range(9):
            q, largo = 136 + i * 16, 95 + (i * 37) % 80
            p += [trazo([(q + 56, 120), (q + 56, 80), (q + 56 + (i - 4) * 14, 80 - abs(i - 4) * 8), (q + 56 + (i - 4) * 14, 0)], tenue),
                  trazo([(q + 56, 280), (q + 56, 320), (q + 56 + (i - 4) * 14, 320 + abs(i - 4) * 8), (q + 56 + (i - 4) * 14, 400)], tenue),
                  trazo([(240, q), (240 - largo, q)], tenue), trazo([(400, q), (400 + largo, q)], tenue),
                  circulo(240 - largo, q, 3.5, relleno=gris), circulo(400 + largo, q, 3.5, relleno=gris)]
        p += [rect(240, 120, 160, 160, panel, gris, 16),
              trazo([(285, 170), (315, 200), (285, 230)], VERDE, 6), trazo([(327, 232), (358, 232)], claro, 6)]
    elif slug == "nexxo":
        p += [rect(70, 55, 500, 290, "#111214", tenue, 18), rect(96, 84, 48, 48, "#077451", rx=14),
              trazo([(105, 108), (113, 108), (119, 94), (126, 123), (131, 108), (136, 108)], "#fff", 3.5)]
        for i in range(5):
            p.append(rect(96, 158 + i * 33, 90, 18, "#077451" if i == 1 else panel, rx=9))
        for f in range(4):
            y = 92 + f * 52
            p += [rect(218, y, 190, 38, panel, rx=10), rect(232, y + 14, 70 + f * 17, 9, gris, rx=4)]
        p += [rect(432, 92, 112, 194, panel, rx=12), rect(448, 238, 80, 30, VERDE, rx=15)]
        p += [rect(448, 112 + i * 24, 80 - i * 14, 9, gris, rx=4) for i in range(4)]
    elif slug == "picocero":
        for i in range(24):
            h = 60 + 70 * math.exp(-((i - 7) / 2.5) ** 2) + 190 * math.exp(-((i - 17) / 2.6) ** 2)
            x = 62 + i * 22
            p.append(rect(x, 350 - min(h, 180), 14, min(h, 180), "#24382f" if h <= 180 else VERDE, rx=3))
            if h > 180:
                p.append(rect(x, 350 - h, 14, h - 184, borde=AMBAR, rx=3))
        p.append(trazo([(48, 168), (592, 168)], AMBAR, 1.5, 'stroke-dasharray="6 7"'))
    elif slug == "rosca-transportadora":
        p += [trazo([(50, 160), (50, 285), (590, 285), (590, 160)], gris, 2.5),
              trazo([(30, 200), (610, 200)], tenue, 14)]
        for k in range(7):
            pts = [(70 + k * 72 + t * 72 + 18 * math.sin(t * 6.283), 200 - 74 * math.cos(t * 6.283))
                   for t in [i / 40 for i in range(41)]]
            p.append(trazo(pts, VERDE if k == 3 else claro, 2.2))
    elif slug == "intercambiador-de-calor":
        p += [rect(60, 92, 520, 216, "#111214", gris, 70)]
        for i in range(8):
            y = 124 + i * 22
            p.append(trazo([(100, y), (540, y)], AMBAR if i < 4 else AZUL, 4))
        for i in range(5):
            y = (100, 220) if i % 2 else (180, 300)
            p.append(trazo([(170 + i * 75, y[0]), (170 + i * 75, y[1])], claro, 2.5))
    else:
        for k, c in enumerate((ROJO, AZUL, VERDE)):
            p.append(trazo([(x, 200 + 90 * math.sin(x / 70 + k * 2.094)) for x in range(0, 641, 8)], c, 2.5))

    return ('<svg viewBox="0 0 640 400" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            '<rect width="640" height="400" fill="#0d0e10"/>' + "".join(p) + "</svg>")


def icono(base):
    if (RAIZ / "assets" / "img" / "foto.jpg").exists():
        return f'<div class="icono foto"><img src="{base}assets/img/foto.jpg" alt="Nicolas Sgandurra"></div>'
    return ('<div class="icono"><svg viewBox="0 0 76 76" aria-hidden="true">'
            '<text x="38" y="47" text-anchor="middle" fill="#ededef" font-size="27" font-weight="600" '
            'letter-spacing="-1.5" font-family="Inter, Segoe UI, sans-serif">NS</text>'
            f'<circle cx="57" cy="22" r="3.5" fill="{VERDE}"/></svg></div>')


# ---------------------------------------------------------------- Paleta de comandos
def paleta(fichas, inicio, proyectos, base):
    """Ctrl K: secciones, proyectos y enlaces. Sin JS no se abre, pero nada depende de ella."""
    grupos = [("Ir a", [("#", n, "Sección", f"{inicio}{h}", "") for n, h in SECCIONES])]
    grupos.append(("Proyectos", [("◆", d["titulo"], d["area"].split()[0], f"{proyectos}{d['slug']}.html",
                                  d["area"] + " " + " ".join(d["tecnologias"])) for d in ordenar(fichas)]))
    grupos.append(("Enlaces", [
        ("@", "Copiar correo", "Acción", "copiar", CORREO),
        ("in", "LinkedIn", "Enlace", LINKEDIN, ""),
        ("gh", "GitHub", "Enlace", GITHUB, "código repositorios"),
        ("≡", "Catálogo de fichas", "Enlace", f"{base}catalogo/index.html", "lista todos"),
    ]))
    filas, n = [], 0
    for titulo, items in grupos:
        filas.append(f'<li class="paleta-grupo" role="presentation">{titulo}</li>')
        for glifo, nombre, tipo, destino, extra in items:
            n += 1
            dentro = (f'<span class="glifo" aria-hidden="true">{E(glifo)}</span>'
                      f'<span class="nombre">{E(nombre)}</span><span class="tipo">{E(tipo)}</span>')
            clave = E(f"{nombre} {tipo} {extra}".lower())
            if destino == "copiar":
                filas.append(f'<li role="option" id="op-{n}" data-clave="{clave}"><button type="button" data-copiar="{CORREO}" tabindex="-1">{dentro}</button></li>')
            else:
                filas.append(f'<li role="option" id="op-{n}" data-clave="{clave}"><a href="{E(destino)}" tabindex="-1">{dentro}</a></li>')
    return f"""<dialog class="paleta" id="paleta" aria-label="Buscar en el sitio">
  <div class="paleta-buscar">{LUPA}<input id="paleta-texto" type="text" role="combobox" aria-expanded="true" aria-controls="paleta-lista" aria-autocomplete="list" placeholder="Buscar en el sitio" autocomplete="off" spellcheck="false"></div>
  <ul class="paleta-lista" id="paleta-lista" role="listbox">
    {chr(10).join(filas)}
  </ul>
  <p class="paleta-vacia" hidden>Sin resultados</p>
  <div class="paleta-pie"><span><kbd>↑</kbd><kbd>↓</kbd> moverse</span><span><kbd>Enter</kbd> abrir</span><span><kbd>Esc</kbd> cerrar</span></div>
</dialog>"""


# ---------------------------------------------------------------- Piezas
def pagina(titulo, descripcion, cuerpo, base, fichas, inicio="", proyectos="proyectos/",
           vista_previa=False, scripts=(), clase=""):
    robots = '<meta name="robots" content="noindex">' if vista_previa else ""
    aviso = '<p class="aviso">Vista previa con borradores</p>' if vista_previa else ""
    js = "\n".join(f'<script src="{base}assets/portfolio/{s}.js" defer></script>' for s in ("pagina", *scripts))
    return f"""<!doctype html>
<html lang="es-AR" class="sin-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(titulo)}</title>
<meta name="description" content="{E(descripcion)}">
<meta name="theme-color" content="#08090a">
<meta property="og:title" content="{E(titulo)}">
<meta property="og:description" content="{E(descripcion)}">
<meta property="og:type" content="website">
{robots}
<link rel="icon" href="{base}assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{E(FUENTES)}">
<link rel="stylesheet" href="{base}assets/portfolio/portfolio.css">
{js}
</head>
<body class="{clase}">
<a class="saltar" href="#contenido">Saltar al contenido</a>
{aviso}
<header class="nav">
  <a class="firma" href="{inicio or '#inicio'}"><img src="{base}assets/favicon.svg" alt=""><span>Nicolas Sgandurra</span></a>
  <nav aria-label="Principal"><ul>
    <li><a href="{inicio}#trabajo">Proyectos</a></li>
    <li class="opcional"><a href="{inicio}#sobre-mi">Sobre mí</a></li>
    <li class="opcional"><a href="{inicio}#laboratorio">Laboratorio</a></li>
    <li class="opcional"><a href="{inicio}#trayectoria">Trayectoria</a></li>
    <li><a href="{inicio}#contacto">Contacto</a></li>
  </ul></nav>
  <button class="buscar" type="button" data-paleta aria-haspopup="dialog" aria-label="Abrir el buscador del sitio"><span class="solo-escritorio">Buscar</span><span class="solo-movil">Menú</span><kbd data-atajo>Ctrl K</kbd></button>
</header>
{cuerpo}
{paleta(fichas, inicio, proyectos, base)}
</body>
</html>
"""


def tono(d):
    return TONOS.get(d["area"], "#b49cff")


def ordenar(fichas):
    pos = {s: i for i, s in enumerate(ORDEN)}
    return sorted(fichas, key=lambda d: (d["borrador"], pos.get(d["slug"], len(ORDEN)), d["orden"], d["titulo"]))


def captura(d, base, carga="lazy"):
    """Captura dentro de una ventanita, apoyada sobre un fondo del color del área."""
    clase = ' class="figura"' if d["slug"].startswith("dlr") else ""
    return ('<div class="captura"><div class="captura-barra" aria-hidden="true"><i></i><i></i><i></i></div>'
            f'<img{clase} src="{base}assets/img/{E(d["imagen"])}" alt="" loading="{carga}"></div>')


def marco(d, base, chico=False, carga="lazy"):
    if d.get("imagen") and not (chico and d["slug"] in ARTES):
        dentro, clase = captura(d, base, carga), "marco con-captura"
    else:
        dentro, clase = arte(d["slug"]), "marco"
    return f'<div class="{clase}" style="--tono:{tono(d)}">{dentro}{sello(d)}</div>'


def sello(d):
    return '<span class="sello">Borrador</span>' if d["borrador"] else ""


def chips(lista):
    return '<ul class="chips">' + "".join(f"<li>{E(t)}</li>" for t in lista) + "</ul>"


def sigla(d):
    return f'<span class="sigla" style="--tono:{tono(d)}" aria-hidden="true">{E(d["sigla"])}</span>'


def vitrina(lista, total, base):
    """La ventana de la portada: lista de proyectos a la izquierda y vista previa a la derecha.
    Sin JS se ve el primero y cada fila es un enlace a su ficha."""
    filas, vistas = [], []
    for i, d in enumerate(lista):
        actual = ' aria-current="true"' if i == 0 else ""
        filas.append(f"""        <li><a class="item" href="proyectos/{d['slug']}.html" data-i="{i}"{actual}>{sigla(d)}<span class="item-texto"><span class="item-titulo">{E(d['titulo'])}</span><span class="item-area">{E(d['area'])}</span></span><kbd class="item-abrir" aria-hidden="true">↵</kbd></a></li>""")
        vistas.append(f"""        <div class="vista" data-i="{i}"{'' if i == 0 else ' hidden'}>
          {marco(d, base, carga="eager")}
          <div class="vista-texto"><h3>{E(d['titulo'])}</h3><p>{E(d['resumen'])}</p>{chips(d['tecnologias'][:4])}</div>
        </div>""")
    return f"""<div class="vitrina aparece" data-vitrina>
    <div class="vitrina-barra">
      <button class="vitrina-buscar" type="button" data-paleta aria-haspopup="dialog">{LUPA}<span>Buscar proyectos, secciones y enlaces</span><kbd data-atajo>Ctrl K</kbd></button>
    </div>
    <div class="vitrina-cuerpo">
      <div class="vitrina-lado">
        <p class="vitrina-grupo">Proyectos</p>
        <ul class="vitrina-lista">
{chr(10).join(filas)}
        </ul>
      </div>
      <div class="vitrina-vista">
{chr(10).join(vistas)}
      </div>
    </div>
    <div class="vitrina-pie"><a href="#trabajo">Ver los {total} proyectos</a><span class="atajos"><kbd>↑</kbd><kbd>↓</kbd> recorrer <kbd>Enter</kbd> abrir</span></div>
  </div>"""


def tarjeta_proyecto(d, base, clase):
    chico = "chica" in clase
    return f"""    <a class="tarjeta proyecto {clase} aparece" href="proyectos/{d['slug']}.html">
      {marco(d, base, chico)}
      <div class="texto">
        <span class="area"><i style="--tono:{tono(d)}"></i>{E(d['area'])}</span>
        <h3>{E(d['titulo'])}</h3>
        <p>{E(d['resumen'])}</p>
        {chips(d['tecnologias'][:3 if chico else 4])}
      </div>
      <span class="ir" aria-hidden="true">→</span>
    </a>"""


def clases(n):
    """Dos grandes arriba y el resto de a tres. Las sueltas del final se estiran para no dejar huecos."""
    c = ["grande"] * min(2, n) + ["chica"] * max(0, n - 2)
    if n == 1:
        c[0] += " sola"
    resto = n - 2
    if resto > 0:
        if resto % 3 == 1:
            c[-1] += " fin-1"
        elif resto % 3 == 2:
            c[-1] += " fin-2"
            c[-2] += " fin-2"
        if resto % 2:
            c[-1] += " impar"
    return c


def laboratorio():
    vert = [(130 * math.cos(math.radians(a)), -130 * math.sin(math.radians(a))) for a in (0, 120, 240)]
    dibujo = [circulo(0, 0, r, "rgba(255,255,255,.09)", ancho=1) for r in (65, 130)]
    dibujo.append(trazo(vert + vert[:1], "rgba(255,255,255,.14)", 1, 'stroke-dasharray="4 5"'))
    filas = []
    for (i, letra, color, ohm), (x, y) in zip(FASES, vert):
        dibujo += [f'<line id="fasor-{i}" x1="0" y1="0" x2="{x:.1f}" y2="{y:.1f}" stroke="{color}"/>',
                   circulo(x, y, 4.5, relleno=color),
                   f'<text x="{x * 1.17:.1f}" y="{y * 1.17 + 5:.1f}" text-anchor="middle">{letra}</text>']
        filas.append(f"""        <div class="fase" style="--color-fase:{color}">
          <label for="carga-{i}">Fase {letra}, <span id="ohm-{i}">{ohm} Ω</span></label>
          <output id="u-{i}">{INICIAL[i]}</output>
          <input id="carga-{i}" type="range" min="5" max="100" value="{ohm}">
        </div>""")
    dibujo.append(f'<circle id="punto-n" cx="0" cy="0" r="6.5" fill="{AMBAR}"/>')
    return f"""<section class="bloque laboratorio" id="laboratorio">
  <p class="etiqueta">Laboratorio</p>
  <h2>¿Qué pasa si se corta el neutro?</h2>
  <p class="entrada">Es un tema que doy en clase y se entiende mejor jugando. Cambiá las cargas y mirá cómo se corre el neutro: unas fases quedan con tensión de más y otras de menos.</p>
  <div class="tarjeta ventana aparece">
    <div class="ventana-barra"><div class="puntos" aria-hidden="true"><i></i><i></i><i></i></div><span>Neutro flotante · teorema de Millman</span><div class="relleno"></div></div>
    <div class="banco" id="lab-neutro">
      <div class="fasores-caja"><svg class="fasores" viewBox="-170 -170 340 340" role="img" aria-label="Diagrama fasorial de las tres fases y el punto neutro">{''.join(dibujo)}</svg></div>
      <div class="controles">
{chr(10).join(filas)}
        <label class="interruptor" for="corte"><input id="corte" type="checkbox" checked> Neutro cortado</label>
        <p class="nota">Desplazamiento del neutro: <output id="u-n">{INICIAL["n"]}</output>. Fuente ideal de 220 V por fase y cargas resistivas.</p>
      </div>
    </div>
  </div>
</section>"""


def portada(fichas, base, vista_previa):
    todas = ordenar(fichas)
    grilla = "\n".join(tarjeta_proyecto(d, base, c) for d, c in zip(todas, clases(len(todas))))
    return pagina(
        "Nicolas Sgandurra | Proyectos",
        "Técnico electricista, docente y estudiante de Ingeniería Electromecánica. Simuladores y software para ingeniería.",
        f"""<section class="portada" id="inicio">
  <a class="estado" href="#laboratorio"><span class="estado-marca">Laboratorio</span><span>Probá el simulador<span class="extra"> de neutro flotante</span></span><span class="estado-flecha" aria-hidden="true">→</span></a>
  <h1>Nicolas Sgandurra</h1>
  <p class="lema">Técnico electricista y docente de Circuitos Eléctricos. Estudio Ingeniería Electromecánica en la UTN San Rafael y programo simuladores y software a medida.</p>
  <div class="botones">
    <a class="boton lleno" href="#trabajo">Ver proyectos</a>
    <a class="boton" href="#contacto">Contacto</a>
  </div>
  {vitrina(todas[:EN_VITRINA], len(todas), base)}
</section>

<main id="contenido">
<section class="bloque" id="trabajo">
  <div class="cabeza">
    <div>
      <p class="etiqueta">Proyectos</p>
      <h2>Lo que vengo haciendo</h2>
      <p class="entrada">Cada ficha cuenta el problema, qué hice y hasta dónde llega.</p>
    </div>
    <a class="enlace" href="{base}catalogo/index.html">Catálogo completo</a>
  </div>
  <div class="proyectos">
{grilla}
  </div>
</section>

<section class="bloque" id="sobre-mi">
  <div class="sobre">
    <div class="aparece">
      <p class="etiqueta">Sobre mí</p>
      <h2>Hola, soy Nico.</h2>
      <p>Me recibí de técnico electricista en 2020 y al año siguiente volví a la misma escuela, como docente de Circuitos Eléctricos. En paralelo curso Ingeniería Electromecánica en la UTN San Rafael.</p>
      <p>Cuando un tema cuesta explicarlo en el pizarrón, le hago un simulador; si un cálculo se repite mucho, lo programo. En el software a medida empiezo por sentarme con quien lo va a usar, para ver cómo trabaja.</p>
    </div>
    <aside class="tarjeta perfil aparece">
      <div class="perfil-cabeza">
        {icono(base)}
        <div><p class="perfil-nombre">Nicolas Sgandurra</p><p class="perfil-rol">Técnico electricista y docente</p></div>
      </div>
      <dl>
        <div><dt>Dónde</dt><dd>San Rafael, Mendoza, Argentina</dd></div>
        <div><dt>Estudios</dt><dd>Ingeniería Electromecánica, UTN San Rafael</dd></div>
        <div><dt>Docencia</dt><dd>Circuitos Eléctricos 1 y 2, desde 2021</dd></div>
        <div><dt>Idiomas</dt><dd>Español nativo, inglés intermedio</dd></div>
      </dl>
    </aside>
  </div>
</section>

{laboratorio()}

<section class="bloque" id="trayectoria">
  <p class="etiqueta">Trayectoria</p>
  <h2>El recorrido</h2>
  <div class="recorrido">
    <ol class="camino">
      <li class="aparece"><time>2017</time><div><h3>Tec.Nito</h3><p>Empiezo a trabajar por mi cuenta en reparación de equipos, redes y armado de workstations. Lo sigo haciendo.</p></div></li>
      <li class="aparece"><time>2020</time><div><h3>Técnico electricista</h3><p>Escuela 4-124 Reynaldo Merín.</p></div></li>
      <li class="aparece"><time>2021</time><div><h3>Ingeniería y docencia</h3><p>Entro a Ingeniería Electromecánica en la UTN San Rafael y empiezo a dar Circuitos Eléctricos 1 y 2 en la escuela donde me recibí.</p></div></li>
      <li class="aparece"><time>2022</time><div><h3>Tecnicatura Universitaria en Programación</h3><p>Cursada completa entre 2022 y 2024.</p></div></li>
      <li class="aparece"><time>2026</time><div><h3>Software a medida</h3><p>Desarrollo un sistema de gestión para un comercio, que ya funciona en paralelo con el anterior. Termino de cursar la carrera.</p></div></li>
    </ol>
    <div class="herramientas aparece">
      <div class="tarjeta"><h3>Ingeniería</h3>{chips(["Mathcad", "AutoCAD", "Autodesk Inventor", "Excel"])}</div>
      <div class="tarjeta"><h3>Programación</h3>{chips(["Python", "JavaScript", "TypeScript", "React", "FastAPI", "PostgreSQL"])}</div>
      <div class="tarjeta"><h3>Herramientas</h3>{chips(["Git", "GitHub", "Arduino", "PowerShell"])}</div>
    </div>
  </div>
</section>

<section class="bloque contacto" id="contacto">
  <div class="tarjeta llamado aparece">
    <p class="etiqueta">Contacto</p>
    <h2>Hablemos</h2>
    <p>Si querés saber más de algún proyecto o tenés una propuesta, escribime.</p>
    <div class="botones">
      <a class="boton lleno correo" href="mailto:{CORREO}">{CORREO}</a>
      <button class="boton" type="button" data-copiar="{CORREO}" hidden>Copiar</button>
    </div>
    <div class="redes"><a href="{LINKEDIN}">LinkedIn</a><a href="{GITHUB}">GitHub</a></div>
  </div>
</section>
</main>

{pie(base)}""",
        base, fichas, vista_previa=vista_previa)


def pie(base, inicio=""):
    return f"""<footer class="pie">
  <span>© 2026 Nicolas Leonel Sgandurra · San Rafael, Mendoza</span>
  <nav aria-label="Enlaces del pie"><a href="{GITHUB}">GitHub</a><a href="{LINKEDIN}">LinkedIn</a><a href="{base}catalogo/index.html">Catálogo</a></nav>
</footer>"""


def ficha(d, base, fichas, vista_previa):
    datos = [("Estado", d["estado"]), ("Autoría", d["autoria"]), ("Herramientas", ", ".join(d["tecnologias"]))]
    meta = "".join(f"<div><dt>{k}</dt><dd>{E(v)}</dd></div>" for k, v in datos)
    partes = [f'<dl class="tarjeta datos">{meta}</dl>']
    if d.get("imagen"):
        clase = ' class="figura"' if d["slug"].startswith("dlr") else ""
        partes.append(f'<figure class="tarjeta"><img{clase} src="{base}assets/img/{E(d["imagen"])}" alt="{E(d["pie"])}">'
                      f'<figcaption>{E(d["pie"])}</figcaption></figure>')
    else:
        partes.append(f'<figure class="tarjeta">{arte(d["slug"])}</figure>')
    partes += ["<h2>Problema</h2>", f"<p>{E(d['problema'])}</p>", "<h2>Qué hice</h2>",
               "<ul>" + "".join(f"<li>{E(x)}</li>" for x in d["trabajo"]) + "</ul>"]
    if d.get("resultados"):
        filas = "".join(f'<tr><th scope="row">{E(k)}</th><td>{E(v)}</td></tr>' for k, v in d["resultados"])
        partes += ["<h2>Resultados</h2>", f"<table>{filas}</table>"]
    if d.get("limites"):
        partes += ["<h2>Límites</h2>", "<ul>" + "".join(f"<li>{E(x)}</li>" for x in d["limites"]) + "</ul>"]
    if d.get("enlaces"):
        botones = "".join(f'<a class="boton" href="{E(u)}">{E(t)}</a>' for t, u in d["enlaces"])
        partes.append(f'<div class="botones">{botones}</div>')
    aviso = f'<p class="pendiente">Antes de publicar: {E(d["pendiente"])}</p>' if d["borrador"] else ""
    cuerpo = f"""<main id="contenido">
<header class="cabecera-ficha">
  <a class="volver" href="../index.html#trabajo">Volver a los proyectos</a>
  <p class="area">{E(d['area'])}</p>
  <h1>{E(d['titulo'])}</h1>
  <p class="bajada">{E(d['resumen'])}</p>
  {aviso}
</header>
<article class="cuerpo-ficha">
  {''.join(partes)}
</article>
</main>
{pie(base)}"""
    return pagina(f"{d['titulo']} | Nicolas Sgandurra", d["resumen"], cuerpo, base, fichas,
                  inicio="../index.html", proyectos="", vista_previa=vista_previa, clase="interior")


def generar(destino, fichas, vista_previa=False):
    salida = destino
    proyectos = salida / "proyectos"
    proyectos.mkdir(parents=True, exist_ok=True)
    for viejo in proyectos.glob("*.html"):
        viejo.unlink()
    (salida / "index.html").write_text(portada(fichas, "", vista_previa), encoding="utf-8")
    for d in fichas:
        (proyectos / f"{d['slug']}.html").write_text(ficha(d, "../", fichas, vista_previa), encoding="utf-8")
