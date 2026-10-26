import concurrent.futures, json, re, subprocess, urllib.request, sys, zipfile
from pathlib import Path
from lxml import html, etree

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / '.cache'
CACHE.mkdir(exist_ok=True)

SOURCES = {
 'urban': 'https://www.nature.com/articles/s43588-023-00503-5',
 'biodiversity': 'https://www.nature.com/articles/s41893-022-00851-6',
 'tokamak': 'https://www.nature.com/articles/s41586-021-04301-9',
 'tearing': 'https://www.nature.com/articles/s41586-024-07024-9',
 'drone': 'https://www.nature.com/articles/s41586-023-06419-4',
 'dreamer': 'https://www.nature.com/articles/s41586-025-08744-2',
 'network': 'https://www.nature.com/articles/s42256-024-00879-7',
 'navigation': 'https://www.nature.com/articles/s41467-021-27015-y',
 'cold-atoms': 'https://www.nature.com/articles/s41467-024-52775-8',
 'quantum': 'https://www.nature.com/articles/s41586-026-10759-2',
 'alphatensor': 'https://www.nature.com/articles/s41586-022-05172-4',
 'dqn': 'https://www.nature.com/articles/nature14236',
 'alphazero': 'https://www.nature.com/articles/nature24270',
 'muzero': 'https://www.nature.com/articles/s41586-020-03051-4',
 'water': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC10405199/',
 'economist': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9067926/',
}

def get(url):
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (research figure catalogue; provenance collection)'})
 with urllib.request.urlopen(req,timeout=45) as r: return r.read()

def inspect(item):
 key,url=item
 try:
  path=CACHE/(key+'.html')
  if not path.exists(): path.write_bytes(get(url))
  doc=html.fromstring(path.read_bytes().decode('utf-8'))
  text=' '.join(doc.xpath('//body//text()'))
  text=re.sub(r'\s+',' ',text)
  metas={}
  for e in doc.xpath('//meta[@name or @property]'):
   name=e.get('name') or e.get('property')
   if name.startswith(('citation_','dc.','DC.','prism.')): metas.setdefault(name,[]).append(e.get('content'))
  figs=[]
  for f in doc.xpath('//figure'):
   heading=' '.join(f.xpath('.//h3//text() | .//h2//text() | .//figcaption//text()'))
   imgs=[{k:i.get(k) for k in ['src','data-src','srcset','alt'] if i.get(k)} for i in f.xpath('.//img')]
   links=f.xpath('.//a/@href')
   figs.append({'id':f.get('id'),'heading':re.sub(r'\s+',' ',heading)[:2500],'images':imgs,'links':links})
  licenses=sorted(set(doc.xpath('//a[contains(@href,"creativecommons.org")]/@href')))
  notices=[text[max(0,m.start()-100):m.start()+350] for m in re.finditer(r"Editor.s [Nn]ote|Author Correction|retract|third party|Creative Commons",text)][:12]
  result={'id':key,'url':url,'metadata':metas,'licenses':licenses,'figures':figs,'notices':notices}
  (CACHE/(key+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
  return {'id':key,'title':metas.get('citation_title'),'journal':metas.get('citation_journal_title'),'date':metas.get('citation_publication_date'),'licenses':licenses,'figures':[(f['id'],f['heading'][:140],len(f['images'])) for f in figs],'notices':notices[:2]}
 except Exception as e: return {'id':key,'error':str(e)}

if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
  for result in pool.map(inspect,SOURCES.items()): print(json.dumps(result,ensure_ascii=False))
 try:
  doc=html.fromstring(get('https://chutj.github.io/gallery/'))
  print('REFERENCE',re.sub(r'\s+',' ',' '.join(doc.xpath('//body//text()')))[:6500])
 except Exception as e: print('REFERENCE',str(e))
