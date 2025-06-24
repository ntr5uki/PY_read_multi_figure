#!/usr/bin/env python3
"""
测试 ImageSequenceViewer 的交互式裁剪功能
"""

import numpy as np
import sys
import os

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pynbgui.image_sequence_viewer import ImageSequenceViewer


def create_test_sequence():
    """创建测试图像序列"""
    # 创建一个有明显特征的图像序列
    frames, height, width = 8, 150, 200
    
    # 创建基础图像序列
    sequence = np.zeros((frames, height, width), dtype=np.uint8)
    
    for i in range(frames):
        # 每一帧都有不同的图案
        frame = np.zeros((height, width), dtype=np.uint8)
        
        # 外框
        frame[20:130, 30:170] = 80 + i * 10
        
        # 中央矩形（随帧变化位置）
        center_y = 60 + i * 2
        center_x = 80 + i * 3
        frame[center_y:center_y+30, center_x:center_x+40] = 150 + i * 5
        
        # 内部亮点
        bright_y = center_y + 10
        bright_x = center_x + 15
        frame[bright_y:bright_y+10, bright_x:bright_x+10] = 255
        
        # 添加一些噪声
        noise = np.random.randint(0, 15, (height, width))
        frame = np.clip(frame + noise, 0, 255).astype(np.uint8)
        
        sequence[i] = frame
    
    return sequence


def test_sequence_crop_basic():
    """基本的序列裁剪测试"""
    print("🎯 测试 ImageSequenceViewer 交互式裁剪功能")
    print("=" * 60)
    
    # 创建测试序列
    sequence = create_test_sequence()
    
    print(f"✅ 创建测试图像序列:")
    print(f"   序列尺寸: {sequence.shape}")
    print(f"   帧数: {sequence.shape[0]}")
    print(f"   图像尺寸: {sequence.shape[1]} x {sequence.shape[2]}")
    print(f"   数据类型: {sequence.dtype}")
    print(f"   数据范围: [{sequence.min()}, {sequence.max()}]")
    
    # 创建图像序列查看器
    print(f"\n🚀 创建图像序列查看器...")
    viewer = ImageSequenceViewer(sequence, useRangeSlider=True, showSizeControl=True)
    
    # 显示查看器
    print(f"📺 显示图像序列查看器...")
    viewer.display()
    
    print(f"\n📋 测试步骤:")
    print(f"1. 在上方的图像序列查看器中选择一个参考帧")
    print(f"2. 运行: viewer.crop_sequence_interactive()")
    print(f"3. 在ROI选择器中选择要裁剪的区域")
    print(f"4. 点击 '确认选择' 按钮")
    print(f"5. 运行: viewer.check_crop_result()")
    print(f"6. 查看裁剪后的图像序列")
    
    return viewer


def test_crop_workflow(viewer):
    """测试完整的裁剪工作流程"""
    print(f"\n🔧 测试裁剪工作流程...")
    
    # 显示当前状态
    print(f"📊 当前状态:")
    print(f"   当前帧索引: {viewer.selectWidget.value}")
    print(f"   序列尺寸: {viewer.imageSequence.shape}")
    print(f"   当前图像尺寸: {viewer.getCurrentImage().shape}")
    
    # 启动交互式裁剪
    print(f"\n🎯 启动交互式裁剪...")
    try:
        viewer.crop_sequence_interactive()
        print(f"✅ 交互式裁剪启动成功")
        
        print(f"\n📋 下一步操作:")
        print(f"1. 在ROI选择器中选择区域")
        print(f"2. 点击确认按钮")
        print(f"3. 运行: check_crop_workflow_result(viewer)")
        
        return True
        
    except Exception as e:
        print(f"❌ 启动交互式裁剪失败: {e}")
        return False


def check_crop_workflow_result(viewer):
    """检查裁剪工作流程的结果"""
    print(f"\n🔍 检查裁剪结果...")
    
    # 获取裁剪状态
    status = viewer.get_crop_status()
    print(f"裁剪状态: {status}")
    
    # 检查并应用结果
    success = viewer.check_crop_result()
    
    if success:
        print(f"\n🎉 裁剪工作流程完成!")
        print(f"📊 最终状态:")
        print(f"   新序列尺寸: {viewer.imageSequence.shape}")
        print(f"   新帧数: {viewer.numImages}")
        print(f"   当前图像尺寸: {viewer.getCurrentImage().shape}")
        
        # 验证裁剪结果
        original_frames = 8
        if viewer.numImages == original_frames:
            print(f"✅ 帧数保持不变: {viewer.numImages}")
        else:
            print(f"⚠️ 帧数发生变化: {original_frames} -> {viewer.numImages}")
        
        return True
    else:
        print(f"❌ 裁剪工作流程未完成")
        return False


def test_edge_cases():
    """测试边界情况"""
    print(f"\n🧪 测试边界情况...")
    
    # 测试单帧序列
    print(f"测试单帧序列...")
    single_frame = np.random.rand(1, 100, 150).astype(np.uint8) * 255
    viewer_single = ImageSequenceViewer(single_frame)
    
    print(f"   单帧序列尺寸: {single_frame.shape}")
    print(f"   查看器帧数: {viewer_single.numImages}")
    
    # 测试2D图像
    print(f"\n测试2D图像...")
    image_2d = np.random.rand(100, 150).astype(np.uint8) * 255
    viewer_2d = ImageSequenceViewer(image_2d)
    
    print(f"   2D图像尺寸: {image_2d.shape}")
    print(f"   查看器序列尺寸: {viewer_2d.imageSequence.shape}")
    print(f"   查看器帧数: {viewer_2d.numImages}")
    
    return viewer_single, viewer_2d


def demonstrate_usage():
    """演示使用方法"""
    print(f"\n📖 ImageSequenceViewer 交互式裁剪使用指南")
    print("=" * 60)
    
    print(f"""
## 🎯 功能概述
ImageSequenceViewer 现在支持交互式序列裁剪功能，可以：
- 使用当前显示帧作为参考进行ROI选择
- 对整个图像序列应用相同的裁剪区域
- 自动更新查看器显示裁剪后的序列

## 🚀 使用步骤

### 1. 创建图像序列查看器
```python
from pynbgui.image_sequence_viewer import ImageSequenceViewer
import numpy as np

# 创建或加载图像序列
sequence = np.random.rand(10, 200, 300).astype(np.uint8) * 255
viewer = ImageSequenceViewer(sequence)
viewer.display()
```

### 2. 选择参考帧
在图像序列查看器中选择一个合适的帧作为ROI选择的参考。

### 3. 启动交互式裁剪
```python
viewer.crop_sequence_interactive()
```

### 4. 选择ROI区域
在弹出的ROI选择器中：
- 拖动滑块选择感兴趣区域
- 查看实时预览
- 点击"确认选择"按钮

### 5. 应用裁剪结果
```python
success = viewer.check_crop_result()
if success:
    print("裁剪完成!")
else:
    print("请先完成ROI选择")
```

## 🔧 辅助方法

### 检查裁剪状态
```python
status = viewer.get_crop_status()
print("当前状态:", status)
```

### 获取当前图像
```python
current_image = viewer.getCurrentImage()
print("当前图像尺寸:", current_image.shape)
```

## ⚠️ 注意事项
- 裁剪操作是异步的，需要用户交互完成
- 裁剪会应用到整个图像序列
- 建议选择具有代表性特征的帧作为参考
- 裁剪后原始序列会被替换
""")


if __name__ == "__main__":
    print("🚀 ImageSequenceViewer 交互式裁剪测试")
    print("=" * 60)
    
    # 演示使用方法
    demonstrate_usage()
    
    # 运行基本测试
    viewer = test_sequence_crop_basic()
    
    # 测试边界情况
    viewer_single, viewer_2d = test_edge_cases()
    
    print(f"\n" + "=" * 60)
    print(f"🎮 交互式测试:")
    print(f"1. 运行: test_crop_workflow(viewer)")
    print(f"2. 在ROI选择器中选择区域并确认")
    print(f"3. 运行: check_crop_workflow_result(viewer)")
    print(f"4. 查看裁剪后的图像序列")
    
    print(f"\n💡 提示: 在Jupyter notebook中运行效果最佳")
