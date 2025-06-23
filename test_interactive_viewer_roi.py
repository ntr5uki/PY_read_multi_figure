#!/usr/bin/env python3
"""
测试InteractiveImageViewer的ROI选择功能

测试内容：
1. ROI按钮的显示和初始状态
2. 按钮的启用/禁用状态管理
3. 与PILROISelector的集成
4. 图像数据获取功能
5. ROI结果处理机制
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
        from pynbgui.interactive_image_viewer import InteractiveImageViewer
        from pynbgui.roi_selector_pil import PILROISelector
        print("✓ 成功导入所有模块")
        return InteractiveImageViewer, PILROISelector
    except ImportError as e:
        print(f"❌ 导入模块失败: {e}")
        return None, None

def test_roi_button_initialization():
    """测试ROI按钮的初始化"""
    print("\n=== 测试ROI按钮初始化 ===")
    
    try:
        from pynbgui.interactive_image_viewer import InteractiveImageViewer
        
        # 创建InteractiveImageViewer
        viewer = InteractiveImageViewer()
        
        # 验证ROI按钮存在
        assert hasattr(viewer, 'roi_button'), "ROI按钮未创建"
        assert viewer.roi_button is not None, "ROI按钮为None"
        
        # 验证按钮初始状态
        assert viewer.roi_button.disabled == True, f"ROI按钮初始状态应该是禁用的，实际为: {viewer.roi_button.disabled}"
        
        # 验证按钮属性
        assert '🎯' in viewer.roi_button.description, f"ROI按钮描述不正确: {viewer.roi_button.description}"
        assert viewer.roi_button.button_style == 'success', f"ROI按钮样式不正确: {viewer.roi_button.button_style}"
        
        print("✓ ROI按钮初始化正确")
        print(f"  - 描述: {viewer.roi_button.description}")
        print(f"  - 初始状态: {'禁用' if viewer.roi_button.disabled else '启用'}")
        print(f"  - 按钮样式: {viewer.roi_button.button_style}")
        
        return True
        
    except Exception as e:
        print(f"❌ ROI按钮初始化测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_roi_button_state_management():
    """测试ROI按钮状态管理"""
    print("\n=== 测试ROI按钮状态管理 ===")
    
    try:
        from pynbgui.interactive_image_viewer import InteractiveImageViewer
        
        # 创建InteractiveImageViewer
        viewer = InteractiveImageViewer()
        
        # 验证初始状态为禁用
        assert viewer.roi_button.disabled == True, "初始状态应该是禁用的"
        print("✓ 初始状态: 禁用")
        
        # 创建测试图像数组
        test_array = np.random.randint(0, 255, (3, 100, 100)).astype(np.uint8)
        
        # 模拟数组选择，应该启用按钮
        viewer._on_array_selected("test_array", test_array)
        
        # 验证按钮已启用
        assert viewer.roi_button.disabled == False, "选择数组后按钮应该被启用"
        print("✓ 选择数组后状态: 启用")
        
        # 清除查看器，应该禁用按钮
        viewer._clear_viewer()
        
        # 验证按钮已禁用
        assert viewer.roi_button.disabled == True, "清除查看器后按钮应该被禁用"
        print("✓ 清除查看器后状态: 禁用")
        
        return True
        
    except Exception as e:
        print(f"❌ ROI按钮状态管理测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_current_display_image_retrieval():
    """测试当前显示图像获取功能"""
    print("\n=== 测试当前显示图像获取 ===")
    
    try:
        from pynbgui.interactive_image_viewer import InteractiveImageViewer
        
        # 创建InteractiveImageViewer
        viewer = InteractiveImageViewer()
        
        # 在没有图像时，应该返回None
        display_image = viewer._get_current_display_image()
        assert display_image is None, "没有图像时应该返回None"
        print("✓ 无图像时正确返回None")
        
        # 创建测试图像数组
        test_array = np.random.randint(50, 200, (2, 80, 120)).astype(np.float32)
        
        # 选择数组
        viewer._on_array_selected("test_array", test_array)
        
        # 获取显示图像
        display_image = viewer._get_current_display_image()
        
        # 验证返回的图像
        assert display_image is not None, "有图像时应该返回图像数据"
        assert isinstance(display_image, np.ndarray), "返回的应该是numpy数组"
        assert display_image.dtype == np.uint8, f"返回的图像应该是uint8类型，实际为: {display_image.dtype}"
        assert display_image.ndim == 2, f"返回的图像应该是2D，实际维度: {display_image.ndim}"
        
        print("✓ 有图像时正确返回图像数据")
        print(f"  - 图像形状: {display_image.shape}")
        print(f"  - 数据类型: {display_image.dtype}")
        print(f"  - 像素值范围: [{display_image.min()}, {display_image.max()}]")
        
        return True
        
    except Exception as e:
        print(f"❌ 当前显示图像获取测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_frame_info_functionality():
    """测试帧信息功能"""
    print("\n=== 测试帧信息功能 ===")
    
    try:
        from pynbgui.interactive_image_viewer import InteractiveImageViewer
        
        # 创建InteractiveImageViewer
        viewer = InteractiveImageViewer()
        
        # 在没有图像时，应该返回空字符串
        frame_info = viewer._get_current_frame_info()
        assert frame_info == "", f"没有图像时应该返回空字符串，实际返回: '{frame_info}'"
        print("✓ 无图像时正确返回空字符串")
        
        # 创建单张图像
        single_image = np.random.randint(0, 255, (100, 100)).astype(np.uint8)
        viewer._on_array_selected("single_image", single_image)
        
        frame_info = viewer._get_current_frame_info()
        assert "单张图像" in frame_info, f"单张图像时应该包含'单张图像'，实际返回: '{frame_info}'"
        print(f"✓ 单张图像时: {frame_info}")
        
        # 创建图像序列
        image_sequence = np.random.randint(0, 255, (5, 100, 100)).astype(np.uint8)
        viewer._on_array_selected("image_sequence", image_sequence)
        
        frame_info = viewer._get_current_frame_info()
        assert "第1帧" in frame_info and "共5帧" in frame_info, f"图像序列时应该包含帧信息，实际返回: '{frame_info}'"
        print(f"✓ 图像序列时: {frame_info}")
        
        return True
        
    except Exception as e:
        print(f"❌ 帧信息功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_roi_result_handling():
    """测试ROI结果处理功能"""
    print("\n=== 测试ROI结果处理功能 ===")
    
    try:
        from pynbgui.interactive_image_viewer import InteractiveImageViewer
        
        # 创建InteractiveImageViewer
        viewer = InteractiveImageViewer()
        
        # 在没有ROI选择器时，应该返回None
        roi_result = viewer.get_last_roi_result()
        assert roi_result is None, "没有ROI选择器时应该返回None"
        print("✓ 无ROI选择器时正确返回None")
        
        # 检查ROI状态
        status = viewer.check_roi_status()
        assert "尚未打开" in status, f"应该显示尚未打开ROI选择器，实际: '{status}'"
        print(f"✓ ROI状态检查: {status}")
        
        # 创建测试图像并选择
        test_array = np.random.randint(0, 255, (100, 100)).astype(np.uint8)
        viewer._on_array_selected("test_array", test_array)
        
        # 验证可以获取显示图像（为ROI选择做准备）
        display_image = viewer._get_current_display_image()
        assert display_image is not None, "应该能够获取显示图像"
        
        print("✓ ROI结果处理功能基础验证通过")
        
        return True
        
    except Exception as e:
        print(f"❌ ROI结果处理功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_layout_integration():
    """测试界面布局集成"""
    print("\n=== 测试界面布局集成 ===")
    
    try:
        from pynbgui.interactive_image_viewer import InteractiveImageViewer
        
        # 创建InteractiveImageViewer
        viewer = InteractiveImageViewer()
        
        # 验证主界面包含ROI按钮
        assert hasattr(viewer, 'main_widget'), "应该有main_widget属性"
        assert viewer.main_widget is not None, "main_widget不应该为None"
        
        # 验证main_widget的子组件
        children = viewer.main_widget.children
        assert len(children) >= 4, f"main_widget应该至少有4个子组件，实际有: {len(children)}"
        
        # 验证ROI按钮在正确位置（第二个位置，索引为1）
        roi_button_found = False
        for i, child in enumerate(children):
            if hasattr(child, 'description') and '🎯' in child.description:
                roi_button_found = True
                print(f"✓ ROI按钮在位置 {i+1}")
                break
        
        assert roi_button_found, "在main_widget中未找到ROI按钮"
        
        print("✓ 界面布局集成正确")
        
        return True
        
    except Exception as e:
        print(f"❌ 界面布局集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("开始测试InteractiveImageViewer的ROI选择功能...\n")
    
    # 测试导入
    InteractiveImageViewer, PILROISelector = test_imports()
    if InteractiveImageViewer is None or PILROISelector is None:
        return False
    
    # 运行各项测试
    tests = [
        test_roi_button_initialization,
        test_roi_button_state_management,
        test_current_display_image_retrieval,
        test_frame_info_functionality,
        test_roi_result_handling,
        test_layout_integration,
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
        print("InteractiveImageViewer的ROI选择功能集成成功！")
        print("\n📝 使用说明:")
        print("1. 创建InteractiveImageViewer实例")
        print("2. 选择numpy数组后，ROI按钮会自动启用")
        print("3. 点击'🎯 选择ROI区域'按钮打开ROI选择器")
        print("4. 在ROI选择器中选择区域并确认")
        print("5. 使用get_last_roi_result()获取选择结果")
    else:
        print(f"⚠ 部分测试失败：{passed}/{total} 通过")
    print("="*60)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
