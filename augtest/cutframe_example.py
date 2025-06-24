#!/usr/bin/env python3
"""
cutFrame 函数使用示例
适用于 Jupyter notebook 环境
"""

import numpy as np
from pynbgui.interactive_image_viewer import cutFrame, get_cutframe_result


def create_sample_data():
    """创建示例数据"""
    # 创建一个200x300的2D图像
    height, width = 200, 300
    img2d = np.zeros((height, width), dtype=np.uint8)
    
    # 添加一些图案
    # 外框
    img2d[20:180, 30:270] = 100
    # 中央矩形
    img2d[60:140, 90:210] = 180
    # 内部亮点
    img2d[90:110, 135:165] = 255
    
    # 创建对应的3D图像 (10帧)
    frames = 10
    img3d = np.zeros((frames, height, width), dtype=np.uint8)
    
    for i in range(frames):
        # 每一帧强度不同
        frame_intensity = 0.5 + 0.5 * (i / (frames - 1))
        img3d[i] = (img2d * frame_intensity).astype(np.uint8)
        
        # 添加一些随机噪声
        noise = np.random.randint(0, 20, (height, width))
        img3d[i] = np.clip(img3d[i] + noise, 0, 255).astype(np.uint8)
    
    return img2d, img3d


def example_basic_usage():
    """基本使用示例"""
    print("🎯 cutFrame 基本使用示例")
    print("=" * 40)
    
    # 1. 创建示例数据
    img2d, img3d = create_sample_data()
    print(f"✅ 创建示例数据:")
    print(f"   2D图像尺寸: {img2d.shape}")
    print(f"   3D图像尺寸: {img3d.shape}")
    
    # 2. 调用cutFrame函数
    print(f"\n🚀 启动ROI选择器...")
    roi_selector = cutFrame(img2d, img3d)
    
    print(f"\n📋 使用说明:")
    print(f"1. 在上方的ROI选择器中拖动滑块选择感兴趣区域")
    print(f"2. 建议选择区域: X范围 [90, 210], Y范围 [60, 140]")
    print(f"3. 点击 '确认选择' 按钮")
    print(f"4. 运行下面的代码获取结果:")
    print(f"   result = get_cutframe_result(roi_selector)")
    print(f"   print(f'裁剪结果: {{result.shape if result is not None else \"未完成选择\"}}')") 
    
    return roi_selector


def check_result(roi_selector):
    """检查裁剪结果"""
    result = get_cutframe_result(roi_selector)
    
    if result is not None:
        print(f"✅ 裁剪完成!")
        print(f"   裁剪后的3D图像尺寸: {result.shape}")
        print(f"   数据类型: {result.dtype}")
        
        # 显示一些统计信息
        print(f"\n📊 裁剪结果统计:")
        print(f"   最小值: {result.min()}")
        print(f"   最大值: {result.max()}")
        print(f"   平均值: {result.mean():.2f}")
        print(f"   标准差: {result.std():.2f}")
        
        return result
    else:
        print("⏳ ROI选择尚未完成，请先在选择器中确认选择")
        return None


def example_with_validation():
    """带验证的使用示例"""
    print("\n🔍 带验证的使用示例")
    print("=" * 40)
    
    # 创建数据
    img2d, img3d = create_sample_data()
    
    # 验证输入
    print(f"🔍 验证输入数据...")
    assert img2d.shape[0] == img3d.shape[1], f"高度不匹配: {img2d.shape[0]} != {img3d.shape[1]}"
    assert img2d.shape[1] == img3d.shape[2], f"宽度不匹配: {img2d.shape[1]} != {img3d.shape[2]}"
    print(f"✅ 输入验证通过")
    
    # 调用函数
    roi_selector = cutFrame(img2d, img3d)
    
    return roi_selector


# Jupyter notebook 使用示例
def jupyter_example():
    """
    在Jupyter notebook中的完整使用示例
    """
    print("📓 Jupyter Notebook 使用示例")
    print("=" * 50)
    
    print("""
# 在Jupyter notebook中使用cutFrame函数

## 1. 导入必要的库
```python
import numpy as np
from pynbgui.interactive_image_viewer import cutFrame, get_cutframe_result
```

## 2. 准备数据
```python
# 创建2D参考图像
img2d = np.random.rand(200, 300) * 255
img2d = img2d.astype(np.uint8)

# 创建3D图像数据
img3d = np.random.rand(10, 200, 300) * 255
img3d = img3d.astype(np.uint8)
```

## 3. 调用cutFrame函数
```python
roi_selector = cutFrame(img2d, img3d)
```

## 4. 在ROI选择器中选择区域并确认

## 5. 获取结果
```python
result = get_cutframe_result(roi_selector)
if result is not None:
    print(f'裁剪后的3D图像尺寸: {result.shape}')
else:
    print('请先在ROI选择器中完成选择')
```

## 注意事项
- 确保 img2d.shape[0] == img3d.shape[1] 且 img2d.shape[1] == img3d.shape[2]
- ROI选择是异步的，需要用户交互完成
- 如果取消选择，将返回原始3D图像的副本
""")


if __name__ == "__main__":
    # 显示使用说明
    jupyter_example()
    
    # 运行基本示例
    roi_selector = example_basic_usage()
    
    print(f"\n" + "=" * 50)
    print(f"🎉 示例程序运行完成!")
    print(f"💡 提示: 在Jupyter notebook中运行效果最佳")
