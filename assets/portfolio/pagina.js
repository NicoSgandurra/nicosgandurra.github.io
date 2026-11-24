(function () {
  'use strict';

  document.documentElement.classList.remove('sin-js');
  document.documentElement.classList.add('js');
  var mac = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent);

  /* ---------- Barra: transparente arriba, con fondo al bajar */
  var barra = document.querySelector('.nav');
  function alBajar() { barra.classList.toggle('solida', window.scrollY > 20); }
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
      /* Escalonado entre hermanos: las tarjetas de una grilla entran una detrás de otra */
      var hermanos = Array.prototype.filter.call(el.parentNode.children, function (h) { return h.classList.contains('aparece'); });
      var i = hermanos.indexOf(el);
      if (hermanos.length > 1 && i > 0) el.style.transitionDelay = Math.min(i, 6) * 70 + 'ms';
      el.classList.add('espera');
      observador.observe(el);
    });
  }

  /* ---------- Ventanas que se enderezan al bajar (vitrina y portada de cada proyecto) */
  var inclinables = Array.prototype.slice.call(document.querySelectorAll('.vitrina, [data-inclinar] .marco'));
  if (!reducido && inclinables.length) {
    var pendiente = false;
    var inclinar = function () {
      pendiente = false;
      var alto = window.innerHeight;
      inclinables.forEach(function (el) {
        var r = el.getBoundingClientRect();
        /* 1 cuando el borde de arriba está abajo de la pantalla, 0 cuando llegó al 45 % */
        var k = (r.top - alto * 0.45) / (alto * 0.5);
        el.style.setProperty('--inclinacion', Math.max(0, Math.min(1, k)).toFixed(3));
      });
    };
    window.addEventListener('scroll', function () {
      if (!pendiente) { pendiente = true; requestAnimationFrame(inclinar); }
    }, { passive: true });
    window.addEventListener('resize', inclinar);
    inclinar();
  }

  /* ---------- Cifras que cuentan hasta su valor la primera vez que se ven */
  var cifras = Array.prototype.slice.call(document.querySelectorAll('[data-cifra]'));
  if (!reducido && cifras.length && 'IntersectionObserver' in window) {
    var contar = function (el) {
      var texto = el.textContent;
      var m = texto.match(/^([\d.]+)(,(\d+))?(.*)$/);
      if (!m || /^(19|20)\d\d$/.test(texto.trim())) return;
      var final = parseFloat(m[1].replace(/\./g, '') + (m[3] ? '.' + m[3] : ''));
      var decimales = m[3] ? m[3].length : 0;
      var miles = m[1].indexOf('.') >= 0;
      var formato = function (v) {
        var s = v.toFixed(decimales).split('.');
        if (miles) s[0] = s[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.');
        return s[0] + (decimales ? ',' + s[1] : '') + m[4];
      };
      var inicio = null;
      var paso = function (t) {
        if (inicio === null) inicio = t;
        var x = Math.min(1, (t - inicio) / 1400);
        el.textContent = formato(final * (1 - Math.pow(1 - x, 3)));
        if (x < 1) requestAnimationFrame(paso); else el.textContent = texto;
      };
      requestAnimationFrame(paso);
    };
    var vigiaCifras = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (!e.isIntersecting) return;
        vigiaCifras.unobserve(e.target);
        contar(e.target);
      });
    }, { threshold: 0.6 });
    cifras.forEach(function (c) { vigiaCifras.observe(c); });
  }

  /* ---------- Reflejo que sigue al mouse en las tarjetas */
  document.addEventListener('pointermove', function (ev) {
    if (ev.pointerType !== 'mouse') return;
    var t = ev.target.closest && ev.target.closest('.tarjeta');
    if (!t) return;
    var r = t.getBoundingClientRect();
    t.style.setProperty('--mx', (ev.clientX - r.left) + 'px');
    t.style.setProperty('--my', (ev.clientY - r.top) + 'px');
  }, { passive: true });

  /* ---------- Copiar el correo */
  var aviso = null;
  function avisar(texto) {
    if (aviso) aviso.remove();
    aviso = document.createElement('p');
    aviso.className = 'copiado';
    aviso.setAttribute('role', 'status');
    aviso.textContent = texto;
    document.body.appendChild(aviso);
    var este = aviso;
    setTimeout(function () { este.remove(); }, 1800);
  }
  function copiar(texto) {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(texto).then(function () { avisar('Correo copiado'); }, function () { avisar(texto); });
    } else {
      avisar(texto);
    }
  }
  document.querySelectorAll('[data-copiar]').forEach(function (b) {
    b.hidden = false;
    b.addEventListener('click', function () {
      copiar(b.dataset.copiar);
      if (paleta && paleta.open) paleta.close();
    });
  });

  /* ---------- Paleta de comandos */
  var paleta = document.getElementById('paleta');
  if (paleta && typeof paleta.showModal === 'function') {
    var texto = document.getElementById('paleta-texto');
    var opciones = Array.prototype.slice.call(paleta.querySelectorAll('[role="option"]'));
    var grupos = Array.prototype.slice.call(paleta.querySelectorAll('.paleta-grupo'));
    var vacia = paleta.querySelector('.paleta-vacia');
    var activa = -1;
    var plano = function (s) { return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase(); };

    document.querySelectorAll('[data-atajo]').forEach(function (k) { k.textContent = mac ? '⌘ K' : 'Ctrl K'; });

    var visibles = function () { return opciones.filter(function (o) { return !o.hidden; }); };

    function marcar(i) {
      var lista = visibles();
      opciones.forEach(function (o) { o.setAttribute('aria-selected', 'false'); });
      if (!lista.length) { activa = -1; texto.removeAttribute('aria-activedescendant'); return; }
      activa = (i + lista.length) % lista.length;
      var o = lista[activa];
      o.setAttribute('aria-selected', 'true');
      texto.setAttribute('aria-activedescendant', o.id);
      o.scrollIntoView({ block: 'nearest' });
    }

    function filtrar() {
      var q = plano(texto.value.trim()).split(/\s+/).filter(Boolean);
      opciones.forEach(function (o) {
        var clave = plano(o.dataset.clave);
        o.hidden = !q.every(function (p) { return clave.indexOf(p) >= 0; });
      });
      /* Un grupo se ve si tiene alguna opción visible antes del grupo siguiente */
      grupos.forEach(function (gr) {
        var hay = false;
        for (var n = gr.nextElementSibling; n && !n.classList.contains('paleta-grupo'); n = n.nextElementSibling) {
          if (!n.hidden) { hay = true; break; }
        }
        gr.hidden = !hay;
      });
      vacia.hidden = visibles().length > 0;
      marcar(0);
    }

    function abrir() {
      if (paleta.open) return;
      texto.value = '';
      filtrar();
      paleta.showModal();
      texto.focus();
    }

    function elegir(o) {
      var destino = o && o.firstElementChild;
      if (destino) destino.click();
    }

    document.querySelectorAll('[data-paleta]').forEach(function (b) { b.addEventListener('click', abrir); });
    document.addEventListener('keydown', function (ev) {
      if ((ev.ctrlKey || ev.metaKey) && !ev.altKey && ev.key.toLowerCase() === 'k') {
        ev.preventDefault();
        if (paleta.open) paleta.close(); else abrir();
      }
    });
    texto.addEventListener('input', filtrar);
    texto.addEventListener('keydown', function (ev) {
      if (ev.key === 'ArrowDown') { ev.preventDefault(); marcar(activa + 1); }
      else if (ev.key === 'ArrowUp') { ev.preventDefault(); marcar(activa - 1); }
      else if (ev.key === 'Enter') { ev.preventDefault(); elegir(visibles()[activa]); }
    });
    opciones.forEach(function (o) {
      o.addEventListener('mousemove', function () {
        var i = visibles().indexOf(o);
        if (i !== activa) marcar(i);
      });
    });
    paleta.addEventListener('click', function (ev) {
      if (ev.target === paleta) { paleta.close(); return; }
      var enlace = ev.target.closest('a');
      if (enlace) paleta.close();
    });
  }

  /* ---------- Sección actual resaltada en la barra */
  var enlacesNav = Array.prototype.slice.call(document.querySelectorAll('.nav nav a[href^="#"]'));
  if (enlacesNav.length && 'IntersectionObserver' in window) {
    var porId = {};
    enlacesNav.forEach(function (a) { porId[a.getAttribute('href').slice(1)] = a; });
    var vigia = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        var a = porId[e.target.id];
        if (!a) return;
        if (e.isIntersecting) {
          enlacesNav.forEach(function (o) { o.removeAttribute('aria-current'); });
          a.setAttribute('aria-current', 'true');
        } else if (a.getAttribute('aria-current')) {
          a.removeAttribute('aria-current');
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(porId).forEach(function (id) {
      var s = document.getElementById(id);
      if (s) vigia.observe(s);
    });
  }

  /* ---------- Vitrina de la portada: lista y vista previa */
  var vitrina = document.querySelector('[data-vitrina]');
  if (vitrina) {
    var items = Array.prototype.slice.call(vitrina.querySelectorAll('.item'));
    var vistas = Array.prototype.slice.call(vitrina.querySelectorAll('.vista'));
    var actual = 0;

    var mostrar = function (i) {
      if (i === actual) return;
      actual = i;
      items.forEach(function (it, k) {
        if (k === i) it.setAttribute('aria-current', 'true'); else it.removeAttribute('aria-current');
      });
      vistas.forEach(function (v, k) { v.hidden = k !== i; });
    };
    /* Cualquier gesto del usuario corta el recorrido automático */
    var manual = function () { vitrina.classList.remove('auto'); };

    items.forEach(function (it, i) {
      it.addEventListener('mouseenter', function () { manual(); mostrar(i); });
      it.addEventListener('focus', function () { manual(); mostrar(i); });
      it.addEventListener('keydown', function (ev) {
        var paso = ev.key === 'ArrowDown' ? 1 : ev.key === 'ArrowUp' ? -1 : 0;
        if (!paso) return;
        ev.preventDefault();
        items[(i + paso + items.length) % items.length].focus();
      });
    });

    /* Avanza solo, con una barrita de progreso en CSS. Se frena con el mouse encima. */
    if (!reducido && items.length > 1) {
      vitrina.classList.add('auto');
      vitrina.addEventListener('animationend', function (ev) {
        if (!vitrina.classList.contains('auto') || ev.animationName !== 'avance') return;
        mostrar((actual + 1) % items.length);
      });
      vitrina.addEventListener('touchstart', manual, { passive: true });
    }
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
