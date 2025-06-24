#!/usr/bin/env python3
"""
测试 SizeControl 对交互式裁剪功能的影响修复
"""

import numpy as np
import sys
import os

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pynbgui.image_sequence_viewer import ImageSequenceViewer


def test_sizecontrol_independence():
    """测试交互式裁剪功能不受SizeControl影响"""
    print("🧪 测试 SizeControl 对交互式裁剪的影响")
    print("=" * 50)
    
    # 创建测试序列
    frames, height, width = 3, 100, 150
    sequence = np.random.rand(frames, height, width).astype(np.uint8) * 255
    
    print(f"✅ 创建测试序列:")
    print(f"   序列尺寸: {sequence.shape}")
    
    # 创建查看器（启用SizeControl）
    viewer = ImageSequenceViewer(sequence, useRangeSlider=True, showSizeControl=True)
    
    print(f"\n📊 初始状态:")
    print(f"   原始序列尺寸: {viewer.imageSequence.shape}")
    print(f"   当前图像尺寸: {viewer.getCurrentImage().shape}")
    
    # 显示查看器
    viewer.display()
    
    print(f"\n🔧 测试步骤:")
    print(f"1. 查看器已显示，注意图像大小滑块")
    print(f"2. 运行: test_different_sizes(viewer)")
    print(f"3. 观察不同大小设置下的行为")
    
    return viewer


def test_different_sizes(viewer):
    """测试不同大小设置下的行为"""
    print(f"\n🔍 测试不同SizeControl设置...")
    
    # 获取原始尺寸
    original_shape = viewer.imageSequence.shape
    original_current = viewer.getCurrentImage().shape
    
    print(f"📊 原始状态:")
    print(f"   序列尺寸: {original_shape}")
    print(f"   当前图像尺寸: {original_current}")
    
    # 检查imageViewer的dataDisplay
    if hasattr(viewer.imageViewer, 'dataDisplay'):
        original_display_shape = viewer.imageViewer.dataDisplay.shape
        print(f"   显示数据尺寸: {original_display_shape}")
    else:
        print(f"   显示数据: 不可用")
    
    # 模拟改变SizeControl（如果可能的话）
    if hasattr(viewer.imageViewer, 'sizeSlider') and viewer.imageViewer.sizeSlider is not None:
        print(f"\n🎛️ 当前大小滑块值: {viewer.imageViewer.sizeSlider.value}")
        
        # 测试不同的大小设置
        test_sizes = [0.5, 2.0, 1.0]  # 50%, 200%, 100%
        
        for size in test_sizes:
            print(f"\n测试大小设置: {size}")
            
            # 设置新的大小
            viewer.imageViewer.sizeSlider.value = size
            
            # 检查各种尺寸
            current_shape = viewer.getCurrentImage().shape
            sequence_shape = viewer.imageSequence.shape
            
            print(f"   序列尺寸: {sequence_shape}")
            print(f"   当前图像尺寸: {current_shape}")
            
            if hasattr(viewer.imageViewer, 'dataDisplay'):
                display_shape = viewer.imageViewer.dataDisplay.shape
                print(f"   显示数据尺寸: {display_shape}")
            
            # 验证getCurrentImage()不受影响
            if current_shape == original_current:
                print(f"   ✅ getCurrentImage() 不受SizeControl影响")
            else:
                print(f"   ❌ getCurrentImage() 受到SizeControl影响")
            
            # 验证序列数据不受影响
            if sequence_shape == original_shape:
                print(f"   ✅ imageSequence 不受SizeControl影响")
            else:
                print(f"   ❌ imageSequence 受到SizeControl影响")
    else:
        print(f"⚠️ SizeControl 不可用，无法测试")
    
    print(f"\n📋 下一步测试:")
    print(f"1. 设置不同的图像大小")
    print(f"2. 运行: test_crop_with_different_sizes(viewer)")


def test_crop_with_different_sizes(viewer):
    """测试在不同大小设置下的裁剪功能"""
    print(f"\n🎯 测试不同大小设置下的裁剪功能...")
    
    if hasattr(viewer.imageViewer, 'sizeSlider') and viewer.imageViewer.sizeSlider is not None:
        # 设置一个非1.0的大小
        viewer.imageViewer.sizeSlider.value = 0.7
        print(f"设置图像大小为: {viewer.imageViewer.sizeSlider.value}")
        
        # 检查当前状态
        print(f"\n📊 当前状态:")
        print(f"   序列尺寸: {viewer.imageSequence.shape}")
        print(f"   当前图像尺寸: {viewer.getCurrentImage().shape}")
        
        if hasattr(viewer.imageViewer, 'dataDisplay'):
            print(f"   显示数据尺寸: {viewer.imageViewer.dataDisplay.shape}")
        
        # 尝试启动交互式裁剪
        try:
            print(f"\n🚀 启动交互式裁剪...")
            viewer.crop_sequence_interactive()
            
            print(f"✅ 交互式裁剪启动成功!")
            print(f"📋 现在可以:")
            print(f"1. 在ROI选择器中选择区域")
            print(f"2. 点击确认按钮")
            print(f"3. 运行: check_crop_result_with_size(viewer)")
            
            return True
            
        except Exception as e:
            print(f"❌ 交互式裁剪启动失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    else:
        print(f"⚠️ SizeControl 不可用")
        return False


def check_crop_result_with_size(viewer):
    """检查在SizeControl设置下的裁剪结果"""
    print(f"\n🔍 检查SizeControl设置下的裁剪结果...")
    
    if hasattr(viewer.imageViewer, 'sizeSlider'):
        print(f"当前大小设置: {viewer.imageViewer.sizeSlider.value}")
    
    # 检查裁剪结果
    success = viewer.check_crop_result()
    
    if success:
        print(f"\n🎉 裁剪成功!")
        print(f"📊 结果验证:")
        print(f"   新序列尺寸: {viewer.imageSequence.shape}")
        print(f"   新当前图像尺寸: {viewer.getCurrentImage().shape}")
        
        # 验证尺寸一致性
        seq_height, seq_width = viewer.imageSequence.shape[1], viewer.imageSequence.shape[2]
        curr_height, curr_width = viewer.getCurrentImage().shape
        
        if seq_height == curr_height and seq_width == curr_width:
            print(f"   ✅ 序列和当前图像尺寸一致")
        else:
            print(f"   ❌ 序列和当前图像尺寸不一致")
            print(f"       序列: {seq_height}x{seq_width}")
            print(f"       当前: {curr_height}x{curr_width}")
        
        return True
    else:
        print(f"❌ 裁剪未完成或失败")
        return False


def test_normalization_method():
    """测试归一化方法的正确性"""
    print(f"\n🔧 测试归一化方法...")
    
    # 创建测试数据
    sequence = np.random.rand(2, 50, 75) * 1000  # 0-1000范围
    viewer = ImageSequenceViewer(sequence)
    
    # 获取当前图像
    current_image = viewer.getCurrentImage()
    print(f"原始图像范围: [{current_image.min():.2f}, {current_image.max():.2f}]")
    
    # 测试归一化
    normalized = viewer._normalize_to_uint8(current_image)
    print(f"归一化后范围: [{normalized.min()}, {normalized.max()}]")
    print(f"归一化后类型: {normalized.dtype}")
    print(f"归一化后尺寸: {normalized.shape}")
    
    # 验证
    if normalized.dtype == np.uint8:
        print(f"✅ 数据类型正确")
    else:
        print(f"❌ 数据类型错误")
    
    if normalized.shape == current_image.shape:
        print(f"✅ 尺寸保持不变")
    else:
        print(f"❌ 尺寸发生变化")
    
    if 0 <= normalized.min() and normalized.max() <= 255:
        print(f"✅ 数值范围正确")
    else:
        print(f"❌ 数值范围错误")


if __name__ == "__main__":
    print("🚀 SizeControl 影响修复测试")
    print("=" * 60)
    
    # 测试归一化方法
    test_normalization_method()
    
    # 测试SizeControl独立性
    viewer = test_sizecontrol_independence()
    
    print(f"\n" + "=" * 60)
    print(f"🎮 交互式测试流程:")
    print(f"1. test_different_sizes(viewer)      # 测试不同大小设置")
    print(f"2. test_crop_with_different_sizes(viewer)  # 测试裁剪功能")
    print(f"3. [在ROI选择器中选择区域并确认]")
    print(f"4. check_crop_result_with_size(viewer)     # 检查结果")
    
    print(f"\n💡 修复说明:")
    print(f"现在交互式裁剪功能使用原始数据进行归一化，")
    print(f"不再受到SizeControl缩放的影响。")
