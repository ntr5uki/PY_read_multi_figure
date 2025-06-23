# 智能操作面板 (SmartOperationPanel)

## 📋 概述

智能操作面板是一个基于ipywidgets的下拉菜单组件，专为Jupyter notebook环境设计。它提供了类似原生下拉菜单的用户体验，同时保持了完全的Jupyter兼容性。

## ✨ 主要特性

### 🎯 核心功能
- **下拉菜单效果**: 点击主按钮展开/收起菜单，提供直观的操作体验
- **动态状态管理**: 可以实时启用/禁用菜单项，响应应用状态变化
- **样式自定义**: 支持多种按钮样式（primary, success, info, warning, danger）
- **图标支持**: 菜单项支持emoji图标和文字描述
- **回调机制**: 灵活的事件处理系统，支持自定义回调函数

### 🔧 扩展性设计
- **易于扩展**: 简单的API添加/删除菜单项
- **模块化设计**: 独立的类设计，易于集成到现有项目
- **响应式布局**: 支持不同宽度和样式需求
- **状态监控**: 提供完整的状态查询接口

### 🚀 性能优化
- **轻量级**: 纯ipywidgets实现，无额外依赖
- **高性能**: 测试显示单次菜单切换<0.1ms，菜单项添加<1ms
- **内存友好**: 动态管理组件，支持大量菜单项

## 📦 文件结构

```
├── smart_operation_panel.py          # 核心类实现
├── test_smart_operation_panel.ipynb  # Jupyter notebook演示
├── test_panel_demo.py                # 命令行测试脚本
├── integration_example.py            # 集成示例
└── SmartOperationPanel_README.md     # 本文档
```

## 🚀 快速开始

### 基础使用

```python
from smart_operation_panel import SmartOperationPanel

# 创建操作面板
panel = SmartOperationPanel("🎯 我的操作", "200px")

# 显示面板
panel.display()
```

### 自定义菜单项

```python
# 添加自定义菜单项
panel.add_menu_item(
    item_id='custom_action',
    description='⚡ 自定义操作',
    button_style='primary',
    tooltip='执行自定义操作'
)

# 注册回调函数
def custom_callback(item_id, button):
    print(f"执行操作: {item_id}")

panel.register_callback('custom_action', custom_callback)
```

### 状态管理

```python
# 禁用菜单项
panel.set_menu_item_enabled('custom_action', False)

# 修改样式
panel.set_menu_item_style('custom_action', 'success')

# 查看状态
state = panel.get_menu_state()
print(f"菜单状态: {state}")
```

## 🎨 界面效果

### 收起状态
```
┌─────────────────────┐
│ [🎯 ROI操作 ▼]      │
└─────────────────────┘
```

### 展开状态
```
┌─────────────────────┐
│ [🎯 ROI操作 ▲]      │
├─────────────────────┤
│ [🎯 选择ROI区域]    │
│ [💾 保存当前ROI]    │
│ [📂 加载预设ROI]    │
│ [📊 ROI统计信息]    │
│ [🗑️ 清除ROI]       │
└─────────────────────┘
```

## 📚 API 参考

### SmartOperationPanel 类

#### 构造函数
```python
SmartOperationPanel(title: str = "🎯 操作菜单", width: str = "180px")
```

#### 主要方法

##### 菜单项管理
- `add_menu_item(item_id, description, button_style, tooltip, enabled)` - 添加菜单项
- `remove_menu_item(item_id)` - 删除菜单项
- `set_menu_item_enabled(item_id, enabled)` - 设置启用状态
- `set_menu_item_style(item_id, button_style)` - 设置按钮样式

##### 菜单控制
- `open_menu()` - 打开菜单
- `close_menu()` - 关闭菜单
- `toggle_menu()` - 切换菜单状态

##### 回调管理
- `register_callback(item_id, callback)` - 注册回调函数
- `unregister_callback(item_id)` - 取消注册回调

##### 状态查询
- `get_menu_state()` - 获取菜单状态信息

## 🧪 测试和演示

### 1. 命令行测试
```bash
python test_panel_demo.py
```

### 2. Jupyter notebook演示
```bash
jupyter notebook test_smart_operation_panel.ipynb
```

### 3. 集成示例
```bash
python integration_example.py
```

## 🔗 集成指南

### 集成到现有项目

1. **导入类**
```python
from smart_operation_panel import SmartOperationPanel
```

2. **创建面板**
```python
self.operation_panel = SmartOperationPanel("🎯 操作菜单", "200px")
```

3. **注册回调**
```python
self.operation_panel.register_callback('action_id', self.action_callback)
```

4. **集成到布局**
```python
main_layout = widgets.VBox([
    title_widget,
    self.operation_panel.panel,  # 添加操作面板
    content_widget
])
```

### ROI功能集成示例

```python
class ROIImageViewer:
    def __init__(self):
        # 创建ROI操作面板
        self.roi_panel = SmartOperationPanel("🎯 ROI操作", "200px")
        
        # 注册ROI相关回调
        self.roi_panel.register_callback('select_roi', self._select_roi)
        self.roi_panel.register_callback('save_roi', self._save_roi)
        self.roi_panel.register_callback('load_roi', self._load_roi)
        
        # 初始状态管理
        self._update_roi_state(has_image=False, has_roi=False)
    
    def _update_roi_state(self, has_image: bool, has_roi: bool):
        """根据状态更新菜单可用性"""
        self.roi_panel.set_menu_item_enabled('select_roi', has_image)
        self.roi_panel.set_menu_item_enabled('save_roi', has_roi)
        self.roi_panel.set_menu_item_enabled('clear_roi', has_roi)
```

## 🎯 设计原则

### 1. **用户体验优先**
- 直观的下拉菜单交互
- 清晰的视觉反馈
- 响应式状态管理

### 2. **技术兼容性**
- 纯ipywidgets实现
- 无额外JavaScript依赖
- 完全Jupyter兼容

### 3. **扩展性设计**
- 模块化架构
- 灵活的API设计
- 易于定制和扩展

### 4. **性能考虑**
- 轻量级实现
- 高效的事件处理
- 内存友好的设计

## 🔮 未来规划

### Phase 1: 基础功能 ✅
- [x] 下拉菜单基础实现
- [x] 状态管理系统
- [x] 回调机制
- [x] 测试和文档

### Phase 2: 增强功能 🚧
- [ ] 菜单项分组功能
- [ ] 键盘快捷键支持
- [ ] 动画效果优化
- [ ] 主题样式系统

### Phase 3: 高级功能 📋
- [ ] 嵌套菜单支持
- [ ] 拖拽排序功能
- [ ] 菜单配置持久化
- [ ] 国际化支持

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进智能操作面板！

### 开发环境设置
```bash
# 安装依赖
pip install ipywidgets jupyter

# 运行测试
python test_panel_demo.py

# 启动Jupyter
jupyter notebook test_smart_operation_panel.ipynb
```

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

---

**智能操作面板** - 让Jupyter notebook中的下拉菜单变得简单而强大！ 🚀
