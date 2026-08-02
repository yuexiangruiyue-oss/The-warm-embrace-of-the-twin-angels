# 主架构文档 — 《双生天使的拥抱》

| 字段 | 值 |
|---|---|
| 文档版本 | 1.0 |
| 作者 | 程基岩（Cheng Jiyan）· 技术主程 |
| 状态 | Phase 3 初版 |
| 引擎 | Ren'Py 8.x（Python 3） |
| 目标平台 | Windows / macOS / Linux（Steam） |
| 关联文档 | `design/gdd/*-gdd.md`、`design/concept/game-concept.md`、`design/art/art-bible.md`、`docs/architecture/adr/ADR-001~004` |

---

## 1. 项目概述

《双生天使的拥抱》是一款以**存在性保护**为核心机制的叙事驱动视觉小说。玩家与一位守护天使同行，穿越 16 个 Sephirot（质点）章节，在情感暗流的冲击下保护自己的存在感，最终走向融合、守护或觉醒三种结局。

### 1.1 核心技术需求

| 需求 ID | 来源 | 描述 |
|---|---|---|
| TR-01 | 概念文档 | 16 章 × 5 拍叙事节奏，数据驱动可维护 |
| TR-02 | C2 GDD | 天使始终在场，5 种情绪状态，翅膀 5 阶段演化 |
| TR-03 | C3 GDD | 情感共鸣选择，无正确答案，纹理标签驱动叙事跳转 |
| TR-04 | C4 GDD | Sephirot 双八度进程，直面/逃避/中性标签，时间停滞机制 |
| TR-05 | C5 GDD | 8 种暗流 × 3 强度，天使介入，翅膀亮度代价 |
| TR-06 | 概念文档 | 3 种结局，bond_depth ≥ 0.6 解锁觉醒结局 |
| TR-07 | 美术圣经 | 1920×1080，无障碍可达性等级：全面 |
| TR-08 | 系统分解 | MVP 批次：C1+C2+C3+C5+C4+C6+N1 |

### 1.2 设计支柱对架构的约束

| 支柱 | 架构约束 |
|---|---|
| 天使永不离开 | 天使系统（C2）必须全局常驻，任何场景均可调用 |
| 痛苦可以转化 | 存在保护系统（C5）的代价是可逆的（叙事重置点 Ch16） |
| 从解离到整合 | 状态管理需跟踪 dissociation→integration 的连续变化 |

---

## 2. 引擎架构

### 2.1 引擎选择

详见 `ADR-001-engine-selection.md`。结论：**选择 Ren'Py 8.x**，理由为视觉小说原生支持、Python 扩展性、Steam 集成成熟、社区资源丰富。

### 2.2 Ren'Py 项目结构

```
twin-angels/
├── game/                         # Ren'Py 游戏根目录
│   ├── script.rpy                 # 入口：定义 start label，路由到第一章
│   ├── scripts/                   # 叙事脚本（按章节组织）
│   │   ├── ch01_malkuth.rpy       # 第1章：王国
│   │   ├── ch02_yesod.rpy         # 第2章：基础
│   │   ├── ...
│   │   └── ch16_kether.rpy        # 第16章：王冠
│   ├── systems/                   # 系统层（Python 定义）
│   │   ├── __init__.py
│   │   ├── angel_system.py        # C2 天使陪伴系统
│   │   ├── choice_system.py       # C3 选择系统
│   │   ├── sephirot_system.py     # C4 Sephirot 进程系统
│   │   ├── protection_system.py   # C5 存在保护系统
│   │   ├── narrative_engine.py    # C1 叙事引擎
│   │   └── save_manager.py        # C6 存档与设置
│   ├── data/                      # 数据驱动 JSON
│   │   ├── sephirot/              # 16 章节叙事数据
│   │   │   ├── ch01_malkuth.json
│   │   │   ├── ...
│   │   │   └── ch16_kether.json
│   │   ├── angel/                 # 天使配置
│   │   │   ├── dialogue_pools.json
│   │   │   ├── response_profiles.json
│   │   │   └── wing_config.json
│   │   ├── choices/               # 选择节点数据
│   │   │   └── choice_nodes.json
│   │   ├── protection/            # 存在保护配置
│   │   │   ├── undertow_types.json
│   │   │   └── cost_table.json
│   │   └── endings/               # 结局条件
│   │       └── ending_conditions.json
│   ├── gui/                       # Screen 定义
│   │   ├── angel_overlay.rpy      # 天使覆盖层（常驻 UI）
│   │   ├── choice_screen.rpy      # 选择界面
│   │   ├── protection_screen.rpy  # 存在保护反馈
│   │   ├── sephirot_map.rpy       # Sephirot 进程地图
│   │   └── settings_screen.rpy    # 设置界面
│   ├── images/                    # 美术资产
│   │   ├── characters/
│   │   ├── backgrounds/
│   │   ├── ui/
│   │   └── effects/
│   ├── audio/                     # 音频资产
│   ├── screens.rpy                # 主 Screen 定义（main_menu, game_menu 等）
│   ├── gui.rpy                    # GUI 配置（颜色、字体、布局）
│   ├── options.rpy                # 引擎配置（版本、名称、Steam）
│   └── definitions.rpy            # 全局定义（角色、变量、常量）
├── docs/                          # 文档
├── tests/                         # 测试
└── tools/                         # 工具脚本（数据校验、导出等）
```

### 2.3 脚本组织原则

| 层 | 职责 | 文件 | 规则 |
|---|---|---|---|
| **叙事层** | 讲故事、场景描写、对话 | `scripts/ch*.rpy` | 仅含 `label`、`scene`、`show`、`say`；不直接修改系统状态 |
| **系统层** | 系统逻辑、状态管理 | `systems/*.py` | 纯 Python 类，通过 Ren'Py 的 `python` 块调用；不含叙事文本 |
| **数据层** | 叙事内容、配置 | `data/**/*.json` | 数据驱动，脚本层读取数据层呈现内容 |
| **界面层** | Screen 定义 | `gui/*.rpy` | 仅负责展示，不持有游戏状态；状态从系统层读取 |

**关键原则**：叙事脚本调用系统层接口，系统层读写数据层配置，界面层从系统层读取状态。禁止叙事脚本直接操作数据层 JSON（必须通过系统层接口）。

### 2.4 Screen / Language 层划分

```
┌─────────────────────────────────────────────────────┐
│                    Screen 层（gui/）                  │
│  angel_overlay · choice_screen · protection_screen   │
│  sephirot_map · settings_screen                      │
│  ──────────────────────────────────────────────────  │
│  规则：只读系统状态，不修改；用户输入→系统层接口        │
├─────────────────────────────────────────────────────┤
│                   叙事层（scripts/）                   │
│  ch01~ch16 · label · scene · show · say              │
│  ──────────────────────────────────────────────────  │
│  规则：调用系统层接口推进游戏状态                       │
├─────────────────────────────────────────────────────┤
│                   系统层（systems/）                   │
│  AngelSystem · ChoiceSystem · SephirotSystem          │
│  ProtectionSystem · NarrativeEngine · SaveManager     │
│  ──────────────────────────────────────────────────  │
│  规则：纯逻辑，不含叙事文本；读写数据层                 │
├─────────────────────────────────────────────────────┤
│                   数据层（data/）                      │
│  sephirot/*.json · angel/*.json · choices/*.json     │
│  protection/*.json · endings/*.json                   │
│  ──────────────────────────────────────────────────  │
│  规则：纯数据，无逻辑；启动时加载到内存                  │
└─────────────────────────────────────────────────────┘
```

---

## 3. 系统架构

### 3.1 系统分层

基于 `design/gdd/system-decomposition.md`，将系统分为三层：

| 层 | 系统 | 职责 | 优先级 |
|---|---|---|---|
| **基础层** | C1 叙事引擎 | 叙事节点管理、场景切换、对话呈现 | P0 |
| | C6 存档与设置 | 存档/读档、设置持久化、无障碍配置 | P0 |
| **核心层** | C2 天使陪伴 | 天使情绪状态、对话池、翅膀阶段、拥抱机制 | P0 |
| | C3 选择系统 | 选择呈现、纹理标签处理、bond_depth 计算 | P0 |
| | C5 存在保护 | 暗流触发、天使介入、翅膀亮度代价 | P0 |
| **玩法层** | C4 Sephirot 进程 | 质点完成度、直面/逃避标签、时间停滞 | P0 |
| **叙事层** | N1 五拍节奏 | ENCOUNTER→STRUGGLE→COMFORT→CHOICE→TRANSFORM | P1 |

### 3.2 系统交互架构图

```
                        ┌──────────────────┐
                        │     C1 叙事引擎    │
                        │  NarrativeEngine  │
                        └────────┬─────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
              ┌─────────┐ ┌───────────┐ ┌───────────┐
              │ C3 选择  │ │ C5 存在保护 │ │ C2 天使    │
              │ Choice  │ │ Protection │ │  Angel    │
              │ System  │ │  System    │ │  System   │
              └────┬────┘ └─────┬─────┘ └─────┬─────┘
                   │            │             │
                   │   ┌────────┘             │
                   │   │                      │
                   ▼   ▼                      │
              ┌───────────┐                   │
              │ C4 Sephirot│◄─────bond_depth──┘
              │ Progress  │
              │  System   │
              └─────┬─────┘
                    │
                    ▼
              ┌───────────┐
              │  C6 存档   │
              │ SaveMgr   │
              └───────────┘
```

### 3.3 核心数据流

**选择触发流（主循环）：**

```
C1 到达选择节点
  → C1 调用 C3.present_choices(node_id)
    → C3 从数据层加载选项
    → C3 调用 C2.filter_choices_by_angel_state() （天使状态过滤）
    → 玩家选择选项
  → C3 调用 C3.process_selection(option)
    → C3 更新 bond_depth（relation choices）
    → C3 更新 angel_response_profile
    → 若 option.confrontation_tag 存在:
        C3 调用 C4.process_confrontation(sephirot_id, tag)
    → 若 option.existence_protection:
        C3 触发 C5.trigger_undertow(type, intensity)
    → C3 调用 C2.update_angel_response(option.angel_response_delta)
  → C1 调用 C1.narrative_jump(option.narrative_jump)
```

**暗流触发流（C5 主动）：**

```
C1 叙事到达暗流触发点
  → C1 调用 C5.trigger_undertow(type, intensity)
    → C5 计算翅膀亮度代价
    → C5 调用 C5.apply_wing_cost(cost)
      → 更新 wing_brightness_permanent
    → C5 调用 C2.angel_intervene(type, intensity)
      → C2 更新 angel_emotional_state
      → C2 从对话池选择介入台词
      → C2 更新 angel_intervention_count
    → C5 检查 nihilism_risk
      → 若 risk >= NIHILISM_THRESHOLD: 触发虚无危机事件
  → C1 呈现天使介入对话
```

**Sephirot 完成流（C4 内部）：**

```
C4.process_confrontation(sephirot_id, tag)
  → 根据 tag 计算 progress:
      ENGAGE → progress = 1.0
      ESCAPE → escape_count++, 若 escape_count == 3 → angel_proxy → progress = 0.5
      NEUTRAL → progress = 0.0, C2.angel_advise() 提示重选
  → C4.add_sephirot_progress(sephirot_id, progress)
  → C4.check_completion(sephirot_id)
    → 若完成: 解锁下一 Sephirot
    → C2.update_wing_stage(new_chapter) （更新翅膀阶段）
```

### 3.4 核心接口定义

```python
# === C1 叙事引擎 ===
class NarrativeEngine:
    def get_current_node(self) -> str:
        """返回当前叙事节点 ID"""

    def narrative_jump(self, node_id: str) -> None:
        """跳转到指定叙事节点"""

    def get_current_sephirot(self) -> int:
        """返回当前 Sephirot 章节（1-16）"""

# === C2 天使陪伴系统 ===
class AngelSystem:
    def angel_intervene(self, undertow_type: str, intensity: int) -> str:
        """C5 调用：天使介入，返回介入对话 ID"""

    def angel_advise(self, choice_node_id: str) -> str:
        """C3/C4 调用：天使建议，返回建议对话 ID"""

    def update_angel_response(self, delta: dict) -> None:
        """C3 调用：更新天使响应档案（warmth/depth/protectiveness/vulnerability）"""

    def update_emotional_state(self, event: str) -> None:
        """内部/外部调用：更新天使情绪状态"""

    def get_bond_depth(self) -> float:
        """C4/N5 调用：获取羁绊深度"""

    def add_bond_depth(self, amount: float, source: str) -> None:
        """C3/C4 调用：增加羁绊深度"""

    def get_wing_brightness_displayed(self) -> float:
        """C1/界面层调用：获取显示用翅膀亮度"""

    def update_wing_stage(self, chapter: int) -> None:
        """C4 调用：章节切换时更新翅膀阶段"""

    def attempt_hug(self) -> bool:
        """玩家调用：尝试拥抱天使"""

# === C3 选择系统 ===
class ChoiceSystem:
    def present_choices(self, node_id: str) -> list:
        """C1 调用：呈现选择，返回过滤后的选项列表"""

    def process_selection(self, option_id: str) -> dict:
        """内部调用：处理玩家选择，返回结果（narrative_jump, effects）"""

    def filter_choices_by_angel_state(self, options: list) -> list:
        """内部调用：根据天使状态过滤选项"""

# === C4 Sephirot 进程系统 ===
class SephirotSystem:
    def process_confrontation(self, sephirot_id: str, tag: str) -> float:
        """C3 调用：处理直面标签，返回本次 progress"""

    def add_sephirot_progress(self, sephirot_id: str, amount: float) -> None:
        """内部调用：增加质点完成度"""

    def check_completion(self, sephirot_id: str) -> bool:
        """内部调用：检查质点是否完成"""

    def get_current_sephirot(self) -> str:
        """C1 调用：获取当前质点 ID"""

    def get_progress(self, sephirot_id: str) -> float:
        """界面层调用：获取质点完成度"""

# === C5 存在保护系统 ===
class ProtectionSystem:
    def trigger_undertow(self, undertow_type: str, intensity: int) -> dict:
        """C1 调用：触发暗流，返回效果描述"""

    def apply_wing_cost(self, cost: float) -> None:
        """内部调用：扣除翅膀亮度"""

    def get_wing_brightness_permanent(self) -> float:
        """C2/界面层调用：获取永久翅膀亮度"""

    def get_wing_brightness_temporary(self) -> float:
        """界面层调用：获取临时暗淡值"""

    def recover_temporary_dim(self) -> None:
        """C1 调用：场景结束时恢复临时暗淡"""

    def check_nihilism_risk(self) -> float:
        """内部/C1 调用：检查虚无主义风险"""

    def get_intervention_count(self) -> int:
        """C2 调用：获取当前质点天使介入次数"""

# === C6 存档与设置 ===
class SaveManager:
    def save_game(self, slot: int) -> bool:
        """系统调用：保存游戏"""

    def load_game(self, slot: int) -> bool:
        """系统调用：读取游戏"""

    def get_setting(self, key: str) -> any:
        """任意系统调用：获取设置项"""

    def set_setting(self, key: str, value: any) -> None:
        """任意系统调用：设置设置项"""
```

---

## 4. 状态管理

### 4.1 变量分类

Ren'Py 提供两种持久化机制，本项目按以下规则使用：

| 类型 | Ren'Py 机制 | 用途 | 序列化 |
|---|---|---|---|
| **存档变量** | `default` 声明 | 游戏运行时状态，随存档保存 | 随存档 |
| **持久变量** | `define` + `persistent` | 跨周目数据（成就、解锁、统计） | 独立于存档 |
| **常量** | `define` | 不可变配置值（阈值、基线表） | 不序列化 |

### 4.2 存档变量定义（`definitions.rpy`）

```renpy
# ========== 核心状态变量 ==========

# --- C2 天使陪伴系统 ---
default angel = AngelState(
    presence_mode="display",
    emotional_state="calm",
    wing_stage=1,
    wing_brightness_permanent=1.0,   # CONCERN 1 解决：双层模型
    wing_brightness_temporary=0.0,    # CONCERN 1 解决：临时暗淡
    click_cooldown_until=0.0,
    hug_count_this_sephirot=0,
    hug_limit=3,
    trust_level=0.5,
    bond_depth=0.0,
    memories=[],
    active_dialogue_pool="default",
    angel_response_profile={
        "warmth": 0.5,
        "depth": 0.3,
        "protectiveness": 0.7,
        "vulnerability": 0.2
    }
)

# --- C3 选择系统 ---
default choice_history = []           # 选择历史记录
default nihilism_risk = 0.0           # 虚无主义风险值

# --- C4 Sephirot 进程系统 ---
default sephirot_progress = {}        # {sephirot_id: progress_value}
default current_sephirot = "ch01_malkuth"
default escape_counts = {}            # {sephirot_id: escape_count}
default sephirot_completed = []       # 已完成的质点列表
default time_stuck_active = False     # 时间停滞是否激活

# --- C5 存在保护系统 ---
default angel_intervention_count = 0  # 当前质点天使介入次数
default undertow_history = []         # 暗流触发历史
default wing_cost_accumulated = 0.0   # 当前阶段累计翅膀代价

# --- C1 叙事引擎 ---
default current_chapter = 1
default current_beat = "ENCOUNTER"
defalut narrative_flags = {}          # 叙事标志位
default visited_nodes = []            # 已访问叙事节点

# --- 全局 ---
default play_time = 0.0
default current_save_slot = None
```

### 4.3 持久变量定义

```renpy
# ========== 跨周目持久数据 ==========

# 成就
default persistent.achievements = {}
default persistent.endings_unlocked = []      # ["fusion", "guardian", "awakening"]

# 解锁
default persistent.sephirot_art_unlocked = [] # 质点立绘画廊解锁
default persistent.cg_unlocked = []           # CG 解锁
default persistent.music_unlocked = []        # 音乐室解锁

# 统计
default persistent.total_play_time = 0.0
default persistent.total_hugs = 0
default persistent.total_choices = 0
default persistent.max_bond_depth = 0.0
default persistent.escape_total = 0

# 设置
default persistent.text_speed = 30
default persistent.auto_forward = 0.0
default persistent.self_voicing = False
default persistent.accessibility_level = "full"  # none/basic/enhanced/full
default persistent.wing_brightness_visual = True  # 翅膀亮度视觉化
default persistent.undertow_visual = True         # 暗流视觉效果
default persistent.text_size = "normal"           # small/normal/large/extra_large

# 首次标记
default persistent.first_launch = True
default persistent.seen_prologue = False
```

### 4.4 共享变量所有权矩阵

> **这是 Phase 2 一致性检查的关键交付物。** 以下矩阵明确每个共享变量的单一所有者和允许的读写权限。

| 变量 | 所有者（写入权威） | 读取者 | 写入者（含委托） | 生命周期 | 重置时机 |
|---|---|---|---|---|---|
| `angel.emotional_state` | **C2 AngelSystem** | C1（呈现）, C3（过滤选项）, C5（介入触发条件） | C2（事件驱动）, C5（通过 `angel_intervene()` 委托 C2 修改） | 每场景 | 场景切换时由 C2 内部决定是否重置 |
| `angel_intervention_count` | **C5 ProtectionSystem** | C2（介入频率控制）, C4（完成度参考） | C5（每次介入 +1） | 每质点 | 新质点开始时重置为 0 |
| `angel.wing_brightness_permanent` | **C5 ProtectionSystem** | C2（显示）, C1（呈现）, 界面层 | C5（`apply_wing_cost()` 扣减）, C2（`update_wing_stage()` 阶段切换时重置到基线） | 每翅膀阶段 | 翅膀阶段提升时重置为新阶段基线 |
| `angel.wing_brightness_temporary` | **C5 ProtectionSystem** | C2（显示）, 界面层 | C5（临时暗流效果增加）, C5（`recover_temporary_dim()` 场景结束恢复） | 每场景 | 场景结束时恢复为 0 |
| `angel.bond_depth` | **C3 ChoiceSystem** | C2（天使响应）, C4（结局条件）, N5（结局判定） | C3（relation choices）, C2（拥抱 +0.02/次, "询问天使" +0.01/次）, C4（Ch13 身份选择 +0.15） | 全游戏 | 不重置（跨章节累积） |
| `nihilism_risk` | **C5 ProtectionSystem** | C1（虚无危机事件）, 界面层 | C5（暗流累积计算） | 全游戏 | Ch16 叙事重置点归零 |
| `sephirot_progress[id]` | **C4 SephirotSystem** | C1（解锁判断）, 界面层 | C4（`add_sephirot_progress()`） | 每质点 | 完成后锁定 |
| `escape_counts[id]` | **C4 SephirotSystem** | C2（天使代理判断）, 界面层 | C4（每次 ESCAPE +1） | 每质点 | 完成后锁定 |

**所有权规则：**
1. 每个共享变量有且仅有一个所有者，其他系统只能通过所有者暴露的接口读写。
2. 所有者接口必须包含 getter；setter 仅在所有者认为合理时暴露。
3. 违反所有权规则的直接变量修改在代码审查中标记为 **BLOCKER**。

### 4.5 变量生命周期图

```
游戏开始
  │
  ├── C1: current_chapter=1, current_beat="ENCOUNTER"
  ├── C2: angel 初始化（wing_stage=1, brightness=1.0, bond_depth=0.0）
  ├── C3: choice_history=[]
  ├── C4: sephirot_progress={}, current_sephirot="ch01_malkuth"
  ├── C5: angel_intervention_count=0, nihilism_risk=0.0
  │
  ▼
章节内循环（每场景）
  │
  ├── C5: wing_brightness_temporary 场景结束→恢复0
  ├── C2: angel_emotional_state 场景结束→根据策略重置
  ├── C5: angel_intervention_count 章节内累积
  │
  ▼
质点完成（C4.check_completion → True）
  │
  ├── C4: sephirot_progress[id] 锁定
  ├── C4: escape_counts[id] 锁定
  ├── C2: update_wing_stage(new_chapter)
  │     → wing_brightness_permanent 重置为新阶段基线
  ├── C5: angel_intervention_count → 0
  ├── C5: wing_cost_accumulated → 0.0
  │
  ▼
Ch16 叙事重置点
  │
  ├── C2: wing_brightness_permanent → 1.0（叙事重置）
  ├── C5: nihilism_risk → 0.0
  │
  ▼
结局判定（N5）
  │
  ├── bond_depth >= 0.6 → 觉醒结局
  ├── bond_depth < 0.6 + 选择摧毁天使 → 融合结局
  └── bond_depth < 0.6 + 选择拒绝 → 守护结局
```

---

## 5. 数据驱动设计

### 5.1 设计原则

详见 `ADR-002-data-driven-narrative.md`。结论：**采用 JSON 数据驱动**，叙事内容与代码逻辑分离，支持非程序员（策划/文案）独立编辑内容。

### 5.2 Sephirot 章节数据结构（`data/sephirot/chXX_name.json`）

```json
{
  "sephirot_id": "ch04_chesed",
  "sephirot_name": "仁慈",
  "sephirot_name_en": "Chesed",
  "chapter": 4,
  "octave": "human",
  "octave_direction": "ascending",
  "theme": "给予与接受",
  "undertow_focus": "SHAME_LOOP",
  "wing_stage": 2,
  "beats": [
    {
      "beat_id": "ch04_b01_encounter",
      "beat_type": "ENCOUNTER",
      "scene_script": "ch04_chesed",
      "scene_label": "ch04_b01",
      "undertow_trigger": null,
      "choices": null,
      "next_node": "ch04_b02"
    },
    {
      "beat_id": "ch04_b02_struggle",
      "beat_type": "STRUGGLE",
      "scene_script": "ch04_chesed",
      "scene_label": "ch04_b02",
      "undertow_trigger": {
        "type": "SHAME_LOOP",
        "intensity": 5
      },
      "choices": null,
      "next_node": "ch04_b03"
    },
    {
      "beat_id": "ch04_b03_comfort",
      "beat_type": "COMFORT",
      "scene_script": "ch04_chesed",
      "scene_label": "ch04_b03",
      "undertow_trigger": null,
      "choices": null,
      "next_node": "ch04_b04"
    },
    {
      "beat_id": "ch04_b04_choice",
      "beat_type": "CHOICE",
      "scene_script": "ch04_chesed",
      "scene_label": "ch04_b04",
      "undertow_trigger": null,
      "choices": "ch04_c01",
      "next_node": null
    },
    {
      "beat_id": "ch04_b05_transform",
      "beat_type": "TRANSFORM",
      "scene_script": "ch04_chesed",
      "scene_label": "ch04_b05",
      "undertow_trigger": null,
      "choices": null,
      "next_node": "ch05_b01"
    }
  ]
}
```

### 5.3 统一选项数据结构（CONCERN 2 解决）

> **CONCERN 2 解决方案**：在 C3 选择系统的选项数据结构中新增 `confrontation_tag` 字段，与 C4 Sephirot 进程系统对齐。

```json
{
  "choice_node_id": "ch04_c01",
  "sephirot_id": "ch04_chesed",
  "beat_id": "ch04_b04_choice",
  "choice_type": "confrontation",
  "prompt": "羞耻的声音说你不配被爱。你——",
  "options": [
    {
      "id": "ch04_c01_o01",
      "text": "'我不是错的。我值得被爱。'",
      "texture_tag": "brave_affirm",
      "confrontation_tag": "ENGAGE",
      "progress_value": 1.0,
      "emotional_weight": 0.8,
      "angel_reaction": "aching",
      "angel_response_delta": {
        "warmth": 0.05,
        "depth": 0.08,
        "vulnerability": 0.03
      },
      "bond_depth_delta": 0.03,
      "memory_entry": {
        "type": "choice",
        "sephirot": "ch04_chesed",
        "summary": "在羞耻中选择了肯定自我",
        "emotional_tag": "courage"
      },
      "existence_protection": false,
      "narrative_jump": "ch04_b05"
    },
    {
      "id": "ch04_c01_o02",
      "text": "'……也许他们说得对。'",
      "texture_tag": "internalize_shame",
      "confrontation_tag": "ESCAPE",
      "progress_value": 0.3,
      "emotional_weight": 0.6,
      "angel_reaction": "grieved",
      "angel_response_delta": {
        "warmth": 0.02,
        "protectiveness": 0.05
      },
      "bond_depth_delta": 0.0,
      "memory_entry": {
        "type": "choice",
        "sephirot": "ch04_chesed",
        "summary": "在羞耻中选择了内化",
        "emotional_tag": "shame"
      },
      "existence_protection": true,
      "existence_protection_trigger": {
        "type": "SHAME_LOOP",
        "intensity": 3
      },
      "narrative_jump": "ch04_b05_escape"
    },
    {
      "id": "ch04_c01_o03",
      "text": "（沉默，看向天使）",
      "texture_tag": "seek_angel",
      "confrontation_tag": "NEUTRAL",
      "progress_value": 0.0,
      "emotional_weight": 0.4,
      "angel_reaction": "gentle_prompt",
      "angel_response_delta": {
        "warmth": 0.03,
        "depth": 0.02
      },
      "bond_depth_delta": 0.01,
      "memory_entry": {
        "type": "choice",
        "sephirot": "ch04_chesed",
        "summary": "在羞耻中寻求天使的引导",
        "emotional_tag": "seeking"
      },
      "existence_protection": false,
      "triggers_angel_advise": true,
      "narrative_jump": "ch04_b04_retry"
    }
  ]
}
```

**字段说明：**

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | string | 是 | 选项唯一 ID，格式 `chXX_cYY_oZZ` |
| `text` | string | 是 | 选项显示文本 |
| `texture_tag` | string | 是 | 纹理标签，驱动叙事跳转和记忆纹理 |
| `confrontation_tag` | enum\|null | 否 | `ENGAGE`/`ESCAPE`/`NEUTRAL`，仅直面选择填写；relation/attitude 选择为 null |
| `progress_value` | float | 是 | Sephirot 完成度贡献值（0.0-1.0） |
| `emotional_weight` | float | 是 | 情感权重（0.0-1.0），影响暗流强度计算 |
| `angel_reaction` | string | 是 | 天使反应类型（aching/grieved/gentle_prompt 等） |
| `angel_response_delta` | object | 是 | 天使响应档案变化（warmth/depth/protectiveness/vulnerability） |
| `bond_depth_delta` | float | 是 | 羁绊深度变化值 |
| `memory_entry` | object | 是 | 记忆条目，存入天使记忆库 |
| `existence_protection` | bool | 是 | 是否触发存在保护机制 |
| `existence_protection_trigger` | object\|null | 否 | 存在保护触发配置（type + intensity） |
| `triggers_angel_advise` | bool | 否 | 是否触发天使建议（NEUTRAL 标签专用） |
| `narrative_jump` | string | 是 | 叙事跳转目标节点 |

**`confrontation_tag` 与 `progress_value` 映射关系：**

| confrontation_tag | progress_value | 说明 |
|---|---|---|
| `ENGAGE` | 1.0 | 直面暗流，100% 完成度贡献 |
| `ESCAPE` | 0.3 | 逃避暗流，30% 完成度贡献；第 3 次逃避触发天使代理 → 50% 完成度 |
| `NEUTRAL` | 0.0 | 中性选择，无完成度贡献；天使建议重新选择 |
| `null`（非直面选择） | 由 `texture_tag` 独立决定（1.0/0.7/0.3） | 关系/态度选择，不影响 Sephirot 完成度 |

**冗余设计说明**：`confrontation_tag` 和 `progress_value` 存在语义重叠（ENGAGE→1.0, ESCAPE→0.3），但保留两者是有意为之：
- `confrontation_tag` 供 C4 SephirotSystem 消费，驱动完成度逻辑和逃避计数。
- `progress_value` 供 C3 ChoiceSystem 消费，作为通用进度值。
- 当 `confrontation_tag` 为 null 时，`progress_value` 由 `texture_tag` 独立决定，两者解耦。
- 代码中通过校验规则确保两者一致性（见控制清单 §3.2）。

### 5.4 天使状态数据结构

```python
@dataclass
class AngelState:
    # --- 在场模式 ---
    presence_mode: str          # "display" | "interactive" | "crisis"

    # --- 情绪状态 ---
    emotional_state: str        # "calm" | "concerned" | "grieving" | "protective" | "radiant"

    # --- 翅膀系统（CONCERN 1 解决：双层模型） ---
    wing_stage: int             # 1-5，叙事阶段
    wing_brightness_permanent: float   # 永久亮度，由 C5 扣减，阶段切换时重置
    wing_brightness_temporary: float   # 临时暗淡，场景结束恢复

    # --- 交互 ---
    click_cooldown_until: float # 点击冷却时间戳
    hug_count_this_sephirot: int # 当前质点拥抱次数
    hug_limit: int              # 拥抱上限（默认 3）

    # --- 羁绊 ---
    trust_level: float          # 信任等级（0.0-1.0）
    bond_depth: float           # 羁绊深度（0.0-1.0），结局判定关键变量

    # --- 记忆 ---
    memories: list              # 记忆条目列表
    active_dialogue_pool: str   # 当前对话池 ID

    # --- 响应档案 ---
    angel_response_profile: dict # {warmth, depth, protectiveness, vulnerability}

    @property
    def wing_brightness_displayed(self) -> float:
        """计算显示用翅膀亮度（CONCERN 1 核心公式）"""
        return max(0.05, self.wing_brightness_permanent - self.wing_brightness_temporary)
```

### 5.5 存在保护配置（`data/protection/`）

**暗流类型定义（`undertow_types.json`）：**

```json
{
  "undertow_types": [
    {
      "id": "SHAME_LOOP",
      "name": "羞耻循环",
      "description": "反复回放'你不够好'的声音",
      "base_cost": 0.02,
      "angel_response_type": "warmth",
      "intensity_multipliers": {"low": 0.5, "medium": 1.0, "high": 2.0}
    },
    {
      "id": "POSS_DENY",
      "name": "可能性否认",
      "description": "否定一切好转的可能",
      "base_cost": 0.025,
      "angel_response_type": "depth",
      "intensity_multipliers": {"low": 0.5, "medium": 1.0, "high": 2.0}
    }
  ]
}
```

**代价表（`cost_table.json`）：**

```json
{
  "base_costs": {
    "SHAME_LOOP": 0.020,
    "POSS_DENY": 0.025,
    "PAIN_AMP": 0.030,
    "HOPE_ERASE": 0.025,
    "EXIST_DENY": 0.035,
    "NIHILISM": 0.040,
    "RAGE_INC": 0.025,
    "HARM_GUIDE": 0.045
  },
  "phase_multipliers": {
    "phase_1": 0.0,
    "phase_2a": 1.0,
    "phase_2b": 1.5,
    "phase_3": 2.5
  },
  "intensity_multipliers": {
    "low":    {"min": 1, "max": 3,  "multiplier": 0.5},
    "medium": {"min": 4, "max": 6,  "multiplier": 1.0},
    "high":   {"min": 7, "max": 10, "multiplier": 2.0}
  },
  "floors": {
    "min_brightness": 0.05,
    "nihilism_threshold": 0.7
  }
}
```

**代价计算公式：**

```
total_cost = BASE_COST × PHASE_MULTIPLIER × INTENSITY_MULTIPLIER
wing_brightness_permanent -= total_cost
wing_brightness_permanent = max(wing_stage_baseline[wing_stage] × 0.15, wing_brightness_permanent)
```

> **注意**：亮度下限不是固定的 0.05，而是 `wing_stage_baseline[wing_stage] × 0.15`。这确保高级阶段（阶段 5 基线 0.15）不会因代价扣减到接近 0，保留叙事需要的最低存在感。绝对下限 0.05 作为硬底线仍然生效。

### 5.6 结局条件（`data/endings/ending_conditions.json`）

```json
{
  "endings": [
    {
      "id": "fusion",
      "name": "融合",
      "condition": "bond_depth < 0.6 AND final_choice == 'destroy_angel'",
      "description": "摧毁天使，与暗流融合"
    },
    {
      "id": "guardian",
      "name": "守护",
      "condition": "bond_depth < 0.6 AND final_choice == 'refuse_destruction'",
      "description": "拒绝摧毁天使，守护到最后一刻"
    },
    {
      "id": "awakening",
      "name": "觉醒",
      "condition": "bond_depth >= 0.6 AND final_choice == 'understand_transformation'",
      "description": "理解转化的本质，与天使共同觉醒"
    }
  ]
}
```

---

## 6. 翅膀亮度统一模型（CONCERN 1 解决）

> **CONCERN 1**：天使陪伴 GDD（C2）使用阶段基线模型 `wing_brightness = wing_stage_baseline[wing_stage] - wing_temporary_dim`；存在保护 GDD（C5）使用连续扣减模型 `wing_brightness -= cost; max(0.05, wing_brightness)`。两者冲突。
>
> **解决方案**：双层模型 —— 永久层 + 临时层。详见 `ADR-004-wing-brightness-model.md`。

### 6.1 双层模型定义

```
wing_brightness_displayed = max(0.05, wing_brightness_permanent - wing_brightness_temporary)
```

| 层 | 变量 | 所有者 | 含义 | 重置时机 |
|---|---|---|---|---|
| **永久层** | `wing_brightness_permanent` | C5 ProtectionSystem | 存在保护代价的累积扣减。随阶段基线初始化，只减不增（Ch16 叙事重置除外） | 翅膀阶段提升时重置为新阶段基线 |
| **临时层** | `wing_brightness_temporary` | C5 ProtectionSystem | 场景内临时暗淡效果（如高强度暗流的即时视觉反馈）。非持久 | 场景结束时恢复为 0 |

### 6.2 阶段基线表

来源：C2 GDD `wing_stage_baseline`，与 C5 GDD 累积曲线对齐。

| 翅膀阶段 | 对应章节 | 阶段基线 | C5 累积曲线对应点 | 叙事含义 |
|---|---|---|---|---|
| 1 | Ch1-3 | 1.000 | Phase 1 起点 1.0 | 天使完整明亮 |
| 2 | Ch4-6 | 0.850 | Phase 2a 起点 0.850 | 轻微暗淡 |
| 3 | Ch7-9 | 0.650 | — | 明显暗淡 |
| 4 | Ch10-14 | 0.350 | Phase 2b 中点 0.509→0.159 | 严重暗淡 |
| 5 | Ch15-16 | 0.150 | Phase 3 0.159 | 几近熄灭 |
| 重置 | Ch16 | 1.000 | 叙事重置 1.0 | 觉醒/守护后恢复 |

**对齐验证**：C5 累积曲线的关键点（1.0 → 0.850 → 0.509 → 0.159 → 1.0）与阶段基线的关键点（1.0, 0.85, ~0.5, ~0.15, 1.0）吻合。差异在于：
- C5 曲线是连续扣减的结果，反映**阶段内的动态过程**。
- C2 基线是阶段起始值，反映**叙事阶段的结构性定位**。
- 双层模型统一两者：阶段基线作为 `wing_brightness_permanent` 的初始值，C5 的连续扣减在初始值上累减。

### 6.3 代价扣减流程

```python
def apply_wing_cost(self, cost: float, is_temporary: bool = False) -> None:
    """
    C5 ProtectionSystem 内部方法。
    is_temporary=False: 永久扣减（默认，暗流触发）
    is_temporary=True: 临时暗淡（高强度暗流即时效果）
    """
    if is_temporary:
        self.wing_brightness_temporary += cost
        self.wing_brightness_temporary = min(
            self.wing_brightness_permanent - 0.05,  # 临时暗淡不能超过永久值
            self.wing_brightness_temporary
        )
    else:
        floor = self.wing_stage_baseline[self.wing_stage] * 0.15
        self.wing_brightness_permanent -= cost
        self.wing_brightness_permanent = max(floor, self.wing_brightness_permanent)

def recover_temporary_dim(self) -> None:
    """C1 场景结束时调用"""
    self.wing_brightness_temporary = 0.0

def update_wing_stage(self, new_stage: int) -> None:
    """C2 章节切换时调用"""
    self.wing_stage = new_stage
    self.wing_brightness_permanent = self.wing_stage_baseline[new_stage]
    self.wing_brightness_temporary = 0.0
    self.wing_cost_accumulated = 0.0  # 重置累计代价
```

### 6.4 叙事重置点（Ch16）

在 Ch16 的特定叙事节点，`wing_brightness_permanent` 被重置为 1.0，象征天使在觉醒/守护后的恢复。这是双层模型中唯一允许 `wing_brightness_permanent` 增加的情况。

```python
def narrative_reset_wing_brightness(self) -> None:
    """Ch16 叙事重置点调用"""
    self.wing_brightness_permanent = 1.0
    self.wing_brightness_temporary = 0.0
    self.nihilism_risk = 0.0
```

---

## 7. 存档系统

### 7.1 Ren'Py 存档机制

Ren'Py 的存档系统自动序列化所有 `default` 声明的变量。本项目的系统状态均存储为 `default` 变量（见 §4.2），因此天然支持存档。

### 7.2 存档数据结构

Ren'Py 存档包含以下数据的快照：

```
存档槽数据
├── 引擎元数据
│   ├── timestamp
│   ├── screenshot
│   └── chapter_title
├── C1 叙事状态
│   ├── current_chapter
│   ├── current_beat
│   ├── narrative_flags
│   └── visited_nodes
├── C2 天使状态
│   ├── angel (AngelState 完整对象)
│   │   ├── presence_mode, emotional_state
│   │   ├── wing_stage, wing_brightness_permanent, wing_brightness_temporary
│   │   ├── trust_level, bond_depth
│   │   ├── memories
│   │   └── angel_response_profile
│   └── active_dialogue_pool
├── C3 选择状态
│   ├── choice_history
│   └── nihilism_risk
├── C4 Sephirot 状态
│   ├── sephirot_progress
│   ├── current_sephirot
│   ├── escape_counts
│   ├── sephirot_completed
│   └── time_stuck_active
├── C5 存在保护状态
│   ├── angel_intervention_count
│   ├── undertow_history
│   └── wing_cost_accumulated
└── 全局
    ├── play_time
    └── current_save_slot
```

### 7.3 存档兼容性策略

| 版本 | 策略 |
|---|---|
| 1.0.x（初始发布） | 基线版本，无兼容性处理 |
| 1.x.x（功能更新） | 新增字段提供默认值；`default` 声明自动处理 |
| 2.0.x（重大重构） | 存档迁移脚本：`migrate_save(old_data) -> new_data` |

**数据类序列化注意**：`AngelState` 使用 Python `@dataclass`，Ren'Py 的 pickle 序列化天然支持。但需注意：
- `memories` 列表中的字典不应包含不可序列化的对象（如函数引用）。
- `angel_response_profile` 仅含基础类型（float），安全。

### 7.4 自动存档触发点

| 触发点 | 时机 | 存档槽 |
|---|---|---|
| 质点完成 | C4 `check_completion` 返回 True 后 | 自动存档槽 1 |
| 章节开始 | 新章节第一个 label 进入时 | 自动存档槽 2 |
| 关键选择前 | C3 `present_choices` 调用前 | 自动存档槽 3 |
| 暗流触发前 | C5 `trigger_undertow` 调用前 | 自动存档槽 4 |

---

## 8. 性能考量

### 8.1 性能预算

| 指标 | 目标 | 测量方法 |
|---|---|---|
| 帧率 | 60 FPS（UI 动画），叙事文本无帧率要求 | Ren'Py profiler |
| 内存 | < 1.5 GB（含所有加载的美术资产） | 系统监视器 |
| 加载时间 | 章节切换 < 3 秒 | 计时器 |
| 存档大小 | < 5 MB（不含截图） | 文件大小 |

### 8.2 Sprite 切换优化

| 场景 | 优化策略 |
|---|---|
| 天使表情切换 | 预加载当前场景所需表情到内存；使用 Ren'Py `image` statement 组合 |
| 翅膀阶段过渡 | 阶段切换使用 dissolve transition（~500ms）；阶段内亮度变化使用动态着色（shader），不切换图片 |
| 背景切换 | 使用 `Ren'Py` 内置 `dissolve`/`fade`；大背景图使用 `image` 压缩 |
| Sephirot 角色 | 每章仅加载当前章节角色立绘；章节切换时释放上一章资源 |

**翅膀亮度着色方案**：
- 不为每个亮度值生成不同图片。
- 使用一张基础翅膀图 + Ren'Py `im.MatrixColor` 或自定义 shader 动态调整亮度。
- `wing_brightness_displayed` 值映射到着色参数（0.05→极暗, 1.0→正常）。

### 8.3 翅膀渐变动画

```renpy
# 翅膀亮度变化使用 transform 动态调整
transform wing_brightness_adjust(brightness):
    matrixcolor BrightnessMatrix(brightness * 0.5 + 0.5)
    # brightness 0.05 → matrix 0.525（极暗）
    # brightness 1.0  → matrix 1.0（正常）

# 翅膀显示（Screen 层）
screen angel_wing_display():
    add "angel_wing_base" at wing_brightness_adjust(angel.wing_brightness_displayed)
```

### 8.4 暗流视觉效果

| 暗流强度 | 视觉效果 | 性能策略 |
|---|---|---|
| 低（1-3） | 轻微屏幕边缘暗化 | CSS-like overlay，单层 |
| 中（4-6） | 屏幕震动 + 边缘暗化 + 天使光芒闪烁 | 预渲染 overlay + 简单 transform |
| 高（7-10） | 全屏扭曲 + 色彩偏移 + 天使翅膀剧烈暗淡 | 限制持续时间（< 3 秒）；使用 shader 而非多层叠加 |

### 8.5 数据加载策略

```python
# 启动时加载所有 JSON 数据到内存（总量预计 < 2MB）
init python:
    import json
    import os

    def load_all_data():
        """游戏启动时加载所有数据驱动 JSON"""
        g.data = {}
        g.data['sephirot'] = load_json_dir("data/sephirot/")
        g.data['angel'] = load_json_dir("data/angel/")
        g.data['choices'] = load_json_file("data/choices/choice_nodes.json")
        g.data['protection'] = {
            'undertow_types': load_json_file("data/protection/undertow_types.json"),
            'cost_table': load_json_file("data/protection/cost_table.json")
        }
        g.data['endings'] = load_json_file("data/endings/ending_conditions.json")
```

---

## 9. 安全考量

### 9.1 威胁模型

作为单机叙事游戏，安全威胁较低。主要关注：

| 威胁 | 严重性 | 缓解策略 |
|---|---|---|
| 存档篡改（跳过章节） | 低 | 存档包含 `sephirot_completed` 列表，结局判定检查完整性 |
| 存档损坏 | 中 | Ren'Py 自动备份；定期自动存档 |
| 成就作弊 | 极低 | 不投入反作弊资源（单机游戏） |
| 剧透数据挖掘 | 低 | 剧透内容不放在明文 JSON 中（加密结局条件或后端验证） |

### 9.2 存档完整性

```python
def validate_save(save_data) -> bool:
    """读档时验证存档完整性"""
    # 检查必要字段存在
    required = ['current_chapter', 'angel', 'sephirot_progress', 'bond_depth']
    for field in required:
        if field not in save_data:
            return False

    # 检查值范围合理性
    if not (0.0 <= save_data['angel']['bond_depth'] <= 1.0):
        return False
    if not (0.05 <= save_data['angel']['wing_brightness_permanent'] <= 1.0):
        return False

    # 检查 Sephirot 完成度一致性
    for sid, progress in save_data['sephirot_progress'].items():
        if not (0.0 <= progress <= 1.0):
            return False

    return True
```

---

## 10. 技术风险与知识缺口

### 10.1 技术风险

| 风险 | 概率 | 影响 | 缓解 |
|---|---|---|---|
| Ren'Py `im.MatrixColor` 翅膀着色性能不足 | 中 | 中 | 预备备选方案：GDExtension 自定义 shader 或多图切换 |
| 16 章 JSON 数据量过大导致维护困难 | 中 | 中 | 提供数据校验工具 `tools/validate_data.py`；每章独立文件 |
| Python `@dataclass` 序列化兼容性 | 低 | 高 | 测试存档/读档全流程；预备 fallback 为纯字典 |
| 暗流高频触发导致翅膀亮度过早触底 | 中 | 中 | 代价公式已设下限；Playtest 调参 |
| 时间停滞机制实现复杂度 | 中 | 中 | 早期原型验证；备选简化方案 |

### 10.2 知识缺口

| 缺口 | 描述 | 行动 |
|---|---|---|
| Ren'Py 8.x 具体版本差异 | 训练数据可能不覆盖最新 API 变化 | 开发开始前查阅 `docs/engine-reference/renpy/VERSION.md`（待创建） |
| Steam 集成细节 | Ren'Py Steam 集成的具体配置 | 参考社区文档；早期原型验证 |
| 无障碍 Screen Reader 支持 | Ren'Py self-voicing 的实际效果 | 需要在真实屏幕阅读器上测试 |

### 10.3 引擎参考文档需求

以下引擎参考文档需要在开发前创建（交由主理人安排）：

| 文档 | 内容 | 优先级 |
|---|---|---|
| `docs/engine-reference/renpy/VERSION.md` | 项目钉定的 Ren'Py 版本及关键 API | P0 |
| `docs/engine-reference/renpy/STEAM.md` | Steam 集成配置指南 | P1 |
| `docs/engine-reference/renpy/ACCESSIBILITY.md` | 无障碍功能实现指南 | P1 |

---

## 11. 美术-技术接口协调点

以下是需要与美术总监（林绘澄）协调的技术接口点：

| 协调点 | 技术需求 | 美术交付物 | 状态 |
|---|---|---|---|
| 翅膀亮度着色 | 1 张基础翅膀图（每阶段），通过 shader 动态调亮 | 5 阶段 × 1 张翅膀图（PNG，带 alpha） | 待协调 |
| 天使表情切换 | 每场景预加载表情集 | 6 种表情 × 角色立绘（calm/concerned/grieving/protective/radiant/aching） | 待协调 |
| 暗流视觉效果 | shader 参数（暗化/扭曲/偏色） | 暗流视觉参考图（3 强度等级） | 待协调 |
| UI 尺寸适配 | 1920×1080 基准 + 缩放策略 | UI 元素 PSD（分层） | 待协调 |
| 文字大小无障碍 | 4 级文字大小（small/normal/large/extra_large） | 各级文字渲染测试图 | 待协调 |
| CG 图鉴 | persistent 解锁机制 | CG 图片 + 缩略图 | 待协调 |

---

## 12. 开发批次建议

基于 `system-decomposition.md` 的优先级和架构依赖关系：

| 批次 | 内容 | 依赖 | 产出 |
|---|---|---|---|
| **Batch 0** | 项目骨架 + 数据层 + C1 叙事引擎 + C6 存档 | 无 | 可运行的叙事框架 |
| **Batch 1** | C2 天使陪伴 + C3 选择系统 + C5 存在保护 | Batch 0 | MVP 核心循环 |
| **Batch 2** | C4 Sephirot 进程 + N1 五拍节奏 | Batch 1 | 完整玩法循环 |
| **Batch 3** | Ch1-3 垂直切片内容 + 美术集成 | Batch 2 | 可玩垂直切片 |
| **Batch 4** | Ch4-16 全量内容 + 结局 + 无障碍 | Batch 3 | 完整游戏 |

---

## 附录 A：常量定义汇总

```python
# ========== 全局常量 ==========

# 翅膀阶段基线
WING_STAGE_BASELINE = {1: 1.00, 2: 0.85, 3: 0.65, 4: 0.35, 5: 0.15}

# 章节→翅膀阶段映射
CHAPTER_TO_WING_STAGE = {
    1: 1, 2: 1, 3: 1,           # Phase 1: 遗忘
    4: 2, 5: 2, 6: 2,           # Phase 2a: 试炼上半
    7: 3, 8: 3, 9: 3,           # Phase 2a: 试炼中段
    10: 4, 11: 4, 12: 4,        # Phase 2b: 试炼下半
    13: 4, 14: 4,               # Phase 2b: 身份
    15: 5, 16: 5                # Phase 3: 真相
}

# 亮度下限
MIN_BRIGHTNESS_ABSOLUTE = 0.05   # 绝对硬底线
MIN_BRIGHTNESS_STAGE_RATIO = 0.15  # 阶段基线的 15% 作为动态下限

# 虚无主义阈值
NIHILISM_THRESHOLD = 0.7

# 拥抱参数
HUG_LIMIT_DEFAULT = 3
HUG_BOND_DEPTH_GAIN = 0.02

# 询问天使参数
ASK_ANGEL_BOND_DEPTH_GAIN = 0.01
ASK_ANGEL_COOLDOWN = 30.0  # 秒

# Ch13 身份选择
CH13_IDENTITY_CHOICE_BOND_GAIN = 0.15

# 觉醒结局阈值
AWAKENING_BOND_DEPTH_THRESHOLD = 0.6

# 逃避代理阈值
ESCAPE_PROXY_THRESHOLD = 3  # 第3次逃避触发天使代理
ESCAPE_PROXY_PROGRESS = 0.5  # 天使代理完成度

# 直面标签进度值
CONFRONTATION_PROGRESS = {
    "ENGAGE": 1.0,
    "ESCAPE": 0.3,
    "NEUTRAL": 0.0
}
```

## 附录 B：Sephirot 双八度速查

| 章 | Sephirot | 中文名 | 八度 | 方向 | 翅膀阶段 | 暗流焦点 |
|---|---|---|---|---|---|---|
| 1 | Malkuth | 王国 | 人 | 升 | 1 | SHAME_LOOP |
| 2 | Yesod | 基础 | 人 | 升 | 1 | POSS_DENY |
| 3 | Hod | 荣耀 | 人 | 升 | 1 | PAIN_AMP |
| 4 | Netzach | 胜利 | 人 | 升 | 2 | SHAME_LOOP |
| 5 | Tiphareth | 美 | 人 | 升 | 2 | HOPE_ERASE |
| 6 | Chesed | 仁慈 | 人 | 升 | 2 | EXIST_DENY |
| 7 | Binah | 理解 | 人 | 升 | 3 | PAIN_AMP |
| 8 | Chokhmah | 智慧 | 人 | 升 | 3 | NIHILISM |
| 9 | Da'at | 知识 | 神 | 降 | 3 | EXIST_DENY |
| 10 | Kether-limit | 王冠限 | 神 | 降 | 4 | NIHILISM |
| 11 | RAGE | 愤怒质点 | 神 | 降 | 4 | RAGE_INC |
| 12 | HARM | 伤害质点 | 神 | 降 | 4 | HARM_GUIDE |
| 13 | IDENTITY | 身份质点 | 神 | 降 | 4 | SHAME_LOOP |
| 14 | TRUTH-1 | 真相·上 | 神 | 降 | 4 | POSS_DENY |
| 15 | TRUTH-2 | 真相·下 | 神 | 降 | 5 | EXIST_DENY |
| 16 | Kether | 王冠 | — | — | 5→1 | NIHILISM |

---

*文档结束。本文档与 `ADR-001~004`、`architecture-review.md`、`control-checklist.md` 共同构成完整的技术架构交付物。*
