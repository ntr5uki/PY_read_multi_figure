import ipywidgets as widgets
from IPython.display import display
import numpy as np
from typing import Dict, Tuple, Optional, Callable, Any
import inspect

try:
    from IPython import get_ipython
except ImportError:
    def get_ipython():
        return None


def get_jupyter_numpy_arrays() -> Dict[str, np.ndarray]:
    """
    获取Jupyter工作区中的所有numpy数组变量

    Returns:
        包含变量名和numpy数组的字典
    """
    try:
        ip = get_ipython()
        if ip is None:
            # 如果不在IPython环境中，尝试从调用者的全局命名空间获取
            frame = inspect.currentframe()
            try:
                # 获取调用者的全局命名空间
                if frame and frame.f_back:
                    caller_globals = frame.f_back.f_globals
                    numpy_arrays = {}
                    for var_name, var_value in caller_globals.items():
                        if (not var_name.startswith('_') and
                            isinstance(var_value, np.ndarray) and
                            var_value.ndim >= 2):
                            numpy_arrays[var_name] = var_value
                    return numpy_arrays
                return {}
            finally:
                del frame

        numpy_arrays = {}
        if hasattr(ip, 'user_ns'):
            for var_name, var_value in ip.user_ns.items():
                # 过滤掉私有变量和内置变量
                if (not var_name.startswith('_') and
                    isinstance(var_value, np.ndarray) and
                    var_value.ndim >= 2):  # 至少是2维数组
                    numpy_arrays[var_name] = var_value

        return numpy_arrays
    except Exception as e:
        print(f"获取numpy数组时出错: {e}")
        return {}


def get_array_info(array: np.ndarray) -> str:
    """
    获取数组的信息字符串
    
    Args:
        array: numpy数组
        
    Returns:
        包含形状、数据类型和内存大小的信息字符串
    """
    memory_mb = array.nbytes / (1024 * 1024)
    return f"形状: {array.shape}, 类型: {array.dtype}, 内存: {memory_mb:.1f}MB"


class JupyterArraySelector:
    """
    Jupyter工作区numpy数组选择器
    """
    
    def __init__(self, on_selection_change: Optional[Callable[[str, np.ndarray], None]] = None):
        """
        初始化数组选择器
        
        Args:
            on_selection_change: 选择变化时的回调函数，接收(变量名, 数组)参数
        """
        self.on_selection_change = on_selection_change
        self.arrays: Dict[str, np.ndarray] = {}
        
        # 创建控件
        self._create_widgets()
        self._refresh_arrays()
    
    def _create_widgets(self) -> None:
        """创建界面控件"""
        # 数组选择下拉框
        self.array_dropdown = widgets.Dropdown(
            options=[],
            description='选择数组:',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='400px')
        )
        
        # 刷新按钮
        self.refresh_button = widgets.Button(
            description='🔄 刷新',
            button_style='info',
            tooltip='刷新工作区中的numpy数组列表',
            layout=widgets.Layout(width='80px')
        )
        
        # 信息显示区域
        self.info_label = widgets.HTML(
            value="<i>请选择一个数组</i>",
            layout=widgets.Layout(width='500px')
        )
        
        # 绑定事件
        self.array_dropdown.observe(self._on_array_selection_change, names='value')
        self.refresh_button.on_click(self._on_refresh_clicked)
        
        # 创建主界面
        self.main_widget = widgets.VBox([
            widgets.HBox([self.array_dropdown, self.refresh_button]),
            self.info_label
        ])
    
    def _refresh_arrays(self) -> None:
        """刷新工作区中的numpy数组列表"""
        self.arrays = get_jupyter_numpy_arrays()
        
        if self.arrays:
            # 创建选项列表，显示数组名称和基本信息
            options = []
            for name, array in self.arrays.items():
                label = f"{name} - {array.shape}"
                options.append((label, name))
            
            self.array_dropdown.options = options
            
            # 如果有数组，默认选择第一个
            if options:
                self.array_dropdown.value = options[0][1]
        else:
            self.array_dropdown.options = [("没有找到numpy数组", None)]
            self.info_label.value = "<span style='color: orange;'>⚠️ 工作区中没有找到numpy数组</span>"
    
    def _on_refresh_clicked(self, button: Any) -> None:
        """刷新按钮点击回调"""
        self._refresh_arrays()
        print("🔄 已刷新numpy数组列表")
    
    def _on_array_selection_change(self, change: dict) -> None:
        """数组选择变化回调"""
        selected_name = change['new']

        if selected_name and selected_name in self.arrays:
            selected_array = self.arrays[selected_name]

            # 更新信息显示
            info_text = get_array_info(selected_array)
            self.info_label.value = f"<b>{selected_name}</b>: {info_text}"

            # 调用回调函数（添加异常处理）
            if self.on_selection_change:
                try:
                    self.on_selection_change(selected_name, selected_array)
                except Exception as e:
                    print(f"⚠️ 回调函数执行出错: {e}")
        else:
            self.info_label.value = "<i>请选择一个有效的数组</i>"
    
    def get_selected_array(self) -> Tuple[Optional[str], Optional[np.ndarray]]:
        """
        获取当前选择的数组
        
        Returns:
            (变量名, 数组) 的元组，如果没有选择则返回 (None, None)
        """
        selected_name = self.array_dropdown.value
        if selected_name and selected_name in self.arrays:
            return selected_name, self.arrays[selected_name]
        return None, None
    
    def display(self) -> None:
        """显示选择器界面"""
        display(self.main_widget)


# 使用示例
if __name__ == "__main__":
    def on_array_selected(name: str, array: np.ndarray) -> None:
        print(f"选择了数组: {name}, 形状: {array.shape}")
    
    selector = JupyterArraySelector(on_selection_change=on_array_selected)
    selector.display()
