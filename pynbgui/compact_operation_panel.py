#!/usr/bin/env python3
"""
紧凑型操作面板 - 专为集成到InteractiveImageViewer设计
优化了界面布局，减少空间占用，适合水平排列
"""

import ipywidgets as widgets
from typing import Dict, Callable
import io
from contextlib import redirect_stdout


class CompactOperationPanel:
    """
    紧凑型操作面板，专为集成设计
    - 移除状态标签，减少界面占用
    - 优化布局，适合水平排列
    - 保持完整的回调功能
    """
    
    def __init__(self, title: str = "操作", width: str = "auto"):
        """
        初始化紧凑型操作面板

        Args:
            title: 主按钮显示的标题
            width: 面板宽度（推荐使用'auto'以避免横向滚动条）
        """
        self.title = title
        self.width = width
        self.is_menu_open = False
        self.menu_items: Dict[str, dict] = {}
        self.callbacks: Dict[str, Callable] = {}
        self._preserve_status = False

        # 创建界面组件
        self._create_widgets()
        self._setup_callbacks()
        
    def _create_widgets(self):
        """创建界面组件"""
        # 主操作按钮 - 更紧凑的样式
        self.main_button = widgets.Button(
            description=f'{self.title} ▼',
            button_style='info',
            tooltip=f'点击展开/收起{self.title}菜单',
            layout=widgets.Layout(
                width='auto',  # 自动宽度
                flex='1 1 auto', # 允许增长和收缩
                height='32px',  # 固定高度
                margin='0px',
                border='1px solid #17a2b8',
                border_radius='3px'
            )
        )
        
        # 菜单容器 - 更紧凑的样式
        self.menu_container = widgets.VBox(
            [],
            layout=widgets.Layout(
                border='1px solid #ddd',
                border_radius='3px',
                padding='3px',
                margin='0',
                background_color='#f8f9fa',
                display='none',
                width='auto', # 自动宽度
                max_height='200px',  # 限制最大高度
                overflow='auto'  # 超出时滚动
            )
        )
        
        # 主面板容器 - 最小化边距和内边距
        self.panel = widgets.VBox([ # 使用VBox来包裹，因为main_button和menu_container是垂直排列的
            self.main_button,
            self.menu_container
        ], layout=widgets.Layout(
            margin='0px',
            padding='0px',
            width='auto', # 自动宽度
            flex='1 1 auto' # 允许增长和收缩
        ))
        
    def add_menu_item(self, item_id: str, description: str, 
                     button_style: str = '', tooltip: str = '', 
                     enabled: bool = True) -> None:
        """
        添加菜单项
        
        Args:
            item_id: 菜单项唯一标识
            description: 按钮显示文字
            button_style: 按钮样式
            tooltip: 鼠标悬停提示
            enabled: 是否启用
        """
        # 创建菜单按钮 - 紧凑样式，自适应宽度
        menu_button = widgets.Button(
            description=description,
            button_style=button_style,
            tooltip=tooltip,
            disabled=not enabled,
            layout=widgets.Layout(
                width='auto',       # 自动宽度
                flex='1 1 auto',    # 允许增长和收缩
                height='28px',     # 固定高度
                margin='0px',
                border_radius='2px',
                font_size='11px'   # 更小字体
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
        
        # 绑定点击事件
        def create_click_handler(menu_id):
            def handler(btn):
                self._on_menu_item_click(menu_id, btn)
            return handler
        
        menu_button.on_click(create_click_handler(item_id))
        
        # 更新菜单容器
        self._update_menu_container()
    
    def remove_menu_item(self, item_id: str) -> bool:
        """移除菜单项"""
        if item_id in self.menu_items:
            del self.menu_items[item_id]
            self._update_menu_container()
            return True
        return False
    
    def set_menu_item_enabled(self, item_id: str, enabled: bool) -> bool:
        """设置菜单项启用状态"""
        if item_id in self.menu_items:
            self.menu_items[item_id]['button'].disabled = not enabled
            self.menu_items[item_id]['enabled'] = enabled
            return True
        return False
    
    def set_menu_item_style(self, item_id: str, button_style: str) -> bool:
        """设置菜单项样式"""
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
        # 调用注册的回调函数
        if item_id in self.callbacks:
            try:
                # 捕获回调函数的输出（可选）
                output_buffer = io.StringIO()
                with redirect_stdout(output_buffer):
                    self.callbacks[item_id](item_id, button)
                
                # 获取捕获的输出（用于调试）
                callback_output = output_buffer.getvalue().strip()
                if callback_output:
                    print(f"[{self.title}] {callback_output}")
                
            except Exception as e:
                print(f"[{self.title}] 回调函数执行错误: {str(e)}")
        
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
        self.main_button.button_style = 'warning'
    
    def close_menu(self):
        """关闭菜单"""
        self.is_menu_open = False
        self.menu_container.layout.display = 'none'
        self.main_button.description = f'{self.title} ▼'
        self.main_button.button_style = 'info'
    
    def register_callback(self, item_id: str, callback: Callable):
        """注册菜单项回调函数"""
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


def create_menu_bar_panels() -> tuple:
    """
    创建4个专用面板，用于水平排列的菜单栏

    Returns:
        (file_panel, operation_panel, tools_panel, help_panel)
    """
    # 创建4个面板 - 调整宽度避免横向滚动条
    file_panel = CompactOperationPanel("文件", "auto")
    operation_panel = CompactOperationPanel("操作", "auto")
    tools_panel = CompactOperationPanel("工具", "auto")
    help_panel = CompactOperationPanel("帮助", "auto")
    
    # 工具面板添加ROI选择项
    tools_panel.add_menu_item(
        item_id='roi_select',
        description='🎯 ROI选择',
        button_style='primary',
        tooltip='选择感兴趣区域'
    )
    
    return file_panel, operation_panel, tools_panel, help_panel


def create_horizontal_menu_bar() -> tuple:
    """
    创建水平排列的菜单栏
    
    Returns:
        (menu_bar_widget, (file_panel, operation_panel, tools_panel, help_panel))
    """
    file_panel, operation_panel, tools_panel, help_panel = create_menu_bar_panels()
    
    # 创建水平布局 - 优化避免横向滚动条
    menu_bar = widgets.HBox([
        file_panel.panel,
        operation_panel.panel,
        tools_panel.panel,
        help_panel.panel
    ], layout=widgets.Layout(
        width='100%',
        max_width='100%',  # 限制最大宽度
        margin='3px 0',    # 减少边距
        padding='3px',     # 减少内边距
        border='1px solid #e9ecef',
        border_radius='5px',
        background_color='#ffffff',
        justify_content='flex-start',  # 左对齐
        align_items='flex-start',      # 顶部对齐
        overflow='hidden'  # 隐藏溢出内容
    ))
    
    return menu_bar, (file_panel, operation_panel, tools_panel, help_panel)


# 测试函数
def test_compact_panels():
    """测试紧凑型面板"""
    print("=== 紧凑型操作面板测试 ===")
    
    # 创建菜单栏
    menu_bar, panels = create_horizontal_menu_bar()
    file_panel, operation_panel, tools_panel, help_panel = panels
    
    # 为工具面板注册ROI选择回调
    def roi_select_callback(item_id, button):
        print(f"🎯 ROI选择功能被触发")
    
    tools_panel.register_callback('roi_select', roi_select_callback)
    
    print("菜单栏创建完成，包含4个面板:")
    print(f"- 文件面板: {file_panel.get_menu_state()['item_count']}个菜单项")
    print(f"- 操作面板: {operation_panel.get_menu_state()['item_count']}个菜单项")
    print(f"- 工具面板: {tools_panel.get_menu_state()['item_count']}个菜单项")
    print(f"- 帮助面板: {help_panel.get_menu_state()['item_count']}个菜单项")
    
    return menu_bar, panels


if __name__ == "__main__":
    test_compact_panels()
