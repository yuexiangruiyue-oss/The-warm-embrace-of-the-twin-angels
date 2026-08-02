# Ren'Py 版本参考

## 项目钉定版本

**Ren'Py 8.3.x**（最新稳定版 8.3.7）

## 关键 API 参考

### 存档系统
- `renpy.save(slot)` — 保存到指定槽位
- `renpy.load(slot)` — 从指定槽位读取
- `renpy.unlink_save(slot)` — 删除存档
- `renpy.slot_json(slot)` — 获取槽位 JSON 元数据
- `renpy.slot_time(slot)` — 获取槽位时间戳
- `renpy.slot_screenshot(slot)` — 获取槽位截图

### 叙事控制
- `renpy.pause(duration)` — 暂停指定时间
- `renpy.jump(label)` — 跳转到指定 label
- `renpy.call(label)` — 调用指定 label（带返回）

### 变量声明
- `default var_name = value` — 声明存档级变量
- `define var_name = value` — 声明常量
- `persistent.var_name` — 跨周目持久变量

### Screen 语言
- `screen name():` — 定义 Screen
- `textbutton` — 文本按钮
- `bar value` — 滑动条
- `frame` / `vbox` / `hbox` — 布局容器

### 图像处理
- `im.MatrixColor` — 图像颜色矩阵变换
- `Transform` — 图像变换
- `Solid(color)` — 纯色图像
- `image name = path` — 图像定义

## 已知限制

1. `im.MatrixColor` 在高频调用时可能影响性能（需 playtest 验证）
2. Python `@dataclass` 的 pickle 序列化需要测试兼容性
3. Ren'Py 的 `self-voicing` 功能需要真实屏幕阅读器测试

## 版本兼容性

| 版本 | 策略 |
|------|------|
| 0.1.x | 基线版本，无兼容性处理 |
| 0.x.x | 新增 `default` 变量自动提供默认值 |
| 1.0.x | 存档迁移脚本（如需要） |
