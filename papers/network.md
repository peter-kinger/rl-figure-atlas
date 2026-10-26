# Efficient and scalable reinforcement learning for large-scale network control

Nature Machine Intelligence · 2024 · 优先阅读

[论文原文](https://www.nature.com/articles/s42256-024-00879-7) · [DOI](https://doi.org/10.1038/s42256-024-00879-7)

局部通信、网络拓扑与环境和模型双缓冲的参考；ND 许可仅链接。

许可：CC BY-NC-ND 4.0。分区详见 [筛选依据](../docs/selection.md)，未宣称已核验中科院一区。

## Fig. 1 全局局部与邻域通信

**用途：** 多智能体。

**画法借鉴：** 统一符号并排比较全局观测、独立学习与邻域协作的信息结构。

**解释边界：** 拓扑相连不意味着允许读取邻居全部内部状态。

[原始图页](https://www.nature.com/articles/s42256-024-00879-7/figures/1)

## Fig. 2 网络化 MDP 与模型学习

**用途：** 多智能体。

**画法借鉴：** 把状态拓扑、模型生成经验和真实环境经验分开。

**解释边界：** 模型偏差和局部信息近似误差应分别评价。

[原始图页](https://www.nature.com/articles/s42256-024-00879-7/figures/2)

## Fig. 3 性能与通信样本效率

**用途：** 敏感性与消融。

**画法借鉴：** 同一研究中同时展示任务回报、通信开销和采样效率。

**解释边界：** 只比较峰值回报可能掩盖显著资源差异。

[原始图页](https://www.nature.com/articles/s42256-024-00879-7/figures/3)
