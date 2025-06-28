#!/usr/bin/env python3
"""
测试包安装是否成功
"""

def test_imports():
    """测试所有主要的导入"""
    print("🧪 测试包导入...")
    
    try:
        # 测试主要类的导入
        from pynbgui import InteractiveImageViewer
        print("✅ InteractiveImageViewer 导入成功")
        
        from pynbgui import create_viewer
        print("✅ create_viewer 导入成功")
        
        from pynbgui import create_interactive_viewer
        print("✅ create_interactive_viewer 导入成功")
        
        from pynbgui import ImageSequenceViewer
        print("✅ ImageSequenceViewer 导入成功")
        
        from pynbgui import JupyterArraySelector
        print("✅ JupyterArraySelector 导入成功")
        
        # 测试其他导入
        from pynbgui import H5FileLoader
        print("✅ H5FileLoader 导入成功")
        
        from pynbgui import ImageContrastViewer
        print("✅ ImageContrastViewer 导入成功")
        
        # 测试版本信息
        from pynbgui import __version__
        print(f"✅ 版本信息: {__version__}")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_functionality():
    """测试基本功能"""
    print("\n🔧 测试基本功能...")
    
    try:
        import numpy as np
        from pynbgui import create_viewer
        
        # 创建测试数据
        test_data = np.random.rand(10, 50, 50)
        print(f"✅ 创建测试数据: {test_data.shape}")
        
        # 创建查看器（不显示）
        viewer = create_viewer()
        print("✅ 创建查看器成功")
        
        # 测试获取当前查看器
        current = viewer.get_current_viewer()
        print(f"✅ 获取当前查看器: {current}")
        
        return True
        
    except Exception as e:
        print(f"❌ 功能测试失败: {e}")
        return False

def test_entry_points():
    """测试入口点"""
    print("\n📋 测试入口点...")
    
    try:
        # 尝试使用importlib.metadata（Python 3.8+的标准库）
        try:
            from importlib.metadata import entry_points
            eps = entry_points()
            
            # 查找自定义入口点组
            if hasattr(eps, 'select'):
                # Python 3.10+ 的新API
                pynbgui_eps = eps.select(group='pynbgui')
            else:
                # Python 3.8-3.9 的API
                pynbgui_eps = eps.get('pynbgui', [])
            
            if pynbgui_eps:
                for ep in pynbgui_eps:
                    print(f"✅ 找到入口点: {ep.name} -> {ep.value}")
            else:
                print("⚠️ 没有找到自定义入口点")
                
        except ImportError:
            # 回退到pkg_resources
            import pkg_resources
            entry_points = list(pkg_resources.iter_entry_points('pynbgui'))
            if entry_points:
                for ep in entry_points:
                    print(f"✅ 找到入口点: {ep.name} -> {ep.module_name}:{ep.attrs[0]}")
            else:
                print("⚠️ 没有找到自定义入口点")
            
        return True
        
    except Exception as e:
        print(f"⚠️ 入口点测试跳过: {e}")
        return True  # 不让这个失败影响整体结果

def main():
    """主测试函数"""
    print("📦 测试 py-read-multi-figure 包安装")
    print("=" * 50)
    
    success = True
    
    # 测试导入
    success &= test_imports()
    
    # 测试功能
    success &= test_functionality()
    
    # 测试入口点
    success &= test_entry_points()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 所有测试通过！包安装成功！")
        print("\n📋 在其他项目中的使用方法：")
        print("""
# 方法1: 导入主要类
from pynbgui import InteractiveImageViewer
viewer = InteractiveImageViewer()

# 方法2: 使用便捷函数
from pynbgui import create_viewer
viewer = create_viewer()

# 方法3: 使用完整导入
from pynbgui import create_interactive_viewer
viewer = create_interactive_viewer(useRangeSlider=True, showSizeControl=True)

# 在Jupyter notebook中显示
viewer.display()
        """)
    else:
        print("❌ 测试失败！请检查安装")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 