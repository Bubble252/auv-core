# auv-core

`auv-core` 是全局规划器 `auv-planner` 与局部规划器 `auv-local` 共用的稳定基础层。

当前内容包括：

- 车辆、状态、轨迹、任务、规划和执行契约；
- 姿态与四元数工具；
- 几何、碰撞与 sweep 工具；
- 海流模型与 3D ALOS 制导；
- REMUS100 跟踪控制、PVS 动力学和共享场景构造。

全局规划算法、恢复证书算法、局部反应式策略和强化学习代码不在此仓库。

## 安装

```bash
uv pip install -e .
```

## 边界检查

在工作区根目录运行：

```bash
python scripts/check_repo_dependencies.py --check
```
