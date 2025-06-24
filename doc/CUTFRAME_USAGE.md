# CutFrameSelector 类使用指南

## 📋 概述

`CutFrameSelector` 是一个面向对象的3D图像裁剪工具类，提供交互式ROI选择功能。用户可以在2D参考图像上选择感兴趣区域，然后自动对对应的3D图像进行裁剪。同时保持向后兼容的 `cutFrame` 函数接口。

## 🎯 功能特点

- ✅ **交互式ROI选择**: 使用直观的滑块界面选择感兴趣区域
- ✅ **实时预览**: 在2D参考图像上实时显示ROI框
- ✅ **自动裁剪**: 根据选择的ROI自动裁剪3D图像
- ✅ **尺寸验证**: 自动检查输入图像尺寸的兼容性
- ✅ **Jupyter兼容**: 专为Jupyter notebook环境优化

## 📦 类接口

### CutFrameSelector 类

```python
class CutFrameSelector:
    """3D图像裁剪选择器类"""

    def __init__(self, img2d: np.ndarray, img3d: np.ndarray):
        """初始化裁剪选择器"""

    def display(self) -> 'CutFrameSelector':
        """显示ROI选择器界面"""

    def get_result(self) -> Optional[np.ndarray]:
        """获取裁剪结果"""

    def get_status(self) -> str:
        """获取当前状态描述"""

    def get_roi_info(self) -> Optional[Dict[str, Any]]:
        """获取ROI详细信息"""

    def reset(self) -> None:
        """重置选择器状态"""
```

### 向后兼容函数

```python
def cutFrame(img2d: np.ndarray, img3d: np.ndarray) -> CutFrameSelector:
    """创建3D图像裁剪选择器（便捷函数）"""

def get_cutframe_result(selector: CutFrameSelector) -> Optional[np.ndarray]:
    """获取裁剪结果（便捷函数）"""
```

## 🔧 输入要求

### 尺寸要求
- `img2d.shape[0] == img3d.shape[1]` (高度匹配)
- `img2d.shape[1] == img3d.shape[2]` (宽度匹配)

### 数据类型
- 支持任何numpy数据类型
- 推荐使用 `uint8` 类型以获得最佳显示效果

### 示例尺寸
```python
img2d.shape = (200, 300)      # 2D参考图像
img3d.shape = (10, 200, 300)  # 3D图像 (10帧)
```

## 🚀 使用方法

### 1. 面向对象方式（推荐）

```python
import numpy as np
from pynbgui.interactive_image_viewer import CutFrameSelector

# 准备数据
img2d = np.random.rand(200, 300) * 255
img2d = img2d.astype(np.uint8)

img3d = np.random.rand(10, 200, 300) * 255
img3d = img3d.astype(np.uint8)

# 创建选择器实例
selector = CutFrameSelector(img2d, img3d)

# 显示ROI选择器
selector.display()
```

### 2. 函数式方式（向后兼容）

```python
import numpy as np
from pynbgui.interactive_image_viewer import cutFrame, get_cutframe_result

# 准备数据（同上）
# ...

# 调用cutFrame函数
roi_selector = cutFrame(img2d, img3d)
```

### 2. 用户交互

1. **拖动X范围滑块**: 选择水平方向的ROI范围
2. **拖动Y范围滑块**: 选择垂直方向的ROI范围
3. **实时预览**: 在图像上查看蓝色ROI框
4. **点击确认**: 点击"确认选择"按钮完成选择

### 3. 获取结果

```python
# 检查结果（在用户确认选择后）
result = get_cutframe_result(roi_selector)

if result is not None:
    print(f'✅ 裁剪完成! 新尺寸: {result.shape}')
    # 使用裁剪后的3D图像
    cropped_img3d = result
else:
    print('⏳ 请先在ROI选择器中完成选择')
```

## 📊 完整示例

```python
import numpy as np
from pynbgui.interactive_image_viewer import cutFrame, get_cutframe_result

def example_usage():
    # 1. 创建示例数据
    height, width, frames = 200, 300, 10
    
    # 2D参考图像（带有一些图案）
    img2d = np.zeros((height, width), dtype=np.uint8)
    img2d[50:150, 75:225] = 128  # 中央矩形
    img2d[75:125, 100:200] = 255  # 内部亮区
    
    # 3D图像（每帧强度不同）
    img3d = np.zeros((frames, height, width), dtype=np.uint8)
    for i in range(frames):
        intensity = int(255 * (i + 1) / frames)
        img3d[i] = img2d * intensity // 255
    
    print(f"数据准备完成:")
    print(f"  img2d: {img2d.shape}")
    print(f"  img3d: {img3d.shape}")
    
    # 2. 启动ROI选择
    roi_selector = cutFrame(img2d, img3d)
    
    print(f"ROI选择器已启动，请在界面中选择区域")
    
    return roi_selector

# 运行示例
roi_selector = example_usage()

# 稍后检查结果
# result = get_cutframe_result(roi_selector)
```

## ⚠️ 注意事项

### 异步操作
- `CutFrameSelector` 是异步操作，需要用户交互完成
- 创建实例后立即显示ROI选择器
- 用户点击确认按钮后，裁剪结果才会可用

### 获取结果的正确方式
```python
# 创建选择器并显示
selector = CutFrameSelector(img2d, img3d).display()

# 用户在界面中选择ROI并点击确认后
result = selector.get_result()
if result is not None:
    print(f"裁剪成功，结果尺寸: {result.shape}")
else:
    print("请先在ROI选择器中完成选择")
```

### 环境要求
- **推荐**: Jupyter notebook 环境
- **支持**: IPython 环境
- **限制**: 命令行环境可能无法正常显示界面

### 错误处理
```python
try:
    roi_selector = cutFrame(img2d, img3d)
except ValueError as e:
    print(f"尺寸不匹配: {e}")
```

## 🔍 故障排除

### 问题1: 界面不显示
**原因**: 不在Jupyter notebook环境中
**解决**: 在Jupyter notebook中运行代码

### 问题2: 尺寸不匹配错误
**原因**: img2d和img3d的尺寸不兼容
**解决**: 检查并调整图像尺寸
```python
print(f"img2d.shape: {img2d.shape}")
print(f"img3d.shape: {img3d.shape}")
print(f"要求: {img2d.shape} 的后两维应该等于 {img3d.shape} 的后两维")
```

### 问题3: 获取不到结果
**原因**: 用户尚未在ROI选择器中确认选择，或者回调函数未正确执行
**解决**:
1. 确保在ROI选择器中点击了"确认选择"按钮
2. 等待几秒钟让回调函数完成执行
3. 检查控制台是否有"✅ 3D图像裁剪完成"的消息

## 🎨 高级用法

### 自定义ROI处理
```python
def custom_roi_processing(roi_selector):
    """自定义ROI处理逻辑"""
    result = get_cutframe_result(roi_selector)
    
    if result is not None:
        # 对裁剪结果进行进一步处理
        processed = np.mean(result, axis=0)  # 时间平均
        return processed
    return None
```

### 批量处理
```python
def batch_cutframe(img2d, img3d_list):
    """批量处理多个3D图像"""
    results = []
    
    for i, img3d in enumerate(img3d_list):
        print(f"处理第 {i+1}/{len(img3d_list)} 个3D图像...")
        roi_selector = cutFrame(img2d, img3d)
        # 等待用户选择...
        results.append(roi_selector)
    
    return results
```

## 📚 相关函数

- `get_cutframe_result(roi_selector)`: 获取裁剪结果
- `PILROISelector`: 底层ROI选择器组件
- `InteractiveImageViewer`: 完整的图像查看器（包含cutFrame功能）
