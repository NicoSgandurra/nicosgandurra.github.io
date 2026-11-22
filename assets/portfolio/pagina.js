(function () {
  'use strict';

  /* ---------- Barra: transparente sobre la portada, sólida al bajar */
  var barra = document.querySelector('.nav');
  function alBajar() { barra.classList.toggle('solida', window.scrollY > 40); }
  window.addEventListener('scroll', alBajar, { passive: true });
  alBajar();

  /* ---------- Aparición suave. Sin JS, o con movimiento reducido, todo queda visible. */
  var reducido = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reducido && 'IntersectionObserver' in window) {
    var observador = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.remove('espera');
        observador.unobserve(e.target);
      });
    }, { threshold: 0, rootMargin: '0px 0px -40px' });
    document.querySelectorAll('.aparece').forEach(function (el) {
      if (el.getBoundingClientRect().top < window.innerHeight) return;
      el.classList.add('espera');
      observador.observe(el);
    });
  }

  /* ---------- Neutro flotante, por el teorema de Millman */
  var lab = document.getElementById('lab-neutro');
  if (!lab) return;

  var U = 220;
  var ESCALA = 130 / U;
  var FASES = [['r', 0], ['t', 120], ['s', 240]].map(function (f) {
    var a = f[1] * Math.PI / 180;
    return { id: f[0], x: U * Math.cos(a), y: U * Math.sin(a) };
  });
  var corte = lab.querySelector('#corte');

  function punto(p) { return [p.x * ESCALA, -p.y * ESCALA]; }

  function calcular() {
    var gs = 0, nx = 0, ny = 0;
    FASES.forEach(function (f) {
      var ohm = Number(lab.querySelector('#carga-' + f.id).value);
      lab.querySelector('#ohm-' + f.id).textContent = ohm + ' Ω';
      nx += f.x / ohm;
      ny += f.y / ohm;
      gs += 1 / ohm;
    });
    var n = corte.checked ? { x: nx / gs, y: ny / gs } : { x: 0, y: 0 };
    var pn = punto(n);

    FASES.forEach(function (f) {
      var v = Math.hypot(f.x - n.x, f.y - n.y);
      var pf = punto(f);
      var linea = lab.querySelector('#fasor-' + f.id);
      linea.setAttribute('x1', pn[0]);
      linea.setAttribute('y1', pn[1]);
      linea.setAttribute('x2', pf[0]);
      linea.setAttribute('y2', pf[1]);
      var salida = lab.querySelector('#u-' + f.id);
      salida.textContent = v.toFixed(1).replace('.', ',') + ' V';
      /* Banda de ±8 % */
      salida.dataset.estado = v > U * 1.08 ? 'alta' : v < U * 0.92 ? 'baja' : 'normal';
    });

    var marca = lab.querySelector('#punto-n');
    marca.setAttribute('cx', pn[0]);
    marca.setAttribute('cy', pn[1]);
    lab.querySelector('#u-n').textContent = Math.hypot(n.x, n.y).toFixed(1).replace('.', ',') + ' V';
  }

  lab.addEventListener('input', calcular);
  calcular();
})();
