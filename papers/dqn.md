# Human-level control through deep reinforcement learning

Nature · 2015 · 经典补充

[论文原文](https://www.nature.com/articles/nature14236) · [DOI](https://doi.org/10.1038/nature14236)

经典 DQN，原图保留链接；不要把其价值网络误画成直接输出连续控制。

许可：需另行授权。分区详见 [筛选依据](../docs/selection.md)，未宣称已核验中科院一区。

## Fig. 1 观测到动作价值的映射

**用途：** MDP 框架。

**画法借鉴：** 区分输入观测、特征提取和每个离散动作的 Q 值。

**解释边界：** Q 值不是动作概率。

[原始图页](https://www.nature.com/articles/nature14236)

## Fig. 2 回报与价值估计并行监测

**用途：** 学习曲线。

**画法借鉴：** 将任务表现与内部价值估计放在不同坐标轴或面板。

**解释边界：** 价值估计升高不一定代表策略表现改善。

[原始图页](https://www.nature.com/articles/nature14236)
