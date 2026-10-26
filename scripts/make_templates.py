"""Original vector drawing templates. No third-party figure tracing."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'templates';OUT.mkdir(exist_ok=True)
C={'ink':'#233c38','green':'#36745f','blue':'#46758a','orange':'#b96a42','paper':'#f7f6f0','line':'#aebbb1'}

def start(title,subtitle):
 return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="760" viewBox="0 0 1200 760" role="img" aria-label="{escape(title)}"><title>{escape(title)}</title><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="{C['green']}"/></marker></defs><style>text{{font-family:'Microsoft YaHei','Noto Sans CJK SC',sans-serif;fill:{C['ink']}}}.label{{font-size:19px}}.small{{font-size:15px;fill:#57716a}}.node{{fill:#fffefa;stroke:{C['line']};stroke-width:1.5}}.flow{{fill:none;stroke:{C['green']};stroke-width:2.5;marker-end:url(#arrow)}}.learn{{fill:none;stroke:{C['blue']};stroke-width:2;stroke-dasharray:7 5;marker-end:url(#arrow)}}</style><rect width="1200" height="760" fill="{C['paper']}"/><text x="55" y="62" font-size="32" font-weight="700">{title}</text><text x="55" y="99" class="small">{subtitle}</text>'''
def node(x,y,w,h,title,*lines):
 s=f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" class="node"/><text x="{x+20}" y="{y+35}" class="label" font-weight="700">{escape(title)}</text>'
 for i,line in enumerate(lines):s+=f'<text x="{x+20}" y="{y+65+26*i}" class="small">{escape(line)}</text>'
 return s+'</g>'
def flow(d,label='',x=0,y=0,learn=False):
 return f'<path d="{d}" class="{"learn" if learn else "flow"}"/>'+ (f'<text x="{x}" y="{y}" class="small">{escape(label)}</text>' if label else '')
def finish(s,name,footer):
 s+=f'<path d="M55 680H1145" stroke="{C["line"]}"/><text x="55" y="713" class="small">{escape(footer)}</text><text x="55" y="740" font-size="12">RL FIGURE ATLAS · Original editable template · CC BY 4.0 · 2026</text></svg>'
 (OUT/f'{name}.svg').write_text(s,encoding='utf-8')

s=start('MDP 决策闭环','定义实体与时间顺序，再添加网络结构。示例为作者原创框架，不是论文原图。')
s+=node(70,180,350,140,'策略 / Agent','输入：可用于决策的 sₜ','输出：aₜ ~ πθ(· | sₜ)')+node(730,180,390,140,'环境 / Process','物理过程与人类响应','sₜ₊₁ ~ P(· | sₜ, aₜ)')
s+=flow('M420 235H730','动作 aₜ',535,216)+flow('M920 320V410H240V320','下一状态 sₜ₊₁、奖励 rₜ₊₁',460,399)
s+=node(350,490,520,125,'任务定义','状态 S · 动作 A · 转移 P · 奖励 R · 折扣 γ','优化期望折扣累计奖励；标注终止条件与决策间隔')
finish(s,'01-mdp-loop','实线 = 环境交互。完整状态不可获取时，应改用观测和记忆，不直接假定 MDP。')
s=start('POMDP 观测与信念','把真实过程、观测通道和决策者的内部记忆分开。')
s+=node(55,200,310,150,'真实环境状态 sₜ','生态 / 水文 / 社会过程','系统真实状态可能不可见')+node(440,200,300,150,'观测模型 O','监测、遥感、传感器','产生局部观测 oₜ')+node(815,200,330,150,'策略 π(aₜ | bₜ)','bₜ = 信念 / 记忆表征','由历史观测和动作更新')
s+=flow('M365 270H440','采样',378,250)+flow('M740 270H815','oₜ',759,250)+flow('M975 350V440H200V350','动作 aₜ 作用于环境',480,428)
s+=node(330,505,560,110,'观测实验','比较缺测、噪声、延迟、监测频率；以相同环境测试策略')
finish(s,'02-pomdp-observation','模拟器中的全局变量不等于在线观测；历史窗口不自动保证完全可观测。')
s=start('约束 MDP 与执行前安全层','奖励优化与约束检查是两条信息通路；根据方法选择可行域过滤或惩罚。')
s+=node(55,210,270,130,'候选策略','输出候选动作 aₜ','优化任务回报 Jᴿ')+node(430,210,310,130,'安全层 / 可行域','状态相关动作约束','输出可执行动作 ãₜ')+node(845,210,300,130,'受控环境','更新状态与任务奖励','返回约束代价 cₜ₊₁')
s+=flow('M325 270H430','aₜ',370,251)+flow('M740 270H845','ãₜ',781,251)+flow('M995 340V420H190V340','状态、奖励与约束代价',465,406)
s+=node(300,500,610,125,'评估需同时展示','任务表现 · 约束违例率 · 违例严重度 · 控制开销','必要时画风险—收益关系，而不是只报总回报')
finish(s,'03-cmdp-safety','可行域过滤的有效性依赖状态和模型；经验上零违例不等于形式化安全证明。')
s=start('多智能体 CTDE','集中训练、分散执行；执行阶段每个主体只使用允许的观测与通信。')
s+=node(365,150,470,120,'集中训练的价值函数','输入：训练允许的全局状态与联合动作','更新各主体策略参数；训练后移除该支路')
for x,i in [(65,1),(445,2),(825,3)]:
 s+=node(x,370,300,120,f'主体 {i} 的局部策略',f'局部观测 oₜⁱ → 动作 aₜⁱ','可选：邻域通信 / 共享参数')
 s+=flow(f'M600 270V315H{x+150}V370','参数更新' if i==2 else '',625,320,True)
s+=node(330,555,540,85,'共享环境 / 网络化过程','联合动作改变系统；各主体获得自己的观测和奖励')
for x in [215,595,975]:s+=flow(f'M{x} 490V525H600V555')
finish(s,'04-marl-ctde','虚线 = 训练更新。CTDE 是一种组织方式，不代表所有多主体算法都使用集中 critic。')
s=start('训练与部署的两条闭环','明确哪些数据用于学习，哪些信息在实际运行时可用。')
s+=node(55,180,300,140,'训练环境','物理模拟器 / 数字孪生','参数扰动与场景采样')+node(450,180,300,140,'学习器 + 经验库','采样 transition / trajectory','更新策略参数 θ')+node(850,180,300,140,'策略检查点','验证集选择','冻结版本并记录配置')
s+=flow('M355 250H450','经验',380,232)+flow('M750 250H850','更新 θ',778,232,True)
s+=node(135,470,360,130,'真实 / 留出测试环境','测试事件、年份、区域','与训练数据隔离')+node(725,470,350,130,'部署策略 πθ','仅输入在线观测','输出可执行控制动作')
s+=flow('M1000 320V400H900V470','部署',1015,400,True)+flow('M725 520H495','动作',585,506)+flow('M315 600V640H900V600','观测反馈',570,630)
finish(s,'05-training-deployment','若部署时继续学习，应标注更新通路，并将在线适应与冻结策略测试分开。')
s=start('世界模型与想象策略学习','真实经验训练环境模型，模型生成的想象轨迹用于策略优化。')
s+=node(55,200,280,140,'真实环境经验','观测 oₜ · 动作 aₜ','奖励 rₜ₊₁ · 下一观测')+node(450,200,300,140,'学习到的世界模型','编码、潜在动态与预测','估计奖励和未来表征')+node(865,200,280,140,'想象 rollout','由模型生成','不能标作真实测量')
s+=flow('M335 265H450','拟合模型',354,245,True)+flow('M750 265H865','展开',790,245)
s+=node(450,490,360,120,'Actor–Critic 学习','用想象回报更新策略与价值','策略再与真实环境交互')
s+=flow('M1005 340V545H810','想象轨迹',970,450,True)+flow('M450 550H190V340','新的真实交互',220,533)
finish(s,'06-world-model','长时模型误差会累积；模型预测准确性与控制收益需要分别验证。')
s=start('人地耦合的双层治理决策','此图为概念框架；需要按具体研究定义政策时标、个体行动与生态反馈。')
s+=node(65,170,350,140,'规划者 / 治理策略','观测：系统指标与社会统计','动作：配额、税率、激励')+node(780,170,350,140,'个体 / 区域主体','观测：资源、价格、局部环境','动作：生产、取水、减排')
s+=flow('M415 230H780','慢尺度政策 / 约束',490,210)+flow('M780 290H415','社会结果反馈',515,275)
s+=node(350,465,500,140,'地球系统过程','生态、水文、气候与资源动态','状态转移影响主体机会与制度目标')
s+=flow('M955 310V530H850','资源利用',975,425)+flow('M350 530H235V310','系统反馈',80,440)
finish(s,'07-coupled-governance','规划者目标、主体效用和生态指标须分别定义；不要把社会福利简化为所有主体同质。')
s=start('分层决策与时间尺度','上层给出目标或子任务，下层按较快节奏执行；环境反馈跨尺度返回。')
s+=node(70,190,370,145,'上层策略','每 K 步：更新目标 gₖ','如：区域配置 / 月度水量')+node(760,190,370,145,'下层策略','每个决策步：输出动作 aₜ','如：闸门开度 / 日调水量')
s+=flow('M440 260H760','目标 / 子任务 gₖ',535,240)
s+=node(380,490,450,125,'环境过程与目标达成','记录实际状态、底层奖励与上层累计结果')
s+=flow('M945 335V550H830','执行',960,450)+flow('M380 550H240V335','目标级反馈',95,435)
finish(s,'08-hierarchical-timescales','上层和下层的奖励、终止条件、折扣和更新周期需要各自标注。')

# A vector glyph sheet: primitive components for assembling scientific diagrams.
glyphs=[('Agent','<circle cx="44" cy="30" r="17"/><path d="M17 78V66Q44 36 71 66V78"/>'),('Environment','<path d="M10 72L32 25L52 55L67 35L88 72Z"/><circle cx="73" cy="16" r="8"/>'),('Observation','<path d="M4 44Q45 2 86 44Q45 86 4 44Z"/><circle cx="45" cy="44" r="13"/>'),('Action','<path d="M8 43H78M58 23L78 43L58 63"/>'),('Reward','<path d="M45 8L55 31L82 34L62 53L68 80L45 66L22 80L28 53L8 34L35 31Z"/>'),('Policy','<rect x="5" y="8" width="80" height="70" rx="3"/><text x="30" y="57" font-size="38" stroke="none">π</text>'),('Memory','<path d="M15 15H76V76H15Z M25 29H64M25 45H64M25 61H52"/>'),('Graph','<path d="M14 18L74 22L42 72Z M14 18L42 72"/><circle cx="14" cy="18" r="7"/><circle cx="74" cy="22" r="7"/><circle cx="42" cy="72" r="7"/>'),('Sensor','<path d="M45 80V45M23 80H67M28 28Q45 11 62 28M14 17Q45 -8 76 17"/><circle cx="45" cy="42" r="6"/>'),('Constraint','<path d="M45 5L78 20V45Q76 69 45 84Q14 69 12 45V20Z M28 44L40 56L64 30"/>'),('Uncertainty','<path d="M13 65H78 M23 56V30M12 30H34M12 56H34M64 70V15M54 15H74M54 70H74"/>'),('Clock','<circle cx="45" cy="43" r="34"/><path d="M45 18V43L65 56"/>'),('Data','<ellipse cx="45" cy="16" rx="31" ry="10"/><path d="M14 16V70Q45 90 76 70V16M14 43Q45 63 76 43"/>'),('World model','<circle cx="45" cy="43" r="35"/><ellipse cx="45" cy="43" rx="16" ry="35"/><path d="M10 43H80M17 24H73M17 62H73"/>'),('Human feedback','<circle cx="25" cy="23" r="12"/><path d="M7 70V53Q25 30 43 53V70M50 17H85V48H65L53 60V48H50Z"/>'),('Spatial grid','<path d="M7 7H83V83H7ZM7 32H83M7 57H83M32 7V83M57 7V83"/>')]
s=start('强化学习绘图图元','16 个原创可编辑矢量图标；整组复制至 PowerPoint、Inkscape 或 Illustrator 后编辑。')
for i,(name,drawing) in enumerate(glyphs):
 x=85+(i%8)*140;y=170+(i//8)*230
 s+=f'<g id="icon-{name.lower().replace(" ","-")}" transform="translate({x},{y})" fill="none" stroke="{C["green"]}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">{drawing}</g><text x="{x+45}" y="{y+120}" class="small" text-anchor="middle">{name}</text>'
finish(s,'09-rl-icon-sheet','建议：颜色表示语义角色，箭头表示数据或因果方向；相同元素在全文中保持一致。')

s=start('分析图组合草图','空白布局模板，无实验数据。替换为实际结果，并标明统计单位与不确定性。')
panels=[('a  学习效率','环境交互步数','留出评估回报'),('b  实际任务表现','基线与提出方法','物理指标 / 成功率'),('c  策略行为','时间 / 空间位置','动作与系统响应'),('d  风险与权衡','成本 / 风险','收益 / 生态效益')]
for i,(title,xlabel,ylabel) in enumerate(panels):
 x=65+(i%2)*575;y=155+(i//2)*255
 s+=f'<text x="{x}" y="{y}" class="label">{title}</text><path d="M{x+60} {y+35}V{y+175}H{x+490}" fill="none" stroke="{C["ink"]}"/><text x="{x+150}" y="{y+208}" class="small">{xlabel}</text><text x="{x+85}" y="{y+70}" class="small">{ylabel}</text><text x="{x+200}" y="{y+135}" class="small">填入真实实验数据</text>'
finish(s,'10-analysis-panel-layout','在图注写清：随机种子 n、评估事件数、误差带含义、平滑窗口及训练测试隔离。')
print('Created',len(list(OUT.glob('*.svg'))),'original SVG templates')
