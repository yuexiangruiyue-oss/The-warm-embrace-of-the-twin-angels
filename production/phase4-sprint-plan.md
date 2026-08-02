# Phase 4 预制作 — 汇编与首个冲刺计划

> **汇编者**：游承峰（主理人）
>
> **范围**：3位成员并行产出的7份文档，共6232行
>
> **日期**：2026-08-02
>
> **判定**：✅ **PASS** — 全部交付物就绪，可进入 Batch 0 开发

---

## 一、Phase 4 产出总览

| 成员 | 文档 | 行数 |
|------|------|------|
| design-strategist | `design/ux/ux-specification.md` | 1736 |
| art-director | `design/art/asset-specs.md` | 943 |
| engineering-lead | `production/epics/epic-breakdown.md` | 1007 |
| engineering-lead | `tests/test-framework.md` | 1232 |
| engineering-lead | `production/batch0-skeleton.md` | 1118 |
| engineering-lead | `production/dev-workflow.md` | 465 |
| **合计** | **6份文档** | **6501行** |

### 跨成员协调结果

art-director 与 design-strategist 完成了5处文档更新和ID对齐：
- 对话框双背景系统（深紫藤默认 + 浅紫雾低刺激）已统一
- C-E05（恢复确认按钮）已取消，特性总数 54→53
- WCAG AA对比度验证通过
- UX规格ID全面对齐矩阵B-/S-/C-体系

---

## 二、主理人决策

### 决策1：字号分档 — 采用 24/30/34/38px

design-strategist 建议 24/27/30/34px，art-director 建议 24/30/34/38px。

**判定：采用 art-director 方案（24/30/34/38px）**

理由：可访问性优先原则。更大的字号范围惠及视力受损玩家，且38px在1920×1080画布、1760px文字宽度下30字/行不溢出（已验证）。design-strategist 的27px档位与30px差异过小，用户体验区分度不足。

### 决策2：GDD回写 — 进入Batch 0前完成

C2/C3/C4/C5四份GDD需与架构文档对齐：
- C2（天使陪伴）：翅膀亮度改为ADR-004双层模型
- C3（选择系统）：选项数据结构新增confrontation_tag和bond_depth_delta
- C4（质点进程）：确认confrontation_tag消费逻辑
- C5（存在保护）：翅膀亮度改为ADR-004双层模型

**执行方式**：由 design-strategist 在Batch 0期间同步完成，不阻塞开发启动。

### 决策3：Ren'Py版本 — 钉定8.3.x

**判定：Ren'Py 8.3.x（最新稳定版）**

由 engineering-lead 在Batch 0启动前创建 `docs/engine-reference/renpy/VERSION.md`。

---

## 三、首个冲刺计划：Batch 0

### 目标

**Ch1骨架章节可从开始到结束完整走通，存档/读档恢复正确。**

### Batch 0范围（16个Story，~36人日）

| Epic | Story | 标题 | 复杂度 | 人日 |
|------|-------|------|--------|------|
| E0 | S0.1 | 项目初始化与Git配置 | M | 2 |
| E0 | S0.2 | 目录结构与配置文件 | M | 2 |
| E0 | S0.3 | JSON数据层框架 | L | 4 |
| E0 | S0.4 | 数据校验工具 | M | 2 |
| E0 | S0.5 | CI流水线搭建 | M | 2 |
| E0 | S0.6 | 开发文档与README | S | 1 |
| E1 | S1.1 | 存档槽位系统 | L | 3 |
| E1 | S1.2 | 自动存档触发 | M | 2 |
| E1 | S1.3 | 存档数据序列化 | M | 2 |
| E1 | S1.4 | 读档状态恢复 | L | 3 |
| E1 | S1.5 | 存档UI实现 | M | 2 |
| E2 | S2.1 | 对话框与文本渲染 | L | 3 |
| E2 | S2.2 | 立绘显示与切换 | M | 2 |
| E2 | S2.3 | 背景图管理 | S | 1 |
| E2 | S2.4 | 跳过与自动模式 | M | 2 |
| E2 | S2.5 | Ch1五拍叙事骨架 | XL | 3 |

### Batch 0前置条件

| # | 事项 | 负责人 | 状态 |
|---|------|--------|------|
| 1 | GitHub仓库创建 | 用户 | 待审批 |
| 2 | Ren'Py版本钉定 | engineering-lead | 待执行 |
| 3 | 美术占位图（angel_placeholder.png + beloved_placeholder.png） | art-director | 待执行 |
| 4 | GDD回写（C2/C3/C4/C5） | design-strategist | Batch 0期间同步 |

### Batch 0 Exit标准

- [ ] Ch1从开始到结束可完整走通
- [ ] 五拍叙事结构（ENCOUNTER→STRUGGLE→COMFORT→CHOICE→TRANSFORM）可体验
- [ ] 存档/读档功能正常，状态恢复正确
- [ ] 跳过/自动模式工作正常
- [ ] CI流水线通过（lint + 数据校验 + 单元测试）
- [ ] 23个阻塞性测试用例中T21-T23通过

---

## 四、完整开发路线图

| Batch | 范围 | Story数 | 人日 | 交付物 |
|-------|------|---------|------|--------|
| **Batch 0** | 骨架+C1叙事+C6存档 | 16 | ~36 | Ch1可运行原型 |
| **Batch 1** | C3选择+C5存在保护+C2天使陪伴 | 16 | ~43 | Ch1-3完整体验（Phase 1遗忘期） |
| **Batch 2** | C4质点进程+集成+可访问性 | 9 | ~30 | Ch1-8完整体验（Phase 2前半） |
| **Batch 3** | 内容制作+UI/UX+打磨 | 13 | ~66 | 完整游戏（Ch1-16） |
| **合计** | | **54** | **~175** | |

### 版本号方案

- v0.1.0 — Batch 0完成
- v0.2.0 — Batch 1完成
- v0.3.0 — Batch 2完成
- v1.0.0 — Batch 3完成（发布候选）

---

## 五、待用户审批项

### 必须审批（阻塞Batch 0启动）

1. **GitHub仓库创建**：需要用户创建仓库并配置分支保护规则
2. **Ren'Py版本确认**：确认钉定8.3.x

### 建议审批（不阻塞但推荐）

3. **GDD回写范围**：确认C2/C3/C4/C5四份GDD的回写范围
4. **美术占位图方案**：简易占位即可，还是需要一定质量的初始立绘
5. **字号分档决策**：确认采用24/30/34/38px

---

## 六、Phase 4质量门判定

### ✅ PASS

**通过项**：
1. UX规格完整覆盖8个部分，65项可访问性特性全部映射（含12项UX扩展项纳入矩阵）
2. 资产规格覆盖6项Batch 1交付物+16角色立绘+背景图+命名规范
3. Epic/Story拆分清晰，54个Story均有验收标准和依赖关系
4. 测试框架4层金字塔，23个阻塞性用例
5. Batch 0骨架35个初始文件，Exit标准20项
6. 开发工作流完整（Git/Commit/Review/DoD/版本号）
7. 跨成员协调完成，5处文档更新+ID对齐
8. WCAG AA对比度验证通过

**注意事项**：
- 字号分档差异已由主理人裁定
- GDD回写在Batch 0期间同步进行，不阻塞开发
- 翅膀着色方案性能待Batch 1期间验证

---

## 七、Phase 5衔接

Phase 5（制作）将按冲刺循环执行：
1. engineering-lead 实现就绪Story
2. quality-lead 产QA计划与烟雾测试
3. design-strategist 做设计评审与范围检查
4. 主理人收尾并回顾

首个冲刺（Sprint 1）= Batch 0的前8个Story（E0全部+E1前3个），预计2周。
