# Deep-reinforcement-learning-based water diversion strategy

Environmental Science and Ecotechnology · 2024 · 优先阅读

[论文原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC10405199/) · [DOI](https://doi.org/10.1016/j.ese.2023.100298)

过程模型加 DDPG、SHAP、权重敏感性与环境参数不确定性；仅链接原图。

许可：CC BY-NC-ND 4.0。分区详见 [筛选依据](../docs/selection.md)，未宣称已核验中科院一区。

## Fig. 1 过程模型与强化学习耦合

**用途：** MDP 框架。

**画法借鉴：** 借鉴物理过程环境和学习算法的双层组织，初始化与交互用不同线型。

**解释边界：** 原文为 CC BY-NC-ND；本库仅提供来源入口。

[原始图页](https://pmc.ncbi.nlm.nih.gov/articles/PMC10405199/figure/fig1/)

## Fig. 6 水质与调水量同时评价

**用途：** 多目标权衡。

**画法借鉴：** 把水质、控制量和总回报分面呈现，检查是否以水量换水质。

**解释边界：** 回报权重变化后，总回报不能直接横向比较。

[原始图页](https://pmc.ncbi.nlm.nih.gov/articles/PMC10405199/figure/fig6/)

## Fig. 7 SHAP 解释调控动作

**用途：** 策略解释。

**画法借鉴：** 把全局贡献与变量相互作用分开，注明解释对象是动作还是价值。

**解释边界：** SHAP 解释模型关联，不证明物理因果作用。

[原始图页](https://pmc.ncbi.nlm.nih.gov/articles/PMC10405199/figure/fig7/)

## Fig. 8 奖励与时间尺度敏感性

**用途：** 敏感性与消融。

**画法借鉴：** 将目标权重、控制间隔与优化超参数分开讨论。

**解释边界：** 控制间隔改变时，时间累计奖励和折扣需要一致。

[原始图页](https://pmc.ncbi.nlm.nih.gov/articles/PMC10405199/figure/fig8/)

## Fig. 9 过程模型不确定性压力测试

**用途：** 稳健性与风险。

**画法借鉴：** 同一策略在多组环境参数下测试，比较水质和决策响应。

**解释边界：** 模拟器参数扰动不是对未来气候全部不确定性的覆盖。

[原始图页](https://pmc.ncbi.nlm.nih.gov/articles/PMC10405199/figure/fig9/)
