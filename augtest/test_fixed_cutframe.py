#!/usr/bin/env python3
"""
测试修复后的 CutFrameSelector
"""

import numpy as np
import sys
import os

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pynbgui.interactive_image_viewer import CutFrameSelector


def create_test_data():
    """创建测试数据"""
    # 创建一个有明显特征的2D图像
    img2d = np.zeros((100, 150), dtype=np.uint8)
    
    # 添加一些图案
    img2d[20:80, 30:120] = 100   # 外框
    img2d[40:60, 60:90] = 200    # 中央矩形
    img2d[45:55, 70:80] = 255    # 内部亮点
    
    # 创建对应的3D图像
    frames = 5
    img3d = np.zeros((frames, 100, 150), dtype=np.uint8)
    
    for i in range(frames):
        # 每一帧强度不同
        intensity = 0.4 + 0.6 * (i / (frames - 1))
        img3d[i] = (img2d * intensity).astype(np.uint8)
        
        # 添加一些噪声
        noise = np.random.randint(0, 10, (100, 150))
        img3d[i] = np.clip(img3d[i] + noise, 0, 255).astype(np.uint8)
    
    return img2d, img3d


def test_fixed_cutframe():
    """测试修复后的功能"""
    print("🎯 测试修复后的 CutFrameSelector")
    print("=" * 50)
    
    # 创建测试数据
    img2d, img3d = create_test_data()
    
    print(f"✅ 创建测试数据:")
    print(f"   2D图像尺寸: {img2d.shape}")
    print(f"   3D图像尺寸: {img3d.shape}")
    print(f"   数据类型: {img2d.dtype}, {img3d.dtype}")
    
    # 创建选择器
    selector = CutFrameSelector(img2d, img3d)
    
    print(f"\n📊 初始状态:")
    print(f"   状态: {selector.get_status()}")
    print(f"   结果: {selector.get_result()}")
    
    # 显示选择器
    print(f"\n🎯 显示ROI选择器...")
    selector.display()
    
    print(f"\n📋 使用说明:")
    print(f"1. 在上方的ROI选择器中选择感兴趣区域")
    print(f"2. 建议选择包含中央矩形的区域，例如:")
    print(f"   - X范围: [60, 90] (包含中央矩形)")
    print(f"   - Y范围: [40, 60] (包含中央矩形)")
    print(f"3. 点击 '确认选择' 按钮")
    print(f"4. 然后运行检查函数:")
    print(f"   check_result(selector)")
    
    return selector


def check_result(selector):
    """检查选择结果"""
    print(f"\n🔍 检查选择结果...")
    
    # 获取状态和结果
    status = selector.get_status()
    result = selector.get_result()
    roi_info = selector.get_roi_info()
    
    print(f"当前状态: {status}")
    
    if result is not None:
        print(f"\n✅ 成功获取裁剪结果!")
        print(f"   原始3D图像尺寸: {selector.img3d.shape}")
        print(f"   裁剪后3D图像尺寸: {result.shape}")
        print(f"   数据类型: {result.dtype}")
        
        if roi_info:
            print(f"\n📊 ROI详细信息:")
            coords = roi_info['coordinates']
            print(f"   ROI坐标: {coords}")
            print(f"   X范围: {roi_info['x_range']}")
            print(f"   Y范围: {roi_info['y_range']}")
            print(f"   宽度: {roi_info['width']} 像素")
            print(f"   高度: {roi_info['height']} 像素")
            print(f"   面积: {roi_info['area']} 像素")
            
            # 验证裁剪尺寸
            expected_height = roi_info['height']
            expected_width = roi_info['width']
            actual_height, actual_width = result.shape[1], result.shape[2]
            
            if actual_height == expected_height and actual_width == expected_width:
                print(f"✅ 裁剪尺寸验证通过")
            else:
                print(f"⚠️ 裁剪尺寸不匹配:")
                print(f"   期望: {expected_height} x {expected_width}")
                print(f"   实际: {actual_height} x {actual_width}")
        
        # 显示一些统计信息
        print(f"\n📈 裁剪结果统计:")
        print(f"   最小值: {result.min()}")
        print(f"   最大值: {result.max()}")
        print(f"   平均值: {result.mean():.2f}")
        print(f"   标准差: {result.std():.2f}")
        
        # 计算压缩比
        original_size = selector.img3d.size
        cropped_size = result.size
        compression_ratio = cropped_size / original_size
        
        print(f"\n📏 尺寸比较:")
        print(f"   原始数据大小: {original_size:,} 像素")
        print(f"   裁剪后大小: {cropped_size:,} 像素")
        print(f"   保留比例: {compression_ratio:.2%}")
        print(f"   节省空间: {(1-compression_ratio):.2%}")
        
        return True
        
    else:
        print(f"❌ 结果仍然是 None")
        print(f"   请确保:")
        print(f"   1. 已经在ROI选择器中选择了区域")
        print(f"   2. 点击了 '确认选择' 按钮")
        print(f"   3. 等待几秒钟让回调完成")
        
        return False


def quick_test():
    """快速测试（小尺寸）"""
    print(f"\n🚀 快速测试（小尺寸）")
    print("=" * 30)
    
    # 创建小尺寸测试数据
    img2d = np.random.rand(50, 75).astype(np.uint8) * 255
    img3d = np.random.rand(3, 50, 75).astype(np.uint8) * 255
    
    print(f"小尺寸测试数据:")
    print(f"   img2d.shape: {img2d.shape}")
    print(f"   img3d.shape: {img3d.shape}")
    
    # 创建选择器
    selector = CutFrameSelector(img2d, img3d)
    selector.display()
    
    print(f"\n💡 快速测试提示:")
    print(f"   选择任意区域并确认，然后运行:")
    print(f"   check_result(selector)")
    
    return selector


if __name__ == "__main__":
    print("🎉 CutFrameSelector 修复验证")
    print("=" * 50)
    print("现在回调功能已经修复，按下确认按钮后应该能正常获取结果！")
    
    # 运行主测试
    selector = test_fixed_cutframe()
    
    print(f"\n" + "=" * 50)
    print(f"🎮 测试完成后的操作:")
    print(f"1. 选择ROI区域并点击确认")
    print(f"2. 运行: check_result(selector)")
    print(f"3. 或者运行快速测试: quick_test()")
