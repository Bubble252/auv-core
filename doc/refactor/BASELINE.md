# auv-core Refactor Baseline

**状态**：`REF_CORE_READY`<br>
**仓库**：`settled_共享基础`（发行名 `auv-core`）<br>
**基线 commit**：`fdbfcc1`<br>
**日期**：2026-11-13

## 测试与检查

| 检查 | 命令 | 基线 |
|---|---|---|
| pytest | `/home/bubble/水下机器人/.venv/bin/python -m pytest -q tests` | `24 passed, 5 skipped` |
| ruff | `/home/bubble/水下机器人/.venv/bin/python -m ruff check src tests` | PASS |
| format | `/home/bubble/水下机器人/.venv/bin/python -m ruff format --check src tests` | PASS |
| shape | `/home/bubble/水下机器人/.venv/bin/python /home/bubble/水下机器人/总协调/scripts/check_code_shape.py --root . --check` | 0 new；存量 25 条在 `CODE_SHAPE_BASELINE.json` |
| dependency | `/home/bubble/水下机器人/.venv/bin/python /home/bubble/水下机器人/scripts/check_repo_dependencies.py --check` | PASS（工作区根执行） |

## 已知失败与跳过

- 5 个 PVS 测试因外部 `PythonVehicleSimulator` checkout 或其绘图依赖不可用而跳过；
  这是环境缺包，不是通过。
- `contracts.py`（695 行）和 `geometry.py`（544 行）超过新库模块硬上限；已进入
  ratchet baseline，触碰时必须拆分完整职责或写 waiver。
- `mypy` 的两个外部 PVS stub 错误保留在 G01 记录中，不在本候选混入修复。

## 等价性入口

```bash
/home/bubble/水下机器人/.venv/bin/python \
  /home/bubble/水下机器人/总协调/scripts/check_refactor_equivalence.py \
  --expected <before.json> --actual <after.json>
```

候选级证据记录在 `doc/refactor/EQUIVALENCE.md`。

## 回滚点

- 基线 commit：`fdbfcc1`；
- 回滚方式：`git revert <candidate-commit>`，不在 `main` 上 `reset --hard`；
- 回滚后重新运行本页全部命令。
