# 强化学习论文常见分析图

先写科学问题，再选图形。下表中的建议是本库的分析设计，不代表所列论文都使用了这些统计方法。

| 科学问题 | 建议图形与数据 | 可借鉴的图 | 必须避免 |
|---|---|---|---|
| 是否学会、用了多少交互 | 学习曲线：环境交互步数 × 留出评估表现；独立随机种子 | [流场 Fig. 2](../papers/navigation.md)、[AI Economist Fig. 2](../papers/economist.md) | 只报训练奖励；把时间步当独立样本 |
| 与传统方法相比好多少 | 配对任务指标、分布图和效应量；共同测试事件 | [CAPTAIN Fig. 5](../papers/biodiversity.md)、[Dreamer Fig. 4](../papers/dreamer.md) | 只有 RL 算法互比，缺少规则、MPC 或优化基线 |
| 实际物理目标是否改善 | 物理单位的结果曲线 / 误差分布 | [托卡马克 Fig. 2](../papers/tokamak.md)、[调水 Fig. 6](../papers/water.md) | 总奖励变化替代水质、能耗等实际指标 |
| 策略在何时做了什么 | 共用时间轴的驱动、动作、状态和目标响应 | [冷原子 Fig. 2](../papers/cold-atoms.md)、[无人机 Fig. 4](../papers/drone.md) | 将所有变量叠在一个多重坐标轴上 |
| 策略的空间规律是什么 | 同尺度轨迹、动作场、空间优先级地图 | [流场 Fig. 3、5](../papers/navigation.md)、[CAPTAIN Fig. 6](../papers/biodiversity.md) | 截取最成功个例、不显示失败 |
| 输入怎样关联到动作 | 条件动作图、SHAP、局部敏感性；固定解释对象 | [调水 Fig. 7](../papers/water.md) | 将 SHAP 直接解释为物理因果贡献 |
| 哪个模块有效 | 移除单一机制的性能对比；一致计算预算 | [Dreamer Fig. 6](../papers/dreamer.md) | 同时改变多个模块却归因于一个模块 |
| 对参数是否敏感 | 关键权重 / 控制间隔的曲线或热图 | [调水 Fig. 8](../papers/water.md)、[撕裂控制 Fig. 4](../papers/tearing.md) | 只画最佳参数，隐去失败区间 |
| 对缺测和观测噪声是否可靠 | 观测质量 × 成功率 / 物理目标 | [CAPTAIN Fig. 2](../papers/biodiversity.md) | 用训练时全部已见扰动宣称未知稳健性 |
| 能否迁移到新场景 | 训练场景 × 测试场景矩阵，零样本和微调分开 | [流场 Fig. 7](../papers/navigation.md)、[城市规划 Fig. 2](../papers/urban.md) | 将重新训练后的表现称为直接泛化 |
| 极端情形是否安全 | 违例率、严重度、失败时间与尾部损失 | [撕裂控制 Fig. 2、4](../papers/tearing.md) | 均值良好就宣称安全；漏掉失败终止 |
| 多目标之间怎样交换 | 非支配结果、目标散点与参考点；各目标有单位 | [CAPTAIN Fig. 3](../papers/biodiversity.md)、[AI Economist Fig. 3](../papers/economist.md) | 将不同权重的几个点称为完整 Pareto 前沿 |
| 多主体如何协作或获益 | 主体收益分布、资源流、局部与整体指标 | [AI Economist Fig. 4、9](../papers/economist.md)、[网络控制 Fig. 1](../papers/network.md) | 只有社会总量，掩盖个体损失 |
| 性能代价能否接受 | 交互样本、训练耗时、推理延迟、通信量与收益 | [AlphaTensor Fig. 5](../papers/alphatensor.md)、[网络控制 Fig. 3](../papers/network.md) | 仅用“更快”描述不同硬件与训练预算 |

## 可执行的最小实验组合

对于地球系统中的序贯决策论文，先准备：一张决策框架图、一组留出评估的学习曲线、一组相同情景下的物理结果比较、一组策略行为解释，以及一组跨情景或扰动测试。存在安全条件或多个利益目标时，增加约束和权衡结果。

每项比较至少记录：方法、训练种子、评估事件 / 年份 / 区域、是否在训练中出现、环境交互预算、物理目标、总回报、违例情况、计算开销。重复次数按实验变异与算力确定；不把任意固定次数宣称为充分统计保证。

## 数据表结构建议

训练数据可用 `method, seed, env_steps, eval_return, eval_physical_metric`。每个独立训练种子先在固定测试集上汇总，再跨种子计算区间。带相关性的事件或时间序列不能直接按每个时刻独立重采样。

行为数据可用 `scenario, method, seed, episode, time, state_name, state_value, action_name, action_value, reward, constraint_cost`。多主体追加 `agent_id`；空间动作追加坐标与参考系统。

明确误差带含义：标准差表示离散程度；标准误反映均值估计精度；置信区间依赖抽样假设和计算方法。保留未平滑结果，写出平滑窗口。不同回报尺度、不同训练预算或测试分布不应直接比较。

## 推荐的图序

Fig. 1 研究问题与 MDP → Fig. 2 主要效果 → Fig. 3 策略行为 → Fig. 4 稳健性 / 泛化 → Fig. 5 机制与权衡。若论文的关键贡献是安全或多主体治理，应把对应结果前移。

[四面板空白分析模板](../templates/10-analysis-panel-layout.svg) 仅提供版式，不含示意实验曲线。
