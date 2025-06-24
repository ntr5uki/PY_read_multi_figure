from typing import Optional, Tuple, Dict, Any, Callable, List
import numpy as np

from .roi_selector_pil import PILROISelector


class CutFrameSelector:
    """
    3D图像裁剪选择器类

    使用ROI选择器对3D图像进行交互式裁剪
    """

    def __init__(self, img2d: np.ndarray, img3d: np.ndarray):
        """
        初始化裁剪选择器

        Args:
            img2d: 2D参考图像，用于ROI选择
            img3d: 3D图像数据，将根据ROI进行裁剪

        Raises:
            ValueError: 当输入图像尺寸不匹配时
        """
        # 验证输入
        self._validate_inputs(img2d, img3d)

        # 存储原始数据
        self.img2d = img2d.copy()
        self.img3d = img3d.copy()

        # 状态管理
        self.roi_coords: Optional[Tuple[int, int, int, int]] = None
        self.cropped_result: Optional[np.ndarray] = None
        self.is_completed = False
        self.is_cancelled = False

        # 外部回调函数列表
        self.external_confirm_callbacks: List[Callable] = []
        self.external_cancel_callbacks: List[Callable] = []

        # 创建ROI选择器
        self.roi_selector = PILROISelector(self.img2d)
        self._setup_callbacks()

    def _validate_inputs(self, img2d: np.ndarray, img3d: np.ndarray) -> None:
        """验证输入图像的尺寸兼容性"""
        if img2d.shape[0] != img3d.shape[1] or img2d.shape[1] != img3d.shape[2]:
            raise ValueError(
                f"图像尺寸不匹配: img2d.shape={img2d.shape}, "
                f"img3d.shape={img3d.shape}。要求: img2d.shape[0] == img3d.shape[1] "
                f"且 img2d.shape[1] == img3d.shape[2]"
            )

    def _setup_callbacks(self) -> None:
        """设置ROI选择器的回调函数"""
        # 保存原始回调方法的引用
        original_on_confirm = self.roi_selector._on_confirm
        original_on_cancel = self.roi_selector._on_cancel

        def enhanced_on_confirm(button) -> None:
            """增强的确认回调函数"""
            # 先调用原始的确认逻辑
            original_on_confirm(button)
            # 然后执行裁剪
            self._execute_crop()

        def enhanced_on_cancel(button) -> None:
            """增强的取消回调函数"""
            # 先调用原始的取消逻辑
            original_on_cancel(button)
            # 然后更新状态
            self._handle_cancel()

        # 设置ROI选择器的回调
        # 确保PILROISelector内部的回调先被设置（通过其__init__或display方法触发）
        # 然后再添加CutFrameSelector自身的回调
        self.roi_selector.register_confirm_callback(self._on_confirm)
        self.roi_selector.register_cancel_callback(self._on_cancel)

    def _on_confirm(self, button) -> None:
        """确认回调函数"""
        self._execute_crop()

        # 调用外部注册的确认回调
        for callback in self.external_confirm_callbacks:
            try:
                callback(self)
            except Exception as e:
                print(f"⚠️ 外部确认回调执行失败: {e}")

    def _on_cancel(self, button) -> None:
        """取消回调函数"""
        self._handle_cancel()

        # 调用外部注册的取消回调
        for callback in self.external_cancel_callbacks:
            try:
                callback(self)
            except Exception as e:
                print(f"⚠️ 外部取消回调执行失败: {e}")

    def _execute_crop(self) -> None:
        """执行3D图像裁剪"""
        print(f"DEBUG: _execute_crop 被调用. roi_selector.roi_result: {self.roi_selector.roi_result}")
        if self.roi_selector.roi_result is None:
            print("❌ 无法获取ROI坐标")
            return

        self.roi_coords = self.roi_selector.roi_result
        x_min, x_max, y_min, y_max = self.roi_coords

        # 执行裁剪
        self.cropped_result = self.img3d[:, y_min:y_max, x_min:x_max]
        self.is_completed = True

        print(f"✅ 3D图像裁剪完成")
        print(f"   原始尺寸: {self.img3d.shape}")
        print(f"   ROI坐标: ({x_min}, {y_min}) 到 ({x_max}, {y_max})")
        print(f"   裁剪后尺寸: {self.cropped_result.shape}")

    def _handle_cancel(self) -> None:
        """处理取消操作"""
        self.is_cancelled = True
        self.roi_coords = None
        self.cropped_result = None
        print("❌ ROI选择被取消")

    def display(self) -> 'CutFrameSelector':
        """
        显示ROI选择器界面

        Returns:
            self，支持链式调用
        """
        print("🎯 请在ROI选择器中选择感兴趣区域")
        print(f"   参考图像尺寸: {self.img2d.shape}")
        print(f"   3D图像尺寸: {self.img3d.shape}")

        self.roi_selector.display()
        return self

    def get_result(self) -> Optional[np.ndarray]:
        """
        获取裁剪结果

        Returns:
            裁剪后的3D图像，如果尚未完成选择则返回None
        """
        return self.cropped_result

    def get_status(self) -> str:
        """
        获取当前状态描述

        Returns:
            状态描述字符串
        """
        if self.is_completed and self.cropped_result is not None:
            return f"✅ 裁剪完成，结果尺寸: {self.cropped_result.shape}"
        elif self.is_cancelled:
            return "❌ 操作已取消"
        else:
            return "⏳ 等待用户选择ROI..."

    def get_roi_info(self) -> Optional[Dict[str, Any]]:
        """
        获取ROI信息

        Returns:
            包含ROI详细信息的字典，如果尚未选择则返回None
        """
        if self.roi_coords is None:
            return None

        x_min, x_max, y_min, y_max = self.roi_coords
        width = x_max - x_min
        height = y_max - y_min
        area = width * height

        return {
            'coordinates': self.roi_coords,
            'x_range': (x_min, x_max),
            'y_range': (y_min, y_max),
            'width': width,
            'height': height,
            'area': area,
            'original_shape': self.img2d.shape,
            'cropped_shape': (height, width) if self.cropped_result is None else self.cropped_result.shape[1:]
        }

    def reset(self) -> None:
        """重置选择器状态"""
        self.roi_coords = None
        self.cropped_result = None
        self.is_completed = False
        self.is_cancelled = False
        print("🔄 选择器状态已重置")

    def register_confirm_callback(self, callback: Callable[['CutFrameSelector'], None]) -> None:
        """
        注册确认回调函数

        Args:
            callback: 回调函数，接收CutFrameSelector实例作为参数
        """
        self.external_confirm_callbacks.append(callback)

    def register_cancel_callback(self, callback: Callable[['CutFrameSelector'], None]) -> None:
        """
        注册取消回调函数

        Args:
            callback: 回调函数，接收CutFrameSelector实例作为参数
        """
        self.external_cancel_callbacks.append(callback)


# 便捷函数，保持向后兼容
def cutFrame(img2d: np.ndarray, img3d: np.ndarray) -> CutFrameSelector:
    """
    创建3D图像裁剪选择器（便捷函数）

    Args:
        img2d: 2D参考图像，用于ROI选择
        img3d: 3D图像数据，将根据ROI进行裁剪

    Returns:
        CutFrameSelector实例

    Raises:
        ValueError: 当输入图像尺寸不匹配时
    """
    return CutFrameSelector(img2d, img3d).display()


def get_cutframe_result(selector: CutFrameSelector) -> Optional[np.ndarray]:
    """
    获取cutFrame的裁剪结果（便捷函数，保持向后兼容）

    Args:
        selector: CutFrameSelector实例

    Returns:
        裁剪后的3D图像，如果尚未完成选择则返回None
    """
    return selector.get_result()
