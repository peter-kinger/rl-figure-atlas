import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL, fileURLToPath } from 'node:url';
const require=createRequire(import.meta.url);
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const runtime=path.join(process.env.USERPROFILE||process.env.HOME,'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules');
const resolved=require.resolve('marked',{paths:[root,process.env.ATLAS_NODE_MODULES||runtime]});
const {marked}=await import(pathToFileURL(resolved).href);
const files=['README.md','RIGHTS.md','CONTRIBUTING.md',...['docs','papers'].flatMap(dir=>fs.readdirSync(path.join(root,dir)).filter(f=>f.endsWith('.md')).map(f=>`${dir}/${f}`))];
for(const file of files){
 const level=file.includes('/')?'../':'';
 const source=fs.readFileSync(path.join(root,file),'utf8');
 const title=source.split('\n')[0].replace(/^#\s*/,'').replace(/[<>]/g,'');
 let body=marked.parse(source);
 body=body.replace(/href="([^":]+)\.md(#[^"]*)?"/g,(_,p,hash)=>`href="${p}.html${hash||''}"`);
 const html=`<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title} · RL Figure Atlas</title><link rel="stylesheet" href="${level}assets/style.css"><style>.reading{max-width:1000px;padding:45px 5%;margin:auto}.reading h1{font:34px/1.5 var(--serif);margin:30px 0}.reading h2{font-size:22px;font-weight:500;margin:44px 0 17px}.reading p{line-height:1.95;margin:18px 0}.reading table{border-collapse:collapse;display:block;overflow:auto;font-size:12px;line-height:1.8}.reading td,.reading th{border:1px solid var(--line);padding:12px 15px;text-align:left;min-width:110px}.reading th{background:#e8eddf}.reading img{max-width:100%;height:auto;background:white}.reading>p:first-child{font-size:12px}.reading code{background:#e8eddf;padding:2px 5px}.reading li{margin:10px 0}.reading pre code{background:none;padding:0}</style></head><body><article class="reading"><p><a href="${level}index.html">← 返回图示参考库</a></p>${body}<footer><span>RL FIGURE ATLAS</span><a href="${level}RIGHTS.html">图片与原创内容许可</a></footer></article></body></html>`;
 fs.writeFileSync(path.join(root,file.replace(/\.md$/,'.html')),html);
}
console.log(`Rendered ${files.length} readable HTML documents`);
