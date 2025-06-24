#!/usr/bin/env python3
"""
测试 cutFrame 函数的功能
"""

import numpy as np
import sys
import os

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pynbgui.interactive_image_viewer import CutFrameSelector, cutFrame, get_cutframe_result


def test_cutframe_class():
    """测试CutFrameSelector类的功能"""
    print("🧪 开始测试 CutFrameSelector 类...")

    # 创建测试数据
    height, width = 200, 300
    frames = 10

    # 创建2D参考图像（模拟一个简单的图案）
    img2d = np.zeros((height, width), dtype=np.uint8)
    # 添加一些图案
    img2d[50:150, 75:225] = 128  # 中央矩形
    img2d[75:125, 100:200] = 255  # 内部亮区

    # 创建3D图像（每一帧都有不同的强度）
    img3d = np.zeros((frames, height, width), dtype=np.uint8)
    for i in range(frames):
        # 每一帧的强度递增
        intensity = int(255 * (i + 1) / frames)
        img3d[i] = img2d * intensity // 255
        # 添加一些噪声
        noise = np.random.randint(0, 30, (height, width))
        img3d[i] = np.clip(img3d[i] + noise, 0, 255).astype(np.uint8)

    print(f"✅ 测试数据创建完成:")
    print(f"   img2d.shape: {img2d.shape}")
    print(f"   img3d.shape: {img3d.shape}")
    print(f"   img2d数据类型: {img2d.dtype}")
    print(f"   img3d数据类型: {img3d.dtype}")

    # 测试类的创建和基本功能
    print("\n🔍 测试CutFrameSelector类...")
    try:
        # 正确的尺寸
        selector = CutFrameSelector(img2d, img3d)
        print("✅ CutFrameSelector创建成功")

        # 测试状态方法
        print(f"   初始状态: {selector.get_status()}")
        print(f"   ROI信息: {selector.get_roi_info()}")

        # 显示选择器
        selector.display()

        # 错误的尺寸
        wrong_img2d = np.zeros((100, 100), dtype=np.uint8)
        try:
            CutFrameSelector(wrong_img2d, img3d)
            print("❌ 尺寸检查失败 - 应该抛出异常")
        except ValueError as e:
            print(f"✅ 尺寸检查正确抛出异常: {e}")

    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        return None

    print(f"\n🎯 ROI选择器已创建，请在界面中选择ROI区域")
    print(f"   建议选择区域: X范围 [100, 200], Y范围 [75, 125]")
    print(f"   选择完成后，可以使用以下代码获取结果:")
    print(f"   result = selector.get_result()")
    print(f"   status = selector.get_status()")
    print(f"   roi_info = selector.get_roi_info()")

    return selector


def test_cutframe_basic():
    """测试cutFrame函数的基本功能（向后兼容）"""
    print("\n🧪 开始测试 cutFrame 函数（向后兼容）...")

    # 创建测试数据
    height, width = 200, 300
    frames = 10

    # 创建2D参考图像（模拟一个简单的图案）
    img2d = np.zeros((height, width), dtype=np.uint8)
    # 添加一些图案
    img2d[50:150, 75:225] = 128  # 中央矩形
    img2d[75:125, 100:200] = 255  # 内部亮区

    # 创建3D图像（每一帧都有不同的强度）
    img3d = np.zeros((frames, height, width), dtype=np.uint8)
    for i in range(frames):
        # 每一帧的强度递增
        intensity = int(255 * (i + 1) / frames)
        img3d[i] = img2d * intensity // 255
        # 添加一些噪声
        noise = np.random.randint(0, 30, (height, width))
        img3d[i] = np.clip(img3d[i] + noise, 0, 255).astype(np.uint8)

    print(f"✅ 测试数据创建完成:")
    print(f"   img2d.shape: {img2d.shape}")
    print(f"   img3d.shape: {img3d.shape}")
    print(f"   img2d数据类型: {img2d.dtype}")
    print(f"   img3d数据类型: {img3d.dtype}")

    # 测试尺寸检查
    print("\n🔍 测试尺寸检查...")
    try:
        # 正确的尺寸
        roi_selector = cutFrame(img2d, img3d)
        print("✅ 尺寸检查通过")

        # 错误的尺寸
        wrong_img2d = np.zeros((100, 100), dtype=np.uint8)
        try:
            cutFrame(wrong_img2d, img3d)
            print("❌ 尺寸检查失败 - 应该抛出异常")
        except ValueError as e:
            print(f"✅ 尺寸检查正确抛出异常: {e}")

    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        return False

    print(f"\n🎯 ROI选择器已创建，请在界面中选择ROI区域")
    print(f"   建议选择区域: X范围 [100, 200], Y范围 [75, 125]")
    print(f"   选择完成后，可以使用以下代码获取结果:")
    print(f"   result = get_cutframe_result(roi_selector)")
    print(f"   if result is not None:")
    print(f"       print(f'裁剪后的3D图像尺寸: {{result.shape}}')")

    return roi_selector


def test_cutframe_edge_cases():
    """测试cutFrame函数的边界情况"""
    print("\n🧪 测试边界情况...")
    
    # 测试最小尺寸
    small_img2d = np.ones((10, 10), dtype=np.uint8) * 100
    small_img3d = np.ones((5, 10, 10), dtype=np.uint8) * 200
    
    print(f"小尺寸测试:")
    print(f"   img2d.shape: {small_img2d.shape}")
    print(f"   img3d.shape: {small_img3d.shape}")
    
    try:
        roi_selector_small = cutFrame(small_img2d, small_img3d)
        print("✅ 小尺寸图像测试通过")
        return roi_selector_small
    except Exception as e:
        print(f"❌ 小尺寸图像测试失败: {e}")
        return None


def demonstrate_usage():
    """演示cutFrame函数的使用方法"""
    print("\n📖 cutFrame 函数使用演示:")
    print("=" * 50)
    
    print("""
使用步骤:
1. 准备数据:
   - img2d: 2D参考图像，用于ROI选择
   - img3d: 3D图像数据，将根据ROI进行裁剪
   - 要求: img2d.shape[0] == img3d.shape[1] 且 img2d.shape[1] == img3d.shape[2]

2. 调用函数:
   roi_selector = cutFrame(img2d, img3d)

3. 在弹出的ROI选择器中选择感兴趣区域

4. 点击"确认选择"按钮

5. 获取结果:
   result = get_cutframe_result(roi_selector)
   if result is not None:
       print(f'裁剪后的3D图像尺寸: {result.shape}')

注意事项:
- 这是一个异步过程，需要用户交互完成
- 在Jupyter notebook中使用效果最佳
- 如果取消选择，将返回原始的3D图像副本
""")


if __name__ == "__main__":
    print("🚀 CutFrameSelector 类测试程序")
    print("=" * 50)

    # 演示使用方法
    demonstrate_usage()

    # 运行类测试
    selector = test_cutframe_class()

    # 运行向后兼容测试
    roi_selector = test_cutframe_basic()

    # 运行边界情况测试
    roi_selector_small = test_cutframe_edge_cases()

    print("\n" + "=" * 50)
    print("📝 测试完成说明:")
    print("1. 如果在Jupyter notebook中运行，ROI选择器界面应该已经显示")
    print("2. 请在界面中选择ROI区域并点击确认")
    print("3. 使用以下方法获取结果:")
    print("   - 类方式: selector.get_result(), selector.get_status()")
    print("   - 函数方式: get_cutframe_result(roi_selector)")
    print("4. 如果在命令行中运行，可能无法显示交互界面")
