"""Collect curated, licensed publisher figures; regenerate static catalogues."""
import concurrent.futures, hashlib, io, json, re, sys, urllib.parse
from pathlib import Path
from lxml import html
from PIL import Image
from inspect_sources import SOURCES, get, inspect
from curation import PAPERS

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
DATE='2026-10-26'
for directory in ['data','assets','figures','papers','evidence']:
 (ROOT/directory).mkdir(exist_ok=True)

def compact(text): return re.sub(r'\s+',' ',text).strip()
def first(meta,*keys,default=''):
 for k in keys:
  if meta.get(k):return meta[k][0]
 return default

def make_paper(key):
 path=ROOT/'.cache'/f'{key}.html'
 if not path.exists(): inspect((key,SOURCES[key]))
 doc=html.fromstring(path.read_bytes().decode('utf-8'))
 metas={}
 for e in doc.xpath('//meta[@name]'):
  metas.setdefault(e.get('name'),[]).append(e.get('content',''))
 body=compact(' '.join(doc.xpath('//body//text()')))
 # Article rights are read independently of CC-licensed references in captions.
 rights=body.split('Rights and permissions')[-1] if 'Rights and permissions' in body else body[:15000]
 license='CC BY-NC-ND 4.0' if re.search(r'Attribution-NonCommercial-NoDerivatives|CC BY-NC-ND',rights) else ('CC BY 4.0' if re.search(r'Creative Commons Attribution (4.0|License 4.0)|CC BY\)',rights) else '需另行授权')
 license_url={'CC BY 4.0':'https://creativecommons.org/licenses/by/4.0/','CC BY-NC-ND 4.0':'https://creativecommons.org/licenses/by-nc-nd/4.0/'}.get(license,'')
 topic,priority,why,specs=PAPERS[key]
 online=first(metas,'citation_online_date','dc.date','citation_publication_date')
 year=int(re.search(r'20\d\d|19\d\d',online).group())
 p={'id':key,'title':first(metas,'citation_title','dc.title'),'journal':first(metas,'citation_journal_title'),'year':2024 if key=='water' else year,'online_date':online,'doi':first(metas,'citation_doi'),'url':SOURCES[key],'authors':metas.get('citation_author',metas.get('dc.creator',[])),'topic':topic,'priority':priority,'why':why,'license':license,'license_url':license_url,'verified_at':DATE,'quality_status':'顶级期刊' if first(metas,'citation_journal_title')=='Nature' else 'Q1 候选 · 见分区证据','ranking_system':'JCR 2025 汇编待核对','cas_status':'未核验，不宣称中科院一区'}
 ranking_file=ROOT/'evidence/journal-rankings.json'
 if ranking_file.exists():
  rank=next((r for r in json.loads(ranking_file.read_text(encoding='utf-8'))['journals'] if r['journal']==p['journal']),None)
  if rank:
   p.update(quality_status='Q1 · 2025 公开汇编',ranking_system=rank['system'],ranking_evidence=rank)
 if not p['doi']:p['doi']=first(metas,'prism.doi','dc.identifier').replace('doi:','')
 allfig=doc.xpath('//figure[.//img]')
 results=[]
 for n,title,category,lesson,caveat in specs:
  if 'nature.com' in p['url']:
   f=next((f for f in allfig if re.match(r'(Fig\.|Figure)\s*'+str(n)+r'[:.]',compact(' '.join(f.xpath('.//figcaption//text()'))))),None)
  else:
   f=next((f for f in allfig if (f.get('id') or '').lower() in ['f'+str(n),'fig'+str(n)]),None)
  if f is None: raise ValueError(f'{key}: figure {n} not found')
  caption=compact(' '.join(f.xpath('.//text()')))
  # Save brief evidence of rights review, without republishing full article text.
  exclusions=re.findall(r'.{0,70}(?:credit|copyright|permission|adapted from|reproduced from).{0,160}',caption,re.I)
  figure_url=next((urllib.parse.urljoin(p['url'],u) for u in f.xpath('.//a/@href') if '/figures/' in u or 'figure/' in u),p['url'])
  src=urllib.parse.urljoin(p['url'],f.xpath('.//img')[0].get('src'))
  if 'springernature.com' in src:src=src.replace('/lw685/','/full/')
  fid=f'{key}-fig{n}'
  entry={'id':fid,'paper_id':key,'figure':f'Fig. {n}','title':title,'category':category,'lesson':lesson,'caveat':caveat,'source_url':figure_url,'image_source_url':src,'local_path':None,'license':license,'license_url':license_url,'status':'original' if license=='CC BY 4.0' and not exclusions else 'source-only','verified_at':DATE,'modifications':'未裁切、未重绘；按比例显示。' if license=='CC BY 4.0' and not exclusions else '未在本库转载原图；通过来源查看。','figure_credit_review':'图注中未发现单独排除条款；保留原图整张，不抽取面板。' if not exclusions else '图注有独立来源标注，暂仅链接：'+'; '.join(exclusions)}
  if entry['status']=='original':entry['local_path']=f'figures/{fid}'+('.jpg' if '.jpg' in src else '.png')
  entry['attribution']=f"{'; '.join(p['authors'])}. {p['title']}. {p['journal']} ({p['year']}), Fig. {n}. https://doi.org/{p['doi']}. {license}. {entry['modifications']}"
  results.append(entry)
 evidence={'paper_id':key,'source_url':p['url'],'retrieved_at':DATE,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'license':license,'license_url':license_url,'license_evidence':rights[max(0,rights.find('Open Access')):max(0,rights.find('Open Access'))+700] if 'nature.com' in p['url'] else re.search(r'.{0,100}(?:CC BY-NC-ND|Distributed under a Creative Commons).{0,180}',body).group() if re.search(r'.{0,100}(?:CC BY-NC-ND|Distributed under a Creative Commons).{0,180}',body) else 'See publisher rights section.','figures':[{'id':f['id'],'source_url':f['source_url'],'credit_review':f['figure_credit_review']} for f in results]}
 (ROOT/'evidence'/f'{key}.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
 return p,results

def download(f):
 if not f['local_path']:return
 path=ROOT/f['local_path']
 if not path.exists():path.write_bytes(get(f['image_source_url']))
 with Image.open(path) as im:
  im.verify()
 with Image.open(path) as im: f['width'],f['height']=im.size
 f['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()

def build():
 papers=[];figures=[]
 for key in PAPERS:
  p,fs=make_paper(key);papers.append(p);figures.extend(fs)
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:list(pool.map(download,figures))
 for name,data in [('papers',papers),('figures',figures)]:
  (ROOT/'data'/f'{name}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'assets'/'catalog.js').write_text('window.ATLAS = '+json.dumps({'papers':papers,'figures':figures},ensure_ascii=False)+';\n',encoding='utf-8')
 bib=[]
 for p in papers:
  bib.append('@article{'+p['id']+',\n  title={'+p['title']+'},\n  author={'+' and '.join(p['authors'])+'},\n  journal={'+p['journal']+'},\n  year={'+str(p['year'])+'},\n  doi={'+p['doi']+'}\n}')
  fs=[f for f in figures if f['paper_id']==p['id']]
  content=f"# {p['title']}\n\n{p['journal']} · {p['year']} · {p['priority']}\n\n[论文原文]({p['url']}) · [DOI](https://doi.org/{p['doi']})\n\n{p['why']}\n\n许可：{p['license']}。分区详见 [筛选依据](../docs/selection.md)，未宣称已核验中科院一区。\n"
  for f in fs:
   content+=f"\n## {f['figure']} {f['title']}\n\n**用途：** {f['category']}。\n\n**画法借鉴：** {f['lesson']}\n\n**解释边界：** {f['caveat']}\n\n[原始图页]({f['source_url']})\n"
   if f['local_path']:content+=f"\n![{f['title']}](../{f['local_path']})\n\n{f['attribution']}\n"
  (ROOT/'papers'/f"{p['id']}.md").write_text(content,encoding='utf-8')
 (ROOT/'references.bib').write_text('\n\n'.join(bib)+'\n',encoding='utf-8')
 print(json.dumps({'papers':len(papers),'figures':len(figures),'local_originals':sum(bool(f['local_path']) for f in figures),'source_only':sum(not f['local_path'] for f in figures)},ensure_ascii=False))

if __name__=='__main__':build()
