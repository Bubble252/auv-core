# auv-core Module Map

**状态**：`REF_CORE_COMPLETE`<br>
**用途**：说明共享层的职责、边界、公共 API、测试和重构豁免。

## 模块清单

| 模块路径 | 主要职责 | 非职责 | 公共 API | 对应测试 | Owner | Waiver |
|---|---|---|---|---|---|---|
| `src/auv_core/_validation.py` | 内部数组、有限值、正数和角度校验 | 不定义业务契约 | 无（以下划线模块为内部实现） | `tests/test_validation.py` | core | 无 |
| `src/auv_core/__init__.py` | 惰性导出稳定公共符号 | 不实现几何或控制算法 | `__all__` 中的全部公共符号 | `tests/test_import_boundary.py` | core | 无 |
| `src/auv_core/contracts.py` | 状态、任务、规划结果、执行器与评价契约 | 不读文件、不启动仿真、不做规划 | `contracts.__all__` | 契约与消费方 smoke | core | 存量文件长度 |
| `src/auv_core/attitude.py` | 四元数与姿态角转换 | 不实现制导律或控制器 | `attitude.__all__` | `tests/test_guidance.py` 等 | core | 无 |
| `src/auv_core/current.py` | 均匀流和深度剪切流采样 | 不实现控制器 | `DepthShearCurrent`, `UniformCurrent` | `tests/test_current.py` | core | 无 |
| `src/auv_core/geometry.py` | 船体扫掠、障碍物距离和间隙计算 | 不规划路径、不改状态 | `geometry.__all__` | `tests/test_geometry.py` | core | 存量文件长度 |
| `src/auv_core/guidance.py` | 三维 ALOS 制导与参考生成 | 不输出执行器命令 | `AlosSolution`, `ThreeDAlosGuidance` | `tests/test_guidance.py` | core | 存量函数长度/复杂度 |
| `src/auv_core/interfaces.py` | Guidance、SafetyFilter、TrackingController、SimulatorBackend 协议 | 不实现具体策略 | `interfaces.__all__` | `tests/test_import_boundary.py` | core | 无 |
| `src/auv_core/scenarios.py` | 固定与 M5 场景构造 | 不执行训练、不读 artifact | `scenarios.__all__` | 消费方 smoke | core | 无 |
| `src/auv_core/control/remus100.py` | REMUS100 跟踪控制器 | 不推进动力学、不读环境 | `control.__all__` | `tests/test_pvs_remus100.py` | core | 存量函数长度/复杂度 |
| `src/auv_core/dynamics/remus100.py` | PVS REMUS100 后端适配 | 不定义控制律、不读 artifact | `PvsRemus100Backend` | `tests/test_pvs_remus100.py` | core | 外部 PVS 边界 |
| `src/auv_core/control/__init__.py` | 控制子包导出 | 不实现控制算法 | `control.__all__` | 消费者 import smoke | core | 无 |
| `src/auv_core/dynamics/__init__.py` | 动力学子包导出 | 不实现动力学算法 | `dynamics.__all__` | 消费者 import smoke | core | 无 |

## 边界说明

| 模块 | 允许依赖 | 禁止依赖 | 说明 |
|---|---|---|---|
| `auv_core` | 标准库、NumPy | `auv_planner`、`auv_local`、`auv_rl`、`auv_lowlevel`、`auv_isaaclab` | 共享契约和纯计算，不反向依赖消费者 |
| `_validation` | 标准库、NumPy | `contracts` 及其他业务模块 | 只提供无状态校验，避免循环 import |
| `guidance` / `control` | `contracts`、`attitude`、`_validation` | 规划器、学习框架、仿真环境 | 控制器和制导器保持可单测 |
| `dynamics/remus100` | PVS 外部源码和 `contracts` | 规划器、局部策略 | PVS 路径只作为外部资产适配，不做跨仓库源码 import |

## 变更规则

- 修改公共 API、模块边界或继承层级时，同步更新本表和测试。
- 新增模块必须有 3–6 行模块 docstring，说明职责、边界、关键不变量和输入输出。
- `_validation.py` 以下划线开头，属于包内实现；消费者不得直接依赖它。
