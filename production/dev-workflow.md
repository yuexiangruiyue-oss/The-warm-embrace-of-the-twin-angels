# 开发工作流

> **The Embrace of the Twin Angels** — Development Workflow
>
> 产出者：程基岩（engineering-lead）
>
> 日期：2026-08-02
>
> 依赖文档：`production/epics/epic-breakdown.md`、`docs/architecture/control-checklist.md`、`docs/architecture/main-architecture.md`

---

## 目录

1. [Git 分支策略](#1-git-分支策略)
2. [提交规范](#2-提交规范)
3. [Code Review 规则](#3-code-review-规则)
4. [Definition of Done](#4-definition-of-done)
5. [版本号方案](#5-版本号方案)
6. [Story 实现流程](#6-story-实现流程)
7. [冲刺节奏](#7-冲刺节奏)

---

## 1. Git 分支策略

### 1.1 分支模型

采用简化的 Git Flow 模型，适合小团队（1-3 人）开发：

```
main ────────────────────────────────────────────────────────►
  │                          ↑               ↑
  │                       release/v0.1    release/v0.2
  │                          ↑               ↑
  └─ develop ───────────────────────────────────────────────►
       │         ↑         ↑         ↑
       │    feature/E3.1  feature/E4.2  feature/E5.3
       │         │         │         │
       └─ feature/E0.1 ───┘         │
                    │                │
                    └─ PR ──► develop
```

### 1.2 分支命名规范

| 分支类型 | 命名格式 | 示例 | 生命周期 |
|---------|---------|------|---------|
| 主分支 | `main` | `main` | 永久 |
| 集成分支 | `develop` | `develop` | 永久 |
| 功能分支 | `feature/E{Epic}.{Story}-{slug}` | `feature/E3.1-choice-data-structure` | 合并后删除 |
| 发布分支 | `release/v{MAJOR}.{MINOR}.{PATCH}` | `release/v0.1.0` | 合并后删除 |
| 热修复 | `hotfix/v{MAJOR}.{MINOR}.{PATCH}` | `hotfix/v0.1.1` | 合并后删除 |

### 1.3 分支保护规则

| 分支 | 保护规则 |
|------|---------|
| `main` | 禁止直接推送；只接受 PR；需 ≥1 review approve；CI 必须通过 |
| `develop` | 禁止直接推送；只接受 PR；CI 必须通过 |
| `feature/*` | 可直接推送；无 review 要求（建议自审） |

### 1.4 合并策略

- `feature/*` → `develop`：**Squash Merge**（压缩为一个提交，保持 develop 历史干净）
- `develop` → `main`：**Merge Commit**（保留集成分支记录，便于追溯）
- `release/*` → `main`：**Merge Commit** + **Tag**
- `hotfix/*` → `main` + `develop`：**Merge Commit**（同时修复两个分支）

---

## 2. 提交规范

### 2.1 提交格式

所有提交消息遵循 Conventional Commits 格式：

```
type(scope): 简短描述

[可选正文：详细说明]

[可选脚注：关联 Story ID / GDD / ADR]
```

### 2.2 提交类型（type）

| 类型 | 用途 | 示例 |
|------|------|------|
| `feat` | 新功能实现 | `feat(c5): implement undertow trigger engine` |
| `fix` | Bug 修复 | `fix(c2): wing brightness dynamic floor calculation` |
| `refactor` | 重构（不改变行为） | `refactor(c3): extract choice validation to separate function` |
| `test` | 新增或修改测试 | `test(c4): add sephirot completion tests` |
| `docs` | 文档变更 | `docs(arch): update ADR-004 with implementation notes` |
| `chore` | 构建/工具/依赖 | `chore(infra): update CI to use Python 3.11` |
| `style` | 格式/风格（不改逻辑） | `style(c1): fix indentation in narrative_beat.rpy` |

### 2.3 作用域（scope）

| 作用域 | 对应系统/模块 |
|--------|-------------|
| `c1` | C1 叙事引擎 |
| `c2` | C2 天使陪伴系统 |
| `c3` | C3 选择系统 |
| `c4` | C4 质点进程系统 |
| `c5` | C5 存在保护机制 |
| `c6` | C6 存档系统 |
| `data` | 数据层（JSON） |
| `ui` | 界面层（Screen） |
| `infra` | 基础设施（CI/Git/工具） |
| `arch` | 架构文档 |
| `a11y` | 可访问性 |

### 2.4 提交消息示例

```
feat(c5): implement 8 undertow type definitions and trigger engine

- Add undertow_definitions.json with all 8 undertow types
- Implement ExistentialProtection.trigger_undertow() method
- Add intensity mapping (1-3→low, 4-6→mid, 7-10→high)
- HARM_GUIDE triggers urgent intervention with no delay

Refs: Story E4.1, GDD:C5-§2.1, ADR-004
```

```
fix(c2): correct wing brightness dynamic floor calculation

The dynamic floor was using a fixed 0.05 minimum instead of
the stage-based baseline × 0.15. Updated to use
WING_STAGE_BASELINE[stage] * 0.15 as the floor, with 0.05
as the absolute minimum.

Refs: Story E5.2, ADR-004
```

### 2.5 提交粒度

- **一个提交 = 一个逻辑变更**：不要在一个提交中混合多个无关变更
- **Story 关联**：每个提交消息脚注标注关联的 Story ID
- **可回溯**：通过 `git log --grep="Story E4.1"` 可找到某个 Story 的所有提交
- **频率**：建议每天至少提交一次到功能分支（即使 WIP）

---

## 3. Code Review 规则

### 3.1 Review 触发条件

| 场景 | 是否需要 Review | 审核者 |
|------|----------------|--------|
| `feature/*` → `develop` PR | ✅ 需要 | team-lead 或另一名开发者 |
| `develop` → `main` PR | ✅ 需要 | team-lead |
| `hotfix/*` → `main` PR | ✅ 需要 | team-lead |
| `feature/*` 分支内提交 | ❌ 不需要 | 自审即可 |

### 3.2 Review 检查表

按 `control-checklist.md` 的 Code Review 检查表执行：

#### 3.2.1 架构一致性（A1-A5）

| 编号 | 检查项 | 要求 |
|------|--------|------|
| A1 | 系统依赖方向 | 无循环依赖，符合 ADR-003 依赖方向图 |
| A2 | 层次分离 | 叙事层不直接调用界面层；系统层不直接操作 Screen |
| A3 | 接口契约 | 系统间调用通过定义的接口，不直接访问内部属性 |
| A4 | 数据驱动 | 叙事内容/选择/暗流定义在 JSON 中，非硬编码 |
| A5 | 引擎一致性 | 使用 Ren'Py 8.x API，不使用已废弃 API |

#### 3.2.2 数据一致性（D1-D5）

| 编号 | 检查项 | 要求 |
|------|--------|------|
| D1 | confrontation_tag ↔ progress_value | ENGAGE→1.0, ESCAPE→0.3, NEUTRAL→0.0 |
| D2 | narrative_jump 目标存在 | 所有 jump 目标指向已定义的 label |
| D3 | angel_response_delta 完整性 | 四维字段（warmth/depth/protectiveness/vulnerability）齐全 |
| D4 | JSON Schema 合规 | 所有 JSON 文件通过 Schema 校验 |
| D5 | 质点-章节映射 | 16 质点与 16 章节一一对应 |

#### 3.2.3 翅膀亮度（W1-W6）

| 编号 | 检查项 | 要求 |
|------|--------|------|
| W1 | 双层模型使用 | 使用 permanent/temporary 双层，不直接覆盖 |
| W2 | 动态下限 | displayed ≥ max(基线×15%, 0.05) |
| W3 | 阶段重置 | 阶段切换时 permanent 重置为新基线 |
| W4 | temporary 清零 | 场景结束时 clear_temporary_dim() 被调用 |
| W5 | Ch16 重置 | Ch16 调用 reset_for_ch16() |
| W6 | 代价公式 | 使用 BASE_COST × PHASE_MULT × INTENSITY_MULT × UNDERTOW_MULT |

#### 3.2.4 状态管理（S1-S6）

| 编号 | 检查项 | 要求 |
|------|--------|------|
| S1 | 变量所有权 | 共享变量仅由所有者系统写入 |
| S2 | after_load 钩子 | 读档后完整性校验和状态恢复正确 |
| S3 | persistent 正确使用 | 跨周目数据用 persistent，存档级用 default |
| S4 | 新游戏重置 | 新游戏时 default 重置，persistent 保留 |
| S5 | 变量范围钳制 | wing_brightness ∈ [0.05, 1.0]，chapter ∈ [1, 16] |
| S6 | 禁止操作 P1-P10 | 对照禁止操作清单无违反 |

#### 3.2.5 测试（T1-T4）

| 编号 | 检查项 | 要求 |
|------|--------|------|
| T1 | 先写测试 | Story 实现前先写验收标准对应测试 |
| T2 | 关键路径覆盖 | 翅膀亮度、选择分发、暗流触发、质点判定有测试 |
| T3 | CI 通过 | lint + 数据校验 + 单元测试 + 集成测试全绿 |
| T4 | 覆盖率 | 新增代码覆盖率 ≥ 80% |

### 3.3 Review 流程

```
1. 开发者创建 PR → 填写 PR 描述（关联 Story ID、变更摘要、测试结果）
2. 审核者检查 → 按 3.2 检查表逐项审核
3. 反馈 → 审核者在 PR 中评论，标记 BLOCKER / SUGGESTION / NIT
4. 修改 → 开发者根据反馈修改，推送新提交
5. 批准 → 审核者 approve
6. 合并 → Squash Merge 到 develop
```

### 3.4 Review 标记

| 标记 | 含义 | 处理 |
|------|------|------|
| **BLOCKER** | 必须修改才能合并 | 开发者必须修改 |
| **SUGGESTION** | 建议修改但不阻塞 | 开发者可选择是否修改 |
| **NIT** | 小问题（拼写/格式） | 开发者可选择是否修改 |
| **QUESTION** | 需要讨论 | 在 PR 中回复讨论 |

---

## 4. Definition of Done

### 4.1 Story 级 DoD

一个 Story 被视为"完成"需要满足以下**全部**条件：

| # | 条件 | 验证方法 |
|---|------|---------|
| 1 | 代码实现完成 | 所有 Story 描述中的功能已实现 |
| 2 | 验收标准全部满足 | 逐条对照 Story 的验收标准，每条 ✅ |
| 3 | 先写测试 | 验收标准对应的测试用例已编写且通过 |
| 4 | CI 通过 | lint + 数据校验 + 单元测试 + 集成测试全绿 |
| 5 | 覆盖率达标 | 新增代码覆盖率 ≥ 80% |
| 6 | Code Review 通过 | 至少 1 人 approve，无未解决 BLOCKER |
| 7 | 禁止操作清单检查 | 对照 P1-P10 无违反 |
| 8 | 变量所有权检查 | 新增/修改的变量所有权正确 |
| 9 | GDD/ADR 引用完整 | 代码注释/提交消息标注关联的 GDD 章节/ADR |
| 10 | 测试证据路径留存 | 在 Story 文件中记录测试文件路径 |

### 4.2 Epic 级 DoD

一个 Epic 被视为"完成"需要满足以下条件：

| # | 条件 |
|---|------|
| 1 | Epic 下所有 Story 完成（或明确移除） |
| 2 | Epic 级集成测试通过 |
| 3 | Epic 交接检查项全部通过（参见 `epic-breakdown.md` 的 Batch 交接检查） |
| 4 | 文档更新完成（如涉及架构/GDD 变更） |

### 4.3 Batch 级 DoD

| # | 条件 |
|---|------|
| 1 | Batch 下所有 Epic 完成 |
| 2 | Batch Exit 检查清单全部通过（参见 `batch0-skeleton.md`） |
| 3 | 全量集成测试通过 |
| 4 | 可玩验证通过（Batch 目标场景可走通） |

---

## 5. 版本号方案

### 5.1 语义化版本

采用 SemVer 格式：`MAJOR.MINOR.PATCH`

| 版本段 | 含义 | 何时递增 |
|--------|------|---------|
| MAJOR | 存档格式不兼容变更 | 存档数据结构变更导致旧存档无法读取 |
| MINOR | 新功能/新内容 | 每个 Batch 完成时 |
| PATCH | Bug 修复 | 热修复后 |

### 5.2 版本号与 Batch 映射

| Batch | 版本号范围 | 说明 |
|-------|-----------|------|
| Batch 0 | v0.1.0 | 骨架 + C1 + C6 可运行 |
| Batch 1 | v0.2.0 | C3 + C5 + C2 核心系统可玩 |
| Batch 2 | v0.3.0 | C4 + 集成 + 可访问性 |
| Batch 3 | v1.0.0 | 完整可发布游戏 |

### 5.3 版本标记

- **Git Tag**：每个版本在 `main` 分支打 tag：`v0.1.0`、`v0.2.0` 等
- **options.rpy**：`config.version` 字段同步更新
- **存档兼容**：`config.script_version` 递增表示存档格式变更

### 5.4 预发布版本

| 标记 | 含义 | 示例 |
|------|------|------|
| `-alpha` | 内部测试 | `v0.1.0-alpha.1` |
| `-beta` | 外部测试 | `v0.3.0-beta.1` |
| `-rc` | 发布候选 | `v1.0.0-rc.1` |

---

## 6. Story 实现流程

### 6.1 从 TaskList 到代码

```
TaskUpdate(status=in_progress)
    │
    ▼
1. 读 Story 文件 → 理解需求、验收标准、依赖
    │
    ▼
2. 读相关 GDD / ADR / 控制清单
    │
    ▼
3. 创建功能分支：git checkout -b feature/E{X.Y}-{slug}
    │
    ▼
4. 先写测试（验证驱动开发）
   - 编写验收标准对应的测试用例
   - 运行测试确认全部 FAIL（因为还没实现）
    │
    ▼
5. 实现代码
   - 按编码标准编写（CC-§3）
   - 按变量所有权矩阵声明变量（CC-§4）
   - 按数据驱动原则分离数据与逻辑（ADR-002）
    │
    ▼
6. 运行测试确认全部 PASS
   - 单元测试
   - 集成测试（如涉及跨系统）
   - 数据校验（如涉及 JSON）
    │
    ▼
7. 自审 Code Review 检查表
   - 对照 A1-A5, D1-D5, W1-W6, S1-S6, T1-T4
    │
    ▼
8. 提交 + 推送 + 创建 PR
   - 遵循提交规范
   - PR 描述含 Story ID、变更摘要、测试结果
    │
    ▼
9. Code Review
   - 根据反馈修改
   - 获得 approve
    │
    ▼
10. Squash Merge → develop
    │
    ▼
11. 删除功能分支
    │
    ▼
12. TaskUpdate(status=completed)
    │
    ▼
13. 检查 TaskList → 认领下一个 Story
```

### 6.2 Story 实现检查点

每个 Story 实现过程中需回答以下问题：

| # | 问题 | 如果"否" |
|---|------|---------|
| 1 | 验收标准是否清晰可测试？ | 回问 team-lead / design-strategist 澄清 |
| 2 | 是否有 GDD 需求可追溯？ | 标记知识缺口，回问主理人 |
| 3 | 是否先写了测试？ | 补写测试，不要跳过 |
| 4 | 是否遵循变量所有权矩阵？ | 修正，确保所有者正确 |
| 5 | 是否有禁止操作（P1-P10）？ | 修正，不要违反 |
| 6 | JSON 数据是否通过校验？ | 修正数据，运行 validate_data.py |
| 7 | 是否标注了 GDD/ADR 引用？ | 在代码注释和提交消息中标注 |
| 8 | 测试是否全部通过？ | 不要在测试失败时标记 Story 完成 |

### 6.3 知识诚实原则

按角色定位中的"知识诚实"要求：

- **引擎 API 不确定时标记缺口**：不臆造 Ren'Py 8.x API。如果不确定某个 API 是否存在或如何使用，在代码中标记 `# TODO: 需验证 API — {API名}` 并在 Story 完成报告中列出。
- **GDD 需求不明确时回问**：不要基于猜测实现。如果 GDD 描述模糊，回问 design-strategist / 文策渊。
- **架构决策变更时更新 ADR**：如果在实现过程中发现需要偏离 ADR，不要默默偏离——先创建新的 ADR 或更新现有 ADR，再按新决策实现。

---

## 7. 冲刺节奏

### 7.1 冲刺长度

| 阶段 | 冲刺长度 | 理由 |
|------|---------|------|
| Batch 0 | 1 个冲刺（~2 周） | 16 Story，~36 人日，2 人并行 |
| Batch 1 | 1 个冲刺（~2 周） | 16 Story，~43 人日，2 人并行 |
| Batch 2 | 1 个冲刺（~2.5 周） | 9 Story，~30 人日，含集成测试 |
| Batch 3 | 2 个冲刺（~5 周） | 13 Story，~66 人日，含内容制作 |

### 7.2 每日节奏

| 时段 | 活动 |
|------|------|
| 开始 | 检查 TaskList，认领/继续 Story |
| 开发 | 实现 → 测试 → 提交 |
| 结束 | 推送到功能分支，检查 CI 结果 |

### 7.3 冲刺节奏

| 活动 | 频率 | 参与者 |
|------|------|--------|
| TaskList 检查 | 每日 | 全员 |
| PR Review | 按需 | team-lead 或另一名开发者 |
| 冲刺规划 | 每个 Batch 开始 | 全员 |
| 冲刺回顾 | 每个 Batch 结束 | 全员 |
| Batch Exit 检查 | 每个 Batch 结束 | engineering-lead + team-lead |

### 7.4 并行工作策略

Batch 0-2 期间（系统实现阶段），建议按系统边界并行分配：

| 开发者 1 | 开发者 2 | 并行条件 |
|---------|---------|---------|
| Epic 0（骨架）+ Epic 1（C6） | Epic 2（C1） | 无依赖冲突 |
| Epic 3（C3） | Epic 4（C5）+ Epic 5（C2） | C3 依赖 C5（过滤），但可先实现 C3 核心 |
| Epic 6（C4）+ Epic 7（可访问性） | 集成测试 + Bug 修复 | C4 依赖 C3+C5，需等 Batch 1 完成 |

Batch 3 期间（内容制作阶段），建议按章节范围并行：

| 开发者 1 | 开发者 2 |
|---------|---------|
| Ch1-4 叙事脚本 | Ch5-8 叙事脚本 |
| Ch9-13 叙事脚本 | Ch14-16 叙事脚本 |
| 音频集成 + 翅膀着色 | UI/UX + Steam 集成 |

### 7.5 阻塞与升级

| 场景 | 处理 |
|------|------|
| Story 依赖的前置 Story 未完成 | 标记 blocked，在 TaskList 中设置 addBlockedBy |
| GDD 需求不明确 | 回问 design-strategist / 文策渊，通过 SendMessage 通知 team-lead |
| 引擎 API 不确定 | 标记 `# TODO: 需验证 API`，在 Story 报告中列出 |
| 美术资产未就绪 | 使用占位资产，标记 `# TODO: 替换美术资产` |
| 性能问题 | 先记录 Profile 数据，不在当前 Story 中优化，创建新 Story |

---

**文档结束**

> 本文档为开发工作流的完整规范。覆盖 Git 分支策略、提交规范、Code Review 规则、Definition of Done、版本号方案、Story 实现流程和冲刺节奏。
>
> 待协调项：
> 1. GitHub 仓库创建和分支保护规则配置（需主理人审批）
> 2. 冲刺长度需根据实际团队规模和可用时间调整
> 3. Code Review 审核者角色需在团队中明确分配
> 4. 版本号方案需与 Steam 发布节奏对齐
