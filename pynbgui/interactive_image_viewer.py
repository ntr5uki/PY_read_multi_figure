import ipywidgets as widgets
from IPython.display import display
import numpy as np
from typing import Optional
from .jupyter_array_selector import JupyterArraySelector
from .image_sequence_viewer import ImageSequenceViewer
from .roi_selector_pil import PILROISelector
from .horizontal_menu_bar import create_horizontal_menu_bar


class InteractiveImageViewer:
    """
    交互式图像查看器，结合了Jupyter数组选择器和图像序列查看器
    """

    def __init__(self, useRangeSlider: bool = True, showSizeControl: bool = True):
        """
        初始化交互式图像查看器

        Args:
            useRangeSlider: 是否使用范围滑块，默认为True
            showSizeControl: 是否显示图像大小控制，默认为True
        """
        self.useRangeSlider = useRangeSlider
        self.showSizeControl = showSizeControl
        self.imageViewer: Optional[ImageSequenceViewer] = None

        # 先创建状态显示和容器
        self.status_label = widgets.HTML(
            value="<i>请选择一个numpy数组开始查看图像</i>",
            layout=widgets.Layout(margin="10px 0"),
        )

        # 创建图像查看器容器
        self.viewer_container = widgets.VBox([])

        # 创建紧凑型菜单栏
        self.menu_bar, self.menu_panels = create_horizontal_menu_bar()
        (
            self.file_panel,
            self.operation_panel,
            self.tools_panel,
            self.help_panel,
        ) = self.menu_panels

        # 注册工具面板的ROI选择回调
        self.tools_panel.register_callback("roi_select", self._on_roi_menu_clicked)

        # 初始状态禁用ROI选择（没有图像时）
        self.tools_panel.set_menu_item_enabled("roi_select", False)

        # 创建ROI选择按钮
        self.roi_button = widgets.Button(
            description="🎯 选择ROI区域",
            button_style="success",
            tooltip="选择当前图像的感兴趣区域",
            disabled=True,  # 初始状态为禁用
            layout=widgets.Layout(width="150px", margin="5px 0"),
        )
        self.roi_button.on_click(self._on_roi_button_clicked)

        # 创建数组选择器（在其他组件创建之后）
        self.arraySelector = JupyterArraySelector(
            on_selection_change=self._on_array_selected
        )

        # 创建主界面
        self.main_widget = widgets.VBox(
            [
                widgets.HTML("<h3>📊 交互式图像查看器</h3>"),
                self.menu_bar,  # 紧凑型菜单栏
                self.roi_button,  # ROI按钮放在数组选择器上方
                self.arraySelector.main_widget,
                self.status_label,
                self.viewer_container,
            ]
        )

    def _on_array_selected(self, name: str, array: np.ndarray) -> None:
        """
        数组选择回调函数

        Args:
            name: 选择的数组变量名
            array: 选择的numpy数组
        """
        try:
            # 确保status_label已经初始化
            if not hasattr(self, "status_label") or self.status_label is None:
                print(f"⚠️ 状态标签未初始化，跳过数组选择: {name}")
                return

            # 检查数组维度
            if array.ndim == 2:
                # 2D数组，直接显示
                self.status_label.value = (
                    f"✅ 已选择2D数组 <b>{name}</b> - 形状: {array.shape}"
                )
                self._create_or_update_viewer(array)

            elif array.ndim == 3:
                # 3D数组，作为图像序列显示
                self.status_label.value = f"✅ 已选择3D数组 <b>{name}</b> - 形状: {array.shape} ({array.shape[0]}帧图像)"
                self._create_or_update_viewer(array)

            elif array.ndim == 4:
                # 4D数组，需要降维处理
                if array.shape[0] == 1:
                    # 第一维是1，可以squeeze
                    squeezed_array = array.squeeze()
                    if squeezed_array.ndim == 3:
                        self.status_label.value = f"✅ 已选择4D数组 <b>{name}</b> - 自动降维为: {squeezed_array.shape} ({squeezed_array.shape[0]}帧图像)"
                        self._create_or_update_viewer(squeezed_array)
                    else:
                        self.status_label.value = (
                            f"⚠️ 4D数组 <b>{name}</b> 降维后仍不是3D，无法显示"
                        )
                        self._clear_viewer()
                else:
                    # 取第一个切片
                    first_slice = array[0]
                    if first_slice.ndim == 3:
                        self.status_label.value = f"✅ 已选择4D数组 <b>{name}</b> - 显示第一个切片: {first_slice.shape} ({first_slice.shape[0]}帧图像)"
                        self._create_or_update_viewer(first_slice)
                    else:
                        self.status_label.value = (
                            f"⚠️ 4D数组 <b>{name}</b> 的切片不是3D，无法显示"
                        )
                        self._clear_viewer()
            else:
                self.status_label.value = (
                    f"❌ 数组 <b>{name}</b> 的维度({array.ndim}D)不支持显示"
                )
                self._clear_viewer()

        except Exception as e:
            if hasattr(self, "status_label") and self.status_label is not None:
                self.status_label.value = f"❌ 处理数组 <b>{name}</b> 时出错: {str(e)}"
            else:
                print(f"❌ 处理数组 {name} 时出错: {str(e)}")
            self._clear_viewer()

    def _create_or_update_viewer(self, array: np.ndarray) -> None:
        """
        创建或更新图像查看器

        Args:
            array: 要显示的numpy数组
        """
        try:
            if self.imageViewer is None:
                # 创建新的图像查看器
                self.imageViewer = ImageSequenceViewer(
                    array, self.useRangeSlider, self.showSizeControl
                )
                if (
                    hasattr(self, "viewer_container")
                    and self.viewer_container is not None
                ):
                    self.viewer_container.children = [self.imageViewer.combinedWidget]
            else:
                # 更新现有的图像查看器
                self.imageViewer.updateImageSequence(array)

            # 启用ROI按钮（图像查看器创建成功后）
            if hasattr(self, "roi_button") and self.roi_button is not None:
                self.roi_button.disabled = False

            # 启用工具面板的ROI选择项
            if hasattr(self, "tools_panel") and self.tools_panel is not None:
                self.tools_panel.set_menu_item_enabled("roi_select", True)

        except Exception as e:
            if hasattr(self, "status_label") and self.status_label is not None:
                self.status_label.value = f"❌ 创建图像查看器时出错: {str(e)}"
            else:
                print(f"❌ 创建图像查看器时出错: {str(e)}")
            self._clear_viewer()

    def _clear_viewer(self) -> None:
        """清除图像查看器"""
        self.imageViewer = None
        if hasattr(self, "viewer_container") and self.viewer_container is not None:
            self.viewer_container.children = []

        # 禁用ROI按钮（没有图像查看器时）
        if hasattr(self, "roi_button") and self.roi_button is not None:
            self.roi_button.disabled = True

        # 禁用工具面板的ROI选择项
        if hasattr(self, "tools_panel") and self.tools_panel is not None:
            self.tools_panel.set_menu_item_enabled("roi_select", False)

    def display(self) -> None:
        """显示交互式图像查看器"""
        display(self.main_widget)

    def refresh_arrays(self) -> None:
        """刷新可用的numpy数组列表"""
        self.arraySelector._refresh_arrays()

    def get_current_viewer(self) -> Optional[ImageSequenceViewer]:
        """
        获取当前的图像序列查看器

        Returns:
            当前的ImageSequenceViewer实例，如果没有则返回None
        """
        return self.imageViewer

    def _on_roi_menu_clicked(self, item_id: str, button) -> None:
        """
        菜单栏ROI选择回调函数

        Args:
            item_id: 菜单项ID
            button: 点击的按钮widget
        """
        print("🎯 从菜单栏触发ROI选择")
        # 调用原有的ROI按钮点击逻辑
        if self.imageViewer is None:
            print("❌ 请先选择一个图像数组")
            return
        self.imageViewer.crop_sequence_interactive()

    def _on_roi_button_clicked(self, button) -> None:
        """
        ROI按钮点击回调函数

        Args:
            button: 点击的按钮widget
        """
        try:
            # 获取当前显示的图像数据
            display_image = self._get_current_display_image()
            if display_image is None:
                self.status_label.value = "❌ 无法获取当前显示的图像数据"
                return

            # 获取当前图像信息用于显示
            current_frame_info = self._get_current_frame_info()

            # 创建并显示ROI选择器
            roi_selector = PILROISelector(display_image)
            roi_selector.display()

            # 存储ROI选择器引用，用于后续结果处理
            self.current_roi_selector = roi_selector

            # 更新状态显示
            self.status_label.value = (
                f"🎯 ROI选择器已打开 {current_frame_info}，请选择感兴趣区域后点击确认"
            )

        except Exception as e:
            self.status_label.value = f"❌ 打开ROI选择器时出错: {str(e)}"
            print(f"ROI选择器错误: {e}")

    def _get_current_frame_info(self) -> str:
        """
        获取当前帧的信息字符串

        Returns:
            当前帧信息的描述字符串
        """
        try:
            if self.imageViewer is None:
                return ""

            if (
                hasattr(self.imageViewer, "selectWidget")
                and self.imageViewer.selectWidget is not None
            ):
                current_index = self.imageViewer.selectWidget.value
                total_frames = self.imageViewer.numImages
                if total_frames > 1:
                    return f"(第{current_index + 1}帧，共{total_frames}帧)"
                else:
                    return "(单张图像)"

            return ""
        except Exception:
            return ""

    def get_last_roi_result(self) -> Optional[tuple]:
        """
        获取最后一次ROI选择的结果

        Returns:
            ROI坐标 (x_min, x_max, y_min, y_max) 或 None
        """
        if (
            hasattr(self, "current_roi_selector")
            and self.current_roi_selector is not None
        ):
            return self.current_roi_selector.roi_result
        return None

    def check_roi_status(self) -> str:
        """
        检查ROI选择状态并返回状态信息

        Returns:
            ROI选择状态的描述字符串
        """
        if (
            not hasattr(self, "current_roi_selector")
            or self.current_roi_selector is None
        ):
            return "尚未打开ROI选择器"

        roi_result = self.current_roi_selector.roi_result
        if roi_result is not None:
            x_min, x_max, y_min, y_max = roi_result
            width = x_max - x_min
            height = y_max - y_min
            area = width * height
            return f"✅ ROI已选择: 坐标({x_min}, {y_min}) 到 ({x_max}, {y_max}), 大小: {width}×{height}, 面积: {area}像素"
        elif self.current_roi_selector.is_cancelled:
            return "❌ ROI选择已取消"
        else:
            return "⏳ ROI选择器已打开，等待用户选择..."

    def _get_current_display_image(self) -> Optional[np.ndarray]:
        """
        获取当前显示的经过对比度调整的图像数据

        Returns:
            当前显示的图像数据（uint8格式），如果无法获取则返回None
        """
        try:
            # 检查图像查看器是否存在
            if self.imageViewer is None:
                return None

            # 检查ImageContrastViewer是否存在
            if (
                not hasattr(self.imageViewer, "imageViewer")
                or self.imageViewer.imageViewer is None
            ):
                return None

            # 获取经过对比度调整的显示数据
            contrast_viewer = self.imageViewer.imageViewer
            if (
                hasattr(contrast_viewer, "dataDisplay")
                and contrast_viewer.dataDisplay is not None
            ):
                return contrast_viewer.dataDisplay.copy()

            # 如果没有显示数据，尝试获取原始数据
            if hasattr(contrast_viewer, "data") and contrast_viewer.data is not None:
                # 将原始数据转换为uint8格式
                data = contrast_viewer.data
                if data.dtype != np.uint8:
                    # 简单的归一化到0-255范围
                    data_min, data_max = data.min(), data.max()
                    if data_max > data_min:
                        data = ((data - data_min) / (data_max - data_min) * 255).astype(
                            np.uint8
                        )
                    else:
                        data = np.zeros_like(data, dtype=np.uint8)
                return data.copy()

            return None

        except Exception as e:
            print(f"获取当前显示图像时出错: {e}")
            return None


# 便捷函数
def create_interactive_viewer(
    useRangeSlider: bool = True, showSizeControl: bool = True
) -> InteractiveImageViewer:
    """
    创建交互式图像查看器的便捷函数

    Args:
        useRangeSlider: 是否使用范围滑块，默认为True
        showSizeControl: 是否显示图像大小控制，默认为True

    Returns:
        InteractiveImageViewer实例
    """
    return InteractiveImageViewer(useRangeSlider, showSizeControl)


# 使用示例
if __name__ == "__main__":
    # 创建一些测试数据
    import numpy as np

    # 创建测试数组
    test_2d = np.random.rand(100, 100)
    test_3d = np.random.rand(10, 100, 100)
    test_4d = np.random.rand(1, 10, 100, 100)

    print("已创建测试数组:")
    print(f"test_2d: {test_2d.shape}")
    print(f"test_3d: {test_3d.shape}")
    print(f"test_4d: {test_4d.shape}")
    print("\n现在可以使用交互式查看器选择这些数组进行查看")

    # 创建交互式查看器
    viewer = create_interactive_viewer()
    viewer.display()
