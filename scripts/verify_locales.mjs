import {chromium} from 'playwright';
import {readFileSync,writeFileSync,existsSync} from 'node:fs';
import {resolve,dirname} from 'node:path';
import {createServer} from 'node:http';
import assert from 'node:assert/strict';
const root=resolve('.'),cfg=JSON.parse(readFileSync('i18n/config.json'));
const server=createServer((req,res)=>{let name=decodeURIComponent(req.url.split('?')[0]);if(name.endsWith('/'))name+='index.html';let p=resolve(root,'.'+name);if(!p.startsWith(root+'/')||!existsSync(p)){res.writeHead(404);return res.end();}res.setHeader('Content-Type',({html:'text/html;charset=utf-8',js:'application/javascript',css:'text/css'})[p.split('.').pop()]||'application/octet-stream');res.end(readFileSync(p));});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base=`http://127.0.0.1:${server.address().port}`;
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/home/nmaldaner/.cache/ms-playwright/chromium-1234/chrome-linux/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext(),p=await context.newPage(),errors=[],svgIssues=[];p.on('pageerror',e=>errors.push(e.message));let checked=0,links=0;
try{
for(const lang of ['pt','en','es']){
const prefix=lang==='pt'?'':lang+'/';
for(const file of cfg.pages){
 await p.setViewportSize({width:1440,height:1000});await p.goto(base+'/'+prefix+file);await p.waitForFunction(()=>window.INEMA);
 assert.equal(await p.locator('html').getAttribute('lang'),lang==='pt'?'pt-BR':lang);
 assert.equal(await p.evaluate(()=>INEMA.progress('curso').total),48);
 assert.equal(await p.locator('[data-course-languages] a').count(),3);
 for(const href of await p.locator('a[href],script[src],link[href]').evaluateAll(els=>els.map(x=>x.getAttribute('href')||x.getAttribute('src')))){
  if(/^(https?:|data:|mailto:)/.test(href))continue;
  const [dest,hash]=href.split('#'),target=dest?resolve(root,prefix,dirname(file),dest):resolve(root,prefix,file);
  assert.ok(existsSync(target),`broken ${prefix+file} -> ${href}`);links++;
  if(hash&&target.endsWith('.html'))assert.ok(readFileSync(target,'utf8').includes(`id="${hash}"`));
 }
 assert.ok(!/⟪P\d+⟫/.test(await p.locator('body').innerText()));
 const overflow=await p.locator('svg[role="img"] text').evaluateAll(nodes=>nodes.flatMap(t=>{const b=t.getBBox(),v=t.ownerSVGElement.viewBox.baseVal;return b.x< -1||b.x+b.width>v.width+1?[t.textContent]:[]}));
 if(overflow.length)svgIssues.push({file:prefix+file,overflow});
 await p.setViewportSize({width:390,height:844});assert.ok(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),prefix+file+' mobile overflow');checked++;
}
await p.goto(base+'/'+prefix+'curso/trilha1/modulo-1-1.html');
assert.equal(await p.locator('[data-inema-read-toggle]').first().getAttribute('aria-pressed'),'false');
await p.locator('[data-inema-read-toggle]').first().click();
assert.equal(await p.locator('[data-inema-read-toggle]').first().getAttribute('aria-pressed'),'true');
await p.evaluate(()=>{const n=document.querySelector('[data-inema-block]');const r=document.createRange();r.setStart(n.firstChild,0);r.setEnd(n.firstChild,10);INEMA.highlight(r,{color:'yellow',note:'locale note'});});
await p.reload();assert.ok(await p.locator('mark.inema-hl').count()>0);
let state=await p.evaluate(()=>JSON.parse(INEMA.exportJSON()));assert.equal(state.courseId,'agent-skills-codex'+(lang==='pt'?'':'-'+lang));
assert.ok(await p.evaluate(()=>!INEMA.importJSON(JSON.stringify({schemaVersion:1,courseId:'different-course',read:{}})).ok));
await p.goto(base+'/'+prefix+'index.html');await p.screenshot({path:`verificacao/i18n/${lang}-mobile.png`});
}
await p.goto(base+'/en/curso/trilha2/modulo-2-2.html#topico-2');await p.locator('[data-course-languages] a[lang="es"]').click();assert.ok(p.url().endsWith('/es/curso/trilha2/modulo-2-2.html#topico-2'));
await p.setViewportSize({width:1440,height:1000});await p.screenshot({path:'verificacao/i18n/es-module.png'});
assert.deepEqual(errors,[]);assert.deepEqual(svgIssues,[]);
writeFileSync('verificacao/i18n/browser.json',JSON.stringify({pages:checked,links,errors,svgIssues,languageSwitch:true,isolatedProgress:true,persistentNotes:true},null,2));console.log({pages:checked,links,errors,svgIssues});
}finally{await browser.close();server.close();}
