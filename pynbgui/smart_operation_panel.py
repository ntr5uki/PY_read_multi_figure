#!/usr/bin/env python3
"""
智能操作面板 - 独立测试类
实现类似下拉菜单的操作面板，用于ROI功能整合

特性：
- 主按钮点击展开/收起菜单
- 支持图标和文字的菜单项
- 动态状态管理
- 易于扩展的菜单结构
- 响应式界面设计
"""

import ipywidgets as widgets
from IPython.display import display
from typing import Dict, Callable, Optional, List, Tuple
import time


class SmartOperationPanel:
    """智能操作面板类 - 模拟下拉菜单效果"""
    
    def __init__(self, title: str = "🎯 操作菜单", width: str = "180px"):
        """
        初始化智能操作面板
        
        Args:
            title: 主按钮显示的标题
            width: 面板宽度
        """
        self.title = title
        self.width = width
        self.is_menu_open = False
        self.menu_items: Dict[str, dict] = {}
        self.callbacks: Dict[str, Callable] = {}
        self._preserve_status = False  # 标志位，用于保护状态信息不被覆盖
        
        # 创建界面组件
        self._create_widgets()
        self._setup_callbacks()
        
    def _create_widgets(self):
        """创建界面组件"""
        # 主操作按钮
        self.main_button = widgets.Button(
            description=f'{self.title} ▼',
            button_style='success',
            tooltip='点击展开/收起操作菜单',
            layout=widgets.Layout(
                width=self.width,
                margin='5px 0',
                border='1px solid #28a745',
                border_radius='4px'
            )
        )
        
        # 菜单容器（初始隐藏）
        self.menu_container = widgets.VBox(
            [],  # 初始为空，后续动态添加
            layout=widgets.Layout(
                border='1px solid #ddd',
                border_radius='4px',
                padding='5px',
                margin='0 0 5px 0',
                background_color='#f8f9fa',
                display='none',  # 初始隐藏
                width=self.width
            )
        )
        
        # 状态显示标签
        self.status_label = widgets.HTML(
            value="<i style='color: #6c757d; font-size: 12px;'>点击主按钮展开菜单</i>",
            layout=widgets.Layout(margin='5px 0')
        )
        
        # 主面板容器
        self.panel = widgets.VBox([
            self.main_button,
            self.menu_container,
            self.status_label
        ], layout=widgets.Layout(
            border='1px solid #e9ecef',
            border_radius='6px',
            padding='10px',
            margin='10px',
            background_color='#ffffff'
        ))
        

    
    def add_menu_item(self, item_id: str, description: str, 
                     button_style: str = '', tooltip: str = '', 
                     enabled: bool = True) -> None:
        """
        添加菜单项
        
        Args:
            item_id: 菜单项唯一标识
            description: 按钮显示文字
            button_style: 按钮样式 ('primary', 'success', 'info', 'warning', 'danger', '')
            tooltip: 鼠标悬停提示
            enabled: 是否启用
        """
        # 创建菜单按钮
        menu_button = widgets.Button(
            description=description,
            button_style=button_style,
            tooltip=tooltip,
            disabled=not enabled,
            layout=widgets.Layout(
                width=f'{int(self.width[:-2]) - 20}px',  # 减去padding
                margin='2px 0',
                border_radius='3px'
            )
        )
        
        # 存储菜单项信息
        self.menu_items[item_id] = {
            'button': menu_button,
            'description': description,
            'style': button_style,
            'tooltip': tooltip,
            'enabled': enabled
        }
        
        # 绑定点击事件 - 修复闭包问题
        def create_click_handler(menu_id):
            def handler(btn):
                self._on_menu_item_click(menu_id, btn)
            return handler

        menu_button.on_click(create_click_handler(item_id))
        
        # 更新菜单容器
        self._update_menu_container()
    
    def remove_menu_item(self, item_id: str) -> bool:
        """
        移除菜单项
        
        Args:
            item_id: 要移除的菜单项ID
            
        Returns:
            是否成功移除
        """
        if item_id in self.menu_items:
            del self.menu_items[item_id]
            self._update_menu_container()
            return True
        return False
    
    def set_menu_item_enabled(self, item_id: str, enabled: bool) -> bool:
        """
        设置菜单项启用状态
        
        Args:
            item_id: 菜单项ID
            enabled: 是否启用
            
        Returns:
            是否成功设置
        """
        if item_id in self.menu_items:
            self.menu_items[item_id]['button'].disabled = not enabled
            self.menu_items[item_id]['enabled'] = enabled
            return True
        return False
    
    def set_menu_item_style(self, item_id: str, button_style: str) -> bool:
        """
        设置菜单项样式
        
        Args:
            item_id: 菜单项ID
            button_style: 新的按钮样式
            
        Returns:
            是否成功设置
        """
        if item_id in self.menu_items:
            self.menu_items[item_id]['button'].button_style = button_style
            self.menu_items[item_id]['style'] = button_style
            return True
        return False
    
    def _update_menu_container(self):
        """更新菜单容器内容"""
        menu_buttons = [item['button'] for item in self.menu_items.values()]
        self.menu_container.children = menu_buttons
    
    def _setup_callbacks(self):
        """设置回调函数"""
        self.main_button.on_click(self._on_main_button_click)
    
    def _on_main_button_click(self, button):
        """主按钮点击处理"""
        self.toggle_menu()
    
    def _on_menu_item_click(self, item_id: str, button):
        """菜单项点击处理"""
        # 更新状态显示
        item_desc = self.menu_items[item_id]['description']
        timestamp = time.strftime("%H:%M:%S")
        self.status_label.value = f"<span style='color: #28a745;'>[{timestamp}] 点击了: {item_desc}</span>"

        # 调用注册的回调函数
        if item_id in self.callbacks:
            try:
                # 创建输出捕获器来捕获print输出
                import io
                import sys
                from contextlib import redirect_stdout

                # 捕获回调函数的输出
                output_buffer = io.StringIO()
                with redirect_stdout(output_buffer):
                    self.callbacks[item_id](item_id, button)

                # 获取捕获的输出
                callback_output = output_buffer.getvalue().strip()

                # 如果有输出，显示在状态标签中并设置保护标志
                if callback_output:
                    # 只显示第一行输出，避免界面过于拥挤
                    first_line = callback_output.split('\n')[0]
                    self.status_label.value = f"<span style='color: #28a745;'>[{timestamp}] {first_line}</span>"
                    self._preserve_status = True  # 保护这个状态信息

            except Exception as e:
                self.status_label.value = f"<span style='color: #dc3545;'>回调函数执行错误: {str(e)}</span>"
                self._preserve_status = True  # 保护错误信息

        # 点击菜单项后自动收起菜单
        self.close_menu()
    
    def toggle_menu(self):
        """切换菜单显示状态"""
        if self.is_menu_open:
            self.close_menu()
        else:
            self.open_menu()
    
    def open_menu(self):
        """打开菜单"""
        self.is_menu_open = True
        self.menu_container.layout.display = 'block'
        self.main_button.description = f'{self.title} ▲'
        self.main_button.button_style = 'info'
        self.status_label.value = "<i style='color: #17a2b8; font-size: 12px;'>菜单已展开，请选择操作</i>"
    
    def close_menu(self):
        """关闭菜单"""
        self.is_menu_open = False
        self.menu_container.layout.display = 'none'
        self.main_button.description = f'{self.title} ▼'
        self.main_button.button_style = 'success'

        # 只有在没有重要信息需要保护时才显示"菜单已收起"
        if not self._preserve_status:
            # 检查是否有重要信息（点击信息、错误信息）
            current_value = self.status_label.value
            if ("点击了:" not in current_value and
                "回调函数执行错误" not in current_value):
                self.status_label.value = "<i style='color: #6c757d; font-size: 12px;'>菜单已收起</i>"

        # 重置保护标志（下次菜单操作时重新判断）
        self._preserve_status = False
    
    def register_callback(self, item_id: str, callback: Callable):
        """
        注册菜单项回调函数
        
        Args:
            item_id: 菜单项ID
            callback: 回调函数，接收(item_id, button)参数
        """
        self.callbacks[item_id] = callback
    
    def unregister_callback(self, item_id: str):
        """取消注册回调函数"""
        if item_id in self.callbacks:
            del self.callbacks[item_id]
    
    def get_menu_state(self) -> dict:
        """获取菜单状态信息"""
        return {
            'is_open': self.is_menu_open,
            'item_count': len(self.menu_items),
            'enabled_items': [id for id, item in self.menu_items.items() if item['enabled']],
            'disabled_items': [id for id, item in self.menu_items.items() if not item['enabled']]
        }
    
    def display(self):
        """显示操作面板"""
        display(self.panel)
        return self


# 测试和演示函数
def create_test_panel() -> SmartOperationPanel:
    """创建测试面板"""
    panel = SmartOperationPanel("🎯 ROI操作", "200px")

    # 手动添加ROI相关菜单项
    roi_menu_items = [
        ('select_roi', '🎯 选择ROI区域', 'primary', '选择感兴趣区域'),
        ('save_roi', '💾 保存当前ROI', '', '保存当前ROI设置'),
        ('load_roi', '📂 加载预设ROI', '', '从预设中加载ROI'),
        ('roi_stats', '📊 ROI统计信息', 'info', '显示ROI区域统计'),
        ('clear_roi', '🗑️ 清除ROI', 'warning', '清除当前ROI设置')
    ]

    for item_id, description, style, tooltip in roi_menu_items:
        panel.add_menu_item(item_id, description, style, tooltip)

    # 注册一些测试回调函数
    def roi_select_callback(item_id, button):
        print(f"🎯 执行ROI选择操作 - ID: {item_id}")

    def roi_save_callback(item_id, button):
        print(f"💾 执行ROI保存操作 - ID: {item_id}")

    def roi_stats_callback(item_id, button):
        print(f"📊 显示ROI统计信息 - ID: {item_id}")

    # 注册回调函数
    panel.register_callback('select_roi', roi_select_callback)
    panel.register_callback('save_roi', roi_save_callback)
    panel.register_callback('roi_stats', roi_stats_callback)

    return panel


def demo_state_management():
    """演示状态管理功能"""
    print("=== 智能操作面板状态管理演示 ===")

    panel = create_test_panel()

    # 演示状态管理
    print("1. 初始状态:")
    print(f"   菜单状态: {panel.get_menu_state()}")

    # 禁用某些按钮（确保菜单项存在）
    if 'save_roi' in panel.menu_items:
        panel.set_menu_item_enabled('save_roi', False)
        print("   - 禁用 save_roi: 成功")
    if 'load_roi' in panel.menu_items:
        panel.set_menu_item_enabled('load_roi', False)
        print("   - 禁用 load_roi: 成功")
    print("2. 禁用保存和加载按钮后:")
    print(f"   菜单状态: {panel.get_menu_state()}")

    # 修改按钮样式（确保菜单项存在）
    if 'select_roi' in panel.menu_items:
        panel.set_menu_item_style('select_roi', 'success')
        print("   - 修改 select_roi 样式: 成功")
    if 'clear_roi' in panel.menu_items:
        panel.set_menu_item_style('clear_roi', 'danger')
        print("   - 修改 clear_roi 样式: 成功")
    print("3. 修改按钮样式后完成")

    return panel


def demo_dynamic_menu():
    """演示动态菜单功能"""
    print("=== 动态菜单演示 ===")

    # 创建空的动态面板（现在默认就是空的）
    panel = SmartOperationPanel("🔧 动态菜单", "220px")

    # 动态添加菜单项
    dynamic_items = [
        ('action1', '⚡ 快速操作', 'primary', '执行快速操作'),
        ('action2', '🔍 详细分析', 'info', '进行详细分析'),
        ('action3', '⚙️ 高级设置', 'warning', '打开高级设置'),
    ]

    for item_id, desc, style, tooltip in dynamic_items:
        panel.add_menu_item(item_id, desc, style, tooltip)

    print("动态菜单创建完成，包含3个自定义菜单项")
    return panel


if __name__ == "__main__":
    print("智能操作面板测试程序")
    print("=" * 40)
    
    # 基础功能测试
    print("\n1. 创建基础测试面板:")
    test_panel = create_test_panel()
    
    # 状态管理测试
    print("\n2. 状态管理测试:")
    state_panel = demo_state_management()
    
    # 动态菜单测试
    print("\n3. 动态菜单测试:")
    dynamic_panel = demo_dynamic_menu()
    
    print("\n测试完成！在Jupyter notebook中运行以下代码查看效果:")
    print("panel = create_test_panel()")
    print("panel.display()")
