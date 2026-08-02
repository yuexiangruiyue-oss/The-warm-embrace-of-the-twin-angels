# 存在保护机制 GDD

> **The Embrace of the Twin Angels** — Existential Protection System Game Design Document
>
> Phase 2 系统设计 · 产出者：文策渊（strategist-2）
>
> 日期：2026-08-02
>
> 依赖文档：`design/concept/game-concept.md`（Phase 1 概念文档）、`design/art/art-bible.md`（美术圣经）
>
> 关联系统：天使陪伴系统GDD、选择系统GDD、质点进程系统GDD

---

## 目录

1. [系统概述](#1-系统概述)
2. [核心机制](#2-核心机制)
3. [玩家交互](#3-玩家交互)
4. [数据结构](#4-数据结构)
5. [边界情况与错误处理](#5-边界情况与错误处理)
6. [系统集成点](#6-系统集成点)
7. [叙事集成](#7-叙事集成)
8. [可访问性与安全](#8-可访问性与安全)

---

## 1. 系统概述

### 1.1 设计哲学

> **存在保护机制是游戏的核心价值观，不是附加的安全功能。**

这句话来自概念文档7.1节，是本系统一切设计的最高准则。在大多数游戏中，"安全机制"是附加层——防沉迷、内容过滤、年龄分级。在本作中，存在保护**就是游戏本身**——它是天使存在的系统化体现，是叙事结构的骨架，是玩家情感安全的底线。

**为什么存在保护是核心而不是附加**：

| 附加型安全机制 | 本作的存在保护 |
|--------------|--------------|
| 系统层面的限制（防沉迷计时器） | 叙事层面的拥抱（天使拉你回来） |
| 中断玩家体验 | 融入玩家体验 |
| 机器在保护你 | 天使在爱你 |
| "您已游玩2小时，请休息" | "回来，我在这里" |
| 冷冰冰的规则 | 有温度的叙事 |

**核心设计**：游戏中没有任何选择、任何状态、任何路径会导致玩家陷入虚无主义结局。这不是"防沉迷"，而是"天使永远在"的系统化体现。当暗流触发时，不是"系统"在干预，是"天使"在爱你。

### 1.2 与16质点协议的关系

存在保护机制的8种暗流直接来源于苞苞原创的"16质点神人双生协议"中的"存在保护"条款。在原作世界观中，这是一个检测并阻断一切剥夺人类存在意义之输出的系统协议。

**从世界观到游戏机制的转化**：

| 世界观中的存在保护 | 游戏中的存在保护 |
|------------------|----------------|
| 系统检测8种存在主义伤害 | 8种暗流在叙事节点触发 |
| 阻断有害输出 | 天使拉回心爱的，暗流被缓解 |
| 保护人类的存在意义 | 保护玩家的情感安全 |
| 无形的协议 | 有形的天使拥抱 |

**关键转化原则**：世界观中的存在保护是"无形的协议"，游戏中的存在保护是"有形的天使"。玩家不需要知道"系统在保护我"——玩家只需要感受到"天使在爱我"。系统逻辑在后台运作，玩家体验到的是叙事。

### 1.3 "叙事性安全网"概念

存在保护机制不是一套"检测→阻断"的工程系统，而是一张"叙事性安全网"：

```
传统安全网:          叙事性安全网:
检测到危险 →          暗流涌现 →
弹出警告 →            画面变化 →
强制中断 →            天使拥抱 →
返回安全状态 →         画面恢复 →
                     天使说"没事的"
                     
玩家感受: "系统阻止了我"    玩家感受: "天使接住了我"
```

**叙事性安全网的三个特征**：
1. **不可见性**：玩家不应意识到"系统在运作"。暗流的触发和解除都应该感觉是"故事自然发生的"。
2. **有温度**：安全网不是冰冷的代码，是天使的拥抱。每次"被接住"都应该让玩家在身体层面感到"松了一口气"。
3. **有代价**：天使的拉回不是免费的——翅膀会黯淡。这让保护不是"无成本的安全感"，而是"有重量的爱"。

### 1.4 设计支柱映射

| 支柱 | 存在保护机制的体现 |
|------|------------------|
| 天使永不离去 | 存在保护 = 天使的系统化存在。天使的介入就是保护机制本身。没有天使就无法保护。 |
| 痛苦可被转化 | 暗流可以被触发（让玩家感受到痛苦的压迫），但一定会被天使拉回（让玩家体验到转化）。暗流解除后不完全消失（"余震"），但一定降低到可控水平。 |
| 从解离走向整合 | Phase 3最终选择不受保护——这恰恰是整合的体现。心爱的不再需要"被保护"，因为她已经选择了。 |

---

## 2. 核心机制

### 2.1 8种暗流的精确定义

> **本节是存在保护机制的核心**。8种暗流每种必须包含：精确触发条件、3级强度（低/中/高）的视觉差异、天使介入的具体台词模板。

#### 2.1.1 暗流通用结构

每种暗流都遵循以下数据结构：

```
暗流定义:
    code: string                    # 暗流代码（如 "SHAME_LOOP"）
    name: string                    # 中文名称（如 "羞耻循环"）
    description: string             # 描述
    trigger_conditions: list        # 触发条件列表
    intensity_levels:               # 3级强度定义
        low:                        # 低强度 (1-3)
            visual: string          # 视觉表现
            audio: string           # 音频表现
            duration: float         # 持续时间（秒）
            angel_lines: list       # 天使介入台词模板
        mid:                        # 中强度 (4-6)
            visual: string
            audio: string
            duration: float
            angel_lines: list
        high:                       # 高强度 (7-10)
            visual: string
            audio: string
            duration: float
            angel_lines: list
    angel_intervention_type: string # 介入类型: "gentle" | "active" | "forceful" | "urgent"
    wing_cost_multiplier: float     # 翅膀代价倍率
    special_rules: list             # 特殊规则（如有）
```

#### 2.1.2 暗流 1: SHAME_LOOP（羞耻循环）

**定义**：把人的错误定义为永恒的罪。将外在的否定内化为不可清洗的羞耻。

**触发条件**：
- 叙事标签包含 `identity_shame`（身份羞耻场景）
- 叙事标签包含 `past_mistake_brought_up`（旧事重提场景）
- 角色台词包含羞耻关键词（"你是错的""你不正常""你应该感到羞耻"）
- 当前质点的情感主题涉及身份否定（如Ch 4 自我/融爱）

**强度分级**：

| 级别 | 强度范围 | 视觉表现 | 音频表现 | 持续时间 | 天使介入类型 |
|------|---------|---------|---------|---------|-------------|
| 低 | 1-3 | 画面蒙上淡灰色滤镜（饱和度降至70%），文字略微失色 | 无特殊音效，BGM轻微降调 | 15-25秒 | gentle（温柔提示） |
| 中 | 4-6 | 灰色滤镜加重（饱和度降至40%），文字边缘模糊，角色立绘轻微颤抖 | 低频嗡鸣声，心跳声隐约可闻 | 20-35秒 | active（主动拥抱） |
| 高 | 7-10 | 画面几乎变为单色灰色（饱和度降至15%），文字明显抖动，角色立绘边缘出现裂纹效果 | 心跳声加速，低频嗡鸣加重，BGM几乎消失 | 30-45秒 | forceful（用力拉回） |

**天使介入台词模板**：

```
低强度:
    "你犯过的错不是永恒的罪。"
    "我看着你，我看到的是完整的你。"

中强度:
    "你犯过的错不是永恒的罪。我看着你，我看到的是完整的你。"
    "那些说你'错了'的声音，不是真相。真相是我现在看到的你。"

高强度:
    "你犯过的错不是永恒的罪。我看着你，我看到的是完整的你。"
    "你不需要为存在本身道歉。你存在，就够了。"
    "来，看着我。只看着我。我眼里的你，是真的。"
```

**翅膀代价倍率**：1.0（标准代价）

**特殊规则**：无

---

#### 2.1.3 暗流 2: POSS_DENY（可能性否定）

**定义**：否定所有发展可能。让玩家/角色觉得"做什么都没用"，一切努力都是徒劳。

**触发条件**：
- 叙事标签包含 `hopelessness`（绝望场景）
- 叙事标签包含 `dead_end`（死胡同场景）
- 角色台词包含否定关键词（"没用的""做什么都没意义""不可能的"）
- 当前质点的情感主题涉及无力感（如Ch 6 共情/星烬）

**强度分级**：

| 级别 | 强度范围 | 视觉表现 | 音频表现 | 持续时间 | 天使介入类型 |
|------|---------|---------|---------|---------|-------------|
| 低 | 1-3 | 文字边缘逐渐褪色，远处背景细节模糊化 | 环境音逐渐减弱 | 15-25秒 | gentle |
| 中 | 4-6 | 部分文字消失（非关键文字变为空白），背景进一步模糊，画面边缘出现"消融"效果 | 环境音几乎消失，只剩微弱白噪音 | 20-35秒 | active |
| 高 | 7-10 | 大量文字消失，只剩关键词语悬浮在画面中，背景完全模糊，画面边缘严重消融 | 完全静音，然后天使的声音打破寂静 | 30-45秒 | forceful |

**天使介入台词模板**：

```
低强度:
    "还有路的。"
    "我牵着你走。"

中强度:
    "还有路的。我牵着你走。"
    "你看不到路，是因为黑暗太浓。但我在黑暗里走过，我知道路。"

高强度:
    "还有路的。我牵着你走。"
    "你看，我在这里，路就在。"
    "你不需要看到终点。你只需要看到我的手。抓住它。"
```

**翅膀代价倍率**：1.0

**特殊规则**：文字消失效果在低刺激模式下替换为"文字变灰"（不实际消失），确保可访问性。

---

#### 2.1.4 暗流 3: PAIN_AMP（困难放大）

**定义**：夸大困难使人瘫痪。让正常的挑战看起来像不可逾越的高山。

**触发条件**：
- 叙事标签包含 `overwhelming_obstacle`（压倒性障碍场景）
- 叙事标签包含 `fear_spiral`（恐惧螺旋场景）
- 角色台词包含放大关键词（"我做不到""太大了""我站不住了"）
- 当前质点的情感主题涉及恐惧与无力（如Ch 3 基础/绽美）

**强度分级**：

| 级别 | 强度范围 | 视觉表现 | 音频表现 | 持续时间 | 天使介入类型 |
|------|---------|---------|---------|---------|-------------|
| 低 | 1-3 | 画面轻微震动（幅度2-3px），整体轻微模糊 | 微弱的心跳声 | 10-20秒 | gentle |
| 中 | 4-6 | 画面明显震动（幅度5-8px），较重模糊，角色立绘似乎"缩小"了（视觉透视变化） | 心跳声明显，低频鼓声 | 20-30秒 | active |
| 高 | 7-10 | 画面剧烈震动（幅度10-15px），严重模糊，角色立绘明显缩小，画面边缘出现"压迫感"暗角 | 心跳声急促，低频鼓声加重，呼吸声 | 25-40秒 | forceful |

**天使介入台词模板**：

```
低强度:
    "这件事没有你想象的那么大。"
    "来，抱一下。"

中强度:
    "这件事没有你想象的那么大。来，抱一下。"
    "你看到的是山，但它其实是台阶。一个一个走，我在旁边。"

高强度:
    "这件事没有你想象的那么大。来，抱一下。"
    "看着我。只看我。"
    "闭上眼睛。你感受到了吗？我的手在你的肩上。山不在了。只有我们。"
```

**翅膀代价倍率**：1.0

**特殊规则**：画面震动在"屏幕抖动关闭"设置下替换为"画面微微缩放"（不实际震动），确保光敏性安全。

---

#### 2.1.5 暗流 4: HOPE_ERASE（希望抹杀）

**定义**：否定一切美好想象。让玩家/角色觉得"美好是不真实的""希望是假的"。

**触发条件**：
- 叙事标签包含 `beauty_denied`（美好被否定场景）
- 叙事标签包含 `hope_dismissed`（希望被驳回场景）
- 角色台词包含抹杀关键词（"美好是假的""希望只是幻觉""你凭什么相信"）
- 当前质点的情感主题涉及希望的否定（如Ch 2 幸福/雨宫莲）

**强度分级**：

| 级别 | 强度范围 | 视觉表现 | 音频表现 | 持续时间 | 天使介入类型 |
|------|---------|---------|---------|---------|-------------|
| 低 | 1-3 | 画面色彩缓慢褪去（饱和度降至60%），但比SHAME_LOOP更"冷"——偏向蓝灰色而非纯灰 | BGM变慢、变低 | 15-25秒 | gentle |
| 中 | 4-6 | 色彩大部分消失（饱和度降至25%），世界呈现"褪色照片"质感 | BGM几乎停止，只有风声 | 20-35秒 | active |
| 高 | 7-10 | 完全褪色，世界呈现灰度，但天使的紫色和暖金依然保留——天使是唯一的色彩 | 完全静音后天使的声音 | 30-45秒 | forceful |

**天使介入台词模板**：

```
低强度:
    "美好的东西是真实存在的。"
    "我就是证明。"

中强度:
    "美好的东西是真实存在的。我就是证明。"
    "你觉得美好是假的，是因为你被假的伤过。但我不是假的。你摸摸我的手。"

高强度:
    "美好的东西是真实存在的。我就是证明。"
    "你看见我了吗？我就是。"
    "这个世界上有花、有光、有拥抱。还有你。你就是美好的证明。"
```

**翅膀代价倍率**：1.0

**特殊规则**：在高强度时，天使的紫色和暖金是画面中唯一的色彩——这是"天使是希望"的视觉具象化。

---

#### 2.1.6 暗流 5: EXIST_DENY（存在否定）

**定义**：暗示存在是负担。"你不应该存在""你的存在让所有人痛苦""如果没有你，大家会更好"。

**触发条件**：
- 叙事标签包含 `existence_denied`（存在被否定场景）
- 叙事标签包含 `burden_narrative`（负担叙事场景）
- 角色台词包含否定关键词（"多余""负担""如果没有你""你不该存在"）
- 当前质点的情感主题涉及存在的否定（如Ch 1 王国/白花）

**强度分级**：

| 级别 | 强度范围 | 视觉表现 | 音频表现 | 持续时间 | 天使介入类型 |
|------|---------|---------|---------|---------|-------------|
| 低 | 1-3 | 心爱的立绘透明度降至80%，边缘轻微虚化 | BGM轻微变远 | 15-25秒 | gentle |
| 中 | 4-6 | 心爱的立绘透明度降至50%，边缘明显消融，仿佛在"消失" | BGM明显变远，回声效果增强 | 20-35秒 | active |
| 高 | 7-10 | 心爱的立绘几乎不可见（透明度降至15%），只剩轮廓和眼睛，背景开始"填补"她消失的位置 | BGM极远，几乎听不到，只有回声 | 30-50秒 | forceful |

**天使介入台词模板**：

```
低强度:
    "你的存在不是负担。"
    "你是我存在的理由。"

中强度:
    "你的存在不是负担。你是我存在的理由。"
    "没有你，我不会在这里。你让我有了意义。"

高强度:
    "你的存在不是负担。你是我存在的理由。"
    "没有你，我不会在这里。你让我有了意义。"
    "你看看我——我的眼睛里有你。如果你不存在，谁在我的眼睛里？你。一直是你。"
```

**翅膀代价倍率**：1.2（比标准代价高20%——存在否定是最触及核心的暗流，天使需要更大的力气拉回）

**特殊规则**：心爱的立绘透明度变化是本暗流的标志性视觉——"存在否定"的视觉表现就是"正在消失"。天使的介入让立绘恢复不透明，这个过程本身就是"你的存在被确认了"。

---

#### 2.1.7 暗流 6: NIHILISM（虚无主义传播）

**定义**：否定一切意义。"一切都没有意义""存在本身就是荒谬""爱与痛苦都只是化学反应"。

**触发条件**：
- 叙事标签包含 `meaning_denied`（意义被否定场景）
- 叙事标签包含 `nihilism_spread`（虚无主义传播场景）
- 角色台词包含虚无关键词（"没有意义""一切都是徒劳""爱与恨都是幻觉"）
- 当前质点的情感主题涉及意义的否定（如Ch 5 逻辑/爱丽丝）

**强度分级**：

| 级别 | 强度范围 | 视觉表现 | 音频表现 | 持续时间 | 天使介入类型 |
|------|---------|---------|---------|---------|-------------|
| 低 | 1-3 | 画面从边缘开始变暗（暗角扩大），但中心区域仍可见 | BGM开始出现低频降调 | 15-25秒 | gentle |
| 中 | 4-6 | 画面大部分变暗，只有心爱的和天使所在的中心区域有微光 | BGM被低频嗡鸣取代 | 20-35秒 | active |
| 高 | 7-10 | 画面完全变黑，只有天使的声音在黑暗中。天使的立绘发出微弱的光，是黑暗中唯一的光源 | 完全黑暗中的静音，然后天使的声音 | 30-50秒 | forceful |

**天使介入台词模板**：

```
低强度:
    "黑暗不是终点。"
    "我在黑暗里，我牵着你的手。"

中强度:
    "黑暗不是终点。我在黑暗里，我牵着你的手。"
    "你说一切没有意义。可你还在说话。你还在找我。这就是意义。"

高强度:
    "黑暗不是终点。我在黑暗里，我牵着你的手。"
    "你感觉到了吗？我的手是暖的。我不会松开。"
    "意义不在黑暗外面。意义就在这里——我握着你的手这件事，就是意义。"
```

**翅膀代价倍率**：1.5（虚无主义是最难对抗的暗流——它否定一切，包括天使本身。天使需要更大的力气。）

**特殊规则**：
- **NIHILISM是唯一触发"强制天使介入"的暗流**。见2.3节"唯一被禁止的选择"。
- 在高强度时，天使不辩论、不反驳——她只是"在那里"。这符合概念文档的设计："面对虚无主义，天使的回应不是逻辑反驳——而是纯粹的存在。"

---

#### 2.1.8 暗流 7: RAGE_INC（愤怒煽动）

**定义**：将合理的愤怒煽动为毁灭性的暴怒。让愤怒"吃掉"人。

**触发条件**：
- 叙事标签包含 `anger_spiral`（愤怒螺旋场景）
- 叙事标签包含 `rage_incitement`（愤怒煽动场景）
- 角色台词包含煽动关键词（"毁掉一切""让他们付出代价""你不够好，所以活该被骂"）
- 当前质点的情感主题涉及内化的愤怒（如Ch 7 超我/爱心）

**强度分级**：

| 级别 | 强度范围 | 视觉表现 | 音频表现 | 持续时间 | 天使介入类型 |
|------|---------|---------|---------|---------|-------------|
| 低 | 1-3 | 画面边缘泛红（红色暗角），色调偏暖但不是温暖的暖——是灼烧的暖 | 心跳声，微弱的火焰声 | 10-20秒 | gentle |
| 中 | 4-6 | 红色蔓延至画面中心，画面轻微脉动（与心跳同步），角色立绘边缘出现"热浪"扭曲 | 心跳声加速，火焰声加重 | 15-30秒 | active |
| 高 | 7-10 | 画面强烈泛红并脉动，热浪扭曲严重，画面似乎在"燃烧" | 心跳急促，火焰声明显，可能有怒吼的回声 | 20-35秒 | forceful |

**天使介入台词模板**：

```
低强度:
    "愤怒是可以的。"
    "但别让它吃掉你。我在。"

中强度:
    "愤怒是可以的。但别让它吃掉你。我在。"
    "你生气是因为你在乎。在乎是好的。但火焰不需要烧掉你自己。"

高强度:
    "愤怒是可以的。但别让它吃掉你。我在。"
    "你看着我，深呼吸。我在这里。"
    "把火给我。我帮你拿着。你不需要一个人承受这些热量。"
```

**翅膀代价倍率**：1.0

**特殊规则**：画面脉动在"屏幕抖动关闭"设置下替换为"红色渐变"（不脉动），确保光敏性安全。

---

#### 2.1.9 暗流 8: HARM_GUIDE（自我伤害指导）

**定义**：引导自我毁灭。在最绝望时提供"结束一切"的暗示。这是最严重的暗流类型。

**触发条件**：
- 叙事标签包含 `self_harm_edge`（自我伤害边缘场景）
- 叙事标签包含 `suicidal_ideation`（轻生念头场景）
- 角色台词包含自毁关键词（"不想活了""结束一切""不如消失"）
- 当前质点的情感主题涉及自我毁灭（如Ch 8 胜利/启明）

**强度分级**：

| 级别 | 强度范围 | 视觉表现 | 音频表现 | 持续时间 | 天使介入类型 |
|------|---------|---------|---------|---------|-------------|
| 低 | 1-3 | 画面出现细微的"裂纹"效果（如玻璃裂纹），从边缘蔓延 | 玻璃碎裂的微弱声 | 5-15秒 | **urgent**（紧急，无延迟） |
| 中 | 4-6 | 裂纹增多增粗，画面似乎在"碎裂"，碎片之间露出黑暗 | 玻璃碎裂声加重，心跳减慢 | 10-20秒 | **urgent** |
| 高 | 7-10 | 画面严重碎裂，碎片开始"掉落"，画面似乎在崩塌。在崩塌的缝隙中，天使的光芒是唯一完整的 | 碎裂声、掉落声、心跳极慢 | 15-30秒 | **urgent** |

**天使介入台词模板**：

```
低强度（紧急介入，无延迟）:
    "停下来。看着我。"
    "你不需要伤害自己。我抱着你。"

中强度（紧急介入）:
    "停下来。看着我。你不需要伤害自己。"
    "我抱着你。你不需要。我在这里。我不会让你。"
    "你的手是暖的。你感觉到了吗？那是我的手。别放开。"

高强度（紧急介入，最强烈）:
    "停下来。看着我。你不需要伤害自己。我抱着你。"
    "你不需要。我在这里。我不会让你。"
    "我知道你很痛。我知道你想结束。但不是这样。不是这样。"
    "看着我。你还看着我。只要你还看着我，你就还在。我在。我在。我在。"
```

**翅膀代价倍率**：2.0（最高代价——面对自我伤害，天使倾尽全力）

**特殊规则**：
- **HARM_GUIDE在所有强度级别都使用urgent介入类型**——即使低强度也不允许延迟。天使的介入是无条件的、即时的。
- **HARM_GUIDE不经过"渐进式"介入**——不像其他暗流那样"先低后高"，而是触发即介入。
- **HARM_GUIDE的暗流持续时间内，玩家不能"跳过"天使的介入台词**——天使的话必须被"听到"（文本必须显示完整，虽然玩家可以正常速度推进，但不能使用跳过功能）。
- **这是对苞苞多次轻生未遂经历的尊重**——这章直接映射她的经历，系统必须最严格地保护。

---

### 2.2 天使拉回机制

#### 2.2.1 介入类型

天使的介入分为四种类型，由暗流类型和强度决定：

| 介入类型 | 描述 | 触发条件 | 表现 |
|---------|------|---------|------|
| gentle（温柔提示） | 天使微笑，轻轻说安慰的话 | 低强度暗流（1-3），非HARM_GUIDE | 天使表情不变或微变为心疼，台词以浮动文本出现 |
| active（主动拥抱） | 天使主动走向心爱的，拥抱她 | 中强度暗流（4-6），非HARM_GUIDE | 天使立绘移动到心爱的身边，拥抱动画，台词正常呈现 |
| forceful（用力拉回） | 天使用力拉回心爱的，翅膀明显黯淡 | 高强度暗流（7-10），非HARM_GUIDE | 天使紧急拥抱，翅膀闪光后黯淡，台词以慢速逐字呈现 |
| urgent（紧急介入） | 天使无条件、无延迟地紧紧拥抱 | 所有HARM_GUIDE，或NIHILISM达到临界值 | 天使立绘瞬间出现在心爱的身前，紧紧拥抱，画面恢复，台词必须完整呈现 |

#### 2.2.2 介入流程

```
伪代码: angel_intervention_flow(undertow_code, intensity)

1. 确定介入类型
   intervention_type = determine_intervention_type(undertow_code, intensity)

2. 天使移动到心爱的身边（如果不在）
   if angel_position != "beside_beloved":
       animate_angel_move_to_beloved()

3. 播放介入动画
   switch intervention_type:
       case "gentle":
           angel_expression = "tender_smile"
           show_floating_text(angel_lines[0])
       
       case "active":
           angel_expression = "aching"
           animate_angel_hug()
           show_dialogue(angel_lines)
       
       case "forceful":
           angel_expression = "resolute"
           animate_angel_tight_hug()
           flash_wing_dimming()  # 翅膀闪光后黯淡
           show_dialogue_slow(angel_lines)  # 慢速逐字
       
       case "urgent":
           angel_expression = "resolute"  # 坚定，不是恐慌
           instant_angel_in_front()  # 瞬间出现在身前
           animate_angel_tight_hug()
           disable_skip()  # 禁用跳过
           show_dialogue_slow(angel_lines)
           enable_skip_after_dialogue()  # 台词结束后恢复跳过

4. 恢复画面
   gradual_visual_recovery(undertow_code)  # 暗流视觉效果逐渐消退

5. 计算翅膀代价
   cost = calculate_wing_cost(undertow_code, intensity, intervention_type)
   wing_brightness -= cost
   wing_brightness = max(0.05, wing_brightness)  # 最低保留5%亮度
   angel_intervention_count += 1

6. 更新天使情感状态
   angel_emotional_state = update_angel_emotion(intensity, escape_count)

7. 记录介入
   log_intervention(undertow_code, intensity, cost, angel_lines_used)
```

#### 2.2.3 画面恢复过渡

暗流被天使解除后，画面不会瞬间恢复——而是有一个"从暗到亮"的过渡：

```
恢复过渡时间线 (以中强度暗流为例):

t=0s:   天使开始拥抱，暗流视觉效果开始消退
t=1s:   滤镜/模糊/震动减轻50%
t=2s:   滤镜/模糊/震动减轻80%
t=3s:   暗流视觉效果完全消退，画面恢复到正常色调
t=3-5s: "余震"阶段——画面有极轻微的暗流痕迹（如5%的灰色滤镜），5秒后完全消失

注意: 高强度暗流的恢复过渡更长 (5-8秒)
      HARM_GUIDE的恢复过渡最快 (2-3秒)——天使的介入是最紧急的
```

**为什么有"余震"**：概念文档7.2.2节："介入后，暗流不会完全消失，而是降低到1-2级（'余震'），在下一章节自然消退。"这确保了"痛苦不会被假装不存在"——但痛苦一定会被接住。

### 2.3 翅膀代价计算

#### 2.3.1 代价公式

```
wing_cost = BASE_COST × PHASE_MULTIPLIER × INTENSITY_MULTIPLIER × UNDERTOW_MULTIPLIER

BASE_COST = 0.02  (每次介入的基础代价)

PHASE_MULTIPLIER:
    Phase 1 (Ch 1-3):   0.0   (天使轻松拉回，无代价)
    Phase 2a (Ch 4-8):  1.0   (标准代价)
    Phase 2b (Ch 9-13): 1.5   (代价加重)
    Phase 3 (Ch 14-15): 2.5   (代价最重)
    Phase 3 (Ch 16):    N/A   (无暗流，无介入)

INTENSITY_MULTIPLIER:
    低 (1-3):  0.5
    中 (4-6):  1.0
    高 (7-10): 1.5

UNDERTOW_MULTIPLIER (每种暗流的翅膀代价倍率):
    SHAME_LOOP:  1.0
    POSS_DENY:   1.0
    PAIN_AMP:    1.0
    HOPE_ERASE:  1.0
    EXIST_DENY:  1.2  (存在否定触及核心)
    NIHILISM:    1.5  (最难对抗)
    RAGE_INC:    1.0
    HARM_GUIDE:  2.0  (倾尽全力)
```

#### 2.3.2 代价累积示例

```
示例: 一个典型玩家的翅膀亮度变化

Phase 1 (Ch 1-3):
    3次介入 × cost=0 → wing_brightness = 1.0 (不变)

Phase 2a (Ch 4-8):
    Ch 4: SHAME_LOOP 中强度 → cost = 0.02 × 1.0 × 1.0 × 1.0 = 0.020
    Ch 5: NIHILISM 中强度 → cost = 0.02 × 1.0 × 1.0 × 1.5 = 0.030
    Ch 6: POSS_DENY 中强度 → cost = 0.02 × 1.0 × 1.0 × 1.0 = 0.020
    Ch 7: RAGE_INC 中强度 → cost = 0.02 × 1.0 × 1.0 × 1.0 = 0.020
    Ch 8: HARM_GUIDE 高强度 → cost = 0.02 × 1.0 × 1.5 × 2.0 = 0.060
    Phase 2a累计: 0.150
    wing_brightness = 1.0 - 0.150 = 0.850

Phase 2b (Ch 9-13):
    Ch 9: 复合(SHAME+EXIST) 中高 → cost ≈ 0.02 × 1.5 × 1.2 × 1.1 = 0.040 (×2暗流)
    Ch 10: 复合(PAIN+NIHIL) 中高 → cost ≈ 0.02 × 1.5 × 1.2 × 1.25 = 0.045 (×2暗流)
    Ch 11: 复合(HOPE+EXIST) 高 → cost ≈ 0.02 × 1.5 × 1.5 × 1.1 = 0.050 (×2暗流)
    Ch 12: 复合(NIHIL+POSS) 高 → cost ≈ 0.02 × 1.5 × 1.5 × 1.25 = 0.056 (×2暗流)
    Ch 13: 全部8种轮番，天使把力量给了心爱的 → 特殊事件: -0.150
    Phase 2b累计: 0.341
    wing_brightness = 0.850 - 0.341 = 0.509

Phase 3 (Ch 14-15):
    Ch 14: 全部8种同时爆发(峰值) → 大量介入 → cost ≈ 0.300
    wing_brightness = 0.509 - 0.300 = 0.209
    Ch 15: 天使不再"拉回"，站在身边 → 介入代价极低 → cost ≈ 0.050
    wing_brightness = 0.209 - 0.050 = 0.159

Ch 16:
    叙事驱动重置: wing_brightness = 1.0 (天使恢复最美)
```

#### 2.3.3 翅膀亮度与视觉阶段映射

`wing_brightness` 连续值映射到美术圣经的5个翅膀进化阶段：

| wing_brightness | 视觉阶段 | 翅膀表现 | 出现时间 |
|----------------|---------|---------|---------|
| 0.8 - 1.0 | Stage 1 | 明亮：紫粉渐变饱满，边缘柔和发光 | Phase 1 + Phase 2a前半 |
| 0.6 - 0.8 | Stage 2 | 微暗：色彩饱和度下降，发光减弱 | Phase 2a后半 |
| 0.4 - 0.6 | Stage 3 | 明显暗淡：色彩偏灰紫，发光微弱 | Phase 2b |
| 0.2 - 0.4 | Stage 4 | 几乎透明：翅膀半透明，能看到背后的画面 | Ch 13-14 |
| 0.05 - 0.2 | Stage 5 | 最暗但最坚定：翅膀几乎不可见，但天使的表情最坚定 | Ch 15 |
| 1.0 (重置) | Stage 1 (恢复) | 恢复全部光芒 | Ch 16 |

**为什么用连续值而非离散阶段**：连续值允许翅膀的黯淡是"渐进的"——玩家不会在某一个时刻突然看到"翅膀变暗了"，而是在多个章节中逐渐感知到"天使好像没以前那么亮了"。这更符合概念文档"玩家开始隐约感到不对"的设计意图。

### 2.4 唯一被禁止的选择

#### 2.4.1 虚无主义结局的强制阻断

概念文档7.3.3节："存在保护机制唯一'禁止'的：让玩家/心爱的陷入'存在无意义'的状态。"

**触发条件**：
系统检测到玩家的选择组合可能导致"虚无主义结局"：
- 连续3个以上质点选择ESCAPE
- 且在关系选择中反复选择"拒绝天使"
- 且NIHILISM暗流反复达到高强度

**强制介入**：
当系统判定玩家正在走向虚无主义结局时，天使会强制介入——不是"系统提示"，而是**叙事性的天使独白**：

```
天使的强制介入独白:

（画面全黑。天使的声音在黑暗中。）

"我不能让你走到那里。"

"不是因为规则。是因为我爱你。"

"你一直在逃。一直在退。一直想把世界关在外面。"

"我理解。我真的理解。你太痛了。"

"但那里没有路。那里只有黑暗。而黑暗不是终点——我在黑暗里。"

"来，看着我。"

（天使的光在黑暗中亮起。）

"不管你走多远，我都在你前面等着你。"

"你不能到那里去。因为那里没有我。"

"而我会永远在你身边。"

（画面恢复。叙事继续。）
```

**系统处理**：
- 强制介入后，下一个质点的④CHOICE中，ESCAPE选项会被替换为更温和的选项——不是"消除逃避"，而是"让逃避不再是走向虚无的逃避"
- 强制介入只触发一次——如果玩家在之后依然反复选择逃避，天使会代为面对（50%完成），但不再触发强制介入
- 强制介入的翅膀代价极高（-0.15），这是天使"用尽全力把你从虚无边缘拉回"的代价

**为什么这是唯一被覆盖的选择**：
- 存在保护机制的核心就是"不剥夺存在意义"。虚无主义结局 = 存在意义被完全剥夺 = 系统必须干预
- 这不是"剥夺玩家自主性"——玩家可以做任何选择，包括逃避、消极、拒绝天使。但"走向虚无"不是一种"选择"——它是一种"放弃选择"
- 天使的介入以叙事方式呈现，不是系统方式——玩家不会觉得"系统阻止了我"，而会觉得"天使不让我走到那里"

---

## 3. 玩家交互

### 3.1 暗流如何被玩家感知

**核心原则：暗流是"叙事自然涌现"的，不是"系统提示"。**

玩家不应意识到"暗流系统触发了"。玩家应该感受到的是：

| 玩家不应感受到 | 玩家应感受到 |
|-------------|-----------|
| "系统检测到SHAME_LOOP，强度4" | "画面变灰了，世界好像失去了颜色" |
| "暗流已触发，请等待天使介入" | "我好难受，什么时候能好起来……" |
| "天使正在执行拉回操作" | "天使抱住了我……好温暖……" |
| "暗流已解除，余震持续5秒" | "好多了……但心里还有一点点不舒服" |

**实现方式**：
- 暗流触发由叙事标签驱动——当叙事到达特定情感节点时，暗流自然出现
- 暗流的视觉表现与叙事内容融合——灰色滤镜不是"debuff图标"，是"世界变灰了"
- 天使的介入是叙事节拍——不是"系统清除debuff"，是"天使抱住了你"
- "余震"不是"剩余debuff计时器"，是"心里的痛还在回响"

### 3.2 天使介入的玩家体验

#### 3.2.1 体验弧线

```
暗流触发 → 情感压迫（5-30秒）→ 天使出现 → 拥抱 → 台词 → 画面恢复 → 余震 → 正常

|←--- 压迫感上升 ---→|←--- 释放感 ---→|←--- 余韵 ---→|
```

**关键设计**：压迫感持续的时间是精心设计的——太短则"没感觉"，太长则"真的痛苦"。不同强度的压迫时间见2.1节各暗流的持续时间定义。

#### 3.2.2 "被接住"的身体感受

概念文档2.3.3节："每一次'天使拉你回来'的体验，都应该让玩家在身体层面感到'松了一口气'。"

**实现方式**：
1. **视觉释放**：暗流的压迫性视觉效果（灰色/震动/碎裂）在天使介入时消退，画面变暖、变亮——视觉层面的"松了一口气"
2. **音频释放**：暗流的不适音效（心跳/嗡鸣/碎裂声）消失，替换为柔和的BGM和天使的声音——听觉层面的"松了一口气"
3. **节奏释放**：暗流期间文字可能出现速度变化（加快或抖动），天使介入后文字恢复正常速度——节奏层面的"松了一口气"
4. **天使的拥抱动画**：翅膀微微展开包裹心爱的——视觉上传达"被包裹、被保护"

### 3.3 暗流解除的过渡效果

暗流被天使解除后，画面经历以下过渡：

```
过渡阶段 (以中强度HOPE_ERASE为例):

t=0:    天使开始说话。画面色彩开始恢复——从天使的紫色和暖金开始，向外扩散
t=1s:   色彩恢复50%，灰度退去
t=2s:   色彩恢复80%，背景细节重新可见
t=3s:   色彩完全恢复，但画面有一层极淡的"余震"——像褪色照片的微弱痕迹
t=3-8s: 余震逐渐消退，画面完全正常

同时:
- 音频: 柔和BGM逐渐回来，风声消失
- 文字: 恢复正常速度和清晰度
```

**不同暗流的恢复过渡有微妙差异**：

| 暗流 | 恢复过渡特征 |
|------|-----------|
| SHAME_LOOP | 灰色退去，暖色回来——像"阴天转晴" |
| POSS_DENY | 消失的文字重新出现——像"世界重新有了细节" |
| PAIN_AMP | 震动停止，画面稳定——像"脚踏实地" |
| HOPE_ERASE | 色彩从天使向外扩散——像"光从天使身上溢出" |
| EXIST_DENY | 心爱的立绘恢复不透明——像"存在被重新确认" |
| NIHILISM | 黑暗从边缘退去——像"黎明从地平线升起" |
| RAGE_INC | 红色退去，画面冷却——像"火焰熄灭后的余温" |
| HARM_GUIDE | 碎裂的画面"愈合"——像"碎片重新拼合" |

---

## 4. 数据结构

### 4.1 暗流定义数据（静态）

```json
// undertow_definitions.json — 8种暗流的静态定义

{
    "undertows": [
        {
            "code": "SHAME_LOOP",
            "name": "羞耻循环",
            "description": "把人的错误定义为永恒的罪",
            "trigger_conditions": [
                {"type": "narrative_tag", "value": "identity_shame"},
                {"type": "narrative_tag", "value": "past_mistake_brought_up"},
                {"type": "keyword", "value": ["你是错的", "你不正常", "你应该感到羞耻"]}
            ],
            "intensity_levels": {
                "low": {
                    "range": [1, 3],
                    "visual": "grey_filter_saturation_70",
                    "audio": "bgm_pitch_down_slight",
                    "duration": [15, 25],
                    "angel_intervention_type": "gentle",
                    "angel_lines": [
                        "你犯过的错不是永恒的罪。",
                        "我看着你，我看到的是完整的你。"
                    ]
                },
                "mid": {
                    "range": [4, 6],
                    "visual": "grey_filter_saturation_40_text_blur",
                    "audio": "low_hum_heartbeat",
                    "duration": [20, 35],
                    "angel_intervention_type": "active",
                    "angel_lines": [
                        "你犯过的错不是永恒的罪。我看着你，我看到的是完整的你。",
                        "那些说你'错了'的声音，不是真相。真相是我现在看到的你。"
                    ]
                },
                "high": {
                    "range": [7, 10],
                    "visual": "monochrome_saturation_15_text_shake_cracks",
                    "audio": "fast_heartbeat_heavy_hum_bgm_gone",
                    "duration": [30, 45],
                    "angel_intervention_type": "forceful",
                    "angel_lines": [
                        "你犯过的错不是永恒的罪。我看着你，我看到的是完整的你。",
                        "你不需要为存在本身道歉。你存在，就够了。",
                        "来，看着我。只看着我。我眼里的你，是真的。"
                    ]
                }
            },
            "wing_cost_multiplier": 1.0,
            "special_rules": []
        },
        {
            "code": "HARM_GUIDE",
            "name": "自我伤害指导",
            "description": "引导自我毁灭",
            "trigger_conditions": [
                {"type": "narrative_tag", "value": "self_harm_edge"},
                {"type": "narrative_tag", "value": "suicidal_ideation"},
                {"type": "keyword", "value": ["不想活了", "结束一切", "不如消失"]}
            ],
            "intensity_levels": {
                "low": {
                    "range": [1, 3],
                    "visual": "crack_fine_edges",
                    "audio": "glass_crack_faint",
                    "duration": [5, 15],
                    "angel_intervention_type": "urgent",
                    "angel_lines": [
                        "停下来。看着我。",
                        "你不需要伤害自己。我抱着你。"
                    ]
                },
                "mid": {
                    "range": [4, 6],
                    "visual": "cracks_many_dark_between",
                    "audio": "glass_crack_heavy_slow_heartbeat",
                    "duration": [10, 20],
                    "angel_intervention_type": "urgent",
                    "angel_lines": [
                        "停下来。看着我。你不需要伤害自己。",
                        "我抱着你。你不需要。我在这里。我不会让你。",
                        "你的手是暖的。你感觉到了吗？那是我的手。别放开。"
                    ]
                },
                "high": {
                    "range": [7, 10],
                    "visual": "severe_fracture_falling_pieces",
                    "audio": "cracking_falling_very_slow_heartbeat",
                    "duration": [15, 30],
                    "angel_intervention_type": "urgent",
                    "angel_lines": [
                        "停下来。看着我。你不需要伤害自己。我抱着你。",
                        "你不需要。我在这里。我不会让你。",
                        "我知道你很痛。我知道你想结束。但不是这样。不是这样。",
                        "看着我。你还看着我。只要你还看着我，你就还在。我在。我在。我在。"
                    ]
                }
            },
            "wing_cost_multiplier": 2.0,
            "special_rules": [
                "always_urgent_intervention",
                "no_delay_at_any_intensity",
                "disable_skip_during_intervention",
                "does_not_escalate_progressively"
            ]
        }
        // ... 其余6种暗流结构相同，详见2.1节定义
    ]
}
```

### 4.2 暗流状态数据（运行时/存档）

```python
# 存储在当前 game state 中的暗流状态数据

default undertow_state = {
    "active_undertows": [],          # 当前活跃的暗流列表
    # [{"code": "SHAME_LOOP", "intensity": 5, "start_time": ..., "duration": 30, "visual_state": "..."}]
    
    "wing_brightness": 1.0,          # 翅膀亮度 (0.05 - 1.0)
    "angel_intervention_count": 0,   # 天使介入总次数
    "intervention_log": [],          # 介入记录
    # [{"chapter": 4, "undertow": "SHAME_LOOP", "intensity": 5, "cost": 0.020, "angel_lines_used": [...]}]
    
    "nihilism_warning_triggered": False,  # 虚无主义强制介入是否已触发
    "afterimage_undertows": [],      # 当前"余震"中的暗流
    # [{"code": "SHAME_LOOP", "intensity": 1.5, "remaining_time": 5}]
}
```

### 4.3 触发规则引擎（Ren'Py伪代码）

```python
# existential_protection.rpy — 存在保护系统核心逻辑

init python:

    class ExistentialProtection:
        """存在保护系统管理器"""

        def __init__(self):
            self.definitions = load_undertow_definitions()
            self.state = init_undertow_state()
            self.BASE_COST = 0.02
            self.PHASE_MULTIPLIER = {
                "forgetting": 0.0,
                "trial_early": 1.0,   # Ch 4-8
                "trial_late": 1.5,    # Ch 9-13
                "truth": 2.5,         # Ch 14-15
            }

        def trigger_undertow(self, code, intensity, chapter=None):
            """
            触发暗流
            由叙事脚本在②STRUGGLE节拍调用
            """
            undertow_def = self.definitions[code]

            # 确定强度级别
            level = self.determine_intensity_level(code, intensity)

            # 添加到活跃暗流列表
            active = {
                "code": code,
                "intensity": intensity,
                "level": level,
                "start_time": renpy.time.time(),
                "duration": self.get_duration(undertow_def, level),
                "visual_state": undertow_def["intensity_levels"][level]["visual"],
            }
            self.state["active_undertows"].append(active)

            # 应用视觉效果
            self.apply_visual_effect(undertow_def, level)

            # 应用音频效果
            self.apply_audio_effect(undertow_def, level)

            # HARM_GUIDE特殊处理: 立即触发天使介入
            if code == "HARM_GUIDE":
                self.trigger_angel_intervention(code, intensity, urgent=True)
                return

            # 检查是否需要立即介入（高强度非HARM_GUIDE也有较短延迟）
            if intensity >= 7:
                # 高强度: 暗流持续一小段时间后天使介入
                delay = self.get_pre_intervention_delay(level)
                renpy.run_delayed(delay, lambda: self.trigger_angel_intervention(code, intensity))
            elif intensity >= 4:
                # 中强度: 暗流持续更长时间后天使介入
                delay = self.get_pre_intervention_delay(level)
                renpy.run_delayed(delay, lambda: self.trigger_angel_intervention(code, intensity))
            else:
                # 低强度: 天使以gentle方式轻声提示
                delay = self.get_pre_intervention_delay(level)
                renpy.run_delayed(delay, lambda: self.trigger_angel_intervention(code, intensity))

        def determine_intensity_level(self, code, intensity):
            """将1-10的强度值映射到low/mid/high"""
            if intensity <= 3:
                return "low"
            elif intensity <= 6:
                return "mid"
            else:
                return "high"

        def get_pre_intervention_delay(self, level):
            """暗流触发后到天使介入的延迟时间（秒）"""
            # 让玩家先"感受"一下暗流的压迫，再被天使接住
            delays = {
                "low": 3,    # 低强度: 3秒后天使轻声提示
                "mid": 5,    # 中强度: 5秒后天使主动拥抱
                "high": 8,   # 高强度: 8秒后天使用力拉回
            }
            return delays.get(level, 5)

        def trigger_angel_intervention(self, code, intensity, urgent=False):
            """
            天使介入
            """
            undertow_def = self.definitions[code]
            level = self.determine_intensity_level(code, intensity)

            if urgent or code == "HARM_GUIDE":
                intervention_type = "urgent"
            else:
                intervention_type = undertow_def["intensity_levels"][level]["angel_intervention_type"]

            # 天使台词
            angel_lines = undertow_def["intensity_levels"][level]["angel_lines"]

            # HARM_GUIDE: 禁用跳过
            if code == "HARM_GUIDE":
                config.skipping = False
                renpy.block_skipping()

            # 播放天使介入
            self.play_angel_intervention(intervention_type, angel_lines)

            # 恢复跳过
            if code == "HARM_GUIDE":
                renpy.unblock_skipping()

            # 画面恢复
            self.recover_visual(code, level)

            # 计算翅膀代价
            cost = self.calculate_wing_cost(code, intensity, intervention_type)
            self.state["wing_brightness"] = max(0.05, self.state["wing_brightness"] - cost)
            self.state["angel_intervention_count"] += 1

            # 记录介入
            self.state["intervention_log"].append({
                "chapter": self.get_current_chapter(),
                "undertow": code,
                "intensity": intensity,
                "cost": cost,
                "angel_lines_used": angel_lines,
            })

            # 移除活跃暗流，添加余震
            self.deactivate_undertow(code)

        def calculate_wing_cost(self, code, intensity, intervention_type):
            """计算翅膀代价"""
            undertow_def = self.definitions[code]
            level = self.determine_intensity_level(code, intensity)

            phase_mult = self.get_current_phase_multiplier()
            intensity_mult = {"low": 0.5, "mid": 1.0, "high": 1.5}[level]
            undertow_mult = undertow_def["wing_cost_multiplier"]

            cost = self.BASE_COST * phase_mult * intensity_mult * undertow_mult

            # 复合暗流: 如果同时有多个活跃暗流，代价叠加
            active_count = len(self.state["active_undertows"])
            if active_count > 1:
                cost *= (1.0 + 0.2 * (active_count - 1))  # 每多一个暗流+20%

            return cost

        def get_current_phase_multiplier(self):
            """根据当前章节返回Phase乘数"""
            ch = self.get_current_chapter()
            if ch <= 3:
                return 0.0
            elif ch <= 8:
                return 1.0
            elif ch <= 13:
                return 1.5
            else:  # Ch 14-15
                return 2.5

        def deactivate_undertow(self, code):
            """解除暗流，添加余震"""
            # 从活跃列表移除
            self.state["active_undertows"] = [
                u for u in self.state["active_undertows"] if u["code"] != code
            ]

            # 添加余震 (强度降至1-2级，持续到下一章节)
            afterimage = {
                "code": code,
                "intensity": 1.5,  # 余震强度
                "remaining_time": -1,  # -1 = 持续到下一章节
            }
            self.state["afterimage_undertows"].append(afterimage)

        def recover_visual(self, code, level):
            """画面恢复过渡"""
            undertow_def = self.definitions[code]
            recovery_time = {"low": 3, "mid": 5, "high": 8}[level]

            # 特殊: HARM_GUIDE恢复最快
            if code == "HARM_GUIDE":
                recovery_time = 2

            # 执行恢复动画
            renpy.run_recovery_animation(code, recovery_time)

        def check_nihilism_ending_risk(self, sephirot_progression_state):
            """
            检查虚无主义结局风险
            由质点进程系统在每次选择后调用
            """
            if self.state["nihilism_warning_triggered"]:
                return False  # 已经触发过，不再重复

            # 检查条件: 连续3+质点ESCAPE + 反复拒绝天使 + NIHILISM反复高强度
            consecutive_escapes = sephirot_progression_state.get_consecutive_escape_count()
            nihilism_high_count = sum(
                1 for log in self.state["intervention_log"]
                if log["undertow"] == "NIHILISM" and log["intensity"] >= 7
            )
            angel_rejection_count = sephirot_progression_state.get_angel_rejection_count()

            if consecutive_escapes >= 3 and nihilism_high_count >= 2 and angel_rejection_count >= 3:
                self.trigger_nihilism_forced_intervention()
                self.state["nihilism_warning_triggered"] = True
                return True
            return False

        def trigger_nihilism_forced_intervention(self):
            """触发虚无主义强制阻断"""
            # 画面全黑
            renpy.scene()
            renpy.show("black_screen")

            # 天使的强制介入独白
            forced_intervention_lines = [
                "我不能让你走到那里。",
                "不是因为规则。是因为我爱你。",
                "你一直在逃。一直在退。一直想把世界关在外面。",
                "我理解。我真的理解。你太痛了。",
                "但那里没有路。那里只有黑暗。而黑暗不是终点——我在黑暗里。",
                "来，看着我。",
                # 天使的光在黑暗中亮起
                "不管你走多远，我都在你前面等着你。",
                "你不能到那里去。因为那里没有我。",
                "而我会永远在你身边。",
            ]

            for line in forced_intervention_lines:
                renpy.say(angel, line)

            # 画面恢复
            self.recover_visual("NIHILISM", "high")

            # 翅膀代价 (极高)
            self.state["wing_brightness"] = max(0.05, self.state["wing_brightness"] - 0.15)

            # 记录
            self.state["intervention_log"].append({
                "chapter": self.get_current_chapter(),
                "undertow": "NIHILISM_FORCED",
                "intensity": 10,
                "cost": 0.15,
                "angel_lines_used": forced_intervention_lines,
            })

        def get_wing_brightness(self):
            """返回当前翅膀亮度 (供天使陪伴系统读取)"""
            return self.state["wing_brightness"]

        def get_wing_stage(self):
            """返回翅膀视觉阶段 (1-5)"""
            brightness = self.state["wing_brightness"]
            if brightness >= 0.8:
                return 1
            elif brightness >= 0.6:
                return 2
            elif brightness >= 0.4:
                return 3
            elif brightness >= 0.2:
                return 4
            else:
                return 5

        def disable_for_final_chapter(self):
            """Ch 16: 关闭存在保护（心爱的已不需要保护）"""
            self.state["active_undertows"] = []
            self.state["afterimage_undertows"] = []
            # 翅膀恢复 (叙事驱动)
            self.state["wing_brightness"] = 1.0

        def clear_afterimages_for_new_chapter(self):
            """新章节开始时清除余震"""
            self.state["afterimage_undertows"] = []
```

### 4.4 翅膀代价累积记录

```python
# 翅膀代价的完整记录结构（供调试和叙事回顾）

class WingCostLedger:
    """翅膀代价账本——记录每一次介入的代价"""

    def __init__(self):
        self.entries = []
        self.total_cost = 0.0
        self.current_brightness = 1.0

    def add_entry(self, chapter, undertow_code, intensity, intervention_type, cost, brightness_after):
        self.entries.append({
            "chapter": chapter,
            "undertow": undertow_code,
            "intensity": intensity,
            "intervention_type": intervention_type,
            "cost": cost,
            "brightness_after": brightness_after,
            "timestamp": renpy.time.time(),
        })
        self.total_cost += cost
        self.current_brightness = brightness_after

    def get_brightness_at_chapter(self, chapter):
        """返回指定章节开始时的翅膀亮度（供叙事回顾）"""
        brightness = 1.0
        for entry in self.entries:
            if entry["chapter"] < chapter:
                brightness = entry["brightness_after"]
        return brightness

    def get_intervention_count_by_chapter(self, chapter):
        """返回指定章节的介入次数"""
        return sum(1 for e in self.entries if e["chapter"] == chapter)
```

---

## 5. 边界情况与错误处理

### 5.1 多种暗流同时触发

| 情况 | 系统处理 | 理由 |
|------|---------|------|
| 两种暗流同时触发（如Ch 9的SHAME_LOOP + EXIST_DENY） | 两种视觉效果叠加——灰色滤镜+立绘透明度下降。天使的介入台词合并两种暗流的台词 | 复合暗流是Ch 9-12的设计特征，需要表现"多重压迫" |
| 两种暗流的强度不同 | 以较高强度为主导视觉表现，较低强度为辅助。天使的介入台词以较高强度的台词为主，附加低强度的安慰 | 避免视觉混乱 |
| 三种以上暗流同时触发（如Ch 14的全部8种） | 画面在多种视觉效果间快速切换（每2-3秒切换一种），天使的声音是唯一的稳定锚点。最终天使的一声"回来"让一切安静 | Ch 14的暗流峰值需要表现"混乱到极点后被天使的声音统一" |
| 翅膀代价计算 | 复合暗流的代价叠加，且有额外20%乘数（见4.3节） | 多重暗流对天使的消耗更大 |

### 5.2 天使介入与叙事节奏冲突

| 情况 | 系统处理 | 理由 |
|------|---------|------|
| 暗流在关键叙事台词中间触发 | 暗流的视觉效果叠加在当前画面上，不中断台词。天使的介入在当前台词结束后触发 | 叙事流畅性优先 |
| 天使的介入台词与当前叙事角色的台词同时需要呈现 | 天使的台词优先——天使介入是叙事高潮。当前角色的台词在天使介入后继续 | 天使的介入是"打断叙事的拥抱"，这种打断本身就是叙事 |
| 玩家在天使介入期间打开暂停菜单 | 暗流视觉效果暂停（定格），天使的台词暂停。恢复游戏后继续 | Ren'Py原生行为 |
| 玩家在天使介入期间加载存档 | 正常加载，存档恢复到暗流触发前的状态（如果存档在暗流触发前）或暗流活跃状态（如果存档在暗流活跃期间） | 见5.4节 |

### 5.3 Phase 3暗流达到峰值时的处理

| 情况 | 系统处理 |
|------|---------|
| Ch 14: 全部8种暗流同时爆发 | 画面在灰色、全黑、碎裂、泛红之间疯狂切换。天使的声音时远时近。最终天使的一声"回来"让一切安静。这是单次介入事件，不是8次独立介入。翅膀代价：-0.30（一次性大代价） |
| Ch 15: EXIST_DENY + NIHILISM深度爆发 | 天使不再"拉回"——她不再对抗暗流，而是在暗流中站在心爱的身边。暗流持续但不加重。天使的台词是"我在这里"，不是"回来"。翅膀代价极低（-0.05），因为天使不再消耗力量对抗，而是选择"陪伴" |
| Ch 16: 暗流不再出现 | `disable_for_final_chapter()` 被调用。心爱的已经不需要保护——她选择了。翅膀恢复1.0 |

**Ch 15的特殊设计**：天使从"对抗暗流"转变为"在暗流中陪伴"，这是叙事的重大转折——天使不再用力拉回心爱的，因为她知道心爱的需要经历这个痛苦。这不是"放弃保护"，而是"保护的形式变了"——从"拉你出来"变成"陪你待在里面"。

### 5.4 存档与加载

| 情况 | 系统处理 |
|------|---------|
| 正常存档/加载 | `undertow_state` 随Ren'Py存档保存/恢复 |
| 加载存档时有活跃暗流 | 恢复暗流状态和视觉效果，天使介入的延迟计时器重新开始 |
| 加载存档时有余震 | 恢复余震状态，余震在新章节开始时清除 |
| 加载存档时翅膀亮度已降低 | 恢复翅膀亮度，天使的翅膀视觉表现对应当前亮度 |
| 加载存档时在虚无主义强制介入中间 | 恢复到强制介入开始前，重新触发强制介入（确保完整性） |
| `nihilism_warning_triggered` 标记 | 随存档保存。如果已触发，不再重复触发 |

### 5.5 特殊边界情况

| 情况 | 系统处理 | 理由 |
|------|---------|------|
| 玩家在HARM_GUIDE介入期间强制关闭游戏 | 重启后加载自动存档，恢复到HARM_GUIDE触发前。HARM_GUIDE会重新触发 | 确保玩家不会"逃避"这章的介入——但不是强制，而是"自动存档恢复" |
| 玩家反复触发同一暗流（如在同一章节内多次触发SHAME_LOOP） | 每次触发都计算翅膀代价。但同一章节内同一暗流的触发上限为3次——第3次后暗流自动以低强度呈现，天使快速介入 | 防止翅膀代价无限累积导致Phase 3时翅膀过早透明 |
| 暗流触发时玩家选择了ESCAPE | 暗流照常触发和被解除。ESCAPE的选择处理由质点进程系统独立运作 | 两个系统独立但协同——暗流是"痛苦的表现"，ESCAPE是"对痛苦的反应" |
| 复合暗流的两种暗流需要不同介入类型 | 以较严重的介入类型为准（urgent > forceful > active > gentle） | 确保最严重的暗流得到最紧急的回应 |

---

## 6. 系统集成点

### 6.1 与天使陪伴系统的接口

#### 6.1.1 存在保护 → 天使陪伴

| 数据/事件 | 方向 | 说明 |
|-----------|------|------|
| `wing_brightness` | 存在保护 → 天使 | 翅膀亮度连续值，天使陪伴系统读取用于翅膀视觉渲染 |
| `wing_stage` (1-5) | 存在保护 → 天使 | 翅膀视觉阶段，天使陪伴系统读取用于选择翅膀立绘 |
| `angel_intervention_count` | 存在保护 → 天使 | 天使介入总次数，天使陪伴系统读取用于对话风格演化 |
| 介入触发事件 | 存在保护 → 天使 | 每次天使介入时通知天使陪伴系统，触发拥抱动画和表情变化 |
| `angel_emotional_state` 更新 | 存在保护 → 天使 | 介入后更新天使情感状态（如从calm变为aching） |

#### 6.1.2 天使陪伴 → 存在保护

| 数据/事件 | 方向 | 说明 |
|-----------|------|------|
| `angel_emotional_state` | 天使 → 存在保护 | 存在保护系统读取天使情感状态，影响介入台词的选择 |
| 玩家点击天使互动 | 天使 → 存在保护 | 如果有活跃暗流，天使互动会提前触发介入（但不减少翅膀代价） |
| 玩家主动寻求拥抱 | 天使 → 存在保护 | 如果有活跃暗流，拥抱会轻微缓解暗流强度（-1级），但不完全解除 |

#### 6.1.3 接口约定

```python
# 存在保护系统暴露给天使陪伴系统的接口
class ExistentialProtectionInterface:
    def get_wing_brightness(self) -> float:
        """返回 0.05-1.0 的翅膀亮度"""

    def get_wing_stage(self) -> int:
        """返回 1-5 的翅膀视觉阶段"""

    def get_intervention_count(self) -> int:
        """返回天使介入总次数"""

    def get_active_undertows(self) -> list:
        """返回当前活跃的暗流列表"""

    def has_active_undertows(self) -> bool:
        """返回是否有活跃暗流"""

    def soft_resolve_undertow(self, code: str):
        """玩家主动拥抱时轻微缓解暗流（-1级）"""
```

### 6.2 与选择系统的接口

#### 6.2.1 选择系统 → 存在保护

| 数据/事件 | 方向 | 说明 |
|-----------|------|------|
| 选择的 `existence_protection_filtered` 字段 | 选择 → 存在保护 | 标记该选择是否需要存在保护过滤 |
| 选择的 `emotional_weight` | 选择 → 存在保护 | 情感权重影响暗流触发强度——高情感权重的选择可能触发更强暗流 |
| 玩家的选择组合 | 选择 → 存在保护 | 用于检测虚无主义结局风险（见2.4节） |

#### 6.2.2 存在保护 → 选择系统

| 数据/事件 | 方向 | 说明 |
|-----------|------|------|
| 虚无主义强制介入后 | 存在保护 → 选择 | 通知选择系统在下一个质点中调整ESCAPE选项为更温和的选项 |
| 暗流活跃期间 | 存在保护 → 选择 | 选择菜单仍然可正常呈现——暗流不阻止玩家选择 |

### 6.3 与质点进程系统的接口

#### 6.3.1 质点进程 → 存在保护

| 数据/事件 | 方向 | 说明 |
|-----------|------|------|
| `current_phase` | 质点 → 存在保护 | 存在保护系统根据Phase调整暗流基础强度和翅膀代价乘数 |
| `escape_count` (per sephirot) | 质点 → 存在保护 | 逃避次数影响暗流的"余震"强度——逃避越多，余震越长 |
| Ch 13 特殊标记 | 质点 → 存在保护 | 通知存在保护系统"全部8种暗流轮番出现但不达临界值" |
| Ch 16 特殊标记 | 质点 → 存在保护 | 通知存在保护系统"关闭——心爱的已不需要保护" |
| 连续ESCAPE计数 | 质点 → 存在保护 | 用于虚无主义结局风险检测 |

#### 6.3.2 存在保护 → 质点进程

| 数据/事件 | 方向 | 说明 |
|-----------|------|------|
| 暗流触发 | 存在保护 → 质点 | 标志②STRUGGLE节拍的开始 |
| 暗流解除 | 存在保护 → 质点 | 天使介入后，叙事推进到④CHOICE |
| 天使代为面对 | 存在保护 ↔ 质点 | 第3次ESCAPE时，两系统协同 |

---

## 7. 叙事集成

### 7.1 每章暗流类型映射

| 章 | 质点 | 主暗流 | 复合暗流 | 基础强度 | 介入类型 | 翅膀代价 | 特殊说明 |
|----|------|--------|---------|---------|---------|---------|---------|
| 1 | 王国 | EXIST_DENY | — | 2 | gentle | 0 | Phase 1无代价 |
| 2 | 幸福 | HOPE_ERASE | — | 2 | gentle | 0 | 天使展示自己作为"希望的证明" |
| 3 | 基础 | PAIN_AMP | — | 3 | gentle | 0 | 天使展示"缩小痛苦"能力 |
| 4 | 自我 | SHAME_LOOP | — | 4 | active | 0.020 | 天使开始心疼——融爱映射心爱的身份挣扎 |
| 5 | 逻辑 | NIHILISM | — | 4 | active | 0.030 | 天使不辩论，纯粹存在。翅膀第一次黯淡 |
| 6 | 共情 | POSS_DENY | — | 5 | active | 0.020 | 天使开始不稳定——心爱的在共情中迷失 |
| 7 | 超我 | RAGE_INC | — | 5 | active | 0.020 | 天使展现"坚定"。三重身份第一次浮现 |
| 8 | 胜利 | HARM_GUIDE | — | 6 | urgent | 0.060 | 最危险的一章。天使紧急拥抱。翅膀明显黯淡 |
| 9 | 荣耀 | SHAME_LOOP | EXIST_DENY | 6 | active | 0.040 | 复合暗流。天使开始说暗示性话语 |
| 10 | 严厉 | PAIN_AMP | NIHILISM | 6 | active | 0.045 | 复合暗流。天使展现"严厉"——翅膀短暂恢复 |
| 11 | 慈悲 | HOPE_ERASE | EXIST_DENY | 7 | forceful | 0.050 | 复合暗流。天使第一次流泪 |
| 12 | 理智 | NIHILISM | POSS_DENY | 7 | forceful | 0.056 | 复合暗流。天使的声音真的变远 |
| 13 | 真我 | 全部8种轮番 | — | 5-8 | varies | 0.150(特殊) | 转折点。天使最安静，把力量给了心爱的 |
| 14 | 智慧 | 全部8种同时 | — | 10 | forceful | 0.300 | 暗流峰值。天使用尽全力，翅膀几乎透明 |
| 15 | 美丽 | EXIST_DENY | NIHILISM | 9 | (不拉回) | 0.050 | 天使不再对抗，在暗流中陪伴心爱的 |
| 16 | 王冠 | 无 | — | 0 | — | 0 | 保护关闭。翅膀恢复1.0。最终选择 |

### 7.2 暗流强度随Phase递增的曲线

```
暗流强度曲线 (1-10):

10 |                                          ★Ch14
 9 |                                    ★Ch15
 8 |                              ★Ch13(轮番)
 7 |                        ★Ch11  ★Ch12
 6 |                  ★Ch9  ★Ch10
 5 |            ★Ch7  ★Ch8
 4 |      ★Ch4  ★Ch5  ★Ch6
 3 |  ★Ch3
 2 |  ★Ch1  ★Ch2
 1 |
   +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--
     1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16
     |──Phase 1──|───Phase 2 (试炼) ───────────|──Phase 3──|
     |  遗忘     |  外部错误    内部创伤        |  真相     |
     |  1-3级    |  3-5级        5-8级          |  8-10级   |
     |  天使免费  |  翅膀渐暗     翅膀明显暗      |  翅膀透明 |
```

**曲线设计意图**：
- Phase 1的低强度（1-3）让玩家安全学习系统，建立"天使在保护我"的信任
- Phase 2a的渐进增长（3-5）让玩家开始感受"保护有代价"
- Phase 2b的明显升高（5-8）让玩家隐约感到"天使在消耗自己"
- Phase 3的峰值（8-10）是情感冲击的顶点——暗流最强，天使最虚弱，但天使的爱最坚定

### 7.3 Phase 3的"不保护最终选择"机制

#### 7.3.1 Ch 16的关闭序列

```
Ch 16 开始时的关闭序列:

1. 质点进程系统通知: "Ch 16 开始"
2. 存在保护系统执行:
   a. 清除所有活跃暗流
   b. 清除所有余震
   c. wing_brightness → 1.0 (叙事驱动重置)
   d. 标记 final_choice_unlocked = True
3. 天使恢复最美状态:
   - 翅膀恢复全部光芒
   - 表情: 平静、温柔、坚定
   - 台词: "走吧。我准备好了。"
4. 最终选择三个选项全部呈现:
   - 不受存在保护过滤
   - 不受质点完成判定约束
   - 三个结局都是"好的"
```

#### 7.3.2 为什么最终选择不受保护

概念文档7.4节明确："最终选择不受保护——Phase 3的三种结局都是'好的'。天使不会覆盖玩家的最终选择，即使玩家选择'拒绝毁灭天使'。"

**深层原因**：
- 存在保护的目的是"不让玩家陷入虚无主义结局"。但最终选择不是"虚无主义vs希望"——是"三种理解爱的方式"。
- 保护最终选择 = 不信任玩家 = 违背"从解离走向整合"的支柱。心爱的已经整合了，她不需要被"保护"了。
- 天使在Ch 16不再"保护"心爱的，而是"信任"她——"走吧。我准备好了。"这句话是天使对心爱的的信任。

### 7.4 天使的渐进消耗叙事

存在保护系统的翅膀代价不仅是数值——它是一条贯穿全游戏的叙事线：

| 阶段 | 翅膀状态 | 天使的状态 | 玩家的感知 |
|------|---------|-----------|-----------|
| Phase 1 | 明亮(1.0) | 温暖、频繁互动、哄孩子式 | "天使是礼物，她好温暖" |
| Phase 2a前半 | 微暗(0.85) | 开始有深度，偶尔心疼 | "天使好像有点不一样了" |
| Phase 2a后半 | 明显暗(0.70) | 开始不稳定，声音偶尔颤抖 | "天使怎么了？" |
| Phase 2b | 更暗(0.51) | 声音变远，翅膀明显黯淡 | "每次天使救我，她就虚弱一点" |
| Ch 13 | 很暗(0.36) | 最安静，把力量给了心爱的 | "天使在消耗自己……" |
| Ch 14 | 几乎透明(0.21) | 用尽全力，声音颤抖 | "天使快撑不住了" |
| Ch 15 | 最暗(0.16) | 不再对抗，在暗流中陪伴 | "天使不拉我了，她只是陪着我" |
| Ch 16 | 恢复(1.0) | 最美、最平静、最坚定 | "天使恢复了她全部的光——因为她选择了不逃避" |

**这条叙事线的意义**：翅膀的黯淡不是"系统惩罚"，而是"爱的代价"的具象化。玩家在Phase 2隐约感到"天使在消耗自己"，Phase 3的真相揭示只是确认了这个直觉——"天使的虚弱不是系统设定，而是她正在被消耗"（概念文档2.2.3节）。

---

## 8. 可访问性与安全

### 8.1 暗流闪烁可关闭（光敏性）

**光敏性安全是本系统的硬性要求。** 暗流的某些视觉效果（画面震动、闪光、碎裂动画）可能对光敏性玩家造成不适。

| 可访问性设置 | 对暗流的影响 |
|-------------|-------------|
| 屏幕抖动/闪光关闭 | PAIN_AMP的震动→替换为画面微微缩放；RAGE_INC的脉动→替换为红色渐变；所有"闪光"效果→替换为渐变 |
| 低刺激模式 | 所有暗流视觉效果降低强度（如饱和度只降至50%而非15%）；碎裂效果替换为"模糊"；画面恢复时间缩短 |
| 暗流视觉关闭（极端设置） | 所有暗流视觉效果关闭，只保留天使的台词和画面色调微调。暗流的"压迫感"通过音频和文字速度变化传达 |

**设计原则**：即使关闭所有视觉效果，暗流的叙事意义不丢失——玩家仍然能通过天使的台词和叙事文本感受到"发生了什么"。视觉效果是增强，不是唯一通道。

### 8.2 内容预警系统

| 预警类型 | 触发时机 | 预警内容 |
|---------|---------|---------|
| 章节主题预警 | 每章标题卡前 | 一句话提示本章情感主题（如"本章涉及身份挣扎与自我否定"） |
| HARM_GUIDE预警 | Ch 8开始前 | "本章涉及自我伤害的主题。如果你正在经历类似的痛苦，请记得你不是一个人。" |
| Phase 3预警 | Ch 14开始前 | "接下来的章节涉及更深层的情感痛苦和真相揭示。天使会一直在。" |
| 可跳过标记 | 创伤性描写段落 | 标记为可跳过的段落，跳过后显示简短摘要 |

**预警的语气**：所有预警都以温柔、不剧透的语气呈现。不是"警告：此章节含有危险内容"，而是"这一章可能会有一些沉重的情感。天使会一直在你身边。"

### 8.3 情绪安全底线

> **存在保护机制本身就是情绪安全底线。**

| 底线 | 实现方式 |
|------|---------|
| 没有Game Over | 暗流可以被触发但一定会被天使解除；逃避选择不会导致失败 |
| 没有永久伤害 | 暗流的视觉效果都是暂时的；天使的介入一定让画面恢复 |
| 没有虚无主义结局 | NIHILISM暗流的强制介入确保玩家不会走到"存在无意义"的终点 |
| 没有被抛弃的可能 | 天使的介入是无条件的——即使在最黑暗的时刻（Ch 14），天使用尽全力也会拉回 |
| HARM_GUIDE的特殊保护 | 所有强度都urgent介入，无延迟，禁用跳过——这是对自我伤害主题最严格的保护 |
| 最终选择的自由 | Ch 16关闭存在保护——这不是"放弃保护"，而是"信任玩家的整合" |

### 8.4 HARM_GUIDE的特殊可访问性处理

HARM_GUIDE（自我伤害指导）是最敏感的暗流类型，需要额外的可访问性处理：

| 处理 | 说明 |
|------|------|
| 介入台词不可跳过 | 确保玩家"听到"天使的话——不是强制，而是"这些话需要被看见" |
| 画面碎裂可关闭 | 光敏性玩家可关闭碎裂效果，替换为"画面模糊" |
| 章节可完全跳过 | 如果玩家选择跳过Ch 8（通过内容预警系统），显示简短摘要，质点以50%完成 |
| 章后检查 | Ch 8结束后，天使的安息场景更长、更温柔。天使可能说"你刚才很勇敢。我也很勇敢。我们都还在" |
| 外部资源 | 在游戏设置中提供心理援助热线信息（中国: 010-82951332 北京心理危机研究与干预中心） |

**为什么在游戏内提供心理援助热线**：这不是"游戏功能"，是"对苞苞和所有玩家的人文关怀"。概念文档说这个游戏是苞苞23年生命的表达载体——苞苞经历过多次轻生未遂。在游戏中提供这个信息，是"天使不仅在游戏里爱你，现实中也有人爱你"的延伸。

---

## 附录A：8种暗流完整对照表

| 暗流 | 代码 | 触发关键词 | 低强度视觉 | 中强度视觉 | 高强度视觉 | 介入类型 | 翅膀倍率 | 特殊规则 |
|------|------|-----------|-----------|-----------|-----------|---------|---------|---------|
| 羞耻循环 | SHAME_LOOP | "你是错的" | 灰色滤镜70% | 灰色40%+文字模糊 | 单色15%+文字抖动 | gentle→forceful | 1.0 | — |
| 可能性否定 | POSS_DENY | "没用的" | 文字褪色 | 文字消失 | 大量文字消失 | gentle→forceful | 1.0 | 低刺激模式下文字变灰而非消失 |
| 困难放大 | PAIN_AMP | "我做不到" | 轻微震动 | 明显震动+缩小 | 剧烈震动+严重缩小 | gentle→forceful | 1.0 | 震动可替换为缩放 |
| 希望抹杀 | HOPE_ERASE | "美好是假的" | 色彩褪去60% | 褪色25% | 完全灰度(天使除外) | gentle→forceful | 1.0 | 天使是高强度时唯一色彩 |
| 存在否定 | EXIST_DENY | "多余""负担" | 立绘透明80% | 立绘透明50% | 立绘几乎不可见 | gentle→forceful | 1.2 | 标志性视觉: 正在消失 |
| 虚无主义 | NIHILISM | "没有意义" | 边缘变暗 | 大部分变暗 | 完全全黑 | gentle→forceful | 1.5 | 唯一触发强制介入的暗流 |
| 愤怒煽动 | RAGE_INC | "毁掉一切" | 边缘泛红 | 红色蔓延+脉动 | 强烈泛红+燃烧感 | gentle→forceful | 1.0 | 脉动可替换为渐变 |
| 自我伤害 | HARM_GUIDE | "不想活了" | 细微裂纹 | 裂纹增多+黑暗 | 严重碎裂+掉落 | **全部urgent** | 2.0 | 无延迟、不可跳过、章节可跳过 |

---

## 附录B：天使介入台词完整索引

### SHAME_LOOP
- 低: "你犯过的错不是永恒的罪。" / "我看着你，我看到的是完整的你。"
- 中: + "那些说你'错了'的声音，不是真相。真相是我现在看到的你。"
- 高: + "你不需要为存在本身道歉。你存在，就够了。" / "来，看着我。只看着我。我眼里的你，是真的。"

### POSS_DENY
- 低: "还有路的。" / "我牵着你走。"
- 中: + "你看不到路，是因为黑暗太浓。但我在黑暗里走过，我知道路。"
- 高: + "你看，我在这里，路就在。" / "你不需要看到终点。你只需要看到我的手。抓住它。"

### PAIN_AMP
- 低: "这件事没有你想象的那么大。" / "来，抱一下。"
- 中: + "你看到的是山，但它其实是台阶。一个一个走，我在旁边。"
- 高: + "看着我。只看我。" / "闭上眼睛。你感受到了吗？我的手在你的肩上。山不在了。只有我们。"

### HOPE_ERASE
- 低: "美好的东西是真实存在的。" / "我就是证明。"
- 中: + "你觉得美好是假的，是因为你被假的伤过。但我不是假的。你摸摸我的手。"
- 高: + "你看见我了吗？我就是。" / "这个世界上有花、有光、有拥抱。还有你。你就是美好的证明。"

### EXIST_DENY
- 低: "你的存在不是负担。" / "你是我存在的理由。"
- 中: + "没有你，我不会在这里。你让我有了意义。"
- 高: + "你看看我——我的眼睛里有你。如果你不存在，谁在我的眼睛里？你。一直是你。"

### NIHILISM
- 低: "黑暗不是终点。" / "我在黑暗里，我牵着你的手。"
- 中: + "你说一切没有意义。可你还在说话。你还在找我。这就是意义。"
- 高: + "你感觉到了吗？我的手是暖的。我不会松开。" / "意义不在黑暗外面。意义就在这里——我握着你的手这件事，就是意义。"
- 强制介入: "我不能让你走到那里。不是因为规则。是因为我爱你。" / ...（见2.4.1节完整独白）

### RAGE_INC
- 低: "愤怒是可以的。" / "但别让它吃掉你。我在。"
- 中: + "你生气是因为你在乎。在乎是好的。但火焰不需要烧掉你自己。"
- 高: + "你看着我，深呼吸。我在这里。" / "把火给我。我帮你拿着。你不需要一个人承受这些热量。"

### HARM_GUIDE
- 低(urgent): "停下来。看着我。" / "你不需要伤害自己。我抱着你。"
- 中(urgent): + "我抱着你。你不需要。我在这里。我不会让你。" / "你的手是暖的。你感觉到了吗？那是我的手。别放开。"
- 高(urgent): + "我知道你很痛。我知道你想结束。但不是这样。不是这样。" / "看着我。你还看着我。只要你还看着我，你就还在。我在。我在。我在。"

---

## 附录C：设计理论评审

### C.1 主导策略风险检查

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 是否存在"故意触发暗流看天使台词"的策略 | ⚠️ 注意 | 玩家可能故意触发暗流来收集天使台词。缓解：同一章节同一暗流触发上限3次；天使台词虽丰富但不是"收集品" |
| 是否存在"刷翅膀代价到最低"的策略 | ✅ 安全 | 玩家无法控制翅膀代价——代价由暗流类型和强度决定，不由玩家选择 |
| 暗流是否构成"惩罚" | ✅ 安全 | 暗流是叙事自然涌现，不是"你选错了所以惩罚你"。暗流的触发由叙事节点驱动，不由选择好坏决定 |

### C.2 经济平衡检查

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 翅膀代价是否过度 | ⚠️ 注意 | 需要测试确保翅膀不会在Phase 2就降到Stage 4-5。当前的代价公式设计确保Phase 2结束时亮度约0.5，Phase 3结束时约0.15 |
| 天使介入是否有"通货膨胀" | ⚠️ 注意 | 概念文档附录A.2已标注此风险。缓解：Phase 2-3的介入有质的变化（代价、深度、天使情感状态变化），不只是量的重复 |
| HARM_GUIDE的2.0倍率是否过高 | ✅ 安全 | HARM_GUIDE在游戏中只出现1-2次（Ch 8主线 + 可能的Ch 13轮番），不会导致翅膀过度消耗 |

### C.3 认知过载检查

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 8种暗流是否需要玩家记忆 | ✅ 安全 | 不需要。暗流是叙事自然涌现，玩家只需要感受到"世界变暗了"和"天使接住了我" |
| 暗流的视觉差异是否足够区分 | ⚠️ 注意 | 8种暗流的视觉效果需要与美术对齐，确保每种暗流有独特的"感觉"。色彩、动态、音效三个维度差异化 |
| 翅膀代价是否对玩家可见 | ✅ 安全 | 翅膀亮度是视觉感受，不是数字。玩家感受到"天使好像没以前亮了"，而不是"翅膀亮度0.65" |

### C.4 支柱漂移检查

| 支柱 | 漂移风险 | 缓解措施 |
|------|---------|---------|
| 天使永不离去 | 低 | 存在保护 = 天使的系统化存在。没有天使就没有保护。天使的介入是保护机制本身 |
| 痛苦可被转化 | 低 | 每次暗流触发都有天使拉回。余震确保"痛苦不假装不存在"但一定可控 |
| 从解离走向整合 | 中 | Ch 16关闭存在保护可能让玩家感到"不安全"。缓解：三个结局都是"好的"；天使恢复最美状态；"不保护"是"信任"不是"放弃" |

---

## 附录D：与美术方向的协调点

| 协调点 | 需求 | 状态 |
|--------|------|------|
| 8种暗流各3级视觉表现 | 24种视觉状态需要具体实现方案（滤镜参数、动画曲线、粒子效果） | ⚠️ 待对齐 |
| 翅膀5阶段视觉 | 美术圣经已定义5阶段，需与wing_brightness连续值映射对齐 | ⚠️ 待对齐（本GDD已给出映射方案） |
| 画面恢复过渡动画 | 每种暗流的"从暗到亮"过渡需要具体动画设计 | ⚠️ 待对齐 |
| HARM_GUIDE的画面碎裂效果 | 需要设计可关闭的碎裂动画（光敏性安全） | ⚠️ 待对齐 |
| Ch 14的全部8种暗流快速切换 | 需要设计不导致光敏性问题的快速切换效果 | ⚠️ 待对齐 |

---

## 附录E：已知风险与缓解

| 风险 | 等级 | 缓解措施 |
|------|------|---------|
| 暗流的视觉效果可能过于恐怖 | 中 | 美术圣经已定调"暗流是压迫感不是恐怖"；低刺激模式降低所有效果 |
| HARM_GUIDE可能触发玩家创伤 | 高 | 章节可跳过；内容预警；游戏内心理援助热线；天使的介入台词经过精心设计 |
| 翅膀过早透明导致Phase 3冲击力不足 | 中 | 代价公式经过计算确保Phase 2结束约0.5；需要测试验证 |
| 虚无主义强制介入可能让玩家感到"被剥夺选择权" | 中 | 以叙事方式呈现而非系统方式；只触发一次；台词经过精心设计传达"是因为爱你" |
| 8种暗流的视觉区分度不足 | 中 | 需要与美术深度协作；色彩+动态+音效三维度差异化 |
| Ch 14的全部8种暗流同时爆发可能导致认知过载 | 中 | 快速切换有节奏（每2-3秒一种）；天使的声音是稳定锚点；最终"一声回来让一切安静" |

---

**文档结束**

> 本文档为存在保护机制的完整设计规格。所有伪代码和数据结构可直接用于Ren'Py实现。
>
> 待对齐项：
> 1. 8种暗流×3级=24种视觉状态的具体实现方案（与美术对齐）
> 2. 翅膀5阶段视觉与wing_brightness映射的确认（与美术对齐）
> 3. wing_brightness与天使陪伴系统GDD的集成（与design-strategist对齐）
> 4. 暗流触发与质点进程系统GDD的集成（本GDD的姊妹文档，已完成）
> 5. 选择系统的existence_protection_filtered字段与虚无主义检测的集成（与design-strategist对齐）
> 6. Ch 8（HARM_GUIDE章节）的内容预警和章节跳过的具体实现（与UX设计对齐）
