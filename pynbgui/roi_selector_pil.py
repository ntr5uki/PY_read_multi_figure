"""
基于PIL和ipywidgets的ROI选择器
完全避免使用matplotlib，提供稳定的Jupyter notebook交互体验
"""

import io
import time
from typing import Optional, Tuple, Union
import numpy as np
from PIL import Image, ImageDraw
import ipywidgets as widgets
from IPython.display import display


class PILROISelector:
    """基于PIL的ROI选择器类"""
    
    def __init__(self, image: np.ndarray):
        """
        初始化ROI选择器
        
        Args:
            image: 输入的numpy图像数组，支持2D灰度图或3D彩色图
        """
        self.original_image = self._prepare_image(image)
        self.image_height, self.image_width = self.original_image.shape[:2]
        
        # ROI选择结果
        self.roi_result: Optional[Tuple[int, int, int, int]] = None
        self.is_cancelled = False
        
        # 节流更新控制
        self._last_update_time = 0
        self._update_delay = 0.05  # 50ms节流延迟
        
        # 创建UI组件
        self._create_widgets()
        self._setup_callbacks()
        
    def _prepare_image(self, image: np.ndarray) -> np.ndarray:
        """准备图像数据，确保格式正确"""
        if image.ndim == 2:
            # 灰度图转换为RGB
            return np.stack([image, image, image], axis=-1)
        elif image.ndim == 3 and image.shape[2] == 3:
            # RGB图像
            return image
        elif image.ndim == 3 and image.shape[2] == 1:
            # 单通道3D转换为RGB
            return np.repeat(image, 3, axis=2)
        else:
            raise ValueError(f"不支持的图像维度: {image.shape}")
    
    def _create_widgets(self):
        """创建所有UI组件"""
        # 图像显示组件
        self.image_widget = widgets.Image(
            format='png',
            width=600,
            height=400
        )

        # 计算合理的默认ROI范围
        x_margin = min(50, self.image_width // 4)
        y_margin = min(50, self.image_height // 4)

        x_default_min = x_margin
        x_default_max = max(x_default_min + 10, self.image_width - x_margin)
        y_default_min = y_margin
        y_default_max = max(y_default_min + 10, self.image_height - y_margin)

        # X轴范围滑块
        self.x_range_slider = widgets.IntRangeSlider(
            value=[x_default_min, x_default_max],
            min=0,
            max=self.image_width,
            step=1,
            description='X范围:',
            style={'description_width': '60px'},
            layout=widgets.Layout(width='500px')
        )

        # Y轴范围滑块
        self.y_range_slider = widgets.IntRangeSlider(
            value=[y_default_min, y_default_max],
            min=0,
            max=self.image_height,
            step=1,
            description='Y范围:',
            style={'description_width': '60px'},
            layout=widgets.Layout(width='500px')
        )
        

        
        # 控制按钮
        self.confirm_button = widgets.Button(
            description='确认选择',
            button_style='success',
            layout=widgets.Layout(width='100px', margin='5px')
        )
        
        self.cancel_button = widgets.Button(
            description='取消',
            button_style='danger',
            layout=widgets.Layout(width='100px', margin='5px')
        )
        
        # 按钮容器
        self.button_box = widgets.HBox([
            self.confirm_button,
            self.cancel_button
        ], layout=widgets.Layout(justify_content='center'))
        
        # 主容器
        self.main_container = widgets.VBox([
            self.image_widget,
            self.x_range_slider,
            self.y_range_slider,
            self.button_box
        ], layout=widgets.Layout(
            align_items='center',
            padding='20px',
            border='1px solid #ddd',
            border_radius='5px'
        ))
        
        # 初始化图像显示
        self._update_image_display()
    
    def _setup_callbacks(self):
        """设置回调函数"""
        self.x_range_slider.observe(self._on_range_change, names='value')
        self.y_range_slider.observe(self._on_range_change, names='value')
        self.confirm_button.on_click(self._on_confirm)
        self.cancel_button.on_click(self._on_cancel)
    
    def _on_range_change(self, change) -> None:
        """滑块值变化时的回调函数（带节流）"""
        current_time = time.time()
        if current_time - self._last_update_time > self._update_delay:
            self._update_image_display()
            self._last_update_time = current_time
    
    def _update_image_display(self):
        """更新图像显示，包含ROI框"""
        # 获取当前ROI坐标
        x_min, x_max = self.x_range_slider.value
        y_min, y_max = self.y_range_slider.value
        
        # 创建PIL图像
        pil_image = Image.fromarray(self.original_image.astype(np.uint8))
        
        # 绘制ROI框
        draw = ImageDraw.Draw(pil_image)
        
        # 绘制矩形框（蓝色，线宽2）
        draw.rectangle(
            [(x_min, y_min), (x_max, y_max)],
            outline='blue',
            width=2
        )

        # 绘制角点标记
        corner_size = 5
        corners = [
            (x_min, y_min), (x_max, y_min),
            (x_min, y_max), (x_max, y_max)
        ]

        for corner_x, corner_y in corners:
            draw.rectangle(
                [(corner_x - corner_size, corner_y - corner_size),
                 (corner_x + corner_size, corner_y + corner_size)],
                fill='blue'
            )
        
        # 转换为bytes并更新widget
        buffer = io.BytesIO()
        pil_image.save(buffer, format='PNG')
        self.image_widget.value = buffer.getvalue()
    

    
    def _on_confirm(self, button) -> None:
        """确认按钮回调"""
        x_min, x_max = self.x_range_slider.value
        y_min, y_max = self.y_range_slider.value
        self.roi_result = (x_min, x_max, y_min, y_max)
        self._close_widget()
    
    def _on_cancel(self, button) -> None:
        """取消按钮回调"""
        self.is_cancelled = True
        self.roi_result = None
        self._close_widget()
    
    def _close_widget(self):
        """关闭widget界面"""
        self.main_container.close()
    
    def display(self):
        """显示ROI选择器"""
        display(self.main_container)
        return self


def select_roi_interactive(image: np.ndarray) -> PILROISelector:
    """
    交互式ROI选择函数

    Args:
        image: 输入的numpy图像数组

    Returns:
        ROI选择器实例，用户交互完成后可通过.roi_result获取结果
    """
    selector = PILROISelector(image)
    selector.display()

    # 注意：在Jupyter notebook中，这个函数会立即返回
    # 实际的ROI选择结果需要通过selector.roi_result获取
    return selector


# 便捷函数
def create_roi_selector(image: np.ndarray) -> PILROISelector:
    """
    创建ROI选择器实例
    
    Args:
        image: 输入的numpy图像数组
        
    Returns:
        ROI选择器实例
    """
    return PILROISelector(image)
