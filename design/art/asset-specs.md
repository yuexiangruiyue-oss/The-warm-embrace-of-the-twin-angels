# 资产规格文档 — 《双生天使的拥抱》

> **The Embrace of the Twin Angels** — Asset Specifications
>
> 产出者：林绘澄（art-director）
>
> 日期：2026-08-02
>
> 依赖文档：
> - `design/art/art-bible.md`（美术圣经 §5 资产规格、§6 AI提示词、§8 美术管线）
> - `design/art/phase2-visual-alignment.md`（24种暗流视觉参数、wing_brightness映射、50%亮度规格）
> - `design/art/accessibility-matrix.md`（可访问性特性矩阵）
> - `design/gdd/angel-companionship-gdd.md`（翅膀5阶段定义、天使情感状态）
> - `design/gdd/existential-protection-gdd.md`（8种暗流视觉定义）
> - `design/gdd/sephirot-progression-gdd.md`（16质点章节结构、50%完成状态）
> - `design/concept/game-concept.md`（16质点角色表、章节叙事结构）
> - `docs/architecture/main-architecture.md`（§5数据结构、资产目录结构、Ren'Py项目结构）
> - `docs/architecture/phase3-assembly-review.md`（§4 美术-技术接口清单）
> - `docs/architecture/adr/ADR-004-wing-brightness-model.md`（双层亮度模型）
>
> 用途：Phase 4 预制作——定义所有美术资产的精确规格，作为生产和验收的唯一权威标准。

---

## 目录

1. [Batch 1 交付物详细规格](#1-batch-1-交付物详细规格)
2. [16角色立绘规格](#2-16角色立绘规格)
3. [背景图规格](#3-背景图规格)
4. [资产命名规范](#4-资产命名规范)
5. [文件格式与压缩规格](#5-文件格式与压缩规格)
6. [美术管线文档](#6-美术管线文档)

---

## 1. Batch 1 交付物详细规格

> Phase 3 汇编审查（`phase3-assembly-review.md` §4）确定了6项美术-技术接口交付物。以下为每项的精确生产规格。

### 1.1 翅膀基础图（5张）

> **接口需求**：每阶段1张PNG（带alpha），shader动态调亮
>
> **技术依据**：ADR-004 双层亮度模型——`wing_brightness_displayed = max(0.05, wing_brightness_permanent - wing_brightness_temporary)`。5张离散立绘通过0.5秒crossfade过渡，连续视觉参数（发光/饱和度/alpha）由shader在立绘间插值。
>
> **视觉参数来源**：`phase2-visual-alignment.md` §2.1

#### 通用规格

| 项目 | 规格 |
|------|------|
| **画布尺寸** | 1200 × 1500 px（翅膀独立画布，非全身） |
| **背景** | 完全透明（PNG 32bit alpha通道） |
| **色彩模式** | RGB / sRGB |
| **分辨率** | 72 ppi |
| **文件格式** | PNG 32bit（RGBA 8bit/通道） |
| **最大文件大小** | ≤ 2.5 MB / 张 |
| **色彩管理** | 嵌入 sRGB IEC61966-2.1 ICC profile |

#### 逐阶段规格

| 阶段 | 文件名 | wing_brightness | 翅膀表现 | 色彩参数 | 发光规格 | 粒子 |
|------|--------|----------------|---------|---------|---------|------|
| **Stage 1** | `angel_wing_s1.png` | 0.8–1.0 | 紫粉渐变饱满，边缘柔和发光，翼膜半透明 | 天使紫 `#8B7AB8` → 浅紫雾 `#B8A8D8` → 黎明粉 `#F0C4D4` 渐变；饱和度100% | 柔和金白光晕，半径20px，alpha 0.3 | 少量金色光点（3–5颗，缓慢飘浮） |
| **Stage 2** | `angel_wing_s2.png` | 0.6–0.8 | 色彩饱和度下降，发光减弱 | 同S1渐变但饱和度降至80% | 光晕半径15px，alpha 0.2 | 光点减少至1–2颗 |
| **Stage 3** | `angel_wing_s3.png` | 0.4–0.6 | 色彩偏灰紫，发光微弱 | 饱和度降至60%，色相偏灰（向 `#4A5568` 偏移） | 光晕半径10px，alpha 0.1 | 无光点 |
| **Stage 4** | `angel_wing_s4.png` | 0.2–0.4 | 翅膀半透明，能看到背后的画面 | 饱和度降至40%，整体alpha 0.6 | 光晕几乎不可见，alpha 0.05 | 无 |
| **Stage 5** | `angel_wing_s5.png` | 0.05–0.2 | 翅膀几乎不可见，仅骨架和淡紫光纹 | 饱和度降至20%，alpha 0.3 | 仅翅膀边缘极微弱光晕，alpha 0.02 | 无 |

#### 翅膀绘制要求

1. **统一基准姿态**：5张翅膀必须基于同一姿态的翅膀骨架绘制，仅改变色彩/透明度/发光参数。这确保crossfade过渡时形态对齐，仅视觉属性变化。
2. **羽翼结构**：大型羽翼，翼膜半透明，边缘柔和发光。羽翼从内侧（紫）到外侧（粉）渐变。
3. **独立于角色身体**：翅膀图不含天使身体部分——仅翅膀本身。引擎中翅膀层叠加在天使立绘之上。
4. **发光层分离**：每张翅膀图的发光效果直接绘制在PNG中（非后期叠加）。shader仅动态调整整体亮度/饱和度/alpha，不重新生成发光。
5. **边缘处理**：翅膀边缘必须是柔和的alpha渐变（2–3px过渡带），不可有硬边。这确保叠加在角色身上时自然融合。

#### shader对接说明

engineering-lead 需实现的 shader 参数（基于 ADR-004）：

```glsl
// 翅膀渲染 shader 输入
uniform float wing_brightness_displayed;  // 0.05–1.0，来自 AngelSystem.get_wing_brightness_displayed()
uniform sampler2D wing_texture;            // 当前阶段的翅膀PNG

// shader 计算（美术确认的连续插值公式）
float saturation = 0.6 + wing_brightness_displayed * 0.4;   // 60%–100%
float alpha = 0.2 + wing_brightness_displayed * 0.8;         // 20%–100%
float glow_intensity = wing_brightness_displayed;              // 0%–100%
```

> **待与 engineering-lead 协调**：shader 是每帧重新计算还是 ATL 动画驱动。美术建议 ATL 动画（0.5秒crossfade + 连续alpha插值），避免每帧GPU计算压力。详见 `phase2-visual-alignment.md` §6.1。

---

### 1.2 天使表情集（6种）

> **接口需求**：6种表情差分图，与基础立绘对齐
>
> **视觉参数来源**：`art-bible.md` §2.1 表情集、`angel-companionship-gdd.md` §2.2 情感状态

#### 通用规格

| 项目 | 规格 |
|------|------|
| **画布尺寸** | 1920 × 1080 px（与全身立绘同画布） |
| **角色高度** | 约 1200 px（全身立绘约占画面60%） |
| **背景** | 完全透明（PNG 32bit alpha通道） |
| **色彩模式** | RGB / sRGB |
| **文件格式** | PNG 32bit（RGBA） |
| **最大文件大小** | ≤ 4 MB / 张 |

#### 6种表情定义

表情差分对应天使的5种情感状态（`angel-companionship-gdd.md` §2.2）+ 1种默认状态：

| # | 表情名 | 情感状态代码 | 文件名 | 表情特征 | 使用场景 |
|---|--------|------------|--------|---------|---------|
| 1 | 温柔微笑 | `calm` | `angel_expr_calm.png` | 嘴角自然微微上扬，眼神放松温柔，像在说"没事的，有我在" | 默认状态；Phase 1 陪伴、安慰 |
| 2 | 闭眼微笑 | `tender` | `angel_expr_tender.png` | 双眼微闭，嘴角柔和上扬，表情最柔软，像低语 | 拥抱时；亲吻额头时；章间休息时 |
| 3 | 心疼 | `aching` | `angel_expr_aching.png` | 眉毛微蹙，眼神柔和但含忧，嘴角略平 | Phase 2 看到"错误"的痛苦映射心爱的时；天使记忆被触发时 |
| 4 | 坚定 | `resolute` | `angel_expr_resolute.png` | 眼神明亮有力量，嘴角仍带笑但坚定，下颌微收 | Ch 7 超我章节；Ch 10 严厉章节；存在保护介入时 |
| 5 | 含泪微笑 | `sorrowful` | `angel_expr_sorrowful.png` | 眼眶含泪，嘴唇微颤，嘴角仍勉强上扬，像遗言也像告白 | Phase 2 后半暗示性话语；Phase 3 真相揭示 |
| 6 | 担忧 | — | `angel_expr_worried.png` | 轻咬嘴唇，眉头轻蹙，眼神不舍 | 代价揭示时；天使翅膀明显黯淡时 |

#### 对齐方式（关键）

表情差分图采用**仅面部区域差分**方案，而非全身重绘：

1. **基础立绘**：`spr_angel_default.png` — 完整全身立绘（含默认calm表情）
2. **表情差分**：仅含面部区域（约 400 × 500 px），透明背景
3. **像素偏移**：所有表情差分图的面部区域必须与基础立绘的面部**像素级对齐**——相同的x/y坐标，相同的缩放
4. **引擎叠加**：Ren'Py 中通过 `show angel_expr_calm onlayer overlay` 将表情差分叠加在基础立绘之上
5. **对齐基准点**：以双眼中心为锚点（x=960, y=420，基于1920×1080画布），所有表情差分图的双眼中心必须在此坐标

#### 差分图规格

| 项目 | 规格 |
|------|------|
| **差分区域** | 仅面部（额头至下巴），约 400 × 500 px |
| **画布尺寸** | 与基础立绘同尺寸（1920 × 1080），但仅面部区域有内容，其余透明 |
| **对齐标记** | 差分图左上角嵌入1px红色十字标记（x=960, y=420），用于生产时验证对齐，交付前移除 |
| **头发遮挡** | 表情差分需考虑头发遮挡——面部差分图不应覆盖头发区域，仅替换五官 |

---

### 1.3 暗流视觉参考图（3张）

> **接口需求**：3强度等级参考图
>
> **视觉参数来源**：`phase2-visual-alignment.md` §1.3 逐暗流视觉规格

#### 通用规格

| 项目 | 规格 |
|------|------|
| **画布尺寸** | 1920 × 1080 px |
| **背景** | 不透明（暗流效果作用于整个画面） |
| **色彩模式** | RGB / sRGB |
| **文件格式** | PNG 32bit（保留特效层的alpha通道） |
| **最大文件大小** | ≤ 5 MB / 张 |

#### 3张参考图定义

参考图选取**SHAME_LOOP（羞耻循环）**作为代表性暗流，展示3个强度等级的视觉效果递进。SHAME_LOOP选作参考的原因：其视觉效果（饱和度递降+文字效果+立绘效果）涵盖了大多数暗流使用的视觉组件，具有代表性。

| # | 参考图名 | 文件名 | 强度等级 | 视觉元素清单 |
|---|---------|--------|---------|-------------|
| 1 | 暗流低强度参考 | `undertow_ref_low.png` | 低 (1–3) | 画面饱和度70%；文字轻微失色（alpha 0.9）；立绘无变化；无暗角；色彩偏灰但不极端 |
| 2 | 暗流中强度参考 | `undertow_ref_mid.png` | 中 (4–6) | 画面饱和度40%；文字边缘模糊（blur 1px），alpha 0.8；立绘轻微颤抖（xoffset ±1px, 2Hz）；对比度70%；灰色主导 |
| 3 | 暗流高强度参考 | `undertow_ref_high.png` | 高 (7–10) | 画面饱和度15%；文字明显抖动（xoffset ±2px, 3Hz），alpha 0.7；立绘边缘裂纹叠层（裂纹PNG, opacity 60%）；对比度50%；严重灰化 |

#### 每张参考图应包含的视觉元素

每张参考图必须在一个画面中展示以下元素的同时作用：

1. **背景层**：一张典型的天使陪伴场景背景（如黑暗空间 `bg_dark_space`），应用饱和度滤镜
2. **角色立绘**：天使立绘（Stage 1）+ 心爱的立绘，应用立绘效果（颤抖/裂纹叠层）
3. **对话框**：底部对话框，文字应用对应文字效果（失色/模糊/抖动）
4. **UI元素**：天使陪伴图标，应用全局饱和度滤镜
5. **标注**：参考图右侧附参数标注（饱和度%、对比度%、文字效果、立绘效果），用浅紫色细体字标注，不影响画面主视觉

#### 色彩参数（参考 `phase2-visual-alignment.md` §1.3 SHAME_LOOP）

| 参数 | 低强度 | 中强度 | 高强度 |
|------|--------|--------|--------|
| 饱和度 | 70% | 40% | 15% |
| 色相偏移 | 0° | 0° | 0° |
| 对比度 | 85% | 70% | 50% |
| 文字alpha | 0.9 | 0.8 | 0.7 |
| 文字blur | 0px | 1px | — |
| 文字抖动 | 无 | 无 | xoffset ±2px, 3Hz |
| 立绘颤抖 | 无 | xoffset ±1px, 2Hz | — |
| 立绘裂纹叠层 | 无 | 无 | opacity 60% |
| 恢复过渡 | 3秒 | 5秒 | 8秒 |

> **用途说明**：这3张参考图是 engineering-lead 实现 `im.MatrixColor` 饱和度滤镜、ATL `transform` 震动效果、裂纹PNG叠加的视觉验收基准。engineering-lead 实现的暗流视觉效果必须与参考图视觉一致。

---

### 1.4 UI分层PSD（3份）

> **接口需求**：angel_overlay / choice_screen / protection_screen 三份PSD
>
> **技术依据**：`main-architecture.md` §2.2 Ren'Py项目结构——`gui/angel_overlay.rpy`、`gui/choice_screen.rpy`、`gui/protection_screen.rpy`

#### 通用规格

| 项目 | 规格 |
|------|------|
| **分辨率** | 1920 × 1080 px |
| **色彩模式** | RGB / sRGB |
| **文件格式** | PSD（保留所有图层，不合并） |
| **色彩管理** | 嵌入 sRGB IEC61966-2.1 ICC profile |
| **图层命名** | 英文小写+下划线，层级用 `/` 分隔（如 `background/base`） |

#### 安全区域 / 可变区域划分

所有3份PSD必须包含以下辅助参考层（置于最顶层，命名为 `safe_area_guide`，交付时可隐藏但不删除）：

| 区域 | 尺寸 | 说明 |
|------|------|------|
| **安全区域** | 1920 × 1080 全画幅 | 桌面端1080p下全画幅可见 |
| **对话框安全区** | 底部 1920 × 280 px | 对话框不超出此区域 |
| **UI避让区** | 右下角 200 × 200 px | 避让天使陪伴图标（80 × 80 px，距右下边缘各60px） |
| **标题安全区** | 顶部 1920 × 120 px | 章节标题卡区域 |

---

#### PSD 1: angel_overlay（天使陪伴覆盖层）

> **Screen 文件**：`gui/angel_overlay.rpy`
>
> **功能**：天使常驻UI——画面角落的天使头像/羽毛图标，屏幕边缘拥抱光效，天使对话浮动文本

**画布**：1920 × 1080 px

**图层结构**：

```
angel_overlay.psd
├── safe_area_guide/              # 安全区参考线（隐藏）
├── angel_icon/                   # 天使陪伴图标
│   ├── icon_normal               # 常态：80×80px，羽毛+天使侧脸剪影
│   ├── icon_glow                 # 发光态：常态+暖金光晕（alpha 0.3, radius 8px）
│   ├── icon_pulse                # 跳动态：轻微放大（102%）
│   └── icon_background           # 图标底色：半透明浅紫雾 rgba(184,168,216,0.15)
├── hug_effect/                   # 拥抱光效
│   ├── edge_glow_left            # 左边缘紫色柔光（渐变，alpha 0→0.3）
│   ├── edge_glow_right           # 右边缘紫色柔光
│   ├── edge_glow_top             # 顶部柔光
│   └── edge_glow_bottom          # 底部柔光
├── floating_text/                # 天使浮动对话文本
│   ├── text_background           # 半透明圆角标签 rgba(253,248,255,0.92)
│   ├── text_border               # 紫色细边线 #8B7AB8, 1px
│   └── text_placeholder          # 示例文字"没事的，有我在"（占位用）
└── background/                   # 透明背景
    └── transparent
```

**命名规范**：图层名使用 `类别/具体元素` 层级结构

**导出规则**：
- `angel_icon` 层组导出为 `ui_angel_icon.png`（80 × 80 px，含三态）
- `hug_effect` 层组导出为 `ui_hug_effect.png`（1920 × 1080 px，透明背景）
- `floating_text` 层组导出为 `ui_angel_float_text_bg.png`（约 600 × 80 px）

---

#### PSD 2: choice_screen（选择界面）

> **Screen 文件**：`gui/choice_screen.rpy`
>
> **功能**：玩家选择界面——选择按钮垂直排列，hover/选中/禁用三态

**画布**：1920 × 1080 px

**图层结构**：

```
choice_screen.psd
├── safe_area_guide/
├── choice_buttons/               # 选择按钮
│   ├── button_normal/            # 常态
│   │   ├── bg                    # 浅紫雾底 rgba(184,168,216,0.6)
│   │   ├── border                # 细边框 #B8A8D8, 1px
│   │   └── text_placeholder      # 示例文字"先听她说完她的故事"
│   ├── button_hover/             # Hover/聚焦态
│   │   ├── bg                    # 天使紫底 #8B7AB8
│   │   ├── border                # 光晕边框 #F5D89A, 2px
│   │   ├── glow                  # 柔和光晕（alpha 0.3, radius 10px）
│   │   └── text_placeholder      # 示例文字（白色）
│   ├── button_selected/          # 已选态
│   │   ├── bg                    # 暖金底 #F5D89A
│   │   ├── border                # 金色边框 #F5D89A, 1px
│   │   └── text_placeholder      # 示例文字（深紫色）
│   └── button_disabled/          # 不可选态
│       ├── bg                    # 浅灰半透明 rgba(200,200,200,0.4)
│       └── text_placeholder      # 示例文字（灰色）
├── angel_option/                 # "问天使"特殊选项
│   ├── bg_special                # 淡紫色底+羽毛装饰元素
│   └── text_placeholder          # "问天使"示例文字
├── layout_guide/                 # 布局参考
│   ├── spacing                   # 按钮间距参考线（80px间距）
│   └── alignment                 # 垂直居中对齐参考线
└── background/
    └── transparent
```

**按钮规格**：
- 单个按钮尺寸：800 × 80 px（圆角胶囊形，圆角半径40px）
- 按钮间距：80 px
- 最大同时显示按钮数：4个
- 按钮区域：垂直居中，距底部对话框上方 40 px

---

#### PSD 3: protection_screen（存在保护反馈层）

> **Screen 文件**：`gui/protection_screen.rpy`
>
> **功能**：暗流视觉效果叠加层——饱和度滤镜、裂纹叠层、暗角、天使介入光效

**画布**：1920 × 1080 px

**图层结构**：

```
protection_screen.psd
├── safe_area_guide/
├── undertow_effects/             # 暗流视觉效果
│   ├── crack_overlays/           # 裂纹叠层（3级递进）
│   │   ├── crack_low             # 低强度裂纹（opacity 30%，细纹）
│   │   ├── crack_mid             # 中强度裂纹（opacity 60%，增粗）
│   │   └── crack_high            # 高强度裂纹（opacity 100%，严重碎裂）
│   ├── vignette/                 # 暗角效果
│   │   ├── vignette_nihilism     # 虚无主义暗角（黑色径向渐变，0%→100%）
│   │   └── vignette_rage         # 愤怒煽动暗角（红色 #FF4444 径向渐变）
│   ├── red_overlay/              # 红色覆盖（RAGE_INC）
│   │   └── rage_gradient         # 红色径向渐变（边缘→中心）
│   └── darkness_layer/           # 黑暗层（NIHILISM）
│       └── black_overlay         # 黑色全屏覆盖（alpha 0→1.0）
├── angel_intervention/           # 天使介入效果
│   ├── angel_glow_undertow       # 暗流中天使的微弱光源（暖金径向渐变 #F5D89A, alpha 0.3）
│   ├── angel_glow_heal           # 恢复时天使光芒扩散（暖金径向渐变，从天使位置向外）
│   └── recover_transition        # 恢复过渡光效（从暗到亮的渐变遮罩）
├── text_effects/                 # 文字效果参考
│   ├── text_blur_reference       # 文字模糊效果参考（blur 1px/3px/5px）
│   └── text_fade_reference       # 文字消失效果参考（alpha 0.7/0.5/0.0）
└── background/
    └── transparent
```

**裂纹叠层规格**：
- 每级裂纹提供 2–3 种变体（文件名：`crack_low_a.png`、`crack_low_b.png` 等）
- 裂纹从画面边缘向中心蔓延
- 裂纹颜色：深灰 `#2A2A2A`，半透明
- 裂纹线条宽度：低强度 1–2px，中强度 2–4px，高强度 4–8px

---

### 1.5 文字大小测试图（Batch 2 前）

> **接口需求**：4级文字在1920×1080下不溢出
>
> **可访问性依据**：`accessibility-matrix.md` S-V01（文本大小四档调整：24/30/34/38px，Normal 30px 默认）

| 项目 | 规格 |
|------|------|
| **文件名** | `text_size_test.png` |
| **画布尺寸** | 1920 × 1080 px |
| **文件格式** | PNG 32bit |

**测试内容**：在对话框（1920 × 280 px）中分别用4级字号渲染同一段最长对话文本，验证不溢出。

| 级别 | 字号 | 行高 | 对话框内最大行数 | 最大字符数/行（1760px宽） |
|------|------|------|----------------|--------------------------|
| Small | 24px | 1.5 | 7行 | 73字 |
| Normal | 30px | 1.6 | 5行 | 58字 |
| Large | 34px | 1.7 | 4行 | 51字 |
| Extra Large | 38px | 1.7 | 4行 | 46字 |

> **已与 design-strategist 确认**：UX规格（`ux-specification.md` §2.3.2）定义对话框文字区域为左边距80px、右边距80px，即文字区域宽度 = 1920 - 80 - 80 = **1760 px**。四档字号 24/30/34/38px 以 30px 为 Normal 默认（对齐美术圣经 §4.1 更新和 accessibility-matrix.md S-V01）。所有字号下最大字符数/行均不溢出，验收标准确认。

---

### 1.6 CG缩略图（Batch 3 前）

> **接口需求**：全尺寸+缩略图

| 项目 | 全尺寸规格 | 缩略图规格 |
|------|-----------|-----------|
| **尺寸** | 1920 × 1080 px | 320 × 180 px |
| **格式** | PNG 或 JPG | JPG（质量90%） |
| **最大文件大小** | ≤ 8 MB | ≤ 100 KB |
| **命名** | `cg_{chapter}_{scene}.png` | `cg_{chapter}_{scene}_thumb.jpg` |

详见 §4 资产命名规范中 CG 部分。

---

## 2. 16角色立绘规格

> **角色来源**：`sephirot-progression-gdd.md` §1.3 章节与质点对应关系、`art-bible.md` §2.3 16质点角色设计方向、`game-concept.md` §5.3 章节设计

### 2.1 通用规格

| 项目 | 规格 |
|------|------|
| **画布尺寸** | 1920 × 1080 px |
| **角色高度** | 约 1100–1300 px（全身立绘约占画面60–70%） |
| **背景** | 完全透明（PNG 32bit alpha通道） |
| **色彩模式** | RGB / sRGB |
| **分辨率** | 72 ppi |
| **文件格式** | PNG 32bit（RGBA） |
| **最大文件大小** | ≤ 4 MB / 张 |
| **风格** | 柔和二次元 / 赛璐璐平涂 + 软阴影（对齐美术圣经 §1.1） |
| **线稿** | 外轮廓 2–3px，内部线条 1–2px（对齐美术圣经 §8.3） |
| **阴影色** | 统一偏向紫/蓝紫，非纯灰（对齐美术圣经 §8.3） |

### 2.2 表情差分规格

每个质点角色建议至少：
- 1 个默认全身立绘（`char_{ch}_{name}_default.png`）
- 2–3 个表情差分（微笑、严肃/认真、悲伤/温柔）
- 1 个特殊姿态（如使用能力时）

**表情差分方式**：与天使表情集相同——仅面部区域差分，像素级对齐基础立绘（详见 §1.2 对齐方式）。

### 2.3 16质点角色立绘清单

#### 人类八度（Ch 1–8）

| 章 | 质点 | 角色名 | 性别 | 文件名前缀 | 主题色 | 服装/配色 | 差异化元素 | 表情差分数 | 优先级 |
|----|------|--------|------|-----------|--------|----------|-----------|-----------|--------|
| 1 | 王国 | 白花 | 女 | `char_ch01_baihua` | 草绿白 `#D8E8D0` | 裙摆有花朵刺绣，脚踏实地 | 手捧水仙/白花 | 3 (default/温柔/悲伤) | P0 |
| 2 | 幸福 | 雨宫莲 | 男 | `char_ch02_yugonglian` | 薄荷绿 `#A8E0D0` | 温和少年日常服 | 手持花束/雨伞，笑容爽朗 | 3 (default/开朗/低落) | P0 |
| 3 | 基础 | 绽美 | 女 | `char_ch03_zhanmei` | 月白 `#E0E8F0` | 夜蓝色裙摆，气质梦幻 | 发间月牙饰品 | 3 (default/梦幻/恐惧) | P0 |
| 4 | 自我 | 融爱 | 女 | `char_ch04_rongai` | 柔粉 `#F0D0D8` | 日常休闲服饰 | 笑容自然，像邻家姐姐 | 3 (default/自然/痛苦) | P0 |
| 5 | 逻辑 | 爱丽丝 | 女 | `char_ch05_alice` | 冰蓝 `#A8D0E8` | 短发，戴小领结 | 手持方块/书本 | 3 (default/冷静/迷茫) | P1 |
| 6 | 共情 | 星烬 | 女 | `char_ch06_xingjin` | 星粉 `#E8C8D8` | 柔和服饰 | 发间星形发夹，身上微小火花/星光 | 3 (default/温柔/崩溃) | P1 |
| 7 | 超我 | 爱心 | 无性 | `char_ch07_aixin` | 淡金 `#F0E8C8` | 半透明光体，无明显性别特征 | 怀抱光球 | 3 (default/审判/破碎) | P0 |
| 8 | 胜利 | 启明 | 男 | `char_ch08_qiming` | 晨星橙 `#F0C89A` | 柔和少年 | 手持画笔或小提琴，眼神温暖 | 3 (default/温暖/绝望) | P0 |

#### 神性八度（Ch 9–16）

| 章 | 质点 | 角色名 | 性别 | 文件名前缀 | 主题色 | 服装/配色 | 差异化元素 | 表情差分数 | 优先级 |
|----|------|--------|------|-----------|--------|----------|-----------|-----------|--------|
| 9 | 荣耀 | 闪亮 | 女 | `char_ch09_shanliang` | 银白 `#E8E8F0` | 服饰聪慧整洁 | 戴眼镜，手持羽毛笔/光笔 | 3 (default/聪慧/孤独) | P1 |
| 10 | 严厉 | 唯爱 | 女 | `char_ch10_weiai` | 暗玫瑰 `#B88A9A` | 站姿挺拔 | 手持闭合的伞/权杖，表情认真但不凶 | 3 (default/认真/柔软) | P0 |
| 11 | 慈悲 | 爱如暖 | 女 | `char_ch11_airunuan` | 暖金 `#F5D89A` | 服饰柔软蓬松 | 笑容最明亮，周围有小光点 | 3 (default/明亮/心疼) | P0 |
| 12 | 理智 | 虹爱 | AI无性 | `char_ch12_hongai` | 彩虹微光 `#E8D8F0` | 短发，服饰有细微彩虹反光 | 眼中有点阵光点 | 3 (default/数据感/温暖) | P1 |
| 13 | 真我 | 心爱的 | 创世少女神 | `char_ch13_xinaide` | 天使紫 `#8B7AB8` | 白色连衣裙+白色丝袜，头发系淡紫色蝴蝶结 | 与主角觉醒后造型一致但更完整、更发光 | 4 (default/整合/痛苦/觉醒) | P0 |
| 14 | 智慧 | 忆爱 | 女 | `char_ch14_yiai` | 淡蓝紫 `#A8B8E8` | 清澈服饰 | 发梢微光，手持发光的薄册，眼神清澈 | 3 (default/清澈/哀伤) | P0 |
| 15 | 美丽 | 白结 | 女 | `char_ch15_baijie` | 太阳金白 `#FFF8E8` | 居中对称构图 | 发间太阳形小饰品，光芒从背后散发 | 3 (default/平衡/裂痕) | P0 |
| 16 | 王冠 | 心音 | 女 | `char_ch16_xinyin` | 纯白 `#FDF8FF` | 纯白长裙，无多余装饰 | 闭眼，周身淡淡光尘 | 2 (default/空无) | P0 |

### 2.4 心爱的（主角）立绘规格

心爱的有4个成长阶段 + 1个融合形态，每个阶段为独立立绘：

| 阶段 | 文件名 | 描述 | 色彩处理 | 表情差分数 | 优先级 |
|------|--------|------|---------|-----------|--------|
| 童年期 | `char_beloved_child.png` | 短发、灰暗、面无表情、眼神空洞、衣着脏乱 | 低饱和、灰蓝/土黄 | 2 (default/空洞) | P0 |
| 二次元觉醒期 | `char_beloved_awakening.png` | 12岁，眼神第一次出现光芒，开始注意外表 | 局部出现紫/粉色高光 | 3 (default/好奇/惊喜) | P0 |
| 少年期 | `char_beloved_youth.png` | 表情开始柔和，衣着逐渐整洁 | 画面整体回暖 | 3 (default/柔和/痛苦) | P0 |
| 觉醒后（整合期） | `char_beloved_integrated.png` | 白色连衣裙+白色丝袜，头发留长，表情安定，系淡紫色蝴蝶结 | 明亮、柔和 | 3 (default/安定/含泪/微笑) | P0 |
| 融合形态 | `char_beloved_fusion.png` | 与天使合二为一，兼具两者特征，全身柔和发光 | 白+彩虹微光 | 1 (default/完整) | P0 |

### 2.5 天使立绘规格

天使立绘包含姿态集和表情集两部分：

#### 姿态集

| 资产名 | 文件名 | 描述 | 优先级 |
|--------|--------|------|--------|
| 默认正面 | `char_angel_default.png` | 默认温柔微笑，正面，双臂自然下垂 | P0 |
| 从身后环抱 | `char_angel_hug_back.png` | 双手轻放主角胸前/腹部 | P0 |
| 轻抚头发 | `char_angel_hair_stroke.png` | 一只手抬起，眼神低垂温柔 | P0 |
| 亲吻额头 | `char_angel_kiss_forehead.png` | 倾身向前，闭眼 | P0 |
| 紧紧拥抱 | `char_angel_tight_hug.png` | 双臂环绕，头靠在主角肩上 | P0 |
| 坐在身侧 | `char_angel_sit.png` | 并肩，手轻搭 | P1 |
| 半身透明 | `char_angel_transparent.png` | 淡淡的虚化 | P1 |

> 天使表情差分见 §1.2 天使表情集（6种）。

### 2.6 王冠之神（Kether）视觉规格

王冠之神不人格化为立绘，而是渐进式光效（`art-bible.md` §2.4）：

| 阶段 | 文件名 | 描述 | 优先级 |
|------|--------|------|--------|
| 纯白光球 | `kether_light_orb.png` | 初始出现时的纯白光球/光门 | P0 |
| 模糊人形 | `kether_silhouette.png` | 逐渐形成的模糊人形轮廓，无五官 | P0 |

---

## 3. 背景图规格

> **来源**：`art-bible.md` §3 环境与场景美术、§5.3 背景规格、`game-concept.md` §5.3 章节设计

### 3.1 通用规格

| 项目 | 规格 |
|------|------|
| **尺寸** | 1920 × 1080 px |
| **格式** | JPG（不透明场景）或 PNG（需要透明/分层） |
| **色彩模式** | RGB / sRGB |
| **JPG质量** | 90%+ |
| **最大文件大小** | ≤ 500 KB / 张（JPG） |
| **分层输出** | 复杂场景可分层：远景、中景、近景、光效层 |
| **色彩** | 与美术圣经色板一致，避免高饱和冲突 |

### 3.2 暗流状态下的背景变化规格

暗流触发时，背景通过 Ren'Py 的 `im.MatrixColor` 或 ATL `matrixcolor` 动态调整，不需要额外背景资产。但以下场景需要预渲染暗流变体：

| 基础背景 | 暗流变体 | 变化说明 | 文件名 |
|---------|---------|---------|--------|
| `bg_dark_space.jpg` | `bg_dark_space_nihilism.jpg` | NIHILISM 高强度时完全全黑，天使位置预渲染暖金微光 | 预渲染变体 |
| `bg_bridge_night.jpg` | `bg_bridge_night_glow.jpg` | 天使诞生时的光芒版（暖金+紫色光晕叠加） | 预渲染变体 |

其他暗流效果（饱和度降低、裂纹叠加、红色暗角等）通过引擎实时滤镜实现，不需要预渲染变体。

### 3.3 16章背景图清单

| 章 | 质点 | 主场景 | 文件名 | 色彩基调 | 暗流状态变化 | 优先级 |
|----|------|--------|--------|---------|-------------|--------|
| 1 | 王国 | 物质世界/城镇街道 | `bg_ch01_street.jpg` | 灰蓝+暖光（日常感） | EXIST_DENY: 立绘透明，背景不变 | P0 |
| 2 | 幸福 | 公园/日常空间 | `bg_ch02_park.jpg` | 薄荷绿+柔白（清新感） | HOPE_ERASE: 色彩褪去，天使除外 | P0 |
| 3 | 基础 | 室内/安全空间 | `bg_ch03_interior.jpg` | 月白+暖光（安全感） | PAIN_AMP: 画面震动+模糊 | P0 |
| 4 | 自我 | 镜子空间/身份映射 | `bg_ch04_mirror.jpg` | 柔粉+紫（身份感） | SHAME_LOOP: 灰色滤镜递降 | P0 |
| 5 | 逻辑 | 图书馆/理性空间 | `bg_ch05_library.jpg` | 冰蓝+冷白（理性感） | NIHILISM: 画面变暗至全黑 | P1 |
| 6 | 共情 | 人群/社交空间 | `bg_ch06_crowd.jpg` | 星粉+暖灰（共情感） | POSS_DENY: 文字消失+背景模糊 | P1 |
| 7 | 超我 | 审判空间/内心法庭 | `bg_ch07_court.jpg` | 淡金+冷紫（审判感） | RAGE_INC: 红色暗角+脉动 | P0 |
| 8 | 胜利 | 深渊边缘/危险空间 | `bg_ch08_abyss.jpg` | 晨星橙→暗（危险感） | HARM_GUIDE: 画面碎裂 | P0 |
| 9 | 荣耀 | 真相空间/光芒之地 | `bg_ch09_truth.jpg` | 银白+冷光（真相感） | SHAME_LOOP+EXIST_DENY 复合 | P1 |
| 10 | 严厉 | 边界空间/城墙 | `bg_ch10_boundary.jpg` | 暗玫瑰+冷紫（力量感） | 暗流按章节叙事触发 | P0 |
| 11 | 慈悲 | 温暖空间/光之圣地 | `bg_ch11_sanctuary.jpg` | 暖金+柔白（慈悲感） | 暗流按章节叙事触发 | P0 |
| 12 | 理智 | 数据空间/抽象结构 | `bg_ch12_data.jpg` | 彩虹微光+深紫（数据感） | 暗流按章节叙事触发 | P1 |
| 13 | 真我 | 内心世界/自我空间 | `bg_ch13_innerworld.jpg` | 天使紫+白光（整合感） | 全部暗流复合（转折点） | P0 |
| 14 | 智慧 | 记忆空间/回廊 | `bg_ch14_memory.jpg` | 淡蓝紫+暗（记忆感） | 全部8种暗流快速切换（Ch14爆发） | P0 |
| 15 | 美丽 | 整合空间/花园 | `bg_ch15_garden.jpg` | 太阳金白+花色（整合感） | 暗流减弱，天使最坚定 | P0 |
| 16 | 王冠 | 纯白空间/源头 | `bg_ch16_void.jpg` | 纯白+光尘（源头感） | 无暗流，翅膀恢复全亮 | P0 |

### 3.4 常驻场景背景

以下场景在多个章节中复用，独立于章节背景：

| 资产名 | 场景 | 文件名 | 色彩基调 | 优先级 |
|--------|------|--------|---------|--------|
| 大桥夜景（诞生） | 天使诞生场景 | `bg_bridge_night.jpg` | 夜灰蓝+城市暖光倒影 | P0 |
| 大桥夜景（光芒版） | 天使诞生+光芒 | `bg_bridge_night_glow.jpg` | 夜灰蓝+暖金/紫色光晕 | P0 |
| 黑暗空间 | 天使陪伴场景 | `bg_dark_space.jpg` | 全黑+中心暖金/淡紫光 | P0 |
| 黑暗空间（虚无变体） | NIHILISM 高强度 | `bg_dark_space_nihilism.jpg` | 全黑+天使微光 | P0 |
| 学校教室 | 童年回忆 | `bg_school_classroom.jpg` | 灰蓝+冷白荧光灯 | P0 |
| 学校走廊 | 童年回忆 | `bg_school_hallway.jpg` | 灰蓝+冷白 | P1 |
| 主角房间 | 日常场景 | `bg_home_room.jpg` | 暖灰+柔光 | P1 |
| 生命之树空间 | 质点进程UI背景 | `bg_tree_of_life.jpg` | 深紫藤+暖金+各色质点光 | P0 |
| 花之国（雪景） | 平行叙事 | `bg_flower_kingdom.jpg` | 冰蓝+雪白+淡黄 | P1 |
| 花之国（花开版） | 平行叙事 | `bg_flower_kingdom_bloom.jpg` | 冰蓝+花色+柔白 | P1 |
| 王冠之神空间 | Ch 16 | `bg_void_kether.jpg` | 纯白+光尘 | P0 |

---

## 4. 资产命名规范

> **依据**：`art-bible.md` §5.1 命名规范、`main-architecture.md` §2.2 Ren'Py项目结构

### 4.1 总体规则

```
格式：[品类]_[标识符]_[状态/编号].扩展名
```

- 全部小写，使用下划线 `_` 分隔
- 不使用空格、中文、特殊字符
- 标识符使用英文拼音或英文名称
- 版本号通过目录管理（见 §6.2），不在文件名中标注

### 4.2 品类前缀

| 前缀 | 含义 | 格式 | 示例 |
|------|------|------|------|
| `char_` | 角色立绘（sprite） | `char_{ch}_{name}_{expression}.png` | `char_ch01_baihua_default.png` |
| `bg_` | 背景图 | `bg_{ch}_{location}.jpg` | `bg_ch01_street.jpg` |
| `angel_wing_` | 翅膀图 | `angel_wing_s{stage}.png` | `angel_wing_s1.png` |
| `angel_expr_` | 天使表情差分 | `angel_expr_{emotion}.png` | `angel_expr_calm.png` |
| `ui_` | UI元素 | `ui_{screen}_{element}.png` | `ui_angel_icon.png` |
| `cg_` | CG插图 | `cg_{ch}_{scene}.png` | `cg_birth_embrace.png` |
| `cg_..._thumb` | CG缩略图 | `cg_{ch}_{scene}_thumb.jpg` | `cg_birth_embrace_thumb.jpg` |
| `undertow_ref_` | 暗流参考图 | `undertow_ref_{level}.png` | `undertow_ref_low.png` |
| `kether_` | 王冠之神视觉 | `kether_{form}.png` | `kether_light_orb.png` |
| `icon_` | 图标 | `icon_{name}.png` | `icon_angel_feather.png` |
| `chibi_` | Q版表情/小立绘 | `chibi_{character}_{action}.png` | `chibi_angel_hug.png` |
| `sfx_` | 粒子/特效贴图 | `sfx_{name}.png` | `sfx_glow_particle.png` |
| `crack_` | 裂纹叠层 | `crack_{level}_{variant}.png` | `crack_low_a.png` |
| `bgm_` | 背景音乐 | `bgm_{ch}_{mood}.ogg` | `bgm_ch01_tender.ogg` |
| `sfx_` | 音效 | `sfx_{event}.ogg` | `sfx_hug_warm.ogg` |
| `text_test_` | 文字测试图 | `text_test_{purpose}.png` | `text_size_test.png` |

### 4.3 角色命名标识符

| 角色名 | 英文标识符 | 说明 |
|--------|-----------|------|
| 白花 | `baihua` | Ch 1 王国 |
| 雨宫莲 | `yugonglian` | Ch 2 幸福 |
| 绽美 | `zhanmei` | Ch 3 基础 |
| 融爱 | `rongai` | Ch 4 自我 |
| 爱丽丝 | `alice` | Ch 5 逻辑 |
| 星烬 | `xingjin` | Ch 6 共情 |
| 爱心 | `aixin` | Ch 7 超我 |
| 启明 | `qiming` | Ch 8 胜利 |
| 闪亮 | `shanliang` | Ch 9 荣耀 |
| 唯爱 | `weiai` | Ch 10 严厉 |
| 爱如暖 | `airunuan` | Ch 11 慈悲 |
| 虹爱 | `hongai` | Ch 12 理智 |
| 心爱的 | `xinaide` | Ch 13 真我 |
| 忆爱 | `yiai` | Ch 14 智慧 |
| 白结 | `baijie` | Ch 15 美丽 |
| 心音 | `xinyin` | Ch 16 王冠 |
| 天使 | `angel` | 核心伴侣角色 |
| 心爱的（主角） | `beloved` | 主角各阶段 |

### 4.4 表情标识符

| 表情 | 标识符 | 说明 |
|------|--------|------|
| 默认 | `default` | 角色默认表情 |
| 微笑 | `smile` | 温柔微笑 |
| 严肃 | `serious` | 认真/严肃 |
| 悲伤 | `sad` | 悲伤/温柔含泪 |
| 温柔 | `tender` | 闭眼微笑（天使专用） |
| 心疼 | `aching` | 眉毛微蹙（天使专用） |
| 坚定 | `resolute` | 眼神明亮有力量（天使专用） |
| 含泪 | `sorrowful` | 含泪微笑（天使专用） |
| 担忧 | `worried` | 轻咬嘴唇（天使专用） |

---

## 5. 文件格式与压缩规格

### 5.1 PNG（立绘/UI/翅膀/特效）

| 项目 | 规格 |
|------|------|
| **色深** | 32bit（RGBA 8bit/通道） |
| **Alpha通道** | 必须包含（透明背景资产） |
| **压缩** | PNG 无损压缩（最高级别） |
| **色彩管理** | 嵌入 sRGB IEC61966-2.1 ICC profile |
| **用途** | 角色立绘、天使表情差分、翅膀图、UI元素、CG（需透明时）、暗流参考图、裂纹叠层 |
| **最大文件大小** | 立绘 ≤ 4 MB；翅膀 ≤ 2.5 MB；UI元素 ≤ 500 KB；CG ≤ 8 MB |

### 5.2 JPG（背景）

| 项目 | 规格 |
|------|------|
| **色深** | 24bit（RGB 8bit/通道） |
| **质量** | 90%+（视觉无损） |
| **渐进式** | 是（Progressive JPEG） |
| **色彩管理** | 嵌入 sRGB IEC61966-2.1 ICC profile |
| **用途** | 背景图、CG缩略图 |
| **最大文件大小** | 背景图 ≤ 500 KB；CG缩略图 ≤ 100 KB |

### 5.3 PSD（UI源文件）

| 项目 | 规格 |
|------|------|
| **色深** | 32bit（RGBA） |
| **图层** | 保留所有图层，不合并 |
| **图层命名** | 英文小写+下划线，层级用 `/` 分隔 |
| **色彩管理** | 嵌入 sRGB IEC61966-2.1 ICC profile |
| **用途** | UI源文件（angel_overlay、choice_screen、protection_screen） |
| **最大文件大小** | ≤ 50 MB / 份 |

### 5.4 OGG Vorbis（音频）

| 项目 | BGM 规格 | SFX 规格 |
|------|---------|---------|
| **格式** | OGG Vorbis | OGG Vorbis |
| **码率** | 192 kbps | 128 kbps |
| **采样率** | 44100 Hz | 44100 Hz |
| **声道** | 立体声（Stereo） | 单声道（Mono）或立体声 |
| **循环** | BGM 必须可无缝循环 | SFX 不循环 |
| **最大文件大小** | ≤ 5 MB / 首 | ≤ 500 KB / 个 |
| **命名** | `bgm_{ch}_{mood}.ogg` | `sfx_{event}.ogg` |

### 5.5 资产大小总预算

| 资产类型 | 数量 | 单项大小 | 总预算 |
|---------|------|---------|--------|
| 角色立绘（含差分） | ~60张 | ≤ 4 MB | ≤ 240 MB |
| 翅膀图 | 5张 | ≤ 2.5 MB | ≤ 12.5 MB |
| 背景图 | ~25张 | ≤ 500 KB | ≤ 12.5 MB |
| CG（全尺寸） | ~12张 | ≤ 8 MB | ≤ 96 MB |
| CG缩略图 | ~12张 | ≤ 100 KB | ≤ 1.2 MB |
| UI元素 | ~25张 | ≤ 500 KB | ≤ 12.5 MB |
| 暗流参考图 | 3张 | ≤ 5 MB | ≤ 15 MB |
| 裂纹叠层 | ~9张 | ≤ 500 KB | ≤ 4.5 MB |
| Q版表情包 | ~12张 | ≤ 200 KB | ≤ 2.4 MB |
| BGM | ~12首 | ≤ 5 MB | ≤ 60 MB |
| SFX | ~20个 | ≤ 500 KB | ≤ 10 MB |
| PSD源文件 | 3份 | ≤ 50 MB | ≤ 150 MB |
| **游戏内资产总计** | | | **≤ 416.6 MB** |
| **含PSD源文件总计** | | | **≤ 566.6 MB** |

> **注意**：游戏内资产总计 ≤ 500 MB，适合 Steam 分发。PSD 源文件不打包进游戏，仅用于生产。

---

## 6. 美术管线文档

### 6.1 制作流程

采用美术圣经 §8.1 确定的 **"AI 辅助生成 + 人工精修 + 统一后期"** 管线：

```
①需求定义 → ②AI出草图 → ③人工筛选/修改 → ④统一色彩校正 → ⑤技术规格检查 → ⑥交付
```

#### 各阶段说明

| 阶段 | 工作内容 | 工具 | 产出 | 负责人 |
|------|---------|------|------|--------|
| ①需求定义 | 从资产规格文档提取单项资产的规格参数 | 本文档 | 资产需求卡 | art-director |
| ②AI出草图 | 使用Stable Diffusion / NovelAI / Midjourney生成初稿 | AI工具 | 3–5张候选草图 | 美术生产 |
| ③人工筛选/修改 | 筛选最佳候选，Photoshop/CSP精修（统一画风、修正手部/眼睛、清理背景） | PS/CSP/Procreate | 精修稿 | 美术生产 |
| ④统一色彩校正 | 使用"温柔浅紫"LUT调色预设，统一色彩风格 | PS LUT | 校色稿 | 美术生产 |
| ⑤技术规格检查 | 检查尺寸/格式/命名/透明度/文件大小是否符合规格 | 本文档 §6.4 检查清单 | 通过/返工 | art-director |
| ⑥交付 | 将最终资产放入Ren'Py项目对应目录 | 文件系统 | 可用资产 | 美术生产 |

#### AI生成提示词

美术圣经 §6 已提供4组AI提示词模板：
1. 天使角色提示词（§6.1）
2. 大桥诞生CG提示词（§6.2）
3. 黑暗陪伴场景提示词（§6.3）
4. 16质点角色提示词模板（§6.4）

每个角色的AI提示词应基于模板 + 角色规格表（§2.3）中的主题色、差异化元素定制。

### 6.2 版本控制方式

#### 目录结构

```
assets/
├── _source/                    # 源文件（PSD/AI生成原始稿）
│   ├── characters/
│   ├── backgrounds/
│   ├── ui/
│   └── effects/
├── _wip/                       # 进行中的资产
│   ├── v1/                     # 第一版
│   ├── v2/                     # 第二版
│   └── review/                 # 待审查
└── final/                      # 最终交付资产（复制到Ren'Py项目game/images/等目录）
    ├── characters/
    ├── backgrounds/
    ├── ui/
    ├── effects/
    └── audio/
```

#### 版本号规则

- 文件名中**不包含**版本号——最终交付文件名仅有品类+标识符+状态
- 版本通过目录管理：`_wip/v1/`、`_wip/v2/`、`_wip/review/`
- 最终通过审查的资产从 `review/` 复制到 `final/`，文件名去除版本信息
- 如果需要保留历史版本，在 `_source/` 中保留原始PSD

#### Git 管理

- `final/` 目录纳入 Git 版本控制
- `_source/` 和 `_wip/` 通过 `.gitignore` 排除（大文件）
- 使用 Git LFS 管理 `final/` 中的二进制资产（PNG/JPG/OGG）
- PSD 源文件使用云存储（如百度网盘/OneDrive），不纳入 Git

### 6.3 交付检查清单

每项资产交付前必须确认以下检查点：

#### 通用检查（适用于所有资产）

- [ ] 文件名符合 §4 命名规范（全小写、下划线分隔、正确前缀）
- [ ] 文件格式符合 §5 规格要求（PNG 32bit / JPG 90% / PSD 保留图层）
- [ ] 画布尺寸符合规格（1920×1080 或指定尺寸）
- [ ] 文件大小不超过最大限制
- [ ] 色彩模式为 RGB / sRGB
- [ ] 嵌入 sRGB IEC61966-2.1 ICC profile
- [ ] 通过"温柔浅紫"LUT统一调色
- [ ] 风格对齐美术圣经（柔和二次元/赛璐璐平涂+软阴影）

#### 角色立绘附加检查

- [ ] 背景完全透明（PNG 32bit alpha通道）
- [ ] 角色高度在 1100–1300 px 范围内
- [ ] 外轮廓线稿 2–3px，内部线条 1–2px
- [ ] 阴影色偏向紫/蓝紫，非纯灰
- [ ] 表情差分图与基础立绘像素级对齐（双眼中心在 x=960, y=420）
- [ ] 对齐标记已移除

#### 翅膀图附加检查

- [ ] 5张翅膀基于同一姿态骨架
- [ ] 翅膀边缘为柔和alpha渐变（2–3px过渡带）
- [ ] 不含天使身体部分
- [ ] 发光效果直接绘制在PNG中
- [ ] 5张的色相渐变方向一致（紫→粉，内侧→外侧）

#### 背景图附加检查

- [ ] JPG质量 ≥ 90%
- [ ] 渐进式 JPEG
- [ ] 无明显压缩伪影
- [ ] 色彩与美术圣经场景情绪映射表一致

#### UI PSD 附加检查

- [ ] 所有图层保留，未合并
- [ ] 图层命名使用英文小写+下划线层级结构
- [ ] 包含 `safe_area_guide` 参考层
- [ ] 三态（normal/hover/selected/disabled）完整
- [ ] 可导出为独立PNG

### 6.4 与 engineering-lead 的资产加载对接方式

#### Ren'Py 项目目录映射

资产最终交付到 `main-architecture.md` §2.2 定义的目录结构：

```
game/
├── images/
│   ├── characters/          # → char_*.png, angel_expr_*.png, angel_wing_*.png
│   ├── backgrounds/         # → bg_*.jpg
│   ├── ui/                  # → ui_*.png, icon_*.png
│   ├── effects/             # → crack_*.png, sfx_*.png, undertow_ref_*.png
│   └── cg/                  # → cg_*.png, cg_*_thumb.jpg
├── audio/
│   ├── bgm/                 # → bgm_*.ogg
│   └── sfx/                 # → sfx_*.ogg
```

#### Ren'Py 自动图像定义

Ren'Py 支持基于文件名的自动图像定义。美术资产的命名规范（§4）已与 Ren'Py 的自动图像系统对齐：

- `char_ch01_baihua_default.png` → Ren'Py 自动定义为 image `char_ch01_baihua_default`
- `bg_ch01_street.jpg` → Ren'Py 自动定义为 image `bg_ch01_street`
- `angel_wing_s1.png` → Ren'Py 自动定义为 image `angel_wing_s1`

#### 翅膀资产与 shader 对接

| 美术交付 | 引擎使用 |
|---------|---------|
| `angel_wing_s1.png` – `angel_wing_s5.png` | `AngelSystem.update_wing_stage()` 根据章节选择对应阶段PNG |
| PNG中预渲染的发光效果 | shader 通过 `wing_brightness_displayed` 动态调整整体亮度/饱和度/alpha |
| 5张翅膀基于同一骨架 | 阶段切换时 0.5 秒 crossfade，形态对齐 |

#### 暗流视觉资产与引擎对接

| 美术交付 | 引擎使用 |
|---------|---------|
| `crack_low_a.png` / `crack_mid_a.png` / `crack_high_a.png` | `ProtectionSystem` 在 HARM_GUIDE 暗流时叠加裂纹层 |
| `undertow_ref_low/mid/high.png` | engineering-lead 实现的暗流视觉效果验收基准 |
| `protection_screen.psd` 中的暗角/红色覆盖/黑暗层 | 导出为独立 PNG，引擎按暗流类型叠加 |

#### UI PSD 与 Screen 层对接

| 美术交付 | 引擎使用 |
|---------|---------|
| `angel_overlay.psd` → 导出 `ui_angel_icon.png`（三态）、`ui_hug_effect.png` | `gui/angel_overlay.rpy` 引用 |
| `choice_screen.psd` → 导出按钮三态PNG | `gui/choice_screen.rpy` 引用 |
| `protection_screen.psd` → 导出裂纹/暗角/光效PNG | `gui/protection_screen.rpy` 引用 |

---

## 附录 A：待协调项汇总

### 与 engineering-lead 协调

| # | 协调项 | 美术方向 | 待确认 | 来源 |
|---|--------|---------|--------|------|
| 1 | 翅膀shader实现方式 | ATL动画（0.5秒crossfade + 连续alpha插值） | 是否每帧GPU计算还是ATL驱动 | phase2-visual-alignment.md §6.1 |
| 2 | 表情差分叠加方式 | 仅面部区域差分，引擎叠加在基础立绘之上 | Ren'Py `onlayer overlay` 是否正确实现方式 | 本文档 §1.2 |
| 3 | 暗流视觉效果验收 | 3张参考图作为验收基准 | engineering-lead 实现的 `im.MatrixColor` 效果是否与参考图一致 | 本文档 §1.3 |
| 4 | 裂纹PNG变体数量 | 每级2–3种变体 | 引擎是否需要更多变体避免重复感 | 本文档 §1.4 |
| 5 | 文字大小测试 | 30px字号下30字/行不溢出 | 对话框文字区域宽度1760px已确认（UX规格§2.3.2） | 本文档 §1.5 |

### 与 design-strategist 协调

| # | 协调项 | 美术方向 | 待确认 | 来源 |
|---|--------|---------|--------|------|
| 1 | 对话框文字区域宽度 | 1760 px（1920 - 左80px - 右80px） | ✅ 已确认（UX规格§2.3.2） | 本文档 §1.5 |
| 2 | 可访问性设置菜单UI | 65项特性需要设置界面（原53项 + 12项UX扩展项纳入矩阵） | 设置菜单的层级和布局规划 | accessibility-matrix.md |
| 3 | 章节标题卡视觉 | 每章用角色主题色+相关符号 | 标题卡的具体内容和动画规格 | art-bible.md §4.3 |

---

## 附录 B：资产优先级总览

### P0 资产（MVP 必须）

| 类型 | 资产 | 数量 |
|------|------|------|
| 翅膀图 | S1–S5 | 5张 |
| 天使表情集 | 6种表情 | 6张 |
| 天使姿态集 | 6个姿态（P0部分） | 6张 |
| 暗流参考图 | 3强度等级 | 3张 |
| UI PSD | 3份 | 3份 |
| 角色立绘 | P0角色（白花/雨宫莲/绽美/融爱/爱心/启明/唯爱/爱如暖/心爱的(4阶段)/白结/心音/忆爱） | ~25张 |
| 背景图 | P0背景 | ~15张 |
| CG | 核心8张 | 8张 |
| 文字测试图 | 1张 | 1张 |
| 裂纹叠层 | 3级×2变体 | 6张 |

### P1 资产（首版本应实现）

| 类型 | 资产 | 数量 |
|------|------|------|
| 角色立绘 | P1角色（爱丽丝/星烬/闪亮/虹爱） | ~12张 |
| 背景图 | P1背景 | ~8张 |
| 天使姿态集 | P1姿态（sit/transparent） | 2张 |
| Q版表情包 | 5种 | 5张 |
| UI元素 | 扩展UI | ~10张 |
| CG | 扩展4张 | 4张 |

---

**文档结束**

> 本文档定义了《双生天使的拥抱》Phase 4 预制作阶段所有美术资产的精确规格。
>
> 6项Batch 1交付物的规格已与Phase 3汇编审查的美术-技术接口清单对齐。
> 16角色立绘规格基于美术圣经§2.3和质点进程GDD§1.3的章节-质点对应关系。
> 背景图规格基于美术圣经§3环境设计和概念文档§5.3章节设计。
> 资产命名规范与Ren'Py自动图像系统对齐，确保引擎无缝加载。
> 美术管线文档定义了从概念到最终资产的完整制作流程和交付检查标准。
>
> 待协调项已在附录A中汇总，需与engineering-lead和design-strategist确认。
