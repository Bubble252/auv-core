# auv-core Contract Audit

**状态**：`REF_CORE_AUDIT_PASS`<br>
**日期**：2026-11-13<br>
**范围**：`contracts`、`geometry`、`guidance`、`current`、`control` 的公共数据类、
Protocol、单位和 shape/异常约定。

## Dataclass 与 Protocol

- 公共数据类统一使用 `@dataclass(frozen=True)`；状态、任务、规划结果、场景、
  几何结果和控制诊断均不可原地修改。
- `PlanReason`、`PlanStatus` 使用 `str, Enum`，保持可序列化和稳定取值。
- 边界接口使用 `@runtime_checkable Protocol`：`CurrentField`、`ActuatorCommand`、
  `Guidance`、`SafetyFilter`、`TrackingController`、`SimulatorBackend`。
- 具体实现通过构造函数注入依赖：`UniformCurrent` / `DepthShearCurrent` 实现流场，
  `ThreeDAlosGuidance` 实现制导，`Remus100TrackingController` 实现跟踪控制，
  `PvsRemus100Backend` 适配外部 PVS 动力学。
- 本仓库不新增空壳基类或转发层；`SafetyFilter` 留给容错仓库实现，不在共享层伪造。

## 单位与命名

| 后缀 | 含义 | 例子 |
|---|---|---|
| `_m` | 米 | `position_ned_m`, `goal_radius_m`, `min_clearance_m` |
| `_mps`, `_mps2` | 米/秒、米/秒² | `linear_velocity_body_mps`, `linear_accel_body_mps2` |
| `_rad`, `_rps` | 弧度、弧度/秒 | `quat_xyzw` 姿态角、`angular_velocity_body_rps` |
| `_rpm` | 转/分 | `propeller_rpm`, `speed_integral_rpm` |
| `_s` | 秒 | `t_s`, `stamp_s`, `valid_until_s` |
| `_j` | 焦耳 | `energy_j` |
| 无后缀 | 无量纲、布尔、标识或配置 | `success`, `risk_budget`, `seed`, `name` |

位置统一为 NED，body 速度/加速度统一为 FRD，四元数统一为 `xyzw`。所有公共数组
使用 `FloatArray = NDArray[np.float64]`；向量 shape 为 `(3,)`，四元数为 `(4,)`，
路径为 `(N, 3)` / `(N, 4)`。

## Shape 与异常

- `_validation.as_array/as_vector/as_point` 统一 shape 和有限值检查；
- `finite_positive` / `finite_non_negative` 统一标量范围检查；
- `wrap_angle` 统一到 `[-pi, pi)`，并拒绝非有限角度；
- 原有 `ValueError` 文本由 `tests/test_validation.py` 锁定，公共消费者的 shape 错误
  由 `tests/test_contract_audit.py` 和现有契约测试覆盖。

## 结论

本审计不删除公共 API，不改变算法、单位、坐标系或异常类型；只把重复校验收敛到
`_validation.py` 并用测试固定契约。Step 1 的 dataclass / Protocol / 单位 / shape /
异常项审计通过。
