import numpy as np
from ipywidgets import FloatSlider, Output, interact, IntRangeSlider, widgets
from IPython.display import display
from PIL import Image
from io import BytesIO
from typing import Union, Tuple, Optional


class ImageContrastViewer:
    def __init__(self, data: np.ndarray) -> None:
        """
        初始化图像对比度查看器

        Args:
            data: 输入的图像数据，numpy数组，支持2D或3D（会自动压缩为2D）
        """
        self.data: np.ndarray = data
        # 确保数据是2维的
        if len(data.shape) == 3:
            self.data = data.squeeze()  # 移除大小为1的维度
        self.dataDisplay: np.ndarray = np.interp(
            self.data, (self.data.min(), self.data.max()), (0, 255)
        ).astype(np.uint8)
        self.imageWidget: widgets.Image = widgets.Image(
            format="jpeg"
        )  # 用于显示图像的 Image 控件
        self.plotOutput: Output = Output()  # 用于包裹 image_widget 和 print 输出

        # 初始化可能稍后创建的属性
        self.useRangeSlider: bool = False
        self.rangeSlider: Optional[IntRangeSlider] = None
        self.vminSlider: Optional[FloatSlider] = None
        self.vmaxSlider: Optional[FloatSlider] = None

    def updateImageData(self, newData: np.ndarray) -> None:
        """
        更新图像数据并刷新显示，而不重新创建滑块。
        """
        self.data = newData
        if len(self.data.shape) == 3:
            self.data = self.data.squeeze()
        self.dataDisplay = np.interp(
            self.data, (self.data.min(), self.data.max()), (0, 255)
        ).astype(np.uint8)
        # 触发滑块的更新，如果它们已经存在的话
        # 这里需要更复杂的逻辑来触发已存在的interact控件的更新，
        # 暂时先不实现，因为interact默认会重新创建控件

    def imResize(
        self, sizeRatio: Union[Tuple[float, float], Tuple[float], float] = (1, 1)
    ) -> None:
        """
        调整图像大小

        Args:
            sizeRatio: 缩放比例，可以是：
                      - (height_ratio, width_ratio): 分别指定高度和宽度缩放比例
                      - (ratio,): 统一缩放比例
                      - ratio: 统一缩放比例（单个数值）
        """
        if isinstance(sizeRatio, (int, float)):
            sizeRatio = (sizeRatio,)

        if len(sizeRatio) == 2:
            shape0 = round(self.dataDisplay.shape[0] * sizeRatio[0])
            shape1 = round(self.dataDisplay.shape[1] * sizeRatio[1])
        elif len(sizeRatio) == 1:
            shape0 = round(self.dataDisplay.shape[0] * sizeRatio[0])
            shape1 = round(self.dataDisplay.shape[1] * sizeRatio[0])
        else:
            raise ValueError(
                "sizeRatio must be a tuple of length 1 or 2, or a single number"
            )
        # 使用PIL进行图像缩放
        img_pil = Image.fromarray(self.dataDisplay, mode="L")
        img_resized = img_pil.resize(
            (shape1 // 8 * 8, shape0 // 8 * 8), resample=Image.LANCZOS
        )
        self.dataDisplay = np.array(img_resized).astype(np.uint8)

    def saveImage(self, filename: str = "./tmp/tmp_image.png") -> None:
        """
        保存当前显示的图像到文件

        Args:
            filename: 保存的文件路径，默认为'./tmp/tmp_image.png'
        """
        img = Image.fromarray(self.dataDisplay, mode="L")
        img.save(filename)

    def display(self, useRangeSlider: bool = False):
        """
        显示交互式图像对比度调节界面

        Args:
            useRangeSlider: 是否使用双滑动条，False则使用两个独立滑块

        创建滑块用于调节图像对比度，图像会根据滑块值实时更新显示
        """
        self.useRangeSlider = useRangeSlider

        if self.useRangeSlider:
            if self.rangeSlider is None:
                self._createRangeSlider()
        else:
            if self.vminSlider is None or self.vmaxSlider is None:
                self._createSeparateSliders()

        # 确保 plot_output 已经包含图像
        with self.plotOutput:
            # 初始显示图像，使用默认对比度
            if useRangeSlider:
                self._updateContrastImage(self.rangeSlider.value[0], self.rangeSlider.value[1])
            else:
                self._updateContrastImage(self.vminSlider.value, self.vmaxSlider.value)
            display(self.imageWidget)  # 第一次显示 image_widget

        if useRangeSlider:
            return widgets.VBox([self.rangeSlider, self.plotOutput])
        else:
            return widgets.VBox([widgets.HBox([self.vminSlider, self.vmaxSlider]), self.plotOutput])

    def _createRangeSlider(self) -> None:
        """创建范围滑块"""
        self.rangeSlider = IntRangeSlider(
            value=[0, 255],
            min=0,
            max=255,
            step=1,
            description="Contrast:",
            style={"description_width": "initial"},
            layout={"width": "600px"},
        )
        self.rangeSlider.observe(self._onRangeSliderChange, names="value")

    def _onRangeSliderChange(self, change) -> None:
        """范围滑块值变化回调"""
        vmin, vmax = change["new"]
        with self.plotOutput:
            self._updateContrastImage(vmin, vmax)

    def _createSeparateSliders(self) -> None:
        """创建独立滑块"""
        self.vminSlider = FloatSlider(
            min=0,
            max=100,
            step=1,
            value=0,
            description="Vmin:",
            style={"description_width": "initial"},
            layout={"width": "600px"},
        )
        self.vmaxSlider = FloatSlider(
            min=155,
            max=255,
            step=1,
            value=255,
            description="Vmax:",
            style={"description_width": "initial"},
            layout={"width": "600px"},
        )
        self.vminSlider.observe(self._onSeparateSlidersChange, names="value")
        self.vmaxSlider.observe(self._onSeparateSlidersChange, names="value")
        # self.separate_sliders_widget = VBox([self.vminSlider, self.vmaxSlider, self.plotOutput]) # 移除

    def _onSeparateSlidersChange(self, change) -> None:
        """独立滑块值变化回调"""
        vmin = self.vminSlider.value
        vmax = self.vmaxSlider.value
        with self.plotOutput:
            self._updateContrastImage(vmin, vmax)

    def _updateContrastImage(self, vmin: float, vmax: float) -> None:
        """
        根据给定的对比度范围更新并显示图像。
        """
        if vmin >= vmax:
            vmax = vmin + 1
        # 在NumPy数组上进行对比度调整
        adjusted_data = np.interp(self.dataDisplay, [vmin, vmax], [0, 255]).astype(
            np.uint8
        )
        img: Image.Image = Image.fromarray(adjusted_data, mode="L")
        # 将PIL图像转换为PNG格式的字节流
        buffered = BytesIO()
        img.save(buffered, format="jpeg", quality=80)
        self.imageWidget.value = buffered.getvalue()
        # print(f"Contrast: [{vmin:.0f}, {vmax:.0f}]")

    def _displayWithRangeSlider(self) -> None:
        """使用双滑动条（范围滑块）显示"""

        def updateContrastRange(contrastRange: Tuple[int, int] = (0, 255)) -> None:
            """
            使用范围滑块更新图像对比度

            Args:
                contrastRange: 对比度范围 (vmin, vmax)
            """
            vmin, vmax = contrastRange
            if vmin >= vmax:
                vmax = vmin + 1

            # 创建PIL图像用于调整对比度
            img: Image.Image = Image.fromarray(self.dataDisplay, mode="L")
            # 调整对比度
            img = img.point(lambda x: np.interp(x, [vmin, vmax], [0, 255]))
            # 直接显示PIL图像
            display(img)
            print(f"Contrast Range: [{vmin}, {vmax}]")

        # 创建范围滑块
        rangeSlider = IntRangeSlider(
            value=[0, 255],
            min=0,
            max=255,
            step=1,
            description="Contrast:",
            style={"description_width": "initial"},
            layout={"width": "600px"},  # 设置滑块宽度
        )

        interact(updateContrastRange, contrastRange=rangeSlider)

    def _displayWithSeparateSliders(self) -> None:
        """使用两个独立滑块显示"""

        def updateContrast(vmin: float = 0, vmax: float = 255) -> None:
            """
            更新图像对比度的回调函数

            Args:
                vmin: 对比度最小值 (0-100)
                vmax: 对比度最大值 (155-255)
            """
            if vmin >= vmax:
                vmax = vmin + 1
            # 创建PIL图像用于调整对比度
            img: Image.Image = Image.fromarray(self.dataDisplay, mode="L")
            # 调整对比度
            img = img.point(lambda x: np.interp(x, [vmin, vmax], [0, 255]))
            # 直接显示PIL图像
            display(img)
            # print(f"Contrast: [{vmin:.0f}, {vmax:.0f}]")

        # 创建交互式控件
        vminSlider = FloatSlider(
            min=0,
            max=100,
            step=1,
            value=0,
            description="Vmin:",
            style={"description_width": "initial"},
            layout={"width": "600px"},
        )
        vmaxSlider = FloatSlider(
            min=155,
            max=255,
            step=1,
            value=255,
            description="Vmax:",
            style={"description_width": "initial"},
            layout={"width": "600px"},
        )

        interact(updateContrast, vmin=vminSlider, vmax=vmaxSlider)


# 使用示例
if __name__ == "__main__":
    # 准备数据
    originalData: np.ndarray = np.random.rand(600, 800) * 1000 - 300
    viewer: ImageContrastViewer = ImageContrastViewer(originalData)

    # 使用双滑动条
    # viewer.display(useRangeSlider=True)

    # 或使用两个独立滑块（默认）
    viewer.display(useRangeSlider=False)
