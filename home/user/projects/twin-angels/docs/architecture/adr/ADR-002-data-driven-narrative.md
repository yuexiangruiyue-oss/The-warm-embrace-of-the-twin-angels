# ADR-002: 数据驱动叙事设计

| 字段 | 值 |
|---|---|
| ADR 编号 | 002 |
| 标题 | 数据驱动 JSON vs 硬编码脚本 |
| 状态 | ACCEPTED |
| 日期 | 2025-07-14 |
| 决策者 | 程基岩（技术主程） |
| 关联文档 | `design/gdd/sephirot-progression-gdd.md`、`design/gdd/choice-system-gdd.md`、`main-architecture.md` §5 |

## 上下文

本项目包含 16 个 Sephirot 章节，每章 5 个叙事节拍（ENCOUNTER → STRUGGLE → COMFORT → CHOICE → TRANSFORM），每章至少 1 个选择节点，每个选择节点 2-4 个选项。总数据量：

- 16 章 × 5 拍 = 80 个叙事节点
- ~20-30 个选择节点 × 3 选项 = ~60-90 个选项
- 每个选项含 10+ 字段（text, texture_tag, confrontation_tag, progress_value, angel_response_delta 等）
- 天使对话池：每章节 10-20 条对话 = ~200-320 条
- 存在保护配置：8 种暗流 × 3 强度 = 24 组配置

这些数据需要被多个系统消费：C1（叙事引擎）读取叙事流程，C3（选择系统）读取选项，C4（Sephirot 系统）读取完成度配置，C5（存在保护）读取暗流配置，C2（天使系统）读取对话池。

## 备选方案

### 方案 A：JSON 数据驱动

**概述**：所有叙事内容、选择节点、系统配置存储为 JSON 文件，代码逻辑从 JSON 读取数据驱动行为。

**优势**：
- 内容与代码分离：文案/策划可独立编辑 JSON，不触碰代码。
- 可校验：JSON Schema 可在构建前校验数据完整性和一致性。
- 可diff：版本控制下 JSON 文件的变更清晰可追踪。
- 可批量处理：工具脚本可批量修改、校验、导出数据。
- 多人协作友好：不同人编辑不同 JSON 文件，冲突少。
- 可扩展：新增字段只需修改 JSON Schema，不影响已有数据。

**劣势**：
- 运行时解析开销（可忽略，启动时一次性加载到内存）。
- JSON 不支持注释（可通过 `_comment` 字段或外部文档弥补）。
- 数据校验需要额外工具开发。
- 调试时需要查看 JSON 文件而非代码内联。

### 方案 B：Ren'Py 脚本内联硬编码

**概述**：所有叙事内容、选择、系统配置直接写在 `.rpy` 脚本中，使用 Ren'Py 原生的 `menu`、`label`、`$` 变量赋值。

**优势**：
- 无需额外数据格式：直接使用 Ren'Py 脚本语言。
- 调试直观：所有内容在脚本中，断点可设。
- 无解析开销。
- Ren'Py 原生 `menu` 支持选择分支。

**劣势**：
- 内容与逻辑耦合：修改一个选项的 `angel_response_delta` 需要编辑脚本代码。
- 可维护性差：90 个选项的字段散落在脚本中，难以全局查看和修改。
- 多人协作冲突高：多人编辑同一 `.rpy` 文件容易冲突。
- 无法程序化校验：选项数据的一致性（如 `confrontation_tag` 与 `progress_value` 映射）无法自动检查。
- 系统消费困难：C4/C5 需要从脚本中提取数据，Ren'Py 脚本不是结构化数据。
- 可扩展性差：新增字段需要修改脚本中的每个选项。

### 方案 C：混合模式（脚本叙事 + Python 字典配置）

**概述**：叙事流程用 Ren'Py 脚本（`.rpy`），系统配置和选择数据用 Python 字典定义在 `systems/` 模块中。

**优势**：
- 叙事流程保持 Ren'Py 原生体验。
- 系统配置用 Python 字典，比 JSON 更灵活（支持函数引用、条件逻辑）。
- 调试比 JSON 方便。

**劣势**：
- 配置数据嵌入代码中，文案/策划无法独立编辑。
- Python 字典的语法对非程序员不友好（引号、逗号、缩进）。
- 版本控制 diff 不如 JSON 清晰。
- 无法使用 JSON Schema 校验。

## 决策

**选择方案 A：JSON 数据驱动。**

### 决策理由

1. **内容与代码分离是核心需求**：本项目有大量叙事内容（16 章 × 5 拍 + 选择 + 对话池），文案/策划需要独立编辑内容而不触碰系统代码。JSON 是非程序员最易上手的结构化数据格式。

2. **多系统消费同一数据**：一个选择选项的数据需要被 C3（处理选择）、C4（处理直面标签）、C2（处理天使响应）同时消费。JSON 作为中立数据格式，各系统按需读取字段，互不耦合。

3. **可校验性是质量保障**：`confrontation_tag` 与 `progress_value` 的一致性、`angel_response_delta` 的字段完整性、叙事跳转目标的存在性等，均可通过 JSON Schema + 校验脚本自动检查。这在硬编码方案中几乎不可能实现。

4. **CONCERN 2 的解决依赖数据驱动**：统一选项数据结构（新增 `confrontation_tag` 字段）需要全局修改所有选项。JSON 数据驱动下，修改 JSON Schema + 运行校验脚本即可发现所有需要更新的选项；硬编码方案需要逐个脚本文件搜索修改。

5. **性能影响可忽略**：全部 JSON 数据启动时加载到内存，预计 < 2MB。运行时无解析开销（内存读取）。

### 混合策略

虽然选择 JSON 数据驱动，但叙事**呈现**仍使用 Ren'Py 脚本（`.rpy`）。具体分工：

| 内容 | 存储形式 | 消费者 |
|---|---|---|
| 叙事流程（章节 → 节拍 → 场景） | JSON（`data/sephirot/*.json`） | C1 读取流程，调用 `.rpy` label |
| 场景对话与描写 | Ren'Py 脚本（`scripts/ch*.rpy`） | C1 直接呈现 |
| 选择节点与选项 | JSON（`data/choices/choice_nodes.json`） | C3 读取并呈现 |
| 天使对话池 | JSON（`data/angel/dialogue_pools.json`） | C2 读取并选择 |
| 系统配置（暗流、代价、结局） | JSON（`data/protection/*.json`） | C4/C5 读取 |

**原则**：结构化数据用 JSON，叙事文本用 Ren'Py 脚本。JSON 定义"做什么"（数据），Ren'Py 脚本定义"怎么说"（文本）。

## 后果

### 正面后果

- 文案/策划可独立编辑 JSON 内容，不依赖程序员。
- JSON Schema 校验在 CI 中自动运行，数据错误早期发现。
- 新增字段（如 `confrontation_tag`）只需更新 Schema + 校验脚本。
- 版本控制 diff 清晰，code review 容易。
- 未来可开发可视化编辑器（Web/GUI）编辑 JSON，进一步降低门槛。

### 负面后果

- 需要开发数据校验工具（`tools/validate_data.py`），预估 1-2 天工时。
- JSON 不支持注释，需要用 `_comment` 字段或外部文档记录设计意图。
- 调试时需要同时查看 JSON 数据和代码逻辑。
- 数据结构变更需要迁移已有 JSON 数据（但初期数据量小，影响有限）。

### 风险缓解

| 风险 | 缓解措施 |
|---|---|
| JSON 语法错误导致加载失败 | 启动时 `load_all_data()` 包含 try-except，给出明确错误提示 |
| 数据不一致（字段缺失/类型错误） | JSON Schema + `tools/validate_data.py` 在 CI 中强制校验 |
| JSON 无注释 | 约定 `_comment` 字段用于行内注释；复杂设计意图记录在 GDD 中 |
| 数据迁移 | 版本化数据结构（JSON 中包含 `"schema_version": 1`），提供迁移脚本 |

## 数据校验规则（关键项）

以下校验规则在 `tools/validate_data.py` 中实现：

```python
# 选项数据校验规则
def validate_choice_option(option):
    # 1. 必填字段存在
    required = ['id', 'text', 'texture_tag', 'progress_value',
                'emotional_weight', 'angel_reaction', 'angel_response_delta',
                'bond_depth_delta', 'memory_entry', 'existence_protection',
                'narrative_jump']
    for field in required:
        assert field in option, f"选项 {option.get('id', '?')} 缺少字段: {field}"

    # 2. confrontation_tag 与 progress_value 一致性
    if option.get('confrontation_tag') == 'ENGAGE':
        assert option['progress_value'] == 1.0
    elif option.get('confrontation_tag') == 'ESCAPE':
        assert option['progress_value'] == 0.3
    elif option.get('confrontation_tag') == 'NEUTRAL':
        assert option['progress_value'] == 0.0

    # 3. angel_response_delta 字段完整性
    delta = option['angel_response_delta']
    valid_keys = {'warmth', 'depth', 'protectiveness', 'vulnerability'}
    for key in delta:
        assert key in valid_keys, f"未知 angel_response_delta 字段: {key}"
        assert -0.1 <= delta[key] <= 0.1, f"delta 值超出范围: {key}={delta[key]}"

    # 4. narrative_jump 目标存在性
    assert node_exists(option['narrative_jump']), f"跳转目标不存在: {option['narrative_jump']}"

    # 5. bond_depth_delta 范围
    assert -0.05 <= option['bond_depth_delta'] <= 0.15, "bond_depth_delta 超出范围"
```

## 验证里程碑

| 里程碑 | 验证内容 | 时间点 |
|---|---|---|
| M1 | JSON Schema 定义完成，可校验现有数据 | Batch 0 |
| M2 | `tools/validate_data.py` 集成到 CI | Batch 0 |
| M3 | Ch1-3 全量数据通过校验 | Batch 3 |

---

*本 ADR 与主架构文档 §5 对应。*
