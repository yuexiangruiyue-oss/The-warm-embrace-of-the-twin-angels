# 架构评审报告 — 《双生天使的拥抱》

| 字段 | 值 |
|---|---|
| 评审版本 | 1.0 |
| 评审者 | 程基岩（技术主程） |
| 日期 | 2025-07-14 |
| 评审范围 | 主架构文档 + ADR-001~004 |
| 评审结论 | **PASS（附注意事项）** |

---

## 1. 评审结论

**整体评定：PASS（附注意事项）**

架构文档完整覆盖了项目需求，两个 Phase 2 CONCERN 均已解决并落地方案。系统分层清晰，接口契约明确，数据驱动设计合理。存在 3 个需关注的事项和 2 个低风险项，均不阻塞开发启动。

| 维度 | 评分 | 说明 |
|---|---|---|
| 需求覆盖度 | ✅ PASS | 8 项技术需求（TR-01~08）全部覆盖 |
| CONCERN 解决 | ✅ PASS | CONCERN 1（翅膀亮度）+ CONCERN 2（选项数据结构）均已解决 |
| 系统分层 | ✅ PASS | 4 层分离（叙事/系统/数据/界面），依赖方向无循环 |
| 接口契约 | ✅ PASS | 6 系统 × ~5 接口/系统 = ~30 个接口明确定义 |
| 状态管理 | ✅ PASS | 共享变量所有权矩阵完整，单一写入权威明确 |
| 数据驱动 | ✅ PASS | JSON 结构定义完整，校验规则明确 |
| 存档系统 | ✅ PASS | Ren'Py 原生机制满足需求，完整性校验已设计 |
| 性能考量 | ⚠️ ATTENTION | 翅膀着色方案需原型验证；暗流高强效果需限制时长 |
| 安全考量 | ✅ PASS | 威胁模型合理，存档完整性校验已设计 |
| 知识缺口 | ⚠️ ATTENTION | 引擎版本参考文档待创建；Steam 集成需原型验证 |

---

## 2. 架构优点

### 2.1 叙事与系统分离清晰

四层架构（叙事层 → 系统层 → 数据层 → 界面层）将"说什么"（Ren'Py 脚本）、"做什么"（Python 系统）、"配置什么"（JSON 数据）、"显示什么"（Screen）彻底分离。文案/策划可独立编辑 `.rpy` 和 JSON，不触碰系统代码。

### 2.2 CONCERN 解决方案优雅

**CONCERN 1（翅膀亮度）**：双层模型（permanent + temporary）不是简单妥协，而是对两个 GDD 设计意图的统一——阶段基线提供叙事结构锚点，连续扣减提供玩家行为反馈。动态下限策略（阶段基线×15%）确保亮度不会偏离叙事弧线太远。

**CONCERN 2（选项数据结构）**：`confrontation_tag` 字段的引入使 C3 和 C4 的数据消费解耦。`confrontation_tag` → `progress_value` 的映射关系明确，且保留了 `progress_value` 独立性供非直面选择使用。冗余设计（两者并存）是有意的，由校验脚本保证一致性。

### 2.3 共享变量所有权矩阵

这是本架构的核心质量保障机制。每个共享变量有且仅有一个所有者，其他系统通过接口读写。这从根本上避免了 Phase 2 CONCERN 类问题的再次发生——任何违反所有权的代码修改在 review 中标记为 BLOCKER。

### 2.4 数据驱动 + 校验工具

JSON 数据驱动 + `tools/validate_data.py` 校验脚本的组合，使数据错误在 CI 阶段就被发现。特别是 `confrontation_tag` 与 `progress_value` 的一致性校验、`narrative_jump` 目标存在性校验、`angel_response_delta` 字段完整性校验，都是针对本项目特定风险设计的。

### 2.5 引擎选择论证充分

ADR-001 对 Ren'Py/Unity/Godot 的比较基于项目实际需求（视觉小说 + 无障碍 + 小团队 + PC/Steam），而非通用引擎排名。拒绝 Unity 和 Godot 的理由具体（过度工程化、无障碍缺失），不是笼统的"不适合"。

---

## 3. 需关注事项

### 3.1 [ATTENTION] 翅膀亮度着色方案需原型验证

**问题**：主架构 §8.2 提出 `im.MatrixColor` 或自定义 shader 实现翅膀动态着色。Ren'Py 的 `im.MatrixColor` 在频繁更新（每帧调整亮度参数）时的性能表现未经验证。

**影响**：如果性能不足，翅膀亮度变化可能卡顿，影响核心视觉体验。

**建议**：在 Batch 1 阶段创建性能测试原型：
- 测试 60 FPS 下 `im.MatrixColor` 每帧更新参数的性能。
- 备选方案 1：预渲染 10-20 个亮度等级的翅膀图片，离散切换。
- 备选方案 2：使用 Ren'Py 的 `Transform.matrixcolor` + 动画过渡。

**优先级**：P1（Batch 1 原型验证）

### 3.2 [ATTENTION] 引擎版本参考文档缺失

**问题**：主架构 §10.2 标记了 3 份引擎参考文档（VERSION.md、STEAM.md、ACCESSIBILITY.md）待创建。开发开始前这些文档的缺失可能导致 API 误用。

**影响**：Ren'Py 8.x 的具体版本差异、Steam 集成配置、无障碍 API 细节未确认，可能导致返工。

**建议**：在 Batch 0 开始前，由技术主程创建 `docs/engine-reference/renpy/VERSION.md`，至少包含：
- 项目钉定的 Ren'Py 版本号
- 关键 API（`im.MatrixColor`、`Screen`、`persistent`、`default`、`init python`）的版本兼容性说明
- 已知的版本特定问题

**优先级**：P0（Batch 0 前完成）

### 3.3 [ATTENTION] 暗流高频触发的平衡性

**问题**：C5 存在保护系统的代价公式（`BASE_COST × PHASE_MULTIPLIER × INTENSITY_MULTIPLIER`）的参数需要在实际游玩中调整。如果暗流触发频率过高或代价过大，翅膀亮度可能过早触底，破坏叙事弧线。

**影响**：玩家体验——翅膀过早暗淡导致后期叙事（Ch15-16 的"几近熄灭"）失去对比冲击力。

**建议**：
- Batch 1 实现 C5 时，将所有代价参数集中到 `data/protection/cost_table.json`，便于 playtest 调参。
- Batch 3 垂直切片（Ch1-3）playtest 时，验证 Phase 1（代价乘数 0.0）和 Phase 2a 起点（乘数 1.0）的体验。
- 预留"全局代价缩放"设置（`global_cost_multiplier`），可在不修改 JSON 的前提下快速调整难度。

**优先级**：P2（Batch 3 playtest 验证）

---

## 4. 低风险项

### 4.1 [LOW RISK] Python @dataclass 序列化兼容性

**问题**：`AngelState` 使用 Python `@dataclass`，依赖 Ren'Py 的 pickle 序列化。虽然 pickle 理论上支持 dataclass，但 Ren'Py 的存档系统可能有特殊处理。

**影响**：存档/读档可能出现序列化错误。

**缓解**：Batch 0 阶段编写存档/读档单元测试，覆盖 `AngelState` 的完整序列化。备选方案：将 `AngelState` 改为纯字典结构。

### 4.2 [LOW RISK] 时间停滞机制实现复杂度

**问题**：C4 Sephirot 系统的"时间停滞"机制（escape_count 达到阈值后激活）的实现细节在 GDD 中描述较模糊。

**影响**：实现时可能遇到边界情况（如时间停滞期间的选择处理、恢复条件等）。

**缓解**：Batch 2 实现 C4 时，先编写详细的设计文档再编码。备选方案：如果时间停滞过于复杂，可简化为"第3次逃避直接触发天使代理完成50%"，不实现真正的"停滞"状态。

---

## 5. GDD 更新需求

以下 GDD 文档需要在开发开始前更新，以与架构文档保持一致：

| GDD | 更新内容 | 优先级 | 负责人 |
|---|---|---|---|
| `angel-companionship-gdd.md` | 翅膀亮度改为双变量模型（permanent + temporary）；`wing_brightness_displayed` 作为计算属性 | P0 | 文策渊（策划）确认 + 程基岩（技术）提供数据结构 |
| `existential-protection-gdd.md` | 翅膀亮度扣减改为双层模型；下限从固定 0.05 改为动态 `wing_stage_baseline[stage] × 0.15` | P0 | 同上 |
| `choice-system-gdd.md` | 选项数据结构新增 `confrontation_tag` 字段；新增 `bond_depth_delta` 字段 | P0 | 同上 |
| `sephirot-progression-gdd.md` | 确认 `confrontation_tag` 与选项数据结构对齐；确认 escape 代理完成度为 0.5 | P1 | 同上 |

---

## 6. 美术-技术接口协调清单

以下事项需要与美术总监（林绘澄）协调，建议在 Batch 1 开始前完成首次对接：

| # | 协调项 | 技术需求规格 | 美术交付物 | 截止时间 |
|---|---|---|---|---|
| 1 | 翅膀基础图 | 每阶段 1 张 PNG（带 alpha 通道），1920×1080 画布，翅膀区域居中。技术侧通过 shader 动态调整亮度，不需要多亮度版本。 | 5 张翅膀基础图（阶段 1-5） | Batch 1 前 |
| 2 | 天使表情集 | 每个情绪状态对应的表情差分图（calm/concerned/grieving/protective/radiant/aching），与基础立绘对齐。 | 6 表情 × 1 基础立绘 = 6 张差分图 | Batch 1 前 |
| 3 | 暗流视觉效果参考 | 3 个强度等级（低/中/高）的暗流视觉参考图，技术侧据此设计 shader 参数。 | 3 张视觉参考图 | Batch 1 前 |
| 4 | UI 元素分层 PSD | angel_overlay、choice_screen、protection_screen 的 UI 元素需分层 PSD，技术侧据此实现 Screen。 | 3 份分层 PSD | Batch 1 前 |
| 5 | 文字大小测试 | 4 级文字大小（small/normal/large/extra_large）在 1920×1080 下的渲染效果，确保不溢出对话框。 | 4 级文字渲染测试图 | Batch 2 前 |
| 6 | CG 图鉴缩略图 | 每个 CG 需要全尺寸 + 缩略图版本，技术侧实现 persistent 解锁机制。 | CG 图片 + 缩略图 | Batch 3 前 |

---

## 7. 评审签字

| 角色 | 姓名 | 评审意见 | 签字 |
|---|---|---|---|
| 技术主程 | 程基岩 | 架构完整，CONCERN 已解决，可启动 Batch 0 开发 | ✅ |
| 主理人 | 游承峰 | （待确认） | ⬜ |
| 美术总监 | 林绘澄 | （待确认美术-技术接口） | ⬜ |
| 策划 | 文策渊 | （待确认 GDD 更新需求） | ⬜ |

---

*本评审报告与主架构文档、ADR-001~004、control-checklist.md 共同构成完整的技术架构交付物。*
