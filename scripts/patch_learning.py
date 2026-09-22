from pathlib import Path
p=Path('assets/learn.js');s=p.read_text()
if 'function navigateToCourseAnchor' in s:
    raise SystemExit('Correções já presentes; nenhuma alteração necessária.')
s=s.replace("var main = document.querySelector('main') || document.body;",'var main = document.body;')
s=s.replace("    main.addEventListener('click', onMainClick);", "    main.addEventListener('click', onMainClick);\n    var themeButton = document.getElementById('theme-toggle');\n    if (themeButton) themeButton.addEventListener('click', function () { setPref('theme', document.documentElement.classList.contains('dark') ? 'claro' : 'inema-dark'); });")
# Resolve cross-page destinations from the trusted course manifest, not imported URLs.
helper='''  function navigateToCourseAnchor(anchor, blockId) {
    var match = String(anchor || '').match(/^modulo-(\\d+-\\d+)#(topico-\\d+)$/);
    if (!match && blockId) {
      var b = String(blockId).match(/^m(\\d+-\\d+)-t(\\d+)-/);
      if (b) match = [b[0], b[1], 'topico-' + b[2]];
    }
    if (!match) return false;
    var mods = manifestModules();
    for (var i = 0; i < mods.length; i++) {
      if (mods[i].id !== match[1] || !mods[i].href) continue;
      var meta = document.querySelector('meta[name="course-root"]');
      var base = new URL(meta ? meta.content : './', window.location.href);
      var url = new URL(mods[i].href, base);
      url.hash = blockId || match[2];
      window.location.href = url.href;
      return true;
    }
    return false;
  }

'''
s=s.replace('  function jumpTo(item) {',helper+'  function jumpTo(item) {')
s=s.replace('      flashTarget(target);\n    }\n  }\n\n  function openAncestors',"      flashTarget(target);\n    } else { navigateToCourseAnchor(item.kind === 'topic' ? item.id : null, item.blockId); }\n  }\n\n  function openAncestors")
s=s.replace("    // fallback best-effort por scroll cru\n    if (typeof meta.lastScroll === 'number') {\n      try { window.scrollTo(0, meta.lastScroll); return true; } catch (e) {}\n    }", "    if (anchor) return navigateToCourseAnchor(anchor); // stable cross-page anchor")
# No checkpoint outside real topic pages; do not clobber last lesson at the homepage.
s=s.replace("    debounce('checkpoint', function () {\n      var meta = getMeta();", "    if (!topicId && !topicEls().length) return;\n    debounce('checkpoint', function () {\n      var meta = getMeta();")
# Notes from other pages are not orphaned merely because current page lacks that block.
s=s.replace('      // ordena por offset desc p/ nao invalidar offsets ao inserir marks', '      if (!block) continue; // Other course pages own their blocks.\n      // ordena por offset desc p/ nao invalidar offsets ao inserir marks')
# export unknown top-level data in a dedicated persisted namespace.
s=s.replace('    return {\n      schemaVersion: SCHEMA_VERSION,\n      courseId: S.courseId,\n      exportedAt:', "    return Object.assign({}, storageGet(key('extra'), {}), {\n      schemaVersion: SCHEMA_VERSION,\n      courseId: S.courseId,\n      exportedAt:")
s=s.replace('      meta: getMeta()\n    };\n  }\n\n  function exportJSON', '      meta: getMeta()\n    });\n  }\n\n  function exportJSON')
a=s.index("    if (typeof parsed.schemaVersion !== 'number'");b=s.index('    var incoming = migrate(parsed);',a)
s=s[:a]+'''    function object(v) { return !!v && typeof v === 'object' && !Array.isArray(v); }
    function safeKeys(v) {
      if (!v || typeof v !== 'object') return true;
      return Object.keys(v).every(function (k) { return k !== '__proto__' && k !== 'constructor' && k !== 'prototype' && safeKeys(v[k]); });
    }
    var valid = object(parsed) && Number.isInteger(parsed.schemaVersion) && parsed.schemaVersion === SCHEMA_VERSION && parsed.courseId === S.courseId && safeKeys(parsed);
    ['read','doubts','notes','checks','meta'].forEach(function (k) { if (parsed[k] != null && !object(parsed[k])) valid = false; });
    if (valid) {
      Object.keys(parsed.read || {}).forEach(function (k) { if (typeof parsed.read[k] !== 'boolean') valid = false; });
      Object.keys(parsed.doubts || {}).forEach(function (k) { if (!object(parsed.doubts[k])) valid = false; });
      Object.keys(parsed.checks || {}).forEach(function (k) { if (!object(parsed.checks[k])) valid = false; });
      Object.keys(parsed.notes || {}).forEach(function (k) {
        var arr = parsed.notes[k];
        if (!Array.isArray(arr)) { valid = false; return; }
        arr.forEach(function (n) {
          if (!object(n) || typeof n.id !== 'string' || typeof n.quote !== 'string' || SWATCHES.indexOf(n.color) < 0 || (n.note != null && typeof n.note !== 'string')) valid = false;
          if (n.anchor != null && (!object(n.anchor) || !Number.isInteger(n.anchor.startOffset) || !Number.isInteger(n.anchor.endOffset) || n.anchor.startOffset < 0 || n.anchor.endOffset < n.anchor.startOffset)) valid = false;
        });
      });
    }
    if (!valid) { res.errors.push('Arquivo incompatível: curso, versão ou estrutura inválida.'); return res; }
    var extra = storageGet(key('extra'), {});
    Object.keys(parsed).forEach(function (k) { if (['schemaVersion','courseId','exportedAt','read','doubts','notes','checks','meta'].indexOf(k) < 0) extra[k] = parsed[k]; });

'''+s[b:]
s=s.replace('      res.applied = countItems(incoming);','      storageSet(key(\'extra\'), extra);\n      rehydrateAll();\n      res.applied = countItems(incoming);')
s=s.replace('    res.ok = true;\n    return res;\n  }\n\n  function countItems',"    storageSet(key('extra'), extra);\n    rehydrateAll();\n    res.ok = true;\n    return res;\n  }\n\n  function countItems")
s=s.replace("    rawRemove(key('meta'));", "    rawRemove(key('meta'));\n    rawRemove(key('extra'));")
p.write_text(s)
p=Path('scripts/verify.mjs');s=p.read_text().replace('chromium-1243/chrome-linux64/chrome','chromium-1234/chrome-linux/chrome');p.write_text(s)
# notes link targets need ids as well as data attributes
p=Path('scripts/build_course.py');s=p.read_text().replace('data-inema-block="{bid}-p1"','id="{bid}-p1" data-inema-block="{bid}-p1"').replace('data-inema-block="{bid}-p2"','id="{bid}-p2" data-inema-block="{bid}-p2"');p.write_text(s)
