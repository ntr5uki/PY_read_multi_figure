#!/usr/bin/env python3
"""
CutFrameSelector 类的单元测试
"""

import numpy as np
import sys
import os

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pynbgui.interactive_image_viewer import CutFrameSelector


def test_class_initialization():
    """测试类的初始化"""
    print("🧪 测试 CutFrameSelector 类初始化...")
    
    # 创建兼容的测试数据
    img2d = np.random.rand(100, 150).astype(np.uint8) * 255
    img3d = np.random.rand(5, 100, 150).astype(np.uint8) * 255
    
    # 测试正常初始化
    try:
        selector = CutFrameSelector(img2d, img3d)
        print("✅ 类初始化成功")
        
        # 检查初始状态
        assert selector.get_result() is None, "初始结果应该为None"
        assert selector.get_roi_info() is None, "初始ROI信息应该为None"
        assert "等待用户选择" in selector.get_status(), "初始状态应该是等待选择"
        assert not selector.is_completed, "初始状态不应该是完成"
        assert not selector.is_cancelled, "初始状态不应该是取消"
        
        print("✅ 初始状态检查通过")
        
    except Exception as e:
        print(f"❌ 类初始化失败: {e}")
        return False
    
    # 测试尺寸不匹配的情况
    try:
        wrong_img2d = np.random.rand(50, 75).astype(np.uint8) * 255
        CutFrameSelector(wrong_img2d, img3d)
        print("❌ 应该抛出尺寸不匹配异常")
        return False
    except ValueError as e:
        print(f"✅ 正确捕获尺寸不匹配异常: {e}")
    
    return True


def test_class_methods():
    """测试类的方法"""
    print("\n🧪 测试 CutFrameSelector 类方法...")
    
    # 创建测试数据
    img2d = np.random.rand(100, 150).astype(np.uint8) * 255
    img3d = np.random.rand(5, 100, 150).astype(np.uint8) * 255
    
    try:
        selector = CutFrameSelector(img2d, img3d)
        
        # 测试链式调用
        result = selector.display()
        assert result is selector, "display()应该返回self"
        print("✅ 链式调用测试通过")
        
        # 测试重置功能
        selector.reset()
        assert selector.get_result() is None, "重置后结果应该为None"
        assert not selector.is_completed, "重置后不应该是完成状态"
        assert not selector.is_cancelled, "重置后不应该是取消状态"
        print("✅ 重置功能测试通过")
        
        # 测试状态获取
        status = selector.get_status()
        assert isinstance(status, str), "状态应该是字符串"
        assert len(status) > 0, "状态字符串不应该为空"
        print("✅ 状态获取测试通过")
        
        return True
        
    except Exception as e:
        print(f"❌ 方法测试失败: {e}")
        return False


def test_data_integrity():
    """测试数据完整性"""
    print("\n🧪 测试数据完整性...")
    
    # 创建测试数据
    img2d = (np.random.rand(100, 150) * 255).astype(np.uint8)
    img3d = (np.random.rand(5, 100, 150) * 255).astype(np.uint8)
    
    # 保存原始数据的副本
    original_img2d = img2d.copy()
    original_img3d = img3d.copy()
    
    try:
        selector = CutFrameSelector(img2d, img3d)
        
        # 修改原始数据
        img2d[:] = 255  # 设置为明显不同的值
        img3d[:] = 255
        
        # 检查选择器内部的数据是否不受影响
        assert not np.array_equal(selector.img2d, img2d), "内部2D数据应该是独立副本"
        assert not np.array_equal(selector.img3d, img3d), "内部3D数据应该是独立副本"
        assert np.array_equal(selector.img2d, original_img2d), "内部2D数据应该保持原始值"
        assert np.array_equal(selector.img3d, original_img3d), "内部3D数据应该保持原始值"
        
        print("✅ 数据完整性测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 数据完整性测试失败: {e}")
        return False


def test_edge_cases():
    """测试边界情况"""
    print("\n🧪 测试边界情况...")
    
    try:
        # 测试最小尺寸
        small_img2d = np.ones((2, 3), dtype=np.uint8) * 100
        small_img3d = np.ones((1, 2, 3), dtype=np.uint8) * 200
        
        selector = CutFrameSelector(small_img2d, small_img3d)
        print("✅ 最小尺寸测试通过")
        
        # 测试大尺寸
        large_img2d = np.random.rand(1000, 1500).astype(np.uint8) * 255
        large_img3d = np.random.rand(10, 1000, 1500).astype(np.uint8) * 255
        
        selector = CutFrameSelector(large_img2d, large_img3d)
        print("✅ 大尺寸测试通过")
        
        # 测试单帧3D图像
        single_frame_img3d = np.random.rand(1, 100, 150).astype(np.uint8) * 255
        img2d = np.random.rand(100, 150).astype(np.uint8) * 255
        
        selector = CutFrameSelector(img2d, single_frame_img3d)
        print("✅ 单帧3D图像测试通过")
        
        return True
        
    except Exception as e:
        print(f"❌ 边界情况测试失败: {e}")
        return False


def run_all_tests():
    """运行所有测试"""
    print("🚀 CutFrameSelector 类单元测试")
    print("=" * 50)
    
    tests = [
        test_class_initialization,
        test_class_methods,
        test_data_integrity,
        test_edge_cases
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ 测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！")
        return True
    else:
        print("❌ 部分测试失败")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    
    if success:
        print("\n💡 提示: 类已准备好在Jupyter notebook中使用")
        print("📖 运行 cutframe_class_example.py 查看使用示例")
    else:
        print("\n⚠️ 请检查失败的测试并修复问题")
    
    sys.exit(0 if success else 1)
