
(function () {
  try {
    var html = document.documentElement;
    var DEF = { theme: 'inema-dark', font: 'inter', fontScale: 100, lineWidth: 68, leading: 1.7, accent: 'emerald' };
    function clone(o) { var r = {}; for (var x in o) r[x] = o[x]; return r; }
    var p = clone(DEF);
    try {
      var raw = localStorage.getItem('inema.prefs');
      if (raw) {
        var parsed = JSON.parse(raw);
        if (parsed && typeof parsed === 'object') {
          for (var k in DEF) if (parsed[k] != null) p[k] = parsed[k];
        }
      } else {
        // fallback ao tema legado do v1
        var legacy = localStorage.getItem('theme');
        if (legacy === 'light') p.theme = 'claro';
        else if (legacy === 'dark') p.theme = 'inema-dark';
      }
    } catch (e) { p = clone(DEF); }

    // mapa tema -> (.dark on/off, data-theme, color-scheme)
    var THEMES = {
      'inema-dark': { dark: true,  attr: null,        cs: 'dark'  },
      'claro':      { dark: false, attr: null,        cs: 'light' },
      'sepia':      { dark: false, attr: 'sepia',     cs: 'light' },
      'foco':       { dark: null,  attr: 'foco',      cs: null    },  // herda eixo atual
      'contraste':  { dark: true,  attr: 'contraste', cs: 'dark'  }
    };
    var t = THEMES[p.theme] || THEMES['inema-dark'];

    if (t.dark === true) html.classList.add('dark');
    else if (t.dark === false) html.classList.remove('dark');
    // 'foco' (null) preserva o que ja houver no atributo class do <html>

    if (t.attr) html.setAttribute('data-theme', t.attr);
    else html.removeAttribute('data-theme');

    html.style.colorScheme = (t.cs ? t.cs : (html.classList.contains('dark') ? 'dark' : 'light'));

    html.setAttribute('data-font', p.font || 'inter');
    html.setAttribute('data-accent', p.accent || 'emerald');

    // variaveis de leitura (espelham learn.js / learn.css) ANTES do paint
    var s = html.style;
    var scale = (+p.fontScale || 100);
    s.setProperty('--inema-font-scale', (scale / 100).toString());
    s.setProperty('font-size', scale + '%');               // :root em %, nunca px
    s.setProperty('--measure', (+p.lineWidth || 68) + 'ch');
    s.setProperty('--lh-body', (+p.leading || 1.7).toString());
    var fam = p.font === 'system'
      ? 'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif'
      : (p.font === 'leitura'
        ? '"Atkinson Hyperlegible", "Inter", system-ui, sans-serif'
        : '"Inter", system-ui, sans-serif');
    s.setProperty('--font-body', fam);

    var ACC = {
      emerald: [152, 76, 45], blue: [217, 91, 60], purple: [258, 90, 66],
      amber: [38, 92, 50], teal: [174, 72, 41], rose: [350, 89, 60]
    };
    var a = ACC[p.accent] || ACC.emerald;
    s.setProperty('--accent-h', a[0] + '');
    s.setProperty('--accent-s', a[1] + '%');
    s.setProperty('--accent-l', a[2] + '%');
    s.setProperty('--accent', 'hsl(' + a[0] + ' ' + a[1] + '% ' + a[2] + '%)');
  } catch (err) {
    // qualquer falha => default dark, preserva a marca
    try { document.documentElement.classList.add('dark'); document.documentElement.style.colorScheme = 'dark'; } catch (e) {}
  }
})();
