# Ren'Py Engine Version Reference

> **项目**：The Embrace of the Twin Angels
>
> **引擎**：Ren'Py 8.3.x
>
> **确认日期**：2026-08-02
>
> **确认人**：岳祥瑞（项目主理人）

---

## 版本钉定

**Ren'Py 8.3.x（最新稳定版）**

- 下载地址：https://www.renpy.org/latest.html
- 文档地址：https://www.renpy.org/doc/html/
- SDK 目录：`renpy-8.3.x-sdk/`

## 选择理由

参见 `docs/architecture/adr/ADR-001-engine-selection.md`

## 关键特性依赖

本项目依赖的 Ren'Py 8.3.x 关键特性：

| 特性 | 用途 | 文档参考 |
|------|------|---------|
| Screen Language | 14类屏幕UI实现 | main-architecture.md §3 |
| ATL (Animation and Transformation Language) | 翅膀渐变、暗流视觉、天使介入动画 | phase2-visual-alignment.md |
| im.MatrixColor / matrixcolor | 暗流饱和度/色相滤镜 | asset-specs.md §1 |
| Persistent variables | 跨周目状态（结局解锁、CG图鉴） | main-architecture.md §4 |
| Save/Load system | 6组件状态序列化 | main-architecture.md §4.5 |
| Self-voicing | 可访问性 C-A04 | accessibility-matrix.md |
| Layered images | 角色表情差分叠加 | asset-specs.md §2 |
| JSON data loading | 数据驱动叙事（ADR-002） | main-architecture.md §5 |

## 版本更新策略

- 开发期间钉定 8.3.x，不跨大版本升级
- 如遇 bug fix 小版本更新，经测试后可升级
- 发布前确认最终版本号
