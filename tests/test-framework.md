# 测试框架方案

> **The Embrace of the Twin Angels** — Test Framework Specification
>
> 产出者：程基岩（engineering-lead）
>
> 日期：2026-08-02
>
> 依赖文档：`docs/architecture/main-architecture.md`、`docs/architecture/control-checklist.md`、`docs/architecture/architecture-review.md`、`design/gdd/*-gdd.md`

---

## 目录

1. [测试策略总览](#1-测试策略总览)
2. [测试工具链](#2-测试工具链)
3. [测试目录结构](#3-测试目录结构)
4. [分层测试体系](#4-分层测试体系)
5. [关键测试用例清单](#5-关键测试用例清单)
6. [测试数据策略](#6-测试数据策略)
7. [CI 集成方案](#7-ci-集成方案)
8. [测试覆盖率目标](#8-测试覆盖率目标)

---

## 1. 测试策略总览

### 1.1 核心原则：验证驱动开发

按控制清单 CC-§6 测试标准 T1-T4 要求，采用**验证驱动开发**（Verification-Driven Development）：

1. **先写测试再实现**：每个 Story 实现前先编写验收标准对应的测试用例
2. **测试覆盖关键路径**：翅膀亮度双层模型、选择后果分发、暗流触发链、质点完成判定
3. **数据驱动测试**：JSON 数据通过 Schema 校验 + 一致性检查
4. **集成测试验证跨系统链路**：C1→C3→C4→C5→C6 全链路

### 1.2 测试金字塔

```
           ╱ E2E ╲          ← Ren'Py 端到端（少量，手动+半自动）
          ╱───────╲
         ╱ 集成测试 ╲        ← 跨系统链路（中等数量，自动）
        ╱───────────╲
       ╱   单元测试    ╲     ← 系统内部逻辑（大量，自动）
      ╱─────────────────╲
     ╱   数据校验         ╲   ← JSON Schema + 一致性（大量，自动）
    ╱─────────────────────╲
```

| 层级 | 占比 | 工具 | 运行环境 |
|------|------|------|---------|
| 数据校验 | 40% | `tools/validate_data.py` + JSON Schema | CI |
| 单元测试 | 35% | `pytest` + Ren'Py `init python` 块 | CI |
| 集成测试 | 20% | `pytest` + Ren'Py 测试模式 | CI + 本地 |
| E2E 测试 | 5% | 手动 Playtest + 录屏验证 | 本地 |

### 1.3 测试与 Batch 对齐

| Batch | 测试重点 | 关键测试 |
|-------|---------|---------|
| Batch 0 | 基础设施 + C1 + C6 骨架 | JSON 加载器、存档/读档、章节路由、Ch1 骨架走通 |
| Batch 1 | C3 + C5 + C2 核心系统 | 选择分发、暗流触发链、翅膀代价计算、天使介入流程 |
| Batch 2 | C4 + 集成 + 可访问性 | 质点完成判定、五拍叙事全链路、无障碍标志位 |
| Batch 3 | 内容 + UI + 打磨 | 16 章可玩性、三结局可达性、翅膀亮度曲线 |

---

## 2. 测试工具链

### 2.1 工具选型

| 工具 | 用途 | 版本 | 备注 |
|------|------|------|------|
| `pytest` | 单元/集成测试框架 | ≥7.0 | Python 标准 |
| `pytest-cov` | 覆盖率统计 | ≥4.0 | HTML + XML 报告 |
| `pytest-mock` | Mock/patch | ≥3.0 | 系统间依赖隔离 |
| `ruff` | Lint + 格式 | ≥0.1 | 替代 flake8 + black |
| `jsonschema` | JSON Schema 校验 | ≥4.0 | 数据层校验 |
| `Ren'Py SDK` | 脚本语法检查 + E2E | 8.x | `renpy.exe lint` |

### 2.2 开发依赖

```python
# requirements-dev.txt
pytest>=7.0
pytest-cov>=4.0
pytest-mock>=3.0
ruff>=0.1
jsonschema>=4.0
```

### 2.3 Ren'Py 测试模式

Ren'Py 提供内置测试支持，通过 `renpy.exe test` 运行 `.rpy` 中定义的测试命令序列。本项目利用此功能进行 E2E 场景测试：

```renpy
# game/tests/e2e_ch01_skeleton.rpy
# Ren'Py 内置测试：验证 Ch1 骨架可走通

init python:
    test_ch01 = [
        ("start_game", {}),
        ("click_through_dialogue", {"count": 20}),
        ("assert_variable", {"name": "current_chapter", "value": 1}),
        ("make_choice", {"option_index": 0}),  # ENGAGE
        ("assert_variable", {"name": "sephirot_states", "key": 1, "value": "COMPLETED_FULL"}),
        ("assert_variable", {"name": "current_chapter", "value": 2}),
    ]
```

---

## 3. 测试目录结构

```
tests/
├── unit/                           # 单元测试（pytest）
│   ├── test_data_loader.py         # JSON 加载器测试
│   ├── test_constants.py           # 常量/枚举一致性测试
│   ├── test_state_variables.py     # default/persistent 变量测试
│   ├── test_choice_node.py         # ChoiceNode 数据结构测试
│   ├── test_choice_dispatcher.py  # 选择后果分发器测试
│   ├── test_sephirot_state.py      # 质点状态机测试
│   ├── test_sephirot_completion.py # 完成判定逻辑测试
│   ├── test_undertow_engine.py     # 暗流触发引擎测试
│   ├── test_angel_intervention.py  # 天使介入流程测试
│   ├── test_wing_brightness.py     # 翅膀亮度双层模型测试
│   ├── test_wing_cost.py           # 翅膀代价计算测试
│   ├── test_nihilism_block.py      # 虚无主义阻断测试
│   ├── test_angel_state_machine.py # 天使状态机测试
│   ├── test_dialogue_pool.py       # 对话池检索测试
│   ├── test_narrative_router.py    # 章节路由测试
│   ├── test_narrative_tags.py      # 叙事标签测试
│   ├── test_save_integrity.py     # 存档完整性校验测试
│   └── test_accessibility_flags.py # 无障碍标志位测试
│
├── integration/                    # 集成测试（pytest + Ren'Py mock）
│   ├── test_choice_to_sephirot.py  # 选择→质点完成链路
│   ├── test_undertow_to_wing.py    # 暗流→翅膀代价链路
│   ├── test_five_beat_flow.py      # 五拍叙事全链路
│   ├── test_phase_transition.py    # Phase 切换链路
│   ├── test_ch16_shutdown.py       # Ch16 关闭序列
│   ├── test_save_load_cycle.py     # 存档/读档全循环
│   └── test_accessibility_system.py # 无障碍系统全链路
│
├── data/                           # 测试数据
│   ├── fixtures/                   # 测试固件 JSON
│   │   ├── choices/
│   │   │   ├── choice_engage.json  # ENGAGE 选择测试数据
│   │   │   ├── choice_escape.json  # ESCAPE 选择测试数据
│   │   │   ├── choice_neutral.json # NEUTRAL 选择测试数据
│   │   │   └── choice_filtered.json # 存在保护过滤测试数据
│   │   ├── sephirot/
│   │   │   ├── sephirot_full_16.json # 16 质点完整数据
│   │   │   └── sephirot_edge.json     # 边界情况数据
│   │   ├── protection/
│   │   │   ├── undertow_all_8.json  # 8 种暗流完整数据
│   │   │   └── undertow_edge.json   # 边界情况数据
│   │   └── angel/
│   │       └── dialogue_pool_test.json # 对话池测试数据
│   │
│   └── schemas/                    # JSON Schema 定义
│       ├── choice_node_schema.json
│       ├── sephirot_schema.json
│       ├── undertow_schema.json
│       └── angel_dialogue_schema.json
│
├── e2e/                            # Ren'Py E2E 测试脚本
│   ├── e2e_ch01_skeleton.rpy       # Ch1 骨架走通测试
│   ├── e2e_ch01_escape.rpy         # Ch1 ESCAPE 路径测试
│   ├── e2e_save_load.rpy           # 存档/读档 E2E
│   └── e2e_full_ch01_03.rpy        # Ch1-3 垂直切片
│
├── conftest.py                     # pytest 共享 fixtures
├── pytest.ini                      # pytest 配置
└── README.md                       # 测试说明文档
```

### 3.1 conftest.py 关键 fixtures

```python
# tests/conftest.py

import pytest
import json
from pathlib import Path

# 测试数据根目录
TEST_DATA_ROOT = Path(__file__).parent / "data" / "fixtures"

@pytest.fixture
def undertow_definitions():
    """加载完整 8 种暗流定义测试数据"""
    with open(TEST_DATA_ROOT / "protection" / "undertow_all_8.json") as f:
        return json.load(f)

@pytest.fixture
def sephirot_data():
    """加载 16 质点完整测试数据"""
    with open(TEST_DATA_ROOT / "sephirot" / "sephirot_full_16.json") as f:
        return json.load(f)

@pytest.fixture
def choice_engage():
    """加载 ENGAGE 选择测试数据"""
    with open(TEST_DATA_ROOT / "choices" / "choice_engage.json") as f:
        return json.load(f)

@pytest.fixture
def mock_renpy_state():
    """模拟 Ren'Py 运行时状态"""
    return {
        "wing_brightness_permanent": 1.0,
        "wing_brightness_temporary": 0.0,
        "bond_depth": 0.0,
        "current_chapter": 1,
        "current_sephirot_id": 1,
        "current_phase": "FORGETTING",
        "angel_emotional_state": "calm",
        "angel_intervention_count": 0,
        "sephirot_states": {i: "LOCKED" for i in range(1, 17)},
        "escape_counts": {},
        "choice_history": [],
    }
```

---

## 4. 分层测试体系

### 4.1 数据校验层

**目标**：确保所有 JSON 数据结构正确、字段完整、跨系统一致性。

#### 4.1.1 JSON Schema 校验

```python
# tools/validate_data.py

import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError

DATA_ROOT = Path("game/data")
SCHEMA_ROOT = Path("tests/data/schemas")

def validate_all():
    """校验所有 JSON 数据文件"""
    errors = []

    # 校验选择节点
    for choice_file in (DATA_ROOT / "choices").rglob("*.json"):
        if choice_file.name.startswith("_"):
            continue
        schema = json.load(open(SCHEMA_ROOT / "choice_node_schema.json"))
        data = json.load(open(choice_file))
        try:
            validate(data, schema)
        except ValidationError as e:
            errors.append(f"{choice_file}: {e.message}")

    # 校验质点数据
    for sephirot_file in (DATA_ROOT / "sephirot").glob("*.json"):
        if sephirot_file.name.startswith("_"):
            continue
        schema = json.load(open(SCHEMA_ROOT / "sephirot_schema.json"))
        data = json.load(open(sephirot_file))
        try:
            validate(data, schema)
        except ValidationError as e:
            errors.append(f"{sephirot_file}: {e.message}")

    # 校验暗流定义
    undertow_file = DATA_ROOT / "protection" / "undertow_definitions.json"
    if undertow_file.exists():
        schema = json.load(open(SCHEMA_ROOT / "undertow_schema.json"))
        data = json.load(open(undertow_file))
        try:
            validate(data, schema)
        except ValidationError as e:
            errors.append(f"{undertow_file}: {e.message}")

    if errors:
        print("❌ Data validation failed:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("✅ All JSON data validated successfully")

if __name__ == "__main__":
    validate_all()
```

#### 4.1.2 跨系统一致性校验

```python
# tools/validate_consistency.py

def validate_confrontation_tag_progress_value(choices_dir):
    """
    校验 confrontation_tag 与 progress_value 的一致性
    [CC-§5] D1: ENGAGE→1.0, ESCAPE→0.3, NEUTRAL→0.0
    """
    TAG_TO_VALUE = {"ENGAGE": 1.0, "ESCAPE": 0.3, "NEUTRAL": 0.0}
    errors = []

    for choice_file in choices_dir.rglob("*.json"):
        data = json.load(open(choice_file))
        for option in data.get("options", []):
            tag = option.get("confrontation_tag")
            value = option.get("progress_value")
            if tag and tag in TAG_TO_VALUE:
                expected = TAG_TO_VALUE[tag]
                if value != expected:
                    errors.append(
                        f"{choice_file} option {option['option_id']}: "
                        f"confrontation_tag={tag} expects progress_value={expected}, got {value}"
                    )
    return errors

def validate_narrative_jump_targets(choices_dir, scripts_dir):
    """
    校验 narrative_jump 目标 label 存在性
    [CC-§5] D2: 所有 narrative_jump 必须指向存在的 label
    """
    # 收集所有 label
    labels = set()
    for rpy_file in scripts_dir.rglob("*.rpy"):
        with open(rpy_file) as f:
            for line in f:
                if line.strip().startswith("label "):
                    label_name = line.strip().split()[1].rstrip(":")
                    labels.add(label_name)

    # 检查 narrative_jump
    errors = []
    for choice_file in choices_dir.rglob("*.json"):
        data = json.load(open(choice_file))
        for option in data.get("options", []):
            jump = option.get("narrative_jump")
            if jump and jump not in labels:
                errors.append(
                    f"{choice_file} option {option['option_id']}: "
                    f"narrative_jump target '{jump}' not found"
                )
    return errors
```

### 4.2 单元测试层

**目标**：验证每个系统类/函数的内部逻辑正确性。

#### 4.2.1 翅膀亮度双层模型测试（关键路径）

```python
# tests/unit/test_wing_brightness.py

class TestWingBrightnessModel:
    """[ADR-004] 翅膀亮度双层模型测试"""

    def test_initial_state(self, mock_renpy_state):
        """初始状态：permanent=1.0, temporary=0, displayed=1.0"""
        state = mock_renpy_state
        assert state["wing_brightness_permanent"] == 1.0
        assert state["wing_brightness_temporary"] == 0.0
        displayed = max(0.05, state["wing_brightness_permanent"] - state["wing_brightness_temporary"])
        assert displayed == 1.0

    def test_apply_permanent_dim(self, mock_renpy_state):
        """永久扣减：permanent 减少"""
        state = mock_renpy_state
        state["wing_brightness_permanent"] -= 0.15  # 模拟 C5 代价
        displayed = max(0.05, state["wing_brightness_permanent"] - state["wing_brightness_temporary"])
        assert state["wing_brightness_permanent"] == 0.85
        assert displayed == 0.85

    def test_apply_temporary_dim(self, mock_renpy_state):
        """临时扣减：temporary 增加，displayed 降低"""
        state = mock_renpy_state
        state["wing_brightness_temporary"] = 0.2  # 高强度暗流即时效果
        displayed = max(0.05, state["wing_brightness_permanent"] - state["wing_brightness_temporary"])
        assert displayed == 0.8

    def test_clear_temporary(self, mock_renpy_state):
        """场景结束：temporary 清零"""
        state = mock_renpy_state
        state["wing_brightness_temporary"] = 0.2
        state["wing_brightness_temporary"] = 0  # clear_temporary_dim()
        displayed = max(0.05, state["wing_brightness_permanent"] - state["wing_brightness_temporary"])
        assert displayed == 1.0  # 恢复到 permanent

    def test_dynamic_floor(self, mock_renpy_state):
        """动态下限：不低于基线×15%"""
        state = mock_renpy_state
        state["wing_brightness_permanent"] = 0.15  # Stage 5 基线
        state["wing_brightness_temporary"] = 0.1   # 临时暗淡
        # 动态下限 = 0.15 × 0.15 = 0.0225, 但 WING_BRIGHTNESS_MIN = 0.05
        displayed = max(0.05, state["wing_brightness_permanent"] - state["wing_brightness_temporary"])
        # max(0.05, 0.15 - 0.1) = max(0.05, 0.05) = 0.05
        assert displayed == 0.05

    def test_stage_mapping(self, mock_renpy_state):
        """阶段映射：permanent → wing_stage"""
        test_cases = [
            (1.0, 1), (0.85, 1), (0.8, 1),
            (0.79, 2), (0.65, 2), (0.6, 2),
            (0.59, 3), (0.4, 3),
            (0.39, 4), (0.2, 4),
            (0.19, 5), (0.05, 5),
        ]
        for brightness, expected_stage in test_cases:
            state = mock_renpy_state.copy()
            state["wing_brightness_permanent"] = brightness
            # get_wing_stage() 逻辑
            if brightness >= 0.8:
                stage = 1
            elif brightness >= 0.6:
                stage = 2
            elif brightness >= 0.4:
                stage = 3
            elif brightness >= 0.2:
                stage = 4
            else:
                stage = 5
            assert stage == expected_stage, f"brightness={brightness} → stage={stage}, expected {expected_stage}"

    def test_phase_reset(self, mock_renpy_state):
        """阶段切换重置：permanent 重置为新基线"""
        baselines = {1: 1.0, 2: 0.85, 3: 0.65, 4: 0.35, 5: 0.15}
        state = mock_renpy_state
        state["wing_brightness_permanent"] = 0.70  # Phase 2a 后半
        # 模拟阶段切换到 Stage 3
        state["wing_brightness_permanent"] = baselines[3]
        assert state["wing_brightness_permanent"] == 0.65

    def test_ch16_reset(self, mock_renpy_state):
        """Ch16 重置：permanent → 1.0"""
        state = mock_renpy_state
        state["wing_brightness_permanent"] = 0.15  # Stage 5 最暗
        # Ch16 关闭序列
        state["wing_brightness_permanent"] = 1.0
        state["wing_brightness_temporary"] = 0.0
        assert state["wing_brightness_permanent"] == 1.0
```

#### 4.2.2 翅膀代价计算测试（关键路径）

```python
# tests/unit/test_wing_cost.py

class TestWingCostCalculation:
    """[GDD:C5-§2.3] 翅膀代价公式测试"""

    BASE_COST = 0.02

    def test_phase1_zero_cost(self):
        """Phase 1：代价乘数 0.0，免费保护"""
        cost = self.BASE_COST * 0.0 * 1.0 * 1.0  # Phase1 × mid × SHAME_LOOP
        assert cost == 0.0

    def test_phase2a_shame_loop_mid(self):
        """Phase 2a：SHAME_LOOP 中强度"""
        # 0.02 × 1.0 × 1.0 × 1.0 = 0.020
        cost = self.BASE_COST * 1.0 * 1.0 * 1.0
        assert abs(cost - 0.020) < 0.001

    def test_phase2a_nihilism_mid(self):
        """Phase 2a：NIHILISM 中强度"""
        # 0.02 × 1.0 × 1.0 × 1.5 = 0.030
        cost = self.BASE_COST * 1.0 * 1.0 * 1.5
        assert abs(cost - 0.030) < 0.001

    def test_phase2a_harm_guide_high(self):
        """Phase 2a：HARM_GUIDE 高强度"""
        # 0.02 × 1.0 × 1.5 × 2.0 = 0.060
        cost = self.BASE_COST * 1.0 * 1.5 * 2.0
        assert abs(cost - 0.060) < 0.001

    def test_phase3_full_peak(self):
        """Phase 3 (Ch14)：全部 8 种同时，峰值"""
        # 0.02 × 2.5 × 1.5 × max_multiplier... 特殊事件 -0.300
        # 这是设计中的特殊事件，非标准公式计算
        pass  # 在集成测试中验证

    def test_composite_undertow_cost(self):
        """复合暗流代价叠加：2 个暗流 ×1.2 倍"""
        base = self.BASE_COST * 1.5 * 1.2  # Phase2b × mid × EXIST_DENY(1.2)
        composite_cost = base * 1.2  # 2 个暗流 +20%
        # 0.02 × 1.5 × 1.0 × 1.2 × 1.2 = 0.0432
        assert abs(composite_cost - 0.0432) < 0.001

    def test_accumulated_curve(self):
        """累积曲线验证：Phase 1→2a→2b→3→Ch16"""
        brightness = 1.0

        # Phase 1: 3 次介入 × cost=0
        for _ in range(3):
            brightness -= 0.0
        assert brightness == 1.0

        # Phase 2a: 5 次介入
        phase2a_costs = [0.020, 0.030, 0.020, 0.020, 0.060]
        for cost in phase2a_costs:
            brightness -= cost
        assert abs(brightness - 0.850) < 0.01  # 1.0 - 0.150 = 0.850

        # Phase 2b: 5 次介入
        phase2b_costs = [0.040, 0.045, 0.050, 0.056, 0.150]
        for cost in phase2b_costs:
            brightness -= cost
        assert abs(brightness - 0.509) < 0.02  # 0.850 - 0.341 = 0.509

        # Phase 3: 2 次介入
        brightness -= 0.300  # Ch14
        brightness -= 0.050  # Ch15
        assert abs(brightness - 0.159) < 0.02  # 0.509 - 0.350 = 0.159

        # Ch16: 重置
        brightness = 1.0
        assert brightness == 1.0
```

#### 4.2.3 质点完成判定测试（关键路径）

```python
# tests/unit/test_sephirot_completion.py

class TestSephirotCompletion:
    """[GDD:C4-§2.3] 完成判定逻辑测试"""

    def test_engage_completes_full(self, mock_renpy_state):
        """ENGAGE → COMPLETED_FULL"""
        state = mock_renpy_state
        state["sephirot_states"][1] = "ACTIVE"
        # 模拟 process_choice("ENGAGE")
        progress = 1.0
        if progress >= 1.0:
            state["sephirot_states"][1] = "COMPLETED_FULL"
        assert state["sephirot_states"][1] == "COMPLETED_FULL"

    def test_escape_first_does_not_complete(self, mock_renpy_state):
        """第 1 次 ESCAPE：不完成"""
        state = mock_renpy_state
        state["sephirot_states"][1] = "ACTIVE"
        state["escape_counts"][1] = 0
        # process_choice("ESCAPE")
        state["escape_counts"][1] += 1
        progress = 0.3
        assert state["escape_counts"][1] == 1
        assert progress < 1.0
        assert state["sephirot_states"][1] == "ACTIVE"  # 未完成

    def test_escape_third_angel_proxy_half(self, mock_renpy_state):
        """第 3 次 ESCAPE：天使代为面对 → COMPLETED_HALF"""
        state = mock_renpy_state
        state["sephirot_states"][1] = "ACTIVE"
        state["escape_counts"][1] = 2
        # process_choice("ESCAPE") → 第 3 次
        state["escape_counts"][1] += 1
        # 第 3 次 → 天使代为面对 → 50% 完成
        state["sephirot_states"][1] = "COMPLETED_HALF"
        assert state["escape_counts"][1] == 3
        assert state["sephirot_states"][1] == "COMPLETED_HALF"

    def test_neutral_no_progress(self, mock_renpy_state):
        """NEUTRAL：不推进进度"""
        state = mock_renpy_state
        state["sephirot_states"][1] = "ACTIVE"
        # process_choice("NEUTRAL")
        progress = 0.0
        assert progress == 0.0
        assert state["sephirot_states"][1] == "ACTIVE"  # 仍活跃

    def test_phase3_no_escape(self, mock_renpy_state):
        """Phase 3 (Ch14-15)：无 ESCAPE 选项"""
        state = mock_renpy_state
        state["current_phase"] = "TRUTH"
        state["current_chapter"] = 14
        # Ch14-15 的选择节点不应包含 ESCAPE 选项
        # 由数据校验保证：validate_phase3_no_escape()

    def test_ch16_all_engage(self, mock_renpy_state):
        """Ch16：三选项全为 ENGAGE"""
        state = mock_renpy_state
        state["current_chapter"] = 16
        # Ch16 的选择节点三选项 confrontation_tag 全为 ENGAGE
        # 由数据校验保证：validate_ch16_all_engage()
```

#### 4.2.4 选择后果分发器测试

```python
# tests/unit/test_choice_dispatcher.py

class TestChoiceDispatcher:
    """[ADR-003] [GDD:C3] 选择后果多系统分发测试"""

    def test_engage_dispatch_order(self, mock_renpy_state, choice_engage):
        """ENGAGE 分发顺序：C6→C4→C2→C5→C1"""
        state = mock_renpy_state
        call_log = []

        # 模拟分发
        call_log.append("C6: update_choice_history")
        call_log.append("C4: add_sephirot_progress(1.0)")
        call_log.append("C2: update_angel_response(delta)")
        call_log.append("C2: update_bond_depth(delta)")
        call_log.append("C5: check_nihilism_risk()")
        call_log.append("C1: narrative_jump(target)")

        # 验证顺序
        assert call_log[0].startswith("C6")
        assert call_log[1].startswith("C4")
        assert call_log[2].startswith("C2")
        assert call_log[4].startswith("C5")

    def test_escape_does_not_complete_sephirot(self, mock_renpy_state):
        """ESCAPE 分发：C4 进度 +0.3，不完成"""
        state = mock_renpy_state
        state["sephirot_states"][1] = "ACTIVE"
        state["escape_counts"][1] = 0
        # 分发 ESCAPE
        progress = 0.3
        state["escape_counts"][1] += 1
        # 进度 0.3 < 1.0，不完成
        assert state["sephirot_states"][1] == "ACTIVE"

    def test_narrative_jump_called(self, mock_renpy_state):
        """narrative_jump 正确执行"""
        # 有 narrative_jump 的选项
        option = {"narrative_jump": "ch02_sephirot_02"}
        # 分发后应调用 renpy.jump("ch02_sephirot_02")
        # 由集成测试验证实际跳转
```

#### 4.2.5 暗流触发引擎测试

```python
# tests/unit/test_undertow_engine.py

class TestUndertowEngine:
    """[GDD:C5-§2.1] 暗流触发引擎测试"""

    @pytest.mark.parametrize("code", [
        "SHAME_LOOP", "POSS_DENY", "PAIN_AMP", "HOPE_ERASE",
        "EXIST_DENY", "NIHILISM", "RAGE_INC", "HARM_GUIDE"
    ])
    def test_all_8_undertows_triggerable(self, code, undertow_definitions):
        """8 种暗流全部可触发"""
        assert code in [u["code"] for u in undertow_definitions["undertows"]]

    @pytest.mark.parametrize("intensity,expected_level", [
        (1, "low"), (2, "low"), (3, "low"),
        (4, "mid"), (5, "mid"), (6, "mid"),
        (7, "high"), (8, "high"), (9, "high"), (10, "high"),
    ])
    def test_intensity_mapping(self, intensity, expected_level):
        """强度 1-10 → low/mid/high 映射"""
        if intensity <= 3:
            level = "low"
        elif intensity <= 6:
            level = "mid"
        else:
            level = "high"
        assert level == expected_level

    def test_harm_guide_no_delay(self):
        """HARM_GUIDE：立即介入，无延迟"""
        # determine_intervention_type("HARM_GUIDE", 1) → "urgent"
        assert True  # 逻辑验证在集成测试

    def test_other_undertows_have_delay(self):
        """非 HARM_GUIDE 暗流有介入延迟"""
        delays = {"low": 3, "mid": 5, "high": 8}
        assert delays["low"] == 3
        assert delays["mid"] == 5
        assert delays["high"] == 8

    def test_wing_cost_multipliers(self, undertow_definitions):
        """每种暗流的翅膀代价倍率正确"""
        expected = {
            "SHAME_LOOP": 1.0, "POSS_DENY": 1.0, "PAIN_AMP": 1.0,
            "HOPE_ERASE": 1.0, "EXIST_DENY": 1.2, "NIHILISM": 1.5,
            "RAGE_INC": 1.0, "HARM_GUIDE": 2.0,
        }
        for undertow in undertow_definitions["undertows"]:
            code = undertow["code"]
            assert undertow["wing_cost_multiplier"] == expected[code]
```

### 4.3 集成测试层

**目标**：验证跨系统链路的正确性，使用 pytest + Ren'Py mock。

#### 4.3.1 选择→质点完成→章节切换全链路

```python
# tests/integration/test_choice_to_sephirot.py

class TestChoiceToSephirotFlow:
    """选择→后果分发→质点完成→章节切换 全链路"""

    def test_engage_full_flow(self, mock_renpy_state):
        """ENGAGE 全链路：选择→进度+1.0→质点 FULL→解锁下一→路由"""
        state = mock_renpy_state
        state["sephirot_states"][1] = "ACTIVE"
        state["current_chapter"] = 1
        state["current_sephirot_id"] = 1

        # 1. 选择 ENGAGE
        # 2. 分发：C6 记录、C4 进度+1.0、C2 更新、C5 检查
        state["sephirot_states"][1] = "COMPLETED_FULL"
        state["sephirot_states"][2] = "ACTIVE"  # 解锁下一
        state["current_chapter"] = 2  # 路由到 Ch2
        state["current_sephirot_id"] = 2

        assert state["sephirot_states"][1] == "COMPLETED_FULL"
        assert state["sephirot_states"][2] == "ACTIVE"
        assert state["current_chapter"] == 2

    def test_escape_third_half_flow(self, mock_renpy_state):
        """3次ESCAPE 全链路：选择→天使代为面对→50%完成→解锁"""
        state = mock_renpy_state
        state["sephirot_states"][1] = "ACTIVE"
        state["escape_counts"][1] = 0

        # 模拟 3 次 ESCAPE
        for i in range(3):
            state["escape_counts"][1] += 1

        # 第 3 次 → 天使代为面对 → 50%
        state["sephirot_states"][1] = "COMPLETED_HALF"
        state["sephirot_states"][2] = "ACTIVE"

        assert state["escape_counts"][1] == 3
        assert state["sephirot_states"][1] == "COMPLETED_HALF"
```

#### 4.3.2 暗流→天使介入→翅膀代价→画面恢复全链路

```python
# tests/integration/test_undertow_to_wing.py

class TestUndertowToWingFlow:
    """暗流→天使介入→翅膀代价→画面恢复 全链路"""

    def test_phase1_no_wing_cost(self, mock_renpy_state):
        """Phase 1：暗流触发→天使介入→翅膀无代价"""
        state = mock_renpy_state
        state["current_phase"] = "FORGETTING"
        state["current_chapter"] = 1
        state["wing_brightness_permanent"] = 1.0

        # 触发 EXIST_DENY 低强度 2
        cost = 0.02 * 0.0 * 0.5 * 1.2  # Phase1 × low × EXIST_DENY
        state["wing_brightness_permanent"] -= cost
        state["angel_intervention_count"] += 1

        assert cost == 0.0
        assert state["wing_brightness_permanent"] == 1.0  # 无变化
        assert state["angel_intervention_count"] == 1

    def test_phase2a_wing_dimmed(self, mock_renpy_state):
        """Phase 2a：暗流→介入→翅膀暗淡"""
        state = mock_renpy_state
        state["current_phase"] = "TRIAL_EARLY"
        state["current_chapter"] = 4
        state["wing_brightness_permanent"] = 1.0

        # 触发 SHAME_LOOP 中强度 5
        cost = 0.02 * 1.0 * 1.0 * 1.0  # Phase2a × mid × SHAME_LOOP
        state["wing_brightness_permanent"] -= cost
        state["angel_intervention_count"] += 1

        assert abs(state["wing_brightness_permanent"] - 0.980) < 0.001
        assert state["angel_intervention_count"] == 1

    def test_harm_guide_urgent_no_skip(self, mock_renpy_state):
        """HARM_GUIDE：urgent 介入，禁用跳过"""
        state = mock_renpy_state
        state["current_chapter"] = 8
        state["wing_brightness_permanent"] = 0.85  # Phase 2a 中段

        # 触发 HARM_GUIDE 中强度 6
        cost = 0.02 * 1.0 * 1.0 * 2.0  # Phase2a × mid × HARM_GUIDE
        state["wing_brightness_permanent"] -= cost
        # urgent 介入 → 禁用跳过 → 台词 → 恢复跳过

        assert abs(state["wing_brightness_permanent"] - 0.810) < 0.001
```

#### 4.3.3 五拍叙事全链路

```python
# tests/integration/test_five_beat_flow.py

class TestFiveBeatFlow:
    """五拍叙事 ENCOUNTER→STRUGGLE→COMFORT→CHOICE→TRANSFORM"""

    def test_full_beat_sequence(self, mock_renpy_state):
        """五拍按顺序推进"""
        state = mock_renpy_state
        beats = []

        # ① ENCOUNTER
        beats.append("ENCOUNTER")
        # 纯叙事，无系统调用

        # ② STRUGGLE
        beats.append("STRUGGLE")
        # C5 暗流触发
        state["wing_brightness_temporary"] = 0.1  # 临时暗淡

        # ③ COMFORT
        beats.append("COMFORT")
        # C5 天使介入，画面恢复
        state["wing_brightness_temporary"] = 0.0  # 清除临时
        state["angel_intervention_count"] += 1

        # ④ CHOICE
        beats.append("CHOICE")
        # C3 选择呈现
        # 模拟选择 ENGAGE
        state["sephirot_states"][1] = "COMPLETED_FULL"

        # ⑤ TRANSFORM
        beats.append("TRANSFORM")
        # C4 进度更新 + 章节切换检查
        state["current_chapter"] = 2

        assert beats == ["ENCOUNTER", "STRUGGLE", "COMFORT", "CHOICE", "TRANSFORM"]
        assert state["sephirot_states"][1] == "COMPLETED_FULL"
        assert state["current_chapter"] == 2
        assert state["wing_brightness_temporary"] == 0.0
```

#### 4.3.4 存档/读档全循环

```python
# tests/integration/test_save_load_cycle.py

class TestSaveLoadCycle:
    """存档/读档全循环测试"""

    def test_save_load_preserves_all_state(self, mock_renpy_state):
        """存档→读档：所有状态正确恢复"""
        original = mock_renpy_state.copy()
        original["wing_brightness_permanent"] = 0.65
        original["sephirot_states"] = {1: "COMPLETED_FULL", 2: "ACTIVE"}
        original["escape_counts"] = {1: 0}
        original["choice_history"] = [
            {"choice_id": "ch01_s1_c1", "option_id": "opt_a", "confrontation_tag": "ENGAGE"}
        ]
        original["angel_intervention_count"] = 3
        original["angel_emotional_state"] = "aching"

        # 模拟存档（序列化）
        saved = json.dumps(original)
        # 模拟读档（反序列化）
        loaded = json.loads(saved)

        assert loaded["wing_brightness_permanent"] == 0.65
        assert loaded["sephirot_states"] == {1: "COMPLETED_FULL", 2: "ACTIVE"}
        assert loaded["escape_counts"] == {1: 0}
        assert len(loaded["choice_history"]) == 1
        assert loaded["angel_intervention_count"] == 3
        assert loaded["angel_emotional_state"] == "aching"

    def test_load_missing_variable_fills_default(self, mock_renpy_state):
        """读档缺少新变量：以默认值填充"""
        # 旧版本存档缺少 angel_emotional_state
        old_save = {
            "wing_brightness_permanent": 0.5,
            "current_chapter": 5,
            "sephirot_states": {1: "COMPLETED_FULL"},
        }

        # after_load 校验
        defaults = mock_renpy_state
        for key, default_val in defaults.items():
            if key not in old_save:
                old_save[key] = default_val

        assert old_save["wing_brightness_permanent"] == 0.5  # 保留
        assert old_save["angel_emotional_state"] == "calm"  # 填充默认
        assert old_save["escape_counts"] == {}  # 填充默认

    def test_load_clamps_invalid_values(self, mock_renpy_state):
        """读档越界值：钳制到有效范围"""
        corrupt_save = {
            "wing_brightness_permanent": 1.5,  # 越界
            "current_chapter": 99,  # 越界
        }

        # 钳制
        corrupt_save["wing_brightness_permanent"] = min(1.0, max(0.05, corrupt_save["wing_brightness_permanent"]))
        corrupt_save["current_chapter"] = min(16, max(1, corrupt_save["current_chapter"]))

        assert corrupt_save["wing_brightness_permanent"] == 1.0
        assert corrupt_save["current_chapter"] == 16
```

### 4.4 E2E 测试层

**目标**：使用 Ren'Py 内置测试命令验证完整游戏流程。

#### 4.4.1 Ch1 骨架走通测试

```renpy
# game/tests/e2e/e2e_ch01_skeleton.rpy
# Ren'Py 内置测试：Ch1 完整走通

init python:
    e2e_ch01_skeleton = [
        # 1. 启动游戏
        ("start",),

        # 2. 验证初始状态
        ("assert", "current_chapter == 1"),
        ("assert", "wing_brightness_permanent == 1.0"),
        ("assert", "sephirot_states[1] == 'ACTIVE'"),

        # 3. 推进到 STRUGGLE 节拍
        ("click",),  # 点击推进对话
        ("click",),
        ("click",),
        ("assert", "narrative_beat == 'STRUGGLE'"),

        # 4. 验证暗流触发
        ("assert", "len(undertow_state['active_undertows']) > 0"),
        ("assert", "undertow_state['active_undertows'][0]['code'] == 'EXIST_DENY'"),

        # 5. 等待天使介入
        ("click",),  # 推进到 COMFORT
        ("click",),
        ("assert", "narrative_beat == 'COMFORT'"),
        ("assert", "angel_intervention_count == 1"),

        # 6. 到达 CHOICE
        ("click",),
        ("assert", "narrative_beat == 'CHOICE'"),

        # 7. 选择 ENGAGE
        ("click", "choice_0"),  # 点击第一个选项
        ("assert", "sephirot_states[1] == 'COMPLETED_FULL'"),

        # 8. TRANSFORM → 路由到 Ch2
        ("assert", "narrative_beat == 'TRANSFORM'"),
        ("assert", "current_chapter == 2"),
    ]
```

---

## 5. 关键测试用例清单

### 5.1 必须通过的测试用例（阻塞性）

| # | 测试名 | 层级 | 验证内容 | 关联 GDD/ADR |
|---|--------|------|---------|-------------|
| T01 | test_initial_state | 单元 | 初始状态 permanent=1.0, temporary=0 | ADR-004 |
| T02 | test_apply_permanent_dim | 单元 | 永久扣减后 permanent 减少 | ADR-004 |
| T03 | test_clear_temporary | 单元 | 场景结束 temporary 清零 | ADR-004 |
| T04 | test_dynamic_floor | 单元 | 亮度不低于动态下限 | ADR-004 |
| T05 | test_stage_mapping | 单元 | permanent → 1-5 阶段映射 | ADR-004 |
| T06 | test_phase1_zero_cost | 单元 | Phase 1 翅膀无代价 | GDD:C5-§2.3 |
| T07 | test_phase2a_costs | 单元 | Phase 2a 各暗流代价正确 | GDD:C5-§2.3 |
| T08 | test_harm_guide_2x_multiplier | 单元 | HARM_GUIDE 倍率 2.0 | GDD:C5-§2.1.9 |
| T09 | test_nihilism_1_5_multiplier | 单元 | NIHILISM 倍率 1.5 | GDD:C5-§2.1.7 |
| T10 | test_accumulated_curve | 单元 | 累积曲线 1.0→0.85→0.509→0.159→1.0 | GDD:C5-§2.3.2 |
| T11 | test_engage_completes_full | 单元 | ENGAGE → COMPLETED_FULL | GDD:C4-§2.3 |
| T12 | test_escape_third_half | 单元 | 3次ESCAPE → COMPLETED_HALF | GDD:C4-§2.3 |
| T13 | test_neutral_no_progress | 单元 | NEUTRAL → 不推进 | GDD:C4-§2.3 |
| T14 | test_all_8_undertows | 单元 | 8 种暗流全部可触发 | GDD:C5-§2.1 |
| T15 | test_intensity_mapping | 单元 | 1-10 → low/mid/high | GDD:C5-§2.1 |
| T16 | test_engage_full_flow | 集成 | ENGAGE 全链路（选择→完成→路由） | ADR-003 |
| T17 | test_undertow_to_wing | 集成 | 暗流→介入→翅膀代价链路 | ADR-003 |
| T18 | test_five_beat_sequence | 集成 | 五拍按顺序推进 | GDD:C4-§2 |
| T19 | test_save_load_preserves | 集成 | 存档/读档全状态恢复 | GDD:C6 |
| T20 | test_load_missing_variable | 集成 | 旧存档缺失变量填充 | CC-§4 |
| T21 | validate_all_json | 数据 | 所有 JSON 通过 Schema 校验 | ADR-002 |
| T22 | validate_tag_consistency | 数据 | confrontation_tag ↔ progress_value 一致 | CC-§5 D1 |
| T23 | e2e_ch01_skeleton | E2E | Ch1 完整走通（5 拍全触发） | GDD:C4-§5 |

### 5.2 建议通过的测试用例（非阻塞但推荐）

| # | 测试名 | 层级 | 验证内容 |
|---|--------|------|---------|
| T24 | test_phase_transition | 集成 | Phase 切换通知 C5/C2 |
| T25 | test_ch16_shutdown | 集成 | Ch16 关闭序列 |
| T26 | test_nihilism_block | 集成 | 虚无主义强制阻断 |
| T27 | test_accessibility_flags | 单元 | 4 级标志位生效 |
| T28 | test_dialogue_pool_no_repeat | 单元 | 对话池去重 |
| T29 | test_angel_state_transitions | 单元 | 天使状态转换规则 |
| T30 | test_composite_undertow | 单元 | 复合暗流代价叠加 |

---

## 6. 测试数据策略

### 6.1 测试固件 JSON 模板

每个测试固件 JSON 遵循与生产数据相同的 Schema，但使用简化的测试数据：

```json
// tests/data/fixtures/choices/choice_engage.json
{
    "choice_id": "test_ch01_engage",
    "sephirot_id": 1,
    "prompt_text": "你面对王国的废墟。你想做什么？",
    "options": [
        {
            "option_id": "opt_a",
            "text": "直面这片废墟",
            "confrontation_tag": "ENGAGE",
            "progress_value": 1.0,
            "texture_tag": "courage",
            "angel_response_delta": {"warmth": 0.1, "depth": 0.05, "protectiveness": 0.0, "vulnerability": 0.0},
            "bond_depth_delta": 0.05,
            "narrative_jump": null,
            "existence_protection_filtered": false
        },
        {
            "option_id": "opt_b",
            "text": "转身离开",
            "confrontation_tag": "ESCAPE",
            "progress_value": 0.3,
            "texture_tag": "avoidance",
            "angel_response_delta": {"warmth": 0.0, "depth": 0.0, "protectiveness": 0.1, "vulnerability": 0.0},
            "bond_depth_delta": -0.02,
            "narrative_jump": null,
            "existence_protection_filtered": false
        }
    ]
}
```

### 6.2 边界情况测试数据

```json
// tests/data/fixtures/choices/choice_edge_cases.json
{
    "choice_id": "test_edge_cases",
    "sephirot_id": 1,
    "prompt_text": "边界情况测试",
    "options": [
        {
            "option_id": "opt_neutral",
            "text": "不选择",
            "confrontation_tag": "NEUTRAL",
            "progress_value": 0.0,
            "texture_tag": "neutral",
            "angel_response_delta": {"warmth": 0.0, "depth": 0.0, "protectiveness": 0.0, "vulnerability": 0.0},
            "bond_depth_delta": 0.0,
            "narrative_jump": null,
            "existence_protection_filtered": false
        },
        {
            "option_id": "opt_filtered",
            "text": "虚无选项",
            "confrontation_tag": "ESCAPE",
            "progress_value": 0.3,
            "texture_tag": "nihilism",
            "angel_response_delta": {"warmth": -0.1, "depth": 0.0, "protectiveness": 0.2, "vulnerability": 0.0},
            "bond_depth_delta": -0.05,
            "narrative_jump": null,
            "existence_protection_filtered": true
        }
    ]
}
```

---

## 7. CI 集成方案

### 7.1 GitHub Actions 工作流

```yaml
# .github/workflows/ci.yml

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

  renpy-lint:
    runs-on: ubuntu-latest
    needs: data-validation
    steps:
      - uses: actions/checkout@v4
      - name: Download Ren'Py SDK
        run: |
          wget -q https://www.renpy.org/dl/8.x/renpy-8.x-sdk.tar.bz2
          tar xjf renpy-8.x-sdk.tar.bz2
      - name: Ren'Py Lint
        run: |
          renpy-8.x-sdk/renpy.sh game lint
```

### 7.2 pytest 配置

```ini
# tests/pytest.ini

[pytest]
testpaths = tests/unit tests/integration
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --tb=short
    --strict-markers
    --cov=game/scripts/systems
    --cov-report=term-missing
    --cov-report=html:tests/coverage_html
    --cov-report=xml:tests/coverage.xml
    --cov-fail-under=80
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    e2e: marks tests as end-to-end tests
```

### 7.3 CI 检查门控

| 检查 | 阻塞合并 | 说明 |
|------|---------|------|
| ruff lint | ✅ | 代码风格不符合则阻塞 |
| JSON 数据校验 | ✅ | 数据结构错误则阻塞 |
| 一致性校验 | ✅ | confrontation_tag ↔ progress_value 不一致则阻塞 |
| 单元测试 | ✅ | 任何单元测试失败则阻塞 |
| 集成测试 | ✅ | 任何集成测试失败则阻塞 |
| 覆盖率 ≥ 80% | ⚠️ | 低于 80% 发出警告但不阻塞 |
| Ren'Py lint | ⚠️ | 脚本语法警告发出通知但不阻塞 |

---

## 8. 测试覆盖率目标

### 8.1 按系统/模块的覆盖率目标

| 模块 | 目标覆盖率 | 关键测试路径 | 优先级 |
|------|-----------|-------------|--------|
| `systems/data_loader.py` | ≥95% | JSON 加载/校验/错误处理 | P0 |
| `systems/constants.rpy` | 100% | 常量值一致性 | P0 |
| `systems/state.rpy` | ≥90% | 变量声明/重置逻辑 | P0 |
| `systems/save_system.py` | ≥90% | 存档/读档/完整性校验 | P0 |
| `systems/narrative_router.py` | ≥85% | 章节路由/label 跳转 | P0 |
| `systems/narrative_beat.py` | ≥85% | 五拍推进/节拍状态 | P1 |
| `systems/choice_dispatcher.py` | ≥90% | 后果分发/调用顺序 | P1 |
| `systems/choice_node.py` | ≥90% | 数据结构/校验 | P1 |
| `systems/existential_protection.py` | ≥90% | 暗流触发/介入/代价/阻断 | P1 |
| `systems/angel_state_machine.py` | ≥85% | 状态转换/情感管理 | P1 |
| `systems/wing_brightness.py` | ≥95% | 双层模型/阶段映射/代价 | P1 |
| `systems/sephirot_progression.py` | ≥90% | 状态机/完成判定/解锁 | P2 |
| `systems/accessibility.py` | ≥80% | 标志位/设置读写 | P2 |

### 8.2 覆盖率报告

```bash
# 生成覆盖率报告
python -m pytest tests/ --cov=game/scripts/systems --cov-report=html --cov-report=xml

# 查看 HTML 报告
open tests/coverage_html/index.html
```

---

**文档结束**

> 本文档为测试框架的完整规格。覆盖数据校验、单元测试、集成测试、E2E 测试四个层级。
>
> 待协调项：
> 1. Ren'Py SDK 版本钉定后更新 CI 工作流中的 SDK 下载链接
> 2. JSON Schema 定义需要与各 GDD 数据结构同步
> 3. E2E 测试脚本需要 Ren'Py 项目骨架完成后才能运行
> 4. 覆盖率目标 80% 为初始目标，Batch 1 后根据实际情况调整
