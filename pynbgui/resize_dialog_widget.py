import ipywidgets as widgets
import numpy as np
from typing import Tuple, Optional, override
from .confirm_cancel_mixin import ConfirmCancelMixin
from simpleeval import simple_eval

class ResizePopupWidget(ConfirmCancelMixin):
    def __init__(self, imgin: np.ndarray):
        super().__init__() # 确保调用父类的构造函数以初始化 self.content
        self.imgin = imgin
        self.confirmSize: Optional[Tuple[int, ...]] = None

        # 创建文本输入框
        self.size_input = widgets.Text(
            value=str(imgin.shape),
            description='新尺寸:',
            disabled=False
        )

        # 创建主容器，并将输入框和按钮添加到其中
        self.main_container = widgets.VBox([
            self.size_input,
            self.button_box
        ])
        # 将主容器设置为mixin的显示内容
        if self.main_container is None:
            raise ValueError("主容器未设置，请检查代码逻辑")
        self.set_main_container(self.main_container)
        self.register_confirm_callback(self._confirm_action)

    def _confirm_action(self, button) -> None:
        """确认按钮的实际动作"""
        try:
            input_str = self.size_input.value.strip()
            parts = input_str.strip('()').split(',')
            parsed_shape_list = []
            for p in parts:
                p_stripped = p.strip()
                if p_stripped:
                    try:
                        # 使用 simpleeval 安全地评估数学表达式
                        evaluated_value = simple_eval(p_stripped)
                        parsed_shape_list.append(round(float(evaluated_value)))
                    except (SyntaxError, NameError, TypeError) as e:
                        raise ValueError(f"无效的尺寸表达式 '{p_stripped}': {e}")
            parsed_shape = tuple(parsed_shape_list)
            self.confirmSize = parsed_shape
        except ValueError:
            print("无效的尺寸输入格式，请使用 (H, W) 或 (D, H, W) 格式")
            self.confirmSize = None # 设置为None表示解析失败

    @override
    def _on_confirm_action(self, button) -> None:
        pass
      
    def _on_cancel_action(self, button) -> None:
        """取消按钮的实际动作"""
        # 根据要求，取消没有任何动作
        pass

    def get_confirm_size(self) -> Optional[Tuple[int, ...]]:
        return self.confirmSize

    def display(self) -> None:
        """显示弹窗"""
        from IPython.display import display
        display(self.main_container)

if __name__ == "__main__":
    imgin = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
    popup = ResizePopupWidget(imgin)
    popup.display()