# 选择系统 GDD

> **项目**：《双生天使的拥抱》
> **系统编号**：C3
> **阶段**：Phase 2 系统设计
> **产出者**：文策渊（design-strategist）
> **日期**：2026-08-02
> **设计支柱**：支柱三·从解离走向整合
> **依据**：`design/concept/game-concept.md` §2.1.1、§2.2.2、§7.3

---

## 1. 系统概述

### 1.1 设计理念："情感共振选择"模型

传统视觉小说的选择系统是"分支树"——选择A走向路线A，选择B走向路线B，选错了就"Bad End"。这种模型的核心假设是：**选择有对错之分，玩家的目标是找到"正确答案"**。

本游戏彻底拒绝这个假设。

《双生天使的拥抱》采用"情感共振选择"模型——选择不是"解谜"，而是"表达"。玩家面临的选择没有正确答案，每个选择都是"有效的"，它们改变的不是"能否通关"，而是**通向终点的路径纹理**和**天使回应你的方式**。

**一句话定义**：在关键叙事节点呈现行动/态度/关系三类情感共振选择，选择改变天使回应纹理而非通关路径。

### 1.2 核心设计原则

1. **选择不设正确答案**。没有任何选择是"最优解"。每个选择都推进质点进程，只是推进的纹理不同。
2. **选择改变天使的回应**。天使对玩家的态度、对话内容、拥抱温度会随选择演变——这是选择的"后果"，但不是"惩罚"。
3. **选择被存在保护过滤**。任何可能导致虚无主义结局的选择，都会被系统以叙事方式温柔转化为"天使拉你回来"。
4. **最终选择不受保护**。Phase 3的三种结局选择是完全自由的，存在保护不干预。
5. **选择是自我探索的工具**。选择的本质不是"做对"，而是"如果是你，你会怎么做"。

### 1.3 设计意图

为什么要这样设计？

- **苞苞的创伤包含"被否定选择"的经历**——她的身份选择被外界否定为"错的"。如果游戏中的选择也有"对错"，就是在重复创伤。让所有选择都"有效"，是对"你的感受是真实的"的肯定。
- **解离→整合的弧线需要选择来驱动**。早期选择感觉"遥远"（解离），中期选择开始"刺痛"（参与），后期选择"不可逃避"（整合）。选择的情感重量随进程递增，这本身就是从解离走向整合的体验。
- **天使的回应是选择的核心反馈**。选择的"后果"不是数值变化，而是天使对待你的方式变化——这让选择始终是关于"关系"的，而非关于"策略"的。

---

## 2. 核心机制

### 2.1 三种选择类型

| 选择类型 | 代码 | 核心问题 | 玩家在表达什么 | 示例 |
|---------|------|---------|--------------|------|
| 行动选择 | `action` | "你做什么？" | 你如何对待面前的处境 | "如何拯救白花？" → ①直接用奇迹之力 ②先听她说完 ③问天使 |
| 态度选择 | `attitude` | "你怎么想？" | 你如何理解正在发生的事 | "雨宫莲问'你凭什么相信美好？'" → ①因为天使在 ②因为痛苦也是真的 ③我不知道，但不想放弃 |
| 关系选择 | `relation` | "你怎么爱？" | 你如何回应天使的陪伴 | "天使第一次拥抱你时" → ①僵硬地接受 ②本能地靠近 ③沉默 |

**类型设计原理**：

- **行动选择**是最"外在"的——关于你与世界的交互方式。Phase 1以行动选择为主，因为早期玩家（和心爱的）处于"解决问题"的处理器模式。
- **态度选择**是最"内在"的——关于你如何理解意义。Phase 2中段态度选择增多，因为玩家开始面对"为什么"而非"怎么做"。
- **关系选择**是最"亲密"的——关于你与天使的连接。关系选择贯穿全程，但在Phase 2后半和Phase 3占比最高，因为此时玩家与天使的关系成为情感核心。

### 2.2 选择不设正确答案

**机制**：每个选择节点的每个选项都有一个 `progress_value`（进度值）、`texture_tag`（纹理标签）和 `confrontation_tag`（直面标签）。

- `progress_value`：该选项推进质点进程的程度。所有选项的`progress_value`都≥0——没有任何选项"不推进"。
  - "勇敢"选择（直面痛苦）：`progress_value = 1.0`
  - "温和"选择（缓慢面对）：`progress_value = 0.7`
  - "逃避"选择（暂时回避）：`progress_value = 0.3`（但第三次逃避后天使代为面对，补齐到1.0）
- `texture_tag`：该选项赋予路径的"纹理"——影响天使的回应方式、对话内容、后续叙事的微调。
  - 如`"brave_direct"`（勇敢直接）、`"gentle_patient"`（温和耐心）、`"avoidant"`（回避）、`"dependent_on_angel"`（依赖天使）等。
- **【架构对齐回写】`confrontation_tag`**：直面标签，标记该选项在情感面对中的角色。取值为 `ENGAGE`（直面）/ `ESCAPE`（逃避）/ `NEUTRAL`（中性）/ `null`（非直面选择，如纯关系/态度选择）。
  - `confrontation_tag` 与 `progress_value` 的关系：`ENGAGE → 1.0`、`ESCAPE → 0.3`、`NEUTRAL → 0.0`。当 `confrontation_tag` 为 null 时，`progress_value` 由 `texture_tag` 独立决定。
  - `confrontation_tag` 被 C4 质点进程系统消费（驱动完成判定和逃避计数）；`progress_value` 被 C4 消费（进度更新）。两者存在语义冗余但有意保留——`confrontation_tag` 驱动 C4 逻辑，`progress_value` 作为通用进度值。
  - 参考：`docs/architecture/main-architecture.md` §5.3 统一选项数据结构

**关键规则**：`progress_value`的差异不意味着"勇敢更好"——`progress_value = 0.7`的温和选择同样能完成质点，只是需要更长的叙事节拍。纹理的不同让每次游玩都有独特的情感体验。

### 2.3 选择改变天使回应

天使对玩家的回应由`angel_response_profile`决定，该profile根据玩家的选择历史动态更新：

```python
# angel_response_profile — 由选择历史计算的天使回应档案
{
    "warmth": 0.5,          # 0.0-1.0，天使的温暖度（初始0.5）
    "depth": 0.3,           # 0.0-1.0，天使对话的深度（初始0.3，随进程上升）
    "protectiveness": 0.4,  # 0.0-1.0，天使的保护欲（初始0.4）
    "vulnerability": 0.2,   # 0.0-1.0，天使展现自己脆弱面的程度（初始0.2，Phase 2后上升）
}
```

**选择如何影响这些维度**：

| 选择模式 | warmth | depth | protectiveness | vulnerability |
|---------|--------|-------|---------------|--------------|
| 频繁选择"勇敢直面" | ↑ | ↑↑ | ↓（天使觉得你不需要太多保护） | ↑（天使敢展现更多自己） |
| 频繁选择"温和耐心" | ↑↑ | ↑ | → | ↑ |
| 频繁选择"依赖天使" | ↑ | → | ↑↑（天使更保护你） | ↓（天使不敢在你面前脆弱） |
| 频繁选择"逃避" | → | ↓ | ↑↑↑ | ↓ |
| 频繁选择"态度选择中的自我反思" | ↑ | ↑↑↑ | → | ↑↑ |

**这些维度如何影响天使的实际回应**：

- `warmth > 0.7`：天使的对话中加入更多身体接触描写（"她握住你的手"、"她靠得更近"）
- `depth > 0.6`：天使的对话从"没事的，有我在"进化为包含自己感受的深度对话
- `protectiveness > 0.7`：天使的介入更频繁、更紧急（暗流临界值降低10%）
- `vulnerability > 0.5`：天使开始说暗示性话语、展现自己的恐惧（Phase 2后半的行为提前出现）

### 2.4 选择的延迟后果

**核心设计**：选择的后果不是即时呈现的，而是**延迟的**——在后续章节中以天使的"回忆引用"和叙事微调的方式浮现。

- 选择后**不会**立即弹出"天使好感+1"或"质点进度+30%"之类的系统提示。
- 选择后**会**在后续章节中，天使自然地引用："你还记得在Ch 4时，你告诉融爱'你不是错的'吗？那一刻我就知道你很勇敢。"
- 这种延迟后果让选择感觉"真实"——真实的选择后果不是立即的奖励/惩罚，而是改变了你与他人的关系纹理。

---

## 3. 玩家交互

### 3.1 选择UI呈现方式

#### 3.1.1 选择菜单视觉设计

- **位置**：选择按钮垂直排列在画面下方或右侧（根据场景构图调整）。
- **按钮样式**（对齐美术圣经§4.2）：
  - 常态：浅紫雾底（`#B8A8D8`），深紫藤文字（`#6B5A98`），细边框，圆角胶囊形。
  - Hover/聚焦：天使紫底（`#8B7AB8`），白色文字，边缘柔和光晕。
  - 已选确认：暖金底（`#F5D89A`），短暂闪光后淡出。
- **排列间距**：按钮间距≥20px，避免误触。
- **按钮数量**：每次选择2-4个选项（通常为3个）。

#### 3.1.2 选择类型标记

每个选择按钮的左上角有一个小图标标记选择类型：

| 选择类型 | 图标 | 颜色 |
|---------|------|------|
| 行动选择 | 小手图标 | 草绿白 `#D8E8D0` |
| 态度选择 | 小脑图标 | 冰蓝 `#A8D0E8` |
| 关系选择 | 小心图标 | 黎明粉 `#F0C4D4` |

*为什么标记类型*：让玩家在无意识中感知到"这个选择是关于行动/理解/关系的"，帮助玩家建立对自己选择模式的觉察——这本身就是从解离走向整合的体验。

#### 3.1.3 "问天使"选项的呈现

- "问天使"选项始终排在选择列表的**最后**，视觉上与其他选项有轻微区分——左侧有一个小羽毛图标。
- "问天使"不占用正式选择的"名额"——选择它后，天使给出建议，选择菜单重新出现。
- *为什么不把"问天使"混在正式选项中*：如果"问天使"看起来和其他选项一样，玩家可能把它当作"第三个行动选项"而非"寻求帮助的通道"。视觉区分让玩家明白"这是一个安全出口，不是一个选择"。

### 3.2 选择反馈

```
玩家选择一个选项
    │
    ├── 选中的按钮变为暖金底，其他按钮淡出（0.3秒过渡）
    ├── 选中按钮短暂闪光（0.5秒）
    ├── 选择菜单整体淡出
    ├── 叙事引擎继续推进，进入选择后果的叙事段落
    │
    ├── [后台] 记录选择到choice_history
    ├── [后台] 更新angel_response_profile
    ├── [后台] 更新sephirot_progress（progress_value累加）
    ├── [后台] 如果选择与天使相关，存入angel_memories
    ├── [后台] 查询存在保护是否需要过滤（见§8.3）
    └── [后台] 更新天使的active_dialogue_pool（基于新的选择上下文）
```

**关键**：后台处理完全不可见。玩家只看到"选了→故事继续了"。没有任何数值提示、进度条、好感度显示。

### 3.3 选择后果的延迟表现

选择后果在以下时机以"自然"方式浮现：

| 后果类型 | 浮现时机 | 表现方式 |
|---------|---------|---------|
| 天使回应变化 | 选择后的下一个天使对话 | 天使的语气/内容根据angel_response_profile调整 |
| 天使记忆引用 | 后续1-3章的安息阶段或主动对话 | 天使说"你还记得在{章节}时，你……" |
| 叙事微调 | 后续章节的旁白/内心独白 | 心爱的的内心独白根据选择模式调整（如频繁选择"勇敢"→内心独白更自信） |
| 质点完成质量 | 质点完成时的安息场景 | 完成质量100%→天使说"你真的面对了"；50%→天使说"没关系，你尽力了" |
| 结局纹理 | Ch 16最终选择 | angel_response_profile影响天使在最终选择前的话语和结局细节 |

---

## 4. 数据结构

### 4.1 选择节点数据结构

```python
# choice_node — 一个选择节点的完整定义
{
    "id": "ch04_choice_02",                    # 唯一ID
    "chapter": 4,                              # 所属章节
    "sephirot_id": "ch04_self",                # 所属质点
    "type": "attitude",                        # "action" | "attitude" | "relation"
    "prompt": "融爱说'我是不是错的？'",          # 选择提示文本（通常是角色台词或旁白）
    "context_tags": ["identity", "shame"],     # 上下文标签（用于天使对话池匹配）
    
    "options": [                               # 选项列表（通常2-4个）
        {
            "id": "ch04_c02_o01",              # 选项ID
            "text": "'你不是错的'",              # 选项显示文本
            "texture_tag": "brave_affirm",     # 纹理标签
            # 【架构对齐回写】confrontation_tag 与 bond_depth_delta（ADR/主架构 §5.3）
            "confrontation_tag": "ENGAGE",     # 直面标签：ENGAGE/ESCAPE/NEUTRAL/null
            "progress_value": 1.0,             # 进度值 (0.0-1.0)，ENGAGE→1.0
            "bond_depth_delta": 0.03,          # 羁绊深度变化值
            "emotional_weight": 0.8,           # 情感权重 (0.0-1.0)
            "angel_reaction": "aching",        # 天使的即时情感反应
            "angel_response_delta": {          # 对angel_response_profile的影响
                "warmth": +0.05,
                "depth": +0.08,
                "vulnerability": +0.03
            },
            "memory_entry": {                  # 如果选择此项，存入天使记忆的数据
                "choice_summary": "选择了'你不是错的'",
                "recall_weight": 0.85,
                "recall_trigger": "identity_affirmed"
            },
            "existence_protection": false,     # 是否需要存在保护过滤
            "narrative_jump": "ch04_c02_affirm"  # 选择后跳转的叙事标签
        },
        {
            "id": "ch04_c02_o02",
            "text": "'错的是否定你的人'",
            "texture_tag": "angry_redirect",
            "confrontation_tag": "ESCAPE",     # 【架构对齐回写】直面标签
            "progress_value": 0.9,
            "bond_depth_delta": 0.0,           # 【架构对齐回写】羁绊深度变化
            "emotional_weight": 0.7,
            "angel_reaction": "resolute",
            "angel_response_delta": {
                "warmth": +0.03,
                "depth": +0.05,
                "protectiveness": +0.05
            },
            "memory_entry": {
                "choice_summary": "选择了'错的是否定你的人'",
                "recall_weight": 0.7,
                "recall_trigger": "anger_redirect"
            },
            "existence_protection": false,
            "narrative_jump": "ch04_c02_redirect"
        },
        {
            "id": "ch04_c02_o03",
            "text": "'我也是这样过来的'",
            "texture_tag": "vulnerable_share",
            "confrontation_tag": "ENGAGE",     # 【架构对齐回写】直面标签
            "progress_value": 1.0,
            "bond_depth_delta": 0.05,          # 【架构对齐回写】羁绊深度变化
            "emotional_weight": 0.9,
            "angel_reaction": "sorrowful",
            "angel_response_delta": {
                "warmth": +0.08,
                "depth": +0.10,
                "vulnerability": +0.08
            },
            "memory_entry": {
                "choice_summary": "选择了'我也是这样过来的'",
                "recall_weight": 0.90,
                "recall_trigger": "self_disclosure"
            },
            "existence_protection": false,
            "narrative_jump": "ch04_c02_share"
        }
    ],
    
    "angel_advise_option": {                   # "问天使"选项（独立于options）
        "enabled": true,
        "advise_text_pool": [                  # 天使建议的文本池（可能有多条，随机或按上下文选取）
            "你觉得哪一个是真的你？不管你选什么，我都在。",
            "我不告诉你答案。但我告诉你——不管你说什么，我都听到了。"
        ],
        "advise_limit": 2                       # 最多可以"问天使"的次数（第二次天使说"听你心里的声音"）
    },
    
    "can_skip": false,                         # 此选择是否可以被"跳过已读"跳过
    "emotional_safety_note": null              # 情感安全备注（如有特殊处理需求）
}
```

### 4.2 选择历史记录

```python
# choice_history — 玩家的完整选择历史（存档持久化）
[
    {
        "choice_node_id": "ch01_c01",
        "selected_option_id": "ch01_c01_o02",
        "texture_tag": "gentle_patient",
        "chapter": 1,
        "sephirot_id": "ch01_kingdom",
        "timestamp": 1234567890,              # 游戏内时间戳
    },
    {
        "choice_node_id": "ch01_c02",
        "selected_option_id": "ch01_c02_o03",
        "texture_tag": "silent",
        "chapter": 1,
        "sephirot_id": "ch01_kingdom",
        "timestamp": 1234567950,
    },
    # ... 每次选择追加一条
]
```

### 4.3 天使回应映射

```python
# angel_response_profile — 由choice_history动态计算
# 计算时机：每次选择后重新计算
# 计算方式：遍历choice_history中所有选择的angel_response_delta，累加并归一化

def calculate_angel_response_profile(choice_history):
    profile = {
        "warmth": 0.5,          # 基线
        "depth": 0.3,
        "protectiveness": 0.4,
        "vulnerability": 0.2,
    }
    
    for entry in choice_history:
        option = get_option_by_id(entry["selected_option_id"])
        delta = option["angel_response_delta"]
        for key, value in delta.items():
            profile[key] = clamp(profile[key] + value, 0.0, 1.0)
    
    # Phase修正：根据当前章节强制调整某些维度
    current_chapter = get_current_chapter()
    if current_chapter >= 7:   # Phase 2 mid
        profile["vulnerability"] = max(profile["vulnerability"], 0.4)
    if current_chapter >= 13:  # Phase 2 late
        profile["vulnerability"] = max(profile["vulnerability"], 0.6)
        profile["depth"] = max(profile["depth"], 0.7)
    if current_chapter >= 15:  # Phase 3
        profile["warmth"] = max(profile["warmth"], 0.8)
    
    return profile
```

### 4.4 存在保护过滤规则

```python
# existence_protection_filter — 选择系统的存在保护过滤接口
# 由C5存在保护系统实现，C3选择系统在呈现选项前调用

def filter_choice_options(choice_node, choice_history, angel_state):
    """
    在选择菜单呈现前，检查每个选项是否需要存在保护过滤。
    返回过滤后的选项列表。
    """
    filtered_options = []
    
    for option in choice_node["options"]:
        if option["existence_protection"] == false:
            # 不需要过滤，直接保留
            filtered_options.append(option)
        else:
            # 需要过滤——检查玩家选择历史是否表明"走向虚无主义"的趋势
            nihilism_risk = calculate_nihilism_risk(choice_history, option)
            
            if nihilism_risk < NIHILISM_THRESHOLD:
                # 风险低于阈值，允许选择
                filtered_options.append(option)
            else:
                # 风险高于阈值——此选项被存在保护"转化"
                # 不是删除选项，而是替换为一个"天使拉回"的叙事节拍
                transformed_option = {
                    "id": option["id"] + "_protected",
                    "text": option["text"],  # 文本保留——玩家看到的是原选项
                    "texture_tag": "protected",
                    "progress_value": 0.5,   # 进度值降低（天使代为面对的一部分）
                    "emotional_weight": 0.8,
                    "angel_reaction": "resolute",
                    "narrative_jump": "angel_intervention_scene",  # 跳转到天使拉回的叙事
                    "memory_entry": {
                        "choice_summary": "选择了虚无主义选项，被天使拉回",
                        "recall_weight": 0.9,
                        "recall_trigger": "nihilism_protected"
                    }
                }
                filtered_options.append(transformed_option)
    
    return filtered_options


# 虚无主义风险评估
NIHILISM_THRESHOLD = 0.7

def calculate_nihilism_risk(choice_history, option):
    """
    评估选择此选项后，玩家是否走向虚无主义结局。
    考虑因素：
    1. 最近的逃避选择次数
    2. 最近的消极态度选择次数  
    3. 是否连续拒绝天使（关系选择中选择"沉默"/"不需要"）
    4. 当前选项本身的虚无主义倾向
    """
    recent_choices = choice_history[-10:]  # 最近10次选择
    
    avoidance_count = sum(1 for c in recent_choices if c["texture_tag"] in ["avoidant", "passive"])
    negative_attitude = sum(1 for c in recent_choices if c["texture_tag"] in ["nihilistic", "hopeless"])
    angel_rejection = sum(1 for c in recent_choices if c["texture_tag"] in ["reject_angel", "silent_withdraw"])
    
    base_risk = (avoidance_count * 0.15 + 
                 negative_attitude * 0.20 + 
                 angel_rejection * 0.25)
    
    option_risk = option.get("nihilism_tendency", 0.0)
    
    return min(base_risk + option_risk, 1.0)
```

---

## 5. 边界情况与错误处理

### 5.1 玩家反复选择同一类型

**场景**：玩家在所有选择中都选行动选择，或都选态度选择，或都选关系选择。

**处理**：
- **不限制**——玩家可以选择自己偏好的方式。这不是"bug"，而是玩家的表达方式。
- **天使会注意到**：如果连续5次以上选择同一类型，天使在主动对话中会温和地提及：
  - 全选行动选择："你总是先想'做什么'。有时候，也可以先想想'怎么想'。没关系的。"
  - 全选态度选择："你总是在想'为什么'。但有时候，直接去做也是一种答案。"
  - 全选关系选择："你总是先看我。但你也看看你自己——你也很重要。"
- *为什么这样设计*：不硬性纠正玩家的偏好，但通过天使的温和提醒，为玩家提供"也可以试试别的方式"的可能性。这符合"天使不批评，但提供新视角"的设计原则。

### 5.2 极端选择组合

**场景**：玩家的选择组合极为极端——如全部选择"勇敢直面"+全部选择"依赖天使"。

**处理**：
- `angel_response_profile`的多个维度同时达到极端值时，天使的行为出现"复合反应"：
  - `warmth > 0.8` + `protectiveness > 0.8`：天使同时非常温暖又非常保护——她的拥抱更紧、更频繁，但也开始担心你"太依赖她"。天使在Phase 2中段会说"你很勇敢，但你不需要一个人扛。也不需要只靠我——你也可以靠自己。"
  - `depth > 0.8` + `vulnerability > 0.8`：天使同时深沉又脆弱——她的对话变得非常私密、非常真实，但也会让玩家感到"天使好像在告别"。这为Phase 3的真相揭示提前建立了情感张力。
- **数值不设硬上限**：profile值可以到1.0，不会"溢出"或报错。
- *为什么这样设计*：极端选择组合产生独特的天使行为——这让"重玩"有价值。不同的选择风格会看到不同的天使面。

### 5.3 选择与叙事进度冲突

**场景**：玩家在"应该"面对某个情感主题的章节，选择了完全回避该主题的选项。

**处理**：
- **不强制**——玩家可以回避。选择不会被"否决"。
- **质点不点亮（或50%点亮）**：回避选择导致`progress_value`不足（<1.0），质点无法100%完成。
- **天使介入**：当同一质点内逃避选择累计3次，天使代为面对（详见存在保护系统GDD），质点点亮但亮度50%。
- **叙事循环**：逃避后，叙事不会跳过该质点——而是"循环"，天使提供新视角让玩家再次面对。
- *为什么这样设计*：回避是真实的情感反应——有些人确实还没有准备好面对某些事。游戏不强迫，但也不让回避成为永久的避风港。天使的介入既是保护（不让你永远卡住），也是邀请（下次也许可以试试面对）。

### 5.4 玩家在选择菜单中长时间不操作

**场景**：选择菜单出现后，玩家长时间不选择（超过2分钟）。

**处理**：
- **30秒**：天使立绘轻微转向玩家，表情变为`aching`（心疼）——她在等你。
- **60秒**：天使的浮动文本出现："没关系的，慢慢想。我不急。"——不催促。
- **120秒**：天使的浮动文本出现："如果你不知道选什么……就选你觉得最像你的那个。"——提供温和的引导。
- **不自动选择**：系统永远不会替玩家做选择（除了存在保护转化的虚无主义选项，那也是玩家自己选的，只是后果被改变了）。
- *为什么这样设计*：选择焦虑是真实的——有些玩家面对选择会犹豫很久。天使的等待和引导让"犹豫"本身成为被接纳的体验，而非被惩罚的行为。

### 5.5 最终选择的特殊处理

**场景**：Ch 16的最终选择——毁灭天使/拒绝毁灭/理解真相。

**处理**：
- **存在保护完全关闭**：最终选择不受存在保护过滤。三个选项都保留原样，不会被转化。
- **没有"问天使"选项**：这是心爱的自己的选择，天使不会给建议。天使只会说："不管你选什么，都没关系的。"
- **不可跳过**：最终选择不可被"跳过已读"跳过。
- **无时间限制**：玩家可以想多久就想多久。天使不会催促。
- **选择后不可撤销**：一旦选择，叙事直接进入对应结局。没有"你确定吗？"的确认。
  - *为什么不确认*：确认会让"最终选择"变成一个"可以被反悔的操作"，削弱了选择的重量。天使的"不管你选什么，都没关系的"已经提供了情感安全——不需要系统再提供"反悔"的安全。
- **觉醒结局的解锁条件**：`bond_depth >= 0.6`时解锁第三选项"理解真相——毁灭即转化"。如果bond_depth不足，第三选项显示为半透明+锁定状态，鼠标悬停显示"你还没有完全理解……"。
  - *为什么有解锁条件*：觉醒结局代表最深层的理解——它需要玩家在旅途中与天使建立了足够深的连接。这不是"好结局需要刷好感"，而是"深刻的理解需要真实的陪伴"。即使不解锁，前两个结局同样是"好的"。

---

## 6. 系统集成点

### 6.1 与天使陪伴系统（C2）的接口

```
接口名称：angel_advise(choice_node_id)
调用方：C3选择系统
被调方：C2天使陪伴系统
触发时机：玩家在选择菜单中选择"问天使"
输入：choice_node_id
输出：angel_advice_text
说明：详见天使陪伴系统GDD §6.1
```

```
接口名称：update_angel_response(choice_node_id, selected_option_id)
调用方：C3选择系统
被调方：C2天使陪伴系统
触发时机：玩家做出选择后
输入：choice_node_id, selected_option_id
输出：无
副作用：
  - C2根据selected_option的angel_response_delta更新angel_response_profile
  - C2根据selected_option的angel_reaction设置天使即时情感反应
  - C2将memory_entry存入angel_memories（如果recall_weight > 阈值）
  - C2更新active_dialogue_pool（基于新的context_tags）
```

### 6.2 与质点进程系统（C4）的接口

```
接口名称：add_sephirot_progress(sephirot_id, progress_value, confrontation_tag)
调用方：C3选择系统
被调方：C4质点进程系统
触发时机：玩家做出选择后
输入：sephirot_id（质点ID）、progress_value（进度值0.0-1.0）、confrontation_tag（直面标签ENGAGE/ESCAPE/NEUTRAL/null）
输出：sephirot_completed（bool，质点是否已完成）
副作用：
  - 【架构对齐回写】confrontation_tag 被 C4 消费（驱动完成判定和逃避计数）；progress_value 被 C4 消费（进度更新）
  - C4根据 confrontation_tag 判定：
    - ENGAGE → progress +1.0 → COMPLETED_FULL → 解锁下一质点
    - ESCAPE → progress +0.3 → 逃避计数+1 → 第3次ESCAPE → 天使代为面对 → COMPLETED_HALF
    - NEUTRAL → progress +0.0 → 天使提供视角 → 重新选择
    - null（非直面选择）→ 仅累加 progress_value，不影响逃避计数
  - 如果进度达到1.0，C4点亮质点并通知C1叙事引擎进入下一章
  - 如果进度未达1.0，C4通知C1继续当前质点的叙事（循环或推进）
```

### 6.3 与存在保护系统（C5）的接口

```
接口名称：filter_choice_options(choice_node, choice_history)
调用方：C3选择系统
被调方：C5存在保护系统
触发时机：选择菜单呈现前
输入：choice_node（选择节点数据）、choice_history（完整选择历史）
输出：filtered_options（过滤后的选项列表）
说明：详见本GDD §4.4
```

```
接口名称：check_angel_intervention_needed(choice_node_id, selected_option_id)
调用方：C3选择系统
被调方：C5存在保护系统
触发时机：玩家选择一个被存在保护标记的选项后
输入：choice_node_id, selected_option_id
输出：needs_intervention（bool）、intervention_type（暗流类型）
副作用：
  - 如果needs_intervention为true，C5触发天使介入流程
  - C5调用C2的angel_intervene接口
  - 介入完成后，C5通知C3继续叙事（跳转到angel_intervention_scene）
```

---

## 7. 叙事集成

### 7.1 每章选择数量建议

| 章节 | 选择数量 | 类型分布 | 说明 |
|------|---------|---------|------|
| Ch 1 | 2 | 1行动 + 1关系 | 教学章——教会选择系统和天使互动 |
| Ch 2 | 2 | 1态度 + 1行动 | 巩固选择习惯 |
| Ch 3 | 2 | 1行动 + 1关系 | Phase 1收尾 |
| Ch 4 | 3 | 1态度 + 1关系 + 1行动 | Phase 2开篇——选择数量增加 |
| Ch 5 | 2-3 | 1态度 + 1行动 | 虚无主义主题——态度选择是核心 |
| Ch 6 | 3 | 1行动 + 1关系 + 1态度 | 共情过载——关系选择开始增多 |
| Ch 7 | 3 | 1态度 + 1关系 + 1行动 | 超我审判——态度选择是核心 |
| Ch 8 | 2-3 | 1行动 + 1态度 | 自我伤害——行动选择最重要（紧急性） |
| Ch 9 | 3 | 1态度 + 1关系 + 1行动 | 真相主题——关系选择引入天使暗示 |
| Ch 10 | 3 | 1行动 + 1关系 + 1态度 | 严厉——态度选择引入"边界"概念 |
| Ch 11 | 3 | 1态度 + 1关系 + 1行动 | 慈悲——关系选择是核心（天使落泪） |
| Ch 12 | 2-3 | 1态度 + 1关系 | 理智——关系选择是核心（天使声音变远） |
| Ch 13 | 2 | 1身份选择 + 1关系选择 | 真我——特殊：身份选择（四选项，非三选项） |
| Ch 14 | 2 | 1态度 + 1关系 | 真相揭示——选择数量减少（沉重感） |
| Ch 15 | 2 | 1态度 + 1关系 | 终极真相——选择很简短但极重 |
| Ch 16 | 1 | 最终选择（三选项） | 最终选择——无类型标记，无"问天使" |

**总量**：约35-40个选择节点，分布在16章中。

### 7.2 关键选择点设计原则

1. **选择必须在情感高点之后呈现**：不是"遇到问题→选择"，而是"感受痛苦→天使安慰→选择"。选择出现在玩家已经情感投入之后，而非之前。
2. **选择的提示文本应该是角色的话或内心独白，而非系统语言**：不是"你要如何拯救白花？"，而是白花说"我是不是多余的？"——然后玩家选择如何回应。这让选择感觉是对话而非考试。
3. **选项文本应该是第一人称的**：选项是心爱的说的话/做的事/想的念头，用"我"或直接的动作描述。如"'你不是错的'"而非"告诉白花她不是错的"。
4. **每个选择节点至少有一个"温暖"选项**：即使面对最黑暗的主题，也至少有一个选项是"向温暖靠近"的。这不意味着其他选项是"冷的"——只是确保温暖始终可达。
5. **避免"显然正确"的选项**：如果有一个选项明显比其他"更道德"或"更正确"，它就不是好的选择设计。每个选项都应该有其合理性——即使是"逃避"选项，也是真实的情感反应。

### 7.3 选择对结局的影响机制

```
结局判定流程：

Ch 16 最终选择
    │
    ├── 选项1："毁灭天使，完成代价"
    │   └── → 融合结局（Fusion Ending）
    │       结局细节纹理由angel_response_profile调整：
    │       - warmth高 → 融合过程更温暖、更完整
    │       - depth高 → 心爱的的独白更深沉
    │       - vulnerability高 → 天使的最后一句话更私密
    │
    ├── 选项2："拒绝毁灭，承受代价"
    │   └── → 守护结局（Guardian Ending）
    │       结局细节纹理由angel_response_profile调整：
    │       - protectiveness高 → 守护的重量更重
    │       - warmth高 → 天使虽然有限但更温柔
    │
    └── 选项3："理解真相——毁灭即转化"（需bond_depth >= 0.6）
        └── → 觉醒结局（Awakening Ending）
            结局细节纹理由angel_response_profile调整：
            - depth最高 → 心爱的的理解最深刻
            - vulnerability高 → 天使的"你终于明白了"最动人
```

**bond_depth的计算**：

```python
# bond_depth由以下因素累加：
# 1. 关系选择中选择"靠近天使"的次数 × 0.05
# 2. 关系选择中选择"回握/抱住/擦泪"等主动亲密行为 × 0.08
# 3. 主动寻求拥抱的次数 × 0.02（每质点最多计3次）
# 4. 在选择中选择"问天使"的次数 × 0.03（每质点最多计1次）
# 5. Chapter 13身份选择中选择"我都是" × 0.15（关键加分项）
# 6. Chapter 14-15关系选择中选择"抱住她" × 0.10

# bond_depth初始为0.0，最高1.0
# 觉醒结局解锁阈值：0.6
```

*为什么bond_depth影响结局解锁而非"结局好坏"*：三种结局都是"好的"——bond_depth不是"好感度"或"道德值"，它衡量的是"你与天使建立了多深的连接"。更深的连接让你能理解更深层的真相（毁灭即转化），但这不意味着"更浅的连接"得到的结局"更差"——融合结局和守护结局同样是完整的、好的结局。

---

## 8. 可访问性与安全

### 8.1 选择不导致惩罚

**核心原则**：选择系统绝不惩罚玩家。

- **没有"错误选择"**：所有选择都推进游戏。没有任何选择导致"Game Over"或"坏结局"。
- **没有"错过"机制**：如果玩家没有选择某个选项，后续不会出现"你因为没有选X所以失去了Y"的惩罚。天使的回应会不同，但不同的回应都是"好的"——只是纹理不同。
- **逃避不被惩罚**：逃避选择导致质点50%完成而非"失败"。天使代为面对不是"惩罚你逃避"，而是"帮你分担"。
- *为什么这样设计*：苞苞的创伤中包含"做错了就被惩罚"的恐惧。选择系统不惩罚任何选择，是对"你的感受和选择都是被允许的"的系统化肯定。

### 8.2 选择文案的清晰度

- **选项文本使用简短、直接的语言**：每个选项不超过15个汉字。长文本容易让玩家"读不完"或"理解偏差"。
- **选项之间有明确的语义区分**：三个选项不应该是"同一意思的三种说法"——它们应该代表真正不同的态度/行动/关系取向。
- **避免模糊到无法理解**：选项可以有诗意，但不能晦涩到玩家不知道自己在选什么。如"'……沉默'"是可理解的（选择沉默），但"'也许一切终将消逝'"太模糊（不知道在选什么）。
- **提供类型标记帮助理解**：选择类型图标（行动/态度/关系）帮助玩家理解选择的维度。

### 8.3 存在保护对选择的过滤规则

**存在保护系统(C5)对选择系统(C3)的过滤规则**：

1. **过滤只针对虚无主义倾向**：存在保护只过滤可能导致"虚无主义结局"的选择组合。普通的"消极"、"逃避"、"自私"选择**不被过滤**——它们是真实的情感反应，有对应的叙事路径。
2. **过滤不是删除，而是转化**：被存在保护标记的选项不会被从菜单中移除。玩家可以选择它——但选择后的叙事后果被转化为"天使拉回"的场景，而非虚无主义结局。
3. **过滤是累积的**：单次选择不会触发过滤。只有当选择历史表现出"走向虚无主义"的累积趋势时，过滤才激活。
4. **最终选择不被过滤**：Ch 16的三个结局选择完全不受存在保护过滤。
5. **过滤以叙事方式呈现**：玩家不会看到"系统提示：此选择已被存在保护拦截"。玩家看到的是：选择了某选项 → 天使拥抱心爱的 → 天使说"我不能让你走到那里。不是因为规则，是因为我爱你。" → 叙事继续。

### 8.4 选择焦虑的缓解

- **天使的"不管你选什么，都没关系的"**：在选择菜单出现时（特别是关键选择），天使的被动行为中包含一个轻微的安慰动作（如微笑、微微点头），传递"不管你选什么，我都在"的信息。
- **没有时间限制**：所有选择都没有倒计时。玩家可以想多久就想多久。
- **"问天使"作为安全出口**：如果玩家真的不知道选什么，"问天使"提供一个获取视角的通道。
- **选择后不后悔**：选择一旦做出不可撤销，但天使会在后续叙事中让玩家感到"这个选择也是好的"——无论选了什么，天使的回应都是接纳的。

---

> **文档结束**
>
> 本GDD定义了选择系统的完整设计规格。关键决策记录：
> 1. "情感共振选择"模型——无正确答案，选择改变纹理而非通关路径
> 2. 三种选择类型（行动/态度/关系）有明确的情感维度区分和章节分布
> 3. 【架构对齐回写】选项数据结构新增 confrontation_tag（ENGAGE/ESCAPE/NEUTRAL/null）和 bond_depth_delta 字段，与 C4 质点进程系统对齐
> 4. 选择后果延迟呈现——以天使的记忆引用和回应变化为主要反馈
> 5. 存在保护只过滤虚无主义倾向，不过滤普通的消极/逃避选择
> 6. 最终选择不受保护，觉醒结局需要bond_depth >= 0.6
> 7. 选择系统绝不惩罚玩家——所有选择都是"有效的"
>
> 待协调项：
> - 与narrative-writer确认35-40个选择节点的完整文本编写
> - 与code-architect确认choice_node数据结构的Ren'Py实现方案
> - 与C5存在保护系统GDD对齐：虚无主义风险评估的阈值和计算方式需一致
> - 与C4质点进程系统GDD对齐：progress_value的累加逻辑和质点完成判定需一致

---

## 架构对齐记录

> **回写日期**：2025-07-30
> **回写人**：文策渊（design-strategist）
> **对齐依据**：`docs/architecture/main-architecture.md` §5.3 统一选项数据结构

### 回写内容

本次回写将 C3 选择系统 GDD 的选项数据结构与主架构文档 §5.3 对齐，新增 `confrontation_tag` 和 `bond_depth_delta` 字段，以解决 Phase 4 审查中发现的 CONCERN 2（C3 与 C4 选项数据结构不一致）。

#### 修改的章节

| 章节 | 修改内容 |
|------|---------|
| §2.2 选择不设正确答案 | 新增 `confrontation_tag` 字段说明及其与 `progress_value` 的映射关系（ENGAGE→1.0, ESCAPE→0.3, NEUTRAL→0.0） |
| §4.1 选择节点数据结构 | 三个选项示例均新增 `confrontation_tag` 和 `bond_depth_delta` 字段 |
| §6.2 与质点进程系统接口 | `add_sephirot_progress` 接口新增 `confrontation_tag` 参数，明确 C4 消费逻辑 |

#### 核心变更

1. **新增字段 `confrontation_tag`**：枚举值 `ENGAGE`/`ESCAPE`/`NEUTRAL`/`null`，被 C4 质点进程系统消费，驱动完成判定和逃避计数
2. **新增字段 `bond_depth_delta`**：浮点数，表示选择对羁绊深度的影响，被 C2 天使陪伴系统消费
3. **明确消费关系**：`confrontation_tag` → C4（完成判定）；`progress_value` → C4（进度更新）；`bond_depth_delta` → C2（羁绊更新）
4. **冗余设计确认**：`confrontation_tag` 与 `progress_value` 存在语义重叠（ENGAGE→1.0），但有意保留——`confrontation_tag` 驱动 C4 逻辑，`progress_value` 作为通用进度值，非直面选择时两者解耦

#### 未修改的部分

- 三种选择类型定义（§2.1）保持不变
- 天使回应映射（§2.3）保持不变
- 存在保护过滤规则（§4.4）保持不变
- 所有叙事内容保持不变
