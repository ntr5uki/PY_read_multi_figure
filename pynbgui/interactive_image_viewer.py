import ipywidgets as widgets
from IPython.display import display
import numpy as np
from typing import Optional

from .jupyter_array_selector import JupyterArraySelector
from .image_sequence_viewer import ImageSequenceViewer


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
            layout=widgets.Layout(margin='10px 0')
        )

        # 创建图像查看器容器
        self.viewer_container = widgets.VBox([])

        # 创建数组选择器（在其他组件创建之后）
        self.arraySelector = JupyterArraySelector(
            on_selection_change=self._on_array_selected
        )

        # 创建主界面
        self.main_widget = widgets.VBox([
            widgets.HTML("<h3>📊 交互式图像查看器</h3>"),
            self.arraySelector.main_widget,
            self.status_label,
            self.viewer_container
        ])
    
    def _on_array_selected(self, name: str, array: np.ndarray) -> None:
        """
        数组选择回调函数

        Args:
            name: 选择的数组变量名
            array: 选择的numpy数组
        """
        try:
            # 确保status_label已经初始化
            if not hasattr(self, 'status_label') or self.status_label is None:
                print(f"⚠️ 状态标签未初始化，跳过数组选择: {name}")
                return

            # 检查数组维度
            if array.ndim == 2:
                # 2D数组，直接显示
                self.status_label.value = f"✅ 已选择2D数组 <b>{name}</b> - 形状: {array.shape}"
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
                        self.status_label.value = f"⚠️ 4D数组 <b>{name}</b> 降维后仍不是3D，无法显示"
                        self._clear_viewer()
                else:
                    # 取第一个切片
                    first_slice = array[0]
                    if first_slice.ndim == 3:
                        self.status_label.value = f"✅ 已选择4D数组 <b>{name}</b> - 显示第一个切片: {first_slice.shape} ({first_slice.shape[0]}帧图像)"
                        self._create_or_update_viewer(first_slice)
                    else:
                        self.status_label.value = f"⚠️ 4D数组 <b>{name}</b> 的切片不是3D，无法显示"
                        self._clear_viewer()
            else:
                self.status_label.value = f"❌ 数组 <b>{name}</b> 的维度({array.ndim}D)不支持显示"
                self._clear_viewer()

        except Exception as e:
            if hasattr(self, 'status_label') and self.status_label is not None:
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
                    array,
                    self.useRangeSlider,
                    self.showSizeControl
                )
                if hasattr(self, 'viewer_container') and self.viewer_container is not None:
                    self.viewer_container.children = [self.imageViewer.combinedWidget]
            else:
                # 更新现有的图像查看器
                self.imageViewer.updateImageSequence(array)

        except Exception as e:
            if hasattr(self, 'status_label') and self.status_label is not None:
                self.status_label.value = f"❌ 创建图像查看器时出错: {str(e)}"
            else:
                print(f"❌ 创建图像查看器时出错: {str(e)}")
            self._clear_viewer()

    def _clear_viewer(self) -> None:
        """清除图像查看器"""
        self.imageViewer = None
        if hasattr(self, 'viewer_container') and self.viewer_container is not None:
            self.viewer_container.children = []
    
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


# 便捷函数
def create_interactive_viewer(useRangeSlider: bool = True, showSizeControl: bool = True) -> InteractiveImageViewer:
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
