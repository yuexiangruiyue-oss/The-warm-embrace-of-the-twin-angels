# CLAUDE.md -- 项目技术偏好
# The Embrace of the Twin Angels

## 引擎

- Ren'Py 8.3.x (Python 3)
- 目标平台: Windows / macOS / Linux (Steam)
- 分辨率: 1920×1080

## 编码标准

### Ren'Py 脚本 (.rpy)
- `init python:` 块定义 Python 类和函数
- `default` 声明存档变量（随存档保存）
- `persistent.` 声明跨周目变量
- 变量命名: snake_case
- 类名: PascalCase
- 常量: UPPER_SNAKE_CASE
- init 优先级: constants(0) -> state(1) -> systems(2+)

### Python 代码 (.py)
- PEP 8
- ruff lint
- 类型注解推荐
- data_loader.py 需兼容 Ren'Py 运行时和测试环境

### JSON 数据
- UTF-8 编码
- 4 空格缩进
- 模板文件以 `_` 开头
- 数据驱动：叙事内容与代码分离 (ADR-002)

## 架构约束

- 系统间通信: 直接函数调用 + 接口契约 (ADR-003)
- 无事件总线
- 变量所有权矩阵: 每个变量有唯一所有者 (main-architecture.md §6)
- 禁止跨所有者直接修改变量

## 翅膀亮度模型 (ADR-004)

- 双层模型: permanent + temporary
- displayed = max(动态下限, permanent - temporary)
- permanent: 阶段基线初始化 -> C5 代价扣减 -> 阶段切换重置
- temporary: 场景级 -> 场景结束清零
- Phase 1 代价乘数 = 0.0 (免费保护)

## 测试

- 验证驱动开发: 先写测试，再实现
- 单元测试: tests/unit/
- 集成测试: tests/integration/
- 覆盖率目标: >= 80%
- 命令: python -m pytest tests/ -v

## Git 工作流

- 分支: main (稳定), develop (集成), feature/E{X.Y}-{slug}
- 提交: type(scope): description
- 高影响动作（提交、删除、上线）须人工审批
