# auv-core Refactor Inventory

**状态**：`REF_CORE_COMPLETE`<br>
**仓库**：`settled_共享基础`（发行名 `auv-core`）<br>
**基线 commit**：`fdbfcc1`<br>
**日期**：2026-11-13

## 1. 范围与规模

| 对象 | 数量 / 位置 |
|---|---|
| Python 源码 | 13 个模块，`src/auv_core/` |
| 测试 | 7 个测试模块，35 项执行、5 项外部依赖跳过 |
| 公共契约 | `contracts.py`、`interfaces.py`、`attitude.py`、`guidance.py`、`geometry.py` |
| 可修改目录 | `src/auv_core/`、`tests/`、`doc/refactor/` |
| 禁止目录 | `artifacts/`、`outputs/`、`checkpoints/`、`third_party/`、外部 PVS/MSS 源码目录 |

共享层不承载 Goal 历史、artifact、训练配置、局部策略或全局规划实验。

## 2. 验证命令与基线

```bash
cd /home/bubble/水下机器人/settled_共享基础/.worktrees/ref-core-20261113
/home/bubble/水下机器人/.venv/bin/python -m pytest -q tests
/home/bubble/水下机器人/.venv/bin/python -m ruff check src tests
/home/bubble/水下机器人/.venv/bin/python -m ruff format --check src tests
/home/bubble/水下机器人/.venv/bin/python -m mypy src
/home/bubble/水下机器人/.venv/bin/python \
  /home/bubble/水下机器人/总协调/scripts/check_code_shape.py --root . --check
/home/bubble/水下机器人/.venv/bin/python \
  /home/bubble/水下机器人/scripts/check_repo_dependencies.py --check
```

| 检查 | 当前结果 | 说明 |
|---|---|---|
| pytest | `35 passed, 5 skipped` | 5 项需要外部 PVS/绘图依赖 |
| ruff | PASS | 全仓 `src tests` |
| format | PASS | 21 个文件已格式化 |
| mypy | `2 errors / 1 file` | 外部 PVS 包缺少 stubs，未新增 |
| shape | `0 new / 19 suppressed` | 存量 ratchet |
| dependency | PASS | 无反向或跨仓库源码导入 |

## 3. 允许与禁止

- 允许标准库、NumPy 和纯计算方法；不得启动仿真、读 artifact 或修改全局 RNG。
- 公共契约变更必须同时更新消费者 smoke、测试和 Goal。
- 不得导入 `auv_planner`、`auv_local`、`auv_rl`、`auv_lowlevel` 或
  `auv_isaaclab`。
- 不得把局部规划器、全局规划器或训练代码移入本仓库。
- PVS 只作为外部资产适配边界，不复制其源码。

## 4. 已完成重构

| 候选 | 内容 | 结果 |
|---|---|---|
| CORE-D1 | 收敛有限值、正数、非负数和数组 shape 校验 | PASS；异常类型/文本和公共 API 不变 |
| CORE-D2 | 收敛角度归一化 helper | PASS；NaN/Inf 与边界行为由 fixture 锁定 |
| CONTRACT-AUDIT | dataclass、Protocol、单位、shape 审计 | PASS；无空壳基类或跨仓库依赖 |

## 5. G04 自动化候选与人工批准点

| 级别 | 候选 | 证伪条件 | 自动化边界 |
|---|---|---|---|
| L0 | 对候选 diff 运行 ruff import 排序和 format，仅修改被触碰文件 | ruff/format 失败或产生 API diff | 可在 shadow 后自动写入 |
| L1 | 为外部 `python_vehicle_simulator` 增加本地 `.pyi` stub，使 mypy 从 2 errors 降到 0 | mypy 仍有错误，或运行测试/外部 PVS smoke 回退 | 先生成 patch，人工批准 |

以下内容不得自动修改：`contracts.py` 公共字段、单位/坐标系、`__all__`、Protocol
签名、PVS/MSS 适配边界、`CODE_SHAPE_BASELINE.json` 和任何消费者契约。

G04 shadow 扫描必须只读；任何自动写入都必须在独立 worktree 中先跑本页全部检查，
并保留 `git diff` 供人工审查。
