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

        # 界面状态管理
        self._interface_state = {
            'saved_children': None,
            'current_mode': 'normal',  # normal, roi_selecting, resizing
            'temporary_widget': None,
            'is_locked': False
        }

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

        # 注册工具面板的调整大小回调
        self.tools_panel.register_callback("resize_select", self._on_resize_menu_clicked)

        # 初始状态禁用ROI选择（没有图像时）
        self.tools_panel.set_menu_item_enabled("roi_select", False)



        # 创建数组选择器（在其他组件创建之后）
        self.arraySelector = JupyterArraySelector(
            on_selection_change=self._on_array_selected
        )

        # 创建主界面
        self.main_widget = widgets.VBox(
            [
                widgets.HTML("<h3>📊 交互式图像查看器</h3>"),
                self.menu_bar,  # 紧凑型菜单栏
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

    def _enter_temporary_mode(self, mode: str, temporary_widget) -> bool:
        """
        进入临时界面模式

        Args:
            mode: 模式名称 ('roi_selecting', 'resizing', 等)
            temporary_widget: 要显示的临时widget

        Returns:
            True如果成功进入临时模式，False如果当前已在临时模式中
        """
        try:
            # 检查是否已经在临时模式中
            if self._interface_state['is_locked']:
                print("⚠️ 界面正在切换中，请稍候")
                return False

            if self._interface_state['current_mode'] != 'normal':
                print(f"⚠️ 当前正在{self._interface_state['current_mode']}模式中，请先完成当前操作")
                return False

            # 锁定界面状态
            self._interface_state['is_locked'] = True

            # 保存当前界面状态
            self._interface_state['saved_children'] = list(self.main_widget.children)
            self._interface_state['current_mode'] = mode
            self._interface_state['temporary_widget'] = temporary_widget

            # 切换到临时界面
            self.main_widget.children = [temporary_widget]

            print(f"✅ 已进入{mode}模式")
            return True

        except Exception as e:
            print(f"❌ 进入临时模式失败: {e}")
            self._interface_state['is_locked'] = False
            return False

    def _exit_temporary_mode(self) -> bool:
        """
        退出临时界面模式，恢复主界面

        Returns:
            True如果成功退出，False如果出现错误
        """
        try:
            # 恢复主界面
            if self._interface_state['saved_children'] is not None:
                self.main_widget.children = self._interface_state['saved_children']

            # 清理临时widget
            if self._interface_state['temporary_widget'] is not None:
                try:
                    # 尝试关闭临时widget（如果支持close方法）
                    if hasattr(self._interface_state['temporary_widget'], 'close'):
                        self._interface_state['temporary_widget'].close()
                except Exception as e:
                    print(f"⚠️ 清理临时widget时出错: {e}")

            # 重置状态
            old_mode = self._interface_state['current_mode']
            self._interface_state = {
                'saved_children': None,
                'current_mode': 'normal',
                'temporary_widget': None,
                'is_locked': False
            }

            print(f"✅ 已退出{old_mode}模式，恢复主界面")
            return True

        except Exception as e:
            print(f"❌ 退出临时模式失败: {e}")
            # 即使出错也要解锁
            self._interface_state['is_locked'] = False
            return False

    def _on_roi_menu_clicked(self, item_id: str, button) -> None:
        """
        菜单栏ROI选择回调函数

        Args:
            item_id: 菜单项ID
            button: 点击的按钮widget
        """
        print("🎯 从菜单栏触发ROI选择")

        # 检查前置条件
        if self.imageViewer is None:
            print("❌ 请先选择一个图像数组")
            return

        try:
            # 获取当前显示的帧作为参考图像
            current_frame = self.imageViewer.getCurrentImage()
            img2d = self.imageViewer._normalize_to_uint8(current_frame)

            # 创建ROI选择器
            from .image_cropper import CutFrameSelector
            crop_selector = CutFrameSelector(img2d, self.imageViewer.imageSequence)

            # 注册回调以在确认/取消后恢复界面
            crop_selector.register_confirm_callback(self._on_roi_confirmed)
            crop_selector.register_cancel_callback(self._on_roi_cancelled)

            # 进入临时模式
            if self._enter_temporary_mode('roi_selecting', crop_selector.roi_selector.main_container):
                # 保存crop_selector引用以便后续使用
                self._current_crop_selector = crop_selector
                print("🎯 ROI选择界面已显示")
            else:
                print("❌ 无法进入ROI选择模式")

        except Exception as e:
            print(f"❌ 启动ROI选择功能时出错: {e}")
            # 确保在出错时恢复界面
            self._exit_temporary_mode()

    def _on_roi_confirmed(self, crop_selector) -> None:
        """
        ROI选择确认回调函数

        Args:
            crop_selector: CutFrameSelector实例
        """
        try:
            print("✅ 用户确认了ROI选择操作")

            # 获取裁剪结果并应用到图像序列
            if crop_selector and self.imageViewer is not None:
                result = crop_selector.get_result()
                if result is not None:
                    print(f"🎯 应用ROI裁剪结果，新尺寸: {result.shape}")
                    # 更新图像序列
                    self.imageViewer.updateImageSequence(result)
                    # 更新界面显示信息
                    self._update_display_info_after_resize(result)

        except Exception as e:
            print(f"❌ 处理ROI确认时出错: {e}")
        finally:
            # 无论成功失败都要恢复界面
            self._cleanup_roi_operation()

    def _on_roi_cancelled(self, crop_selector) -> None:
        """
        ROI选择取消回调函数

        Args:
            crop_selector: CutFrameSelector实例
        """
        try:
            print("❌ 用户取消了ROI选择操作")
        except Exception as e:
            print(f"❌ 处理ROI取消时出错: {e}")
        finally:
            # 无论成功失败都要恢复界面
            self._cleanup_roi_operation()

    def _cleanup_roi_operation(self) -> None:
        """
        清理ROI选择操作的资源并恢复界面
        """
        try:
            # 清理crop_selector引用
            if hasattr(self, '_current_crop_selector'):
                self._current_crop_selector = None

            # 退出临时模式，恢复主界面
            self._exit_temporary_mode()

        except Exception as e:
            print(f"❌ 清理ROI选择操作时出错: {e}")

    def _on_resize_menu_clicked(self, item_id: str, button) -> None:
        """
        菜单栏调整大小回调函数

        Args:
            item_id: 菜单项ID
            button: 点击的按钮widget
        """
        print("🎯 从菜单栏触发调整大小")

        # 检查前置条件
        if self.imageViewer is None:
            print("❌ 请先选择一个图像数组")
            return

        try:
            # 创建调整大小选择器
            from .resize_dialog_widget import ResizePopupWidget
            resize_selector = ResizePopupWidget(self.imageViewer.imageSequence)

            # 注册回调以在确认/取消后恢复界面
            resize_selector.register_confirm_callback(self._on_resize_confirmed)
            resize_selector.register_cancel_callback(self._on_resize_cancelled)

            # 进入临时模式
            if self._enter_temporary_mode('resizing', resize_selector.main_container):
                # 保存resize_selector引用以便后续使用
                self._current_resize_selector = resize_selector
                print("📏 调整大小界面已显示")
            else:
                print("❌ 无法进入调整大小模式")

        except Exception as e:
            print(f"❌ 启动调整大小功能时出错: {e}")
            # 确保在出错时恢复界面
            self._exit_temporary_mode()

    def _on_resize_confirmed(self, button) -> None:
        """
        调整大小确认回调函数

        Args:
            button: 确认按钮widget
        """
        try:
            print("✅ 用户确认了调整大小操作")

            # 获取新尺寸并应用到图像序列
            if hasattr(self, '_current_resize_selector') and self._current_resize_selector:
                new_size = self._current_resize_selector.get_confirm_size()
                if new_size is not None and self.imageViewer is not None:
                    print(f"📏 将应用新尺寸: {new_size}")

                    # 实现实际的图像序列调整大小逻辑
                    try:
                        from scipy.ndimage import zoom
                        old_shape = self.imageViewer.imageSequence.shape
                        print(f"🔍 原始尺寸: {old_shape}")

                        # 确保新尺寸的维度与原始数据匹配
                        if len(new_size) == len(old_shape):
                            # 计算缩放因子
                            scale_factors = tuple(ns / os for ns, os in zip(new_size, old_shape))
                            print(f"🔍 缩放因子: {scale_factors}")

                            # 应用缩放
                            resized_data = zoom(self.imageViewer.imageSequence, scale_factors, order=1)
                            print(f"🔍 调整后尺寸: {resized_data.shape}")

                            # 更新图像序列
                            self.imageViewer.updateImageSequence(resized_data)
                            print("✅ 图像序列调整大小完成")

                            # 更新界面显示信息
                            self._update_display_info_after_resize(resized_data)

                        else:
                            print(f"❌ 尺寸维度不匹配：新尺寸{len(new_size)}维，原始数据{len(old_shape)}维")

                    except ImportError:
                        print("❌ 缺少scipy库，无法进行图像缩放")
                    except Exception as resize_error:
                        print(f"❌ 调整图像大小时出错: {resize_error}")
                else:
                    print("⚠️ 未获取到有效的新尺寸")

        except Exception as e:
            print(f"❌ 处理调整大小确认时出错: {e}")
        finally:
            # 无论成功失败都要恢复界面
            self._cleanup_resize_operation()

    def _on_resize_cancelled(self, button) -> None:
        """
        调整大小取消回调函数

        Args:
            button: 取消按钮widget
        """
        try:
            print("❌ 用户取消了调整大小操作")
        except Exception as e:
            print(f"❌ 处理调整大小取消时出错: {e}")
        finally:
            # 无论成功失败都要恢复界面
            self._cleanup_resize_operation()

    def _update_display_info_after_resize(self, resized_data: np.ndarray) -> None:
        """
        调整大小后更新界面显示信息

        Args:
            resized_data: 调整大小后的数据
        """
        try:
            # 获取当前选择的数组名称
            selected_name, _ = self.arraySelector.get_selected_array()
            if selected_name:
                # 更新JupyterArraySelector的数组缓存
                self.arraySelector.arrays[selected_name] = resized_data

                # 更新JupyterArraySelector的信息显示
                from .jupyter_array_selector import get_array_info
                info_text = get_array_info(resized_data)
                self.arraySelector.info_label.value = f"<b>{selected_name}</b>: {info_text}"

                # 注意：不修改下拉框选项，避免触发选择变化

                # 更新InteractiveImageViewer的状态显示
                if resized_data.ndim == 2:
                    self.status_label.value = f"✅ 已选择2D数组 <b>{selected_name}</b> - 形状: {resized_data.shape}"
                elif resized_data.ndim == 3:
                    self.status_label.value = f"✅ 已选择3D数组 <b>{selected_name}</b> - 形状: {resized_data.shape} ({resized_data.shape[0]}帧图像)"

                print("🔄 界面显示信息已更新")

        except Exception as e:
            print(f"❌ 更新显示信息时出错: {e}")

    def _cleanup_resize_operation(self) -> None:
        """
        清理调整大小操作的资源并恢复界面
        """
        try:
            # 清理resize_selector引用
            if hasattr(self, '_current_resize_selector'):
                self._current_resize_selector = None

            # 退出临时模式，恢复主界面
            self._exit_temporary_mode()

        except Exception as e:
            print(f"❌ 清理调整大小操作时出错: {e}")


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
