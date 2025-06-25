# 添加菜单按钮并实现功能：精简指南

本指南总结了在 `pynbgui` 项目中添加新菜单按钮及其功能的关键修改点。

## 核心修改点

### 1. `pynbgui/horizontal_menu_bar.py`

**目的**: 定义新的菜单按钮。

**修改位置**: 在 `create_menu_bars` 函数中，添加新的 `tools_panel.add_menu_item` 调用。

**示例**: (添加“调整大小”按钮)

```python
# ...
    tools_panel.add_menu_item(
        item_id='resize_select', # 唯一ID
        description='🎯 调整大小', # 按钮文本
        button_style='primary',
        tooltip='调整大小'
    )
# ...
```

### 2. `pynbgui/interactive_image_viewer.py`

**目的**: 注册菜单按钮的点击事件，并将事件转发到核心逻辑层。

**修改位置**: 

*   在 `InteractiveImageViewer` 类的 `__init__` 方法中注册回调。
*   添加一个新的方法来处理菜单点击事件。

**示例**: 

```python
# ...
class InteractiveImageViewer:
    def __init__(self, ...):
        # ...
        self.tools_panel.register_callback("resize_select", self._on_resize_menu_clicked)
        # ...

    def _on_resize_menu_clicked(self, item_id: str, button) -> None:
        print("🎯 从菜单栏触发调整大小")
        if self.imageViewer is None:
            print("❌ 请先选择一个图像数组")
            return
        self.imageViewer.resize_interactive() # 调用 ImageSequenceViewer 中的方法
# ...
```

### 3. `pynbgui/image_sequence_viewer.py`

**目的**: 实现菜单按钮对应的核心功能逻辑。

**修改位置**: 

*   导入必要的组件 (如 `ResizePopupWidget`)
*   添加一个交互式启动方法 (如 `resize_interactive`)
*   添加一个回调方法来处理交互式组件的确认事件 (如 `_on_resize_confirm`)

**示例**: 

```python
# ...
from .resize_dialog_widget import ResizePopupWidget
# ...

class ImageSequenceViewer:
    # ...
    def resize_interactive(self) -> None:
        try:
            self.resize_selector = ResizePopupWidget(self.imageSequence)
            self.resize_selector.register_confirm_callback(self._on_resize_confirm)
            self.resize_selector.display()
        except Exception as e:
            print(f"❌ 启动交互式调整大小失败: {e}")
            raise

    def _on_resize_confirm(self, wgt: ResizePopupWidget) -> None:
        try:
            if not hasattr(self, 'resize_selector'):
                print("❌ 尚未启动交互式调整大小")
                return
            new_size = wgt.get_confirm_size()
            if new_size is not None:
                from scipy.ndimage import zoom
                old_shape = self.imageSequence.shape
                if len(new_size) == len(old_shape):
                    scale_factors = tuple(ns / os for ns, os in zip(new_size, old_shape))
                    print(f"缩放因子: {scale_factors}")
                    data = zoom(self.imageSequence, scale_factors, order=1)
                    self.updateImageSequence(data)
                else:
                    print(f"❌ 调整大小失败: 新旧尺寸维度不匹配。新尺寸: {new_size}, 旧尺寸: {old_shape}")
            delattr(self, 'resize_selector')
        except Exception as e:
            print(f"❌ 调整大小时出错: {e}")
            raise
# ...
```

### 4. `pynbgui/confirm_cancel_mixin.py` (回调签名)

**目的**: 确保回调函数接收的参数与 Mixin 定义一致。

**注意**: 当前设计中，`confirm_callbacks` 和 `cancel_callbacks` 只接收触发事件的 widget 实例 (`self`) 作为参数。

**示例**: 

```python
# ...
            for callback in self.confirm_callbacks:
                try:
                    callback(self) # 确保只传入 widget 实例
                except Exception as e:
                    print(f"⚠️ 确认回调执行失败: {e}")
# ...
```

## 总结

添加新菜单功能的核心流程是：**定义按钮 -> 注册事件 -> 实现功能**。确保三个主要文件 (`horizontal_menu_bar.py`, `interactive_image_viewer.py`, `image_sequence_viewer.py`) 之间的协作，并注意回调函数的参数签名一致性。
