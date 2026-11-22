(function () {
  var raiz = document.documentElement;
  var boton = document.getElementById('tema');

  function aplicar(oscuro) {
    if (oscuro) raiz.dataset.tema = 'oscuro';
    else delete raiz.dataset.tema;
    boton.textContent = oscuro ? 'Modo claro' : 'Modo oscuro';
  }

  var guardado = null;
  try { guardado = localStorage.getItem('portfolio-tema'); } catch (e) { /* sin almacenamiento */ }
  aplicar(guardado === 'oscuro');

  boton.addEventListener('click', function () {
    var oscuro = raiz.dataset.tema !== 'oscuro';
    aplicar(oscuro);
    try { localStorage.setItem('portfolio-tema', oscuro ? 'oscuro' : 'claro'); } catch (e) { /* sin almacenamiento */ }
  });
})();
