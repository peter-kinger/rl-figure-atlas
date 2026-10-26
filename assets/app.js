'use strict';
const $ = s => document.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const {papers, figures} = window.ATLAS;
const paperMap = Object.fromEntries(papers.map(p => [p.id,p]));
function stored(key, fallback) { try {return JSON.parse(localStorage.getItem(key)) ?? fallback;} catch {return fallback;} }
function persist(key, value) { try {localStorage.setItem(key,JSON.stringify(value));} catch {} }
let saved = new Set(stored('rl-atlas-shortlist',[]));
let category = '', onlySaved = false;
const categories = [...new Set(figures.map(f=>f.category))];
const templateNames = [
 ['01-mdp-loop','MDP 决策闭环','环境、策略、转移、奖励与时间顺序。'],
 ['02-pomdp-observation','部分可观测与信念','区分系统真实状态和实际可获得的信息。'],
 ['03-cmdp-safety','安全约束与执行层','奖励通路与可行性检查分开。'],
 ['04-marl-ctde','多智能体 CTDE','集中训练和分散执行的信息边界。'],
 ['05-training-deployment','训练与部署','区分模拟器学习、留出测试和实际运行。'],
 ['06-world-model','世界模型','真实经验与想象轨迹形成两条循环。'],
 ['07-coupled-governance','人地耦合与双层治理','规划者、个体和地球系统过程。'],
 ['08-hierarchical-timescales','分层决策时标','慢尺度目标与快尺度动作的关系。'],
 ['09-rl-icon-sheet','16 个强化学习图元','观测、动作、策略、网络、风险和资源等。'],
 ['10-analysis-panel-layout','四面板分析布局','学习、效果、行为与权衡的空白图形结构。']
];
$('#summary').textContent = `${papers.length} 篇期刊论文 · ${figures.filter(f=>f.local_path).length} 张原图 · ${templateNames.length} 份矢量模板`;
[...new Set(papers.map(p=>p.topic))].forEach(t=>$('#topic').insertAdjacentHTML('beforeend',`<option>${esc(t)}</option>`));
function drawCategories(){
 $('#categories').innerHTML = ['',...categories].map(c=>`<button class="category ${category===c?'active':''}" data-category="${esc(c)}" aria-pressed="${category===c}">${esc(c||'全部图示')}<span>${c?figures.filter(f=>f.category===c).length:figures.length}</span></button>`).join('');
}
function card(f){
 const p=paperMap[f.paper_id];
 const image = f.local_path ? `<a class="image-link" href="${esc(f.local_path)}" target="_blank" rel="noopener" aria-label="查看完整原图：${esc(f.title)}"><img src="${esc(f.local_path)}" alt="${esc(p.title)}，${esc(f.figure)}；${esc(f.title)}" width="${f.width}" height="${f.height}" loading="lazy"></a>` : `<a class="image-link source-only-panel" href="${esc(f.source_url)}" target="_blank" rel="noopener"><span class="source-id">${esc(f.figure)} ↗</span><p>仅原文入口 · ${esc(p.license)}<br>本库未转载该图</p></a>`;
 return `<article class="figure-card" id="${f.id}">${image}<div class="card-top"><span class="tag">${esc(f.category)}</span><span class="figure-number">${esc(f.figure)}</span></div><h3>${esc(f.title)}</h3><p class="journal">${esc(p.journal)} · ${p.year}<br>${esc(p.topic)}</p><p class="lesson">${esc(f.lesson)}</p><details><summary>读图笔记与来源</summary><p><strong>解释边界</strong><br>${esc(f.caveat)}</p><p><strong>原始论文</strong><br>${esc(p.title)}<br><a href="https://doi.org/${esc(p.doi)}" target="_blank" rel="noopener">DOI: ${esc(p.doi)}</a></p><p><strong>许可与改动</strong><br>${f.license_url?`<a href="${esc(f.license_url)}" target="_blank" rel="noopener">${esc(f.license)}</a>`:esc(f.license)} · ${esc(f.modifications)}</p><p class="attribution">${esc(f.attribution)}</p><p>来源核对：${f.verified_at}。<a href="papers/${p.id}.html">完整阅读笔记 ↗</a></p></details><div class="card-actions"><a href="${esc(f.source_url)}" target="_blank" rel="noopener">原文图页 ↗</a><button class="save" data-save="${f.id}" aria-pressed="${saved.has(f.id)}">${saved.has(f.id)?'✓ 已加入选图':'+ 加入选图'}</button></div></article>`;
}
function render(){
 const q=$('#search').value.trim().toLowerCase(), topic=$('#topic').value, availability=$('#availability').value;
 const selected=figures.filter(f=>{
  const p=paperMap[f.paper_id];
  const searchable=[f.title,f.category,f.lesson,f.caveat,p.title,p.doi,p.topic,p.journal,p.authors.join(' ')].join(' ').toLowerCase();
  return (!category||f.category===category)&&(!topic||p.topic===topic)&&(!availability||f.status===availability)&&(!onlySaved||saved.has(f.id))&&q.split(/\s+/).every(term=>searchable.includes(term));
 });
 $('#gallery').innerHTML=selected.map(card).join('');
 $('#result-count').textContent=`${selected.length} 条 · ${selected.filter(f=>f.local_path).length} 张原图`;
 $('#gallery-title').textContent=onlySaved?'我的选图':category||'全部图示';
 $('#empty').hidden=selected.length>0;
 $('#saved-count').textContent=saved.size;
 $('#shortlist-filter').setAttribute('aria-pressed',onlySaved);
 drawCategories();
}
$('#categories').addEventListener('click',e=>{const b=e.target.closest('[data-category]');if(b){category=b.dataset.category;render();}});
$('#gallery').addEventListener('click',e=>{const b=e.target.closest('[data-save]');if(b){const id=b.dataset.save;saved.has(id)?saved.delete(id):saved.add(id);persist('rl-atlas-shortlist',[...saved]);const position=window.scrollY;render();window.scrollTo(0,position);}});
$('#search').addEventListener('input',render);$('#topic').addEventListener('change',render);$('#availability').addEventListener('change',render);
$('#shortlist-filter').addEventListener('click',()=>{onlySaved=!onlySaved;render();});
$('#reset').addEventListener('click',()=>{category='';onlySaved=false;$('#search').value='';$('#topic').value='';$('#availability').value='';render();});
function notify(message){$('#toast').textContent=message;$('#toast').classList.add('visible');setTimeout(()=>$('#toast').classList.remove('visible'),2500);}
function download(name,body,type){const url=URL.createObjectURL(new Blob([body],{type}));const a=document.createElement('a');a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);}
$('#export').addEventListener('click',()=>{
 const list=figures.filter(f=>saved.has(f.id));if(!list.length){notify('先把感兴趣的图加入选图清单');return;}
 const content='# 我的强化学习绘图参考清单\n\n'+list.map(f=>{const p=paperMap[f.paper_id];return `## ${f.title}\n\n${p.title} · ${p.journal} (${p.year}) · ${f.figure}\n\n用途：${f.category}\n\n画法：${f.lesson}\n\n解释边界：${f.caveat}\n\n[原文图页](${f.source_url}) · [DOI](https://doi.org/${p.doi})\n\n许可：${f.license}。${f.modifications}\n\n署名：${f.attribution}\n`;}).join('\n');
 download('rl-drawing-shortlist.md',content,'text/markdown;charset=utf-8');notify(`已导出 ${list.length} 张图的来源与笔记`);
});
document.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>{
 document.querySelectorAll('.view').forEach(v=>v.hidden=v.id!==`${b.dataset.view}-view`);
 document.querySelectorAll('[data-view]').forEach(btn=>btn.classList.toggle('active',btn===b));
}));
$('#template-grid').innerHTML=templateNames.map(([id,title,description])=>`<article class="template-item"><a href="templates/${id}.svg" target="_blank" rel="noopener"><img src="templates/${id}.svg" alt="${title}，原创可编辑矢量模板" loading="lazy" width="1200" height="760"></a><h3>${title}</h3><p>${description}</p><a href="templates/${id}.svg" download>下载 SVG ↓</a></article>`).join('');
$('#paper-list').innerHTML=papers.map(p=>`<article class="paper-row"><div class="paper-year">${p.year}<span class="paper-priority">${esc(p.priority)}</span></div><div><h3>${esc(p.title)}</h3><p>${esc(p.journal)} · ${esc(p.topic)} · ${esc(p.quality_status)}</p><p>${esc(p.why)}</p></div><div class="paper-links"><a href="${esc(p.url)}" target="_blank" rel="noopener">论文原文 ↗</a><a href="papers/${p.id}.html">绘图阅读笔记 ↗</a><a href="https://doi.org/${esc(p.doi)}" target="_blank" rel="noopener">DOI ↗</a></div></article>`).join('');
const form=$('#mdp-form');const initial=stored('rl-atlas-mdp',{});for(const [k,v] of Object.entries(initial)){if(form.elements.namedItem(k))form.elements.namedItem(k).value=v;}
let currentSvg='',currentMermaid='';
function wrappedText(text,x,y,width=24){const chars=Array.from(text);let s='';for(let i=0;i<chars.length;i+=width)s+=`<text x="${x}" y="${y+Math.floor(i/width)*25}" font-size="17">${esc(chars.slice(i,i+width).join(''))}</text>`;return s;}
function updateWorkbench(){
 const d=Object.fromEntries(new FormData(form));persist('rl-atlas-mdp',d);
 const isPartial=d.model==='POMDP';
 currentSvg=`<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="780" viewBox="0 0 1200 780"><title>${esc(d.model)} 决策框架</title><defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#326b56"/></marker></defs><style>text{font-family:'Microsoft YaHei','Noto Sans CJK SC',sans-serif;fill:#233c38}.box{fill:#fffef8;stroke:#b7c6b9;stroke-width:1.5}.arrow{fill:none;stroke:#326b56;stroke-width:2.5;marker-end:url(#arr)}</style><rect width="1200" height="780" fill="#f6f5ee"/><text x="55" y="62" font-size="32">${esc(d.model)} 决策框架</text>${wrappedText(d.step,55,100,65)}<rect x="70" y="190" width="380" height="180" class="box" rx="4"/><text x="95" y="225" font-size="23">策略与决策者</text>${wrappedText(d.agent,95,266,18)}<text x="95" y="340" font-size="16">${isPartial?'πθ(aₜ | bₜ) · 信念或历史':'πθ(aₜ | sₜ) · 状态反馈'}</text><rect x="735" y="190" width="395" height="180" class="box" rx="4"/><text x="760" y="225" font-size="23">环境过程</text>${wrappedText(d.environment,760,268,19)}<text x="760" y="340" font-size="16">sₜ₊₁ ~ P(· | sₜ, aₜ)</text><path d="M450 260H735" class="arrow"/>${wrappedText(d.action,475,220,15)}<path d="M930 370V465H260V370" class="arrow"/>${wrappedText((isPartial?'观测 oₜ₊₁：':'状态反馈：')+d.observation,320,408,38)}<text x="470" y="452" font-size="16">奖励 rₜ₊₁</text><rect x="70" y="535" width="1060" height="125" class="box" rx="4"/>${wrappedText('奖励：'+d.reward,95,575,54)}${wrappedText('约束：'+d.constraint,95,624,54)}<text x="55" y="710" font-size="15">${isPartial?'POMDP：状态经观测通道产生 o，策略用历史或信念 b。':d.model==='CMDP'?'CMDP：另定义约束代价 Jᶜ 与阈值 d，要求 Jᶜ ≤ d。':'MDP 假设：所选状态应包含预测下一状态所需的决策信息。'}</text><text x="55" y="748" font-size="12">RL Figure Atlas · 原创概念框架 · CC BY 4.0 · 请按真实研究核验假设</text></svg>`;
 $('#mdp-preview').innerHTML=currentSvg;
 const m=s=>String(s).replace(/["\n\r\[\]<>]/g,' ');
 currentMermaid=`flowchart LR\n  A["${m(d.agent)} / ${d.model}"]\n  E["${m(d.environment)}"]\n  A -->|"动作：${m(d.action)}"| E\n  E -->|"${isPartial?'观测与历史':'状态反馈'}：${m(d.observation)}"| A\n  E -->|"奖励：${m(d.reward)}"| A\n  C["约束：${m(d.constraint)}"] -.-> A\n  T["时间间隔：${m(d.step)}"] -.-> E\n`;
 if(isPartial){
  currentMermaid=currentMermaid.split('\n').filter(line=>!line.includes('观测与历史')).join('\n')+'\n';
  currentMermaid+=`  E --> O["观测通道 O"]\n  O -->|"${m(d.observation)}"| B["信念 / 历史记忆 b"]\n  B --> A\n`;
 }
 $('#mermaid-code').textContent=currentMermaid;
}
form.addEventListener('input',updateWorkbench);form.addEventListener('change',updateWorkbench);
$('#download-svg').addEventListener('click',()=>download('my-mdp-framework.svg',currentSvg,'image/svg+xml;charset=utf-8'));
$('#download-mermaid').addEventListener('click',()=>download('my-mdp-framework.mmd',currentMermaid,'text/plain;charset=utf-8'));
render();updateWorkbench();
