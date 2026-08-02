# Epic / Story 拆分文档

> **The Embrace of the Twin Angels** — Epic Breakdown
>
> 产出者：程基岩（engineering-lead）
>
> 日期：2026-08-02
>
> 依赖文档：`design/gdd/system-decomposition.md`、`design/gdd/*-gdd.md`（5份GDD）、`docs/architecture/main-architecture.md`、`docs/architecture/adr/ADR-001~004.md`、`docs/architecture/control-checklist.md`、`docs/architecture/architecture-review.md`

---

## 目录

1. [拆分原则与约定](#1-拆分原则与约定)
2. [Batch 分层总览](#2-batch-分层总览)
3. [Epic 0: 项目骨架与基础设施](#epic-0-项目骨架与基础设施)
4. [Epic 1: C6 存档系统](#epic-1-c6-存档系统)
5. [Epic 2: C1 叙事引擎](#epic-2-c1-叙事引擎)
6. [Epic 3: C3 选择系统](#epic-3-c3-选择系统)
7. [Epic 4: C5 存在保护机制](#epic-4-c5-存在保护机制)
8. [Epic 5: C2 天使陪伴系统](#epic-5-c2-天使陪伴系统)
9. [Epic 6: C4 质点进程系统](#epic-6-c4-质点进程系统)
10. [Epic 7: 可访问性系统](#epic-7-可访问性系统)
11. [Epic 8: UI/UX 实现](#epic-8-uiux-实现)
12. [Epic 9: 内容制作与打磨](#epic-9-内容制作与打磨)
13. [跨 Epic 依赖矩阵](#13-跨-epic-依赖矩阵)
14. [Story 复杂度统计](#14-story-复杂度统计)

---

## 1. 拆分原则与约定

### 1.1 Epic 划分依据

Epic 按**系统拆解优先级**（`system-decomposition.md`）+ **架构分层**（`main-architecture.md`）划分：

| Epic | 对应系统/领域 | 系统优先级 | 架构层 |
|------|-------------|-----------|--------|
| Epic 0 | 项目骨架 + 基础设施 | P0（前置） | 全层 |
| Epic 1 | C6 存档系统 | P0 | 系统层 + 数据层 |
| Epic 2 | C1 叙事引擎 | P0 | 叙事层 + 系统层 |
| Epic 3 | C3 选择系统 | P1 | 系统层 + 数据层 + 界面层 |
| Epic 4 | C5 存在保护机制 | P1 | 系统层 + 数据层 + 界面层 |
| Epic 5 | C2 天使陪伴系统 | P1 | 系统层 + 数据层 + 界面层 |
| Epic 6 | C4 质点进程系统 | P1 | 系统层 + 数据层 |
| Epic 7 | 可访问性系统 | P2 | 界面层 + 系统层 |
| Epic 8 | UI/UX 实现 | P2 | 界面层 |
| Epic 9 | 内容制作与打磨 | P3 | 全层 |

### 1.2 Story 字段约定

每个 Story 包含以下字段：

| 字段 | 说明 |
|------|------|
| **Story ID** | 格式 `E{Epic}.{序号}`，如 `E0.1` |
| **标题** | 简洁的动词短语 |
| **描述** | 具体要做什么，关联的 GDD 章节 / ADR / 控制清单条目 |
| **验收标准** | 可测试的检查项列表 |
| **依赖** | 前置 Story ID 列表（空 = 无前置依赖） |
| **复杂度** | S（≤1人日）/ M（2-3人日）/ L（4-6人日）/ XL（7+人日） |
| **所属 Batch** | 0 / 1 / 2 / 3 |

### 1.3 GDD 需求可追溯性

每个 Story 的描述中标注关联的 GDD 需求 ID 和 ADR 指引：

- `[GDD:C1-§3.2]` = 天使陪伴系统 GDD 第 3.2 节
- `[GDD:C3-§4.1]` = 选择系统 GDD 第 4.1 节
- `[GDD:C4-§2.3]` = 质点进程系统 GDD 第 2.3 节
- `[GDD:C5-§2.1]` = 存在保护机制 GDD 第 2.1 节
- `[GDD:C6-§3.1]` = 存档系统 GDD 第 3.1 节（如有）
- `[ADR-001]` = 引擎选择决策记录
- `[ADR-002]` = JSON 数据驱动决策记录
- `[ADR-003]` = 系统通信模式决策记录
- `[ADR-004]` = 翅膀亮度双层模型决策记录
- `[CC-§3]` = 控制清单第 3 节（编码标准）

---

## 2. Batch 分层总览

| Batch | 范围 | 目标 | 完成 Exit 标准 |
|-------|------|------|---------------|
| **Batch 0** | 项目骨架 + 数据层 + C1 叙事引擎 + C6 存档系统 | 可运行最小原型：能加载 JSON 数据、路由到章节、存档/读档 | Ch1 骨架章节可从开始到结束完整走通，存档恢复正确 |
| **Batch 1** | C3 选择系统 + C5 存在保护 + C2 天使陪伴 | 三大核心系统可玩 | Ch1-3 垂直切片：选择→后果→暗流→天使介入→翅膀变化 完整链路可走通 |
| **Batch 2** | C4 质点进程 + 系统集成 + 可访问性 | 全系统联动 + 无障碍 | Ch1-8 可玩，质点完成判定 + 五拍叙事 + 时间卡住 + 可访问性设置全部生效 |
| **Batch 3** | 16 章叙事内容 + UI/UX + 音频 + 打磨 | 完整可发布游戏 | 16 章全部可玩，3 种结局可达成，Steam 集成就绪 |

### Batch 0 → Batch 1 交接检查

- [ ] C1 章节路由可工作（label 跳转 + 叙事标签系统）
- [ ] C6 存档/读档 + persistent 变量管理正确
- [ ] JSON 数据层骨架 + 加载器 + 校验脚本可工作
- [ ] options.rpy 基础配置完成
- [ ] CI 流水线可运行 lint + typecheck + test

### Batch 1 → Batch 2 交接检查

- [ ] C3 选择→后果分发链路完整（含 `confrontation_tag` 映射）
- [ ] C5 暗流触发→天使介入→翅膀代价→画面恢复链路完整
- [ ] C2 天使状态机 + 翅膀亮度双层模型 + 互动机制可工作
- [ ] 三系统通过共享变量所有权矩阵正确协同

### Batch 2 → Batch 3 交接检查

- [ ] C4 五拍叙事 + 完成判定 + 时间卡住 + 解锁链 完整
- [ ] 6 大系统（C1-C6）通过集成测试
- [ ] 可访问性 4 级标志位全系统生效
- [ ] 翅膀亮度着色方案原型验证通过

---

## Epic 0: 项目骨架与基础设施

> **Batch: 0** | **系统优先级: P0（前置）**
>
> 目标：搭建 Ren'Py 8.x 项目目录结构、Git 仓库、CI 流水线、JSON 数据层骨架、基础配置。

### Story E0.1: Ren'Py 项目初始化与目录结构

| 字段 | 内容 |
|------|------|
| **Story ID** | E0.1 |
| **标题** | 初始化 Ren'Py 项目与目录结构 |
| **描述** | 按照 `main-architecture.md` §3.1 的目录结构创建 Ren'Py 项目。创建 `game/scripts/`（叙事层）、`game/scripts/systems/`（系统层）、`game/data/`（数据层子目录）、`game/gui/`（界面层）、`game/images/`、`game/audio/` 目录。创建 `game/options.rpy` 基础配置文件。[ADR-001] 确认 Ren'Py 8.x 版本。 [CC-§3] 遵循通用编码标准。 |
| **验收标准** | 1. 项目可在 Ren'Py SDK 中打开无报错；2. 目录结构与架构文档 §3.1 完全一致；3. `options.rpy` 包含窗口标题、分辨率 1920×1080、版本号字段；4. 存在 `.gitignore` 文件排除 `*.rpyc`、`*.pyc`、`saves/`；5. 存在 `README.md` 说明项目结构与启动方式 |
| **依赖** | 无 |
| **复杂度** | S |
| **所属 Batch** | 0 |

### Story E0.2: Git 仓库初始化与分支策略

| 字段 | 内容 |
|------|------|
| **Story ID** | E0.2 |
| **标题** | 初始化 Git 仓库与分支策略 |
| **描述** | 初始化 Git 仓库，配置 `.gitignore`、`.gitattributes`（处理换行符）。建立分支策略：`main`（稳定）、`develop`（集成）、`feature/E{X.Y}-{slug}`（功能分支）、`release/v{X.Y.Z}`（发布分支）。建立提交规范：`feat(scope):`、`fix(scope):`、`refactor(scope):`、`test(scope):`、`docs(scope):`、`chore(scope):`。参见 `dev-workflow.md`。 |
| **验收标准** | 1. Git 仓库已初始化；2. `.gitignore` 排除 `saves/`、`*.rpyc`、`*.pyc`、`__pycache__/`、`.env`；3. `main` 和 `develop` 分支存在；4. `CONTRIBUTING.md` 包含分支策略和提交规范；5. 首次提交记录存在 |
| **依赖** | E0.1 |
| **复杂度** | S |
| **所属 Batch** | 0 |

### Story E0.3: JSON 数据层骨架与加载器

| 字段 | 内容 |
|------|------|
| **Story ID** | E0.3 |
| **标题** | 实现 JSON 数据层骨架与通用加载器 |
| **描述** | 按 [ADR-002] 数据驱动决策，创建 `game/data/` 下的 JSON 数据目录骨架：`data/sephirot/`、`data/choices/`、`data/angel/`、`data/protection/`、`data/endings/`。实现通用 JSON 加载器 `systems/data_loader.py`：`load_json(path)` → dict，`load_all(directory)` → dict[str, dict]。实现 JSON Schema 校验框架 `tools/validate_data.py`（基础结构校验）。[GDD:C4-§4] [GDD:C3-§4] 参考各 GDD 的数据结构定义。 |
| **验收标准** | 1. `data/` 下 5 个子目录存在，各含一个 `_template.json` 模板文件；2. `data_loader.py` 可加载任意 JSON 文件并返回 dict；3. 文件不存在时抛出 `DataLoadError`（含文件路径信息）；4. `validate_data.py` 可校验模板文件的结构；5. 单元测试覆盖加载器和校验器（≥90% 行覆盖率） |
| **依赖** | E0.1 |
| **复杂度** | M |
| **所属 Batch** | 0 |

### Story E0.4: 核心常量与枚举定义

| 字段 | 内容 |
|------|------|
| **Story ID** | E0.4 |
| **标题** | 定义核心常量与枚举 |
| **描述** | 在 `game/scripts/systems/constants.rpy` 中定义项目所有常量和枚举：Phase 枚举（FORGETTING/TRIAL_EARLY/TRIAL_LATE/TRUTH）、SephirotState 枚举（LOCKED/ACTIVE/COMPLETED_FULL/COMPLETED_HALF）、ConfrontationTag 枚举（ENGAGE/ESCAPE/NEUTRAL）、UndertowCode 枚举（8 种暗流代码）、AngelEmotionalState 枚举（calm/aching/resolute/sorrowful/tender）、WingStage 常量（1-5）、`WING_BRIGHTNESS_MIN = 0.05`、`NIHILISM_THRESHOLD = 0.7`、`BASE_COST = 0.02`、Phase 乘数表、阶段基线表。参见 `main-architecture.md` §7 常量速查表。 |
| **验收标准** | 1. 所有枚举和常量在 `constants.rpy` 中定义；2. 常量值与 GDD 和架构文档一致；3. 枚举值可被 `init python` 块中的类引用；4. 存在常量值一致性单元测试 |
| **依赖** | E0.1 |
| **复杂度** | S |
| **所属 Batch** | 0 |

### Story E0.5: 变量所有权基座与 default 声明

| 字段 | 内容 |
|------|------|
| **Story ID** | E0.5 |
| **标题** | 声明 default 变量与 persistent 变量 |
| **描述** | 按 `main-architecture.md` §6 变量所有权矩阵，在 `game/scripts/systems/state.rpy` 中声明所有 `default` 变量（存档级）和 `persistent` 变量（跨周目级）。每个变量标注所有者系统、读取者、生命周期、重置时机。包括：`wing_brightness_permanent`、`wing_brightness_temporary`、`bond_depth`、`current_chapter`、`current_sephirot_id`、`current_phase`、`angel_emotional_state`、`angel_intervention_count`、`undertow_state`、`sephirot_states`、`escape_counts`、`choice_history` 等。参见 `control-checklist.md` 禁止操作清单 P1-P10。 |
| **验收标准** | 1. 所有共享变量在 `state.rpy` 中声明，带注释标注所有权；2. 无重复声明；3. `persistent` 变量有 `after_load` 重置逻辑；4. 代码审查确认无跨所有者直接修改（对照禁止操作清单 P1-P10） |
| **依赖** | E0.4 |
| **复杂度** | M |
| **所属 Batch** | 0 |

### Story E0.6: CI 流水线搭建

| 字段 | 内容 |
|------|------|
| **Story ID** | E0.6 |
| **标题** | 搭建 CI 流水线 |
| **描述** | 配置 GitHub Actions CI 流水线（`.github/workflows/ci.yml`）：(1) Python 3 lint（ruff/flake8）→ (2) Ren'Py 脚本语法检查 → (3) JSON 数据校验（`python tools/validate_data.py`）→ (4) 单元测试（`python -m pytest tests/`）→ (5) 构建可玩包（Ren'Py SDK 打包）。在 `requirements-dev.txt` 中固定开发依赖版本。 |
| **验收标准** | 1. CI 在 `develop` 分支推送和 PR 时自动触发；2. lint 失败会阻止合并；3. JSON 校验失败会阻止合并；4. 单元测试失败会阻止合并；5. CI 在 5 分钟内完成 |
| **依赖** | E0.1, E0.3 |
| **复杂度** | M |
| **所属 Batch** | 0 |

---

## Epic 1: C6 存档系统

> **Batch: 0** | **系统优先级: P0**
>
> 目标：实现存档槽位管理、翅膀亮度持久化、质点进度持久化、跨周目 persistent 变量管理。
>
> **GDD 参考**：`main-architecture.md` §6（状态管理）、§7（存档系统）
> **ADR 参考**：ADR-002（数据驱动）
> **控制清单**：CC-§4（状态管理 S1-S6）

### Story E1.1: 存档槽位管理

| 字段 | 内容 |
|------|------|
| **Story ID** | E1.1 |
| **标题** | 实现存档槽位管理与自动存档 |
| **描述** | 基于 Ren'Py 原生存档系统实现：6 个手动槽位 + 3 个自动槽位（auto-1/auto-2/auto-3）+ 快速存档/读档（Q.Save / Q.Load）。每个槽位存储缩略图（当前画面截图）、章节号、质点 ID、翅膀亮度阶段、时间戳。实现 `SaveLoad` 类暴露 `save(slot)`、`load(slot)`、`get_slot_info(slot)` 接口。利用 Ren'Py 的 `$ renpy.save(slot)` 和 `$ renpy.load(slot)` 原生 API。[ADR-002] 确保存档数据结构与 JSON 数据层兼容。 |
| **验收标准** | 1. 6 个手动槽位可独立存档/读档；2. 自动存档在每章开始时触发（auto-1）和每质点完成时触发（auto-2）；3. 槽位缩略图正确显示当前画面；4. 槽位信息显示章节号 + 时间戳 + 翅膀阶段；5. 空槽位显示"空"占位符；6. 存档/读档不丢失任何 default 变量 |
| **依赖** | E0.1, E0.5 |
| **复杂度** | M |
| **所属 Batch** | 0 |

### Story E1.2: 翅膀亮度持久化

| 字段 | 内容 |
|------|------|
| **Story ID** | E1.2 |
| **标题** | 实现翅膀亮度双层模型持久化 |
| **描述** | 按 [ADR-004] 双层模型，持久化 `wing_brightness_permanent` 和 `wing_brightness_temporary` 两个变量。`permanent` 随存档保存，恢复时保持当前值。`temporary` 在场景结束时恢复为 0（`clear_temporary_dim()`）。实现 `get_wing_brightness_displayed()` 计算属性：`max(WING_BRIGHTNESS_MIN, permanent - temporary)`。在 `after_load` 钩子中恢复翅膀亮度并通知天使陪伴系统更新视觉。[CC-§4] S1-S2 变量所有权确认。 |
| **验收标准** | 1. 存档时 `wing_brightness_permanent` 正确保存；2. 读档后 `permanent` 值恢复正确；3. `temporary` 在场景结束时清零；4. `displayed` 计算结果 ≥ `WING_BRIGHTNESS_MIN`（0.05）；5. `after_load` 后天使翅膀视觉与亮度值对应；6. 阶段切换时 `permanent` 重置为新基线 |
| **依赖** | E0.5 |
| **复杂度** | M |
| **所属 Batch** | 0 |

### Story E1.3: 质点进度持久化

| 字段 | 内容 |
|------|------|
| **Story ID** | E1.3 |
| **标题** | 实现质点状态与进度持久化 |
| **描述** | 持久化 `sephirot_states` 字典（16 质点的 LOCKED/ACTIVE/COMPLETED_FULL/COMPLETED_HALF 状态）、`escape_counts` 字典（每个质点的逃避次数）、`choice_history` 列表（全部选择记录含 choice_id、option_id、confrontation_tag、时间戳）。这些数据随 Ren'Py 存档保存。实现 `get_sephirot_progress_summary()` 返回当前进度摘要（供存档界面显示）。[GDD:C4-§3] [ADR-002] |
| **验收标准** | 1. 存档/读档后 16 质点状态完全恢复；2. 逃避计数正确恢复；3. 选择历史完整保留；4. `get_sephirot_progress_summary()` 返回正确摘要（完成数/总数/当前质点）；5. 新游戏时所有质点重置为 LOCKED |
| **依赖** | E0.5 |
| **复杂度** | M |
| **所属 Batch** | 0 |

### Story E1.4: persistent 跨周目变量管理

| 字段 | 内容 |
|------|------|
| **Story ID** | E1.4 |
| **标题** | 实现跨周目 persistent 变量管理 |
| **描述** | 管理跨周目数据：`persistent.endings_seen`（已达成结局列表）、`persistent.cg_unlocked`（已解锁 CG 列表）、`persistent.total_playthroughs`（总周目数）、`persistent.sephirot_completion_records`（各质点历史完成类型记录）、`persistent.first_playthrough`（是否首次游玩）。实现 `after_load` 和 `new_game` 钩子：新游戏时重置 default 变量但保留 persistent 变量。实现 `check_first_playthrough()` 和 `unlock_ending(ending_code)` 接口。[GDD:C6] |
| **验收标准** | 1. 新游戏后 persistent 变量不重置；2. 二周目可访问已解锁 CG 和结局列表；3. `first_playthrough` 在首次游玩为 True，之后为 False；4. 结局达成后 `endings_seen` 正确追加；5. `after_load` 钩子正确恢复 default + persistent 状态 |
| **依赖** | E0.5, E1.1 |
| **复杂度** | M |
| **所属 Batch** | 0 |

### Story E1.5: 存档数据完整性校验

| 字段 | 内容 |
|------|------|
| **Story ID** | E1.5 |
| **标题** | 实现存档数据完整性校验 |
| **描述** | 实现存档数据校验机制：在 `after_load` 时检查所有必要的 default 变量是否存在（防止旧版本存档缺少新变量）。缺失变量以默认值填充并记录警告日志。实现 `validate_save_integrity()` 函数：检查 `wing_brightness_permanent` 范围 [0.05, 1.0]、`current_chapter` 范围 [1, 16]、`sephirot_states` 键完整性。对损坏存档显示"存档已损坏"提示并拒绝加载。参见 `architecture-review.md` §4.1 @dataclass 序列化兼容性风险缓解。 |
| **验收标准** | 1. 读取缺少新变量的旧存档时，缺失变量以默认值填充；2. 范围越界的变量被钳制到有效范围；3. 严重损坏的存档被拒绝加载并显示提示；4. 校验日志写入 `game/log/integrity.log`；5. 单元测试覆盖正常存档、缺失变量存档、损坏存档三种场景 |
| **依赖** | E1.1, E1.2, E1.3 |
| **复杂度** | M |
| **所属 Batch** | 0 |

---

## Epic 2: C1 叙事引擎

> **Batch: 0** | **系统优先级: P0**
>
> 目标：实现章节路由、叙事标签系统、五拍叙事结构框架、章节切换、最小可玩 Ch1 骨架。
>
> **GDD 参考**：`sephirot-progression-gdd.md` §5（Ren'Py 脚本组织）
> **ADR 参考**：ADR-002（数据驱动叙事）
> **控制清单**：CC-§3（叙事层编码标准）

### Story E2.1: 章节路由系统

| 字段 | 内容 |
|------|------|
| **Story ID** | E2.1 |
| **标题** | 实现章节路由与 label 跳转系统 |
| **描述** | 按 [GDD:C4-§5] 的 label 组织方式，实现章节路由：`label ch01_sephirot_01:` → `label ch02_sephirot_02:` → ... → `label ch16_sephirot_16:`。在 `systems/narrative_router.py` 中实现 `NarrativeRouter` 类：`route_to_chapter(chapter_id)` 根据 `current_chapter` 跳转到对应 label。实现 `get_current_narrative_context()` 返回当前章节 ID、质点 ID、Phase。label 命名规范：`ch{NN}_sephirot_{NN}_{pinyin}`。参见 `main-architecture.md` §5.1 系统接口。 |
| **验收标准** | 1. `route_to_chapter(1)` 跳转到 `ch01_sephirot_01` label；2. 章节号 1-16 全部可路由；3. 无效章节号抛出 `InvalidChapterError`；4. 路由时正确更新 `current_chapter` 和 `current_sephirot_id`；5. 跳转后调用 C6 通知存档系统触发自动存档 |
| **依赖** | E0.4, E0.5 |
| **复杂度** | M |
| **所属 Batch** | 0 |

### Story E2.2: 叙事标签系统

| 字段 | 内容 |
|------|------|
| **Story ID** | E2.2 |
| **标题** | 实现叙事标签注册与查询系统 |
| **描述** | 实现叙事标签系统：在叙事脚本中通过 `$ set_narrative_tag("identity_shame")` 注册当前活跃的叙事标签。`systems/narrative_tags.py` 维护一个 `active_narrative_tags` 集合。提供 `has_tag(tag)` / `get_active_tags()` / `clear_tags()` 接口。标签用于驱动 C5 暗流触发（如 `identity_shame` → SHAME_LOOP）和 C2 天使对话池检索。参见 `existential-protection-gdd.md` §2.1 各暗流的触发条件。 |
| **验收标准** | 1. `set_narrative_tag("xxx")` 后 `has_tag("xxx")` 返回 True；2. 场景切换时标签自动清除（`clear_tags()` 被调用）；3. 多标签可同时活跃；4. C5 可通过 `has_tag` 查询触发条件；5. C2 可通过 `get_active_tags()` 检索对话池 |
| **依赖** | E0.5 |
| **复杂度** | S |
| **所属 Batch** | 0 |

### Story E2.3: 五拍叙事结构框架

| 字段 | 内容 |
|------|------|
| **Story ID** | E2.3 |
| **标题** | 实现五拍叙事结构（ENCOUNTER→STRUGGLE→COMFORT→CHOICE→TRANSFORM） |
| **描述** | 按 [GDD:C4-§2] 五拍叙事结构，实现叙事节拍框架。在叙事脚本中通过 `$ narrative_beat = "ENCOUNTER"` 等标记当前节拍。每拍的系统调用约定：①ENCOUNTER（纯叙事，无系统调用）→ ②STRUGGLE（C5 暗流触发：`$ trigger_undertow(code, intensity)`）→ ③COMFORT（C5 天使介入：自动触发）→ ④CHOICE（C3 选择呈现：`$ present_choice(choice_id)`）→ ⑤TRANSFORM（C4 进度更新 + 章节过渡检查）。实现 `advance_beat()` 接口推进节拍。在 `systems/narrative_beat.py` 中实现 `NarrativeBeatManager` 类。 |
| **验收标准** | 1. 五个节拍可按顺序推进；2. ②STRUGGLE 时 `trigger_undertow` 被调用（如叙事脚本指定）；3. ④CHOICE 时选择界面呈现；4. ⑤TRANSFORM 时质点进度更新；5. 节拍顺序不可跳过（②不可在①之前）；6. `advance_beat()` 在 TRANSFORM 后自动检查是否进入下一质点 |
| **依赖** | E2.1, E2.2 |
| **复杂度** | L |
| **所属 Batch** | 0 |

### Story E2.4: 章节切换与过渡逻辑

| 字段 | 内容 |
|------|------|
| **Story ID** | E2.4 |
| **标题** | 实现章节切换、Phase 切换、标题卡过渡 |
| **描述** | 实现章节过渡逻辑：(1) 质点完成 → 触发 TRANSFORM 节拍 → 调用 `complete_sephirot()` → 解锁下一质点 → 路由到下一章节。(2) Phase 切换检测：Ch3→Ch4（FORGETTING→TRIAL_EARLY）、Ch8→Ch9（TRIAL_EARLY→TRIAL_LATE）、Ch13→Ch14（TRIAL_LATE→TRUTH）。Phase 切换时通知 C5 更新代价乘数、通知 C2 更新天使行为模式。(3) 章节标题卡：每章开始时显示章节标题卡 3 秒后淡出。(4) Ch16 特殊处理：通知 C5 `disable_for_final_chapter()`。参见 `existential-protection-gdd.md` §7.1 和 `sephirot-progression-gdd.md` §3。 |
| **验收标准** | 1. 质点完成后自动路由到下一章节；2. Phase 切换时正确更新 `current_phase` 并通知 C5/C2；3. 章节标题卡正确显示并自动淡出；4. Ch16 时 C5 存在保护正确关闭；5. 新章节开始时清除余震（`clear_afterimages_for_new_chapter()`） |
| **依赖** | E2.1, E2.3 |
| **复杂度** | M |
| **所属 Batch** | 0 |

### Story E2.5: Ch1 骨架章节（最小可玩验证）

| 字段 | 内容 |
|------|------|
| **Story ID** | E2.5 |
| **标题** | 实现 Ch1（王国/白花）骨架章节 |
| **描述** | 实现 Ch1 完整骨架章节作为 Batch 0 的可玩验证。Ch1 = 质点 1「王国」，主暗流 EXIST_DENY（低强度 2）。包含：①ENCOUNTER（引入心爱的和天使）→ ②STRUGGLE（EXIST_DENY 低强度触发）→ ③COMFORT（天使 gentle 介入台词）→ ④CHOICE（1 个 ENGAGE + 1 个 ESCAPE 选项）→ ⑤TRANSFORM（质点完成 → 章节切换到 Ch2）。使用占位立绘和占位 BGM。此 Story 的目标是验证 C1+C6 链路完整可走通。[GDD:C5-§7.1] Ch1 映射。 |
| **验收标准** | 1. Ch1 可从开始到结束完整走通（5 拍全部触发）；2. 存档/读档后可从中间节拍恢复；3. 选择 ENGAGE → 质点以 COMPLETED_FULL 完成；4. 选择 ESCAPE → 逃避计数 +1；5. Ch1 结束后正确路由到 Ch2（即使 Ch2 为空骨架）；6. 标题卡「第一章 · 王国」正确显示 |
| **依赖** | E2.1, E2.2, E2.3, E2.4, E1.1, E1.2, E1.3 |
| **复杂度** | L |
| **所属 Batch** | 0 |

---

## Epic 3: C3 选择系统

> **Batch: 1** | **系统优先级: P1**
>
> 目标：实现 choice_node 数据结构、选择界面渲染、选择后果分发器、confrontation_tag 映射。
>
> **GDD 参考**：`choice-system-gdd.md`（全文档）
> **ADR 参考**：ADR-002（数据驱动）、ADR-003（系统通信）
> **控制清单**：CC-§3（系统层编码标准）、CC-§5（数据一致性 D1-D5）

### Story E3.1: choice_node 数据结构与加载

| 字段 | 内容 |
|------|------|
| **Story ID** | E3.1 |
| **标题** | 实现 choice_node 数据结构与 JSON 加载 |
| **描述** | 按 [GDD:C3-§4.1] 和 `main-architecture.md` §5.3 统一选项数据结构，实现 `ChoiceNode` 数据类（Python `@dataclass`）。字段包括：`choice_id`、`sephirot_id`、`prompt_text`、`options` 列表（每个 option 含 `option_id`、`text`、`confrontation_tag`（ENGAGE/ESCAPE/NEUTRAL/null）、`progress_value`、`texture_tag`、`angel_response_delta`（4 维 profile）、`bond_depth_delta`、`narrative_jump`、`existence_protection_filtered`）。实现 `load_choice_node(choice_id)` 从 `data/choices/{chapter}/` 加载 JSON。实现 `validate_choice_option()` 校验函数。参见 `main-architecture.md` §5.3 和 `choice-system-gdd.md` §4.1。 |
| **验收标准** | 1. `ChoiceNode` 可从 JSON 正确加载所有字段；2. `confrontation_tag` 与 `progress_value` 一致性校验通过（ENGAGE→1.0, ESCAPE→0.3, NEUTRAL→0.0）；3. `narrative_jump` 目标存在性校验通过；4. `angel_response_delta` 四维字段完整性校验通过；5. 单元测试覆盖正常/缺失字段/不一致数据三种场景 |
| **依赖** | E0.3, E0.4 |
| **复杂度** | M |
| **所属 Batch** | 1 |

### Story E3.2: 选择界面渲染

| 字段 | 内容 |
|------|------|
| **Story ID** | E3.2 |
| **标题** | 实现选择界面 Screen 与渲染逻辑 |
| **描述** | 在 `gui/choice_screen.rpy` 中实现选择界面 Screen。根据 `ChoiceNode.options` 动态生成选项按钮。每个选项显示 `text` 内容。选项按钮使用项目 UI 风格（紫色/金色主题）。实现选项悬停效果和点击反馈。处理选项数量动态布局（2-4 个选项的布局适配）。实现 `present_choice(choice_id)` 入口函数：加载 ChoiceNode → 渲染 Screen → 等待玩家选择 → 返回 `selected_option_id`。实现 ESCAPE 选项的特殊视觉提示（Phase 1-2 中第 3 次逃避前的高亮提示）。参见 `control-checklist.md` CC-§3 界面层标准。 |
| **验收标准** | 1. 选择界面正确渲染 2-4 个选项；2. 选项文字完整不溢出；3. 悬停效果正确；4. 点击后返回正确的 `option_id`；5. 暗流活跃期间选择界面仍可正常呈现（不阻止选择）；6. 第 3 次 ESCCAPE 时 ENGAGE 选项有高亮提示 |
| **依赖** | E3.1, E0.5 |
| **复杂度** | M |
| **所属 Batch** | 1 |

### Story E3.3: 选择后果分发器

| 字段 | 内容 |
|------|------|
| **Story ID** | E3.3 |
| **标题** | 实现选择后果多系统分发 |
| **描述** | 按 [ADR-003] 直接调用 + 接口契约模式，实现 `ChoiceDispatcher` 类。玩家选择后，分发器按顺序调用：(1) 更新 `choice_history`（C6）→ (2) 调用 `C4.add_sephirot_progress(sephirot_id, progress_value)` → (3) 调用 `C2.update_angel_response(angel_response_delta)` → (4) 更新 `bond_depth`（C2 所有权）→ (5) 通知 `C5.check_nihilism_ending_risk()`（如适用）→ (6) 执行 `narrative_jump`（如存在）。分发器是 C3→C2/C4/C5/C6 的单向调用枢纽。参见 `main-architecture.md` §5.2 核心数据流「选择触发流」。 |
| **验收标准** | 1. 选择后 C4 进度正确更新；2. C2 天使回应 profile 正确更新；3. `bond_depth` 正确修改（C2 所有权）；4. C5 虚无主义风险检查被调用（当选择涉及过滤时）；5. `narrative_jump` 正确跳转；6. 分发顺序符合 ADR-003 依赖方向；7. 单元测试覆盖每种 confrontation_tag 的分发路径 |
| **依赖** | E3.1, E3.2 |
| **复杂度** | L |
| **所属 Batch** | 1 |

### Story E3.4: 存在保护过滤集成

| 字段 | 内容 |
|------|------|
| **Story ID** | E3.4 |
| **标题** | 实现存在保护对选择的过滤逻辑 |
| **描述** | 按 [GDD:C5-§2.4] 和 `choice-system-gdd.md` §5 的过滤规则，实现选择过滤。规则：只过滤虚无主义倾向的选择（NIHILISM 暗流达到 `NIHILISM_THRESHOLD = 0.7` 时）。最终选择（Ch16）不受保护。实现 `filter_choice_options(choice_node, current_undertow_state)` → 过滤后的 options 列表。过滤逻辑：当选项的 `existence_protection_filtered = True` 且当前 NIHILISM 强度 ≥ 0.7 时，该选项被标记为"暂时不可选"（视觉变灰但不移除）。参见 `existential-protection-gdd.md` §2.4。 |
| **验收标准** | 1. NIHILISM 强度 < 0.7 时所有选项可选；2. NIHILISM 强度 ≥ 0.7 且选项 `filtered = True` 时选项变灰；3. 最终选择（Ch16）不受过滤；4. 过滤不影响非虚无主义暗流；5. 被过滤选项仍可见（不移除） |
| **依赖** | E3.1, E3.2, E4.1 |
| **复杂度** | M |
| **所属 Batch** | 1 |

### Story E3.5: 选择数据 JSON 内容骨架

| 字段 | 内容 |
|------|------|
| **Story ID** | E3.5 |
| **标题** | 创建 Ch1-3 选择节点 JSON 数据骨架 |
| **描述** | 在 `data/choices/ch01/`、`ch02/`、`ch03/` 下创建选择节点 JSON 文件骨架。每个质点至少 2 个选择节点（五拍中④CHOICE 节拍）。每个选择节点 2-3 个选项。使用占位文本但数据结构完整正确。供 Batch 1 垂直切片使用。参见 `choice-system-gdd.md` §6（每章选择数量建议）和 §4.1（数据结构）。 |
| **验收标准** | 1. Ch1-3 各含 ≥2 个 choice_node JSON 文件；2. 所有 JSON 通过 `validate_data.py` 校验；3. `confrontation_tag` 与 `progress_value` 一致性校验通过；4. `angel_response_delta` 四维字段完整 |
| **依赖** | E3.1 |
| **复杂度** | S |
| **所属 Batch** | 1 |

---

## Epic 4: C5 存在保护机制

> **Batch: 1** | **系统优先级: P1**
>
> 目标：实现暗流检测引擎、8 种暗流类型、天使介入触发、翅膀代价计算、虚无主义强制阻断。
>
> **GDD 参考**：`existential-protection-gdd.md`（全文档）
> **ADR 参考**：ADR-004（翅膀亮度双层模型）、ADR-003（系统通信）
> **控制清单**：CC-§5（翅膀亮度 W1-W6）

### Story E4.1: 暗流定义数据与触发引擎

| 字段 | 内容 |
|------|------|
| **Story ID** | E4.1 |
| **标题** | 实现 8 种暗流定义数据与触发引擎 |
| **描述** | 按 [GDD:C5-§2.1] 和 §4.1 的暗流通用结构，创建 `data/protection/undertow_definitions.json` 包含全部 8 种暗流定义（SHAME_LOOP/POSS_DENY/PAIN_AMP/HOPE_ERASE/EXIST_DENY/NIHILISM/RAGE_INC/HARM_GUIDE），每种含 3 级强度（low/mid/high）的视觉/音频/持续时间/天使台词。实现 `ExistentialProtection` 类核心方法：`trigger_undertow(code, intensity)` → 添加活跃暗流 → 应用视觉效果 → 根据强度延迟触发天使介入。参见 `existential-protection-gdd.md` §4.3 伪代码。 |
| **验收标准** | 1. 8 种暗流定义 JSON 完整且通过校验；2. `trigger_undertow("SHAME_LOOP", 5)` 正确添加活跃暗流；3. 强度级别映射正确（1-3→low, 4-6→mid, 7-10→high）；4. HARM_GUIDE 触发后立即触发天使介入（无延迟）；5. 其他暗流按强度延迟后触发介入；6. 单元测试覆盖每种暗流触发 |
| **依赖** | E0.3, E0.4, E0.5 |
| **复杂度** | L |
| **所属 Batch** | 1 |

### Story E4.2: 天使介入流程

| 字段 | 内容 |
|------|------|
| **Story ID** | E4.2 |
| **标题** | 实现四种天使介入类型与流程 |
| **描述** | 按 [GDD:C5-§2.2] 实现 4 种介入类型：gentle（低强度，浮动文本）、active（中强度，拥抱动画+正常台词）、forceful（高强度，紧急拥抱+翅膀闪光+慢速台词）、urgent（HARM_GUIDE 全强度，瞬间出现+禁用跳过+慢速台词）。实现 `trigger_angel_intervention(code, intensity)` 方法：确定介入类型 → 天使移动到心爱的 → 播放介入动画 → 呈现台词 → 恢复画面 → 计算翅膀代价 → 记录介入 → 移除活跃暗流+添加余震。HARM_GUIDE 特殊处理：禁用跳过 `config.skipping = False`，台词结束后恢复。参见 `existential-protection-gdd.md` §4.3 `trigger_angel_intervention` 伪代码。 |
| **验收标准** | 1. 4 种介入类型各有正确的视觉/音频表现；2. HARM_GUIDE 全强度使用 urgent 介入；3. urgent 介入期间跳过功能被禁用；4. 介入后画面正确恢复（渐变恢复）；5. 余震正确添加（强度降至 1.5，持续到下一章节）；6. 天使介入次数计数正确更新 |
| **依赖** | E4.1, E5.2 |
| **复杂度** | L |
| **所属 Batch** | 1 |

### Story E4.3: 翅膀代价计算

| 字段 | 内容 |
|------|------|
| **Story ID** | E4.3 |
| **标题** | 实现翅膀代价公式与双层模型扣减 |
| **描述** | 按 [GDD:C5-§2.3] 和 [ADR-004] 实现翅膀代价计算。公式：`cost = BASE_COST × PHASE_MULTIPLIER × INTENSITY_MULTIPLIER × UNDERTOW_MULTIPLIER`。实现 `calculate_wing_cost(code, intensity, intervention_type)` 方法。扣减到 `wing_brightness_permanent`（阶段内永久扣减）。动态下限：`max(wing_stage_baseline[stage] × 0.15, 0.05)`。复合暗流代价叠加（每多一个暗流 +20%）。Phase 1 代价乘数 0.0（免费保护）。实现 `WingCostLedger` 类记录每次介入的代价账本（供调试和叙事回顾）。参见 `existential-protection-gdd.md` §4.4。 |
| **验收标准** | 1. Phase 1 介入代价为 0（翅膀不暗淡）；2. Phase 2a 中强度 SHAME_LOOP 代价 = 0.02 × 1.0 × 1.0 × 1.0 = 0.020；3. Phase 3 高强度 HARM_GUIDE 代价 = 0.02 × 2.5 × 1.5 × 2.0 = 0.150；4. 复合暗流代价正确叠加（2 个暗流 ×1.2 倍）；5. 翅膀亮度不低于动态下限；6. `WingCostLedger` 正确记录每次代价 |
| **依赖** | E4.2, E0.5 |
| **复杂度** | M |
| **所属 Batch** | 1 |

### Story E4.4: 虚无主义强制阻断

| 字段 | 内容 |
|------|------|
| **Story ID** | E4.4 |
| **标题** | 实现虚无主义结局强制阻断机制 |
| **描述** | 按 [GDD:C5-§2.4] 实现虚无主义强制阻断。实现 `check_nihilism_ending_risk(sephirot_state)` 方法：检测连续 3+ 质点 ESCAPE + NIHILISM 反复高强度（≥7）+ 反复拒绝天使（≥3 次）。触发时调用 `trigger_nihilism_forced_intervention()`：画面全黑 → 天使强制介入独白（9 句台词）→ 画面恢复 → 翅膀代价 -0.15 → 标记 `nihilism_warning_triggered = True`（只触发一次）→ 通知 C3 在下一质点调整 ESCAPE 选项为更温和选项。参见 `existential-protection-gdd.md` §4.3 `check_nihilism_ending_risk` 和 `trigger_nihilism_forced_intervention` 伪代码。 |
| **验收标准** | 1. 满足三个条件时强制阻断触发；2. 强制阻断只触发一次（`nihilism_warning_triggered` 标记）；3. 9 句独白台词完整呈现；4. 翅膀代价 -0.15 正确扣减；5. 通知 C3 调整下一质点选项（ESCAPE 替换为温和选项）；6. 不满足条件时不触发 |
| **依赖** | E4.1, E4.3, E3.3 |
| **复杂度** | L |
| **所属 Batch** | 1 |

### Story E4.5: 画面恢复过渡与余震系统

| 字段 | 内容 |
|------|------|
| **Story ID** | E4.5 |
| **标题** | 实现暗流画面恢复过渡与余震管理 |
| **描述** | 按 [GDD:C5-§2.2.3] 和 §3.3 实现画面恢复过渡。实现 `recover_visual(code, level)` 方法：低强度 3 秒恢复、中强度 5 秒恢复、高强度 8 秒恢复、HARM_GUIDE 2 秒恢复。恢复过渡：t=0 暗流视觉效果开始消退 → t=1 消退 50% → t=2 消退 80% → t=3 完全消退 → t=3-8 余震（5% 残留）。每种暗流有独特的恢复特征（SHAME_LOOP 阴天转晴、HOPE_ERASE 色彩从天使扩散等）。实现 `deactivate_undertow(code)` → 移除活跃暗流 + 添加余震。实现 `clear_afterimages_for_new_chapter()` 在新章节清除余震。参见 `existential-protection-gdd.md` §3.3 恢复过渡表。 |
| **验收标准** | 1. 暗流解除后画面正确恢复到正常色调；2. 不同强度的恢复时间正确；3. HARM_GUIDE 恢复最快（2 秒）；4. 余震正确添加并在新章节清除；5. 8 种暗流各有独特的恢复过渡特征 |
| **依赖** | E4.2 |
| **复杂度** | M |
| **所属 Batch** | 1 |

### Story E4.6: Ch 16 关闭序列

| 字段 | 内容 |
|------|------|
| **Story ID** | E4.6 |
| **标题** | 实现 Ch 16 存在保护关闭与翅膀恢复序列 |
| **描述** | 按 [GDD:C5-§7.3] 实现 Ch 16 关闭序列。当 `current_chapter == 16` 时：(1) 清除所有活跃暗流 → (2) 清除所有余震 → (3) `wing_brightness_permanent → 1.0`（叙事驱动重置）→ (4) 标记 `final_choice_unlocked = True` → (5) 天使恢复最美状态（Stage 1 翅膀、平静表情）→ (6) 天使台词"走吧。我准备好了。"→ (7) 最终选择三选项全部呈现，不受过滤。实现 `disable_for_final_chapter()` 方法。参见 `existential-protection-gdd.md` §4.3 `disable_for_final_chapter` 伪代码。 |
| **验收标准** | 1. Ch 16 开始时所有暗流和余震清除；2. 翅膀亮度恢复到 1.0；3. 天使视觉恢复到 Stage 1；4. 最终选择不受存在保护过滤；5. `final_choice_unlocked` 标记正确设置 |
| **依赖** | E4.3, E2.4 |
| **复杂度** | S |
| **所属 Batch** | 1 |

---

## Epic 5: C2 天使陪伴系统

> **Batch: 1** | **系统优先级: P1**
>
> 目标：实现天使存在状态机、翅膀亮度双层模型、互动机制、对话池系统、翅膀阶段进化。
>
> **GDD 参考**：`angel-companionship-gdd.md`（全文档）
> **ADR 参考**：ADR-004（翅膀亮度双层模型）
> **控制清单**：CC-§5（翅膀亮度 W1-W6）

### Story E5.1: 天使存在状态机

| 字段 | 内容 |
|------|------|
| **Story ID** | E5.1 |
| **标题** | 实现 5 种天使存在状态与状态机 |
| **描述** | 按 [GDD:C2-§2] 实现 5 种存在状态：PRESENT（始终在场）、CONCEALED（隐藏但存在）、INTERVENING（介入中）、ABSENT（缺席，Phase 3 特定）、ETERNAL（永恒，Ch 16）。实现 `AngelStateMachine` 类：`get_state()` → 当前状态、`transition_to(new_state)` → 状态切换 + 触发视觉/行为变化。状态转换规则：PRESENT→INTERVENING（暗流触发时）、INTERVENING→PRESENT（介入完成）、PRESENT→CONCEALED（特定叙事）、→ABSENT（Ch 14 特定段落）、→ETERNAL（Ch 16）。参见 `angel-companionship-gdd.md` §2。 |
| **验收标准** | 1. 5 种状态可正确切换；2. 状态转换遵循规则（不可从 ABSENT 直接到 CONCEALED）；3. INTERVENING 状态在暗流触发时正确激活；4. ETERNAL 状态仅在 Ch 16 激活；5. 状态变化触发对应视觉更新 |
| **依赖** | E0.4, E0.5 |
| **复杂度** | M |
| **所属 Batch** | 1 |

### Story E5.2: 翅膀亮度双层模型与阶段进化

| 字段 | 内容 |
|------|------|
| **Story ID** | E5.2 |
| **标题** | 实现翅膀亮度双层模型与 5 阶段视觉进化 |
| **描述** | 按 [ADR-004] 实现双层模型：`wing_brightness_permanent`（阶段基线初始化 → C5 代价永久扣减 → 阶段切换重置）和 `wing_brightness_temporary`（高强度暗流即时效果 → 场景结束恢复）。计算属性：`wing_brightness_displayed = max(动态下限, permanent - temporary)`。阶段基线表：`{1: 1.0, 2: 0.85, 3: 0.65, 4: 0.35, 5: 0.15}`。实现 `on_sephirot_enter(sephirot_id)` → 根据质点阶段设置基线。实现 `get_wing_stage()` → 根据 `permanent` 值返回 1-5 阶段（0.8-1.0→S1, 0.6-0.8→S2, 0.4-0.6→S3, 0.2-0.4→S4, 0.05-0.2→S5）。实现 `apply_wing_dim(amount)` → 扣减 permanent。实现 `clear_temporary_dim()` → 清零 temporary。参见 `main-architecture.md` §8.2 和 `angel-companionship-gdd.md` §3。 |
| **验收标准** | 1. `displayed` 计算结果正确（permanent - temporary，不低于动态下限）；2. 阶段切换时 permanent 重置为新基线；3. `get_wing_stage()` 映射正确；4. `apply_wing_dim(0.15)` 后 permanent 减 0.15；5. `clear_temporary_dim()` 后 temporary = 0；6. 阶段基线值与 GDD 一致 |
| **依赖** | E0.5, E0.4 |
| **复杂度** | L |
| **所属 Batch** | 1 |

### Story E5.3: 天使互动机制

| 字段 | 内容 |
|------|------|
| **Story ID** | E5.3 |
| **标题** | 实现点击天使与寻求拥抱互动 |
| **描述** | 按 [GDD:C2-§3] 实现两种互动机制。(1) 点击天使：30 秒冷却时间，触发天使说一句安慰的话。`angel_advise()` 接口从对话池随机选取台词。(2) 寻求拥抱：空格长按 0.5 秒触发，天使拥抱动画 + 安慰台词。Phase 1-2 每质点 3 次（计数到 3 后提示"天使需要休息"），Phase 3 无限次。活跃暗流期间点击天使可提前触发介入（不减少翅膀代价）。拥抱可轻微缓解暗流（-1 级强度）→ `C5.soft_resolve_undertow(code)`。实现冷却计时器和拥抱次数计数器。参见 `angel-companionship-gdd.md` §3。 |
| **验收标准** | 1. 点击天使后 30 秒内不可再次点击；2. 长按空格 0.5 秒触发拥抱；3. Phase 1-2 每质点拥抱上限 3 次；4. Phase 3 拥抱无限次；5. 活跃暗流时点击天使提前触发介入；6. 拥抱使暗流强度 -1 级；7. 计数器在质点切换时重置 |
| **依赖** | E5.1, E5.4, E4.2 |
| **复杂度** | L |
| **所属 Batch** | 1 |

### Story E5.4: 天使对话池系统

| 字段 | 内容 |
|------|------|
| **Story ID** | E5.4 |
| **标题** | 实现天使对话池三级索引与检索 |
| **描述** | 按 [GDD:C2-§4] 实现对话池三级索引：(1) 按 Phase 索引（FORGETTING/TRIAL_EARLY/TRIAL_LATE/TRUTH），(2) 按 `angel_emotional_state` 索引（calm/aching/resolute/sorrowful/tender），(3) 按 `completion_type` 索引（full/half/none）。创建 `data/angel/dialogue_pool.json` 含骨架对话条目（每 Phase × 每情感 × 每完成类型 ≥ 3 条）。实现 `get_angel_dialogue(phase, emotional_state, completion_type, context_tags)` → 随机选取一条合适台词。实现去重逻辑（同一质点内不重复同一条）。参见 `angel-companionship-gdd.md` §4。 |
| **验收标准** | 1. 三级索引检索返回正确情感和 Phase 的台词；2. 同一质点内不重复同一条台词；3. 无匹配台词时返回兜底台词；4. 对话池 JSON 通过校验；5. `angel_advise()` 调用后返回正确台词 |
| **依赖** | E0.3, E0.4 |
| **复杂度** | M |
| **所属 Batch** | 1 |

### Story E5.5: 天使情感状态管理

| 字段 | 内容 |
|------|------|
| **Story ID** | E5.5 |
| **标题** | 实现 5 种天使情感状态与转换逻辑 |
| **描述** | 按 [GDD:C2-§2.2] 实现 5 种情感状态：calm（平静，Phase 1 默认）、aching（心疼，Phase 2 开始出现）、resolute（坚定，暗流高强度时）、sorrowful（悲伤，翅膀严重暗淡时）、tender（温柔，拥抱/安慰时）。实现 `update_angel_response(angel_response_delta)` → 根据 4 维 profile（warmth/depth/protectiveness/vulnerability）调整情感状态。实现转换规则：Phase 1 以 calm 为主，Phase 2a 引入 aching，Phase 2b 引入 sorrowful，Phase 3 以 resolute + sorrowful 为主。情感状态影响天使立绘表情和对话风格。参见 `angel-companionship-gdd.md` §2.2。 |
| **验收标准** | 1. 5 种情感状态可正确切换；2. `update_angel_response` 根据 profile delta 正确调整；3. Phase 转换时情感状态正确变化；4. 情感状态影响立绘表情选择；5. `angel_emotional_state` 由 C2 独占写入（所有权确认） |
| **依赖** | E5.1, E5.2 |
| **复杂度** | M |
| **所属 Batch** | 1 |

---

## Epic 6: C4 质点进程系统

> **Batch: 2** | **系统优先级: P1**
>
> 目标：实现 SephirotState 状态机、五拍在质点中的实现、完成判定逻辑、时间卡住、解锁链。
>
> **GDD 参考**：`sephirot-progression-gdd.md`（全文档）
> **ADR 参考**：ADR-003（系统通信）
> **控制清单**：CC-§5（数据一致性 D1-D5）

### Story E6.1: SephirotState 状态机

| 字段 | 内容 |
|------|------|
| **Story ID** | E6.1 |
| **标题** | 实现 16 质点状态机与解锁链 |
| **描述** | 按 [GDD:C4-§2] 实现 `SephirotProgression` 类。16 质点初始全为 LOCKED，Ch1 开始时质点 1 设为 ACTIVE。实现 `unlock_next_sephirot(current_id)` → 解锁下一质点。实现 `get_sephirot_state(id)` → LOCKED/ACTIVE/COMPLETED_FULL/COMPLETED_HALF。实现 `complete_sephirot(id, completion_type)` → 设为 COMPLETED_FULL 或 COMPLETED_HALF。质点解锁链严格线性：1→2→3→...→16。双八度结构：Ch1-13 人类八度上行，Ch14-16 神性八度下行。参见 `sephirot-progression-gdd.md` §2 和 §4 伪代码。 |
| **验收标准** | 1. 初始状态 16 质点全 LOCKED；2. `unlock_next_sephirot(1)` 后质点 2 为 ACTIVE；3. `complete_sephirot(1, "full")` 后质点 1 为 COMPLETED_FULL；4. 不可跳过解锁（质点 3 不可能在质点 2 未完成时解锁）；5. 状态持久化正确（存档/读档恢复） |
| **依赖** | E0.5, E1.3 |
| **复杂度** | M |
| **所属 Batch** | 2 |

### Story E6.2: 完成判定逻辑

| 字段 | 内容 |
|------|------|
| **Story ID** | E6.2 |
| **标题** | 实现 ENGAGE/ESCAPE/NEUTRAL 完成判定 |
| **描述** | 按 [GDD:C4-§2.3] 实现完成判定逻辑。`process_choice(confrontation_tag)` → (1) ENGAGE：进度 +1.0 → 质点 COMPLETED_FULL → 解锁下一质点。(2) ESCAPE：进度 +0.3 → 逃避计数 +1 → 第 3 次 ESCAPE 时天使代为面对 → 质点 COMPLETED_HALF（50%完成）→ 解锁下一质点。(3) NEUTRAL：进度 +0.0 → 重新选择。实现 `get_consecutive_escape_count()` 供 C5 虚无主义风险检测使用。Phase 3 特殊处理：Ch14-15 无 ESCAPE 选项，Ch16 三选项全为 ENGAGE。参见 `sephirot-progression-gdd.md` §2.3 完成判定伪代码。 |
| **验收标准** | 1. ENGAGE → 质点 COMPLETED_FULL；2. 3 次 ESCAPE → 质点 COMPLETED_HALF；3. NEUTRAL → 不推进进度；4. 逃避计数正确累计和重置；5. COMPLETED_HALF 视觉差异最小化（不惩罚玩家）；6. Phase 3 无 ESCAPE 选项；7. Ch16 全为 ENGAGE |
| **依赖** | E6.1, E3.3 |
| **复杂度** | L |
| **所属 Batch** | 2 |

### Story E6.3: 时间型卡住机制

| 字段 | 内容 |
|------|------|
| **Story ID** | E6.3 |
| **标题** | 实现时间型卡住检测与渐进提示 |
| **描述** | 按 [GDD:C4-§2.4] 实现时间卡住机制。Phase 1：5 分钟未选择 → 触发提示。Phase 2：7 分钟未选择 → 触发提示。Phase 3：不启用。提示分 3 级递进：(1) 第一级：天使轻声"你还在想吗？没关系，慢慢来"。(2) 第二级（再过 2 分钟）：天使更温柔地引导。(3) 第三级（再过 2 分钟）：高亮 ENGAGE 选项。实现 `check_time_stuck()` 定时检测。参见 `sephirot-progression-gdd.md` §2.4。参见 `architecture-review.md` §4.2 时间停滞复杂度风险评估。 |
| **验收标准** | 1. Phase 1 5 分钟未选择触发第一级提示；2. Phase 2 7 分钟未选择触发第一级提示；3. Phase 3 不触发时间卡住；4. 3 级提示渐进递进；5. 第三级提示高亮 ENGAGE 选项；6. 玩家做出选择后计时器重置 |
| **依赖** | E6.2, E5.4 |
| **复杂度** | M |
| **所属 Batch** | 2 |

### Story E6.4: 质点数据 JSON 骨架

| 字段 | 内容 |
|------|------|
| **Story ID** | E6.4 |
| **标题** | 创建 16 质点 JSON 数据骨架 |
| **描述** | 在 `data/sephirot/` 下创建 16 个质点 JSON 文件（`sephirot_01.json` ~ `sephirot_16.json`）。每个文件包含：`sephirot_id`、`name`（中文名）、`pinyin`、`chapter`（对应章节号）、`phase`、`primary_undertow`（主暗流代码）、`composite_undertows`（复合暗流列表，如有）、`base_intensity`、`intervention_type`、`wing_cost`。数据来自 `existential-protection-gdd.md` §7.1 每章暗流类型映射表。供 Batch 2 集成测试使用。 |
| **验收标准** | 1. 16 个 JSON 文件全部存在且通过校验；2. 暗流映射与 GDD §7.1 一致；3. Phase 标记正确（Ch1-3=FORGETTING, Ch4-8=TRIAL_EARLY, Ch9-13=TRIAL_LATE, Ch14-16=TRUTH）；4. 复合暗流章节（Ch9-12, Ch14）正确标记 |
| **依赖** | E0.3, E4.1 |
| **复杂度** | S |
| **所属 Batch** | 2 |

### Story E6.5: 系统集成测试

| 字段 | 内容 |
|------|------|
| **Story ID** | E6.5 |
| **标题** | 实现 Ch1-8 集成测试（全系统联动验证） |
| **描述** | 实现 Ch1-8 的集成测试场景，验证 6 大系统（C1-C6）全链路联动。测试链路：叙事推进 → 暗流触发 → 天使介入 → 翅膀代价 → 选择呈现 → 后果分发 → 质点完成 → 章节切换。测试覆盖：Phase 1 无代价保护、Phase 2a 翅膀开始暗淡、ESCAPE 三次天使代为面对 50% 完成、虚无主义强制阻断（模拟条件触发）、存档/读档中断恢复。使用 `data/choices/` 和 `data/sephirot/` 的骨架数据。参见 `main-architecture.md` §5.2 核心数据流。 |
| **验收标准** | 1. Ch1-8 全链路可走通无崩溃；2. 翅膀亮度在 Phase 1 保持 1.0；3. Phase 2a 翅膀开始暗淡（0.85→0.70）；4. ESCAPE 三次后 50% 完成；5. 模拟虚无主义条件时强制阻断触发；6. 存档/读档后全系统状态正确恢复；7. 集成测试报告生成 |
| **依赖** | E6.1, E6.2, E6.3, E3.3, E4.4, E5.3 |
| **复杂度** | XL |
| **所属 Batch** | 2 |

---

## Epic 7: 可访问性系统

> **Batch: 2** | **系统优先级: P2**
>
> 目标：实现 4 级全局标志位、字体/速度/色弱/键盘/自动模式、暗流视觉可关闭。
>
> **GDD 参考**：`existential-protection-gdd.md` §8、`angel-companionship-gdd.md` 无障碍章节
> **参考文档**：`docs/architecture/phase3-assembly-review.md` 可访问性-架构对齐

### Story E7.1: 4 级全局无障碍标志位

| 字段 | 内容 |
|------|------|
| **Story ID** | E7.1 |
| **标题** | 实现 4 级全局无障碍标志位系统 |
| **描述** | 实现 4 个全局标志位（persistent 变量）：`low_stim_mode`（低刺激模式）、`visual_undertow_off`（暗流视觉关闭）、`screen_shake_off`（屏幕抖动关闭）、`audio_stable_mode`（音频稳定模式）。在 `state.rpy` 中声明为 persistent 变量（跨周目保持）。实现设置界面读写这些标志位。所有视觉效果系统（C5 暗流、C2 翅膀）和音频系统在渲染前检查标志位。三条不可降级底线：(1) HARM_GUIDE 紧急介入不可关闭、(2) 虚无主义强制阻断不可关闭、(3) 存在保护机制本身不可关闭。参见 `phase3-assembly-review.md` 可访问性-架构对齐。 |
| **验收标准** | 1. 4 个标志位可通过设置界面切换；2. 标志位为 persistent（跨周目保持）；3. `low_stim_mode` 降低所有暗流视觉效果强度；4. `visual_undertow_off` 关闭暗流视觉但保留台词；5. `screen_shake_off` 替换震动为缩放/渐变；6. 三条不可降级底线在任何设置下都生效 |
| **依赖** | E0.5, E4.5 |
| **复杂度** | M |
| **所属 Batch** | 2 |

### Story E7.2: 字体大小与文本速度

| 字段 | 内容 |
|------|------|
| **Story ID** | E7.2 |
| **标题** | 实现 4 级字体大小与文本速度控制 |
| **描述** | 实现 4 级字体大小：small / normal / large / extra_large。在 `options.rpy` 中定义 `gui.text_size` 基础值，运行时根据设置动态缩放。实现文本速度控制：slow（逐字 0.05s）/ normal（0.03s）/ fast（0.01s）/ instant（瞬间显示）。字体大小变更后重新布局对话框确保不溢出。参见 `architecture-review.md` §6 美术-技术接口协调清单第 5 项（文字大小测试）。 |
| **验收标准** | 1. 4 级字体大小可切换且不溢出对话框；2. 4 级文本速度可切换；3. 设置即时生效（不需重启）；4. 字体大小为 persistent（跨周目保持）；5. extra_large 在 1920×1080 下不溢出 |
| **依赖** | E7.1 |
| **复杂度** | S |
| **所属 Batch** | 2 |

### Story E7.3: 键盘导航全覆盖

| 字段 | 内容 |
|------|------|
| **Story ID** | E7.3 |
| **标题** | 实现全键盘导航与快捷键系统 |
| **描述** | 实现全键盘可操作：方向键导航选择选项、Enter 确认、Esc 打开菜单、空格长按拥抱天使、Ctrl 跳过、S 快速存档、L 快速读档、A 自动模式。Tab 键焦点切换（UI 元素间）。所有界面可通过键盘完全操作，不依赖鼠标。实现焦点视觉指示器（紫色边框高亮当前焦点元素）。参见 `existential-protection-gdd.md` §8.1。 |
| **验收标准** | 1. 所有界面可通过键盘完全操作；2. 选择选项可用方向键导航；3. 空格长按触发拥抱；4. 焦点视觉指示器清晰可见；5. 快捷键不与叙事脚本冲突 |
| **依赖** | E7.1 |
| **复杂度** | M |
| **所属 Batch** | 2 |

### Story E7.4: 内容预警系统

| 字段 | 内容 |
|------|------|
| **Story ID** | E7.4 |
| **标题** | 实现内容预警与章节跳过系统 |
| **描述** | 按 [GDD:C5-§8.2] 实现内容预警系统。每章标题卡前显示一句话情感主题预警（如"本章涉及身份挣扎与自我否定"）。Ch8（HARM_GUIDE）前显示特殊预警："本章涉及自我伤害的主题。如果你正在经历类似的痛苦，请记得你不是一个人。"创伤性段落标记为可跳过，跳过后显示简短摘要。Ch8 可完全跳过（质点以 50% 完成）。在游戏设置中提供心理援助热线信息。参见 `existential-protection-gdd.md` §8.2 和 §8.4。 |
| **验收标准** | 1. 每章标题卡前显示情感主题预警；2. Ch8 前显示特殊预警；3. 可跳过段落后显示简短摘要；4. Ch8 可完全跳过（50% 完成）；5. 设置中有心理援助热线信息；6. 预警语气温柔不剧透 |
| **依赖** | E7.1, E2.4 |
| **复杂度** | M |
| **所属 Batch** | 2 |

---

## Epic 8: UI/UX 实现

> **Batch: 3** | **系统优先级: P2**
>
> 目标：实现主菜单、存档界面、设置界面、天使 HUD、选择界面视觉、翅膀亮度可视化。
>
> **参考文档**：`docs/architecture/architecture-review.md` §6 美术-技术接口协调清单

### Story E8.1: 主菜单与标题画面

| 字段 | 内容 |
|------|------|
| **Story ID** | E8.1 |
| **标题** | 实现主菜单界面 |
| **描述** | 实现 `gui/main_menu.rpy` 主菜单 Screen：开始游戏（新游戏）、继续游戏（读档）、设置、图鉴（CG/结局）、退出。首次游玩时"继续游戏"不可用（灰色）。标题画面使用项目主视觉（天使+心爱的剪影）。背景音乐为主题曲。按钮使用紫色/金色主题。参见 `architecture-review.md` §6 美术-技术接口协调清单第 4 项（UI 元素分层 PSD）。 |
| **验收标准** | 1. 主菜单 5 个按钮全部可用；2. 首次游玩"继续游戏"灰色不可用；3. 二周目后"继续游戏"可用；4. 标题画面视觉正确；5. 背景音乐正确播放 |
| **依赖** | E1.4, E7.1 |
| **复杂度** | M |
| **所属 Batch** | 3 |

### Story E8.2: 存档/读档界面

| 字段 | 内容 |
|------|------|
| **Story ID** | E8.2 |
| **标题** | 实现存档/读档界面 |
| **描述** | 实现 `gui/save_load.rpy` 存档/读档 Screen。6 个手动槽位 + 3 个自动槽位网格布局。每个槽位显示：缩略图、章节号、质点进度摘要（完成数/16）、翅膀阶段图标、时间戳。空槽位显示"空"占位符。存档时确认弹窗（"覆盖现有存档？"）。读档时确认弹窗（"当前进度将丢失"）。支持删除存档。参见 Story E1.1 的槽位管理逻辑。 |
| **验收标准** | 1. 9 个槽位网格正确布局；2. 槽位信息完整显示；3. 存档/读档确认弹窗正确；4. 可删除存档；5. 空槽位显示占位符 |
| **依赖** | E1.1, E8.1 |
| **复杂度** | M |
| **所属 Batch** | 3 |

### Story E8.3: 设置界面

| 字段 | 内容 |
|------|------|
| **Story ID** | E8.3 |
| **标题** | 实现设置界面（54 项特性） |
| **描述** | 实现 `gui/preferences.rpy` 设置界面，包含全部无障碍和游戏设置：(1) 字体大小 4 级、(2) 文本速度 4 级、(3) 自动模式间隔、(4) 跳过未读文本开关、(5) 4 级无障碍标志位、(6) BGM 音量、(7) SE 音量、(8) 语音音量、(9) 全屏/窗口、(10) 心理援助热线信息按钮。设置实时生效且为 persistent。参见 `phase3-assembly-review.md` Phase 4 交接要求中 design-strategist 的 54 项特性 UI 规划。 |
| **验收标准** | 1. 全部设置项可调整；2. 设置即时生效；3. 设置为 persistent（跨周目保持）；4. 4 级无障碍标志位在设置界面可见；5. 心理援助热线信息可查看 |
| **依赖** | E7.1, E7.2 |
| **复杂度** | M |
| **所属 Batch** | 3 |

### Story E8.4: 天使状态 HUD

| 字段 | 内容 |
|------|------|
| **Story ID** | E8.4 |
| **标题** | 实现天使状态 HUD 叠加层 |
| **描述** | 实现 `gui/angel_overlay.rpy` 天使状态 HUD 叠加层 Screen。显示元素：(1) 天使立绘（当前情感状态对应表情）、(2) 翅膀视觉（当前亮度/阶段对应渲染）、(3) 拥抱计数器（剩余次数/Phase 1-2，无限/Phase 3）、(4) 点击天使热区（可点击区域指示）。翅膀亮度可视化：通过 `im.MatrixColor` 或预渲染等级图片实现动态亮度。参见 `architecture-review.md` §3.1 翅膀着色方案需原型验证。参见 `angel-companionship-gdd.md` §3 互动机制。 |
| **验收标准** | 1. 天使立绘正确显示当前情感表情；2. 翅膀亮度视觉与 `wing_brightness_displayed` 对应；3. 拥抱计数器正确显示；4. 点击天使热区可触发互动；5. 翅膀亮度变化平滑过渡 |
| **依赖** | E5.2, E5.3, E5.5 |
| **复杂度** | L |
| **所属 Batch** | 3 |

### Story E8.5: 图鉴界面

| 字段 | 内容 |
|------|------|
| **Story ID** | E8.5 |
| **标题** | 实现 CG 图鉴与结局列表界面 |
| **描述** | 实现 `gui/gallery.rpy` 图鉴界面。CG 图鉴：网格布局，已解锁 CG 显示缩略图（点击查看全尺寸），未解锁显示"?"占位符。结局列表：3 种结局（融合/守护/觉醒），已达成显示结局名 + 描述，未达成显示"???"。二周目可访问。使用 `persistent.cg_unlocked` 和 `persistent.endings_seen` 数据。参见 Story E1.4 persistent 变量管理。 |
| **验收标准** | 1. CG 图鉴网格正确布局；2. 已解锁 CG 可查看全尺寸；3. 未解锁 CG 显示"?"占位符；4. 结局列表正确显示已达成/未达成；5. 首次游玩全部锁定 |
| **依赖** | E1.4, E8.1 |
| **复杂度** | M |
| **所属 Batch** | 3 |

---

## Epic 9: 内容制作与打磨

> **Batch: 3** | **系统优先级: P3**
>
> 目标：16 章叙事脚本 + 选择节点数据 + 天使对话池 + 结局分支 + 音频集成 + 最终打磨。

### Story E9.1: Ch1-4 叙事脚本与数据（人类八度·第一批）

| 字段 | 内容 |
|------|------|
| **Story ID** | E9.1 |
| **标题** | 编写 Ch1-4 叙事脚本、选择节点、暗流配置 |
| **描述** | 编写 Ch1（王国/白花）、Ch2（幸福/雨宫莲）、Ch3（基础/绽美）、Ch4（自我/融爱）的完整叙事脚本（`.rpy` 文件）。每章包含五拍完整内容。填充选择节点 JSON 数据（每质点 2-3 个选择，含正式文本和 confrontation_tag）。配置暗流触发（Ch1: EXIST_DENY 低强度 2、Ch2: HOPE_ERASE 低强度 2、Ch3: PAIN_AMP 低强度 3、Ch4: SHAME_LOOP 中强度 4）。填充天使对话池（Phase 1 calm 风格 + Phase 2a aching 风格）。参见各 GDD 的章节映射表。 |
| **验收标准** | 1. Ch1-4 叙事脚本完整可玩；2. 选择节点数据通过校验；3. 暗流按映射表正确触发；4. 天使对话风格与 Phase 一致；5. 翅膀亮度在 Phase 1 保持 1.0，Ch4 开始暗淡 |
| **依赖** | E2.5, E6.5, E3.5, E4.1, E5.4 |
| **复杂度** | XL |
| **所属 Batch** | 3 |

### Story E9.2: Ch5-8 叙事脚本与数据（人类八度·第二批）

| 字段 | 内容 |
|------|------|
| **Story ID** | E9.2 |
| **标题** | 编写 Ch5-8 叙事脚本与数据 |
| **描述** | 编写 Ch5（逻辑/爱丽丝）、Ch6（共情/星烬）、Ch7（超我/爱心）、Ch8（胜利/启明）的完整叙事脚本。Ch5 含 NIHILISM 暗流（中强度 4），天使不辩论纯粹存在。Ch8 含 HARM_GUIDE 暗流（中强度 6），紧急介入，台词不可跳过。填充选择节点和天使对话池（Phase 2a aching + resolute 风格）。Ch8 含内容预警和可跳过机制。参见 `existential-protection-gdd.md` §7.1 每章暗流映射。 |
| **验收标准** | 1. Ch5-8 叙事脚本完整可玩；2. Ch5 NIHILISM 天使不辩论；3. Ch8 HARM_GUIDE 紧急介入正确（不可跳过）；4. Ch8 内容预警正确显示；5. 翅膀亮度在 Ch5 开始明显暗淡（0.70） |
| **依赖** | E9.1 |
| **复杂度** | XL |
| **所属 Batch** | 3 |

### Story E9.3: Ch9-13 叙事脚本与数据（人类八度·第三批）

| 字段 | 内容 |
|------|------|
| **Story ID** | E9.3 |
| **标题** | 编写 Ch9-13 叙事脚本与数据（含复合暗流） |
| **描述** | 编写 Ch9（荣耀）、Ch10（严厉）、Ch11（慈悲）、Ch12（理智）、Ch13（真我/心爱的）的完整叙事脚本。Ch9-12 含复合暗流（两种同时触发）。Ch13 为转折点：全部 8 种暗流轮番出现但不达临界值，天使最安静把力量给了心爱的。Ch13 含身份选择标签（前三个 ESCAPE，"我都是"ENGAGE）。Phase 2b 代价乘数 1.5，翅膀明显暗淡。参见 `existential-protection-gdd.md` §7.1 和 `sephirot-progression-gdd.md` Ch13 特殊处理。 |
| **验收标准** | 1. Ch9-13 叙事脚本完整可玩；2. 复合暗流正确触发（两种同时）；3. Ch13 全部 8 种暗流轮番出现；4. Ch13 身份选择标签正确；5. 翅膀亮度在 Ch13 降至约 0.36 |
| **依赖** | E9.2 |
| **复杂度** | XL |
| **所属 Batch** | 3 |

### Story E9.4: Ch14-16 叙事脚本与数据（神性八度·下行）

| 字段 | 内容 |
|------|------|
| **Story ID** | E9.4 |
| **标题** | 编写 Ch14-16 叙事脚本与结局分支 |
| **描述** | 编写 Ch14（智慧）、Ch15（美丽）、Ch16（王冠）的完整叙事脚本。Ch14：全部 8 种暗流同时爆发（峰值强度 10），天使用尽全力一声"回来"统一一切。Ch15：天使不再对抗暗流，在暗流中陪伴心爱的（EX90 DENY + NIHILISM 深度），代价极低。Ch16：存在保护关闭，翅膀恢复 1.0，三种结局选择（融合/守护/觉醒）。觉醒结局需 `bond_depth >= 0.6`。参见 `existential-protection-gdd.md` §7.3 Ch16 关闭序列和 `sephirot-progression-gdd.md` Phase 3 特殊处理。 |
| **验收标准** | 1. Ch14 全部 8 种暗流同时爆发；2. Ch15 天使不再拉回而是陪伴；3. Ch16 存在保护正确关闭；4. 翅膀恢复到 1.0；5. 三种结局可达成；6. 觉醒结局需 bond_depth ≥ 0.6 |
| **依赖** | E9.3, E4.6 |
| **复杂度** | XL |
| **所属 Batch** | 3 |

### Story E9.5: 音频资产集成

| 字段 | 内容 |
|------|------|
| **Story ID** | E9.5 |
| **标题** | 集成 BGM、SE、语音音频资产 |
| **描述** | 集成全部音频资产：(1) BGM：主题曲、每章背景音乐、暗流期间低频音效、天使介入恢复音效。(2) SE：选择确认音、天使拥抱音、翅膀闪光音、暗流碎裂/震动音效。(3) 语音（如有）：天使介入台词语音。音频文件放置在 `game/audio/bgm/`、`game/audio/se/`、`game/audio/voice/`。在叙事脚本和系统代码中调用 `renpy.music.play()` 和 `renpy.sound.play()`。暗流音频在 `audio_stable_mode` 下降级处理。参见 `existential-protection-gdd.md` 各暗流的音频表现定义。 |
| **验收标准** | 1. BGM 在章节切换时正确切换；2. 暗流音效正确触发；3. 天使介入音效正确；4. 音量设置生效；5. `audio_stable_mode` 下暗流音频降级 |
| **依赖** | E9.1, E9.2, E9.3, E9.4 |
| **复杂度** | L |
| **所属 Batch** | 3 |

### Story E9.6: 翅膀着色方案验证与实现

| 字段 | 内容 |
|------|------|
| **Story ID** | E9.6 |
| **标题** | 验证并实现翅膀动态着色方案 |
| **描述** | 按 `architecture-review.md` §3.1 的建议，在 Batch 1 原型验证基础上实现最终翅膀着色方案。方案 A（首选）：`im.MatrixColor` 动态调整亮度，测试 60 FPS 性能。方案 B（备选）：预渲染 10-20 个亮度等级的翅膀图片，离散切换。方案 C（备选）：`Transform.matrixcolor` + 动画过渡。选择性能最优方案并实现。与美术总监协调翅膀基础图（5 张 PNG，带 alpha 通道）。参见 `architecture-review.md` §3.1。 |
| **验收标准** | 1. 60 FPS 下翅膀亮度变化无卡顿；2. 亮度变化平滑过渡（非突变）；3. Stage 1-5 翅膀视觉与亮度值对应；4. 方案选择有性能测试报告支撑 |
| **依赖** | E5.2, E8.4 |
| **复杂度** | L |
| **所属 Batch** | 3 |

### Story E9.7: Steam 集成与最终打包

| 字段 | 内容 |
|------|------|
| **Story ID** | E9.7 |
| **标题** | 实现 Steam SDK 集成与最终打包 |
| **描述** | 按 [ADR-001] 验证里程碑 M5 实现 Steam 集成：(1) Steam SDK 集成（成就系统：首次拥抱、首次直面、翅膀最暗、三结局达成等）。(2) 云存档支持。(3) Steam Overlay 兼容性。(4) 最终打包：Windows + macOS + Linux 三平台构建。创建 `docs/engine-reference/renpy/STEAM.md` 记录 Steam 集成配置。参见 `architecture-review.md` §3.2 引擎参考文档缺失。 |
| **验收标准** | 1. Steam 成就正确解锁；2. 云存档可同步；3. Steam Overlay 可用；4. 三平台构建成功；5. `STEAM.md` 文档存在 |
| **依赖** | E9.4, E9.5, E9.6 |
| **复杂度** | L |
| **所属 Batch** | 3 |

### Story E9.8: 全量 Playtest 与平衡调参

| 字段 | 内容 |
|------|------|
| **Story ID** | E9.8 |
| **标题** | 全量 Playtest 与平衡调参 |
| **描述** | 按 `architecture-review.md` §3.3 建议，进行全量 Playtest。重点验证：(1) 翅膀亮度累积曲线（Phase 1: 1.0 → Phase 2a: 0.85 → Phase 2b: 0.509 → Phase 3: 0.159 → Ch16: 1.0）。(2) 暗流触发频率不过高不过低。(3) 代价参数需调参时修改 `data/protection/cost_table.json`。(4) 预留 `global_cost_multiplier` 全局缩放设置。(5) 时间卡住机制的提示时机。(6) 天使对话池不重复。(7) 三结局可达性。参见 `existential-protection-gdd.md` 附录 C 设计理论评审。 |
| **验收标准** | 1. 翅膀亮度曲线与设计吻合（±10%）；2. 暗流频率合理（不导致翅膀过早透明）；3. 三结局均可达成；4. Playtest 报告生成；5. 调参记录归档 |
| **依赖** | E9.7 |
| **复杂度** | XL |
| **所属 Batch** | 3 |

---

## 13. 跨 Epic 依赖矩阵

```
Epic 0 (骨架) ─────────────────────────────────────────────────────────────
  │
  ├── E0.1 项目初始化
  │     ├── E0.2 Git 初始化
  │     ├── E0.3 JSON 数据层 ──────────────┐
  │     ├── E0.4 常量定义                    │
  │     │     └── E0.5 default 声明          │
  │     │           ├── E1.1 存档槽位        │
  │     │           ├── E1.2 翅膀持久化       │
  │     │           ├── E1.3 质点持久化       │
  │     │           │     └── E1.4 persistent│
  │     │           │           └── E1.5 校验│
  │     │           ├── E2.1 章节路由         │
  │     │           │     └── E2.2 叙事标签  │
  │     │           │           └── E2.3 五拍│
  │     │           │                 └── E2.4 切换
  │     │           │                       └── E2.5 Ch1骨架 ◄── Epic 0 出口
  │     │           │
  │     │           │  ─── Batch 1 ───
  │     │           │
  │     │           ├── E3.1 choice_node ◄── E0.3
  │     │           │     ├── E3.2 选择界面
  │     │           │     │     └── E3.3 后果分发
  │     │           │     │           └── E3.4 保护过滤 ◄── E4.1
  │     │           │     └── E3.5 数据骨架
  │     │           │
  │     │           ├── E4.1 暗流引擎 ◄── E0.3, E0.4
  │     │           │     ├── E4.2 天使介入 ◄── E5.2
  │     │           │     │     └── E4.3 翅膀代价
  │     │           │     │           └── E4.4 虚无阻断 ◄── E3.3
  │     │           │     │           └── E4.5 恢复过渡
  │     │           │     │           └── E4.6 Ch16关闭 ◄── E2.4
  │     │           │
  │     │           ├── E5.1 状态机
  │     │           │     └── E5.2 双层模型
  │     │           │           ├── E5.3 互动机制 ◄── E5.4, E4.2
  │     │           │           └── E5.5 情感管理
  │     │           │     └── E5.4 对话池 ◄── E0.3
  │     │
  │     │           │  ─── Batch 2 ───
  │     │           │
  │     │           ├── E6.1 状态机 ◄── E1.3
  │     │           │     └── E6.2 完成判定 ◄── E3.3
  │     │           │           └── E6.3 时间卡住 ◄── E5.4
  │     │           ├── E6.4 数据骨架 ◄── E0.3, E4.1
  │     │           └── E6.5 集成测试 ◄── E6.1-E6.3, E3.3, E4.4, E5.3
  │     │
  │     │           ├── E7.1 标志位 ◄── E4.5
  │     │           │     ├── E7.2 字体速度
  │     │           │     ├── E7.3 键盘导航
  │     │           │     └── E7.4 内容预警 ◄── E2.4
  │     │
  │     │           │  ─── Batch 3 ───
  │     │           │
  │     │           ├── E8.1 主菜单 ◄── E1.4, E7.1
  │     │           ├── E8.2 存档界面 ◄── E1.1
  │     │           ├── E8.3 设置界面 ◄── E7.1, E7.2
  │     │           ├── E8.4 天使HUD ◄── E5.2, E5.3, E5.5
  │     │           └── E8.5 图鉴 ◄── E1.4
  │     │
  │     ├── E9.1 Ch1-4 ◄── E2.5, E6.5, E3.5, E4.1, E5.4
  │     │     └── E9.2 Ch5-8
  │     │           └── E9.3 Ch9-13
  │     │                 └── E9.4 Ch14-16 ◄── E4.6
  │     ├── E9.5 音频 ◄── E9.1-E9.4
  │     ├── E9.6 翅膀着色 ◄── E5.2, E8.4
  │     ├── E9.7 Steam ◄── E9.4, E9.5, E9.6
  │     └── E9.8 Playtest ◄── E9.7
  │
  └── E0.6 CI ◄── E0.1, E0.3
```

---

## 14. Story 复杂度统计

### 14.1 按 Batch 统计

| Batch | Epic | Story 数 | S | M | L | XL | 总人日（估） |
|-------|------|---------|---|---|---|----|-----------|
| Batch 0 | Epic 0 | 6 | 2 | 3 | 0 | 0 | ~10 |
| Batch 0 | Epic 1 | 5 | 0 | 4 | 0 | 0 | ~12 |
| Batch 0 | Epic 2 | 5 | 1 | 2 | 2 | 0 | ~14 |
| **Batch 0 小计** | | **16** | **3** | **9** | **2** | **0** | **~36** |
| Batch 1 | Epic 3 | 5 | 1 | 3 | 1 | 0 | ~13 |
| Batch 1 | Epic 4 | 6 | 1 | 2 | 2 | 0 | ~16 |
| Batch 1 | Epic 5 | 5 | 0 | 2 | 2 | 0 | ~14 |
| **Batch 1 小计** | | **16** | **2** | **7** | **5** | **0** | **~43** |
| Batch 2 | Epic 6 | 5 | 1 | 2 | 1 | 1 | ~20 |
| Batch 2 | Epic 7 | 4 | 1 | 3 | 0 | 0 | ~10 |
| **Batch 2 小计** | | **9** | **2** | **5** | **1** | **1** | **~30** |
| Batch 3 | Epic 8 | 5 | 0 | 3 | 2 | 0 | ~16 |
| Batch 3 | Epic 9 | 8 | 0 | 0 | 2 | 5 | ~50 |
| **Batch 3 小计** | | **13** | **0** | **3** | **4** | **5** | **~66** |
| **总计** | | **54** | **7** | **24** | **12** | **6** | **~175** |

### 14.2 按 Epic 统计

| Epic | 名称 | Story 数 | 总人日（估） |
|------|------|---------|-----------|
| Epic 0 | 项目骨架 | 6 | ~10 |
| Epic 1 | C6 存档 | 5 | ~12 |
| Epic 2 | C1 叙事引擎 | 5 | ~14 |
| Epic 3 | C3 选择系统 | 5 | ~13 |
| Epic 4 | C5 存在保护 | 6 | ~16 |
| Epic 5 | C2 天使陪伴 | 5 | ~14 |
| Epic 6 | C4 质点进程 | 5 | ~20 |
| Epic 7 | 可访问性 | 4 | ~10 |
| Epic 8 | UI/UX | 5 | ~16 |
| Epic 9 | 内容制作 | 8 | ~50 |
| **总计** | | **54** | **~175** |

### 14.3 关键路径

最长依赖链（关键路径）：

```
E0.1 → E0.4 → E0.5 → E2.1 → E2.3 → E2.5 → E6.5 → E9.1 → E9.2 → E9.3 → E9.4 → E9.7 → E9.8
```

关键路径 Story 数：13 个，总人日约 ~85 人日。建议关键路径上的 Story 优先分配资源。

---

**文档结束**

> 本文档为 Epic/Story 拆分的完整规格。54 个 Story 覆盖 6 大核心系统 + 基础设施 + 可访问性 + UI/UX + 内容制作。
>
> 待协调项：
> 1. 美术-技术接口：翅膀基础图、天使表情集、暗流视觉参考、UI 分层 PSD（Batch 1 前完成）
> 2. Ren'Py 版本钉定：`docs/engine-reference/renpy/VERSION.md`（Batch 0 前完成）
> 3. GDD 回写确认：C2/C3/C4/C5 四份 GDD 与架构文档对齐
> 4. 翅膀着色方案原型验证（Batch 1 期间）
