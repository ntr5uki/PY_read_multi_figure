#!/usr/bin/env python3
"""
简化的测试脚本，验证ImageSequenceViewer和ImageContrastViewer的修复效果
"""

import numpy as np
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试模块导入"""
    print("=== 测试模块导入 ===")
    try:
        from pynbgui.image_sequence_viewer import ImageSequenceViewer
        from pynbgui.image_contrast_viewer import ImageContrastViewer
        print("✓ 成功导入所有模块")
        return ImageSequenceViewer, ImageContrastViewer
    except ImportError as e:
        print(f"❌ 导入模块失败: {e}")
        return None, None

def test_global_range_feature():
    """测试全局灰度范围功能"""
    print("\n=== 测试全局灰度范围功能 ===")
    
    try:
        from pynbgui.image_contrast_viewer import ImageContrastViewer
        
        # 创建测试数据
        test_data = np.random.randint(50, 150, (100, 100)).astype(np.float32)
        global_range = (0.0, 255.0)
        
        # 测试带全局范围的构造函数
        viewer = ImageContrastViewer(test_data, global_range=global_range)
        
        # 验证全局范围设置
        assert hasattr(viewer, 'global_range'), "缺少global_range属性"
        assert viewer.global_range == global_range, f"全局范围设置错误: {viewer.global_range} != {global_range}"
        
        print(f"✓ 全局范围正确设置: {viewer.global_range}")
        
        # 测试updateImageData使用全局范围
        new_data = np.random.randint(100, 200, (100, 100)).astype(np.float32)
        viewer.updateImageData(new_data)
        
        # 验证全局范围未被修改
        assert viewer.global_range == global_range, "updateImageData后全局范围被意外修改"
        
        print("✓ updateImageData正确保持全局范围")
        return True
        
    except Exception as e:
        print(f"❌ 全局范围功能测试失败: {e}")
        return False

def test_image_sequence_global_range():
    """测试ImageSequenceViewer的全局范围计算"""
    print("\n=== 测试ImageSequenceViewer全局范围计算 ===")
    
    try:
        from pynbgui.image_sequence_viewer import ImageSequenceViewer
        
        # 创建具有不同灰度范围的图像序列
        np.random.seed(42)
        image1 = np.random.randint(0, 100, (50, 50)).astype(np.float32)
        image2 = np.random.randint(50, 200, (50, 50)).astype(np.float32)
        image3 = np.random.randint(100, 255, (50, 50)).astype(np.float32)
        
        image_sequence = np.stack([image1, image2, image3], axis=0)
        
        # 创建ImageSequenceViewer
        viewer = ImageSequenceViewer(image_sequence, useRangeSlider=True, showSizeControl=True)
        
        # 验证全局范围计算
        expected_min = float(image_sequence.min())
        expected_max = float(image_sequence.max())
        
        assert hasattr(viewer, 'globalRange'), "缺少globalRange属性"
        actual_min, actual_max = viewer.globalRange
        
        assert abs(actual_min - expected_min) < 1e-6, f"全局最小值错误: {actual_min} != {expected_min}"
        assert abs(actual_max - expected_max) < 1e-6, f"全局最大值错误: {actual_max} != {expected_max}"
        
        print(f"✓ 全局范围计算正确: [{actual_min:.1f}, {actual_max:.1f}]")
        
        # 验证ImageContrastViewer使用了全局范围
        assert viewer.imageViewer.global_range == viewer.globalRange, "ImageContrastViewer未使用全局范围"
        
        print("✓ ImageContrastViewer正确使用全局范围")
        return True
        
    except Exception as e:
        print(f"❌ ImageSequenceViewer全局范围测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_size_slider_integration():
    """测试大小滑块集成"""
    print("\n=== 测试大小滑块集成 ===")
    
    try:
        from pynbgui.image_contrast_viewer import ImageContrastViewer
        
        # 创建测试数据
        test_data = np.random.randint(0, 255, (100, 100)).astype(np.float32)
        viewer = ImageContrastViewer(test_data)
        
        # 模拟创建大小滑块
        viewer.display(useRangeSlider=True, showSizeControl=True)
        
        # 验证大小滑块存在
        assert hasattr(viewer, 'sizeSlider'), "缺少sizeSlider属性"
        
        if viewer.sizeSlider is not None:
            print("✓ 大小滑块创建成功")
            
            # 测试updateImageData中的大小滑块处理
            original_value = viewer.sizeSlider.value
            viewer.sizeSlider.value = 2.0  # 设置缩放倍数
            
            new_data = np.random.randint(0, 255, (100, 100)).astype(np.float32)
            viewer.updateImageData(new_data)
            
            # 验证缩放倍数保持
            assert viewer.sizeSlider.value == 2.0, f"缩放倍数未保持: {viewer.sizeSlider.value} != 2.0"
            
            print("✓ updateImageData正确保持缩放倍数")
        else:
            print("⚠ 大小滑块未创建，跳过相关测试")
        
        return True
        
    except Exception as e:
        print(f"❌ 大小滑块集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("开始测试ImageSequenceViewer和ImageContrastViewer修复效果...\n")
    
    # 测试导入
    ImageSequenceViewer, ImageContrastViewer = test_imports()
    if ImageSequenceViewer is None or ImageContrastViewer is None:
        return False
    
    # 运行各项测试
    tests = [
        test_global_range_feature,
        test_image_sequence_global_range,
        test_size_slider_integration,
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ 测试 {test_func.__name__} 发生异常: {e}")
            results.append(False)
    
    # 汇总结果
    passed = sum(results)
    total = len(results)
    
    print(f"\n{'='*50}")
    if passed == total:
        print(f"🎉 所有测试通过！({passed}/{total})")
        print("修复效果验证成功！")
    else:
        print(f"⚠ 部分测试失败：{passed}/{total} 通过")
    print("="*50)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
