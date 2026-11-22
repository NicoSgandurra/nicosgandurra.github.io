/* Portada: un vano de línea. El viento enfría el conductor; caliente, se dilata y baja la flecha. */
(function () {
  'use strict';

  var lienzo = document.getElementById('paisaje');
  if (!lienzo || !lienzo.getContext) return;

  /* [viento m/s, corriente admisible A, temperatura con 400 A °C]
     Balance térmico de un cobre de 120 mm²: 25 °C de ambiente, 70 °C de máxima,
     viento perpendicular y pleno sol. Valores precalculados. */
  var TABLA = [
    [0, 319.2, 84.4], [0.5, 478.2, 58.8], [1, 561.7, 50.6], [1.5, 617.3, 46.6], [2, 660.2, 44.1],
    [3, 725.7, 41.0], [4, 800.3, 37.9], [5, 874.6, 35.9], [6, 940.4, 34.5], [7, 1000.0, 33.4],
    [8, 1054.7, 32.6], [9, 1105.4, 31.9], [10, 1152.8, 31.3], [11, 1197.5, 30.9], [12, 1239.8, 30.5],
    [13, 1280.0, 30.2], [14, 1318.4, 29.9], [15, 1355.2, 29.6]
  ];

  var g = lienzo.getContext('2d');
  var caja = lienzo.parentElement;
  var ventana = caja.closest('.ventana') || caja;
  var control = document.getElementById('viento');
  var pausa = document.getElementById('pausa');
  var salidaViento = document.getElementById('v-viento');
  var salidaCorriente = document.getElementById('v-corriente');
  var salidaTemp = document.getElementById('v-temp');

  var fondo = document.createElement('canvas');
  var W, H, DPR, torres = [], rafagas = [];
  var objetivo = Number(control.value);
  var viento = objetivo;
  var manual = false, visible = true, cuadro = null, antes = 0;
  var fase = 0, recorrido = 0;
  var quieto = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function estado(v) {
    for (var i = 1; i < TABLA.length; i++) {
      if (v <= TABLA[i][0]) {
        var a = TABLA[i - 1], b = TABLA[i];
        var k = (v - a[0]) / (b[0] - a[0]);
        return { amperes: a[1] + k * (b[1] - a[1]), grados: a[2] + k * (b[2] - a[2]) };
      }
    }
    var u = TABLA[TABLA.length - 1];
    return { amperes: u[1], grados: u[2] };
  }

  /* Verde frío, ámbar, naranja y rojo según la temperatura */
  function color(t, alfa) {
    var p = [[29, 74, 222, 155], [42, 160, 220, 120], [52, 251, 191, 36], [66, 251, 146, 60], [85, 255, 106, 106]];
    var i = 1;
    while (i < p.length - 1 && t > p[i][0]) i++;
    var a = p[i - 1], b = p[i];
    var k = Math.max(0, Math.min(1, (t - a[0]) / (b[0] - a[0])));
    var c = [1, 2, 3].map(function (j) { return Math.round(a[j] + k * (b[j] - a[j])); });
    return 'rgba(' + c.join(',') + ',' + alfa + ')';
  }

  function azar(semilla) {
    return function () {
      semilla = (semilla * 16807) % 2147483647;
      return (semilla - 1) / 2147483646;
    };
  }

  /* Torre vista de frente: dos montantes que se cierran, celosía y tres ménsulas por lado */
  function torre(c, x, base, h) {
    function semi(f) { return h * (0.1 - 0.072 * Math.min(1, f / 0.62)) - (f > 0.62 ? h * 0.012 * (f - 0.62) / 0.38 : 0); }
    var niveles = [0, 0.14, 0.27, 0.39, 0.5, 0.6, 0.68, 0.76, 0.84, 0.92, 1];
    c.lineCap = 'round';
    c.strokeStyle = 'rgba(255,255,255,.34)';
    c.lineWidth = 1.1;
    c.beginPath();
    [-1, 1].forEach(function (s) {
      niveles.forEach(function (f, i) {
        var px = x + s * semi(f), py = base - h * f;
        if (i) c.lineTo(px, py); else c.moveTo(px, py);
      });
    });
    c.stroke();
    c.strokeStyle = 'rgba(255,255,255,.14)';
    c.lineWidth = 0.8;
    c.beginPath();
    for (var i = 1; i < niveles.length; i++) {
      var a = semi(niveles[i - 1]), b = semi(niveles[i]);
      var ya = base - h * niveles[i - 1], yb = base - h * niveles[i];
      c.moveTo(x - a, ya); c.lineTo(x + b, yb);
      c.moveTo(x + a, ya); c.lineTo(x - b, yb);
    }
    c.stroke();
    var puntos = { izq: [], der: [] };
    c.strokeStyle = 'rgba(255,255,255,.3)';
    c.lineWidth = 1;
    [[0.62, 0.17], [0.76, 0.145], [0.9, 0.12]].forEach(function (m) {
      [-1, 1].forEach(function (s) {
        var px = x + s * h * m[1], py = base - h * m[0];
        c.beginPath();
        c.moveTo(x + s * semi(m[0]), py); c.lineTo(px, py);
        c.lineTo(x + s * semi(m[0] + 0.06), py - h * 0.06);
        c.moveTo(px, py); c.lineTo(px, py + h * 0.04);
        c.stroke();
        puntos[s < 0 ? 'izq' : 'der'].push([px, py + h * 0.04]);
      });
    });
    return puntos;
  }

  function armar() {
    var r = caja.getBoundingClientRect();
    W = Math.max(1, Math.round(r.width));
    H = Math.max(1, Math.round(r.height));
    DPR = Math.min(window.devicePixelRatio || 1, 2);
    lienzo.width = fondo.width = W * DPR;
    lienzo.height = fondo.height = H * DPR;
    g.setTransform(DPR, 0, 0, DPR, 0, 0);

    var c = fondo.getContext('2d');
    c.setTransform(DPR, 0, 0, DPR, 0, 0);
    c.clearRect(0, 0, W, H);
    c.fillStyle = 'rgba(255,255,255,.07)';
    for (var x = 12; x < W; x += 22) {
      for (var y = 12; y < H; y += 22) c.fillRect(x, y, 1, 1);
    }
    var base = H * 0.95, alto = Math.min(H * 0.78, W * 0.62);
    c.strokeStyle = 'rgba(255,255,255,.1)';
    c.beginPath(); c.moveTo(0, base + 0.5); c.lineTo(W, base + 0.5); c.stroke();
    var margen = Math.max(alto * 0.2, W * 0.12);
    torres = [torre(c, margen, base, alto), torre(c, W - margen, base, alto)];
    torres.alto = alto;

    var q = azar(601);
    rafagas = [];
    for (var i = 0; i < Math.round(W / 14); i++) rafagas.push({ x: q() * W, y: q() * H * 0.9, v: 0.5 + q(), f: q() * 6.28 });
  }

  function curva(a, b, flecha, vaiven) {
    return { a: a, b: b, cx: (a[0] + b[0]) / 2, cy: (a[1] + b[1]) / 2 + flecha * 2 + vaiven };
  }

  function sobre(k, u) {
    var w = 1 - u;
    return [w * w * k.a[0] + 2 * w * u * k.cx + u * u * k.b[0], w * w * k.a[1] + 2 * w * u * k.cy + u * u * k.b[1]];
  }

  function pintar() {
    var e = estado(viento);
    g.clearRect(0, 0, W, H);
    g.drawImage(fondo, 0, 0, W, H);

    if (viento > 0.2) {
      g.strokeStyle = 'rgba(255,255,255,' + Math.min(0.16, 0.02 + viento * 0.01) + ')';
      g.lineWidth = 1;
      g.beginPath();
      rafagas.forEach(function (r) {
        var largo = 6 + viento * 6 * r.v, onda = Math.sin(fase + r.f) * 3;
        g.moveTo(r.x - largo, r.y);
        g.quadraticCurveTo(r.x - largo / 2, r.y + onda, r.x, r.y);
      });
      g.stroke();
    }

    /* Flecha: crece con la temperatura del conductor */
    var calor = (e.grados - 29.6) / (84.4 - 29.6);
    var flecha = torres.alto * (0.07 + 0.13 * calor);
    var cable = color(e.grados, 0.95), halo = color(e.grados, 0.12), punto = color(e.grados, 1);
    var principales = [], vanos = [];
    var izq = torres[0].der, der = torres[1].izq;
    for (var k = 0; k < 3; k++) {
      var vaiven = Math.sin(fase * 1.5 + k * 0.7) * viento * 0.18;
      var vano = der[k][0] - izq[k][0];
      var a = torres[0].izq[k], b = torres[1].der[k];
      principales.push(curva(izq[k], der[k], flecha, vaiven));
      /* Los vanos vecinos, cortados por los bordes */
      vanos.push(curva([a[0] - vano, a[1]], a, flecha, vaiven), curva(b, [b[0] + vano, b[1]], flecha, vaiven));
    }
    vanos.concat(principales).forEach(function (v) {
      g.beginPath();
      g.moveTo(v.a[0], v.a[1]);
      g.quadraticCurveTo(v.cx, v.cy, v.b[0], v.b[1]);
      g.strokeStyle = halo;
      g.lineWidth = 7;
      g.stroke();
      g.strokeStyle = cable;
      g.lineWidth = 1.4;
      g.stroke();
    });

    /* Cargas que recorren el vano principal */
    for (var j = 0; j < 3; j++) {
      var v = principales[j];
      for (var n = 0; n < 3; n++) {
        var p = sobre(v, (recorrido + n / 3 + j * 0.11) % 1);
        g.fillStyle = halo;
        g.beginPath(); g.arc(p[0], p[1], 7, 0, 6.283); g.fill();
        g.fillStyle = punto;
        g.beginPath(); g.arc(p[0], p[1], 2, 0, 6.283); g.fill();
      }
    }
  }

  function numeros() {
    var e = estado(objetivo);
    salidaViento.textContent = objetivo.toFixed(1).replace('.', ',') + ' m/s';
    salidaCorriente.textContent = Math.round(e.amperes) + ' A';
    salidaTemp.textContent = Math.round(e.grados) + ' °C';
    salidaTemp.style.color = color(e.grados, 1);
    control.setAttribute('aria-valuetext', salidaViento.textContent + ', admite ' + salidaCorriente.textContent);
  }

  function paso(ahora) {
    cuadro = null;
    if (quieto || !visible || document.hidden) return;
    var dt = antes ? Math.min(0.05, (ahora - antes) / 1000) : 0.016;
    antes = ahora;
    viento += (objetivo - viento) * Math.min(1, dt * 3);
    fase += dt;
    recorrido = (recorrido + dt * estado(viento).amperes / 3000) % 1;
    rafagas.forEach(function (r) {
      r.x += dt * viento * 30 * r.v;
      if (r.x > W + 100) r.x = -10;
    });
    pintar();
    cuadro = requestAnimationFrame(paso);
  }

  function seguir() {
    if (quieto) { viento = objetivo; pintar(); return; }
    if (cuadro === null && visible && !document.hidden) {
      antes = 0;
      cuadro = requestAnimationFrame(paso);
    }
  }

  function fijar(v) {
    objetivo = Math.max(0, Math.min(15, v));
    numeros();
    if (quieto) seguir();
  }

  function rotuloPausa() { pausa.textContent = quieto ? 'Animar' : 'Pausar'; }

  control.addEventListener('input', function () {
    manual = true;
    fijar(Number(control.value));
  });

  /* Con mouse alcanza con moverlo sobre el dibujo. El control toma el mando apenas se lo usa. */
  caja.addEventListener('pointermove', function (ev) {
    if (manual || quieto || ev.pointerType !== 'mouse') return;
    var r = caja.getBoundingClientRect();
    fijar(Math.round((ev.clientX - r.left) / r.width * 30) / 2);
    control.value = objetivo;
  });

  pausa.addEventListener('click', function () {
    quieto = !quieto;
    rotuloPausa();
    seguir();
  });

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (e) {
      visible = e[0].isIntersecting;
      if (visible) seguir();
    }).observe(ventana);
  }
  document.addEventListener('visibilitychange', seguir);

  if ('ResizeObserver' in window) {
    new ResizeObserver(function () {
      var r = caja.getBoundingClientRect();
      if (Math.round(r.width) === W && Math.round(r.height) === H) return;
      armar();
      pintar();
    }).observe(caja);
  }

  armar();
  numeros();
  rotuloPausa();
  pintar();
  seguir();
})();
