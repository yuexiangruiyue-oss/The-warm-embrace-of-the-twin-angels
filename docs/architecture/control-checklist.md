# 控制清单 — 《双生天使的拥抱》

| 字段 | 值 |
|---|---|
| 文档版本 | 1.0 |
| 作者 | 程基岩（技术主程） |
| 日期 | 2025-07-14 |
| 用途 | 开发前控制点、编码标准、Code Review 检查表 |
| 关联文档 | `main-architecture.md`、`ADR-001~004` |

> **使用方式**：本清单是程序员可立即执行的一页规则。每个 Story 实现前对照 §1 确认前置条件；编码时对照 §2 遵守编码标准；提交 PR 时对照 §3 通过检查清单。

---

## 1. 开发前控制点

### 1.1 开始任何 Story 前，确认以下前置条件

| # | 控制点 | 确认方式 | 不满足时的行动 |
|---|---|---|---|
| 1 | 已读对应 GDD 章节 | 阅读记录 | 停止，先读 GDD |
| 2 | 已读主架构对应章节 | 阅读记录 | 停止，先读架构 |
| 3 | 已读相关 ADR | 阅读记录 | 停止，先读 ADR |
| 4 | 共享变量所有权已确认 | 查阅主架构 §4.4 | 停止，先确认所有权 |
| 5 | 接口契约已确认 | 查阅主架构 §3.4 | 停止，先确认接口 |
| 6 | JSON 数据结构已定义 | 查阅主架构 §5 | 停止，先定义数据结构 |
| 7 | 引擎 API 不确定时已标记 | 查阅 `docs/engine-reference/renpy/VERSION.md` | 标记知识缺口，回问主理人 |

### 1.2 GDD 更新确认

在开始涉及以下系统的 Story 前，确认 GDD 已更新：

| 系统 | GDD 更新内容 | 确认方式 |
|---|---|---|
| C2 天使系统 | 翅膀亮度改为双变量模型 | GDD 中出现 `wing_brightness_permanent` |
| C5 存在保护 | 翅膀亮度扣减改为双层模型 | GDD 中出现双层模型公式 |
| C3 选择系统 | 选项数据结构含 `confrontation_tag` | GDD 选项结构含此字段 |
| C4 Sephirot | `confrontation_tag` 与选项数据结构对齐 | GDD 引用的选项结构含此字段 |

---

## 2. 编码标准（按路径作用域）

### 2.1 通用规则（所有代码）

| 规则 | 描述 | 违反后果 |
|---|---|---|
| 验证驱动 | 先写测试，再实现。每个公开方法至少 1 个测试用例 | PR 拒绝 |
| 无硬编码 | 魔法数字必须提取为常量，定义在 `definitions.rpy` 或模块顶部 | PR 拒绝 |
| TODO 格式 | `# TODO[TASK-ID]: 描述` | 格式不符 PR 评论 |
| 类型注解 | Python 函数必须包含参数和返回值类型注解 | PR 评论 |
| 文档字符串 | 公开方法必须包含 docstring | PR 评论 |
| 无不可序列化对象 | 存档变量中不包含函数引用、文件句柄、线程对象 | BLOCKER |

### 2.2 叙事层（`scripts/ch*.rpy`）

| 规则 | 描述 |
|---|---|
| 仅含叙事 | label 内仅含 `scene`/`show`/`say`/`play`/`stop`/`call`/`jump` 和系统层接口调用 |
| 不直接修改状态 | 禁止直接赋值 `angel.bond_depth = 0.5` 等；必须通过系统层接口 |
| 不直接操作 JSON | 禁止 `json.load()`；数据加载由系统层负责 |
| label 命名 | `chXX_bYY_beat_type`（如 `ch04_b01_encounter`） |
| 场景结束钩子 | 每个场景 label 结尾调用 `C5.recover_temporary_dim()` 恢复临时暗淡 |

### 2.3 系统层（`systems/*.py`）

| 规则 | 描述 |
|---|---|
| 纯逻辑 | 不含叙事文本（`"天使说..."` 等）；不调用 Ren'Py 的 `say`/`scene` |
| 接口契约 | 公开方法签名必须与主架构 §3.4 一致；变更需更新架构文档 |
| 单一所有权 | 每个共享变量仅在其所有者模块中直接修改；其他模块通过接口 |
| 依赖方向 | 遵守 ADR-003 §依赖方向图；禁止反向依赖 |
| 无热路径分配 | core 模块避免在循环中创建对象（本项目无高频循环，但原则保留） |
| 可调试 | 关键状态变更含 `renpy.log()` 或 print 调试日志（debug 模式） |
| 可测试 | 每个公开方法可独立单元测试（依赖通过构造函数注入，可 mock） |

### 2.4 数据层（`data/**/*.json`）

| 规则 | 描述 |
|---|---|
| JSON Schema 合规 | 所有 JSON 文件通过对应 Schema 校验 |
| 无函数引用 | JSON 中不包含 Python 代码或函数引用 |
| 字段完整性 | 必填字段不可缺失；可选字段显式标记为 null |
| 命名规范 | ID 格式：`chXX_cYY_oZZ`（选项）、`chXX_bYY_type`（节拍）、`chXX_sephirot_name`（质点） |
| 校验脚本通过 | `python tools/validate_data.py` 无错误 |

### 2.5 界面层（`gui/*.rpy`）

| 规则 | 描述 |
|---|---|
| 不持有游戏状态 | Screen 从系统层读取状态，不自行维护状态 |
| 状态读取用接口 | 通过 `angel.get_wing_brightness_displayed()` 等接口读取，不直接访问变量 |
| 用户输入转发 | 用户操作（点击/选择）通过系统层接口处理，不直接修改变量 |
| 无障碍 | 文字大小支持 4 级；色彩对比度满足 WCAG AA；支持 self-voicing |
| 1920×1080 基准 | 所有 Screen 以 1920×1080 为基准设计，支持等比缩放 |

---

## 3. Code Review 检查表

### 3.1 架构一致性检查

| # | 检查项 | 通过条件 | 严重性 |
|---|---|---|---|
| A1 | 共享变量所有权 | 变量仅在所有者模块中直接修改 | BLOCKER |
| A2 | 依赖方向 | 无反向依赖（见 ADR-003） | BLOCKER |
| A3 | 接口契约 | 公开方法签名与架构 §3.4 一致 | BLOCKER |
| A4 | 层级分离 | 叙事层不直接操作数据层；界面层不持有状态 | BLOCKER |
| A5 | 数据驱动 | 叙事内容来自 JSON，不硬编码在脚本中 | MAJOR |

### 3.2 数据一致性检查

| # | 检查项 | 通过条件 | 严重性 |
|---|---|---|---|
| D1 | confrontation_tag 与 progress_value 一致 | ENGAGE→1.0, ESCAPE→0.3, NEUTRAL→0.0 | BLOCKER |
| D2 | narrative_jump 目标存在 | 跳转目标 label 存在于脚本中 | BLOCKER |
| D3 | angel_response_delta 字段合法 | 仅含 warmth/depth/protectiveness/vulnerability | MAJOR |
| D4 | bond_depth_delta 范围 | -0.05 ~ 0.15 | MAJOR |
| D5 | JSON Schema 校验通过 | `validate_data.py` 无错误 | BLOCKER |

### 3.3 翅膀亮度模型检查

| # | 检查项 | 通过条件 | 严重性 |
|---|---|---|---|
| W1 | 双变量模型 | 使用 `wing_brightness_permanent` + `wing_brightness_temporary`，不使用单变量 `wing_brightness` | BLOCKER |
| W2 | 显示值计算 | `max(0.05, permanent - temporary)` | BLOCKER |
| W3 | 代价下限 | `max(wing_stage_baseline[stage] × 0.15, permanent)` | BLOCKER |
| W4 | 临时暗淡恢复 | 场景结束调用 `recover_temporary_dim()` | MAJOR |
| W5 | 阶段切换重置 | `update_wing_stage()` 重置 permanent 到新基线 + temporary 归零 | BLOCKER |
| W6 | Ch16 叙事重置 | `wing_brightness_permanent` 重置为 1.0 | BLOCKER |

### 3.4 状态管理检查

| # | 检查项 | 通过条件 | 严重性 |
|---|---|---|---|
| S1 | bond_depth 写入者 | 仅 C3（选择）、C2（拥抱/询问）、C4（Ch13）可写入 | BLOCKER |
| S2 | angel_intervention_count 写入者 | 仅 C5 可写入 | BLOCKER |
| S3 | angel_emotional_state 写入者 | 仅 C2 可写入（C5 通过 `angel_intervene()` 委托） | BLOCKER |
| S4 | sephirot_progress 写入者 | 仅 C4 可写入 | BLOCKER |
| S5 | 存档变量用 default | 所有可序列化状态用 `default` 声明 | BLOCKER |
| S6 | 持久变量用 persistent | 跨周目数据用 `persistent.` 前缀 | BLOCKER |

### 3.5 测试检查

| # | 检查项 | 通过条件 | 严重性 |
|---|---|---|---|
| T1 | 公开方法有测试 | 每个公开方法至少 1 个测试用例 | MAJOR |
| T2 | 边界场景测试 | 翅膀亮度触底、bond_depth 溢出、escape_count=3 等边界有测试 | MAJOR |
| T3 | 存档/读档测试 | `AngelState` 完整序列化/反序列化测试通过 | BLOCKER |
| T4 | 数据校验测试 | `validate_data.py` 在 CI 中通过 | BLOCKER |

### 3.6 无障碍检查

| # | 检查项 | 通过条件 | 严重性 |
|---|---|---|---|
| AC1 | 文字大小 4 级 | small/normal/large/extra_large 均不溢出对话框 | MAJOR |
| AC2 | 色彩对比度 | 文字与背景对比度 ≥ 4.5:1（WCAG AA） | MAJOR |
| AC3 | self-voicing | 关键 UI 元素有 self-voicing 文本 | MAJOR |
| AC4 | 键盘可操作 | 所有选择可用键盘完成 | MAJOR |

---

## 4. 系统初始化顺序

系统实例化必须按以下顺序进行（依赖顺序）：

```python
# init python:
# 1. 加载数据
data = load_all_data()

# 2. 基础层
save_manager = SaveManager()           # C6: 无依赖
narrative_engine = NarrativeEngine(data['sephirot'], data['choices'])  # C1: 依赖 data

# 3. 核心层
angel_system = AngelSystem(data['angel'])          # C2: 依赖 data
choice_system = ChoiceSystem(data['choices'])      # C3: 依赖 data
protection_system = ProtectionSystem(data['protection'])  # C5: 依赖 data

# 4. 注入依赖
choice_system.set_angel_system(angel_system)       # C3 → C2
choice_system.set_sephirot_system(sephirot_system) # C3 → C4
choice_system.set_protection_system(protection_system)  # C3 → C5
protection_system.set_angel_system(angel_system)   # C5 → C2

# 5. 玩法层
sephirot_system = SephirotSystem(data['sephirot'])  # C4: 依赖 data
sephirot_system.set_angel_system(angel_system)      # C4 → C2

# 6. 叙事引擎注入
narrative_engine.set_systems(
    angel_system, choice_system, protection_system, sephirot_system
)
```

---

## 5. 常量速查表

开发时快速查阅，避免硬编码：

```python
# 翅膀阶段基线
WING_STAGE_BASELINE = {1: 1.00, 2: 0.85, 3: 0.65, 4: 0.35, 5: 0.15}

# 亮度下限
MIN_BRIGHTNESS_ABSOLUTE = 0.05
MIN_BRIGHTNESS_STAGE_RATIO = 0.15

# 虚无主义
NIHILISM_THRESHOLD = 0.7

# 拥抱
HUG_LIMIT_DEFAULT = 3
HUG_BOND_DEPTH_GAIN = 0.02

# 询问天使
ASK_ANGEL_BOND_DEPTH_GAIN = 0.01
ASK_ANGEL_COOLDOWN = 30.0  # 秒

# Ch13 身份选择
CH13_IDENTITY_CHOICE_BOND_GAIN = 0.15

# 觉醒结局
AWAKENING_BOND_DEPTH_THRESHOLD = 0.6

# 逃避代理
ESCAPE_PROXY_THRESHOLD = 3
ESCAPE_PROXY_PROGRESS = 0.5

# 直面标签进度值
CONFRONTATION_PROGRESS = {"ENGAGE": 1.0, "ESCAPE": 0.3, "NEUTRAL": 0.0}

# 代价乘数
PHASE_MULTIPLIERS = {"phase_1": 0.0, "phase_2a": 1.0, "phase_2b": 1.5, "phase_3": 2.5}
INTENSITY_MULTIPLIERS = {"low": 0.5, "medium": 1.0, "high": 2.0}
```

---

## 6. 禁止操作清单

以下操作在任何情况下都不允许：

| # | 禁止操作 | 理由 |
|---|---|---|
| P1 | 在叙事脚本中直接修改变量（`$ angel.bond_depth = 0.5`） | 违反层级分离和所有权 |
| P2 | 在界面层中直接修改变量 | 界面层不持有状态 |
| P3 | 在 JSON 中写入 Python 代码 | JSON 是纯数据 |
| P4 | 跨系统直接引用内部属性（`choice_system.sephirot_system.progress`） | 必须通过公开接口 |
| P5 | 在非所有者模块中直接修改共享变量 | 违反单一所有权 |
| P6 | 使用单变量 `wing_brightness` | 已改为双变量模型 |
| P7 | 使用固定下限 0.05 替代动态下限 | 动态下限保护叙事弧线 |
| P8 | 跳过 `validate_data.py` 校验提交 JSON | 数据一致性无保障 |
| P9 | 在存档变量中存储不可序列化对象 | 存档/读档会失败 |
| P10 | 创建反向依赖（如 C2 → C3） | 违反依赖方向 |

---

*本控制清单是开发期间的活文档，随架构演进更新。任何规则变更需经技术主程批准。*
