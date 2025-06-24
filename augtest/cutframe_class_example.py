#!/usr/bin/env python3
"""
CutFrameSelector 类使用示例
展示面向对象的3D图像裁剪功能
"""

import numpy as np
from pynbgui.interactive_image_viewer import CutFrameSelector


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


def example_basic_class_usage():
    """基本类使用示例"""
    print("🎯 CutFrameSelector 基本使用示例")
    print("=" * 40)
    
    # 1. 创建示例数据
    img2d, img3d = create_sample_data()
    print(f"✅ 创建示例数据:")
    print(f"   2D图像尺寸: {img2d.shape}")
    print(f"   3D图像尺寸: {img3d.shape}")
    
    # 2. 创建CutFrameSelector实例
    print(f"\n🚀 创建CutFrameSelector实例...")
    selector = CutFrameSelector(img2d, img3d)
    
    # 3. 检查初始状态
    print(f"📊 初始状态:")
    print(f"   状态: {selector.get_status()}")
    print(f"   ROI信息: {selector.get_roi_info()}")
    
    # 4. 显示ROI选择器
    print(f"\n🎯 显示ROI选择器...")
    selector.display()
    
    print(f"\n📋 使用说明:")
    print(f"1. 在上方的ROI选择器中拖动滑块选择感兴趣区域")
    print(f"2. 建议选择区域: X范围 [90, 210], Y范围 [60, 140]")
    print(f"3. 点击 '确认选择' 按钮")
    print(f"4. 运行下面的代码获取结果:")
    print(f"   result = selector.get_result()")
    print(f"   status = selector.get_status()")
    print(f"   roi_info = selector.get_roi_info()")
    
    return selector


def check_selector_result(selector: CutFrameSelector):
    """检查选择器结果"""
    print(f"\n🔍 检查选择器结果...")
    
    # 获取状态
    status = selector.get_status()
    print(f"状态: {status}")
    
    # 获取结果
    result = selector.get_result()
    if result is not None:
        print(f"✅ 裁剪完成!")
        print(f"   裁剪后的3D图像尺寸: {result.shape}")
        print(f"   数据类型: {result.dtype}")
        
        # 获取ROI信息
        roi_info = selector.get_roi_info()
        if roi_info:
            print(f"\n📊 ROI详细信息:")
            print(f"   坐标: {roi_info['coordinates']}")
            print(f"   X范围: {roi_info['x_range']}")
            print(f"   Y范围: {roi_info['y_range']}")
            print(f"   宽度: {roi_info['width']}")
            print(f"   高度: {roi_info['height']}")
            print(f"   面积: {roi_info['area']} 像素")
            print(f"   原始形状: {roi_info['original_shape']}")
            print(f"   裁剪后形状: {roi_info['cropped_shape']}")
        
        # 显示一些统计信息
        print(f"\n📈 裁剪结果统计:")
        print(f"   最小值: {result.min()}")
        print(f"   最大值: {result.max()}")
        print(f"   平均值: {result.mean():.2f}")
        print(f"   标准差: {result.std():.2f}")
        
        return result
    else:
        print("⏳ ROI选择尚未完成，请先在选择器中确认选择")
        return None


def example_advanced_usage():
    """高级使用示例"""
    print("\n🔧 CutFrameSelector 高级使用示例")
    print("=" * 40)
    
    # 创建数据
    img2d, img3d = create_sample_data()
    
    # 创建选择器
    selector = CutFrameSelector(img2d, img3d)
    
    print(f"🎯 高级功能演示:")
    print(f"1. 状态管理: selector.get_status()")
    print(f"2. ROI信息: selector.get_roi_info()")
    print(f"3. 重置功能: selector.reset()")
    print(f"4. 链式调用: CutFrameSelector(img2d, img3d).display()")
    
    # 显示选择器
    selector.display()
    
    return selector


def example_error_handling():
    """错误处理示例"""
    print("\n⚠️ 错误处理示例")
    print("=" * 40)
    
    # 创建不匹配的数据
    img2d = np.zeros((100, 150), dtype=np.uint8)
    img3d = np.zeros((5, 200, 300), dtype=np.uint8)
    
    print(f"测试数据:")
    print(f"   img2d.shape: {img2d.shape}")
    print(f"   img3d.shape: {img3d.shape}")
    
    try:
        selector = CutFrameSelector(img2d, img3d)
        print("❌ 应该抛出异常但没有")
    except ValueError as e:
        print(f"✅ 正确捕获异常: {e}")
    except Exception as e:
        print(f"❌ 意外异常: {e}")


def demonstrate_class_advantages():
    """演示类相比函数的优势"""
    print("\n🌟 CutFrameSelector 类的优势")
    print("=" * 50)
    
    print("""
## 🎯 面向对象的优势

### 1. 更好的状态管理
```python
selector = CutFrameSelector(img2d, img3d)
print(selector.get_status())  # 随时查看状态
```

### 2. 丰富的信息获取
```python
roi_info = selector.get_roi_info()  # 详细的ROI信息
result = selector.get_result()      # 裁剪结果
```

### 3. 灵活的操作控制
```python
selector.reset()        # 重置状态
selector.display()      # 重新显示
```

### 4. 链式调用支持
```python
result = CutFrameSelector(img2d, img3d).display().get_result()
```

### 5. 更好的错误处理
- 构造时验证输入
- 清晰的状态标识
- 详细的异常信息

### 6. 扩展性
- 易于添加新功能
- 支持继承和组合
- 更好的代码组织

## 🔄 向后兼容
仍然支持原有的函数式接口:
```python
# 函数式（向后兼容）
selector = cutFrame(img2d, img3d)
result = get_cutframe_result(selector)

# 面向对象（推荐）
selector = CutFrameSelector(img2d, img3d).display()
result = selector.get_result()
```
""")


if __name__ == "__main__":
    print("🚀 CutFrameSelector 类使用示例")
    print("=" * 50)
    
    # 演示类的优势
    demonstrate_class_advantages()
    
    # 基本使用示例
    selector = example_basic_class_usage()
    
    # 错误处理示例
    example_error_handling()
    
    print(f"\n" + "=" * 50)
    print(f"🎉 示例程序运行完成!")
    print(f"💡 提示: 在Jupyter notebook中运行效果最佳")
    print(f"📖 使用 check_selector_result(selector) 检查结果")
