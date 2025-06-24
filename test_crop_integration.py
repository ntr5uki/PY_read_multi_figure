#!/usr/bin/env python3
"""
测试 ImageSequenceViewer 交互式裁剪功能的集成测试
"""

import numpy as np
import sys
import os

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pynbgui.image_sequence_viewer import ImageSequenceViewer


def create_simple_test_sequence():
    """创建简单的测试序列"""
    # 创建一个小尺寸的测试序列，便于快速测试
    frames, height, width = 3, 80, 120
    
    sequence = np.zeros((frames, height, width), dtype=np.uint8)
    
    for i in range(frames):
        frame = np.zeros((height, width), dtype=np.uint8)
        
        # 创建简单的图案
        # 外框
        frame[10:70, 20:100] = 100 + i * 30
        
        # 中央区域
        center_size = 20 + i * 5
        start_y = (height - center_size) // 2
        start_x = (width - center_size) // 2
        frame[start_y:start_y+center_size, start_x:start_x+center_size] = 200
        
        # 内部亮点
        bright_size = 5
        bright_y = height // 2 - bright_size // 2
        bright_x = width // 2 - bright_size // 2
        frame[bright_y:bright_y+bright_size, bright_x:bright_x+bright_size] = 255
        
        sequence[i] = frame
    
    return sequence


def test_crop_integration():
    """集成测试交互式裁剪功能"""
    print("🧪 ImageSequenceViewer 交互式裁剪集成测试")
    print("=" * 50)
    
    # 创建测试序列
    sequence = create_simple_test_sequence()
    
    print(f"✅ 创建测试序列:")
    print(f"   序列尺寸: {sequence.shape}")
    print(f"   数据范围: [{sequence.min()}, {sequence.max()}]")
    
    # 创建查看器
    viewer = ImageSequenceViewer(sequence, useRangeSlider=True)
    
    print(f"\n🚀 创建查看器完成")
    print(f"   查看器序列尺寸: {viewer.imageSequence.shape}")
    print(f"   帧数: {viewer.numImages}")
    
    # 显示查看器
    print(f"\n📺 显示查看器...")
    viewer.display()
    
    print(f"\n📋 测试步骤:")
    print(f"1. 查看器已显示在上方")
    print(f"2. 运行: start_crop_test(viewer)")
    print(f"3. 在ROI选择器中选择区域并确认")
    print(f"4. 运行: finish_crop_test(viewer)")
    
    return viewer


def start_crop_test(viewer):
    """开始裁剪测试"""
    print(f"\n🎯 开始交互式裁剪测试...")
    
    # 显示当前状态
    print(f"📊 当前状态:")
    print(f"   当前帧: {viewer.selectWidget.value}")
    print(f"   序列尺寸: {viewer.imageSequence.shape}")
    
    current_image = viewer.getCurrentImage()
    print(f"   当前图像尺寸: {current_image.shape}")
    print(f"   当前图像范围: [{current_image.min():.1f}, {current_image.max():.1f}]")
    
    # 启动交互式裁剪
    try:
        viewer.crop_sequence_interactive()
        print(f"\n✅ 交互式裁剪启动成功!")
        print(f"📋 下一步:")
        print(f"   1. 在ROI选择器中选择一个区域")
        print(f"   2. 点击 '确认选择' 按钮")
        print(f"   3. 运行: finish_crop_test(viewer)")
        
        return True
        
    except Exception as e:
        print(f"❌ 启动交互式裁剪失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def finish_crop_test(viewer):
    """完成裁剪测试"""
    print(f"\n🔍 检查裁剪结果...")
    
    # 检查裁剪状态
    if hasattr(viewer, 'crop_selector'):
        status = viewer.get_crop_status()
        print(f"裁剪状态: {status}")
        
        # 尝试应用裁剪结果
        success = viewer.check_crop_result()
        
        if success:
            print(f"\n🎉 裁剪测试成功!")
            print(f"📊 最终结果:")
            print(f"   新序列尺寸: {viewer.imageSequence.shape}")
            print(f"   新帧数: {viewer.numImages}")
            
            # 验证裁剪结果
            if viewer.imageSequence.shape[0] == 3:  # 帧数应该保持不变
                print(f"✅ 帧数验证通过")
            else:
                print(f"⚠️ 帧数发生变化")
            
            if viewer.imageSequence.shape[1] < 80 or viewer.imageSequence.shape[2] < 120:
                print(f"✅ 图像尺寸已裁剪")
            else:
                print(f"⚠️ 图像尺寸未改变")
            
            return True
        else:
            print(f"❌ 裁剪未完成或失败")
            return False
    else:
        print(f"❌ 未找到裁剪选择器，请先运行 start_crop_test(viewer)")
        return False


def quick_test():
    """快速完整测试"""
    print(f"\n🚀 快速完整测试")
    print("=" * 30)
    
    # 创建更小的测试序列
    sequence = np.random.rand(2, 50, 75).astype(np.uint8) * 255
    viewer = ImageSequenceViewer(sequence)
    
    print(f"快速测试序列: {sequence.shape}")
    viewer.display()
    
    print(f"\n💡 快速测试说明:")
    print(f"1. 运行: start_crop_test(viewer)")
    print(f"2. 选择任意区域并确认")
    print(f"3. 运行: finish_crop_test(viewer)")
    
    return viewer


def test_method_availability():
    """测试方法可用性"""
    print(f"\n🔧 测试方法可用性...")
    
    sequence = np.random.rand(2, 30, 40).astype(np.uint8) * 255
    viewer = ImageSequenceViewer(sequence)
    
    # 检查新添加的方法是否存在
    methods_to_check = [
        'crop_sequence_interactive',
        'check_crop_result',
        'get_crop_status',
        '_normalize_to_uint8'
    ]
    
    for method_name in methods_to_check:
        if hasattr(viewer, method_name):
            print(f"✅ {method_name} 方法可用")
        else:
            print(f"❌ {method_name} 方法不存在")
    
    # 测试 _normalize_to_uint8 方法
    try:
        test_image = np.random.rand(30, 40) * 1000  # 0-1000范围
        normalized = viewer._normalize_to_uint8(test_image)
        
        if normalized.dtype == np.uint8:
            print(f"✅ _normalize_to_uint8 返回正确的数据类型")
        else:
            print(f"❌ _normalize_to_uint8 返回错误的数据类型: {normalized.dtype}")
        
        if normalized.min() >= 0 and normalized.max() <= 255:
            print(f"✅ _normalize_to_uint8 返回正确的数值范围: [{normalized.min()}, {normalized.max()}]")
        else:
            print(f"❌ _normalize_to_uint8 返回错误的数值范围: [{normalized.min()}, {normalized.max()}]")
            
    except Exception as e:
        print(f"❌ _normalize_to_uint8 测试失败: {e}")


if __name__ == "__main__":
    print("🚀 ImageSequenceViewer 交互式裁剪集成测试")
    print("=" * 60)
    
    # 测试方法可用性
    test_method_availability()
    
    # 运行主要集成测试
    viewer = test_crop_integration()
    
    print(f"\n" + "=" * 60)
    print(f"🎮 交互式测试流程:")
    print(f"1. start_crop_test(viewer)  # 启动裁剪")
    print(f"2. [在ROI选择器中选择区域并确认]")
    print(f"3. finish_crop_test(viewer)  # 完成裁剪")
    
    print(f"\n🚀 或者运行快速测试:")
    print(f"   quick_viewer = quick_test()")
    
    print(f"\n💡 提示: 在Jupyter notebook中运行效果最佳")
