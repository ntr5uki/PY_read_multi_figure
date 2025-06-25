"""
基于PIL和ipywidgets的ROI选择器
完全避免使用matplotlib，提供稳定的Jupyter notebook交互体验
"""

import io
import time
from typing import Optional, Tuple, Union, Callable
import numpy as np
from PIL import Image, ImageDraw
import ipywidgets as widgets
from IPython.display import display

from .confirm_cancel_mixin import ConfirmCancelMixin


class PILROISelector(ConfirmCancelMixin):
    """基于PIL的ROI选择器类"""
    
    def __init__(self, image: np.ndarray):
        """
        初始化ROI选择器

        Args:
            image: 输入的numpy图像数组，支持2D灰度图或3D彩色图
        """
        # 初始化父类（确认取消按钮）
        super().__init__(confirm_text='确认选择', cancel_text='取消')

        self.original_image = self._prepare_image(image)
        self.image_height, self.image_width = self.original_image.shape[:2]

        # ROI选择结果
        self.roi_result: Optional[Tuple[int, int, int, int]] = None

        # 节流更新控制
        self._last_update_time = 0
        # 根据图像尺寸动态调整节流延迟
        self._update_delay = self._calculate_throttle_delay()

        # 创建UI组件
        self._create_widgets()
        self._setup_callbacks()

        # 设置主容器用于关闭操作
        if self.main_container is None:
            raise ValueError("主容器未设置，请检查代码逻辑")
        self.set_main_container(self.main_container)
        
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

    def _calculate_throttle_delay(self) -> float:
        """
        根据图像尺寸动态计算节流延迟

        Returns:
            节流延迟时间（秒）
        """
        # 计算图像像素数
        total_pixels = self.image_width * self.image_height

        # 根据像素数动态调整延迟
        if total_pixels < 100000:  # 小于100K像素（如320x240）
            return 0.02  # 20ms
        elif total_pixels < 300000:  # 小于300K像素（如640x480）
            return 0.05  # 50ms
        elif total_pixels < 600000:  # 小于600K像素（如640x800）
            return 0.08  # 80ms
        else:  # 大于600K像素
            return 0.1   # 100ms
    
    def _create_widgets(self):
        """创建所有UI组件"""
        # 图像显示组件
        self.image_widget = widgets.Image(
            format='jpeg',
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
        


        # 按钮容器已在父类中创建，直接使用
        
        # 主容器（使用父类的按钮容器）
        self.main_container = widgets.VBox([
            self.image_widget,
            self.x_range_slider,
            self.y_range_slider,
            self.get_button_box()  # 使用父类的按钮容器
        ], layout=widgets.Layout(
            align_items='center',
            padding='20px',
            border='1px solid #ddd',
            border_radius='5px'
        ))
        
        # 初始化图像显示
        self._update_image_display()
    
    # 回调注册方法已在父类中实现

    def _setup_callbacks(self):
        """设置回调函数"""
        self.x_range_slider.observe(self._on_range_change, names='value')
        self.y_range_slider.observe(self._on_range_change, names='value')
        self.register_confirm_callback(self._on_confirm)
        self.register_cancel_callback(self._on_cancel)
    
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
        pil_image.save(buffer, format='JPEG', quality=80)
        self.image_widget.value = buffer.getvalue()
    

    
    def _on_confirm_action(self, button) -> None:
        """实现父类的抽象方法：确认动作"""
        x_min, x_max = self.x_range_slider.value
        y_min, y_max = self.y_range_slider.value
        self.roi_result = (x_min, x_max, y_min, y_max)
        # 父类会自动关闭弹窗

    def _on_cancel_action(self, button) -> None:
        """实现父类的抽象方法：取消动作"""
        self.roi_result = None
        # 父类会自动关闭弹窗

    # 保持向后兼容的方法
    def _on_confirm(self, button) -> None:
        """确认按钮回调（向后兼容）"""
        self._on_confirm_action(button)

    def _on_cancel(self, button) -> None:
        """取消按钮回调（向后兼容）"""
        self._on_cancel_action(button)
    
    # _close_widget 方法已在父类 ConfirmCancelMixin 中实现
    
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
