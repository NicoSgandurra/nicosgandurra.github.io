# Proyectos de Nicolas Sgandurra

Web de proyectos: https://nicosgandurra.github.io/

Hay dos versiones, generadas con las mismas fichas:

- `/`: portfolio personal, con portada interactiva. Los textos están en `portfolio.py`.
- `/catalogo/`: catálogo con todas las fichas agrupadas por área.

La foto es opcional: guardarla como `assets/img/foto.jpg` y regenerar.

Cada archivo de `contenido/` es una ficha. Después de agregar o editar una:

```
python build.py
```

Los HTML se generan con ese comando, no se editan a mano.
