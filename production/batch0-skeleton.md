# Batch 0 项目骨架定义

> **The Embrace of the Twin Angels** — Batch 0 Skeleton Specification
>
> 产出者：程基岩（engineering-lead）
>
> 日期：2026-08-02
>
> 依赖文档：`docs/architecture/main-architecture.md`（目录结构 §3、状态管理 §6）、`docs/architecture/adr/ADR-001~004.md`、`docs/architecture/control-checklist.md`、`production/epics/epic-breakdown.md`（Epic 0-2）

---

## 目录

1. [Batch 0 范围与目标](#1-batch-0-范围与目标)
2. [项目目录结构](#2-项目目录结构)
3. [初始文件清单](#3-初始文件清单)
4. [options.rpy 配置](#4-optionsrpy-配置)
5. [JSON 数据模板](#5-json-数据模板)
6. [核心系统骨架文件](#6-核心系统骨架文件)
7. [Ch1 骨架章节脚本](#7-ch1-骨架章节脚本)
8. [Git 初始化配置](#8-git-初始化配置)
9. [CI 流水线配置](#9-ci-流水线配置)
10. [Batch 0 Exit 检查清单](#10-batch-0-exit-检查清单)

---

## 1. Batch 0 范围与目标

### 1.1 范围

Batch 0 包含以下工作（对应 Epic 0-2）：

| Epic | 范围 | Story 数 |
|------|------|---------|
| Epic 0 | 项目骨架 + 基础设施 | 6 |
| Epic 1 | C6 存档系统 | 5 |
| Epic 2 | C1 叙事引擎 | 5 |
| **合计** | | **16** |

### 1.2 目标

**可运行最小原型**：Ch1 骨架章节可从开始到结束完整走通，存档/读档恢复正确。

具体可玩验证：
1. 启动游戏 → 标题画面 → 开始游戏
2. Ch1（王国/白花）五拍叙事完整走通
3. 暗流触发（EXIST_DENY 低强度）→ 天使介入台词 → 画面恢复
4. 选择呈现（ENGAGE / ESCAPE）→ 后果分发 → 质点完成
5. Ch1 结束 → 路由到 Ch2（骨架）
6. 存档/读档 → 所有状态正确恢复

### 1.3 不包含（推迟到 Batch 1+）

- C3 选择系统的完整后果分发器（Batch 0 仅骨架调用）
- C5 存在保护系统的完整暗流引擎（Batch 0 仅触发+介入骨架）
- C2 天使陪伴系统的完整状态机（Batch 0 仅基础状态）
- C4 质点进程系统的完成判定（Batch 0 仅解锁链骨架）
- UI/UX 完整界面（Batch 0 使用 Ren'Py 默认界面）
- 可访问性系统（Batch 2）
- 音频资产（Batch 0 无音频）
- 美术资产（Batch 0 使用占位图）

---

## 2. 项目目录结构

按 `main-architecture.md` §3.1 定义：

```
the-embrace-of-the-twin-angels/          # 项目根目录
├── game/                                # Ren'Py game 目录
│   ├── scripts/                         # 叙事层
│   │   ├── ch01_sephirot_01.rpy         # Ch1 叙事脚本
│   │   ├── ch02_sephirot_02.rpy         # Ch2 骨架
│   │   ├── ...                          # Ch3-16 骨架（空 label）
│   │   └── tests/                       # E2E 测试脚本
│   │       └── e2e_ch01_skeleton.rpy    # Ch1 走通测试
│   │
│   ├── scripts/                        # 系统层（init python）
│   │   └── systems/
│   │       ├── __init__.rpy             # 系统初始化入口
│   │       ├── constants.rpy            # 常量与枚举
│   │       ├── state.rpy                # default/persistent 变量声明
│   │       ├── data_loader.py            # JSON 加载器
│   │       ├── save_system.rpy           # C6 存档系统
│   │       ├── narrative_router.rpy     # C1 章节路由
│   │       ├── narrative_tags.rpy       # C1 叙事标签系统
│   │       ├── narrative_beat.rpy       # C1 五拍叙事框架
│   │       ├── wing_brightness.rpy      # 翅膀亮度双层模型
│   │       └── save_integrity.rpy       # 存档完整性校验
│   │
│   ├── data/                            # 数据层
│   │   ├── sephirot/                    # 16 质点数据
│   │   │   ├── _template.json          # 模板
│   │   │   └── sephirot_01.json         # Ch1 质点数据
│   │   ├── choices/                     # 选择节点数据
│   │   │   ├── ch01/
│   │   │   │   └── _template.json      # 模板
│   │   ├── angel/                       # 天使数据
│   │   │   ├── _template.json          # 模板
│   │   │   └── dialogue_pool.json      # 对话池骨架
│   │   ├── protection/                  # 存在保护数据
│   │   │   ├── _template.json          # 模板
│   │   │   └── undertow_definitions.json # 8 种暗流定义
│   │   └── endings/                     # 结局数据
│   │       └── _template.json          # 模板
│   │
│   ├── gui/                             # 界面层
│   │   ├── main_menu.rpy                # 主菜单（Ren'Py 默认+定制）
│   │   ├── save_load.rpy                # 存档/读档界面
│   │   ├── preferences.rpy              # 设置界面
│   │   └── choice_screen.rpy            # 选择界面
│   │
│   ├── images/                          # 图片资产
│   │   └── placeholder/                 # 占位图
│   │       ├── angel_placeholder.png   # 天使占位立绘
│   │       └── beloved_placeholder.png # 心爱的占位立绘
│   │
│   ├── audio/                           # 音频资产（Batch 0 为空）
│   │   ├── bgm/
│   │   └── se/
│   │
│   ├── options.rpy                      # Ren'Py 全局配置
│   ├── screens.rpy                      # Ren'Py Screen 定义
│   ├── gui.rpy                          # GUI 主题配置
│   └── script.rpy                       # Ren'Py 脚本入口
│
├── tools/                               # 工具脚本
│   ├── validate_data.py                 # JSON 数据校验
│   └── validate_consistency.py          # 一致性校验
│
├── tests/                               # 测试目录
│   ├── unit/                            # 单元测试
│   ├── integration/                     # 集成测试
│   ├── data/                            # 测试数据
│   ├── conftest.py                      # pytest fixtures
│   └── pytest.ini                       # pytest 配置
│
├── docs/                               # 文档目录
│   ├── architecture/                    # 架构文档
│   ├── engine-reference/               # 引擎参考
│   │   └── renpy/
│   │       └── VERSION.md              # Ren'Py 版本参考
│   └── gdd/                             # GDD
│
├── design/                             # 设计文档
│   └── gdd/
│
├── production/                          # 制作文档
│   ├── epics/
│   │   └── epic-breakdown.md           # Epic/Story 拆分
│   └── batch0-skeleton.md              # 本文档
│
├── .github/
│   └── workflows/
│       └── ci.yml                      # CI 流水线
│
├── .gitignore
├── .gitattributes
├── requirements-dev.txt                 # 开发依赖
├── CONTRIBUTING.md                      # 贡献指南
├── CLAUDE.md                           # 项目技术偏好
└── README.md                           # 项目说明
```

---

## 3. 初始文件清单

### 3.1 必须创建的文件（Batch 0 启动前）

| # | 文件路径 | 内容 | Story |
|---|---------|------|-------|
| 1 | `game/options.rpy` | Ren'Py 全局配置 | E0.1 |
| 2 | `game/script.rpy` | 脚本入口（`label start:`） | E0.1 |
| 3 | `game/gui.rpy` | GUI 主题配置 | E0.1 |
| 4 | `game/screens.rpy` | 基础 Screen 定义 | E0.1 |
| 5 | `game/scripts/systems/constants.rpy` | 常量与枚举 | E0.4 |
| 6 | `game/scripts/systems/state.rpy` | default/persistent 变量 | E0.5 |
| 7 | `game/scripts/systems/__init__.rpy` | 系统初始化入口 | E0.1 |
| 8 | `game/scripts/systems/data_loader.py` | JSON 加载器 | E0.3 |
| 9 | `game/scripts/systems/save_system.rpy` | C6 存档系统 | E1.1 |
| 10 | `game/scripts/systems/save_integrity.rpy` | 存档完整性校验 | E1.5 |
| 11 | `game/scripts/systems/narrative_router.rpy` | C1 章节路由 | E2.1 |
| 12 | `game/scripts/systems/narrative_tags.rpy` | C1 叙事标签 | E2.2 |
| 13 | `game/scripts/systems/narrative_beat.rpy` | C1 五拍框架 | E2.3 |
| 14 | `game/scripts/systems/wing_brightness.rpy` | 翅膀亮度双层模型 | E1.2 |
| 15 | `game/scripts/ch01_sephirot_01.rpy` | Ch1 叙事脚本 | E2.5 |
| 16 | `game/scripts/ch02_sephirot_02.rpy` ~ `ch16_sephirot_16.rpy` | Ch2-16 空骨架 | E2.4 |
| 17 | `game/data/sephirot/_template.json` | 质点数据模板 | E0.3 |
| 18 | `game/data/sephirot/sephirot_01.json` | Ch1 质点数据 | E2.5 |
| 19 | `game/data/choices/ch01/_template.json` | 选择节点模板 | E0.3 |
| 20 | `game/data/angel/_template.json` | 天使数据模板 | E0.3 |
| 21 | `game/data/angel/dialogue_pool.json` | 对话池骨架 | E0.3 |
| 22 | `game/data/protection/_template.json` | 暗流数据模板 | E0.3 |
| 23 | `game/data/protection/undertow_definitions.json` | 8 种暗流定义 | E0.3 |
| 24 | `game/data/endings/_template.json` | 结局数据模板 | E0.3 |
| 25 | `tools/validate_data.py` | JSON 校验脚本 | E0.3 |
| 26 | `tools/validate_consistency.py` | 一致性校验脚本 | E0.3 |
| 27 | `.gitignore` | Git 忽略规则 | E0.2 |
| 28 | `.gitattributes` | Git 属性 | E0.2 |
| 29 | `.github/workflows/ci.yml` | CI 流水线 | E0.6 |
| 30 | `requirements-dev.txt` | 开发依赖 | E0.6 |
| 31 | `tests/pytest.ini` | pytest 配置 | E0.6 |
| 32 | `tests/conftest.py` | pytest fixtures | E0.6 |
| 33 | `CONTRIBUTING.md` | 贡献指南 | E0.2 |
| 34 | `README.md` | 项目说明 | E0.1 |
| 35 | `CLAUDE.md` | 技术偏好 | E0.1 |

---

## 4. options.rpy 配置

```renpy
# game/options.rpy — Ren'Py 全局配置

define config.name = _("双生天使的拥抱")
define config.version = "0.1.0"
define build.name = "TwinAngels"

define gui.show_name = True
define gui.text_size = 33
define gui.text_xsize = 40
define gui.name_text_size = 45
define gui.interface_text_size = 33
define gui.label_text_size = 36
define gui.notify_text_size = 24

define config.screen_width = 1920
define config.screen_height = 1080

define config.window_title = "{#gui.show_name}{#window_title}{#config.name} — {#config.version}"

# 存档配置
define config.save_directory = "TwinAngels-1234567890"

# 自动存档频率
define config.autosave_frequency = 0  # 手动控制，在章节切换时触发

# 文本速度
default preferences.text_cps = 50  # 默认速度

# 跳过设置
default preferences.skip_unseen = False
default preferences.skip_after_choices = False

# 音量
default preferences.music_volume = 0.8
default preferences.sfx_volume = 0.8

# 全屏
default preferences.fullscreen = False

# 主题颜色（紫色/金色）
define gui.accent_color = '#9b6bc5'      # 紫色主题
define gui.idle_color = '#4a4a4a'
define gui.hover_color = '#c8a0e6'
define gui.selected_color = '#c8a0e6'
define gui.insensitive_color = '#8c8c8c'

# 对话框
define gui.textbox_height = 278
define gui.textbox_yalign = 1.0

# 名称框
define gui.name_xpos = 360
define gui.name_ypos = 0
define gui.namebox_width = 420
define gui.namebox_height = 40

# 版本标记（存档兼容性）
define config.script_version = 1  # 增加此值表示存档格式不兼容变更
```

---

## 5. JSON 数据模板

### 5.1 质点数据模板

```json
// game/data/sephirot/_template.json
{
    "sephirot_id": 0,
    "name": "模板",
    "pinyin": "template",
    "chapter": 0,
    "phase": "FORGETTING",
    "primary_undertow": "SHAME_LOOP",
    "composite_undertows": [],
    "base_intensity": 1,
    "intervention_type": "gentle",
    "wing_cost": 0.0,
    "special_rules": []
}
```

### 5.2 Ch1 质点数据

```json
// game/data/sephirot/sephirot_01.json
{
    "sephirot_id": 1,
    "name": "王国",
    "pinyin": "wangguo",
    "chapter": 1,
    "phase": "FORGETTING",
    "primary_undertow": "EXIST_DENY",
    "composite_undertows": [],
    "base_intensity": 2,
    "intervention_type": "gentle",
    "wing_cost": 0.0,
    "special_rules": []
}
```

### 5.3 选择节点模板

```json
// game/data/choices/ch01/_template.json
{
    "choice_id": "template_ch01_c1",
    "sephirot_id": 1,
    "prompt_text": "（选择提示文本）",
    "options": [
        {
            "option_id": "opt_a",
            "text": "（选项 A 文本）",
            "confrontation_tag": "ENGAGE",
            "progress_value": 1.0,
            "texture_tag": "courage",
            "angel_response_delta": {
                "warmth": 0.0,
                "depth": 0.0,
                "protectiveness": 0.0,
                "vulnerability": 0.0
            },
            "bond_depth_delta": 0.0,
            "narrative_jump": null,
            "existence_protection_filtered": false
        },
        {
            "option_id": "opt_b",
            "text": "（选项 B 文本）",
            "confrontation_tag": "ESCAPE",
            "progress_value": 0.3,
            "texture_tag": "avoidance",
            "angel_response_delta": {
                "warmth": 0.0,
                "depth": 0.0,
                "protectiveness": 0.0,
                "vulnerability": 0.0
            },
            "bond_depth_delta": 0.0,
            "narrative_jump": null,
            "existence_protection_filtered": false
        }
    ]
}
```

### 5.4 暗流定义模板

```json
// game/data/protection/_template.json
{
    "code": "TEMPLATE",
    "name": "模板暗流",
    "description": "模板描述",
    "trigger_conditions": [
        {"type": "narrative_tag", "value": "template_tag"},
        {"type": "keyword", "value": ["关键词1", "关键词2"]}
    ],
    "intensity_levels": {
        "low": {
            "range": [1, 3],
            "visual": "template_visual_low",
            "audio": "template_audio_low",
            "duration": [15, 25],
            "angel_intervention_type": "gentle",
            "angel_lines": ["天使台词 1", "天使台词 2"]
        },
        "mid": {
            "range": [4, 6],
            "visual": "template_visual_mid",
            "audio": "template_audio_mid",
            "duration": [20, 35],
            "angel_intervention_type": "active",
            "angel_lines": ["天使台词 1", "天使台词 2"]
        },
        "high": {
            "range": [7, 10],
            "visual": "template_visual_high",
            "audio": "template_audio_high",
            "duration": [30, 45],
            "angel_intervention_type": "forceful",
            "angel_lines": ["天使台词 1", "天使台词 2", "天使台词 3"]
        }
    },
    "wing_cost_multiplier": 1.0,
    "special_rules": []
}
```

### 5.5 对话池骨架

```json
// game/data/angel/dialogue_pool.json
{
    "dialogue_entries": [
        {
            "id": "dlg_001",
            "phase": "FORGETTING",
            "emotional_state": "calm",
            "completion_type": "none",
            "text": "我在这里。你不用害怕。",
            "context_tags": []
        },
        {
            "id": "dlg_002",
            "phase": "FORGETTING",
            "emotional_state": "calm",
            "completion_type": "none",
            "text": "慢慢来。不着急。",
            "context_tags": []
        },
        {
            "id": "dlg_003",
            "phase": "FORGETTING",
            "emotional_state": "calm",
            "completion_type": "full",
            "text": "你做得很好。我在你身边。",
            "context_tags": []
        }
    ]
}
```

### 5.6 结局数据模板

```json
// game/data/endings/_template.json
{
    "ending_code": "TEMPLATE",
    "name": "模板结局",
    "description": "模板描述",
    "conditions": {
        "bond_depth_min": 0.0,
        "chapters_completed": 16,
        "required_tags": []
    },
    "epilogue_text": "（结局后日谈文本）"
}
```

---

## 6. 核心系统骨架文件

### 6.1 constants.rpy

```renpy
# game/scripts/systems/constants.rpy — 常量与枚举定义

init python:

    # ── Phase 枚举 ──
    class Phase:
        FORGETTING = "forgetting"       # Ch 1-3
        TRIAL_EARLY = "trial_early"     # Ch 4-8
        TRIAL_LATE = "trial_late"       # Ch 9-13
        TRUTH = "truth"                 # Ch 14-16

    # ── SephirotState 枚举 ──
    class SephirotState:
        LOCKED = "LOCKED"
        ACTIVE = "ACTIVE"
        COMPLETED_FULL = "COMPLETED_FULL"
        COMPLETED_HALF = "COMPLETED_HALF"

    # ── ConfrontationTag 枚举 ──
    class ConfrontationTag:
        ENGAGE = "ENGAGE"
        ESCAPE = "ESCAPE"
        NEUTRAL = "NEUTRAL"

    # ── UndertowCode 枚举（8 种暗流） ──
    class UndertowCode:
        SHAME_LOOP = "SHAME_LOOP"
        POSS_DENY = "POSS_DENY"
        PAIN_AMP = "PAIN_AMP"
        HOPE_ERASE = "HOPE_ERASE"
        EXIST_DENY = "EXIST_DENY"
        NIHILISM = "NIHILISM"
        RAGE_INC = "RAGE_INC"
        HARM_GUIDE = "HARM_GUIDE"

    # ── AngelEmotionalState 枚举 ──
    class AngelEmotionalState:
        CALM = "calm"
        ACHING = "aching"
        RESOLUTE = "resolute"
        SORROWFUL = "sorrowful"
        TENDER = "tender"

    # ── AngelPresenceState 枚举 ──
    class AngelPresenceState:
        PRESENT = "PRESENT"
        CONCEALED = "CONCEALED"
        INTERVENING = "INTERVENING"
        ABSENT = "ABSENT"
        ETERNAL = "ETERNAL"

    # ── InterventionType 枚举 ──
    class InterventionType:
        GENTLE = "gentle"
        ACTIVE = "active"
        FORCEFUL = "forceful"
        URGENT = "urgent"

    # ── NarrativeBeat 枚举（五拍） ──
    class NarrativeBeat:
        ENCOUNTER = "ENCOUNTER"
        STRUGGLE = "STRUGGLE"
        COMFORT = "COMFORT"
        CHOICE = "CHOICE"
        TRANSFORM = "TRANSFORM"

    # ── 数值常量 ──
    WING_BRIGHTNESS_MIN = 0.05
    NIHILISM_THRESHOLD = 0.7
    BASE_COST = 0.02

    # ── Phase 代价乘数表 ──
    PHASE_MULTIPLIER = {
        Phase.FORGETTING: 0.0,
        Phase.TRIAL_EARLY: 1.0,
        Phase.TRIAL_LATE: 1.5,
        Phase.TRUTH: 2.5,
    }

    # ── 强度乘数表 ──
    INTENSITY_MULTIPLIER = {
        "low": 0.5,
        "mid": 1.0,
        "high": 1.5,
    }

    # ── 翅膀阶段基线表 ──
    WING_STAGE_BASELINE = {
        1: 1.0,
        2: 0.85,
        3: 0.65,
        4: 0.35,
        5: 0.15,
    }

    # ── 介入延迟表（秒） ──
    INTERVENTION_DELAY = {
        "low": 3,
        "mid": 5,
        "high": 8,
    }

    # ── 恢复时间表（秒） ──
    RECOVERY_TIME = {
        "low": 3,
        "mid": 5,
        "high": 8,
    }

    # ── 逃避次数阈值 ──
    ESCAPE_THRESHOLD = 3  # 第 3 次 ESCAPE 触发天使代为面对

    # ── 拥抱次数限制 ──
    HUG_LIMIT_PHASE_1_2 = 3
    HUG_COOLDOWN = 30  # 点击天使冷却（秒）
```

### 6.2 state.rpy

```renpy
# game/scripts/systems/state.rpy — default/persistent 变量声明

# ═══════════════════════════════════════════════════════════
# 存档级变量（default）— 随 Ren'Py 存档保存/恢复
# ═══════════════════════════════════════════════════════════

# ── C1 叙事引擎 ──
default current_chapter = 1                    # 当前章节号 (1-16) | 所有者: C1
default current_sephirot_id = 1                 # 当前质点 ID (1-16) | 所有者: C1
default current_phase = Phase.FORGETTING         # 当前 Phase | 所有者: C1
default narrative_beat = NarrativeBeat.ENCOUNTER # 当前叙事节拍 | 所有者: C1
default active_narrative_tags = set()            # 活跃叙事标签集合 | 所有者: C1

# ── C2 天使陪伴 ──
default wing_brightness_permanent = 1.0         # 翅膀永久亮度 (0.05-1.0) | 所有者: C2
default wing_brightness_temporary = 0.0         # 翅膀临时暗淡 | 所有者: C2
default angel_presence_state = AngelPresenceState.PRESENT  # 天使存在状态 | 所有者: C2
default angel_emotional_state = AngelEmotionalState.CALM   # 天使情感状态 | 所有者: C2
default angel_intervention_count = 0            # 天使介入总次数 | 所有者: C5→C2 读取
default bond_depth = 0.0                        # 情感联结深度 (0.0-1.0) | 所有者: C2
default hug_count_this_sephirot = 0             # 当前质点拥抱次数 | 所有者: C2
default hug_cooldown_end_time = 0               # 点击天使冷却结束时间 | 所有者: C2

# ── C3 选择系统 ──
default choice_history = []                     # 选择历史记录 | 所有者: C3

# ── C4 质点进程 ──
default sephirot_states = {i: SephirotState.LOCKED for i in range(1, 17)}  # 16 质点状态 | 所有者: C4
default escape_counts = {}                      # 各质点逃避计数 {sephirot_id: count} | 所有者: C4
default consecutive_escape_count = 0            # 连续逃避计数 | 所有者: C4

# ── C5 存在保护 ──
default undertow_state = {                      # 暗流运行时状态 | 所有者: C5
    "active_undertows": [],
    "afterimage_undertows": [],
    "nihilism_warning_triggered": False,
    "intervention_log": [],
}
default final_choice_unlocked = False           # 最终选择解锁标记 | 所有者: C5

# ── C6 存档系统 ──
# (存档槽位由 Ren'Py 原生管理，无需 default 变量)


# ═══════════════════════════════════════════════════════════
# 跨周目变量（persistent）— 不随新游戏重置
# ═══════════════════════════════════════════════════════════

default persistent.endings_seen = []             # 已达成结局列表
default persistent.cg_unlocked = []              # 已解锁 CG 列表
default persistent.total_playthroughs = 0        # 总周目数
default persistent.first_playthrough = True      # 是否首次游玩
default persistent.sephirot_completion_records = {}  # 各质点历史完成类型

# ── 无障碍标志位（persistent）──
default persistent.low_stim_mode = False         # 低刺激模式
default persistent.visual_undertow_off = False   # 暗流视觉关闭
default persistent.screen_shake_off = False      # 屏幕抖动关闭
default persistent.audio_stable_mode = False     # 音频稳定模式


# ═══════════════════════════════════════════════════════════
# after_load 钩子：读档后恢复/校验
# ═══════════════════════════════════════════════════════════

label after_load:
    python:
        # 存档完整性校验
        import save_integrity
        save_integrity.validate_save_integrity()

        # 翅膀亮度范围钳制
        wing_brightness_permanent = max(WING_BRIGHTNESS_MIN, min(1.0, wing_brightness_permanent))
        wing_brightness_temporary = max(0.0, wing_brightness_temporary)

        # 章节号范围钳制
        current_chapter = max(1, min(16, current_chapter))

        # 通知系统更新（Batch 1+ 实现）
        # angel_system.update_visual()
        # narrative_router.sync_state()
    return
```

### 6.3 data_loader.py

```python
# game/scripts/systems/data_loader.py — JSON 数据加载器

import json
import os
from pathlib import Path

class DataLoadError(Exception):
    """数据加载错误"""
    def __init__(self, path, message):
        self.path = path
        self.message = message
        super().__init__(f"DataLoadError [{path}]: {message}")

def load_json(path):
    """加载单个 JSON 文件，返回 dict"""
    if not os.path.exists(path):
        raise DataLoadError(path, "File not found")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise DataLoadError(path, f"JSON decode error: {e}")

def load_all(directory):
    """加载目录下所有 JSON 文件，返回 {filename: data} 字典"""
    result = {}
    if not os.path.isdir(directory):
        raise DataLoadError(directory, "Directory not found")
    for filename in os.listdir(directory):
        if filename.endswith('.json') and not filename.startswith('_'):
            filepath = os.path.join(directory, filename)
            result[filename] = load_json(filepath)
    return result

def get_game_data_path():
    """获取 game/data/ 目录路径"""
    # Ren'Py 运行时：config.gamedir
    # 测试环境：基于项目根目录
    try:
        import renpy
        return os.path.join(renpy.config.gamedir, "data")
    except ImportError:
        # 测试环境
        return os.path.join(os.path.dirname(__file__), "..", "..", "data")
```

### 6.4 wing_brightness.rpy

```renpy
# game/scripts/systems/wing_brightness.rpy — 翅膀亮度双层模型

init python:

    class WingBrightnessModel:
        """[ADR-004] 翅膀亮度双层模型

        permanent: 阶段基线初始化 → C5 代价永久扣减 → 阶段切换重置
        temporary: 高强度暗流即时效果 → 场景结束恢复
        displayed: max(动态下限, permanent - temporary)
        """

        @staticmethod
        def get_displayed():
            """返回当前显示亮度"""
            dynamic_floor = max(
                WING_BRIGHTNESS_MIN,
                WING_STAGE_BASELINE.get(WingBrightnessModel.get_stage(), 0.05) * 0.15
            )
            return max(dynamic_floor, wing_brightness_permanent - wing_brightness_temporary)

        @staticmethod
        def get_stage():
            """返回翅膀视觉阶段 (1-5)"""
            b = wing_brightness_permanent
            if b >= 0.8:
                return 1
            elif b >= 0.6:
                return 2
            elif b >= 0.4:
                return 3
            elif b >= 0.2:
                return 4
            else:
                return 5

        @staticmethod
        def apply_permanent_dim(amount):
            """永久扣减（C5 调用）"""
            global wing_brightness_permanent
            wing_brightness_permanent = max(
                WING_BRIGHTNESS_MIN,
                wing_brightness_permanent - amount
            )

        @staticmethod
        def apply_temporary_dim(amount):
            """临时暗淡（高强度暗流即时效果）"""
            global wing_brightness_temporary
            wing_brightness_temporary += amount

        @staticmethod
        def clear_temporary_dim():
            """清除临时暗淡（场景结束）"""
            global wing_brightness_temporary
            wing_brightness_temporary = 0.0

        @staticmethod
        def set_stage_baseline(stage):
            """设置阶段基线（章节切换时调用）"""
            global wing_brightness_permanent
            wing_brightness_permanent = WING_STAGE_BASELINE.get(stage, 1.0)

        @staticmethod
        def reset_for_ch16():
            """Ch16 重置：恢复到 1.0"""
            global wing_brightness_permanent, wing_brightness_temporary
            wing_brightness_permanent = 1.0
            wing_brightness_temporary = 0.0
```

---

## 7. Ch1 骨架章节脚本

```renpy
# game/scripts/ch01_sephirot_01.rpy — Ch1 王国/白花 骨架章节

# Ch1 = 质点 1「王国」，主暗流 EXIST_DENY（低强度 2）
# 五拍叙事：ENCOUNTER → STRUGGLE → COMFORT → CHOICE → TRANSFORM

label ch01_sephirot_01:

    # ── 章节初始化 ──
    $ current_chapter = 1
    $ current_sephirot_id = 1
    $ current_phase = Phase.FORGETTING
    $ active_narrative_tags = set()

    # 自动存档
    $ renpy.save("auto-1")

    # 章节标题卡
    scene black
    show text "第一章 · 王国" at truecenter
    $ renpy.pause(3.0)
    hide text

    # ════════ ① ENCOUNTER ════════
    $ narrative_beat = NarrativeBeat.ENCOUNTER

    scene bg placeholder_01
    show beloved placeholder at center

    "灰色的天空下，废墟绵延到看不到尽头。"
    "心爱的站在废墟的中央，风吹起她的发。"
    "她的身后，一个紫色的身影静静站着。"

    show angel placeholder at left

    angel "我在。"

    "天使的声音很轻，但在风中听得很清楚。"

    # ════════ ② STRUGGLE ════════
    $ narrative_beat = NarrativeBeat.STRUGGLE

    # 设置叙事标签 → 触发暗流
    $ set_narrative_tag("existence_denied")

    "废墟中传来低沉的声音。"
    "「你为什么要在这里？你的存在只是负担。如果没有你，这里不会变成废墟。」"

    # 触发暗流：EXIST_DENY 低强度 2
    $ trigger_undertow("EXIST_DENY", 2)

    "心爱的的立绘微微变淡了。世界好像在否定她存在的意义。"

    # ════════ ③ COMFORT ════════
    $ narrative_beat = NarrativeBeat.COMFORT

    # 天使介入（gentle，Phase 1 无代价）
    angel "你的存在不是负担。"
    angel "你是我存在的理由。"

    "天使轻轻走到心爱的身边。她的翅膀发出温暖的光。"
    "画面慢慢恢复了色彩。心爱的的立绘重新变得清晰。"

    # 暗流解除
    $ deactivate_undertow("EXIST_DENY")

    # ════════ ④ CHOICE ════════
    $ narrative_beat = NarrativeBeat.CHOICE

    "天使握住了心爱的的手。"
    angel "这片废墟不是你的错。但你可以选择——留在这里，还是往前走。"

    # 呈现选择
    $ present_choice("ch01_s1_c1")

    # ════════ ⑤ TRANSFORM ════════
    $ narrative_beat = NarrativeBeat.TRANSFORM

    "无论心爱的做了什么选择，天使都站在她身边。"

    # 质点完成检查（由 C4 处理）
    $ complete_sephirot(1)

    # 路由到下一章
    $ route_to_chapter(2)

    jump ch02_sephirot_02
```

---

## 8. Git 初始化配置

### 8.1 .gitignore

```gitignore
# Ren'Py 编译产物
*.rpyc
*.rpymc

# Python 缓存
__pycache__/
*.pyc
*.pyo

# 存档
saves/

# 环境变量
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# 构建产物
build/
dist/
*.zip
*.tar.gz

# 临时文件
*.tmp
*.log
```

### 8.2 .gitattributes

```gitattributes
# 换行符处理
*.rpy text eol=lf
*.py text eol=lf
*.json text eol=lf
*.md text eol=lf
*.rpyc binary
*.png binary
*.jpg binary
*.webp binary
*.ogg binary
*.mp3 binary
```

### 8.3 CONTRIBUTING.md（摘要）

```markdown
# 贡献指南

## 分支策略

- `main`: 稳定发布分支
- `develop`: 集成分支
- `feature/E{X.Y}-{slug}`: 功能分支（如 `feature/E0.1-project-init`）
- `release/v{X.Y.Z}`: 发布分支
- `hotfix/v{X.Y.Z}`: 热修复分支

## 提交规范

格式：`type(scope): description`

类型：
- `feat`: 新功能
- `fix`: 修复
- `refactor`: 重构
- `test`: 测试
- `docs`: 文档
- `chore`: 杂项

作用域（scope）：
- `c1`: 叙事引擎
- `c2`: 天使陪伴
- `c3`: 选择系统
- `c4`: 质点进程
- `c5`: 存在保护
- `c6`: 存档系统
- `data`: 数据层
- `ui`: 界面层
- `infra`: 基础设施

示例：
- `feat(c5): implement undertow trigger engine`
- `fix(c2): wing brightness dynamic floor calculation`
- `test(c4): add sephirot completion tests`
```

---

## 9. CI 流水线配置

### 9.1 .github/workflows/ci.yml

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install ruff
      - run: ruff check game/scripts/systems/ tests/ tools/

  data-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install jsonschema
      - run: python tools/validate_data.py
      - run: python tools/validate_consistency.py

  unit-tests:
    runs-on: ubuntu-latest
    needs: [lint, data-validation]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements-dev.txt
      - run: python -m pytest tests/unit/ -v --cov=game/scripts/systems --cov-report=xml
      - uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements-dev.txt
      - run: python -m pytest tests/integration/ -v
```

### 9.2 requirements-dev.txt

```text
pytest>=7.0
pytest-cov>=4.0
pytest-mock>=3.0
ruff>=0.1
jsonschema>=4.0
```

---

## 10. Batch 0 Exit 检查清单

### 10.1 功能验证

| # | 检查项 | 验证方法 | 通过标准 |
|---|--------|---------|---------|
| 1 | 项目可在 Ren'Py SDK 中打开 | `renpy.exe game` | 无报错，标题画面显示 |
| 2 | Ch1 可从开始到结束走通 | 手动游玩 Ch1 | 5 拍全部触发，无崩溃 |
| 3 | 选择 ENGAGE → 质点 COMPLETED_FULL | 游玩验证 | `sephirot_states[1] == "COMPLETED_FULL"` |
| 4 | 选择 ESCAPE → 逃避计数 +1 | 游玩验证 | `escape_counts[1] == 1` |
| 5 | Ch1 结束 → 路由到 Ch2 | 游玩验证 | `current_chapter == 2` |
| 6 | 存档/读档 → 状态恢复 | 存档后读档 | 所有 default 变量正确恢复 |
| 7 | 暗流触发 → 天使介入 → 画面恢复 | 游玩验证 | EXIST_DENY 触发 → 天使台词 → 恢复 |
| 8 | Phase 1 翅膀无代价 | 游玩验证 | `wing_brightness_permanent == 1.0` |

### 10.2 技术验证

| # | 检查项 | 验证方法 | 通过标准 |
|---|--------|---------|---------|
| 9 | ruff lint 通过 | `ruff check` | 无错误 |
| 10 | JSON 校验通过 | `python tools/validate_data.py` | 无错误 |
| 11 | 一致性校验通过 | `python tools/validate_consistency.py` | 无错误 |
| 12 | 单元测试通过 | `python -m pytest tests/unit/` | 全部 PASS |
| 13 | 集成测试通过 | `python -m pytest tests/integration/` | 全部 PASS |
| 14 | 覆盖率 ≥ 80% | `pytest --cov` | ≥ 80% |
| 15 | CI 流水线通过 | GitHub Actions | 全绿 |

### 10.3 文档验证

| # | 检查项 | 通过标准 |
|---|--------|---------|
| 16 | 目录结构与架构文档一致 | 对照 `main-architecture.md` §3.1 |
| 17 | 常量值与 GDD 一致 | 对照各 GDD 和架构文档 |
| 18 | 变量所有权矩阵完整 | 对照 `main-architecture.md` §6 |
| 19 | 禁止操作清单 P1-P10 检查 | 无违反 |
| 20 | README 存在且可指导启动 | 新成员可按 README 启动项目 |

### 10.4 Batch 0 → Batch 1 交接

Batch 0 Exit 检查全部通过后，可进入 Batch 1：

- [x] C1 章节路由可工作
- [x] C6 存档/读档 + persistent 变量管理正确
- [x] JSON 数据层骨架 + 加载器 + 校验脚本可工作
- [x] options.rpy 基础配置完成
- [x] CI 流水线可运行 lint + typecheck + test
- [ ] Ch1 骨架章节可玩验证通过（Exit 检查 #2）

---

**文档结束**

> 本文档为 Batch 0 项目骨架的完整定义。包含目录结构、初始文件清单、配置文件、JSON 模板、系统骨架代码、Ch1 骨架脚本、Git 配置、CI 配置和 Exit 检查清单。
>
> 待协调项：
> 1. Ren'Py 版本钉定：创建 `docs/engine-reference/renpy/VERSION.md`
> 2. 美术占位图：需要 `angel_placeholder.png` 和 `beloved_placeholder.png`（可由 art-director 提供简易占位图或使用纯色块）
> 3. CI 环境 Ren'Py SDK 下载链接需在版本钉定后更新
> 4. GitHub 仓库创建和分支初始化需主理人审批
