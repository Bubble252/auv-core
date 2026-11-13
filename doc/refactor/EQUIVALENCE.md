# auv-core Equivalence Evidence

**状态**：`REF_CORE_PASS`<br>
**用途**：记录 CORE-D1 / CORE-D2 重构前后的行为等价证据。

## 候选信息

```yaml
goal: META-G03
candidate: CORE-D1 + CORE-D2
repository: settled_共享基础
base_commit: fdbfcc1
branch: refactor/core-20261113
files:
  - src/auv_core/_validation.py
  - src/auv_core/contracts.py
  - src/auv_core/attitude.py
  - src/auv_core/current.py
  - src/auv_core/geometry.py
  - src/auv_core/guidance.py
  - src/auv_core/control/remus100.py
public_api_change: none
```

## 行为契约

| 项目 | 重构前 | 重构后 | 证据 |
|---|---|---|---|
| 输入 shape / dtype | 三维向量、有限值、float64 | 保持相同校验和错误消息 | `tests/test_validation.py` + 现有契约测试 |
| 输出 shape / dtype | 三维 `float64` | 保持相同 | 同上 |
| 单位 / 坐标系 | NED / body FRD，角度 rad | 保持相同 | 不改变调用方单位 |
| 异常类型和消息 | `ValueError`，shape/finite/positive 消息 | 保持相同 | 负控测试逐条断言 |
| manifest / artifact 字段 | 无 | 无 | 本候选不产生 artifact |
| RNG 调用次数和顺序 | 无随机性 | 无随机性 | 静态检查 |
| 全局状态前后变化 | 无 | 无 | 纯 helper |

## 测试命令

```bash
/home/bubble/水下机器人/.venv/bin/python -m pytest -q tests
/home/bubble/水下机器人/.venv/bin/python -m ruff check src tests
/home/bubble/水下机器人/.venv/bin/python -m ruff format --check src tests
/home/bubble/水下机器人/.venv/bin/python \
  /home/bubble/水下机器人/总协调/scripts/check_code_shape.py --root . --check
/home/bubble/水下机器人/.venv/bin/python \
  /home/bubble/水下机器人/总协调/scripts/check_refactor_equivalence.py \
  --expected tests/fixtures/refactor/core-d1-d2/before.json \
  --actual tests/fixtures/refactor/core-d1-d2/after.json
```

消费者 smoke 在独立 `/tmp` 环境安装 refactor 版 `auv-core`，再以 `--no-deps`
安装两个消费者，不使用跨仓库 `PYTHONPATH`：

```bash
uv venv --python /home/bubble/水下机器人/.venv/bin/python /tmp/auv-core-consumer-smoke
uv pip install --python /tmp/auv-core-consumer-smoke/bin/python \
  -e /home/bubble/水下机器人/settled_共享基础/.worktrees/ref-core-20261113
uv pip install --python /tmp/auv-core-consumer-smoke/bin/python --no-deps \
  -e /home/bubble/水下机器人/settled_全局规划器
uv pip install --python /tmp/auv-core-consumer-smoke/bin/python --no-deps \
  -e /home/bubble/水下机器人/settled_局部规划器_反应式
/tmp/auv-core-consumer-smoke/bin/python -c \
  "from auv_planner import State, ThreeDAlosGuidance, Reference, hull_clearance; \
   from auv_local import LocalObservation, ReactivePolicy; \
   from auv_lowlevel import LowLevelConfig, ReferencePath; \
   print(State, ThreeDAlosGuidance, Reference, hull_clearance, LocalObservation, \
         ReactivePolicy, LowLevelConfig, ReferencePath)"
```

## 结果

- 通过数：`32 passed`
- 跳过数：`5 skipped`（外部 PVS/绘图依赖不可用）
- 已知失败：无新增；存量跳过单独列在 `BASELINE.md`
- 是否新增失败：`no`
- 消费者 smoke：`PASS`（`auv_planner`、`auv_local`、`auv_lowlevel` 均能加载 refactor 版 core 的公共符号）
- 回滚 commit：`3980b25`（REF-CORE 文档与基线提交）
- 等价性 fixture：`tests/fixtures/refactor/core-d1-d2/{before,after}.json`
- 结论：`PASS`

## 人工检查

- [x] 公共 API 删除数为 0；
- [x] 没有修改 reward、termination、success、seed split 或 held-out；
- [x] 没有移动或删除 artifact；
- [x] RNG/时钟/全局状态不适用；
- [x] 只改共享基础仓库。
