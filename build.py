"""Genera la web de proyectos.

    python build.py

contenido/*.json   fichas públicas      -> index.html y proyectos/
borradores/*.json  fichas sin permiso   -> solo vista-previa/ (ambas carpetas ignoradas por Git)

Para publicar un borrador: mover su .json a contenido/ y su imagen de
borradores/img/ a assets/img/, volver a ejecutar y hacer commit.
"""
import html
import json
import shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
SITIO = "Nicolas Sgandurra"
AREAS = ["Sistemas eléctricos", "Ingeniería mecánica y térmica", "Software y automatización"]
E = html.escape


def cargar(carpeta, borrador=False):
    fichas = []
    for f in sorted((RAIZ / carpeta).glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        assert d["area"] in AREAS, f"{f.name}: área desconocida"
        d.update(slug=f.stem, borrador=borrador)
        fichas.append(d)
    return sorted(fichas, key=lambda d: d["orden"])


def pagina(titulo, descripcion, cuerpo, base="", vista_previa=False):
    robots = '<meta name="robots" content="noindex">' if vista_previa else ""
    aviso = '<p class="aviso">Vista previa privada: incluye borradores que todavía no se publican.</p>' if vista_previa else ""
    return f"""<!doctype html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(titulo)}</title>
<meta name="description" content="{E(descripcion)}">
{robots}
<link rel="icon" href="{base}assets/favicon.svg">
<link rel="stylesheet" href="{base}assets/estilo.css">
<script src="{base}assets/tema.js" defer></script>
</head>
<body>
{aviso}
<header class="barra">
  <a class="marca" href="{base}index.html">Nicolas <strong>Sgandurra</strong></a>
  <nav>
    <a href="https://github.com/NicoSgandurra">GitHub</a>
    <a href="https://www.linkedin.com/in/nicosgandurra">LinkedIn</a>
    <button id="tema" type="button">Modo oscuro</button>
  </nav>
</header>
<main>
{cuerpo}
</main>
<footer>
  <span>San Rafael, Mendoza, Argentina</span>
  <a href="mailto:nico.sgandurra@gmail.com">nico.sgandurra@gmail.com</a>
</footer>
</body>
</html>
"""


def tarjeta(d):
    if d.get("imagen"):
        vista = f'<img src="assets/img/{E(d["imagen"])}" alt="" loading="lazy">'
    else:
        vista = f'<span class="sigla" aria-hidden="true">{E(d["sigla"])}</span>'
    marca = '<span class="borrador">Borrador</span>' if d["borrador"] else ""
    return f"""    <a class="tarjeta" href="proyectos/{d['slug']}.html">
      <div class="miniatura">{vista}{marca}</div>
      <div class="texto">
        <h3>{E(d['titulo'])}</h3>
        <p>{E(d['resumen'])}</p>
        <p class="tec">{E(', '.join(d['tecnologias']))}</p>
      </div>
    </a>"""


def portada(fichas, vista_previa):
    grupos = []
    for area in AREAS:
        items = [d for d in fichas if d["area"] == area]
        if items:
            tarjetas = "\n".join(map(tarjeta, items))
            grupos.append(f'<section>\n  <h2>{area}</h2>\n  <div class="grilla">\n{tarjetas}\n  </div>\n</section>')
    cuerpo = """<section class="intro">
  <h1>Proyectos de ingeniería</h1>
  <p>Soy técnico electricista, docente de Circuitos Eléctricos y estudiante avanzado de Ingeniería
  Electromecánica en la UTN San Rafael. Cada proyecto tiene una ficha con el problema, lo que hice y sus límites.</p>
</section>
""" + "\n".join(grupos)
    return pagina(f"{SITIO} | Proyectos de ingeniería",
                  "Proyectos de ingeniería eléctrica, simulación y software de Nicolas Sgandurra.",
                  cuerpo, "", vista_previa)


def ficha(d, vista_previa):
    p = [f'<a class="volver" href="../index.html">Todos los proyectos</a>', '<article class="ficha">']
    if d["borrador"]:
        p.append(f'<p class="pendiente">Antes de publicar: {E(d["pendiente"])}</p>')
    p += [f"<h1>{E(d['titulo'])}</h1>",
          f'<p class="bajada">{E(d["resumen"])}</p>',
          '<dl class="datos">']
    for k, v in [("Estado", d["estado"]), ("Autoría", d["autoria"]), ("Herramientas", ", ".join(d["tecnologias"]))]:
        p.append(f"<div><dt>{k}</dt><dd>{E(v)}</dd></div>")
    p.append("</dl>")
    if d.get("imagen"):
        p.append(f'<figure><img src="../assets/img/{E(d["imagen"])}" alt="{E(d["pie"])}">'
                 f"<figcaption>{E(d['pie'])}</figcaption></figure>")
    p += ["<h2>Problema</h2>", f"<p>{E(d['problema'])}</p>", "<h2>Qué hice</h2>",
          "<ul>" + "".join(f"<li>{E(x)}</li>" for x in d["trabajo"]) + "</ul>"]
    if d.get("resultados"):
        filas = "".join(f'<tr><th scope="row">{E(k)}</th><td>{E(v)}</td></tr>' for k, v in d["resultados"])
        p += ["<h2>Resultados</h2>", f"<table>{filas}</table>"]
    if d.get("limites"):
        p += ["<h2>Límites</h2>", "<ul>" + "".join(f"<li>{E(x)}</li>" for x in d["limites"]) + "</ul>"]
    if d.get("enlaces"):
        p.append('<p class="acciones">' + "".join(f'<a href="{E(u)}">{E(t)}</a>' for t, u in d["enlaces"]) + "</p>")
    p.append("</article>")
    return pagina(f"{d['titulo']} | {SITIO}", d["resumen"], "\n".join(p), "../", vista_previa)


def generar(destino, fichas, vista_previa=False):
    carpeta = destino / "proyectos"
    if carpeta.exists():
        for viejo in carpeta.glob("*.html"):
            viejo.unlink()
    carpeta.mkdir(parents=True, exist_ok=True)
    (destino / "index.html").write_text(portada(fichas, vista_previa), encoding="utf-8")
    for d in fichas:
        (carpeta / f"{d['slug']}.html").write_text(ficha(d, vista_previa), encoding="utf-8")


def main():
    publicas = cargar("contenido")
    borradores = cargar("borradores", True)
    for d in publicas:
        if d.get("imagen"):
            assert (RAIZ / "assets" / "img" / d["imagen"]).exists(), f"falta la imagen de {d['slug']}"
    generar(RAIZ, publicas)
    if borradores:
        previa = RAIZ / "vista-previa"
        generar(previa, sorted(publicas + borradores, key=lambda d: d["orden"]), True)
        shutil.copytree(RAIZ / "assets", previa / "assets", dirs_exist_ok=True)
        if (RAIZ / "borradores" / "img").exists():
            shutil.copytree(RAIZ / "borradores" / "img", previa / "assets" / "img", dirs_exist_ok=True)
    print(f"{len(publicas)} públicas, {len(borradores)} borradores")


if __name__ == "__main__":
    main()
