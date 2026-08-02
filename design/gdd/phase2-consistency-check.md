# Phase 2 跨GDD一致性审查

> **审查者**：游承峰（主理人）
>
> **审查范围**：5份系统设计文档
> - `system-decomposition.md`（系统拆解）
> - `angel-companionship-gdd.md`（天使陪伴系统）
> - `choice-system-gdd.md`（选择系统）
> - `sephirot-progression-gdd.md`（质点进程系统）
> - `existential-protection-gdd.md`（存在保护机制）
>
> **日期**：2026-08-02
>
> **判定**：⚠️ **CONCERNS** — 6/8项通过，2项需在Phase 3技术搭建阶段解决

---

## 审查明细

### 1. 章节映射一致性 ✅ PASS

strategist-2 发现任务描述中的章节-质点对应关系与 `game-concept.md` 不一致，正确地以概念文档为权威源。

**概念文档映射**（已确认权威）：
- Ch 4 = 自我/融爱（Phase 2 试炼起点）
- Ch 8 = 胜利/启明（Phase 2 中段）
- Ch 13 = 真我/心爱的（Phase 2 → Phase 3 转折点）

**判定**：两份新GDD均采用概念文档映射，与Phase 1交付物一致。

---

### 2. 核心共享变量一致性 ✅ PASS（有补充建议）

| 共享变量 | 定义方 | 读取方 | 一致性 |
|---------|--------|--------|--------|
| `bond_depth` (0.0-1.0) | 天使陪伴GDD | 选择系统GDD（结局判定 ≥0.6） | ✅ 一致 |
| `angel_response_profile` (4维) | 选择系统GDD | 天使陪伴GDD、质点进程GDD | ✅ 一致 |
| `progress_value` (0.0-1.0) | 选择系统GDD | 质点进程GDD（累加逻辑） | ✅ 一致 |
| `NIHILISM_THRESHOLD = 0.7` | 选择系统GDD | 存在保护GDD | ✅ 一致 |
| `escape_count` (per sephirot) | 质点进程GDD | 存在保护GDD（影响余震） | ✅ 一致 |
| `current_phase` | 质点进程GDD | 天使陪伴GDD、存在保护GDD | ✅ 一致 |
| `completion_type` ("full"/"half") | 质点进程GDD | 天使陪伴GDD（安息场景对话） | ✅ 一致 |

**补充建议**：`angel_emotional_state` 和 `angel_intervention_count` 在两份新GDD中被引用，但天使陪伴GDD的状态模型中未显式定义。建议在Phase 3技术搭建时，由 engineering-lead 在架构文档中统一定义这两个共享变量的归属和生命周期。

---

### 3. 系统接口一致性 ✅ PASS（有实现细节待对齐）

| 接口 | 定义方 | 调用方 | 一致性 |
|------|--------|--------|--------|
| `angel_intervene(undertow_type, intensity_level)` | 天使陪伴GDD | 存在保护GDD | ✅ 签名一致 |
| `get_bond_depth()` | 天使陪伴GDD | 选择系统GDD | ✅ 一致 |
| `add_sephirot_progress(sephirot_id, progress_value)` | 选择系统GDD | 质点进程GDD | ✅ 一致 |
| `apply_wing_dim(amount)` | 天使陪伴GDD | 存在保护GDD | ⚠️ 见下方说明 |

**`apply_wing_dim` 说明**：天使陪伴GDD定义了 `apply_wing_dim(amount)` 接口（范围0.0-0.3），但存在保护GDD在伪代码中直接使用 `wing_brightness -= cost`。这不是逻辑冲突——`apply_wing_dim` 是封装后的接口，内部实现就是 `wing_brightness -= cost`。Phase 3技术搭建时确认封装关系即可。

---

### 4. 翅膀亮度模型 ⚠️ CONCERN — 需Phase 3解决

**冲突描述**：

| 维度 | 天使陪伴GDD（design-strategist） | 存在保护GDD（strategist-2） |
|------|-------------------------------|--------------------------|
| 模型 | 阶段基线 + 临时黯淡 | 连续递减 + Ch16重置 |
| 公式 | `wing_brightness = wing_stage_baseline[wing_stage] - wing_temporary_dim` | `wing_brightness -= cost; max(0.05, wing_brightness)` |
| 恢复 | 临时黯淡场景后恢复 | 无恢复（永久递减） |
| 驱动 | 章节进入时设置阶段基线 | 每次暗流介入计算代价 |

**分析**：这不是不可调和的矛盾，而是两个视角的互补：
- 天使陪伴GDD的"阶段基线"是**叙事驱动的宏观阶段**（对应5个视觉阶段）
- 存在保护GDD的"连续递减"是**系统驱动的微观累积**（每次介入的具体代价）

**建议的调和模型**（供Phase 3技术搭建参考）：
```
wing_brightness_permanent   # 存在保护系统维护，每次介入递减，不恢复
wing_brightness_temporary   # 介入期间的临时额外黯淡，场景后恢复
wing_brightness_displayed = wing_brightness_permanent - wing_brightness_temporary
```

存在保护GDD的代价公式（`BASE_COST × PHASE_MULTIPLIER × INTENSITY_MULTIPLIER × UNDERTOW_MULTIPLIER`）已经非常精确，且有完整的累积示例（Phase 1: 1.0 → Phase 2a: 0.850 → Phase 2b: 0.509 → Phase 3: 0.159 → Ch16: 1.0重置），应作为技术实现的基准。

**判定**：CONCERN — 不阻塞Phase 2交付，但Phase 3技术搭建时必须由 engineering-lead 统一为单一数据模型。

---

### 5. 选择标签系统 ⚠️ CONCERN — 需Phase 3解决

**冲突描述**：

| 维度 | 选择系统GDD | 质点进程GDD |
|------|-----------|-----------|
| 完成判定输入 | `progress_value` (1.0/0.7/0.3) + `texture_tag` | `confrontation_tag` (ENGAGE/ESCAPE/NEUTRAL) |
| 选项数据结构 | 有 `progress_value`、`texture_tag`，无 `confrontation_tag` | 要求选项包含 `confrontation_tag` 字段 |

**分析**：两套标签不是对立的，而是不同抽象层：
- `confrontation_tag` 是**质点完成判定的输入**（ENGAGE=直面→100%，ESCAPE=逃避→第三次50%，NEUTRAL=中性→不推进）
- `progress_value` 是**进度累积的数值**（1.0/0.7/0.3）
- `texture_tag` 是**叙事纹理标签**（影响天使回应和场景细节）

映射关系清晰：
- ENGAGE → `progress_value = 1.0`
- ESCAPE → `progress_value = 0.3`（第三次补齐到1.0）
- NEUTRAL → 不设 `progress_value`，重新选择

**建议**：在Phase 3技术搭建时，将 `confrontation_tag` 添加到选择系统的选项数据结构中，作为 `progress_value` 的上游判定依据。质点进程GDD已给出完整的JSON数据结构示例（含 `confrontation_tag`、`sephirot_id`、`existence_protection_filtered` 字段），可直接采用。

**判定**：CONCERN — 不阻塞Phase 2交付，但Phase 3技术搭建时必须统一选项数据结构。

---

### 6. 三阶段叙事结构一致性 ✅ PASS

| 阶段 | 概念文档 | 质点进程GDD | 存在保护GDD | 天使陪伴GDD | 选择系统GDD |
|------|---------|-----------|-----------|-----------|-----------|
| Phase 1 遗忘 (Ch1-3) | ✅ | ✅ 翅膀无代价 | ✅ 代价倍率0.0 | ✅ 天使哄孩子式 | ✅ |
| Phase 2 试炼 (Ch4-13) | ✅ | ✅ Ch13转折点 | ✅ 代价倍率1.0→1.5 | ✅ 天使平等式 | ✅ |
| Phase 3 真相 (Ch14-16) | ✅ | ✅ Ch14-15无ESCAPE | ✅ 代价倍率2.5 | ✅ 天使遗言式 | ✅ Ch16三选项均ENGAGE |

---

### 7. 存在保护机制完整性 ✅ PASS

8种暗流全部定义完整，每种包含：
- ✅ 精确触发条件（叙事标签 + 关键词）
- ✅ 3级强度（低1-3/中4-6/高7-10）及差异化视觉
- ✅ 天使介入台词模板
- ✅ 翅膀代价倍率（1.0-2.0）
- ✅ 介入类型（gentle/active/forceful/urgent）

特殊处理验证：
- ✅ NIHILISM 是唯一触发"强制天使介入"的暗流
- ✅ HARM_GUIDE 所有强度均使用urgent介入类型，不可跳过，章节可完全跳过
- ✅ Ch 13 全部8种暗流轮番出现但不达临界值
- ✅ Ch 16 暗流不再出现（心爱的不再需要保护）

---

### 8. 质点完成判定逻辑完整性 ✅ PASS

五拍叙事结构（遭遇→挣扎→天使安慰→选择→转化）完整定义：
- ✅ `confrontation_tag` 三种标签的判定逻辑清晰
- ✅ ESCAPE渐进式天使回应（温柔接纳→共享脆弱→代为面对）
- ✅ 时间型卡住机制（5分钟/7分钟 + 3次提示 + 高亮ENGAGE选项）
- ✅ 50%完成的安全处理（视觉差异最小化、不惩罚、不累计）
- ✅ Phase 3特殊处理（Ch14-15无ESCAPE、Ch16全ENGAGE）
- ✅ Ch 13身份选择标签标注（前三个ESCAPE，"我都是"ENGAGE）

---

## 审查结论

### 判定：⚠️ CONCERNS

**通过项（6/8）**：
1. 章节映射一致性
2. 核心共享变量一致性
3. 系统接口一致性
4. 三阶段叙事结构一致性
5. 存在保护机制完整性
6. 质点完成判定逻辑完整性

**关注项（2/8）——需Phase 3技术搭建解决**：
1. **翅膀亮度模型**：天使陪伴GDD的阶段基线模型与存在保护GDD的连续递减模型需统一为单一数据模型。存在保护GDD的代价公式应作为基准。
2. **选择标签系统**：`confrontation_tag` 字段需添加到选择系统GDD的选项数据结构中。质点进程GDD已给出完整JSON示例。

### Phase 3交接要求

1. engineering-lead 在主架构文档中定义统一的翅膀亮度数据模型
2. engineering-lead 在主架构文档中统一选项数据结构（含 `confrontation_tag`）
3. engineering-lead 定义 `angel_emotional_state` 和 `angel_intervention_count` 的归属系统
4. art-director 与存在保护GDD对齐8种暗流×3级=24种视觉状态的实现方案
5. art-director 确认 wing_brightness 连续值到5个视觉阶段的映射方案

### 不阻塞声明

两项CONCERN均为"接口协调"层面的差异，不涉及核心设计逻辑冲突。两份GDD各自的内部逻辑自洽，跨GDD的差异可在Phase 3技术搭建时由 engineering-lead 统一解决。Phase 2系统设计阶段可以交付。
