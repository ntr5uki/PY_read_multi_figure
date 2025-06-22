"""
基于ipywidgets的ROI选择器 - 完全避免matplotlib图形关闭问题
专门针对Jupyter notebook环境优化
"""

import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output
import io
import base64
from typing import Optional, Tuple, Callable

# 设置matplotlib支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class ROISelectorWidget:
    """
    基于ipywidgets的ROI选择器
    完全避免matplotlib图形关闭问题，支持实时可视化反馈
    """

    def __init__(self, image: np.ndarray, title: str = "ROI选择器"):
        """
        初始化ROI选择器

        Args:
            image: 输入图像数组
            title: 窗口标题
        """
        self.image = image
        self.title = title
        self.roi_coords = None
        self.callback = None
        self.image_widget = None
        self.is_closed = False

        # 创建UI组件
        self._create_ui()

    def _create_ui(self):
        """创建用户界面"""
        # 创建图像显示widget
        self.image_widget = self._create_image_widget()

        # 创建控制按钮
        self.confirm_btn = widgets.Button(
            description='确认选择',
            button_style='success',
            layout=widgets.Layout(width='120px', margin='5px')
        )
        self.cancel_btn = widgets.Button(
            description='取消',
            button_style='danger',
            layout=widgets.Layout(width='120px', margin='5px')
        )
        self.close_btn = widgets.Button(
            description='关闭界面',
            button_style='warning',
            layout=widgets.Layout(width='120px', margin='5px')
        )

        # 创建坐标输入框
        self.x1_input = widgets.IntText(
            value=50,
            description='X1:',
            layout=widgets.Layout(width='150px', margin='2px')
        )
        self.y1_input = widgets.IntText(
            value=50,
            description='Y1:',
            layout=widgets.Layout(width='150px', margin='2px')
        )
        self.x2_input = widgets.IntText(
            value=min(200, self.image.shape[1]-1),
            description='X2:',
            layout=widgets.Layout(width='150px', margin='2px')
        )
        self.y2_input = widgets.IntText(
            value=min(200, self.image.shape[0]-1),
            description='Y2:',
            layout=widgets.Layout(width='150px', margin='2px')
        )

        # 创建更新按钮
        self.update_btn = widgets.Button(
            description='更新预览',
            button_style='primary',
            layout=widgets.Layout(width='100px', margin='2px')
        )

        # 创建预设按钮
        self.preset_center_btn = widgets.Button(
            description='中心区域',
            button_style='info',
            layout=widgets.Layout(width='100px', margin='2px')
        )
        self.preset_full_btn = widgets.Button(
            description='全图',
            button_style='info',
            layout=widgets.Layout(width='100px', margin='2px')
        )

        # 创建状态显示
        h, w = self.image.shape[:2]
        self.status_label = widgets.HTML(
            value=f"<b>图像尺寸:</b> {w} x {h} 像素<br><b>状态:</b> 请设置ROI坐标"
        )

        # 绑定事件
        self.confirm_btn.on_click(self._on_confirm)
        self.cancel_btn.on_click(self._on_cancel)
        self.close_btn.on_click(self._on_close)
        self.update_btn.on_click(self._on_update_preview)
        self.preset_center_btn.on_click(self._preset_center)
        self.preset_full_btn.on_click(self._preset_full)

        # 绑定坐标输入框的变化事件
        self.x1_input.observe(self._on_coord_change, names='value')
        self.y1_input.observe(self._on_coord_change, names='value')
        self.x2_input.observe(self._on_coord_change, names='value')
        self.y2_input.observe(self._on_coord_change, names='value')

        # 创建布局
        coord_row1 = widgets.HBox([self.x1_input, self.y1_input])
        coord_row2 = widgets.HBox([self.x2_input, self.y2_input])
        preset_box = widgets.HBox([self.preset_center_btn, self.preset_full_btn, self.update_btn])
        button_box = widgets.HBox([self.confirm_btn, self.cancel_btn, self.close_btn])

        self.main_widget = widgets.VBox([
            widgets.HTML(f"<h3 style='color: #2e86ab;'>{self.title}</h3>"),
            self.image_widget,
            widgets.HTML("<hr><b style='color: #2e86ab;'>ROI坐标设置:</b>"),
            coord_row1,
            coord_row2,
            widgets.HTML("<b>快速设置:</b>"),
            preset_box,
            widgets.HTML("<hr>"),
            button_box,
            self.status_label
        ], layout=widgets.Layout(padding='10px', border='2px solid #ddd'))

    def _create_image_widget(self, roi_coords: Optional[Tuple[int, int, int, int]] = None) -> widgets.Image:
        """创建图像widget，可选择显示ROI框"""
        # 使用matplotlib生成图像
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.imshow(self.image, cmap='gray' if len(self.image.shape) == 2 else None)
        ax.set_title('图像预览 - ROI选择器')
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('X (像素)')
        ax.set_ylabel('Y (像素)')

        # 如果有ROI坐标，绘制ROI框
        if roi_coords:
            x1, y1, x2, y2 = roi_coords
            # 绘制ROI矩形
            rect_x = [x1, x2, x2, x1, x1]
            rect_y = [y1, y1, y2, y2, y1]
            ax.plot(rect_x, rect_y, 'r-', linewidth=2, label='ROI区域')
            ax.plot(rect_x, rect_y, 'w--', linewidth=1, alpha=0.8)

            # 添加角点标记
            ax.plot([x1, x2, x2, x1], [y1, y1, y2, y2], 'ro', markersize=6)

            # 添加文本标注
            ax.text(x1, y1-10, f'({x1},{y1})', color='red', fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
            ax.text(x2, y2+15, f'({x2},{y2})', color='red', fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

            # 显示ROI尺寸
            roi_w, roi_h = x2 - x1, y2 - y1
            center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
            ax.text(center_x, center_y, f'{roi_w}×{roi_h}',
                   color='yellow', fontweight='bold', ha='center', va='center',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="black", alpha=0.7))

            ax.legend()

        # 将图像保存到内存
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        buf.seek(0)
        plt.close(fig)  # 立即关闭图形，避免显示问题

        # 创建图像widget
        image_widget = widgets.Image(
            value=buf.getvalue(),
            format='png',
            layout=widgets.Layout(max_width='800px', border='1px solid #ccc')
        )

        return image_widget

    def _on_coord_change(self, change):
        """坐标输入框变化时的回调"""
        if self.is_closed:
            return
        # 实时更新状态显示
        try:
            x1, y1, x2, y2 = self.x1_input.value, self.y1_input.value, self.x2_input.value, self.y2_input.value
            h, w = self.image.shape[:2]

            if 0 <= x1 < w and 0 <= x2 < w and 0 <= y1 < h and 0 <= y2 < h and x1 < x2 and y1 < y2:
                roi_w, roi_h = x2 - x1, y2 - y1
                self.status_label.value = f"<b>当前ROI:</b> ({x1},{y1}) 到 ({x2},{y2}) | 尺寸: {roi_w}×{roi_h}"
            else:
                self.status_label.value = "<b style='color: orange;'>坐标无效，请检查输入</b>"
        except:
            pass

    def _on_update_preview(self, button):
        """更新预览按钮回调"""
        if self.is_closed:
            return
        try:
            x1, y1, x2, y2 = self.x1_input.value, self.y1_input.value, self.x2_input.value, self.y2_input.value
            h, w = self.image.shape[:2]

            if not (0 <= x1 < w and 0 <= x2 < w and 0 <= y1 < h and 0 <= y2 < h):
                self.status_label.value = f"<b style='color: red;'>错误:</b> 坐标超出图像范围! 图像大小: {w}x{h}"
                return

            if x1 >= x2 or y1 >= y2:
                self.status_label.value = "<b style='color: red;'>错误:</b> 坐标顺序错误! X2应大于X1，Y2应大于Y1"
                return

            # 更新图像显示
            new_image_widget = self._create_image_widget((x1, y1, x2, y2))
            if hasattr(self.image_widget, 'value'):
                self.image_widget.value = new_image_widget.value
            self.status_label.value = "<b style='color: green;'>预览已更新，显示ROI区域</b>"

        except Exception as e:
            self.status_label.value = f"<b style='color: red;'>更新预览失败:</b> {e}"

    def _on_close(self, button):
        """关闭界面按钮回调"""
        self.is_closed = True
        self.main_widget.close()
        self.status_label.value = "<b style='color: gray;'>界面已关闭</b>"
        print("ROI选择器界面已关闭")

    def _preset_center(self, button):
        """设置中心区域预设"""
        h, w = self.image.shape[:2]
        center_x, center_y = w // 2, h // 2
        size = min(w, h) // 4

        self.x1_input.value = max(0, center_x - size)
        self.y1_input.value = max(0, center_y - size)
        self.x2_input.value = min(w-1, center_x + size)
        self.y2_input.value = min(h-1, center_y + size)

        self.status_label.value = "<b style='color: green;'>已设置中心区域预设</b>"
        # 自动更新预览
        self._on_update_preview(None)

    def _preset_full(self, button):
        """设置全图预设"""
        h, w = self.image.shape[:2]
        self.x1_input.value = 0
        self.y1_input.value = 0
        self.x2_input.value = w - 1
        self.y2_input.value = h - 1

        self.status_label.value = "<b style='color: green;'>已设置全图预设</b>"
        # 自动更新预览
        self._on_update_preview(None)

    def _on_confirm(self, button):
        """确认按钮回调"""
        if self.is_closed:
            return

        try:
            x1 = self.x1_input.value
            y1 = self.y1_input.value
            x2 = self.x2_input.value
            y2 = self.y2_input.value

            # 验证坐标
            h, w = self.image.shape[:2]
            if not (0 <= x1 < w and 0 <= x2 < w and 0 <= y1 < h and 0 <= y2 < h):
                self.status_label.value = f"<b style='color: red;'>错误:</b> 坐标超出图像范围! 图像大小: {w}x{h}"
                return

            if x1 >= x2 or y1 >= y2:
                self.status_label.value = "<b style='color: red;'>错误:</b> 坐标顺序错误! X2应大于X1，Y2应大于Y1"
                return

            self.roi_coords = (x1, y1, x2, y2)
            roi_w, roi_h = x2 - x1, y2 - y1

            # 更新最终预览
            final_image_widget = self._create_image_widget(self.roi_coords)
            if hasattr(self.image_widget, 'value'):
                self.image_widget.value = final_image_widget.value

            self.status_label.value = f"""
            <b style='color: green;'>✅ 已确认ROI选择</b><br>
            <b>坐标:</b> ({x1}, {y1}) 到 ({x2}, {y2})<br>
            <b>尺寸:</b> {roi_w} x {roi_h} 像素<br>
            <b>切片:</b> image[{y1}:{y2}, {x1}:{x2}]<br>
            <b style='color: blue;'>可以点击"关闭界面"按钮关闭选择器</b>
            """

            if self.callback:
                self.callback(self.roi_coords)

        except Exception as e:
            self.status_label.value = f"<b style='color: red;'>错误:</b> {e}"

    def _on_cancel(self, button):
        """取消按钮回调"""
        if self.is_closed:
            return

        self.roi_coords = None
        self.status_label.value = "<b style='color: orange;'>❌ 已取消ROI选择</b>"

        # 重置图像显示
        reset_image_widget = self._create_image_widget()
        if hasattr(self.image_widget, 'value'):
            self.image_widget.value = reset_image_widget.value

        if self.callback:
            self.callback(None)

    def show(self, callback: Optional[Callable] = None) -> widgets.VBox:
        """
        显示ROI选择器
        
        Args:
            callback: 可选的回调函数，当选择完成时调用
            
        Returns:
            主widget，可以用display()显示
        """
        self.callback = callback
        return self.main_widget

    def get_roi(self) -> Optional[Tuple[int, int, int, int]]:
        """
        获取选择的ROI坐标
        
        Returns:
            ROI坐标 (x1, y1, x2, y2) 或 None
        """
        return self.roi_coords


def create_roi_selector(image: np.ndarray, title: str = "ROI选择器") -> ROISelectorWidget:
    """
    创建ROI选择器的便捷函数
    
    Args:
        image: 输入图像数组
        title: 窗口标题
        
    Returns:
        ROI选择器实例
    """
    return ROISelectorWidget(image, title)
