"""Structural verification for the actual published catalogue and assets."""
from pathlib import Path
import hashlib,json,re,sys,xml.etree.ElementTree as ET
from urllib.parse import unquote,urlsplit
from PIL import Image
from lxml import html
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
papers=json.loads((ROOT/'data/papers.json').read_text(encoding='utf-8'))
figures=json.loads((ROOT/'data/figures.json').read_text(encoding='utf-8'))
assert len(papers)==16 and len(figures)==52
assert len({p['id'] for p in papers})==len(papers)
assert len({f['id'] for f in figures})==len(figures)
ids={p['id'] for p in papers}
for p in papers:
 assert p['doi'].startswith('10.') and p['authors'],p['id']
 assert p['ranking_evidence']['quartile']=='Q1',p['id']
 assert (ROOT/'papers'/f"{p['id']}.md").exists()
 assert (ROOT/'evidence'/f"{p['id']}.json").exists()
for f in figures:
 assert f['paper_id'] in ids and f['source_url'].startswith('https://'),f['id']
 assert f['lesson'] and f['caveat'] and f['attribution'],f['id']
 if f['local_path']:
  assert f['license']=='CC BY 4.0' and f['status']=='original',f['id']
  p=ROOT/f['local_path']
  assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
  with Image.open(p) as image:
   assert image.size==(f['width'],f['height']) and min(image.size)>150
   image.verify()
 else: assert f['status']=='source-only'
for svg in (ROOT/'templates').glob('*.svg'):ET.parse(svg)
assert len(list((ROOT/'templates').glob('*.svg')))==10
# Offline graph includes Markdown links and fixed HTML references.
checked=0
for p in [*ROOT.rglob('*.html'),*ROOT.rglob('*.md')]:
 if '.cache' in p.parts:continue
 t=p.read_text(encoding='utf-8')
 refs=re.findall(r'\]\(([^)]+)\)',t)
 if p.suffix=='.html':refs+=html.fromstring(t).xpath('//@href | //@src')
 for ref in refs:
  if urlsplit(ref).scheme or ref.startswith('#') or '${' in ref:continue
  target=p.parent/unquote(ref.split('#')[0])
  assert target.exists(),f'{p.relative_to(ROOT)} → {ref}'
  checked+=1
catalog=(ROOT/'assets/catalog.js').read_text(encoding='utf-8')
assert json.loads(catalog.removeprefix('window.ATLAS = ').rstrip(';\n'))=={'papers':papers,'figures':figures}
print(f'PASS: {len(papers)} papers, {len(figures)} figure records, 35 original images, 10 SVG templates, {checked} relative links; hashes, licenses and exact catalogue match.')
