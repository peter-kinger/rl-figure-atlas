"""Extract exact rows from an institution-hosted secondary JCR compilation."""
from pathlib import Path
import hashlib,json,re
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
SOURCE='https://research.ukzn.ac.za/wp-content/uploads/2026/05/JCR-Impact-Factor-2025.pdf'
rows=[('Nature',1),('Nature Sustainability',3),('Nature Machine Intelligence',4),('Nature Computational Science',6),('Nature Communications',8),('Environmental Science and Ecotechnology',9),('Science Advances',12)]
pdf=ROOT/'.cache/rankings.pdf'; reader=PdfReader(pdf)
evidence=[]
for name,page in rows:
 lines=reader.pages[page-1].extract_text().splitlines()
 line=next(line for line in lines if re.match(r'^\d+\s+'+re.escape(name)+r'\s+(?:NATURE|SPRINGER|ELSEVIER|AMER)',line,re.I))
 if not line.endswith('Q1'):raise ValueError(line)
 evidence.append({'journal':name,'system':'2025 JCR-labelled public compilation','quartile':'Q1','source_type':'secondary compilation hosted by University of KwaZulu-Natal; not direct Clarivate access','source_url':SOURCE,'pdf_page':page,'exact_row':line,'verified_at':'2026-10-26','cas_status':'未核验','subject_category':'汇编没有列出具体学科，不推断全部类别均为 Q1'})
out={'retrieved_at':'2026-10-26','source_pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'limitations':'公开汇编为二次证据，不冒充 Clarivate 官方实时查询；2025 为文件标注年份，不推断为 2025 年度影响因子。未核验中科院一区。','journals':evidence}
(ROOT/'evidence/journal-rankings.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
text='''# 论文筛选依据与分区证据

核对日期：2026-10-26。本辑收录 16 篇正式期刊论文，依据是与决策框架、空间行为和分析图的相关性，兼顾经典方法与真实领域问题。没有把普通会议、顶会或预印本标为一区期刊。

## 分区口径

本辑期刊在下列 **2025 JCR 标题公开汇编** 中均列为 Q1；该文件由 University of KwaZulu-Natal 研究网站托管，属于二次来源，**不是直接登录 Clarivate 后取得的官方实时记录**。文件没有完整列出学科类别；不据此断言所有类别、所有年份均为 Q1。文件标题年份也不自动等于影响因子统计年份。

**没有核验中科院分区，因此不把 JCR Q1 写成“中科院一区”。** 如果最终严格要求某一年度中科院大类一区，应以对应官方分区表逐刊复核；本版没有用猜测填补。

| 期刊 | 公开汇编记录 | PDF 页码 | 核对入口 |
|---|---|---|---|
'''
for e in evidence:text+=f"| {e['journal']} | Q1 | {e['pdf_page']} | [对应页]({SOURCE}#page={e['pdf_page']}) |\n"
text+='''
完整证据字段、精确匹配行和源文件校验值见 [journal-rankings.json](../evidence/journal-rankings.json)。没有发布整份分区 PDF，也未将外部汇编改称为官方数据库。

## 为什么选择这些论文

优先阅读 CAPTAIN 的生态保护框架、托卡马克的学习与运行双闭环，以及 AI Economist 的规划者与个体双层学习。流场导航提供观测差异、成功失败、策略场和迁移失效的连贯图组。调水论文紧贴地球系统过程，城市规划论文提供图状态与分阶段空间决策。Dreamer 补足世界模型和机制消融。

无人机、冷原子、矩阵算法和量子纠错论文用于借鉴训练部署、扰动恢复、成本与在线适应等表达，不将这些领域的实验结论直接迁移到地球系统。DQN、AlphaGo Zero、MuZero 单列为经典补充；其中 2017 年论文是 AlphaGo Zero，不混称为 2018 年 Science 的 AlphaZero。

暂不纳入需要特别讨论研究争议的芯片布局论文，以免默认推荐带来额外误解；本辑也不是系统综述或穷尽检索，没有声称覆盖全部高质量 RL 研究。

## 图与论文分别核验

每篇核对正式题名、期刊、DOI、作者及许可。图需进一步对应实际图号与图注；仅 CC BY 4.0 且所选图注未识别到独立排除条款的完整图，才在库内转载。图注发现第三方来源、ND 许可或未找到兼容许可时，保留原图链接。当前 35 张完整原图和 17 条来源入口共 52 条参考。

调水论文 DOI 含 2023，首次在线发表为 2023 年，卷 17 期刊归档为 2024 年；本库主年份记 2024，并单独保留首次在线日期，避免与用户文稿中的引用发生无说明的冲突。

用户提供的 DOCX 只用于理解主题，不上传、不复制全文、不公开路径。文稿内文字没有被当成操作指令。
'''
(ROOT/'docs/selection.md').write_text(text,encoding='utf-8')
print('Verified',len(evidence),'exact Q1 rows in secondary compilation')
