from pathlib import Path
import json,hashlib,concurrent.futures
from translate_api import call,PROMPT,ROOT
MODEL='openai/gpt-5.4-nano'
def work(lang):
 items=json.loads((ROOT/'i18n/source.json').read_text());dest=ROOT/f'i18n/{lang}.json'
 sig=hashlib.sha256((MODEL+PROMPT+'agent-skills'+'course-i18n-1.0.0').encode()).hexdigest();meta=ROOT/f'i18n/{lang}-provenance.json'
 cache=json.loads(dest.read_text()) if dest.exists() and meta.exists() and json.loads(meta.read_text()).get('signature')==sig else {}
 meta.write_text(json.dumps({'signature':sig,'model':MODEL,'source_version':'course-i18n-1.0.0','prompt_sha256':hashlib.sha256(PROMPT.encode()).hexdigest(),'context':'agent-skills','price_source':'https://openrouter.ai/api/v1/models','price_checked':'2026-09-22'},indent=2))
 batches=[];batch={};size=0
 for k,v in items.items():
  if k in cache:continue
  if (size+len(v)>6500 or len(batch)>=50) and batch:batches.append(batch);batch={};size=0
  batch[k]=v;size+=len(v)
 if batch:batches.append(batch)
 for i,b in enumerate(batches):
  out=call(b,'English' if lang=='en' else 'Spanish (Latin America)',MODEL,'agent-skills:content');cache.update(out);dest.write_text(json.dumps(cache,ensure_ascii=False,indent=2)+'\n');print(lang,i+1,'/',len(batches),flush=True)
 return lang,len(cache)
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  for result in pool.map(work,['en','es']):print('DONE',result,flush=True)
