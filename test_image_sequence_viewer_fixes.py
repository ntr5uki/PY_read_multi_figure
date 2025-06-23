#!/usr/bin/env python3
"""
测试ImageSequenceViewer和ImageContrastViewer修复效果的脚本

测试内容：
1. 图像切换时缩放倍数保持不变
2. 图像序列中所有图像使用相同灰度范围显示
"""

import numpy as np
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from pynbgui.image_sequence_viewer import ImageSequenceViewer
    from pynbgui.image_contrast_viewer import ImageContrastViewer
    print("✓ 成功导入模块")
except ImportError as e:
    print(f"❌ 导入模块失败: {e}")
    sys.exit(1)


def create_test_image_sequence():
    """创建测试用的图像序列，具有不同的灰度范围"""
    # 创建3张不同灰度范围的图像
    np.random.seed(42)  # 确保结果可重现
    
    # 图像1: 灰度范围 0-100
    image1 = np.random.randint(0, 100, (200, 300)).astype(np.float32)
    
    # 图像2: 灰度范围 50-200  
    image2 = np.random.randint(50, 200, (200, 300)).astype(np.float32)
    
    # 图像3: 灰度范围 100-255
    image3 = np.random.randint(100, 255, (200, 300)).astype(np.float32)
    
    # 组合成图像序列
    image_sequence = np.stack([image1, image2, image3], axis=0)
    
    return image_sequence


def test_global_range_consistency():
    """测试全局灰度范围一致性"""
    print("=== 测试全局灰度范围一致性 ===")
    
    # 创建测试图像序列
    image_sequence = create_test_image_sequence()
    
    print(f"图像序列形状: {image_sequence.shape}")
    print(f"图像1灰度范围: [{image_sequence[0].min():.1f}, {image_sequence[0].max():.1f}]")
    print(f"图像2灰度范围: [{image_sequence[1].min():.1f}, {image_sequence[1].max():.1f}]")
    print(f"图像3灰度范围: [{image_sequence[2].min():.1f}, {image_sequence[2].max():.1f}]")
    
    # 创建ImageSequenceViewer
    viewer = ImageSequenceViewer(image_sequence, useRangeSlider=True, showSizeControl=True)
    
    # 检查全局范围计算
    expected_global_min = image_sequence.min()
    expected_global_max = image_sequence.max()
    actual_global_range = viewer.globalRange
    
    print(f"期望全局范围: [{expected_global_min:.1f}, {expected_global_max:.1f}]")
    print(f"实际全局范围: [{actual_global_range[0]:.1f}, {actual_global_range[1]:.1f}]")
    
    # 验证全局范围计算正确
    assert abs(actual_global_range[0] - expected_global_min) < 1e-6, "全局最小值计算错误"
    assert abs(actual_global_range[1] - expected_global_max) < 1e-6, "全局最大值计算错误"
    
    # 验证ImageContrastViewer使用了全局范围
    assert viewer.imageViewer.global_range == actual_global_range, "ImageContrastViewer未使用全局范围"
    
    print("✓ 全局灰度范围一致性测试通过")
    return viewer


def test_size_slider_persistence():
    """测试缩放倍数在图像切换时的保持"""
    print("\n=== 测试缩放倍数保持 ===")
    
    # 创建测试图像序列
    image_sequence = create_test_image_sequence()
    
    # 创建ImageSequenceViewer
    viewer = ImageSequenceViewer(image_sequence, useRangeSlider=True, showSizeControl=True)
    
    # 模拟设置缩放倍数
    test_size_ratio = 2.5
    if viewer.imageViewer.sizeSlider is not None:
        viewer.imageViewer.sizeSlider.value = test_size_ratio
        print(f"设置缩放倍数为: {test_size_ratio}")
        
        # 获取当前图像尺寸
        original_shape = viewer.imageViewer.originalDataDisplay.shape
        current_shape = viewer.imageViewer.dataDisplay.shape
        print(f"原始图像尺寸: {original_shape}")
        print(f"当前图像尺寸: {current_shape}")
        
        # 模拟切换到下一张图像
        print("切换到图像索引1...")
        viewer.selectWidget.value = 1
        
        # 检查缩放倍数是否保持
        new_size_ratio = viewer.imageViewer.sizeSlider.value
        new_shape = viewer.imageViewer.dataDisplay.shape
        
        print(f"切换后缩放倍数: {new_size_ratio}")
        print(f"切换后图像尺寸: {new_shape}")
        
        # 验证缩放倍数保持不变
        assert abs(new_size_ratio - test_size_ratio) < 1e-6, f"缩放倍数未保持，期望{test_size_ratio}，实际{new_size_ratio}"
        
        # 验证图像尺寸符合缩放比例
        expected_height = int(original_shape[0] * test_size_ratio)
        expected_width = int(original_shape[1] * test_size_ratio)
        
        # 允许一定的误差（由于PIL缩放的舍入）
        height_diff = abs(new_shape[0] - expected_height)
        width_diff = abs(new_shape[1] - expected_width)
        
        assert height_diff <= 2, f"图像高度缩放错误，期望约{expected_height}，实际{new_shape[0]}"
        assert width_diff <= 2, f"图像宽度缩放错误，期望约{expected_width}，实际{new_shape[1]}"
        
        print("✓ 缩放倍数保持测试通过")
    else:
        print("⚠ sizeSlider未创建，跳过缩放测试")
    
    return viewer


def test_image_data_update():
    """测试updateImageData方法的修复"""
    print("\n=== 测试updateImageData方法修复 ===")
    
    # 创建测试数据
    test_data1 = np.random.randint(0, 100, (150, 200)).astype(np.float32)
    test_data2 = np.random.randint(150, 255, (150, 200)).astype(np.float32)
    
    # 定义全局范围
    global_range = (0.0, 255.0)
    
    # 创建ImageContrastViewer
    viewer = ImageContrastViewer(test_data1, global_range=global_range)
    
    print(f"初始数据范围: [{test_data1.min():.1f}, {test_data1.max():.1f}]")
    print(f"全局范围: [{global_range[0]:.1f}, {global_range[1]:.1f}]")
    print(f"初始显示数据范围: [{viewer.dataDisplay.min()}, {viewer.dataDisplay.max()}]")
    
    # 更新图像数据
    viewer.updateImageData(test_data2)
    
    print(f"新数据范围: [{test_data2.min():.1f}, {test_data2.max():.1f}]")
    print(f"更新后显示数据范围: [{viewer.dataDisplay.min()}, {viewer.dataDisplay.max()}]")
    
    # 验证使用了全局范围而非新数据的范围
    assert viewer.global_range == global_range, "全局范围被意外修改"
    
    # 验证显示数据正确归一化
    expected_min = np.interp(test_data2.min(), global_range, (0, 255))
    expected_max = np.interp(test_data2.max(), global_range, (0, 255))
    
    actual_min = viewer.dataDisplay.min()
    actual_max = viewer.dataDisplay.max()
    
    print(f"期望显示范围: [{expected_min:.1f}, {expected_max:.1f}]")
    print(f"实际显示范围: [{actual_min}, {actual_max}]")
    
    # 允许一定误差（由于uint8转换）
    assert abs(actual_min - expected_min) <= 2, f"显示最小值错误，期望约{expected_min:.1f}，实际{actual_min}"
    assert abs(actual_max - expected_max) <= 2, f"显示最大值错误，期望约{expected_max:.1f}，实际{actual_max}"
    
    print("✓ updateImageData方法修复测试通过")


def main():
    """主测试函数"""
    print("开始测试ImageSequenceViewer和ImageContrastViewer修复效果...\n")
    
    try:
        # 测试1: 全局灰度范围一致性
        viewer1 = test_global_range_consistency()
        
        # 测试2: 缩放倍数保持
        viewer2 = test_size_slider_persistence()
        
        # 测试3: updateImageData方法修复
        test_image_data_update()
        
        print("\n" + "="*50)
        print("🎉 所有测试通过！修复效果验证成功！")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
