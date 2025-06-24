from .compact_operation_panel import CompactOperationPanel
import ipywidgets as widgets

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
        description='🎯 图像序列剪裁',
        button_style='primary',
        tooltip='选则区域剪裁'
    )
    
    return file_panel, operation_panel, tools_panel, help_panel


def create_horizontal_menu_bar() -> tuple(widgets.HBox, tuple):
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
        print("🎯 ROI选择功能被触发")
    
    tools_panel.register_callback('roi_select', roi_select_callback)
    
    print("菜单栏创建完成，包含4个面板:")
    print(f"- 文件面板: {file_panel.get_menu_state()['item_count']}个菜单项")
    print(f"- 操作面板: {operation_panel.get_menu_state()['item_count']}个菜单项")
    print(f"- 工具面板: {tools_panel.get_menu_state()['item_count']}个菜单项")
    print(f"- 帮助面板: {help_panel.get_menu_state()['item_count']}个菜单项")
    
    return menu_bar, panels
