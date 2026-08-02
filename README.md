# 《双生天使的拥抱》(The Embrace of the Twin Angels)

一款以**存在性保护**为核心机制的叙事驱动视觉小说。

## 项目概述

玩家与一位守护天使同行，穿越 16 个 Sephirot（质点）章节，在情感暗流的冲击下保护自己的存在感，最终走向融合、守护或觉醒三种结局。

- **引擎**: Ren'Py 8.3.x
- **分辨率**: 1920×1080
- **目标平台**: Windows / macOS / Linux (Steam)
- **开发语言**: GDScript (Ren'Py) + Python 3

## 快速开始

### 环境要求

- Ren'Py SDK 8.3.x
- Python 3.11+（用于工具脚本和测试）

### 运行游戏

1. 下载并安装 [Ren'Py SDK](https://www.renpy.org/) 8.3.x
2. 打开 Ren'Py SDK Launcher
3. 选择「打开项目」，指向本项目根目录
4. 点击「启动项目」

或命令行启动：
```bash
renpy.exe "D:\双生天使的怀抱\2026-07-30-13-48-52"
```

### 开发环境

```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 运行 lint
ruff check game/scripts/systems/ tests/ tools/

# 运行数据校验
python tools/validate_data.py
python tools/validate_consistency.py

# 运行测试
python -m pytest tests/ -v
```

## 项目结构

```
├── game/                    # Ren'Py 游戏目录
│   ├── scripts/             # 叙事脚本 + 系统层
│   │   ├── ch01_sephirot_01.rpy  # Ch1 叙事脚本
│   │   ├── ch02~ch16        # Ch2-16 骨架
│   │   └── systems/         # 系统层 (init python)
│   ├── data/                # JSON 数据层
│   ├── gui/                 # 界面层
│   ├── images/              # 图片资产
│   ├── audio/               # 音频资产
│   ├── options.rpy          # 全局配置
│   ├── screens.rpy          # Screen 定义
│   ├── gui.rpy              # GUI 主题
│   └── script.rpy           # 入口
├── tools/                   # 工具脚本
├── tests/                   # 测试
├── docs/                    # 文档
├── design/                  # 设计文档
├── production/              # 制作文档
└── .github/workflows/       # CI 配置
```

## 核心系统

| 系统 | 代号 | 职责 |
|------|------|------|
| 叙事引擎 | C1 | 章节路由、五拍叙事、标签系统 |
| 天使陪伴 | C2 | 天使状态机、翅膀亮度、互动 |
| 选择系统 | C3 | 选择呈现、后果分发 |
| 质点进程 | C4 | 16 质点状态机、完成判定 |
| 存在保护 | C5 | 暗流触发、天使介入、翅膀代价 |
| 存档系统 | C6 | 存档槽位、persistent 管理 |

## 文档

- [主架构文档](docs/architecture/main-architecture.md)
- [Epic/Story 拆分](production/epics/epic-breakdown.md)
- [Batch 0 骨架定义](production/batch0-skeleton.md)
- [贡献指南](CONTRIBUTING.md)
