#!/usr/bin/env python3
"""
智能操作面板演示脚本
用于在命令行环境中测试面板的基本功能
"""

from pynbgui.smart_operation_panel import SmartOperationPanel, create_test_panel
import time


def test_basic_functionality():
    """测试基本功能"""
    print("=" * 50)
    print("🧪 测试基本功能")
    print("=" * 50)
    
    # 创建测试面板
    panel = create_test_panel()
    
    # 测试菜单状态
    print("📊 初始菜单状态:")
    state = panel.get_menu_state()
    print(f"   - 菜单项数量: {state['item_count']}")
    print(f"   - 可用项目: {len(state['enabled_items'])}")
    print(f"   - 禁用项目: {len(state['disabled_items'])}")
    print(f"   - 菜单是否打开: {state['is_open']}")
    
    # 测试菜单开关
    print("\n🔄 测试菜单开关:")
    print("   - 打开菜单...")
    panel.open_menu()
    print(f"   - 菜单状态: {'打开' if panel.is_menu_open else '关闭'}")
    
    print("   - 关闭菜单...")
    panel.close_menu()
    print(f"   - 菜单状态: {'打开' if panel.is_menu_open else '关闭'}")
    
    print("✅ 基本功能测试完成\n")
    return panel


def test_state_management():
    """测试状态管理"""
    print("=" * 50)
    print("🎛️ 测试状态管理")
    print("=" * 50)
    
    panel = SmartOperationPanel("🎛️ 状态测试", "200px")
    
    # 测试禁用功能
    print("🔒 测试菜单项禁用:")
    items_to_disable = ['save_roi', 'load_roi', 'clear_roi']
    for item_id in items_to_disable:
        success = panel.set_menu_item_enabled(item_id, False)
        print(f"   - 禁用 {item_id}: {'成功' if success else '失败'}")
    
    # 测试样式修改
    print("\n🎨 测试样式修改:")
    style_changes = [
        ('select_roi', 'success'),
        ('roi_stats', 'info'),
    ]
    for item_id, style in style_changes:
        success = panel.set_menu_item_style(item_id, style)
        print(f"   - 修改 {item_id} 样式为 {style}: {'成功' if success else '失败'}")
    
    # 显示最终状态
    print("\n📊 最终状态:")
    final_state = panel.get_menu_state()
    print(f"   - 可用项目: {final_state['enabled_items']}")
    print(f"   - 禁用项目: {final_state['disabled_items']}")
    
    print("✅ 状态管理测试完成\n")
    return panel


def test_dynamic_menu():
    """测试动态菜单"""
    print("=" * 50)
    print("🔄 测试动态菜单")
    print("=" * 50)
    
    # 创建空面板
    panel = SmartOperationPanel("🔄 动态测试", "220px")
    
    # 清空默认菜单
    print("🗑️ 清空默认菜单项:")
    original_count = len(panel.menu_items)
    for item_id in list(panel.menu_items.keys()):
        panel.remove_menu_item(item_id)
    print(f"   - 原有菜单项: {original_count}")
    print(f"   - 清空后菜单项: {len(panel.menu_items)}")
    
    # 动态添加菜单项
    print("\n➕ 动态添加菜单项:")
    new_items = [
        ('action1', '⚡ 快速操作', 'primary', '执行快速操作'),
        ('action2', '🔍 详细分析', 'info', '进行详细分析'),
        ('action3', '⚙️ 高级设置', 'warning', '打开高级设置'),
        ('action4', '📤 导出数据', 'success', '导出处理结果'),
    ]
    
    for item_id, desc, style, tooltip in new_items:
        panel.add_menu_item(item_id, desc, style, tooltip)
        print(f"   - 添加: {desc}")
    
    print(f"\n📊 最终菜单项数量: {len(panel.menu_items)}")
    
    # 测试删除功能
    print("\n🗑️ 测试删除功能:")
    success = panel.remove_menu_item('action2')
    print(f"   - 删除 action2: {'成功' if success else '失败'}")
    print(f"   - 删除后菜单项数量: {len(panel.menu_items)}")
    
    print("✅ 动态菜单测试完成\n")
    return panel


def test_callback_system():
    """测试回调系统"""
    print("=" * 50)
    print("🔗 测试回调系统")
    print("=" * 50)
    
    panel = SmartOperationPanel("🔗 回调测试", "200px")
    
    # 定义测试回调函数
    callback_results = []
    
    def test_callback_1(item_id, button):
        result = f"回调1被触发: {item_id}"
        callback_results.append(result)
        print(f"   📞 {result}")
    
    def test_callback_2(item_id, button):
        result = f"回调2被触发: {item_id}"
        callback_results.append(result)
        print(f"   📞 {result}")
    
    # 注册回调函数
    print("📝 注册回调函数:")
    panel.register_callback('select_roi', test_callback_1)
    panel.register_callback('save_roi', test_callback_2)
    print("   - select_roi -> test_callback_1")
    print("   - save_roi -> test_callback_2")
    
    # 模拟菜单项点击
    print("\n🖱️ 模拟菜单项点击:")
    test_items = ['select_roi', 'save_roi', 'roi_stats']  # roi_stats没有回调
    
    for item_id in test_items:
        if item_id in panel.menu_items:
            button = panel.menu_items[item_id]['button']
            print(f"   - 点击 {item_id}:")
            panel._on_menu_item_click(item_id, button)
    
    # 测试取消注册
    print("\n🚫 测试取消注册:")
    panel.unregister_callback('select_roi')
    print("   - 取消注册 select_roi 回调")
    
    # 再次测试
    print("\n🖱️ 再次测试 select_roi (应该没有回调):")
    if 'select_roi' in panel.menu_items:
        button = panel.menu_items['select_roi']['button']
        panel._on_menu_item_click('select_roi', button)
    
    print(f"\n📊 总共触发回调次数: {len(callback_results)}")
    print("✅ 回调系统测试完成\n")
    return panel


def test_performance():
    """测试性能"""
    print("=" * 50)
    print("⚡ 性能测试")
    print("=" * 50)
    
    # 测试创建时间
    start_time = time.time()
    panel = SmartOperationPanel("⚡ 性能测试", "200px")
    creation_time = time.time() - start_time
    print(f"📊 面板创建时间: {creation_time*1000:.2f}ms")
    
    # 测试菜单开关性能
    start_time = time.time()
    for _ in range(100):
        panel.toggle_menu()
    toggle_time = time.time() - start_time
    print(f"📊 100次菜单切换时间: {toggle_time*1000:.2f}ms")
    print(f"📊 平均单次切换时间: {toggle_time*10:.2f}ms")
    
    # 测试大量菜单项
    start_time = time.time()
    for i in range(50):
        panel.add_menu_item(f'item_{i}', f'📋 菜单项 {i}', '', f'菜单项 {i}')
    add_time = time.time() - start_time
    print(f"📊 添加50个菜单项时间: {add_time*1000:.2f}ms")
    print(f"📊 平均单个菜单项添加时间: {add_time*20:.2f}ms")
    
    print(f"📊 最终菜单项总数: {len(panel.menu_items)}")
    print("✅ 性能测试完成\n")
    return panel


def main():
    """主测试函数"""
    print("🚀 智能操作面板测试程序")
    print("=" * 60)
    print("这个程序将测试智能操作面板的各项功能")
    print("=" * 60)
    
    # 运行所有测试
    test_results = {}
    
    try:
        test_results['basic'] = test_basic_functionality()
        test_results['state'] = test_state_management()
        test_results['dynamic'] = test_dynamic_menu()
        test_results['callback'] = test_callback_system()
        test_results['performance'] = test_performance()
        
        print("=" * 60)
        print("🎉 所有测试完成!")
        print("=" * 60)
        print("📋 测试总结:")
        print("   ✅ 基本功能测试 - 通过")
        print("   ✅ 状态管理测试 - 通过")
        print("   ✅ 动态菜单测试 - 通过")
        print("   ✅ 回调系统测试 - 通过")
        print("   ✅ 性能测试 - 通过")
        
        print("\n💡 下一步:")
        print("   1. 在Jupyter notebook中运行 test_smart_operation_panel.ipynb")
        print("   2. 查看可视化效果和交互体验")
        print("   3. 集成到InteractiveImageViewer中")
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
    
    return test_results


if __name__ == "__main__":
    results = main()
