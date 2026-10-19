// Draw every pictogram row from its data-n counts, then reveal rows on one shared clock as they enter the viewport.
(function () {
  var staticMode = /[?&]static=1/.test(location.search) || (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  var figs = document.querySelectorAll('.figs');
  figs.forEach(function (row) {
    var isCoin = row.classList.contains('figs-coin');
    var isEmpty = row.classList.contains('empty');
    var i = 0;
    row.querySelectorAll('.grp').forEach(function (g) {
      var n = parseInt(g.getAttribute('data-n') || '0', 10);
      var frac = g.getAttribute('data-frac');
      var sym = isCoin ? (frac ? '#p-coin' : '#p-coin') : (g.classList.contains('g-open') ? '#p-seat-open' : '#p-seat');
      var html = '';
      for (var k = 0; k < n; k++) {
        html += '<svg style="--i:' + (i++) + '" aria-hidden="true"><use href="' + sym + '"></use></svg>';
      }
      g.innerHTML = html;
      if (frac) g.style.setProperty('--frac', frac);
      g.setAttribute('tabindex', '0');
      g.setAttribute('role', 'img');
      g.setAttribute('aria-label', g.getAttribute('data-label') || '');
    });
    if (isEmpty) row.classList.add('on');
  });
  if (staticMode || !('IntersectionObserver' in window)) { figs.forEach(function (r) { r.classList.add('on'); }); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('on'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px' });
  figs.forEach(function (r) { io.observe(r); });
})();
