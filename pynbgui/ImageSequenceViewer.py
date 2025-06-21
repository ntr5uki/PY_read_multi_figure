import ipywidgets as widgets
from IPython.display import display
import numpy as np

# 使用相对导入，更简洁
from .image_contrast_viewer import ImageContrastViewer


class ImageSequenceViewer:
    def __init__(self, imageSequence: np.ndarray, useRangeSlider: bool = True):
        """
        初始化图像序列查看器。

        Args:
            imageSequence: 灰度图序列，形状为 (z, y, x)
            useRangeSlider: 是否使用范围滑块，默认为True
        """
        if imageSequence.ndim != 3:
            raise ValueError("imageSequence 必须是三维 numpy 数组 (z, y, x)")

        self.imageSequence = imageSequence
        self.numImages = imageSequence.shape[0]
        self.useRangeSlider = useRangeSlider
        
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
            layout=widgets.Layout(width='150px')
        )
        self.selectWidget.observe(self._onValueChange, names='value')

    def _createImageViewer(self) -> None:
        """创建图像查看器"""
        # 获取初始图像（第一张）
        currentImageData = self.imageSequence[0]
        self.imageViewer = ImageContrastViewer(currentImageData)
        
        # 获取图像查看器的widget
        self.imageViewerWidget = self.imageViewer.display(useRangeSlider=self.useRangeSlider)

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
        if self.useRangeSlider and hasattr(self.imageViewer, 'rangeSlider'):
            self.imageViewer._onRangeSliderChange({
                'new': self.imageViewer.rangeSlider.value
            })
        elif not self.useRangeSlider and hasattr(self.imageViewer, 'vminSlider'):
            self.imageViewer._onSeparateSlidersChange({
                'new': self.imageViewer.vminSlider.value
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


if __name__ == "__main__":
    # 创建模拟的灰度图序列用于测试
    dummyImageSequence = np.random.randint(
        0, 256, size=(10, 100, 100), dtype=np.uint8
    )
    
    viewer = ImageSequenceViewer(dummyImageSequence)
    viewer.display()
