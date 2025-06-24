# ImageSequenceViewer 交互式裁剪功能

## 📋 功能概述

为 `ImageSequenceViewer` 类添加了交互式序列裁剪功能，允许用户：
- 使用当前显示帧作为参考进行ROI选择
- 对整个图像序列应用相同的裁剪区域
- 自动更新查看器以显示裁剪后的序列

## ✅ 新增方法

### 1. `crop_sequence_interactive()`

```python
def crop_sequence_interactive(self) -> None:
    """
    使用当前显示帧作为参考，对整个图像序列进行交互式裁剪
    """
```

**功能**:
- 获取当前显示的帧作为2D参考图像
- 自动归一化到0-255范围
- 创建 `CutFrameSelector` 实例
- 显示ROI选择界面

### 2. `check_crop_result()`

```python
def check_crop_result(self) -> bool:
    """
    检查裁剪结果并应用到图像序列
    
    Returns:
        True如果裁剪成功并已应用，False如果尚未完成或失败
    """
```

**功能**:
- 检查裁剪操作状态
- 获取裁剪结果
- 更新图像序列
- 刷新查看器显示

### 3. `get_crop_status()`

```python
def get_crop_status(self) -> str:
    """
    获取当前裁剪操作的状态
    
    Returns:
        状态描述字符串
    """
```

**功能**:
- 返回当前裁剪操作的状态
- 便于用户了解操作进度

### 4. `_normalize_to_uint8()` (内部方法)

```python
def _normalize_to_uint8(self, image: np.ndarray) -> np.ndarray:
    """
    将图像归一化到0-255的uint8范围
    """
```

**功能**:
- 使用全局范围进行归一化
- 确保参考图像的一致性
- 返回uint8格式的图像

### 5. `_on_crop_confirmed()` (内部回调方法)

```python
def _on_crop_confirmed(self, crop_selector) -> None:
    """
    裁剪确认回调函数，自动应用裁剪结果
    """
```

**功能**:
- 自动获取裁剪结果
- 更新图像序列
- 显示详细的裁剪信息
- 清理临时资源

## 🚀 使用方法

### 基本使用流程（自动应用）

```python
from pynbgui.image_sequence_viewer import ImageSequenceViewer
import numpy as np

# 1. 创建图像序列查看器
sequence = np.random.rand(10, 200, 300).astype(np.uint8) * 255
viewer = ImageSequenceViewer(sequence)
viewer.display()

# 2. 选择合适的参考帧（在查看器中切换帧）

# 3. 启动交互式裁剪
viewer.crop_sequence_interactive()

# 4. 在ROI选择器中选择区域并点击确认
# 🎉 裁剪结果会自动应用到图像序列！

# 5. 可选：检查状态
status = viewer.get_crop_status()
print(f"状态: {status}")
```

### 手动检查方式（向后兼容）

```python
# 如果需要手动控制应用时机
viewer.crop_sequence_interactive()

# 用户选择ROI后，手动检查和应用
success = viewer.check_crop_result()
if success:
    print("✅ 裁剪完成!")
    print(f"新序列尺寸: {viewer.imageSequence.shape}")
```

### 状态监控

```python
# 检查裁剪状态
status = viewer.get_crop_status()
print(f"当前状态: {status}")

# 获取当前图像信息
current_image = viewer.getCurrentImage()
print(f"当前图像尺寸: {current_image.shape}")
```

## 🔧 技术实现

### 自动应用机制

1. **回调注册**: 在创建 `CutFrameSelector` 后注册确认回调
2. **自动触发**: 用户点击确认按钮后自动调用 `_on_crop_confirmed`
3. **即时应用**: 获取裁剪结果并立即更新图像序列
4. **资源清理**: 自动清理临时的裁剪选择器引用

### 参考图像获取

1. **使用原始数据**: 始终使用 `getCurrentImage()` 获取原始图像数据
2. **避免SizeControl影响**: 不使用 `imageViewer.dataDisplay`，因为它会受到SizeControl缩放影响
3. **归一化处理**: 使用 `_normalize_to_uint8()` 方法将原始数据归一化到0-255范围
4. **数据验证**: 确保参考图像是2D数组

### 序列更新机制

1. **获取裁剪结果**: 从 `CutFrameSelector` 获取裁剪后的3D数组
2. **更新序列**: 调用 `updateImageSequence()` 方法
3. **刷新显示**: 自动更新查看器界面
4. **清理资源**: 删除临时的裁剪选择器引用

### 错误处理

- 输入验证（2D参考图像检查）
- 异常捕获和详细错误信息
- 状态检查和用户提示

### SizeControl 独立性

**问题**: 最初的实现中，交互式裁剪功能可能会受到SizeControl（图像大小滑块）的影响，因为使用了 `imageViewer.dataDisplay` 作为参考图像。

**解决方案**:
- 始终使用 `getCurrentImage()` 获取原始图像数据
- 通过 `_normalize_to_uint8()` 方法进行归一化
- 确保参考图像的尺寸与原始序列数据一致

**验证**:
- `getCurrentImage()` 返回的是 `imageSequence[index]`，不受SizeControl影响
- `_normalize_to_uint8()` 使用全局范围进行归一化，保持数据一致性

## 📊 测试验证

### 测试覆盖

1. **方法可用性测试**: 验证所有新方法都正确添加
2. **数据类型测试**: 验证归一化方法的正确性
3. **集成测试**: 验证完整的裁剪工作流程
4. **边界情况测试**: 单帧序列、2D图像等

### 测试文件

- `test_sequence_crop.py`: 基本功能测试和使用示例
- `test_crop_integration.py`: 集成测试和方法验证

## 🎯 设计特点

### 1. 最小化代码改动

- 只添加新方法，不修改现有UI组件
- 复用现有的方法和属性
- 保持与现有架构的兼容性

### 2. 用户友好

- 清晰的状态反馈
- 详细的使用说明
- 错误处理和提示

### 3. 灵活性

- 支持任意尺寸的图像序列
- 自动处理数据类型转换
- 兼容现有的对比度调整功能

## 📋 使用示例

### 完整示例

```python
# 创建测试数据
import numpy as np
from pynbgui.image_sequence_viewer import ImageSequenceViewer

# 创建图像序列
frames, height, width = 5, 150, 200
sequence = np.zeros((frames, height, width), dtype=np.uint8)

for i in range(frames):
    # 创建有特征的图像
    frame = np.zeros((height, width), dtype=np.uint8)
    frame[30:120, 40:160] = 100 + i * 30  # 主要区域
    frame[60:90, 80:120] = 200           # 中央区域
    sequence[i] = frame

# 创建查看器
viewer = ImageSequenceViewer(sequence, useRangeSlider=True)
viewer.display()

# 交互式裁剪
print("1. 选择参考帧")
print("2. 启动裁剪:")
print("   viewer.crop_sequence_interactive()")
print("3. 选择ROI区域并确认")
print("4. 应用结果:")
print("   viewer.check_crop_result()")
```

### 状态检查示例

```python
# 检查当前状态
def check_status(viewer):
    print(f"序列尺寸: {viewer.imageSequence.shape}")
    print(f"当前帧: {viewer.selectWidget.value}")
    print(f"裁剪状态: {viewer.get_crop_status()}")
    
    if hasattr(viewer, 'crop_selector'):
        result = viewer.crop_selector.get_result()
        if result is not None:
            print(f"裁剪结果可用: {result.shape}")
        else:
            print("等待用户完成ROI选择")
    else:
        print("尚未启动裁剪操作")
```

## 🎉 总结

成功为 `ImageSequenceViewer` 添加了完整的交互式裁剪功能：

### ✅ 实现的功能
- 交互式ROI选择
- 序列批量裁剪
- 自动界面更新
- 状态监控和反馈

### ✅ 技术特点
- 最小化代码改动
- 复用现有架构
- 完善的错误处理
- 用户友好的接口

### ✅ 测试验证
- 全面的功能测试
- 边界情况覆盖
- 集成测试验证

这个功能为用户提供了便捷的图像序列裁剪工具，可以显著提高图像处理的效率！
