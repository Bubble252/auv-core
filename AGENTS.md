# settled_共享基础 项目规则

本仓库只承载全局规划器与局部规划器共同依赖的稳定契约和基础设施。

## 仓库

- 当前独立路径：`/home/bubble/水下机器人-meta-g02/settled_共享基础`。
- 分支：`main`；发行名：`auv-core`。
- 安装顺序：本仓库先安装，随后才能安装 `auv-planner` 或 `auv-local`。
- 根工作区只保留引用，不跟踪本目录。

## 边界

- Python 发行名：`auv-core`；源码包：`auv_core`。
- 只允许 NumPy 作为运行时第三方依赖。
- `auv_core` 禁止导入 `auv_planner`、`auv_local`、`auv_rl`、`auv_lowlevel`
  或 `auv_isaaclab`。
- 全局规划算法、局部反应式策略、学习训练代码和实验入口不得进入本仓库。
- 修改公共契约时必须同时运行共享层测试，并通知两个消费者仓库。

## 验证

```bash
python -m pytest -q
python ../scripts/check_repo_dependencies.py --check
```

## Git

- 禁止 `git add -A`；只 add 明确文件。
- 提交前运行 `git diff --cached --check`。
- 不自动 commit / push，除非用户明确要求。
