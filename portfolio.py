"""Versión portfolio personal de la web (portfolio/).

La llama build.py con las mismas fichas de contenido/ y borradores/.
Foto opcional: assets/img/foto.jpg. Si no está, se dibuja un diagrama fasorial.
"""
import html
import math
from pathlib import Path

E = html.escape
RAIZ = Path(__file__).resolve().parent
CORREO = "nico.sgandurra@gmail.com"
GITHUB = "https://github.com/NicoSgandurra"
LINKEDIN = "https://www.linkedin.com/in/nicosgandurra"

# Los que van en grande, en este orden. El resto va en la grilla de abajo.
DESTACADOS = ["dlr-linea-132kv", "nexxo", "simuladores-electricos", "oswald"]
FASES = [("r", "R", "#ff8b70", 10), ("t", "T", "#79b8f2", 20), ("s", "S", "#82ebc4", 40)]
INICIAL = {"r": "144,0 V", "t": "249,5 V", "s": "288,0 V", "n": "83,2 V"}  # lo que se ve sin JS
FUENTES = ("https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600"
           "&family=IBM+Plex+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&display=swap")


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
    menta, cobre, tenue = "#82ebc4", "#f0b96e", "#2b5446"

    if slug == "neutro-flotante":
        p += [circulo(cx, cy, r, tenue, ancho=1) for r in (50, 100, 150)]
        fin = [(cx + 150 * math.cos(math.radians(a)), cy - 150 * math.sin(math.radians(a))) for a in (0, 120, 240)]
        p.append(trazo(fin + fin[:1], tenue, 1.5))
        n = (cx + 57, cy - 16)
        for f, c in zip(fin, ("#ff8b70", "#79b8f2", menta)):
            p += [trazo([n, f], c, 4), circulo(*f, 7, relleno=c)]
        p.append(circulo(*n, 10, relleno=cobre))
    elif slug == "motor-paso-a-paso":
        p.append(circulo(cx, cy, 160, tenue))
        for i in range(8):
            a = math.radians(i * 45)
            c = cobre if i in (1, 5) else tenue
            for d in range(5):
                r, b = 106 + d * 11, 0.16
                p.append(trazo([(cx + r * math.cos(a - b), cy + r * math.sin(a - b)),
                                (cx + r * math.cos(a + b), cy + r * math.sin(a + b))], c, 5))
        rotor = [(cx + (84 if i % 2 else 66) * math.cos(i * math.pi / 18),
                  cy + (84 if i % 2 else 66) * math.sin(i * math.pi / 18)) for i in range(37)]
        p += [trazo(rotor, menta), circulo(cx, cy, 18, menta)]
    elif slug == "pcscanner":
        for i in range(9):
            q, largo = 136 + i * 16, 95 + (i * 37) % 80
            p += [trazo([(q + 56, 120), (q + 56, 80), (q + 56 + (i - 4) * 14, 80 - abs(i - 4) * 8), (q + 56 + (i - 4) * 14, 0)], tenue),
                  trazo([(q + 56, 280), (q + 56, 320), (q + 56 + (i - 4) * 14, 320 + abs(i - 4) * 8), (q + 56 + (i - 4) * 14, 400)], tenue),
                  trazo([(240, q), (240 - largo, q)], tenue), trazo([(400, q), (400 + largo, q)], tenue),
                  circulo(240 - largo, q, 4, relleno=cobre), circulo(400 + largo, q, 4, relleno=cobre)]
        p += [rect(240, 120, 160, 160, "#103029", menta),
              trazo([(285, 170), (315, 200), (285, 230)], menta, 7), trazo([(327, 232), (358, 232)], menta, 7)]
    elif slug == "nexxo":
        p += [rect(70, 55, 500, 290, "#102a24", tenue, 20), rect(96, 84, 48, 48, "#077451", rx=14),
              trazo([(105, 108), (113, 108), (119, 94), (126, 123), (131, 108), (136, 108)], "#fff", 3.5)]
        for i in range(5):
            p.append(rect(96, 158 + i * 33, 90, 18, "#077451" if i == 1 else "#18392f", rx=9))
        for f in range(4):
            y = 92 + f * 52
            p += [rect(218, y, 190, 38, "#18392f", rx=10), rect(232, y + 14, 70 + f * 17, 9, tenue, rx=4)]
        p += [rect(432, 92, 112, 194, "#18392f", rx=12), rect(448, 238, 80, 30, menta, rx=15)]
        p += [rect(448, 112 + i * 24, 80 - i * 14, 9, tenue, rx=4) for i in range(4)]
    elif slug == "picocero":
        for i in range(24):
            h = 60 + 70 * math.exp(-((i - 7) / 2.5) ** 2) + 190 * math.exp(-((i - 17) / 2.6) ** 2)
            x = 62 + i * 22
            p.append(rect(x, 350 - min(h, 180), 14, min(h, 180), "#1d5c49", rx=3))
            if h > 180:
                p.append(rect(x, 350 - h, 14, h - 184, borde=cobre, rx=3))
        p.append(trazo([(48, 168), (592, 168)], cobre, 2, 'stroke-dasharray="7 7"'))
    elif slug == "rosca-transportadora":
        p += [trazo([(50, 160), (50, 285), (590, 285), (590, 160)], tenue, 3),
              trazo([(30, 200), (610, 200)], "#4e7567", 14)]
        for k in range(7):
            pts = [(70 + k * 72 + t * 72 + 18 * math.sin(t * 6.283), 200 - 74 * math.cos(t * 6.283))
                   for t in [i / 40 for i in range(41)]]
            p.append(trazo(pts, menta, 3))
    elif slug == "intercambiador-de-calor":
        p += [rect(60, 92, 520, 216, "#102a24", tenue, 70)]
        for i in range(8):
            y = 124 + i * 22
            p.append(trazo([(100, y), (540, y)], cobre if i < 4 else "#79b8f2", 5))
        for i in range(5):
            y = (100, 220) if i % 2 else (180, 300)
            p.append(trazo([(170 + i * 75, y[0]), (170 + i * 75, y[1])], menta, 3))
    else:
        for k, c in enumerate(("#ff8b70", "#79b8f2", menta)):
            p.append(trazo([(x, 200 + 90 * math.sin(x / 70 + k * 2.094)) for x in range(0, 641, 8)], c, 3))

    return ('<svg viewBox="0 0 640 400" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            '<rect width="640" height="400" fill="#0c201b"/>' + "".join(p) + "</svg>")


def retrato(base):
    if (RAIZ / "assets" / "img" / "foto.jpg").exists():
        return f'<img src="{base}assets/img/foto.jpg" alt="Nicolas Sgandurra">'
    p = [circulo(200, 200, r, "#b9cfc2", ancho=1) for r in (70, 118, 188)]
    for i in range(72):
        a, r = math.radians(i * 5), 172 if i % 6 == 0 else 181
        p.append(trazo([(200 + r * math.cos(a), 200 + r * math.sin(a)),
                        (200 + 188 * math.cos(a), 200 + 188 * math.sin(a))], "#8fb3a2", 1))
    for a, c in ((90, "#c65f45"), (210, "#3776a8"), (330, "#077451")):
        x, y = math.cos(math.radians(a)), -math.sin(math.radians(a))
        p += [trazo([(200 + 78 * x, 200 + 78 * y), (200 + 152 * x, 200 + 152 * y)], c, 3),
              circulo(200 + 152 * x, 200 + 152 * y, 6, relleno=c)]
    p += [circulo(200, 200, 76, relleno="#0c201b"),
          '<text x="200" y="222" text-anchor="middle" fill="#82ebc4" font-size="68" font-style="italic" '
          'font-family="Instrument Serif, Georgia, serif">NS</text>']
    return '<svg viewBox="0 0 400 400" aria-hidden="true">' + "".join(p) + "</svg>"


def ondas():
    """Tres fases. El dibujo es periódico, así el desplazamiento no tiene costura."""
    p = []
    for k, (_, _, color, _) in enumerate(FASES):
        pts = [(x, 90 + 52 * math.sin(2 * math.pi * x / 480 + k * 2 * math.pi / 3)) for x in range(0, 2881, 16)]
        p.append(trazo(pts, color, 1.5, 'vector-effect="non-scaling-stroke" opacity=".7"'))
    return '<svg class="ondas" viewBox="0 0 2880 180" preserveAspectRatio="none" aria-hidden="true">' + "".join(p) + "</svg>"


# ---------------------------------------------------------------- Piezas
def pagina(titulo, descripcion, cuerpo, base, inicio="", vista_previa=False, scripts=(), clase=""):
    robots = '<meta name="robots" content="noindex">' if vista_previa else ""
    aviso = '<p class="aviso">Vista previa con borradores</p>' if vista_previa else ""
    js = "\n".join(f'<script src="{base}assets/portfolio/{s}.js" defer></script>' for s in ("pagina", *scripts))
    return f"""<!doctype html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(titulo)}</title>
<meta name="description" content="{E(descripcion)}">
<meta name="theme-color" content="#06120f">
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
  <a class="firma" href="{inicio or '#inicio'}">Nicolas<span> Sgandurra</span></a>
  <nav aria-label="Principal"><ul>
    <li class="opcional"><a href="{inicio}#sobre-mi">Sobre mí</a></li>
    <li><a href="{inicio}#trabajo">Trabajo</a></li>
    <li><a href="{inicio}#trayectoria">Trayectoria</a></li>
    <li><a href="{inicio}#contacto">Contacto</a></li>
  </ul></nav>
</header>
{cuerpo}
</body>
</html>
"""


def visual(d, base):
    if not d.get("imagen"):
        return arte(d["slug"])
    # Los gráficos no se recortan, las capturas sí
    clase = ' class="figura"' if d["slug"].startswith("dlr") else ""
    return f'<img{clase} src="{base}assets/img/{E(d["imagen"])}" alt="" loading="lazy">'


def sello(d):
    return '<span class="sello">Borrador</span>' if d["borrador"] else ""


def obra(d, base):
    return f"""  <a class="obra aparece" href="proyectos/{d['slug']}.html">
    <div class="marco">{visual(d, base)}{sello(d)}</div>
    <div>
      <h3>{E(d['titulo'])}</h3>
      <p>{E(d['resumen'])}</p>
      <p class="tec">{E(', '.join(d['tecnologias']))}</p>
      <span class="ver">Ver el proyecto</span>
    </div>
  </a>"""


def pieza(d, base):
    # En la grilla van dibujos: las capturas no se entienden en ese tamaño
    return f"""    <a class="pieza aparece" href="proyectos/{d['slug']}.html">
      <div class="marco">{arte(d['slug'])}{sello(d)}</div>
      <h3>{E(d['titulo'])}</h3>
      <p>{E(d['resumen'])}</p>
    </a>"""


def laboratorio():
    vert = [(130 * math.cos(math.radians(a)), -130 * math.sin(math.radians(a))) for a in (0, 120, 240)]
    dibujo = [circulo(0, 0, r, "#2b5446", ancho=1) for r in (65, 130)]
    dibujo.append(trazo(vert + vert[:1], "#2b5446", 1, 'stroke-dasharray="4 5"'))
    filas = []
    for (i, letra, color, ohm), (x, y) in zip(FASES, vert):
        dibujo += [f'<line id="fasor-{i}" x1="0" y1="0" x2="{x:.1f}" y2="{y:.1f}" stroke="{color}"/>',
                   circulo(x, y, 5, relleno=color),
                   f'<text x="{x * 1.17:.1f}" y="{y * 1.17 + 5:.1f}" text-anchor="middle">{letra}</text>']
        filas.append(f"""      <div class="fase" style="--color-fase:{color}">
        <label for="carga-{i}">Fase {letra}, carga de <span id="ohm-{i}">{ohm} Ω</span></label>
        <output id="u-{i}">{INICIAL[i]}</output>
        <input id="carga-{i}" type="range" min="5" max="100" value="{ohm}">
      </div>""")
    dibujo.append('<circle id="punto-n" cx="0" cy="0" r="7" fill="#f0b96e"/>')
    return f"""<section class="bloque oscuro laboratorio" id="laboratorio">
  <h2>¿Qué pasa si se <em>corta el neutro</em>?</h2>
  <p class="entrada">Es un tema que doy en clase y se entiende mejor jugando. Cambiá las cargas y mirá cómo se corre el neutro: unas fases quedan con tensión de más y otras de menos.</p>
  <div class="banco" id="lab-neutro">
    <svg class="fasores" viewBox="-170 -170 340 340" role="img" aria-label="Diagrama fasorial de las tres fases y el punto neutro">{''.join(dibujo)}</svg>
    <div>
{chr(10).join(filas)}
      <label class="interruptor" for="corte"><input id="corte" type="checkbox" checked> Neutro cortado</label>
      <p class="nota">Desplazamiento del neutro: <output id="u-n">{INICIAL["n"]}</output>. Fuente ideal de 220 V por fase y cargas resistivas, calculado con el teorema de Millman.</p>
    </div>
  </div>
</section>"""


def portada(fichas, base, vista_previa):
    por_slug = {d["slug"]: d for d in fichas}
    grandes = [por_slug[s] for s in DESTACADOS if s in por_slug]
    areas = list(dict.fromkeys(["Sistemas eléctricos"] + [d["area"] for d in fichas]))
    chicas = sorted((d for d in fichas if d["slug"] not in DESTACADOS), key=lambda d: (areas.index(d["area"]), d["orden"]))
    return pagina(
        "Nicolas Sgandurra | Ingeniería eléctrica y programación",
        "Técnico electricista, docente y estudiante de Ingeniería Electromecánica. Proyectos de electricidad, simulación y software.",
        f"""<section class="portada" id="inicio">
  <canvas id="paisaje" aria-hidden="true"></canvas>
  <div class="presentacion">
    <h1>Nicolas <em>Sgandurra</em></h1>
    <p class="lema">Estudio la electricidad, la enseño y la programo.</p>
    <p class="rol">Técnico electricista y estudiante avanzado de Ingeniería Electromecánica en la UTN San Rafael.</p>
    <div class="botones">
      <a class="boton lleno" href="#trabajo">Ver mi trabajo</a>
      <a class="boton" href="#contacto">Escribime</a>
    </div>
  </div>
  <div class="medidor">
    <div class="medidor-cabeza">
      <label for="viento">Mové el viento</label>
      <button id="pausa" type="button">Pausar</button>
    </div>
    <input id="viento" type="range" min="0" max="15" step="0.5" value="4">
    <dl class="lecturas">
      <div><dt>Viento</dt><dd id="v-viento">4,0 m/s</dd></div>
      <div><dt>Corriente admisible</dt><dd id="v-corriente">800 A</dd></div>
      <div><dt>Temp. con 400&nbsp;A</dt><dd id="v-temp">38 °C</dd></div>
    </dl>
    <p class="supuestos">Cobre de 120 mm², 70 °C de máxima, 25 °C de ambiente, pleno sol y viento perpendicular.</p>
  </div>
</section>

<main id="contenido">
<section class="bloque claro" id="sobre-mi">
  <div class="sobre">
    <div class="retrato aparece">{retrato(base)}</div>
    <div class="aparece">
      <h2>Hola, soy <em>Nico</em>.</h2>
      <p>Me recibí de técnico electricista en 2020 y al año siguiente volví a la misma escuela, como docente de Circuitos Eléctricos. En paralelo curso Ingeniería Electromecánica en la UTN.</p>
      <p>Cuando un tema cuesta explicarlo en el pizarrón, le hago un simulador. Y si un cálculo hay que repetirlo miles de veces, lo programo. También hago software a medida, sentado con quien lo va a usar para entender cómo trabaja.</p>
      <dl class="datos-breves">
        <div><dt>Dónde estoy</dt><dd>San Rafael, Mendoza, Argentina</dd></div>
        <div><dt>Disponibilidad</dt><dd>Desde comienzos de 2027, full time</dd></div>
        <div><dt>Estudios</dt><dd>Ingeniería Electromecánica, graduación prevista en 2027</dd></div>
        <div><dt>Idiomas</dt><dd>Español nativo, inglés intermedio</dd></div>
      </dl>
    </div>
  </div>
</section>

<section class="bloque oscuro" id="trabajo">
  <h2>Proyectos <em>seleccionados</em></h2>
  <p class="entrada">Cada proyecto cuenta el problema, qué hice y hasta dónde llega.</p>
{chr(10).join(obra(d, base) for d in grandes)}
  <div class="piezas">
{chr(10).join(pieza(d, base) for d in chicas)}
  </div>
</section>

{laboratorio()}

<section class="bloque claro" id="trayectoria">
  <h2>El <em>recorrido</em></h2>
  <ol class="camino">
    <li class="aparece"><time>2017</time><div><h3>Tec.Nito</h3><p>Empiezo a trabajar por mi cuenta en reparación de equipos, redes y armado de workstations. Lo sigo haciendo.</p></div></li>
    <li class="aparece"><time>2020</time><div><h3>Técnico Electricista</h3><p>Escuela 4-124 Reynaldo Merín.</p></div></li>
    <li class="aparece"><time>2021</time><div><h3>Ingeniería Electromecánica y docencia</h3><p>Entro a la UTN San Rafael y, en octubre, empiezo a dar Circuitos Eléctricos 1 y 2 en la escuela donde me recibí.</p></div></li>
    <li class="aparece"><time>2022</time><div><h3>Tecnicatura Universitaria en Programación</h3><p>Cursada completa entre 2022 y 2024. Equivalencia pendiente de acreditar.</p></div></li>
    <li class="aparece"><time>2026</time><div><h3>Sistemas de potencia y software a medida</h3><p>Estudio preliminar de capacidad dinámica de una línea de 132 kV y desarrollo de Nexxo, un sistema de gestión que ya funciona en paralelo con el anterior. Termino de cursar la carrera.</p></div></li>
    <li class="aparece"><time>2027</time><div><h3>Lo que sigue</h3><p>Recibirme de ingeniero y trabajar en proyectos eléctricos.</p></div></li>
  </ol>
  <div class="herramientas">
    <div><h3>Ingeniería</h3><p>Mathcad, AutoCAD, Autodesk Inventor, Excel, ETAP (nivel inicial)</p></div>
    <div><h3>Programación</h3><p>Python, JavaScript, TypeScript, React, FastAPI, PostgreSQL</p></div>
    <div><h3>Control de versiones</h3><p>Git y GitHub</p></div>
  </div>
</section>
</main>

<footer>
  <section class="bloque contacto" id="contacto">
    <h2>¿Trabajamos <em>juntos</em>?</h2>
    <a class="correo" href="mailto:{CORREO}">{CORREO}</a>
    <div class="botones">
      <a class="boton" href="{LINKEDIN}">LinkedIn</a>
      <a class="boton" href="{GITHUB}">GitHub</a>
    </div>
    {ondas()}
  </section>
  <div class="pie"><span>Nicolas Leonel Sgandurra</span><span>San Rafael, Mendoza, Argentina</span></div>
</footer>""",
        base, vista_previa=vista_previa, scripts=("linea",))


def ficha(d, base, vista_previa):
    datos = [("Estado", d["estado"]), ("Autoría", d["autoria"]), ("Herramientas", ", ".join(d["tecnologias"]))]
    aside = "".join(f"<dt>{k}</dt><dd>{E(v)}</dd>" for k, v in datos)
    partes = []
    if d.get("imagen"):
        partes.append(f'<figure><img src="{base}assets/img/{E(d["imagen"])}" alt="{E(d["pie"])}">'
                      f'<figcaption>{E(d["pie"])}</figcaption></figure>')
    else:
        partes.append(f"<figure>{arte(d['slug'])}</figure>")
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
  <h1>{E(d['titulo'])}</h1>
  <p class="bajada">{E(d['resumen'])}</p>
  {aviso}
</header>
<article class="bloque claro cuerpo-ficha">
  <aside><dl>{aside}</dl></aside>
  <div>{''.join(partes)}</div>
</article>
</main>
<footer class="pie"><span>Nicolas Leonel Sgandurra</span><a href="mailto:{CORREO}">{CORREO}</a></footer>"""
    return pagina(f"{d['titulo']} | Nicolas Sgandurra", d["resumen"], cuerpo, base,
                  inicio="../index.html", vista_previa=vista_previa, clase="interior")


def generar(destino, fichas, vista_previa=False):
    salida = destino / "portfolio"
    proyectos = salida / "proyectos"
    proyectos.mkdir(parents=True, exist_ok=True)
    for viejo in proyectos.glob("*.html"):
        viejo.unlink()
    (salida / "index.html").write_text(portada(fichas, "../", vista_previa), encoding="utf-8")
    for d in fichas:
        (proyectos / f"{d['slug']}.html").write_text(ficha(d, "../../", vista_previa), encoding="utf-8")
