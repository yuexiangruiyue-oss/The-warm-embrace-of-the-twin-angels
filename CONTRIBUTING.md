# 贡献指南 — 《双生天使的拥抱》

## 分支策略

- `main`: 稳定发布分支
- `develop`: 集成分支
- `feature/E{X.Y}-{slug}`: 功能分支（如 `feature/E0.1-project-init`）
- `release/v{X.Y.Z}`: 发布分支
- `hotfix/v{X.Y.Z}`: 热修复分支

## 提交规范

格式：`type(scope): description`

### 提交类型

- `feat`: 新功能
- `fix`: 修复
- `refactor`: 重构
- `test`: 测试
- `docs`: 文档
- `chore`: 杂项

### 作用域（scope）

- `c1`: 叙事引擎
- `c2`: 天使陪伴
- `c3`: 选择系统
- `c4`: 质点进程
- `c5`: 存在保护
- `c6`: 存档系统
- `data`: 数据层
- `ui`: 界面层
- `infra`: 基础设施

### 示例

- `feat(c5): implement undertow trigger engine`
- `fix(c2): wing brightness dynamic floor calculation`
- `test(c4): add sephirot completion tests`
- `docs(infra): update CI configuration`

## 代码规范

### Ren'Py 脚本（.rpy）

- 使用 `init python:` 块定义 Python 类和函数
- `default` 声明存档变量
- `persistent.` 声明跨周目变量
- 变量命名使用 snake_case
- 类名使用 PascalCase
- 常量使用 UPPER_SNAKE_CASE

### Python 代码（.py）

- 遵循 PEP 8
- 使用 ruff 进行 lint 检查
- 类型注解推荐但非强制

### JSON 数据

- 使用 UTF-8 编码
- 缩进 4 空格
- 模板文件以 `_` 开头（如 `_template.json`）

## 测试

- 单元测试放在 `tests/unit/`
- 集成测试放在 `tests/integration/`
- 运行测试：`python -m pytest tests/ -v`
- 覆盖率目标：≥ 80%

## 变量所有权

- 每个共享变量有唯一所有者系统
- 其他系统只能通过所有者暴露的接口读写
- 违反所有权规则的直接变量修改在代码审查中标记为 BLOCKER
- 详见 `docs/architecture/main-architecture.md` §6
