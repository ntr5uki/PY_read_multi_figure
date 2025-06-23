#!/usr/bin/env python3
"""
智能操作面板集成示例
演示如何将SmartOperationPanel集成到InteractiveImageViewer中
"""

import numpy as np
import ipywidgets as widgets
from IPython.display import display
from typing import Optional
from pynbgui.smart_operation_panel import SmartOperationPanel


class EnhancedImageViewer:
    """
    增强版图像查看器 - 集成智能操作面板
    这是一个简化的示例，展示集成方案
    """
    
    def __init__(self):
        """初始化增强版图像查看器"""
        self.current_image: Optional[np.ndarray] = None
        self.current_roi: Optional[tuple] = None
        self.saved_rois = []
        
        # 创建界面组件
        self._create_widgets()
        self._setup_roi_panel()
        self._setup_callbacks()
        
    def _create_widgets(self):
        """创建基础界面组件"""
        # 标题
        self.title_label = widgets.HTML("<h3>📊 增强版图像查看器</h3>")
        
        # 图像加载按钮（模拟）
        self.load_button = widgets.Button(
            description='📁 加载测试图像',
            button_style='info',
            layout=widgets.Layout(width='150px', margin='5px 0')
        )
        
        # 状态显示
        self.status_label = widgets.HTML(
            value="<i>请加载图像以启用ROI操作</i>",
            layout=widgets.Layout(margin='10px 0')
        )
        
        # 图像显示区域（模拟）
        self.image_display = widgets.HTML(
            value="<div style='width:300px; height:200px; border:2px dashed #ccc; "
                  "display:flex; align-items:center; justify-content:center; "
                  "background-color:#f8f9fa;'>📷 图像显示区域</div>",
            layout=widgets.Layout(margin='10px 0')
        )
        
    def _setup_roi_panel(self):
        """设置ROI操作面板"""
        # 创建智能操作面板（现在默认为空菜单）
        self.roi_panel = SmartOperationPanel("🎯 ROI操作", "200px")

        # 添加ROI相关菜单项
        roi_menu_items = [
            ('select_roi', '🎯 选择ROI区域', 'primary', '选择感兴趣区域'),
            ('save_roi', '💾 保存当前ROI', '', '保存当前ROI设置'),
            ('load_roi', '📂 加载预设ROI', '', '从预设中加载ROI'),
            ('roi_stats', '📊 ROI统计信息', 'info', '显示ROI区域统计'),
            ('clear_roi', '🗑️ 清除ROI', 'warning', '清除当前ROI设置')
        ]

        for item_id, description, style, tooltip in roi_menu_items:
            self.roi_panel.add_menu_item(item_id, description, style, tooltip)

        # 初始状态：禁用所有ROI相关功能
        self._update_roi_panel_state(has_image=False, has_roi=False)
        
    def _setup_callbacks(self):
        """设置回调函数"""
        # 图像加载按钮回调
        self.load_button.on_click(self._on_load_image)
        
        # ROI面板回调
        self.roi_panel.register_callback('select_roi', self._on_select_roi)
        self.roi_panel.register_callback('save_roi', self._on_save_roi)
        self.roi_panel.register_callback('load_roi', self._on_load_roi)
        self.roi_panel.register_callback('roi_stats', self._on_roi_stats)
        self.roi_panel.register_callback('clear_roi', self._on_clear_roi)
        
    def _on_load_image(self, button):
        """加载图像回调（模拟）"""
        # 模拟加载图像
        self.current_image = np.random.randint(0, 255, (300, 400), dtype=np.uint8)
        
        # 更新界面
        self.image_display.value = (
            "<div style='width:300px; height:200px; border:2px solid #28a745; "
            "display:flex; align-items:center; justify-content:center; "
            "background-color:#e8f5e8;'>✅ 图像已加载 (300x400)</div>"
        )
        
        self.status_label.value = "✅ 图像加载成功，ROI操作已启用"
        
        # 更新ROI面板状态
        self._update_roi_panel_state(has_image=True, has_roi=False)
        
    def _on_select_roi(self, item_id, button):
        """选择ROI回调"""
        if self.current_image is None:
            self.status_label.value = "❌ 请先加载图像"
            return
        
        # 模拟ROI选择
        self.current_roi = (50, 350, 75, 225)  # (x_min, x_max, y_min, y_max)
        
        # 更新界面
        self.image_display.value = (
            "<div style='width:300px; height:200px; border:2px solid #007bff; "
            "display:flex; align-items:center; justify-content:center; "
            "background-color:#e3f2fd;'>🎯 ROI已选择<br>区域: (50,75) 到 (350,225)</div>"
        )
        
        self.status_label.value = f"🎯 ROI选择完成: 坐标{self.current_roi}"
        
        # 更新ROI面板状态
        self._update_roi_panel_state(has_image=True, has_roi=True)
        
    def _on_save_roi(self, item_id, button):
        """保存ROI回调"""
        if self.current_roi is None:
            self.status_label.value = "❌ 请先选择ROI区域"
            return
        
        # 保存ROI
        roi_data = {
            'coords': self.current_roi,
            'name': f"ROI_{len(self.saved_rois) + 1}",
            'image_shape': self.current_image.shape if self.current_image is not None else None
        }
        self.saved_rois.append(roi_data)
        
        self.status_label.value = f"💾 ROI已保存: {roi_data['name']} - 坐标{self.current_roi}"
        
    def _on_load_roi(self, item_id, button):
        """加载ROI回调"""
        if not self.saved_rois:
            self.status_label.value = "❌ 暂无保存的ROI"
            return
        
        # 加载最后一个保存的ROI
        last_roi = self.saved_rois[-1]
        self.current_roi = last_roi['coords']
        
        # 更新界面
        self.image_display.value = (
            f"<div style='width:300px; height:200px; border:2px solid #ffc107; "
            f"display:flex; align-items:center; justify-content:center; "
            f"background-color:#fff3cd;'>📂 已加载ROI<br>{last_roi['name']}: {self.current_roi}</div>"
        )
        
        self.status_label.value = f"📂 ROI加载完成: {last_roi['name']} - 坐标{self.current_roi}"
        
        # 更新ROI面板状态
        self._update_roi_panel_state(has_image=True, has_roi=True)
        
    def _on_roi_stats(self, item_id, button):
        """ROI统计信息回调"""
        if self.current_roi is None:
            self.status_label.value = "❌ 请先选择ROI区域"
            return
        
        # 计算ROI统计信息
        x_min, x_max, y_min, y_max = self.current_roi
        width = x_max - x_min
        height = y_max - y_min
        area = width * height
        
        # 模拟像素值统计
        if self.current_image is not None:
            roi_region = self.current_image[y_min:y_max, x_min:x_max]
            mean_val = np.mean(roi_region)
            std_val = np.std(roi_region)
            min_val = np.min(roi_region)
            max_val = np.max(roi_region)
            
            stats_info = (
                f"📊 ROI统计信息:<br>"
                f"• 尺寸: {width}×{height} 像素<br>"
                f"• 面积: {area} 像素<br>"
                f"• 均值: {mean_val:.1f}<br>"
                f"• 标准差: {std_val:.1f}<br>"
                f"• 范围: [{min_val}, {max_val}]"
            )
        else:
            stats_info = f"📊 ROI几何信息: 尺寸{width}×{height}, 面积{area}像素"
        
        self.status_label.value = stats_info
        
    def _on_clear_roi(self, item_id, button):
        """清除ROI回调"""
        self.current_roi = None
        
        # 更新界面
        if self.current_image is not None:
            self.image_display.value = (
                "<div style='width:300px; height:200px; border:2px solid #28a745; "
                "display:flex; align-items:center; justify-content:center; "
                "background-color:#e8f5e8;'>✅ 图像已加载 (300x400)<br>ROI已清除</div>"
            )
        
        self.status_label.value = "🗑️ ROI已清除"
        
        # 更新ROI面板状态
        self._update_roi_panel_state(has_image=True, has_roi=False)
        
    def _update_roi_panel_state(self, has_image: bool, has_roi: bool):
        """更新ROI面板状态"""
        # 根据当前状态更新菜单项可用性
        self.roi_panel.set_menu_item_enabled('select_roi', has_image)
        self.roi_panel.set_menu_item_enabled('save_roi', has_roi)
        self.roi_panel.set_menu_item_enabled('load_roi', len(self.saved_rois) > 0)
        self.roi_panel.set_menu_item_enabled('roi_stats', has_roi)
        self.roi_panel.set_menu_item_enabled('clear_roi', has_roi)
        
        # 更新按钮样式
        if has_image:
            self.roi_panel.set_menu_item_style('select_roi', 'success' if not has_roi else 'primary')
        
    def create_layout(self):
        """创建完整布局"""
        return widgets.VBox([
            self.title_label,
            self.load_button,
            self.roi_panel.panel,  # 集成智能操作面板
            self.status_label,
            self.image_display
        ], layout=widgets.Layout(
            border='1px solid #e9ecef',
            border_radius='6px',
            padding='15px',
            margin='10px'
        ))
        
    def display(self):
        """显示增强版图像查看器"""
        display(self.create_layout())
        return self


def create_enhanced_viewer():
    """创建增强版图像查看器的便捷函数"""
    return EnhancedImageViewer()


def demo_integration():
    """演示集成效果"""
    print("🚀 智能操作面板集成演示")
    print("=" * 50)
    
    # 创建增强版查看器
    viewer = create_enhanced_viewer()
    
    print("✅ 增强版图像查看器创建完成")
    print("\n📋 功能特性:")
    print("  • 智能ROI操作面板")
    print("  • 动态状态管理")
    print("  • ROI保存/加载功能")
    print("  • 实时统计信息")
    print("  • 响应式界面设计")
    
    print("\n💡 使用说明:")
    print("  1. 点击'加载测试图像'按钮")
    print("  2. 点击'ROI操作'展开菜单")
    print("  3. 选择相应的ROI操作")
    print("  4. 观察状态变化和界面响应")
    
    return viewer


if __name__ == "__main__":
    # 命令行演示
    demo_viewer = demo_integration()
    
    print("\n🎯 在Jupyter notebook中运行以下代码查看完整效果:")
    print("from integration_example import create_enhanced_viewer")
    print("viewer = create_enhanced_viewer()")
    print("viewer.display()")
