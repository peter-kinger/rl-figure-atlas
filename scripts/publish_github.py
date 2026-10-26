"""Create the requested public research repository using existing Git credentials.

Credentials are read in memory from the configured Git helper and never printed.
No private source documents or cache files are staged by this script.
"""
import json,subprocess,sys,urllib.request,urllib.error
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
NAME='rl-figure-atlas'

def credentials():
 r=subprocess.run(['git','-c','credential.interactive=never','credential','fill'],input='protocol=https\nhost=github.com\n\n',text=True,capture_output=True,timeout=20,check=True)
 return dict(line.split('=',1) for line in r.stdout.splitlines() if '=' in line)['password']
TOKEN=credentials()
def api(route,method='GET',data=None):
 headers={'Authorization':'Bearer '+TOKEN,'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28','User-Agent':'RL-Figure-Atlas-Publisher'}
 req=urllib.request.Request('https://api.github.com'+route,headers=headers,method=method,data=json.dumps(data).encode() if data is not None else None)
 with urllib.request.urlopen(req,timeout=35) as r:
  return json.load(r) if r.status!=204 else {}

if __name__=='__main__':
 command=sys.argv[1] if len(sys.argv)>1 else 'status'
 owner=api('/user')['login'];repo=f'{owner}/{NAME}'
 if command=='create':
  try:
   api('/repos/'+repo)
  except urllib.error.HTTPError as e:
   if e.code!=404:raise
  else:raise SystemExit('Repository already exists; refusing to overwrite or reuse automatically.')
  d=api('/user/repos','POST',{'name':NAME,'description':'强化学习绘图素材库：MDP 框架、空间策略与分析图。16 papers, 52 figure references, 10 editable SVG templates.','private':False,'auto_init':False,'has_issues':True,'homepage':f'https://{owner}.github.io/{NAME}/'})
  print(json.dumps({'repository':d['html_url'],'visibility':d['visibility'],'owner':owner},ensure_ascii=False))
 elif command=='pages':
  try:d=api('/repos/'+repo+'/pages','POST',{'build_type':'workflow'})
  except urllib.error.HTTPError as e:
   if e.code==409:d=api('/repos/'+repo+'/pages')
   else:print('Pages setup HTTP',e.code,e.read().decode()[:600]);raise SystemExit(1)
  print(json.dumps({'url':d.get('html_url'),'status':d.get('status'),'build_type':d.get('build_type')}))
 elif command=='status':
  runs=api('/repos/'+repo+'/actions/runs?per_page=3')['workflow_runs']
  print(json.dumps([{'id':r['id'],'status':r['status'],'conclusion':r['conclusion'],'url':r['html_url']} for r in runs]))
 elif command=='rerun':
  runs=api('/repos/'+repo+'/actions/runs?per_page=1')['workflow_runs']
  print(api('/repos/'+repo+'/actions/runs/'+str(runs[0]['id'])+'/rerun','POST',{}))
 elif command=='topics':
  print(api('/repos/'+repo+'/topics','PUT',{'names':['reinforcement-learning','scientific-visualization','mdp','earth-system-science','figure-gallery','research']}))
