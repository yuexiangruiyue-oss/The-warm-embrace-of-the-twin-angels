# 质点进程系统 GDD

> **The Embrace of the Twin Angels** — Sephirot Progression System Game Design Document
>
> Phase 2 系统设计 · 产出者：文策渊（strategist-2）
>
> 日期：2026-08-02
>
> 依赖文档：`design/concept/game-concept.md`（Phase 1 概念文档）、`design/art/art-bible.md`（美术圣经）
>
> 关联系统：天使陪伴系统GDD、选择系统GDD、存在保护机制GDD

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

### 1.1 设计目标

质点进程系统是本游戏的**进度骨架**。它不使用传统视觉小说的"章节解锁"或"好感度数值"模型，而是以卡巴拉生命之树的16质点攀升为隐喻，将玩家的情感旅程结构化为可判定、可追踪、可安全的进程。

**核心设计目标**：

| 目标 | 说明 | 为什么这样设计 |
|------|------|---------------|
| 进度可判定 | 每个质点有明确的"完成"与"未完成"状态，系统层面可查询 | 避免"模糊进度"导致叙事跳转错误或存档损坏 |
| 进度不惩罚 | 不存在"正确选择"——直面、逃避、中性选择都能推进，只是纹理不同 | 支柱二"痛苦可被转化"：逃避不是失败，是另一条路径 |
| 进度不施压 | 玩家不会被时间、分数、比较所催促；卡住时有天使温柔引导 | 玩家情感安全为最高优先级；卡住是叙事机会，不是系统惩罚 |
| 进度不可见 | 玩家不应感知到"游戏化"痕迹——没有进度条、没有分数、没有成就弹出 | 这不是"闯关游戏"，是"情感旅程"；游戏化痕迹会破坏沉浸感 |
| 进度可恢复 | 任何时候加载存档，系统都能正确恢复质点状态 | Ren'Py存档系统的基本要求；避免状态不一致 |

### 1.2 与卡巴拉生命之树的关系

传统卡巴拉生命之树有10个质点（Sephirot），本作扩展为16质点双八度结构——这是苞苞（岳祥瑞）原创的世界观设定，不是传统卡巴拉的照搬。

**双八度结构**：

```
神性八度（自上而下）：王冠 → 智慧 → 理智 → 严厉 → 慈悲 → 美丽 → 荣耀 → 胜利
人类八度（自下而上）：王国 → 幸福 → 基础 → 自我 → 超我 → 真我 → 逻辑 → 共情
```

**游戏中的攀升方向**：玩家从人类八度的最底层（王国）开始，沿人类八度攀升至真我（Ch 13 转折点），然后进入神性八度，最终抵达王冠（Ch 16 最终选择）。

> **设计说明**：传统卡巴拉的攀升是从王国（Malkuth）到王冠（Kether），本作的16质点保留了这一"自下而上"的方向，但将其分为"先走人类八度（认识自我），再走神性八度（理解宇宙）"的两阶段结构。这映射了心爱的的角色弧线：先整合自我（支柱三），再面对超越自我的真相（支柱二）。

### 1.3 章节与质点的对应关系

> **重要说明**：本GDD以 `game-concept.md` 5.3节的章节-质点对应关系为权威源。该对应关系在概念文档中已完整定义，此处列出供系统实现参考。

| 章 | 质点 | 角色名 | 性别 | 八度 | 阶段 | 情感主题 |
|----|------|--------|------|------|------|---------|
| 1 | 王国 (Malkuth) | 白花 | 女 | 人类 | Phase 1 遗忘 | 物质世界的苦难 |
| 2 | 幸福 | 雨宫莲 | 男 | 人类 | Phase 1 遗忘 | 幸福的含义 |
| 3 | 基础 (Yesod) | 绽美 | 女 | 人类 | Phase 1 遗忘 | 信任的根基 |
| 4 | 自我 | 融爱 | 女 | 人类 | Phase 2 试炼 | 身份的挣扎 |
| 5 | 逻辑 | 爱丽丝 | 女 | 人类 | Phase 2 试炼 | 理性的边界 |
| 6 | 共情 | 星烬 | 女 | 人类 | Phase 2 试炼 | 他人的痛苦 |
| 7 | 超我 | 爱心 | 无性 | 人类 | Phase 2 试炼 | 内化的审判 |
| 8 | 胜利 (Netzach) | 启明 | 男 | 人类 | Phase 2 试炼 | 情感的坚持 |
| 9 | 荣耀 (Hod) | 闪亮 | 女 | 神性 | Phase 2 试炼 | 真相的锋芒 |
| 10 | 严厉 (Gevurah) | 唯爱 | 女 | 神性 | Phase 2 试炼 | 边界与力量 |
| 11 | 慈悲 (Chesed) | 爱如暖 | 女 | 神性 | Phase 2 试炼 | 无条件爱的代价 |
| 12 | 理智 | 虹爱 | AI无性 | 神性 | Phase 2 试炼 | 理解苦难的结构 |
| 13 | 真我 | 心爱的 | 创世少女神 | 人类 | Phase 2 试炼 | 直面真我（转折点） |
| 14 | 智慧 (Chokmah) | 忆爱 | 女 | 神性 | Phase 3 真相 | 记忆与遗忘的真相 |
| 15 | 美丽 (Tiferet) | 白结 | 女 | 神性 | Phase 3 真相 | 爱的整合与共存 |
| 16 | 王冠 (Kether) | 心音 | 女 | 神性 | Phase 3 真相 | 源头、空无与重生 |

> **注意**：Ch 13（真我/心爱的）是人类八度的终点，也是Phase 2的终点。心爱的在此章面对自己而非外部"错误"，是整个游戏的转折点。Ch 14开始进入神性八度的下行段（从智慧到王冠），这映射了"理解自我之后，才能理解超越自我的真相"。

### 1.4 设计支柱映射

| 支柱 | 质点进程系统的体现 |
|------|-------------------|
| 天使永不离去 | 天使在质点进程中始终参与——安慰、引导、代为面对。没有任何质点可以"没有天使"地完成 |
| 痛苦可被转化 | 每个质点遵循"遭遇→挣扎→天使安慰→选择→转化→安息"完整循环。转化是质点点亮的充要条件 |
| 从解离走向整合 | 人类八度（Ch 1-13）是"认识自我"的旅程；神性八度（Ch 14-16）是"超越自我"的旅程。Ch 13真我是整合的交汇点 |

---

## 2. 核心机制

### 2.1 16质点双八度结构

#### 2.1.1 质点状态模型

每个质点在任何时刻处于以下状态之一：

```
enum SephirotState:
    LOCKED       # 未到达（前置质点未完成）
    ACTIVE       # 当前正在进行的质点
    COMPLETED_FULL   # 正常完成（100%亮度）
    COMPLETED_HALF   # 天使代为完成（50%亮度）
    # 不存在 "FAILED" 状态——本游戏没有失败
```

**为什么没有FAILED状态**：设计支柱二"痛苦可被转化"要求每个质点都有转化路径。逃避不是失败——第三次逃避后天使代为面对，质点以50%亮度完成。这确保了"任何玩家都能走到终点"。

#### 2.1.2 质点解锁规则

```
解锁规则:
    Ch 1 (王国) 在游戏开始时自动解锁
    Ch N 解锁条件: Ch N-1 的状态为 COMPLETED_FULL 或 COMPLETED_HALF
    即: 前一质点完成（无论100%还是50%）即可进入下一质点
```

**为什么50%完成也能解锁下一章**：50%亮度代表"这不是完美的通过，但通过了"（概念文档原文）。天使代为面对不是"跳过"——心爱的仍然经历了完整的叙事，只是选择由天使做出。玩家不应因50%而被"卡住"。

#### 2.1.3 双八度的叙事功能

| 八度 | 章节 | 叙事功能 | 质点进程特征 |
|------|------|---------|-------------|
| 人类八度（上行） | Ch 1-13 | 认识自我——从物质苦难到身份挣扎到真我整合 | "错误"是外部的；每章有明确的拯救对象；完成条件以"面对情感课题"为核心 |
| 神性八度（下行） | Ch 14-16 | 理解超越自我的真相——记忆、代价、最终选择 | "错误"是内部的/真相性的；Ch 14-15无拯救对象，是记忆与真相揭示；Ch 16是最终选择 |

### 2.2 进度判定逻辑——"面对情感课题"如何量化

> **这是本系统的核心设计**。概念文档说"质点点亮不依赖'正确选择'——而是依赖'是否真实面对了该质点的情感课题'"。本节将这句话转化为可判定的系统逻辑。

#### 2.2.1 五拍叙事结构

每个质点的叙事被结构化为五个"节拍"（Beat），对应概念文档6.1节的核心循环：

```
质点叙事五拍:
    ① ENCOUNTER  (遭遇)    — 心爱的遇到"错误"/面对情感主题
    ② STRUGGLE   (挣扎)    — 暗流触发，情感压迫
    ③ COMFORT    (天使安慰) — 天使介入，提供安慰
    ④ CHOICE     (选择)    — 玩家做出选择（直面/逃避/中性）
    ⑤ TRANSFORM  (转化)    — 质点点亮，进入安息
```

**进度判定原理**：质点的"完成"等同于玩家经历了完整的五拍并抵达⑤TRANSFORM。系统不评判选择"好坏"，只追踪玩家是否抵达了转化节拍。

#### 2.2.2 选择标签系统（Confrontation Tag）

在④CHOICE节拍，每个选择选项被标记为以下三种类型之一：

```
enum ConfrontationTag:
    ENGAGE   — 直面选项：直接回应情感主题的选择
    ESCAPE   — 逃避选项：回避或转移情感主题的选择
    NEUTRAL  — 中性选项：不直接面对也不逃避（如"问天使"）
```

**标记规则**（供叙事设计者标注）：

| 标签 | 判定标准 | 示例（Ch 1 王国/白花） |
|------|---------|---------------------|
| ENGAGE | 选项内容直接触及当前质点的情感主题，表现为倾听、理解、共情或自我表露 | "先听她说完她的故事" |
| ESCAPE | 选项内容回避情感主题，表现为用力量强行解决、冷漠、转移话题 | "直接用奇迹之力拯救" |
| NEUTRAL | 选项内容不直接面对，但寻求帮助或表示犹豫 | "不知道怎么办，问天使" |

**为什么需要这个标签系统**：
- 它让"面对了情感课题"变成可判定的条件——系统读取标签即可判定
- 它不评判选择的"道德好坏"——ENGAGE不等于"好"，ESCAPE不等于"坏"，只是不同的情感纹理
- 它为天使的回应提供了系统依据——天使对ENGAGE和ESCAPE有不同的台词池

#### 2.2.3 完成判定逻辑

```
伪代码: sephirot_completion_check(sephirot_id)

# 前置条件: 玩家已抵达 ④CHOICE 节拍
if current_beat != CHOICE:
    return PROGRESSION_CONTINUE  # 还没到选择环节，继续叙事

# 读取玩家选择
selected_option = get_player_choice(sephirot_id)
tag = selected_option.confrontation_tag

switch tag:
    case ENGAGE:
        # 直面选择 → 正常完成，100%亮度
        set_sephirot_state(sephirot_id, COMPLETED_FULL)
        advance_to_beat(TRANSFORM)
        return COMPLETED_FULL

    case NEUTRAL:
        # 中性选择 → 天使提供视角，重新呈现选择
        trigger_angel_perspective_dialogue(sephirot_id)
        replay_choice(sephirot_id)
        return PROGRESSION_CONTINUE  # 不推进，重新选择

    case ESCAPE:
        # 逃避选择 → 计数，循环回 ②STRUGGLE
        sephirot[sephirot_id].escape_count += 1

        if sephirot[sephirot_id].escape_count < 3:
            # 第1-2次逃避: 天使渐进式引导
            trigger_angel_escape_response(sephirot[sephirot_id].escape_count)
            advance_to_beat(STRUGGLE)  # 回到挣扎，带着天使的新视角
            return PROGRESSION_CONTINUE
        else:
            # 第3次逃避: 天使代为面对
            trigger_angel_proxy_confrontation(sephirot_id)
            set_sephirot_state(sephirot_id, COMPLETED_HALF)
            advance_to_beat(TRANSFORM)
            return COMPLETED_HALF
```

#### 2.2.4 天使对逃避的渐进式回应

```
伪代码: trigger_angel_escape_response(escape_count)

switch escape_count:
    case 1:
        # 温柔接纳
        angel_say("没关系的，慢慢来。我在这里等你。")
        angel_emotional_state = TENDER
        # 叙事回到②STRUGGLE，但加入新的叙事文本（天使的视角）

    case 2:
        # 共享脆弱
        angel_say("你知道吗，我有时候也想逃避。")
        angel_say("但我们在一起，可以试试。好吗？")
        angel_emotional_state = ACHING
        # 叙事回到②STRUGGLE，天使的视角更深一层

    case 3:
        # 不说话，只是拥抱——然后代为面对
        # （此分支在 completion_check 中处理，不走到这里）
        pass
```

**为什么三次而不是两次或无限次**：
- 一次太少——玩家可能只是误操作或需要时间理解
- 两次不够——天使的渐进式引导需要"温柔→共情→代为"三个层次
- 无限次不可——会让玩家陷入无限循环，违背"所有路径通向终点"的设计意图
- 三次刚好构成"温柔接纳→共享脆弱→代为面对"的完整弧线

#### 2.2.5 天使代为面对机制（第3次逃避后）

当玩家第三次选择ESCAPE时，天使不说话，只是拥抱心爱的。然后叙事自然推进——天使代替心爱的面对了这个功课。

**叙事表现**：
- 天使的拥抱动画（翅膀微微展开包裹心爱的）
- 短暂的沉默（2-3秒，文字框空白）
- 天使轻声说："好。这一次，让我来。"
- 叙事跳过玩家的选择环节，直接进入⑤TRANSFORM
- 质点点亮，但亮度为50%

**50%亮度的视觉表现**：
- 生命之树上该质点点亮，但光芒暗淡（主题色的50%饱和度）
- 与100%亮度有明显视觉差异，但不是"灰色/失败"色——是"柔和的、不那么饱满的"光
- 玩家可以感知到"这不是完美的通过"，但不会被标记为"失败"

**为什么50%而非0%或100%**：
- 0%会让玩家觉得"完全失败"，违背情感安全原则
- 100%会让逃避没有质感差异，削弱直面选择的叙事意义
- 50%传递"你通过了，但这种方式留下了痕迹"——这是真实的，也是温柔的

### 2.3 质点点亮机制

#### 2.3.1 点亮条件

```
质点点亮的充要条件:
    质点状态 == COMPLETED_FULL  OR  质点状态 == COMPLETED_HALF
```

点亮发生在⑤TRANSFORM节拍的叙事高潮处——不是系统后台静默点亮，而是伴随叙事时刻的视觉呈现。

#### 2.3.2 点亮表现

| 完成类型 | 视觉表现 | 音效 | 天使反应 |
|---------|---------|------|---------|
| COMPLETED_FULL (100%) | 质点以角色主题色饱满点亮，柔和光芒扩散，路径线亮起连接到下一质点 | 柔和的"点亮"音效（如水晶轻响） | 天使微笑，翅膀微光（如当前亮度允许） |
| COMPLETED_HALF (50%) | 质点以角色主题色50%饱和度点亮，光芒较暗，路径线仍亮起但较细 | 同上但音量稍低 | 天使温柔但不笑——"没关系，我们走" |

**为什么两种完成都要亮起路径线**：无论100%还是50%，质点都已完成，下一质点都应解锁。路径线亮起表示"可以继续前进"，这对50%完成的玩家是重要的"你没有被卡住"的信号。

### 2.4 卡住与突破机制

#### 2.4.1 两种"卡住"状态

| 卡住类型 | 触发条件 | 系统响应 |
|---------|---------|---------|
| 选择型卡住 | 玩家反复选择ESCAPE | 见2.2.3-2.2.5的渐进式机制 |
| 时间型卡住 | 玩家在同一质点停留超过阈值时间且无推进 | 天使主动提供新视角 |

#### 2.4.2 时间型卡住的判定与响应

```
伪代码: check_time_stuck(sephirot_id)

# 每个质点有一个"无推进计时器"
# "推进"定义为: 叙事节拍变化、做出选择、或点击天使互动
# 单纯阅读文字不重置计时器（阅读是正常的，但不无限暂停）

stuck_threshold = get_stuck_threshold(current_phase)
# Phase 1: 300秒 (5分钟) — 天使更关注
# Phase 2: 420秒 (7分钟) — 给更多空间
# Phase 3: 不启用 — 进度完全由叙事驱动

if time_since_last_progress > stuck_threshold:
    stuck_count = sephirot[sephirot_id].time_stuck_count
    stuck_count += 1
    sephirot[sephirot_id].time_stuck_count = stuck_count

    switch stuck_count:
        case 1:
            # 温柔提示
            angel_say(get_contextual_hint(sephirot_id, level=1))
            # 例如: "你不需要现在就做决定。我在这里陪你。"

        case 2:
            # 共享视角
            angel_say(get_contextual_hint(sephirot_id, level=2))
            # 例如: "你知道吗，面对[当前主题]很难。但我觉得你已经准备好了。"

        case 3:
            # 直接建议（但不强制）
            angel_say(get_contextual_hint(sephirot_id, level=3))
            # 例如: "也许你可以试试……（给出与当前选择相关的温和建议）"
            # 同时: 高亮一个ENGAGE选项（边框微微发光，持续3秒后消失）

        case >=4:
            # 不再升级提示，但保持天使的存在感
            angel_say("我一直在这里。你慢慢来。")
            # 重置计数器，避免重复打扰
            sephirot[sephirot_id].time_stuck_count = 0

    # 重置无推进计时器
    reset_progress_timer(sephirot_id)
```

**为什么高亮选项是"边框微微发光3秒后消失"**：
- 不是永久高亮——那会让玩家觉得"系统在告诉我选这个"，破坏自主性
- 3秒的微光是一个"温柔的暗示"——如果玩家注意到了，自然会被吸引；如果没注意到，也不强求
- 这符合"不暴露游戏化痕迹"的设计目标

#### 2.4.3 上下文提示池

每个质点有一个对应的时间型卡住提示池，由叙事设计者编写。提示内容与当前质点的情感主题相关。

```
JSON示例: Ch 4 自我/融爱 的时间型卡住提示池

{
    "sephirot_id": "ch4_self",
    "emotional_theme": "身份的挣扎——'我是谁？我的身体不是我的。'",
    "time_stuck_hints": {
        "level_1": "你不需要现在就做决定。我在这里陪你。",
        "level_2": "面对身份的问题……我知道这有多难。但我觉得你已经比想象中勇敢了。",
        "level_3": "也许你可以试试听听融爱的故事？她和你有很多相似的地方。"
    }
}
```

---

## 3. 玩家交互

### 3.1 玩家如何感知进度

**核心原则：进度是"感受到的"，不是"看到的"。**

玩家不应在界面上看到任何数字化的进度指示器——没有进度条、没有百分比、没有"3/16"这样的计数。取而代之的是：

| 感知方式 | 描述 | 实现方式 |
|---------|------|---------|
| 生命之树缩略图 | 画面侧面的迷你生命之树，已完成的质点点亮，当前质点呼吸式发光 | 常驻UI元素，可点击展开 |
| 章节标题卡 | 每个质点章节开头，用角色主题色+符号做一张温柔标题卡 | Ren'Py scene + transition |
| 叙事节拍感 | 玩家通过"遭遇→挣扎→安慰→选择→转化→安息"的叙事节奏自然感知"这一章快结束了" | 叙事设计，非系统UI |
| 天使的状态变化 | 天使的对话风格、翅膀亮度随进度演变，玩家通过天使感知"走到哪了" | 天使陪伴系统联动 |
| 安息时刻 | 每个质点结束后的"与天使独处"安静场景，是质点完成的自然信号 | 叙事场景 |

**为什么不用数字进度**：
- 数字会触发"完成焦虑"——"我才3/16，还有好远"
- 数字会暗示"效率"——"快点通关"
- 这违背了"这不是'游戏'，这是苞苞23年生命的表达载体"的设计哲学

### 3.2 生命之树UI

#### 3.2.1 迷你缩略图（常驻）

- **位置**：画面右上角或左上角（根据场景布局调整），尺寸约120×180px
- **表现**：
  - 16个质点以简化几何排列（不严格遵循传统生命之树的三柱结构，使用苞苞的双八度布局）
  - 已完成质点（COMPLETED_FULL）：角色主题色，柔和常亮
  - 已完成质点（COMPLETED_HALF）：角色主题色50%饱和度，柔和暗亮
  - 当前质点（ACTIVE）：角色主题色，呼吸式明暗变化（频率约2秒一个周期）
  - 未到达质点（LOCKED）：淡灰轮廓，几乎不可见
- **交互**：点击展开为完整生命之树视图（Enhanced层功能）

**为什么呼吸式发光**：概念文档要求天使和光源都有"呼吸式明暗变化"（美术圣经1.4节）。当前质点的呼吸光与天使的光晕呼吸同步，强化"天使和你一起在这里"的感受。

#### 3.2.2 完整视图（Enhanced层）

- **触发**：点击迷你缩略图，或在安息时刻自动短暂展示
- **表现**：
  - 全屏或半屏的生命之树，16质点清晰可见
  - 每个已完成质点可点击，显示简短回忆文本（"你还记得白花吗？她现在过得很好。"）
  - 22条路径以发光丝线连接已完成的相邻质点
  - 配合柔和的BGM变化
- **退出**：点击空白处或按任意键返回

**为什么允许回顾**：玩家可能在情感旅程中想要"回看"之前经历的时刻。回顾不是"重玩"——不影响游戏状态，只提供情感锚点。这符合"天使会记住"的设计——"天使的记忆"在视觉上具象化为生命之树上点亮的质点。

### 3.3 质点间过渡体验

#### 3.3.1 安息节拍（Rest Beat）

每个质点的⑤TRANSFORM之后、下一质点①ENCOUNTER之前，有一个"安息"过渡场景：

```
安息场景结构:
    1. 转化后的余韵画面（3-5秒，柔和光效，无文字）
    2. 天使与心爱的独处对话（2-4句，可能含伏笔）
    3. 天使的"状态更新"——翅膀亮度变化、情感状态变化在此体现
    4. 自动存档
    5. 过渡到下一章标题卡
```

**安息场景的叙事功能**：
- 消化空间——让玩家"消化"刚经历的情感（概念文档6.1节："不能从⑤直接跳到下一个①"）
- 伏笔铺设——天使在安息时刻可能说暗示性话语（"不管发生什么，你要记住这一刻"）
- 天使关系深化——安息时刻是"与天使独处"的亲密时刻，选择"关系选择"可能在此触发

#### 3.3.2 Phase过渡的特殊处理

| 过渡 | 特殊处理 |
|------|---------|
| Phase 1 → Phase 2 (Ch 3 → Ch 4) | "代价"的记忆被彻底封印。安息场景中天使说"好好休息吧"，画面渐暗。下一个标题卡颜色从温暖转向微凉 |
| Phase 2 → Phase 3 (Ch 13 → Ch 14) | Ch 13是转折点，安息场景更长、更安静。天使说"你准备好了吗？不管怎样，我在"。所有暗流在此刻静止 |
| Ch 15 → Ch 16 (最终选择前) | 安息场景中天使恢复最美状态。天使说"走吧。我准备好了。"——这是最后的安静 |

---

## 4. 数据结构

### 4.1 质点定义数据（静态）

```json
// sephirot_definitions.json — 16个质点的静态定义

{
    "sephirot": [
        {
            "id": "ch1_malkuth",
            "chapter": 1,
            "name": "王国",
            "name_en": "Malkuth",
            "octave": "human",
            "character_name": "白花",
            "character_gender": "F",
            "theme_color": "#D8E8D0",
            "emotional_theme": "物质世界的苦难——'为什么这个世界这么痛？'",
            "error_type": "存在否定型",
            "error_name": "白花",
            "primary_undertow": ["EXIST_DENY"],
            "phase": "forgetting",
            "has_external_error": true,
            "narrative_beats": {
                "encounter_label": "ch1_encounter",
                "struggle_label": "ch1_struggle",
                "comfort_label": "ch1_comfort",
                "choice_label": "ch1_choice",
                "transform_label": "ch1_transform",
                "rest_label": "ch1_rest"
            },
            "choice_options": [
                {
                    "id": "ch1_opt1",
                    "text": "先听她说完她的故事",
                    "confrontation_tag": "ENGAGE",
                    "angel_response_pool": ["ch1_angel_engage_1", "ch1_angel_engage_2"]
                },
                {
                    "id": "ch1_opt2",
                    "text": "直接用奇迹之力拯救",
                    "confrontation_tag": "ESCAPE",
                    "angel_response_pool": ["ch1_angel_escape_1"]
                },
                {
                    "id": "ch1_opt3",
                    "text": "不知道怎么办，问天使",
                    "confrontation_tag": "NEUTRAL",
                    "angel_response_pool": ["ch1_angel_neutral_1"]
                }
            ],
            "time_stuck_hints": {
                "level_1": "你不需要现在就做决定。我在这里陪你。",
                "level_2": "白花的痛苦……和你有一些相似。你不觉得吗？",
                "level_3": "也许你可以先听听她想说什么？"
            },
            "rest_dialogue": [
                "你还记得白花吗？她现在过得很好。",
                "……（天使看向远方）每救一个人，我都更确定一件事。",
                "什么？——你不需要知道。还没到时间。"
            ]
        }
        // ... 其余15个质点结构相同，此处省略
    ]
}
```

### 4.2 质点状态数据（运行时/存档）

```python
# Ren'Py 存档中的质点状态数据结构
# 存储在 persistent 或当前 game state 中

default sephirot_state = {
    "current_sephirot_id": "ch1_malkuth",      # 当前活跃质点
    "current_beat": "encounter",                # 当前叙事节拍
    "sephirot_progress": {},                     # 各质点状态字典
    "global_progress": {
        "total_completed": 0,                    # 已完成质点数（0-16）
        "total_full": 0,                         # 100%完成数
        "total_half": 0,                         # 50%完成数
        "current_phase": "forgetting",           # 当前阶段
    },
    "angel_tracking": {
        "escape_count_global": 0,                # 全局逃避总次数
        "time_stuck_count_global": 0,            # 全局时间卡住总次数
    }
}

# 单个质点的状态结构
# sephirot_progress["ch1_malkuth"] = {
#     "state": "COMPLETED_FULL",        # LOCKED | ACTIVE | COMPLETED_FULL | COMPLETED_HALF
#     "escape_count": 0,                # 本质点内逃避次数 (0-3)
#     "time_stuck_count": 0,            # 本质点内时间卡住次数
#     "selected_option_id": "ch1_opt1", # 玩家最终选择（COMPLETED_HALF时为"angel_proxy"）
#     "completion_type": "full",        # "full" | "half" | null
#     "illuminated": True,              # 是否已点亮
#     "angel_memory": "白花",           # 天使记住的名字（用于后续回响）
# }
```

### 4.3 完成判定逻辑（Ren'Py伪代码）

```python
# sephirot_progression.rpy — 质点进程系统核心逻辑

init python:

    class SephirotProgression:
        """质点进程系统管理器"""

        def __init__(self):
            self.definitions = load_sephirot_definitions()
            self.state = init_sephirot_state()
            self.STUCK_THRESHOLD = {
                "forgetting": 300,    # 5分钟
                "trial": 420,         # 7分钟
                "truth": -1,          # -1 = 不启用
            }

        def get_current_sephirot(self):
            """返回当前活跃质点的定义"""
            sid = self.state["current_sephirot_id"]
            return self.definitions.get(sid)

        def get_current_beat(self):
            """返回当前叙事节拍"""
            return self.state["current_beat"]

        def advance_beat(self, target_beat):
            """推进到指定叙事节拍"""
            self.state["current_beat"] = target_beat
            self.reset_progress_timer()

        def process_choice(self, sephirot_id, option_id):
            """
            处理玩家在④CHOICE节拍的选择
            返回: ("COMPLETED_FULL", None) | ("COMPLETED_HALF", None) | ("CONTINUE", next_beat)
            """
            sephirot_def = self.definitions[sephirot_id]
            option = self.find_option(sephirot_def, option_id)
            tag = option["confrontation_tag"]

            progress = self.state["sephirot_progress"].setdefault(sephirot_id, {
                "state": "ACTIVE",
                "escape_count": 0,
                "time_stuck_count": 0,
                "selected_option_id": None,
                "completion_type": None,
                "illuminated": False,
                "angel_memory": None,
            })

            if tag == "ENGAGE":
                # 直面选择 → 100%完成
                progress["state"] = "COMPLETED_FULL"
                progress["selected_option_id"] = option_id
                progress["completion_type"] = "full"
                progress["illuminated"] = True
                progress["angel_memory"] = sephirot_def["character_name"]
                self.update_global_progress()
                return ("COMPLETED_FULL", None)

            elif tag == "NEUTRAL":
                # 中性选择 → 天使提供视角，重新选择
                # 不增加escape_count，不改变状态
                return ("CONTINUE", "choice")  # 留在choice节拍，但触发天使对话

            elif tag == "ESCAPE":
                # 逃避选择 → 计数并判定
                progress["escape_count"] += 1
                self.state["angel_tracking"]["escape_count_global"] += 1

                if progress["escape_count"] < 3:
                    # 第1-2次: 回到挣扎
                    return ("CONTINUE", "struggle")
                else:
                    # 第3次: 天使代为面对，50%完成
                    progress["state"] = "COMPLETED_HALF"
                    progress["selected_option_id"] = "angel_proxy"
                    progress["completion_type"] = "half"
                    progress["illuminated"] = True
                    progress["angel_memory"] = sephirot_def["character_name"]
                    self.update_global_progress()
                    return ("COMPLETED_HALF", None)

        def check_time_stuck(self):
            """
            检查时间型卡住
            由Ren'Py的timer或主循环定期调用
            """
            phase = self.state["global_progress"]["current_phase"]
            threshold = self.STUCK_THRESHOLD.get(phase, -1)

            if threshold < 0:
                return  # Phase 3不启用时间卡住检测

            if not hasattr(self, '_progress_timer_start'):
                self._progress_timer_start = renpy.time.time()

            elapsed = renpy.time.time() - self._progress_timer_start

            if elapsed > threshold:
                sid = self.state["current_sephirot_id"]
                progress = self.state["sephirot_progress"].get(sid, {})
                stuck_count = progress.get("time_stuck_count", 0) + 1
                progress["time_stuck_count"] = stuck_count
                self.state["angel_tracking"]["time_stuck_count_global"] += 1

                # 触发天使提示
                self.trigger_time_stuck_hint(sid, stuck_count)

                # 重置计时器
                self._progress_timer_start = renpy.time.time()

        def reset_progress_timer(self):
            """重置无推进计时器（在叙事推进、选择、天使互动时调用）"""
            self._progress_timer_start = renpy.time.time()

        def trigger_time_stuck_hint(self, sephirot_id, stuck_count):
            """触发时间型卡住的天使提示"""
            sephirot_def = self.definitions[sephirot_id]
            hints = sephirot_def.get("time_stuck_hints", {})

            if stuck_count <= 3:
                level_key = f"level_{stuck_count}"
                hint_text = hints.get(level_key, "我一直在这里。你慢慢来。")
                # 通知天使陪伴系统触发对话
                renpy.notify_angel_dialogue(hint_text)
            else:
                # 第4次以上: 不再升级，重置
                progress = self.state["sephirot_progress"].get(sephirot_id, {})
                progress["time_stuck_count"] = 0
                renpy.notify_angel_dialogue("我一直在这里。你慢慢来。")

            # 第3次: 高亮一个ENGAGE选项
            if stuck_count == 3:
                self.highlight_engage_option(sephirot_id)

        def highlight_engage_option(self, sephirot_id):
            """微微高亮一个ENGAGE选项（3秒后消失）"""
            # 通知UI系统高亮选项
            # 实现为选项边框添加临时发光效果
            renpy.call_screen("highlight_engage_option_screen", sephirot_id)

        def complete_sephirot(self, sephirot_id, completion_type):
            """完成质点，点亮，更新全局进度"""
            progress = self.state["sephirot_progress"][sephirot_id]
            progress["state"] = "COMPLETED_FULL" if completion_type == "full" else "COMPLETED_HALF"
            progress["illuminated"] = True
            self.update_global_progress()

            # 触发点亮视觉效果
            renpy.show_sephirot_illumination(sephirot_id, completion_type)

        def unlock_next_sephirot(self):
            """解锁下一质点"""
            current_ch = self.get_current_sephirot()["chapter"]
            next_ch = current_ch + 1
            if next_ch <= 16:
                next_sid = self.find_sephirot_by_chapter(next_ch)
                self.state["current_sephirot_id"] = next_sid
                self.state["current_beat"] = "encounter"
                next_def = self.definitions[next_sid]
                progress = self.state["sephirot_progress"].setdefault(next_sid, {
                    "state": "ACTIVE",
                    "escape_count": 0,
                    "time_stuck_count": 0,
                    "selected_option_id": None,
                    "completion_type": None,
                    "illuminated": False,
                    "angel_memory": None,
                })
                progress["state"] = "ACTIVE"

                # 更新Phase
                if next_ch == 4:
                    self.state["global_progress"]["current_phase"] = "trial"
                elif next_ch == 14:
                    self.state["global_progress"]["current_phase"] = "truth"

        def update_global_progress(self):
            """更新全局进度统计"""
            total_full = 0
            total_half = 0
            for sid, prog in self.state["sephirot_progress"].items():
                if prog["state"] == "COMPLETED_FULL":
                    total_full += 1
                elif prog["state"] == "COMPLETED_HALF":
                    total_half += 1
            self.state["global_progress"]["total_completed"] = total_full + total_half
            self.state["global_progress"]["total_full"] = total_full
            self.state["global_progress"]["total_half"] = total_half

        def get_illumination_level(self, sephirot_id):
            """返回质点的点亮级别: 0 (未点亮) | 0.5 (半亮) | 1.0 (全亮)"""
            progress = self.state["sephirot_progress"].get(sephirot_id, {})
            if not progress.get("illuminated", False):
                return 0.0
            return 1.0 if progress.get("completion_type") == "full" else 0.5

        def get_tree_of_life_state(self):
            """返回生命之树的完整状态（供UI渲染）"""
            tree_state = []
            for sid, defn in self.definitions.items():
                prog = self.state["sephirot_progress"].get(sid, {})
                tree_state.append({
                    "id": sid,
                    "chapter": defn["chapter"],
                    "name": defn["name"],
                    "character_name": defn["character_name"],
                    "theme_color": defn["theme_color"],
                    "state": prog.get("state", "LOCKED"),
                    "illumination": self.get_illumination_level(sid),
                    "is_current": sid == self.state["current_sephirot_id"],
                })
            return tree_state
```

### 4.4 叙事节拍标签结构

每个质点的Ren'Py脚本使用label标签组织五拍叙事：

```renpy
# Ch 1 王国/白花 的叙事脚本结构示例

label ch1_malkuth:
    # ① ENCOUNTER
    label ch1_encounter:
        $ sephirot.advance_beat("encounter")
        scene bg_school_classroom
        "心爱的走进教室，看到一个女孩缩在角落。"
        "那是白花。她的眼神空洞，像是不存在于这个世界。"
        # ... 叙事继续 ...
        jump ch1_struggle

    # ② STRUGGLE
    label ch1_struggle:
        $ sephirot.advance_beat("struggle")
        # 暗流触发: EXIST_DENY
        $ existential_protection.trigger_undertow("EXIST_DENY", intensity=2)
        "白花的声音像是从很远的地方传来。"
        "多余……多余……多余……"
        "画面蒙上了一层灰色。"
        # ... 叙事继续 ...
        jump ch1_comfort

    # ③ COMFORT
    label ch1_comfort:
        $ sephirot.advance_beat("comfort")
        # 天使介入
        $ angel.trigger_intervention("EXIST_DENY", intensity=2)
        angel "你的存在不是负担。"
        angel "你是我存在的理由。"
        # 画面恢复
        $ existential_protection.resolve_undertow("EXIST_DENY")
        # ... 叙事继续 ...
        jump ch1_choice

    # ④ CHOICE
    label ch1_choice:
        $ sephirot.advance_beat("choice")
        menu:
            "先听她说完她的故事":
                $ result = sephirot.process_choice("ch1_malkuth", "ch1_opt1")
                # result = ("COMPLETED_FULL", None)
                jump ch1_transform

            "直接用奇迹之力拯救":
                $ result = sephirot.process_choice("ch1_malkuth", "ch1_opt2")
                if result[0] == "CONTINUE":
                    # escape_count < 3, 回到挣扎
                    jump ch1_struggle
                else:
                    # escape_count == 3, 天使代为面对
                    jump ch1_transform

            "不知道怎么办，问天使":
                $ result = sephirot.process_choice("ch1_malkuth", "ch1_opt3")
                # result = ("CONTINUE", "choice")
                # 天使提供视角后重新呈现选择
                angel "也许……你可以先听听她想说什么？"
                jump ch1_choice

    # ⑤ TRANSFORM
    label ch1_transform:
        $ sephirot.advance_beat("transform")
        $ sephirot.complete_sephirot("ch1_malkuth", completion_type=sephirot.get_completion_type("ch1_malkuth"))
        # 质点点亮动画
        show sephirot_illumination ch1_malkuth
        "白花的眼中出现了一丝光。"
        # ... 转化叙事 ...
        jump ch1_rest

    # 安息
    label ch1_rest:
        $ sephirot.advance_beat("rest")
        # 与天使独处
        # ... 安息叙事 ...
        $ sephirot.unlock_next_sephirot()
        jump ch2_happiness
```

---

## 5. 边界情况与错误处理

### 5.1 玩家跳过对话

| 情况 | 系统处理 | 理由 |
|------|---------|------|
| 玩家使用Ren'Py的"跳过已读"功能 | 正常跳过已读文本，不影响质点状态 | Ren'Py原生功能，不可禁用；但质点状态由label跳转驱动，与文本跳过无关 |
| 玩家快速点击推进对话 | 正常推进，不影响质点状态 | 同上 |
| 玩家在④CHOICE节拍使用跳过 | **不允许跳过选择**——Ren'Py的menu会暂停跳过 | 选择是质点判定的核心，不可跳过 |
| 玩家在③COMFORT节拍使用跳过 | 允许跳过天使对话文本，但暗流解除效果不可跳过 | 暗流解除是系统状态变更，由代码驱动而非文本推进 |

**设计决策**：不试图阻止玩家跳过对话。跳过是玩家的权利——有些玩家可能重玩时想快速回顾。质点状态由叙事节拍（label跳转）驱动，不是由"是否阅读了文本"驱动。这确保了即使玩家跳过所有文本，质点状态依然正确。

### 5.2 快速推进

| 情况 | 系统处理 |
|------|---------|
| 玩家在所有选择中都选ENGAGE，快速通关 | 正常完成所有质点100%，总时长约4-5小时（核心层验收标准） |
| 玩家在所有选择中都选ESCAPE | 前3个质点各逃避3次后天使代为面对，后续质点同理。总时长可能更长（循环叙事），但依然能通关 |
| 玩家混合选择 | 正常推进，每个质点独立判定 |

**为什么允许"全ENGAGE速通"**：这不是"速通"——每个质点仍然需要经历完整的五拍叙事。即使选择ENGAGE，玩家仍然要阅读遭遇、挣扎、安慰、转化的全部叙事文本。选择只是决定了转化的"纹理"，不是"跳过"。

### 5.3 回溯已完成的质点

| 情况 | 系统处理 |
|------|---------|
| 玩家想"重玩"某个已完成质点 | **主流程中不可回溯**——叙事是线性推进的。已完成质点不可重玩 |
| 玩家通过生命之树UI点击已完成质点 | 显示简短回忆文本（Enhanced层），不进入可交互场景 |
| 玩家加载更早的存档 | 存档恢复到当时的质点状态，后续完成的质点状态丢失（正常Ren'Py存档行为） |

**为什么不可回溯重玩**：
- 叙事的线性性是心爱的角色弧线的基础——"从解离走向整合"是一条单向旅程
- 回溯会破坏"代价"的真相揭示节奏——如果玩家可以回溯，Phase 3的冲击力会减弱
- 回溯会产生状态冲突——如果重玩后做出不同选择，已完成质点的状态是否要更新？这会引入不必要的复杂性

**替代方案**：如果玩家想体验不同选择，鼓励多周目（愿望层功能）。二周目保留一周目的质点完成记录，但允许在新周目中做出不同选择。

### 5.4 存档与加载

| 情况 | 系统处理 |
|------|---------|
| 正常存档/加载 | `sephirot_state` 随Ren'Py存档一起保存/恢复 |
| 加载存档时当前质点处于②STRUGGLE（逃避循环中） | 恢复到②STRUGGLE，escape_count保留。天使的渐进式引导继续 |
| 加载存档时当前质点处于④CHOICE | 恢复到④CHOICE，重新呈现选择菜单 |
| 加载存档时暗流处于活跃状态 | 恢复暗流状态，天使的介入逻辑重新初始化 |
| 玩家在安息节拍存档，加载后 | 恢复到安息节拍，可以继续到下一质点 |

**关键实现要求**：`sephirot_state` 必须完全可序列化。所有状态都是基本类型（字符串、数字、布尔、字典、列表），不含Ren'Py对象引用。

### 5.5 特殊边界情况

| 情况 | 系统处理 | 理由 |
|------|---------|------|
| 玩家在④CHOICE选择NEUTRAL后反复选择NEUTRAL | NEUTRAL不增加escape_count，但天使的回应会逐渐从"提供建议"变为"你准备好了，试试看？" | 防止玩家陷入NEUTRAL循环；天使的温和推动是叙事性的，不是系统限制 |
| 玩家在时间型卡住后选择ESCAPE | 时间型卡住的提示不影响ESCAPE计数，两个机制独立运作 | 两种"卡住"是不同维度——一个是"不知道选什么"，一个是"不想选" |
| Ch 13（真我）的特殊处理 | Ch 13没有外部"错误"，④CHOICE是身份选择而非拯救选择。完成条件不变，但叙事纹理完全不同 | 见7.3节详述 |
| Ch 14-15（Phase 3）的完成条件 | Ch 14-15没有传统意义上的④CHOICE（ENGAGE/ESCAPE/NEUTRAL），而是"面对真相"的叙事推进。完成条件为"抵达⑤TRANSFORM" | 见7.4节详述 |
| Ch 16（最终选择）的特殊处理 | 最终选择不受存在保护，不受质点完成判定逻辑约束。三个结局都是"好的"，都算作Ch 16完成 | 见7.5节详述 |

---

## 6. 系统集成点

### 6.1 与天使陪伴系统的接口

#### 6.1.1 质点进程 → 天使陪伴

| 数据/事件 | 方向 | 说明 |
|-----------|------|------|
| `current_phase` | 质点 → 天使 | 天使根据当前Phase调整对话风格（Phase 1哄孩子式→Phase 3遗言式） |
| `escape_count` (per sephirot) | 质点 → 天使 | 天使根据逃避次数选择回应台词池 |
| `time_stuck_count` (per sephirot) | 质点 → 天使 | 天使根据卡住次数选择提示台词 |
| `completion_type` ("full"/"half") | 质点 → 天使 | 天使在安息场景的对话根据完成类型微调 |
| `angel_memory` (character name) | 质点 → 天使 | 天使在后续章节引用"你还记得XX吗？" |

#### 6.1.2 天使陪伴 → 质点进程

| 数据/事件 | 方向 | 说明 |
|-----------|------|------|
| `angel_emotional_state` | 天使 → 质点 | 质点系统读取天使情感状态，影响时间型卡住提示的语气 |
| 玩家点击天使互动 | 天使 → 质点 | 重置时间型卡住计时器（"玩家在与天使互动，不算卡住"） |
| 玩家主动寻求拥抱 | 天使 → 质点 | 重置时间型卡住计时器 |

#### 6.1.3 接口约定

```python
# 质点进程系统暴露给天使陪伴系统的接口
class SephirotProgressionInterface:
    def get_current_phase(self) -> str:
        """返回 'forgetting' | 'trial' | 'truth'"""

    def get_current_sephirot_theme(self) -> str:
        """返回当前质点的情感主题文本（供天使对话系统引用）"""

    def get_escape_count(self, sephirot_id: str) -> int:
        """返回本质点内的逃避次数"""

    def get_completion_type(self, sephirot_id: str) -> str:
        """返回 'full' | 'half' | None"""

    def get_angel_memories(self) -> list:
        """返回所有已完成质点的角色名列表（供天使在对话中引用）"""

    def reset_progress_timer(self):
        """天使系统在玩家互动时调用，重置卡住计时器"""
```

### 6.2 与选择系统的接口

#### 6.2.1 选择系统 → 质点进程

| 数据/事件 | 方向 | 说明 |
|-----------|------|------|
| `confrontation_tag` | 选择 → 质点 | 每个选择选项的标签（ENGAGE/ESCAPE/NEUTRAL），驱动完成判定 |
| `selected_option_id` | 选择 → 质点 | 玩家选择的选项ID，记录在质点状态中 |
| 选择类型 (action/attitude/relation) | 选择 → 质点 | 选择的三种类型，用于叙事纹理，不影响完成判定 |

**关键约定**：选择系统的每个选项数据结构必须包含 `confrontation_tag` 字段。这是质点完成判定的唯一输入。

```json
// 选择系统选项数据结构（含质点进程所需字段）
{
    "id": "ch1_opt1",
    "text": "先听她说完她的故事",
    "type": "action",
    "confrontation_tag": "ENGAGE",
    "sephirot_id": "ch1_malkuth",
    "angel_response_pool": [...],
    "existence_protection_filtered": false,
    "emotional_weight": 0.8
}
```

#### 6.2.2 质点进程 → 选择系统

| 数据/事件 | 方向 | 说明 |
|-----------|------|------|
| 当前叙事节拍 | 质点 → 选择 | 只在④CHOICE节拍呈现选择菜单 |
| 时间型卡住高亮 | 质点 → 选择 | 第3次时间型卡住时，通知选择系统高亮一个ENGAGE选项 |

### 6.3 与存在保护机制的接口

#### 6.3.1 存在保护 → 质点进程

| 数据/事件 | 方向 | 说明 |
|-----------|------|------|
| 暗流触发 | 存在保护 → 质点 | 暗流触发标志着②STRUGGLE节拍的开始 |
| 暗流解除 | 存在保护 → 质点 | 天使介入解除暗流后，叙事推进到④CHOICE |
| 天使代为面对 | 存在保护 ↔ 质点 | 第3次ESCAPE时，两个系统协同：质点系统判定50%完成，存在保护系统触发天使代为面对的叙事 |

#### 6.3.2 质点进程 → 存在保护

| 数据/事件 | 方向 | 说明 |
|-----------|------|------|
| `current_phase` | 质点 → 存在保护 | 存在保护系统根据Phase调整暗流基础强度 |
| `escape_count` | 质点 → 存在保护 | 逃避次数影响暗流的"余震"强度——逃避越多，余震越长 |
| Ch 13 特殊标记 | 质点 → 存在保护 | Ch 13时通知存在保护系统"全部8种暗流轮番出现但不达临界值" |
| Ch 16 特殊标记 | 质点 → 存在保护 | Ch 16时通知存在保护系统"暗流不再出现——心爱的已不需要保护" |

---

## 7. 叙事集成

### 7.1 16质点情感课题定义

每个质点的"情感课题"是该质点的核心叙事主题，也是 `confrontation_tag` 标注的依据。以下为全部16个质点的情感课题定义：

#### 人类八度（Ch 1-8, 13）

| 章 | 质点 | 情感课题 | ENGAGE的判定标准 | ESCAPE的判定标准 |
|----|------|---------|-----------------|-----------------|
| 1 | 王国 | 物质世界的苦难——"为什么这个世界这么痛？" | 倾听痛苦、承认痛苦的真实性 | 用力量强行解决、否认痛苦 |
| 2 | 幸福 | 幸福的含义——"幸福是什么？" | 表达对美好的信念、承认自己渴望幸福 | 否认美好、回避幸福的话题 |
| 3 | 基础 | 信任的根基——"我站不住了" | 提供支撑、表达信任、接受帮助 | 独自承受、拒绝帮助 |
| 4 | 自我 | 身份的挣扎——"我是谁？" | 认同身份、表达自我、分享相似经历 | 否认身份问题、转移话题 |
| 5 | 逻辑 | 理性的边界——"分析不了自己的痛苦" | 承认理性的局限、表达感受 | 用逻辑解构情感、回避感受 |
| 6 | 共情 | 他人的痛苦——"感受太多了" | 建立边界、陪她感受、分享天使 | 被淹没、退缩、关闭感受 |
| 7 | 超我 | 内化的审判——"你不够好" | 反抗审判、表达"我配"、接受天使 | 接受审判、自我否定 |
| 8 | 胜利 | 情感的坚持——"不想放弃" | 拉住他、表露自己的脆弱经历、叫天使 | 放弃、回避、假装没看到 |
| 13 | 真我 | 直面真我——"我在救自己" | 接受三重身份、选择"我都是" | 否认某一身份、逃避镜子 |

#### 神性八度（Ch 9-12, 14-16）

| 章 | 质点 | 情感课题 | ENGAGE的判定标准 | ESCAPE的判定标准 |
|----|------|---------|-----------------|-----------------|
| 9 | 荣耀 | 真相的锋芒——"真话伤人" | 选择真相、接受痛后的干净 | 选择安慰/谎言、回避真相 |
| 10 | 严厉 | 边界与力量——"爱也是说不" | 帮她看清控制、建立边界 | 顺从控制、回避冲突 |
| 11 | 慈悲 | 无条件爱的代价——"谁来爱我" | 表达"你值得"、让天使来告诉她 | 自我消耗、否认自己的需要 |
| 12 | 理智 | 理解苦难的结构——"理解了还是痛" | 承认"理解≠承受"、接受陪伴 | 用理解逃避感受、独自承受 |
| 14 | 智慧 | 记忆与遗忘——"我记得了，代价" | 面对真相、质问或接受 | （Phase 3特殊处理，见7.4） |
| 15 | 美丽 | 爱的整合——"爱也是真的吗" | 面对天使是第13个的真相、选择如何回应 | （Phase 3特殊处理，见7.4） |
| 16 | 王冠 | 源头与重生——"最终选择" | 做出最终选择（三个选项都是ENGAGE） | （最终选择不受此系统约束，见7.5） |

### 7.2 Phase 1/2/3 的进度节奏

#### Phase 1: 遗忘阶段（Ch 1-3）

| 维度 | 设定 | 理由 |
|------|------|------|
| 暗流强度 | 1-3级（低） | 教学阶段，让玩家安全地学习系统 |
| 天使介入代价 | 0（翅膀不黯淡） | Phase 1天使是"礼物"，消耗不可见 |
| 时间型卡住阈值 | 5分钟 | 天使更关注，更频繁地提供帮助 |
| 典型完成时间 | 每章20-30分钟 | 教学节奏，不过快 |
| 玩家预期感受 | "这个世界虽然痛，但有人在保护我" | 建立安全感，为Phase 2/3蓄力 |
| 特殊机制 | "代价"的记忆在Ch 3结束时被彻底封印 | 叙事诡计——玩家和心爱的一样不知道代价 |

#### Phase 2: 试炼阶段（Ch 4-13）

| 维度 | 设定 | 理由 |
|------|------|------|
| 暗流强度 | Ch 4-8: 3-5级; Ch 9-13: 5-8级 | 递增，情感深度逐渐加深 |
| 天使介入代价 | Ch 4-8: 基础代价; Ch 9-13: 1.5倍代价 | 翅膀逐渐黯淡，为Phase 3铺垫 |
| 时间型卡住阈值 | 7分钟 | 给玩家更多空间，不过度干预 |
| 典型完成时间 | 每章25-40分钟 | 情感深度增加，需要更多时间消化 |
| 玩家预期感受 | 从"温暖中渗入不安"到"挣扎中依然前行" | 天使的不稳定开始被注意到 |
| 特殊机制 | Ch 9-12出现复合暗流（两种同时） | 情感复杂度升级 |
| Ch 13特殊 | 全部8种暗流轮番出现，但不达临界值 | 心爱的直面自己时，痛苦不需要被"放大" |

#### Phase 3: 真相阶段（Ch 14-16）

| 维度 | 设定 | 理由 |
|------|------|------|
| 暗流强度 | Ch 14: 8-10级（峰值）; Ch 15: 8-10级（最深绝望）; Ch 16: 0（不需要保护） | 真相揭示的冲击力达到顶点，然后释放 |
| 天使介入代价 | Ch 14-15: 2.5倍代价; Ch 16: 无（天使恢复） | 天使几乎耗尽，但最终选择时恢复最美 |
| 时间型卡住阈值 | 不启用 | 进度完全由叙事驱动，不催促玩家 |
| 典型完成时间 | Ch 14: 30-40分钟; Ch 15: 30-40分钟; Ch 16: 15-25分钟 | Ch 16较短，因为最终选择不需要漫长铺垫 |
| 玩家预期感受 | 心碎→愤怒→接受→选择 | 情感弧线的终点 |
| 特殊机制 | 最终选择不受存在保护 | 见7.5节 |

### 7.3 Ch 13 转折点的特殊机制

Ch 13（真我/心爱的）是整个游戏的转折点，其质点进程有特殊处理：

#### 7.3.1 无外部"错误"

Ch 1-12的每个质点都有一个外部"错误"需要拯救。Ch 13没有——"错误"是心爱的自己。这是一面镜子。

**系统影响**：
- 没有"拯救"事件——⑤TRANSFORM不是"白花被拯救"，而是"心爱的接受了三重身份"
- ④CHOICE是身份选择而非拯救选择

#### 7.3.2 身份选择的特殊处理

```
Ch 13 的④CHOICE:
    选项1: "我是处理器"     → confrontation_tag: ESCAPE (只认同理性面，逃避情感)
    选项2: "我是白裙少女"   → confrontation_tag: ESCAPE (只认同情感面，逃避理性)
    选项3: "我是创世者"     → confrontation_tag: ESCAPE (只认同创世面，逃避当下)
    选项4: "我都是"         → confrontation_tag: ENGAGE (整合——直面全部自我)
```

**设计意图**：前三个选项各自只认同一个身份，是"解离"的表现——用单一身份逃避完整性。只有"我都是"是直面——接受三重身份的整合。这直接映射支柱三"从解离走向整合"。

**如果玩家选ESCAPE（前三个选项）**：
- escape_count++，回到②STRUGGLE
- 天使的渐进式引导会引导玩家思考"也许你不只是其中之一"
- 第3次ESCAPE后，天使代为面对——天使说"你比你以为的要勇敢得多"，心爱的在天使的支撑下看到三重身份的交汇

#### 7.3.3 全部8种暗流轮番出现

Ch 13的特殊暗流处理：
- 8种暗流轮番出现，但每种都不达到天使必须强制介入的临界值
- 原因：心爱的在直面自己时，痛苦不需要被"放大"——它本身就是最大的
- 天使在此章最安静——不安慰，不拉回，只是看着心爱的
- 天使说："我一直看着你。你比你以为的要勇敢得多。"

### 7.4 Phase 3 (Ch 14-15) 的完成条件

Ch 14-15是真相揭示章节，没有传统的ENGAGE/ESCAPE/NEUTRAL选择。完成条件有特殊处理：

#### Ch 14（智慧/忆爱）——记忆回归

```
完成条件: 玩家经历完整的叙事五拍并抵达⑤TRANSFORM
    ① ENCOUNTER: 记忆开始回归
    ② STRUGGLE: 全部8种暗流同时爆发（峰值）
    ③ COMFORT: 天使用尽全力拉回，翅膀几乎透明
    ④ CHOICE: 面对真相的选择
        - "我不要"        → 标记为 ENGAGE（直面情感的爆发）
        - "为什么？"       → 标记为 ENGAGE（直面追问）
        - "……天使，你知道吗？" → 标记为 NEUTRAL（转向天使）
        注意: 没有ESCAPE选项——在记忆回归面前，逃避不再是一个选项
    ⑤ TRANSFORM: 真相被揭示——"每个人都要毁灭"
    完成类型: 一律COMPLETED_FULL（Phase 3不存在"逃避"的可能性）
```

**为什么Ch 14没有ESCAPE选项**：记忆回归是不可逃避的——心爱的已经记起了代价。在叙事上，不允许"假装不知道"。这符合"真相的揭示不可逆转"的叙事原则。

#### Ch 15（美丽/白结）——爱的整合

```
完成条件: 玩家经历完整的叙事五拍并抵达⑤TRANSFORM
    ① ENCOUNTER: 天使告诉心爱的"我是第13个"
    ② STRUGGLE: EXIST_DENY + NIHILISM深度爆发
    ③ COMFORT: 天使不再"拉回"——在暗流中站在心爱的身边
    ④ CHOICE:
        - "不"            → ENGAGE（直面拒绝）
        - "我知道"        → ENGAGE（直面接受）
        - "那又怎样"      → ENGAGE（直面超越）
        注意: 同样没有ESCAPE——面对天使的真相，逃避不再可能
    ⑤ TRANSFORM: 心爱的崩溃→天使的独白→"我永远在你身边"
    完成类型: 一律COMPLETED_FULL
```

### 7.5 Ch 16 最终选择的特殊处理

Ch 16（王冠/心音）是最终选择章，完全脱离质点进程的常规判定逻辑：

```
Ch 16 特殊处理:
    1. 暗流不出现——存在保护系统收到"不再需要保护"的信号
    2. 天使恢复最美状态——wing_brightness重置为1.0（叙事驱动，非系统恢复）
    3. 最终选择有三个选项，都是ENGAGE:
        ① "毁灭天使，完成代价" → 融合结局
        ② "拒绝毁灭，承受代价" → 守护结局
        ③ "理解真相——毁灭即转化" → 觉醒结局
    4. 三个结局都是"好的"——没有坏结局
    5. 完成类型: 一律COMPLETED_FULL
    6. 三个结局不受存在保护——天使不会覆盖玩家的最终选择
    7. 觉醒结局可能有额外解锁条件（如羁绊深度达到阈值）——但这不是"隐藏结局"，而是"更深层理解的结局"
```

**为什么最终选择不受存在保护**：概念文档7.4节明确："最终选择不受保护——Phase 3的三种结局都是'好的'"。存在保护确保玩家"不会陷入绝望"，但最终选择不是"绝望vs希望"的选择——是"三种理解爱的方式"的选择。保护在这里反而是对玩家自主性的不尊重。

### 7.6 暗流类型与章节映射

> 此处仅列出映射概要。暗流的详细定义（触发条件、强度分级、视觉表现、天使介入台词）见存在保护机制GDD。

| 章 | 质点 | 主暗流 | 复合暗流 | 基础强度范围 | Phase |
|----|------|--------|---------|-------------|-------|
| 1 | 王国 | EXIST_DENY | — | 1-3 | 1 |
| 2 | 幸福 | HOPE_ERASE | — | 1-3 | 1 |
| 3 | 基础 | PAIN_AMP | — | 1-3 | 1 |
| 4 | 自我 | SHAME_LOOP | — | 3-5 | 2 |
| 5 | 逻辑 | NIHILISM | — | 3-5 | 2 |
| 6 | 共情 | POSS_DENY | — | 4-6 | 2 |
| 7 | 超我 | RAGE_INC | — | 4-6 | 2 |
| 8 | 胜利 | HARM_GUIDE | — | 5-7 | 2 |
| 9 | 荣耀 | SHAME_LOOP | EXIST_DENY | 5-7 | 2 |
| 10 | 严厉 | PAIN_AMP | NIHILISM | 5-7 | 2 |
| 11 | 慈悲 | HOPE_ERASE | EXIST_DENY | 6-8 | 2 |
| 12 | 理智 | NIHILISM | POSS_DENY | 6-8 | 2 |
| 13 | 真我 | 全部8种轮番 | — | 5-8 (不达临界) | 2 |
| 14 | 智慧 | 全部8种同时 | — | 8-10 (峰值) | 3 |
| 15 | 美丽 | EXIST_DENY | NIHILISM | 8-10 (最深绝望) | 3 |
| 16 | 王冠 | 无 | — | 0 | 3 |

---

## 8. 可访问性与安全

### 8.1 进度不构成压力

| 设计决策 | 实现方式 | 理由 |
|---------|---------|------|
| 没有进度条/百分比 | 生命之树只显示点亮状态，不显示数字 | 数字会触发完成焦虑 |
| 没有时间限制 | 时间型卡住机制是"帮助"不是"催促"——天使说的是"慢慢来" | 疗愈体验不应有时间压力 |
| 没有分数/评级 | 完成类型（100%/50%）不显示为分数，只表现为光芒亮度差异 | 50%不是"差评"，是"另一种通过" |
| 没有比较 | 不存在"其他玩家的进度"或"平均完成时间" | 这不是竞争性体验 |
| 没有成就弹出 | 质点点亮时没有Steam成就式的弹窗 | 弹窗会打断情感沉浸 |

### 8.2 卡住时的温柔引导

| 层次 | 引导方式 | 语气 |
|------|---------|------|
| 选择型卡住（ESCAPE） | 天使渐进式回应：温柔接纳→共享脆弱→代为面对 | 从"没关系"到"让我来" |
| 时间型卡住（1次） | 天使轻声提示 | "你不需要现在就做决定" |
| 时间型卡住（2次） | 天使分享视角 | "面对[主题]很难。但我觉得你准备好了" |
| 时间型卡住（3次） | 天使温和建议+选项微光 | "也许你可以试试……" |
| 时间型卡住（4次+） | 不再升级，保持陪伴 | "我一直在这里" |

**关键原则**：任何引导都以天使的口吻呈现，不是系统提示。玩家不应意识到"系统在帮我"，而应感觉到"天使在关心我"。

### 8.3 不暴露"游戏化"痕迹

| 禁止 | 允许 |
|------|------|
| "进度: 3/16" | 生命之树上3个质点点亮 |
| "完成度: 100%" | 质点饱满发光 |
| "跳过此章节" | 不存在跳过功能 |
| "选择正确！" / "选择错误" | 天使对不同选择有不同回应，但不说"对/错" |
| "解锁成就：直面自我" | 不存在成就系统 |
| "ESC次数：2/3" | 天使说"我有时候也想逃避"（叙事性回应） |
| 经验值/等级 | 不存在 |

### 8.4 50%完成的安全处理

50%完成（COMPLETED_HALF）是本系统最需要谨慎处理的状态——它可能让玩家感到"我做错了"。

**安全措施**：
1. **视觉差异最小化**：50%亮度的光芒与100%的差异是"柔和vs饱满"，不是"暗vs亮"。50%的光芒仍然是温暖的、角色主题色的，不是灰色或失败的。
2. **叙事确认**：50%完成后的安息场景中，天使不会说"你本应该自己面对"，而是说"没关系，我们走"——确认这是有效的通过。
3. **不影响后续**：50%完成与100%完成一样解锁下一质点，一样推进叙事。不存在"50%积累过多导致坏结局"的机制。
4. **不累计惩罚**：每个质点的escape_count独立计算。一个质点的50%完成不会影响下一个质点的起始状态。
5. **可感知但不焦虑**：玩家可以注意到"这个质点没那么亮"，但不会被明确告知"你逃避了"。差异是隐性的，需要观察力才能发现。

### 8.5 与可访问性设置的对齐

| 可访问性设置 | 对质点进程系统的影响 |
|-------------|-------------------|
| 低刺激模式 | 生命之树呼吸光效减慢；质点点亮动画简化 |
| 屏幕抖动/闪光关闭 | 质点点亮时不使用闪光效果，改用渐变 |
| 文字大小调整 | 生命之树缩略图的文字（如有）随之调整 |
| 天使陪伴光效关闭 | 生命之树的光效不受影响（它是独立UI元素） |
| 内容警告与跳过 | 时间型卡住提示不含创伤性内容；选择菜单可在内容警告后呈现 |

### 8.6 情绪安全底线

质点进程系统本身是情绪安全的一部分——它确保：
1. **永远可以前进**：没有永久卡住的状态，天使会帮助突破
2. **永远没有失败**：没有FAILED状态，只有"完成了"和"还没完成"
3. **永远不被催促**：时间型卡住是"帮助"不是"催促"
4. **永远不被评判**：50%完成不是"差评"，是"另一种通过"
5. **最终选择永远自由**：Phase 3的最终选择不受任何系统约束

---

## 附录A：设计理论评审

### A.1 主导策略风险检查

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 是否存在"最优选择"路径 | ✅ 安全 | ENGAGE和ESCAPE都能完成质点，只是纹理不同。不存在"最优" |
| 是否存在"让天使代替"策略 | ⚠️ 注意 | 玩家可能故意选ESCAPE三次让天使代为面对。缓解：50%亮度的视觉差异传递"这不是完美的通过"；天使代为面对的叙事有情感重量（天使说"这一次，让我来"），不是轻松的"跳过" |
| 是否存在"刷选项"策略 | ✅ 安全 | NEUTRAL选项不增加escape_count，但天使的回应会逐渐推动玩家做出ENGAGE/ESCAPE选择 |
| 是否存在"速通"策略 | ✅ 安全 | 即使全选ENGAGE，每章仍需经历完整五拍叙事。质点系统不提供"跳过叙事"的途径 |

### A.2 认知过载检查

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 16质点结构是否对玩家造成认知负担 | ✅ 安全 | 玩家不需要理解"质点""八度"等术语。系统在后台运作，玩家只感知到"章节推进"和"生命之树点亮" |
| 五拍叙事结构是否对玩家造成认知负担 | ✅ 安全 | 五拍是叙事节奏，不是玩家需要记忆的规则。玩家自然地感受到"遇到问题→感到痛苦→天使安慰→做出选择→事情好转"的节奏 |
| confrontation_tag是否对玩家可见 | ✅ 安全 | 标签是系统内部数据，玩家不可见。玩家只感受到"这个选择让天使微笑"vs"这个选择让天使温柔地说'慢慢来'" |
| 50%完成的视觉差异是否引发焦虑 | ⚠️ 注意 | 需要在测试中验证。如果玩家普遍感到焦虑，考虑进一步弱化差异或增加天使的安抚台词 |

### A.3 支柱漂移检查

| 支柱 | 漂移风险 | 缓解措施 |
|------|---------|---------|
| 天使永不离去 | 低 | 天使在每个质点的③COMFORT和⑥REST中都有戏份。50%完成时天使"代为面对"更是天使深度参与的体现 |
| 痛苦可被转化 | 低 | 每个质点都有完整的"痛苦→安慰→转化"循环。50%完成也是一种转化——"不完美的通过也是通过" |
| 从解离走向整合 | 中 | Ch 13的身份选择机制需要确保前三个ESCAPE选项不会让玩家觉得"我在选错"。缓解：天使的渐进式引导明确传达"也许你不只是其中之一"，引导玩家走向整合 |

---

## 附录B：与美术方向的协调点

| 协调点 | 需求 | 状态 |
|--------|------|------|
| 生命之树16质点布局图 | 需要16质点的具体排列位置（双八度布局），供UI实现 | ⚠️ 待对齐 |
| 质点点亮动画 | 每个质点以角色主题色点亮的动画效果（100%和50%两种） | ⚠️ 待对齐 |
| 章节标题卡 | 16张标题卡，每张使用角色主题色+符号 | 美术圣经4.3节已定义方向 |
| 迷你生命之树缩略图 | 120×180px的常驻UI元素，需适配不同屏幕布局 | ⚠️ 待对齐 |
| 50%亮度的视觉表现 | 需要明确"50%饱和度的主题色"的具体色值和发光效果 | ⚠️ 待对齐 |

---

## 附录C：已知风险与缓解

| 风险 | 等级 | 缓解措施 |
|------|------|---------|
| 50%完成可能让玩家感到"做错了" | 中 | 视觉差异最小化；天使的叙事确认；不影响后续进程 |
| 时间型卡住可能打扰沉浸中的玩家 | 中 | 阈值设置较长（5-7分钟）；提示以天使口吻呈现；可考虑在设置中关闭 |
| Ch 13的身份选择可能让玩家困惑"为什么前三个是ESCAPE" | 中 | 天使的渐进式引导解释"也许你不只是其中之一"；叙事文本暗示三重身份的同时存在 |
| NEUTRAL选项的无限循环 | 低 | 天使的回应逐渐推动玩家做出ENGAGE/ESCAPE选择；第3次NEUTRAL后天使可能说"你准备好了，试试看？" |
| 大量质点定义数据（16×复杂结构）的维护成本 | 中 | 数据结构化存储为JSON；叙事设计者只需填写标签和文本，不需要理解系统逻辑 |
| 质点完成判定与叙事脚本的同步问题 | 中 | label命名规范强制五拍结构；系统通过label跳转追踪节拍，不依赖文本内容 |

---

**文档结束**

> 本文档为质点进程系统的完整设计规格。所有伪代码和数据结构可直接用于Ren'Py实现。
>
> 待对齐项：
> 1. 生命之树16质点布局图（与美术对齐）
> 2. 50%亮度的具体视觉规格（与美术对齐）
> 3. confrontation_tag字段与选择系统GDD的集成（与design-strategist对齐）
> 4. wing_brightness与天使陪伴系统GDD的集成（与design-strategist对齐）
> 5. 暗流触发/解除与存在保护机制GDD的集成（本GDD的姊妹文档）
