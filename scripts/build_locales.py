#!/usr/bin/env python3
"""Offline full-course localization. API acquisition is a separate opt-in script.
IDs, code, data fixtures, and source PT are preserved. Requires beautifulsoup4.
"""
from pathlib import Path
from bs4 import BeautifulSoup,Comment,Doctype,NavigableString
import json,re,hashlib,html,subprocess,shutil,os,sys
VERSION='course-i18n-1.0.0'
CAT={};ACTIONS=[]
def key(s):return hashlib.sha256((VERSION+'\0'+s).encode()).hexdigest()[:24]
def unit(s,setter,markup=False,markdown=False):
 if not s:return
 lead=re.match(r'^\s*',s).group();tail=re.search(r'\s*$',s).group();v=s.strip();protected=[]
 def mask(m):protected.append(m.group());return '⟪P'+str(len(protected)-1)+'⟫'
 if markup:v=re.sub(r'<(?:code|pre)\b[^>]*>.*?</(?:code|pre)>|<[^>]*>',mask,v,flags=re.S)
 if markdown:v=re.sub(r'```.*?```|`[^`\n]+`|(?<=\]\()[^)]+(?=\))',mask,v,flags=re.S)
 v=re.sub(r'https?://[^\s<>]+|\b(?:CLAUDE|AGENTS|README)\.md\b',mask,v)
 v=re.sub(r'(?<![\w])(?:[~.]?/)?(?:[\w.-]+/)+[\w.*-]*|\b[\w.-]+\.(?:md|csv|json|py|html|yaml|toml|js|zip)\b|\$[a-z][a-z0-9-]+|\bSKILL\.md\b',mask,v)
 v=html.unescape(v) if markup else v
 if not re.search(r'[A-Za-zÀ-ÿ]',re.sub(r'⟪P\d+⟫','',v)):return
 if v in ['INEMA.CLUB','INEMA.PRO','INEMA','Laya','Jev','TypeSafe','Python','JSON','HTML','API','GitHub','Claude','Codex']:return
 k=key(v);CAT[k]=v
 def apply(value):
  if markup:value=html.escape(html.unescape(value),quote=False)
  for i,t in enumerate(protected):value=value.replace('⟪P'+str(i)+'⟫',t)
  setter(lead+value+tail)
 ACTIONS.append((k,apply))
def json_units(obj):
 if isinstance(obj,list):
  for x in obj:json_units(x)
 elif isinstance(obj,dict):
  for k,v in obj.items():
   if k in ['title','q','question','front','back','explanation','feedback','description'] and isinstance(v,str):unit(v,lambda t,o=obj,k=k:o.__setitem__(k,t))
   elif k=='explain' and isinstance(v,dict):
    for answer,text in v.items():
     if isinstance(text,str):unit(text,lambda t,o=v,a=answer:o.__setitem__(a,t))
   elif k=='options' and isinstance(v,list):
    for i,t in enumerate(v):
     if isinstance(t,str):unit(t,lambda s,o=v,i=i:o.__setitem__(i,s))
     else:json_units(t)
   elif isinstance(v,(list,dict)):json_units(v)
def code_or_prose(text,setter):
 # Localize educational prompts; retain executable commands and data contracts.
 executable=bool(re.search(r'(?m)^\s*(?:from |import |def |if |else:|return |git |cd |python3 |curl |source |flowchart |[A-Za-z_]+\s*=|[{}]|"[^"\n]+"\s*:)',text))
 if not executable:unit(text,setter,markdown=True);return
 lines=text.splitlines(keepends=True)
 for i,line in enumerate(lines):
  m=re.match(r'^(\s*# ?)([^!].*?)(\n?)$',line)
  if m:unit(m[2],lambda t,i=i,m=m:lines.__setitem__(i,m[1]+t+m[3]))
 ACTIONS.append((None,lambda _:setter(''.join(lines))))
def soup_units(s):
 selected=set()
 for e in s.find_all(['h1','h2','h3','h4','h5','h6','p','li','summary','button','label','a','figcaption','td','th','span','strong','em','text','title','small','option','div','footer']):
  if any(id(p) in selected for p in e.parents) or e.find_parent(['script','style','code','pre']):continue
  if e.find(['div','p','ul','ol','li','button','svg','input','textarea','section','h1','h2','h3','table']):continue
  if not e.get_text(strip=True):continue
  selected.add(id(e))
  def setter(t,e=e):
   frag=BeautifulSoup(t,'html.parser');e.clear()
   for n in list(frag.contents):e.append(n)
  unit(e.decode_contents(),setter,markup=True)
 for n in list(s.find_all(string=True)):
  if isinstance(n,(Comment,Doctype)) or n.find_parent(['script','style','code','pre']) or any(id(p) in selected for p in n.parents):continue
  unit(str(n),lambda t,n=n:n.replace_with(NavigableString(t)))
 for pre in s.find_all('pre'):
  code=pre.find('code');target=code if code else pre
  code_or_prose(target.get_text(),lambda t,target=target:setattr(target,'string',t))
 for e in s.find_all(True):
  for a in ['alt','title','aria-label','placeholder','data-fb','data-cap','data-def']:
   if e.get(a):unit(e[a],lambda t,e=e,a=a:e.__setitem__(a,t))
  if e.name=='meta' and (e.get('name')=='description' or e.get('property') in ['og:title','og:description']):unit(e['content'],lambda t,e=e:e.__setitem__('content',t))
  if e.get('data-check-definition'):
   o=json.loads(e['data-check-definition']);json_units(o);ACTIONS.append((None,lambda _,e=e,o=o:e.__setitem__('data-check-definition',json.dumps(o,ensure_ascii=False))))
 for e in s.select('script[type="application/json"]'):
  o=json.loads(e.string);json_units(o);ACTIONS.append((None,lambda _,e=e,o=o:setattr(e,'string',json.dumps(o,ensure_ascii=False))))
def pages(root):
 return [root/x for x in json.loads((root/'i18n/config.json').read_text())['pages']]
def langnav(s,root,rel,lang):
 for e in s.select('[data-course-languages],#course-language-css,script[data-course-language-hash],link[rel="canonical"],link[rel="alternate"][hreflang]'):e.decompose()
 base='https://inematds.github.io/'+root.name+'/'
 current=root/(lang if lang!='pt' else '')/rel
 nav=s.new_tag('nav',attrs={'data-course-languages':'','aria-label':{'pt':'Idioma do curso','en':'Course language','es':'Idioma del curso'}[lang]})
 for code,label in [('pt','Português'),('en','English'),('es','Español')]:
  folder='' if code=='pt' else code+'/'
  url=base+folder+rel.as_posix();loc='pt-BR' if code=='pt' else code
  s.head.append(s.new_tag('link',rel='alternate',hreflang=loc,href=url))
  a=s.new_tag('a',href=os.path.relpath(root/folder/rel,current.parent),hreflang=loc,lang=loc);a.string=label
  if code==lang:a['aria-current']='page'
  nav.append(a)
 s.head.append(s.new_tag('link',rel='alternate',hreflang='x-default',href=base+rel.as_posix()))
 s.head.append(s.new_tag('link',rel='canonical',href=base+('' if lang=='pt' else lang+'/')+rel.as_posix()))
 style=s.new_tag('style',id='course-language-css');style.string='[data-course-languages]{position:fixed;bottom:0;left:0;right:0;z-index:60;display:flex;gap:1.25rem;padding:.65rem;justify-content:center;background:#111827;color:#f3f4f6}[data-course-languages] a{color:inherit;font:14px system-ui}[data-course-languages] [aria-current]{font-weight:bold;text-decoration:underline}[data-course-languages] a:focus-visible{outline:2px solid #38bdf8;outline-offset:4px}body{padding-bottom:75px}'
 s.head.append(style);s.body.append(nav)
 sc=s.new_tag('script',attrs={'data-course-language-hash':''});sc.string="document.querySelectorAll('[data-course-languages] a').forEach(function(a){a.addEventListener('click',function(){a.href=a.getAttribute('href').split('#')[0]+location.hash;});});";s.body.append(sc)
def collect(root,lang):
 global CAT,ACTIONS
 CAT={};ACTIONS=[];outputs={};cfg=json.loads((root/'i18n/config.json').read_text())
 for p in pages(root):
  s=BeautifulSoup(p.read_text(),'html.parser')
  for e in s.select('[data-course-languages],#course-language-css,script[data-course-language-hash]'):e.decompose()
  if lang!='pt':soup_units(s)
  outputs[p.relative_to(root)]=s
 for rel in cfg['markdown']:
  p=root/rel;parts=re.split(r'(\n\n)',p.read_text());holder=parts[:]
  # Fence-aware segmentation: protect complete fenced code, don't split it into translatable prose.
  parts=re.split(r'(```.*?```)',p.read_text(),flags=re.S);holder=parts[:]
  for i,part in enumerate(parts):
   if part.startswith('```'):
    first,body=part.split('\n',1) if '\n' in part else (part,'')
    if body.endswith('```'):code_or_prose(body[:-3],lambda t,holder=holder,i=i,first=first:holder.__setitem__(i,first+'\n'+t+'```'))
    continue
   chunks=re.split(r'(\n\n)',part);sub=chunks[:]
   for j,text in enumerate(chunks):
    if text.strip():unit(text,lambda t,sub=sub,j=j:sub.__setitem__(j,t),markdown=True)
   ACTIONS.append((None,lambda _,holder=holder,i=i,sub=sub:holder.__setitem__(i,''.join(sub))))
  outputs[Path(rel)]=holder
 ui=json.loads((root/f'i18n/ui-{lang}.json').read_text()) if lang!='pt' else {}
 for rel,tokens in cfg['js_tokens'].items():
  src=(root/rel).read_text();replacements={}
  if hashlib.sha256(src.encode()).hexdigest()!=cfg['js_hashes'][rel]:raise RuntimeError('Stale JS tokens: '+rel)
  for t in tokens:
   if t['value'] in ui:replacements[t['start']]=(t['end'],json.dumps(ui[t['value']],ensure_ascii=False))
  for start,(end,v) in sorted(replacements.items(),reverse=True):src=src[:start]+v+src[end:]
  if lang!='pt':
   labels={'en':{'todas':'all','yellow':'yellow','green':'green','blue':'blue','pink':'pink','doubt':'question'},'es':{'todas':'todos','yellow':'amarillo','green':'verde','blue':'azul','pink':'rosa','doubt':'duda'}}[lang]
   src=src.replace('o.textContent = c;', 'o.textContent = '+json.dumps(labels)+'[c] || c;')
   src=src.replace("'inema-journey__tag', 'duvida'","'inema-journey__tag', "+json.dumps('question' if lang=='en' else 'duda'))
   src=src.replace("courseId:'jev-curso'","courseId:'jev-curso-"+lang+"'")
   src=src.replace("toLocaleString('pt-BR'","toLocaleString('"+lang+"'")
  outputs[Path(rel)]=src
 return outputs
def build(root,lang):
 outputs=collect(root,lang);cache=json.loads((root/f'i18n/{lang}.json').read_text())
 review=root/f'i18n/review-{lang}.json'
 if review.exists():cache.update(json.loads(review.read_text()))
 missing=set(CAT)-set(cache)
 if missing:raise RuntimeError(f'{lang}: {len(missing)} missing translations')
 for k,f in ACTIONS:f(cache[k] if k else None)
 cfg=json.loads((root/'i18n/config.json').read_text());dst=root/lang
 for rel in cfg['copy']:
  p=dst/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/rel,p)
  if rel == 'assets/patches.css':
   hint={'en':' On mobile, swipe the diagram to see every step.','es':' En el móvil, desliza el diagrama para ver todas las etapas.'}[lang]
   p.write_text(p.read_text().replace(' No celular, deslize o diagrama para ver todas as etapas.',hint))
 for rel,obj in outputs.items():
  if isinstance(obj,BeautifulSoup):
   obj.html['lang']=lang
   meta=obj.select_one('meta[name="inema-course"],meta[name="curso"]')
   if meta:meta['content']=meta['content']+'-'+lang
   tag=obj.select_one('[data-inema-manifest]')
   if tag:
    o=json.loads(tag.string)
    if isinstance(o.get('course'),str):o['course']+='-'+lang
    elif isinstance(o.get('course'),dict):o['course']['id']+='-'+lang
    tag.string=json.dumps(o,ensure_ascii=False)
   for e in obj.select('[onclick]'):
    if 'openModal(' in e['onclick']:e['onclick']=e['onclick'].replace('Módulo ', 'Module ' if lang=='en' else 'Módulo ')
   langnav(obj,root,rel,lang)
   obj=re.sub(r"(?i)(<!doctype html>)\s*",r"\1\n",str(obj))
  elif isinstance(obj,list):obj=''.join(obj)
  p=dst/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(obj)
 print(root.name,lang,len(cfg['pages']),'pages',len(CAT),'units')
def main():
 root=Path(__file__).resolve().parents[1]
 for lang in ['en','es']:build(root,lang)
 for p in pages(root):
  s=BeautifulSoup(p.read_text(),'html.parser');langnav(s,root,p.relative_to(root),'pt');p.write_text(re.sub(r'(?i)(<!doctype html>)\s*',r'\1\n',str(s)))
if __name__=='__main__':main()
