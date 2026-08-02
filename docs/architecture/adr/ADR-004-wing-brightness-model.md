# ADR-004: 翅膀亮度统一模型 — 双层模型

| 字段 | 值 |
|---|---|
| ADR 编号 | 004 |
| 标题 | 翅膀亮度模型统一：阶段基线 vs 连续扣减 |
| 状态 | ACCEPTED |
| 日期 | 2025-07-14 |
| 决策者 | 程基岩（技术主程） |
| 关联文档 | `design/gdd/angel-companionship-gdd.md`、`design/gdd/existential-protection-gdd.md`、`design/gdd/phase2-consistency-check.md` CONCERN 1 |
| 解决 | Phase 2 一致性检查 CONCERN 1 |

## 上下文

### 冲突描述

Phase 2 一致性检查发现两个 GDD 对翅膀亮度使用了互相冲突的数据模型：

**C2 天使陪伴 GDD（阶段基线模型）：**

```python
wing_stage_baseline = {1: 1.00, 2: 0.85, 3: 0.65, 4: 0.35, 5: 0.15}
wing_brightness = wing_stage_baseline[wing_stage] - wing_temporary_dim
```

- 翅膀亮度由**当前阶段的基线值**减去**临时暗淡值**决定。
- 阶段基线是固定的，由章节进度决定。
- 只有 `wing_temporary_dim` 是动态的，且是临时的。
- 含义：翅膀亮度主要由叙事阶段决定，存在保护只是临时影响。

**C5 存在保护 GDD（连续扣减模型）：**

```python
wing_brightness -= cost
wing_brightness = max(0.05, wing_brightness)
# cost = BASE_COST × PHASE_MULTIPLIER × INTENSITY_MULTIPLIER
```

- 翅膀亮度由**连续扣减**暗流代价决定。
- 没有阶段基线概念，只有绝对下限 0.05。
- 扣减是永久的（除非叙事重置）。
- 含义：翅膀亮度由玩家行为（暗流触发）累积决定。

### 冲突影响

| 问题 | 影响 |
|---|---|
| 翅膀亮度的**初始值**是什么？ | C2 说阶段基线，C5 说上一帧的值减去 cost |
| 存在保护代价是**永久的还是临时的**？ | C2 说临时（`wing_temporary_dim`），C5 说永久（`-=`） |
| 翅膀亮度有**下限**吗？ | C2 说阶段基线（间接下限），C5 说 0.05（绝对下限） |
| **谁拥有**翅膀亮度的写入权？ | C2 和 C5 都在写，违反单一所有权原则 |

### C5 累积曲线与 C2 阶段基线的对齐分析

C5 GDD 提供的累积曲线关键点：`1.0 → 0.850 → 0.509 → 0.159 → 1.0（重置）`

C2 GDD 的阶段基线：`{1: 1.00, 2: 0.85, 3: 0.65, 4: 0.35, 5: 0.15}`

| 叙事位置 | C5 累积曲线值 | C2 阶段基线 | 对齐情况 |
|---|---|---|---|
| Phase 1 起点 | 1.000 | 阶段 1: 1.00 | ✅ 完全一致 |
| Phase 2a 起点 | 0.850 | 阶段 2: 0.85 | ✅ 完全一致 |
| Phase 2b 中点 | 0.509 | 阶段 3-4 之间: 0.65→0.35 | ⚠️ 近似，C5 是动态过程值 |
| Phase 3 终点 | 0.159 | 阶段 5: 0.15 | ✅ 基本一致（0.159 ≈ 0.15） |
| 叙事重置 | 1.000 | 重置: 1.00 | ✅ 完全一致 |

**结论**：两个模型描述的是同一个叙事曲线，只是粒度不同。C2 的阶段基线是"结构性锚点"（每阶段的起始值），C5 的累积曲线是"动态过程"（阶段内的扣减轨迹）。两者可以统一。

## 备选方案

### 方案 A：仅用阶段基线模型（采用 C2 方案）

- 存在保护代价只影响 `wing_temporary_dim`，场景结束恢复。
- 翅膀亮度完全由叙事阶段决定，玩家行为无永久影响。

**劣势**：存在保护失去意义；无法实现 C5 累积曲线；与 C5 GDD 设计意图冲突。

### 方案 B：仅用连续扣减模型（采用 C5 方案）

- 存在保护代价永久扣减翅膀亮度。
- 没有阶段基线概念。

**劣势**：失去叙事结构锚点；翅膀阶段失去意义；与 C2 GDD 设计意图冲突；亮度可能过早触底。

### 方案 C：双层模型（永久层 + 临时层）✅ 选择

```python
wing_brightness_displayed = max(0.05, wing_brightness_permanent - wing_brightness_temporary)
```

- `wing_brightness_permanent`：阶段基线初始化，C5 代价永久扣减（在阶段内），阶段切换时重置为新基线。
- `wing_brightness_temporary`：场景内临时暗淡，场景结束恢复。

**优势**：
- **统一两个 GDD**：阶段基线（C2）作为永久层的初始值，连续扣减（C5）在初始值上累减。
- **保留叙事结构**：阶段基线提供结构性锚点，确保翅膀亮度跟随叙事弧线。
- **保留存在保护意义**：永久扣减使玩家行为有长期影响（阶段内），C5 系统完整生效。
- **实现 C5 累积曲线**：阶段基线 + 连续扣减 = 累积曲线的自然产出。
- **支持叙事重置**：Ch16 可重置 `wing_brightness_permanent` 为 1.0，象征觉醒。
- **所有权清晰**：C5 拥有写入权，C2 仅在阶段切换时通过 C5 接口重置。

## 决策

**选择方案 C：双层模型（永久层 + 临时层）。**

### 决策理由

1. **解决 CONCERN 1 的根本矛盾**：两个 GDD 描述的是同一叙事曲线的不同方面。双层模型将"阶段结构"（C2）和"动态过程"（C5）统一到一个模型中，各司其职。

2. **保留两个系统的设计意图**：C2 的 5 阶段翅膀演化和阶段基线得以保留；C5 的存在保护代价机制完整生效。

3. **所有权清晰**：C5 ProtectionSystem 是翅膀亮度（permanent + temporary）的唯一所有者。C2 AngelSystem 通过 C5 暴露的 `update_wing_stage()` 接口在阶段切换时重置 permanent 层。

4. **叙事重置点自然实现**：Ch16 的叙事重置只需将 `wing_brightness_permanent` 设为 1.0。

### 代价下限策略

原 C5 GDD 使用固定下限 `max(0.05, wing_brightness)`。双层模型中，永久层下限改为动态：

```python
floor = wing_stage_baseline[wing_stage] * 0.15
wing_brightness_permanent = max(floor, wing_brightness_permanent)
```

| 翅膀阶段 | 阶段基线 | 动态下限（基线×15%） | 绝对下限 |
|---|---|---|---|
| 1 | 1.00 | 0.150 | 0.05 |
| 2 | 0.85 | 0.128 | 0.05 |
| 3 | 0.65 | 0.098 | 0.05 |
| 4 | 0.35 | 0.053 | 0.05 |
| 5 | 0.15 | 0.023 → 被 0.05 截断 | 0.05 |

**设计意图**：
- 动态下限确保翅膀亮度不会因过度扣减而远低于阶段基线，保留叙事需要的"最低存在感"。
- 绝对下限 0.05 作为硬底线仍然生效（通过 `max(0.05, displayed)` 保证）。
- 阶段 5 的动态下限（0.023）被绝对下限（0.05）截断，确保最低亮度可见。

### 临时层规则

```python
# 临时暗淡增加
wing_brightness_temporary += temp_cost
# 临时暗淡不能使显示亮度低于绝对下限
wing_brightness_temporary = min(
    wing_brightness_permanent - 0.05,
    wing_brightness_temporary
)
# 场景结束恢复
def recover_temporary_dim():
    wing_brightness_temporary = 0.0
```

**临时层用途**：高强度暗流（7-10）的即时视觉冲击。暗流触发时，除了永久扣减代价外，额外施加临时暗淡，增强视觉反馈。场景结束后临时暗淡恢复，但永久代价保留。

### 完整计算流程

```
暗流触发（C5.trigger_undertow）
  │
  ├── 1. 计算永久代价
  │     cost = BASE_COST × PHASE_MULTIPLIER × INTENSITY_MULTIPLIER
  │     floor = wing_stage_baseline[wing_stage] × 0.15
  │     wing_brightness_permanent -= cost
  │     wing_brightness_permanent = max(floor, wing_brightness_permanent)
  │
  ├── 2. 计算临时暗淡（仅高强度暗流）
  │     if intensity >= 7:
  │         temp_cost = cost × 0.5  # 临时暗淡为永久代价的 50%
  │         wing_brightness_temporary += temp_cost
  │         wing_brightness_temporary = min(
  │             wing_brightness_permanent - 0.05,
  │             wing_brightness_temporary
  │         )
  │
  ├── 3. 计算显示亮度
  │     wing_brightness_displayed = max(0.05,
  │         wing_brightness_permanent - wing_brightness_temporary)
  │
  └── 4. 天使介入（C2.angel_intervene）
        → 更新 angel_emotional_state
        → 选择介入对话
        → angel_intervention_count += 1

场景结束（C1 调用 C5.recover_temporary_dim）
  └── wing_brightness_temporary = 0.0
      → wing_brightness_displayed = max(0.05, wing_brightness_permanent)

翅膀阶段切换（C4 完成 → C2.update_wing_stage）
  ├── wing_stage = new_stage
  ├── wing_brightness_permanent = wing_stage_baseline[new_stage]
  ├── wing_brightness_temporary = 0.0
  └── wing_cost_accumulated = 0.0

Ch16 叙事重置
  ├── wing_brightness_permanent = 1.0
  ├── wing_brightness_temporary = 0.0
  └── nihilism_risk = 0.0
```

## 后果

### 正面后果

- CONCERN 1 彻底解决：两个 GDD 的翅膀亮度模型统一为单一数据模型。
- 翅膀亮度所有权清晰：C5 是唯一所有者，C2 通过接口操作。
- 叙事弧线得到保障：阶段基线确保亮度跟随叙事结构。
- 存在保护有意义：永久扣减使玩家行为有长期影响。
- 视觉反馈丰富：临时层提供即时视觉冲击，永久层提供长期叙事弧线。

### 负面后果

- 实现复杂度增加：需要管理两个变量及其交互规则。
- 需要严格测试：阶段切换、场景结束、Ch16 重置等边界场景需要充分测试。
- 代价平衡需要 playtest：永久扣减的速率需要通过 playtest 调整。

### GDD 更新要求

本 ADR 被接受后，以下 GDD 需要更新以保持一致：

| GDD | 更新内容 |
|---|---|
| `angel-companionship-gdd.md` | 将 `wing_brightness` 单变量替换为 `wing_brightness_permanent` + `wing_brightness_temporary` 双变量；`wing_brightness_displayed` 作为计算属性 |
| `existential-protection-gdd.md` | 将 `wing_brightness -= cost; max(0.05, ...)` 替换为双层模型扣减逻辑；下限从固定 0.05 改为动态 `wing_stage_baseline[stage] × 0.15`（绝对下限 0.05 保留） |

## 验证里程碑

| 里程碑 | 验证内容 | 时间点 |
|---|---|---|
| M1 | 双层模型实现完成，单元测试覆盖所有边界场景 | Batch 1 |
| M2 | 阶段切换时亮度重置正确 | Batch 2 |
| M3 | C5 累积曲线（1.0→0.85→0.5→0.15→1.0）在 playtest 中复现 | Batch 3 |
| M4 | 高强度暗流临时暗淡 + 场景恢复正确 | Batch 3 |

---

*本 ADR 解决 Phase 2 一致性检查 CONCERN 1。与主架构文档 §6 对应。*
