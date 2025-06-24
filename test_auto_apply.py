#!/usr/bin/env python3
"""
测试自动应用裁剪结果功能
"""

import numpy as np
import sys
import os

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pynbgui.image_sequence_viewer import ImageSequenceViewer


def test_auto_apply_feature():
    """测试自动应用功能"""
    print("🧪 测试自动应用裁剪结果功能")
    print("=" * 50)
    
    # 创建测试序列
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
    
    print(f"\n📋 自动应用测试步骤:")
    print(f"1. 查看器已显示在上方")
    print(f"2. 运行: start_auto_apply_test(viewer)")
    print(f"3. 在ROI选择器中选择区域并点击确认")
    print(f"4. 观察自动应用过程")
    print(f"5. 运行: verify_auto_apply_result(viewer)")
    
    return viewer


def start_auto_apply_test(viewer):
    """开始自动应用测试"""
    print(f"\n🎯 开始自动应用测试...")
    
    # 记录原始状态
    original_shape = viewer.imageSequence.shape
    original_num_images = viewer.numImages
    
    print(f"📊 原始状态:")
    print(f"   序列尺寸: {original_shape}")
    print(f"   帧数: {original_num_images}")
    print(f"   当前帧: {viewer.selectWidget.value}")
    
    # 启动交互式裁剪
    try:
        print(f"\n🚀 启动交互式裁剪（带自动应用）...")
        viewer.crop_sequence_interactive()
        
        print(f"\n✅ 交互式裁剪启动成功!")
        print(f"📋 现在请:")
        print(f"1. 在ROI选择器中选择一个区域")
        print(f"2. 点击 '确认选择' 按钮")
        print(f"3. 观察控制台输出的自动应用过程")
        print(f"4. 然后运行: verify_auto_apply_result(viewer)")
        
        # 存储原始状态供后续验证
        viewer._test_original_shape = original_shape
        viewer._test_original_num_images = original_num_images
        
        return True
        
    except Exception as e:
        print(f"❌ 启动交互式裁剪失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_auto_apply_result(viewer):
    """验证自动应用结果"""
    print(f"\n🔍 验证自动应用结果...")
    
    # 检查是否有原始状态记录
    if not hasattr(viewer, '_test_original_shape'):
        print(f"❌ 没有找到原始状态记录，请先运行 start_auto_apply_test(viewer)")
        return False
    
    original_shape = viewer._test_original_shape
    original_num_images = viewer._test_original_num_images
    
    # 检查当前状态
    current_shape = viewer.imageSequence.shape
    current_num_images = viewer.numImages
    
    print(f"📊 状态对比:")
    print(f"   原始序列尺寸: {original_shape}")
    print(f"   当前序列尺寸: {current_shape}")
    print(f"   原始帧数: {original_num_images}")
    print(f"   当前帧数: {current_num_images}")
    
    # 验证结果
    success = True
    
    # 检查帧数是否保持不变
    if current_num_images == original_num_images:
        print(f"✅ 帧数保持不变: {current_num_images}")
    else:
        print(f"❌ 帧数发生变化: {original_num_images} -> {current_num_images}")
        success = False
    
    # 检查是否发生了裁剪
    if (current_shape[1] < original_shape[1] or current_shape[2] < original_shape[2]):
        print(f"✅ 图像尺寸已裁剪")
        print(f"   高度: {original_shape[1]} -> {current_shape[1]}")
        print(f"   宽度: {original_shape[2]} -> {current_shape[2]}")
    else:
        print(f"⚠️ 图像尺寸未改变，可能未进行裁剪")
    
    # 检查crop_selector是否已清理
    if hasattr(viewer, 'crop_selector'):
        print(f"⚠️ crop_selector 仍然存在，可能清理不完整")
        success = False
    else:
        print(f"✅ crop_selector 已正确清理")
    
    # 检查查看器是否正常工作
    try:
        current_image = viewer.getCurrentImage()
        print(f"✅ 查看器功能正常，当前图像尺寸: {current_image.shape}")
    except Exception as e:
        print(f"❌ 查看器功能异常: {e}")
        success = False
    
    # 清理测试状态
    if hasattr(viewer, '_test_original_shape'):
        delattr(viewer, '_test_original_shape')
    if hasattr(viewer, '_test_original_num_images'):
        delattr(viewer, '_test_original_num_images')
    
    if success:
        print(f"\n🎉 自动应用功能验证成功!")
        print(f"   裁剪结果已自动应用到图像序列")
        print(f"   查看器状态正常")
    else:
        print(f"\n❌ 自动应用功能验证失败")
        print(f"   请检查上述问题")
    
    return success


def test_callback_registration():
    """测试回调注册功能"""
    print(f"\n🔧 测试回调注册功能...")
    
    # 创建简单的测试数据
    img2d = np.random.rand(50, 75).astype(np.uint8) * 255
    img3d = np.random.rand(2, 50, 75).astype(np.uint8) * 255
    
    from pynbgui.image_cropper import CutFrameSelector
    
    # 创建选择器
    selector = CutFrameSelector(img2d, img3d)
    
    # 测试回调注册
    callback_called = {'confirm': False, 'cancel': False}
    
    def test_confirm_callback(crop_selector):
        callback_called['confirm'] = True
        print(f"🔔 确认回调被调用")
    
    def test_cancel_callback(crop_selector):
        callback_called['cancel'] = True
        print(f"🔔 取消回调被调用")
    
    # 注册回调
    selector.register_confirm_callback(test_confirm_callback)
    selector.register_cancel_callback(test_cancel_callback)
    
    print(f"✅ 回调注册完成")
    print(f"   确认回调数量: {len(selector.external_confirm_callbacks)}")
    print(f"   取消回调数量: {len(selector.external_cancel_callbacks)}")
    
    # 验证回调列表
    if len(selector.external_confirm_callbacks) == 1:
        print(f"✅ 确认回调注册成功")
    else:
        print(f"❌ 确认回调注册失败")
    
    if len(selector.external_cancel_callbacks) == 1:
        print(f"✅ 取消回调注册成功")
    else:
        print(f"❌ 取消回调注册失败")
    
    return selector


if __name__ == "__main__":
    print("🚀 自动应用裁剪结果功能测试")
    print("=" * 60)
    
    # 测试回调注册
    test_callback_registration()
    
    # 测试自动应用功能
    viewer = test_auto_apply_feature()
    
    print(f"\n" + "=" * 60)
    print(f"🎮 交互式测试流程:")
    print(f"1. start_auto_apply_test(viewer)    # 启动测试")
    print(f"2. [在ROI选择器中选择区域并确认]")
    print(f"3. verify_auto_apply_result(viewer)  # 验证结果")
    
    print(f"\n💡 新功能说明:")
    print(f"现在点击确认按钮后，裁剪结果会自动应用到图像序列，")
    print(f"无需手动调用 check_crop_result() 方法。")
