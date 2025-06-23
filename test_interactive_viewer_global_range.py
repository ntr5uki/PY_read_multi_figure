#!/usr/bin/env python3
"""
测试InteractiveImageViewer数据更新时全局灰度范围重新计算的脚本

测试内容：
1. ImageSequenceViewer.updateImageSequence()是否重新计算全局灰度范围
2. 新的全局灰度范围是否正确传递给ImageContrastViewer
3. InteractiveImageViewer通过数组选择器更新数据时的行为
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
        from pynbgui.interactive_image_viewer import InteractiveImageViewer
        print("✓ 成功导入所有模块")
        return ImageSequenceViewer, ImageContrastViewer, InteractiveImageViewer
    except ImportError as e:
        print(f"❌ 导入模块失败: {e}")
        return None, None, None

def test_update_image_sequence_global_range():
    """测试ImageSequenceViewer.updateImageSequence()的全局范围重新计算"""
    print("\n=== 测试updateImageSequence()全局范围重新计算 ===")
    
    try:
        from pynbgui.image_sequence_viewer import ImageSequenceViewer
        
        # 创建初始图像序列（灰度范围 0-100）
        np.random.seed(42)
        initial_sequence = np.random.randint(0, 100, (3, 50, 50)).astype(np.float32)
        
        # 创建ImageSequenceViewer
        viewer = ImageSequenceViewer(initial_sequence, useRangeSlider=True, showSizeControl=True)
        
        # 验证初始全局范围
        initial_global_range = viewer.globalRange
        expected_initial_min = float(initial_sequence.min())
        expected_initial_max = float(initial_sequence.max())
        
        print(f"初始图像序列范围: [{expected_initial_min:.1f}, {expected_initial_max:.1f}]")
        print(f"初始全局范围: [{initial_global_range[0]:.1f}, {initial_global_range[1]:.1f}]")
        
        assert abs(initial_global_range[0] - expected_initial_min) < 1e-6, "初始全局最小值错误"
        assert abs(initial_global_range[1] - expected_initial_max) < 1e-6, "初始全局最大值错误"
        
        # 验证ImageContrastViewer使用了正确的全局范围
        assert viewer.imageViewer.global_range == initial_global_range, "ImageContrastViewer初始全局范围错误"
        
        print("✓ 初始全局范围设置正确")
        
        # 创建新的图像序列（灰度范围 150-255）
        new_sequence = np.random.randint(150, 255, (4, 60, 60)).astype(np.float32)
        
        # 更新图像序列
        viewer.updateImageSequence(new_sequence)
        
        # 验证新的全局范围
        new_global_range = viewer.globalRange
        expected_new_min = float(new_sequence.min())
        expected_new_max = float(new_sequence.max())
        
        print(f"新图像序列范围: [{expected_new_min:.1f}, {expected_new_max:.1f}]")
        print(f"更新后全局范围: [{new_global_range[0]:.1f}, {new_global_range[1]:.1f}]")
        
        # 验证全局范围已更新
        assert abs(new_global_range[0] - expected_new_min) < 1e-6, f"新全局最小值错误: {new_global_range[0]} != {expected_new_min}"
        assert abs(new_global_range[1] - expected_new_max) < 1e-6, f"新全局最大值错误: {new_global_range[1]} != {expected_new_max}"
        
        # 验证ImageContrastViewer的全局范围也已更新
        assert viewer.imageViewer.global_range == new_global_range, f"ImageContrastViewer全局范围未更新: {viewer.imageViewer.global_range} != {new_global_range}"
        
        # 验证全局范围确实发生了变化
        assert new_global_range != initial_global_range, "全局范围应该发生变化但没有变化"
        
        print("✓ updateImageSequence()正确重新计算并更新全局范围")
        return True
        
    except Exception as e:
        print(f"❌ updateImageSequence()全局范围测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_interactive_viewer_data_update():
    """测试InteractiveImageViewer的数据更新机制"""
    print("\n=== 测试InteractiveImageViewer数据更新机制 ===")
    
    try:
        from pynbgui.interactive_image_viewer import InteractiveImageViewer
        
        # 创建InteractiveImageViewer
        interactive_viewer = InteractiveImageViewer(useRangeSlider=True, showSizeControl=True)
        
        # 创建第一个测试数组（灰度范围 0-50）
        array1 = np.random.randint(0, 50, (2, 40, 40)).astype(np.float32)
        
        # 模拟数组选择
        interactive_viewer._on_array_selected("test_array1", array1)
        
        # 验证图像查看器已创建
        assert interactive_viewer.imageViewer is not None, "图像查看器未创建"
        
        # 获取第一次的全局范围
        first_global_range = interactive_viewer.imageViewer.globalRange
        expected_first_min = float(array1.min())
        expected_first_max = float(array1.max())
        
        print(f"第一个数组范围: [{expected_first_min:.1f}, {expected_first_max:.1f}]")
        print(f"第一次全局范围: [{first_global_range[0]:.1f}, {first_global_range[1]:.1f}]")
        
        assert abs(first_global_range[0] - expected_first_min) < 1e-6, "第一次全局最小值错误"
        assert abs(first_global_range[1] - expected_first_max) < 1e-6, "第一次全局最大值错误"
        
        # 创建第二个测试数组（灰度范围 200-255）
        array2 = np.random.randint(200, 255, (3, 50, 50)).astype(np.float32)
        
        # 模拟选择新数组
        interactive_viewer._on_array_selected("test_array2", array2)
        
        # 获取第二次的全局范围
        second_global_range = interactive_viewer.imageViewer.globalRange
        expected_second_min = float(array2.min())
        expected_second_max = float(array2.max())
        
        print(f"第二个数组范围: [{expected_second_min:.1f}, {expected_second_max:.1f}]")
        print(f"第二次全局范围: [{second_global_range[0]:.1f}, {second_global_range[1]:.1f}]")
        
        # 验证全局范围已正确更新
        assert abs(second_global_range[0] - expected_second_min) < 1e-6, "第二次全局最小值错误"
        assert abs(second_global_range[1] - expected_second_max) < 1e-6, "第二次全局最大值错误"
        
        # 验证全局范围确实发生了变化
        assert second_global_range != first_global_range, "全局范围应该发生变化但没有变化"
        
        print("✓ InteractiveImageViewer正确处理数据更新时的全局范围重新计算")
        return True
        
    except Exception as e:
        print(f"❌ InteractiveImageViewer数据更新测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_edge_cases():
    """测试边界情况"""
    print("\n=== 测试边界情况 ===")
    
    try:
        from pynbgui.image_sequence_viewer import ImageSequenceViewer
        
        # 测试2D到3D数组的更新
        initial_2d = np.random.randint(0, 100, (50, 50)).astype(np.float32)
        viewer = ImageSequenceViewer(initial_2d)
        
        initial_range = viewer.globalRange
        print(f"2D数组初始范围: [{initial_range[0]:.1f}, {initial_range[1]:.1f}]")
        
        # 更新为3D数组
        new_3d = np.random.randint(150, 200, (3, 60, 60)).astype(np.float32)
        viewer.updateImageSequence(new_3d)
        
        new_range = viewer.globalRange
        print(f"3D数组更新后范围: [{new_range[0]:.1f}, {new_range[1]:.1f}]")
        
        # 验证范围正确更新
        expected_min = float(new_3d.min())
        expected_max = float(new_3d.max())
        
        assert abs(new_range[0] - expected_min) < 1e-6, "2D到3D更新时全局最小值错误"
        assert abs(new_range[1] - expected_max) < 1e-6, "2D到3D更新时全局最大值错误"
        
        print("✓ 2D到3D数组更新时全局范围正确计算")
        return True
        
    except Exception as e:
        print(f"❌ 边界情况测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("开始测试InteractiveImageViewer数据更新时的全局灰度范围重新计算...\n")
    
    # 测试导入
    ImageSequenceViewer, ImageContrastViewer, InteractiveImageViewer = test_imports()
    if None in [ImageSequenceViewer, ImageContrastViewer, InteractiveImageViewer]:
        return False
    
    # 运行各项测试
    tests = [
        test_update_image_sequence_global_range,
        test_interactive_viewer_data_update,
        test_edge_cases,
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
    
    print(f"\n{'='*60}")
    if passed == total:
        print(f"🎉 所有测试通过！({passed}/{total})")
        print("InteractiveImageViewer数据更新时全局灰度范围重新计算修复成功！")
    else:
        print(f"⚠ 部分测试失败：{passed}/{total} 通过")
    print("="*60)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
