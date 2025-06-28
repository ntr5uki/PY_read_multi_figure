import ipywidgets as widgets
from IPython.display import display
import numpy as np
from typing import Optional

# 使用相对导入，更简洁
from .image_contrast_viewer import ImageContrastViewer
from .image_cropper import CutFrameSelector
from .resize_dialog_widget import ResizePopupWidget


class ImageSequenceViewer:
    def __init__(self, imageSequence: np.ndarray, useRangeSlider: bool = True, showSizeControl: bool = True):
        """
        初始化图像序列查看器。

        Args:
            imageSequence: 灰度图像或序列，形状为 (y, x) 或 (z, y, x)
            useRangeSlider: 是否使用范围滑块，默认为True
            showSizeControl: 是否显示图像大小控制，默认为True
        """
        # 支持2D和3D数组
        if imageSequence.ndim == 2:
            # 如果是2D数组，转换为3D (1, y, x)
            imageSequence = imageSequence[np.newaxis, :, :]
        elif imageSequence.ndim != 3:
            raise ValueError("imageSequence 必须是二维或三维 numpy 数组")

        self.imageSequence = imageSequence
        self.numImages = imageSequence.shape[0]
        self.useRangeSlider = useRangeSlider
        self.showSizeControl = showSizeControl

        # 计算整个图像序列的全局灰度范围，确保显示一致性
        self.globalRange = (float(imageSequence.min()), float(imageSequence.max()))

        # 创建图像选择控件
        self._createSelectWidget()

        # 创建图像查看器
        self._createImageViewer()
        
        # 创建组合控件
        self.combinedWidget = widgets.HBox([
            self.selectWidget, 
            self.imageViewerWidget
        ])

    def _createSelectWidget(self) -> None:
        """创建图像选择控件"""
        options = [(str(i), i) for i in range(self.numImages)]
        self.selectWidget = widgets.Select(
            options=options,
            value=0,
            description='',
            disabled=False,
            layout=widgets.Layout(width='70px',height='256px')
        )
        self.selectWidget.observe(self._onValueChange, names='value')

    def _createImageViewer(self) -> None:
        """创建图像查看器"""
        # 获取初始图像（第一张）
        currentImageData = self.imageSequence[0]
        # 传递全局灰度范围以确保图像序列显示一致性
        self.imageViewer = ImageContrastViewer(currentImageData, global_range=self.globalRange)

        # 获取图像查看器的widget
        self.imageViewerWidget = self.imageViewer.display(
            useRangeSlider=self.useRangeSlider,
            showSizeControl=self.showSizeControl
        )

    def _onValueChange(self, change: dict) -> None:
        """
        处理选择控件值变化的回调函数
        
        Args:
            change: 包含新值的字典
        """
        selected_index = change['new']
        newImageData = self.imageSequence[selected_index]
        
        # 更新图像数据
        self.imageViewer.updateImageData(newImageData)
        
        # 触发图像更新
        self._triggerImageUpdate()

    def _triggerImageUpdate(self) -> None:
        """触发图像查看器的更新"""
        # 触发对比度滑块更新
        if self.useRangeSlider and hasattr(self.imageViewer, 'rangeSlider') and self.imageViewer.rangeSlider is not None:
            self.imageViewer._onRangeSliderChange({
                'new': self.imageViewer.rangeSlider.value
            })
        elif not self.useRangeSlider and hasattr(self.imageViewer, 'vminSlider') and self.imageViewer.vminSlider is not None:
            self.imageViewer._onSeparateSlidersChange({
                'new': self.imageViewer.vminSlider.value
            })

        # 触发大小滑块更新，确保缩放倍数在图像切换时保持
        if hasattr(self.imageViewer, 'sizeSlider') and self.imageViewer.sizeSlider is not None:
            self.imageViewer._onSizeSliderChange({
                'new': self.imageViewer.sizeSlider.value
            })

    def display(self) -> None:
        """显示图像序列查看器"""
        display(self.combinedWidget)

    def getCurrentImage(self) -> np.ndarray:
        """
        获取当前选中的图像
        
        Returns:
            当前选中的图像数据
        """
        return self.imageSequence[self.selectWidget.value]

    def setCurrentIndex(self, index: int) -> None:
        """
        设置当前选中的图像索引

        Args:
            index: 图像索引
        """
        if 0 <= index < self.numImages:
            self.selectWidget.value = index
        else:
            raise ValueError(f"索引 {index} 超出范围 [0, {self.numImages-1}]")

    def updateImageSequence(self, newImageSequence: np.ndarray) -> None:
        """
        更新图像序列数据

        Args:
            newImageSequence: 新的图像序列，形状为 (z, y, x)
        """
        if newImageSequence.ndim == 2:
            # 如果是2D数组，转换为3D (1, y, x)
            newImageSequence = newImageSequence[np.newaxis, :, :]
        elif newImageSequence.ndim != 3:
            raise ValueError("newImageSequence 必须是二维或三维 numpy 数组")

        # 更新数据
        self.imageSequence = newImageSequence
        self.numImages = newImageSequence.shape[0]

        # 重新计算新图像序列的全局灰度范围
        self.globalRange = (float(newImageSequence.min()), float(newImageSequence.max()))

        # 更新ImageContrastViewer的全局范围
        self.imageViewer.global_range = self.globalRange

        # 重新创建选择控件
        self._createSelectWidget()

        # 更新图像查看器
        currentImageData = self.imageSequence[0]
        self.imageViewer.updateImageData(currentImageData)

        # 更新组合控件
        self.combinedWidget.children = [self.selectWidget, self.imageViewerWidget]

        # 触发图像更新
        self._triggerImageUpdate()

    def crop_sequence_interactive(self) -> None:
        """
        使用当前显示帧作为参考，对整个图像序列进行交互式裁剪

        该方法会：
        1. 获取当前显示的帧作为2D参考图像
        2. 将其归一化到0-255范围
        3. 使用CutFrameSelector进行交互式ROI选择
        4. 用裁剪结果更新整个图像序列
        """
        try:
            # 获取当前显示的帧（原始数据，不受SizeControl影响）
            current_frame = self.getCurrentImage()

            # 始终使用原始数据进行归一化，避免SizeControl的影响
            # 注意：不使用 imageViewer.dataDisplay，因为它会受到SizeControl缩放影响
            img2d = self._normalize_to_uint8(current_frame)

            # 确保img2d是2D数组
            if img2d.ndim != 2:
                raise ValueError(f"参考图像必须是2D数组，当前维度: {img2d.ndim}")

            # 使用完整的图像序列作为3D数据
            img3d = self.imageSequence

            # 创建CutFrameSelector实例
            self.crop_selector = CutFrameSelector(img2d, img3d)

            # 注册确认回调，点击确认后自动应用裁剪结果
            self.crop_selector.register_confirm_callback(self._on_crop_confirmed)

            # 显示ROI选择器
            self.crop_selector.display()

        except Exception as e:
            print(f"❌ 启动交互式裁剪时出错: {e}")
            raise

    def resize_interactive(self) -> None:
        try:

            # 创建CutFrameSelector实例
            self.resize_selector = ResizePopupWidget(self.imageSequence)

            # 注册确认回调，点击确认后自动应用裁剪结果
            self.resize_selector.register_confirm_callback(self._on_resize_confirm)

            # 显示ROI选择器
            self.resize_selector.display()
            
        except Exception as e:
            print(f"❌ 启动交互式裁剪时出错: {e}")
            raise

    def _normalize_to_uint8(self, image: np.ndarray) -> np.ndarray:
        """
        将图像归一化到0-255的uint8范围

        Args:
            image: 输入图像数组

        Returns:
            归一化后的uint8图像
        """
        # 使用全局范围进行归一化，确保一致性
        data_min, data_max = self.globalRange
        if data_max > data_min:
            normalized = np.interp(image, (data_min, data_max), (0, 255))
        else:
            normalized = np.zeros_like(image)

        return normalized.astype(np.uint8)

    def _on_crop_confirmed(self, crop_selector) -> None:
        """
        裁剪确认回调函数，自动应用裁剪结果

        Args:
            crop_selector: CutFrameSelector实例
        """
        try:
            # 获取裁剪结果
            result = crop_selector.get_result()

            if result is not None:
                # 更新图像序列
                self.updateImageSequence(result)

                # 清理裁剪选择器引用
                if hasattr(self, 'crop_selector'):
                    delattr(self, 'crop_selector')
            else:
                print("⚠️ 裁剪结果为空，无法自动应用")

        except Exception as e:
            print(f"❌ 自动应用裁剪结果时出错: {e}")
            import traceback
            traceback.print_exc()

    def check_crop_result(self) -> bool:
        """
        检查裁剪结果并应用到图像序列

        Returns:
            True如果裁剪成功并已应用，False如果尚未完成或失败
        """
        if not hasattr(self, 'crop_selector'):
            print("❌ 尚未启动交互式裁剪")
            return False

        # 获取裁剪结果
        result = self.crop_selector.get_result()
        status = self.crop_selector.get_status()

        print(f"📊 裁剪状态: {status}")

        if result is not None:
            try:
                # 更新图像序列
                self.updateImageSequence(result)
                # 清理裁剪选择器引用
                delattr(self, 'crop_selector')
                print("✅ 裁剪成功并已应用")
                return True
            except Exception as e:
                print(f"❌ 应用裁剪结果时出错: {e}")
                return False
        else:
            print("⏳ 裁剪尚未完成，请在ROI选择器中完成选择")
            return False

    def get_crop_status(self) -> str:
        """
        获取当前裁剪操作的状态

        Returns:
            状态描述字符串
        """
        if not hasattr(self, 'crop_selector'):
            return "未启动交互式裁剪"

        return self.crop_selector.get_status()

    def _on_resize_confirm(self, wgt: ResizePopupWidget) -> None:
        try:
            if not hasattr(self, 'resize_selector'):
                print("❌ 尚未启动交互式调整大小")
                return
            new_size = wgt.get_confirm_size()
            if new_size is not None:
                from scipy.ndimage import zoom
                old_shape = self.imageSequence.shape
                if len(new_size) == len(old_shape):
                    scale_factors = tuple(ns / os for ns, os in zip(new_size, old_shape))
                    print(f"缩放因子: {scale_factors}")
                    data = zoom(self.imageSequence, scale_factors, order=1)  # order=1双线性插值
                    self.updateImageSequence(data) # type: ignore
            delattr(self, 'resize_selector')
        except Exception as e:
            print(f"❌ 调整大小时出错: {e}")
            raise


if __name__ == "__main__":
    # 创建模拟的灰度图序列用于测试
    dummyImageSequence = np.random.randint(
        0, 256, size=(10, 100, 100), dtype=np.uint8
    )
    
    viewer = ImageSequenceViewer(dummyImageSequence)
    viewer.display()
