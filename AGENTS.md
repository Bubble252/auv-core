# settled_共享基础 项目规则

本仓库只承载全局规划器与局部规划器共同依赖的稳定契约和基础设施。

## 仓库

- 当前独立路径：`/home/bubble/水下机器人/settled_共享基础`。
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

## 治理入口

- 工作区规则：`/home/bubble/水下机器人/AGENTS.md`；
- canonical 代码规范：`/home/bubble/水下机器人/总协调/doc/governance/CODE_STYLE.md`；
- 接口与单位契约：`/home/bubble/水下机器人/总协调/doc/governance/CODE_INTERFACE_CONTRACT.md`；
- Goal / matrix / ledger schema：`/home/bubble/水下机器人/总协调/configs/governance/`。

本仓库不复制上述正文。新增 Goal、实验矩阵或 research 记录时，先读 canonical
文档；共享层本身不承载 Goal 历史、artifact 或训练配置。

## 验证

```bash
pytest -q tests
ruff check src tests
ruff format --check src tests
python /home/bubble/水下机器人/总协调/scripts/check_code_shape.py --root . --check
python /home/bubble/水下机器人/scripts/check_repo_dependencies.py --check
```

`mypy src` 仍会在外部 PVS 依赖上报告 2 个缺少 stub 的错误；这是已登记基线，
不能通过关闭检查或增加无到期 waiver 隐藏。

重构基线、模块职责、候选和 G04 交接边界见 `doc/refactor/`：

- `BASELINE.md`：测试、已知失败和回滚点；
- `INVENTORY.md`：允许/禁止目录、自动化候选和人工批准点；
- `MODULE_MAP.md`：模块职责与非职责；
- `EQUIVALENCE.md`：CORE-D1/D2 行为等价证据。

## Git

- 禁止 `git add -A`；只 add 明确文件。
- 提交前运行 `git diff --cached --check`。
- 不自动 commit / push，除非用户明确要求。
