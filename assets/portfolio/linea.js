/* Portada: una línea de alta tensión al atardecer. El viento enfría el conductor. */
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
  var portada = lienzo.parentElement;
  var control = document.getElementById('viento');
  var pausa = document.getElementById('pausa');
  var salidaViento = document.getElementById('v-viento');
  var salidaCorriente = document.getElementById('v-corriente');
  var salidaTemp = document.getElementById('v-temp');

  var fondo = document.createElement('canvas');
  var frente = document.createElement('canvas');
  var W, H, DPR, horizonte;
  var torres = [], vanos = [], molinos = [], pasto = [], rafagas = [];
  var objetivo = Number(control.value);
  var viento = objetivo;
  var manual = false;
  var visible = true;
  var cuadro = null;
  var antes = 0;
  var fase = 0, recorrido = 0, giro = 0;
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

  /* De verde frío a cobre y a rojo, según la temperatura */
  function color(t, alfa) {
    var p = [[29, 130, 235, 196], [38, 190, 225, 170], [50, 240, 185, 110], [70, 255, 125, 70], [85, 255, 72, 60]];
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

  function capa(c) {
    c.width = lienzo.width;
    c.height = lienzo.height;
    var x = c.getContext('2d');
    x.setTransform(DPR, 0, 0, DPR, 0, 0);
    return x;
  }

  function pintarFondo() {
    var c = capa(fondo);
    var r = azar(132);
    var cielo = c.createLinearGradient(0, 0, 0, horizonte);
    cielo.addColorStop(0, '#040f10');
    cielo.addColorStop(0.42, '#0a2926');
    cielo.addColorStop(0.74, '#2f5a4b');
    cielo.addColorStop(0.92, '#b5794c');
    cielo.addColorStop(1, '#eba766');
    c.fillStyle = cielo;
    c.fillRect(0, 0, W, horizonte + 2);

    for (var i = 0; i < W * H / 6500; i++) {
      var y = r() * horizonte * 0.62;
      c.fillStyle = 'rgba(225,245,235,' + (0.65 * r() * (1 - y / horizonte)) + ')';
      var d = r() < 0.92 ? 1 : 2;
      c.fillRect(r() * W, y, d, d);
    }

    var sx = W * 0.6, sr = Math.min(W, H) * 0.075;
    var brillo = c.createRadialGradient(sx, horizonte, 0, sx, horizonte, sr * 7);
    brillo.addColorStop(0, 'rgba(255,214,150,.75)');
    brillo.addColorStop(0.2, 'rgba(250,170,100,.3)');
    brillo.addColorStop(1, 'rgba(250,170,100,0)');
    c.fillStyle = brillo;
    c.fillRect(0, 0, W, horizonte);
    c.fillStyle = '#ffd9a0';
    c.beginPath();
    c.arc(sx, horizonte - sr * 0.1, sr, 0, Math.PI * 2);
    c.fill();

    /* Mesetas */
    [['#3b5547', 0.06, 3.1], ['#1d3a31', 0.035, 7.7], ['#0d231e', 0.014, 12.4]].forEach(function (m) {
      c.fillStyle = m[0];
      c.beginPath();
      c.moveTo(0, H);
      for (var x = 0; x <= W + 8; x += 8) {
        var u = x / Math.max(W, 700);
        var ola = Math.sin(u * m[2] + m[2]) + 0.45 * Math.sin(u * m[2] * 2.7);
        c.lineTo(x, horizonte + 3 - H * m[1] * Math.max(0, Math.min(0.75, ola)));
      }
      c.lineTo(W + 8, H);
      c.closePath();
      c.fill();
    });

    var suelo = c.createLinearGradient(0, horizonte, 0, H);
    suelo.addColorStop(0, '#0d231e');
    suelo.addColorStop(1, '#040c0a');
    c.fillStyle = suelo;
    c.fillRect(0, horizonte + 3, W, H);
  }

  function pintarTorre(c, t) {
    var h = t.alto, x = t.x, y = t.base;
    function semi(f) {
      if (f < 0.62) return h * (0.12 - 0.087 * f / 0.62);
      return h * Math.max(0.004, 0.033 - 0.029 * (f - 0.62) / 0.38);
    }
    c.strokeStyle = '#030b09';
    c.lineCap = 'round';
    c.lineWidth = Math.max(0.6, h * 0.0075);
    c.beginPath();
    [-1, 1].forEach(function (s) {
      c.moveTo(x + s * semi(0), y);
      c.lineTo(x + s * semi(0.62), y - h * 0.62);
      c.lineTo(x + s * semi(1), y - h);
    });
    c.stroke();

    c.lineWidth = Math.max(0.35, h * 0.0032);
    c.beginPath();
    var niveles = [0, 0.16, 0.3, 0.42, 0.53, 0.62, 0.69, 0.76, 0.83, 0.89, 0.95];
    for (var i = 1; i < niveles.length; i++) {
      var a = semi(niveles[i - 1]), b = semi(niveles[i]);
      var ya = y - h * niveles[i - 1], yb = y - h * niveles[i];
      c.moveTo(x - a, ya); c.lineTo(x + b, yb);
      c.moveTo(x + a, ya); c.lineTo(x - b, yb);
      c.moveTo(x - b, yb); c.lineTo(x + b, yb);
    }
    c.stroke();

    t.puntos = [];
    [[0.68, 0.16], [0.785, 0.138], [0.885, 0.115]].forEach(function (m) {
      [-1, 1].forEach(function (s) {
        var px = x + s * h * m[1], py = y - h * m[0];
        c.lineWidth = Math.max(0.5, h * 0.005);
        c.beginPath();
        c.moveTo(x + s * semi(m[0]), py); c.lineTo(px, py);
        c.lineTo(x + s * semi(m[0] + 0.045), py - h * 0.045);
        c.stroke();
        c.lineWidth = Math.max(0.6, h * 0.009);
        c.beginPath();
        c.moveTo(px, py); c.lineTo(px, py + h * 0.035);
        c.stroke();
        t.puntos.push([px, py + h * 0.035]);
      });
    });
  }

  function armar() {
    var caja = portada.getBoundingClientRect();
    W = Math.round(caja.width);
    H = Math.round(caja.height);
    DPR = Math.min(window.devicePixelRatio || 1, 1.6);
    lienzo.width = W * DPR;
    lienzo.height = H * DPR;
    g.setTransform(DPR, 0, 0, DPR, 0, 0);

    var angosto = W < 760;
    horizonte = H * (angosto ? 0.64 : 0.72);

    /* Torres equiespaciadas, en perspectiva hacia el punto de fuga */
    var fugaX = W * (angosto ? 0.22 : 0.43);
    var avanceX = W * (angosto ? 0.68 : 0.45);
    var altoCerca = Math.min(H * (angosto ? 0.47 : 0.72), W * (angosto ? 1.1 : 0.62));
    torres = [];
    for (var i = 15; i >= 0; i--) {
      var z = i === 0 ? 0.5 : 1 + (i - 1) * 0.95;
      torres.push({ x: fugaX + avanceX / z, base: horizonte + (H - horizonte) * 0.96 / z, alto: altoCerca / z, z: z });
    }

    pintarFondo();
    var cf = capa(frente);
    torres.forEach(function (t) { pintarTorre(cf, t); });

    vanos = [];
    for (var j = 1; j < torres.length; j++) {
      var a = torres[j - 1], b = torres[j];
      for (var k = 0; k < 6; k++) {
        vanos.push({
          a: a.puntos[k], b: b.puntos[k], k: k, n: j, z: b.z,
          flecha: (a.alto + b.alto) * 0.036, ancho: Math.max(0.45, Math.min(2.2, 1.9 / b.z))
        });
      }
    }

    var r = azar(601);
    molinos = [];
    var cuantos = angosto ? 4 : 8;
    for (var m = 0; m < cuantos; m++) {
      molinos.push({ x: W * (0.04 + 0.4 * (m + r() * 0.6) / cuantos), alto: H * (0.03 + 0.032 * r()), f: r() * 6.28 });
    }

    pasto = [];
    for (var p = 0; p < Math.min(700, W * 0.55); p++) {
      var prof = Math.pow(r(), 0.6);
      pasto.push({ x: r() * W, y: horizonte + 8 + prof * (H - horizonte), l: 2 + prof * prof * 22, f: r() * 6.28 });
    }

    rafagas = [];
    for (var q = 0; q < (angosto ? 35 : 80); q++) {
      rafagas.push({ x: r() * W, y: r() * H * 0.92, v: 0.5 + r(), f: r() * 6.28 });
    }
  }

  function pintar() {
    var e = estado(viento);
    g.drawImage(fondo, 0, 0, W, H);

    g.strokeStyle = 'rgba(200,222,205,.62)';
    g.lineWidth = 1.1;
    g.beginPath();
    molinos.forEach(function (m) {
      var y = horizonte - m.alto;
      g.moveTo(m.x, horizonte + 3); g.lineTo(m.x, y);
      for (var i = 0; i < 3; i++) {
        var a = giro + m.f + i * 2.094;
        g.moveTo(m.x, y); g.lineTo(m.x + Math.cos(a) * m.alto * 0.48, y + Math.sin(a) * m.alto * 0.48);
      }
    });
    g.stroke();

    g.drawImage(frente, 0, 0, W, H);

    var cable = color(e.grados, 0.85), halo = color(e.grados, 0.1), punto = color(e.grados, 1);
    vanos.forEach(function (v) {
      var vaiven = Math.sin(fase * 1.4 + v.n + v.k * 0.4) * viento * 0.22 / v.z;
      var cx = (v.a[0] + v.b[0]) / 2 + vaiven;
      var cy = (v.a[1] + v.b[1]) / 2 + v.flecha * 2;
      g.beginPath();
      g.moveTo(v.a[0], v.a[1]);
      g.quadraticCurveTo(cx, cy, v.b[0], v.b[1]);
      g.strokeStyle = halo;
      g.lineWidth = v.ancho * 6;
      g.stroke();
      g.strokeStyle = cable;
      g.lineWidth = v.ancho;
      g.stroke();

      if (v.z < 10) {
        var u = (recorrido + v.n * 0.31 + Math.floor(v.k / 2) / 3) % 1, w = 1 - u;
        var px = w * w * v.a[0] + 2 * w * u * cx + u * u * v.b[0];
        var py = w * w * v.a[1] + 2 * w * u * cy + u * u * v.b[1];
        g.fillStyle = halo;
        g.beginPath(); g.arc(px, py, v.ancho * 6, 0, 6.283); g.fill();
        g.fillStyle = punto;
        g.beginPath(); g.arc(px, py, v.ancho * 1.5, 0, 6.283); g.fill();
      }
    });

    g.strokeStyle = 'rgba(150,180,140,.3)';
    g.lineWidth = 1;
    g.beginPath();
    pasto.forEach(function (p) {
      var i = Math.min(1.25, viento * 0.07 + Math.sin(fase * 3 + p.f) * (0.05 + viento * 0.009));
      g.moveTo(p.x, p.y);
      g.quadraticCurveTo(p.x, p.y - p.l * 0.6, p.x + Math.sin(i) * p.l, p.y - Math.cos(i) * p.l);
    });
    g.stroke();

    if (viento > 0.2) {
      g.strokeStyle = 'rgba(215,242,228,' + Math.min(0.2, 0.025 + viento * 0.012) + ')';
      g.beginPath();
      rafagas.forEach(function (r) {
        var largo = 8 + viento * 9 * r.v, onda = Math.sin(fase + r.f) * 5;
        g.moveTo(r.x - largo, r.y);
        g.quadraticCurveTo(r.x - largo / 2, r.y + onda, r.x, r.y);
      });
      g.stroke();
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
    giro += dt * Math.min(viento, 12) * 0.32;
    recorrido = (recorrido + dt * estado(viento).amperes / 2400) % 1;
    rafagas.forEach(function (r) {
      r.x += dt * viento * 38 * r.v;
      if (r.x > W + 120) r.x = -10;
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

  function rotuloPausa() {
    pausa.textContent = quieto ? 'Animar' : 'Pausar';
  }

  control.addEventListener('input', function () {
    manual = true;
    fijar(Number(control.value));
  });

  /* Con mouse alcanza con moverlo. El control toma el mando apenas se lo usa. */
  portada.addEventListener('pointermove', function (ev) {
    if (manual || quieto || ev.pointerType !== 'mouse' || ev.target.closest('.medidor, a, button')) return;
    fijar(Math.round(ev.clientX / W * 30) / 2);
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
    }).observe(portada);
  }
  document.addEventListener('visibilitychange', seguir);

  if ('ResizeObserver' in window) {
    new ResizeObserver(function () {
      var c = portada.getBoundingClientRect();
      if (Math.round(c.width) === W && Math.round(c.height) === H) return;
      armar();
      pintar();
    }).observe(portada);
  }

  armar();
  numeros();
  rotuloPausa();
  pintar();
  seguir();
})();
