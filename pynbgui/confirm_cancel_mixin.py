#!/usr/bin/env python3
"""
确认取消按钮混入类

提供标准的确认和取消按钮功能，以及回调注册机制。
其他需要确认/取消功能的控件可以继承此类。
"""

import ipywidgets as widgets
from typing import Callable, Optional, List
from abc import ABC, abstractmethod


class ConfirmCancelMixin(ABC):
    """
    确认取消按钮混入类
    
    提供标准的确认和取消按钮，以及回调注册机制。
    子类需要实现 _on_confirm_action 和 _on_cancel_action 方法。
    """
    
    def __init__(self,
                 confirm_text: str = '确认选择',
                 cancel_text: str = '取消',
                 confirm_style: str = 'success',
                 cancel_style: str = 'danger',
                 button_width: str = '100px',
                 button_margin: str = '5px',
                 auto_close: bool = True):
        """
        初始化确认取消按钮

        Args:
            confirm_text: 确认按钮文本
            cancel_text: 取消按钮文本
            confirm_style: 确认按钮样式
            cancel_style: 取消按钮样式
            button_width: 按钮宽度
            button_margin: 按钮边距
            auto_close: 是否在确认/取消后自动关闭弹窗
        """
        # 状态管理
        self.is_cancelled = False
        self.is_confirmed = False
        self.is_closed = False

        # 外部回调函数列表
        self.confirm_callbacks: List[Callable] = []
        self.cancel_callbacks: List[Callable] = []

        # 弹窗相关
        self.main_container: Optional[widgets.Widget] = None
        self.auto_close_on_action: bool = auto_close  # 是否在动作后自动关闭
        
        # 创建确认按钮
        self.confirm_button = widgets.Button(
            description=confirm_text,
            button_style=confirm_style,
            layout=widgets.Layout(width=button_width, margin=button_margin)
        )
        
        # 创建取消按钮
        self.cancel_button = widgets.Button(
            description=cancel_text,
            button_style=cancel_style,
            layout=widgets.Layout(width=button_width, margin=button_margin)
        )
        
        # 按钮容器
        self.button_box = widgets.HBox([
            self.confirm_button,
            self.cancel_button
        ], layout=widgets.Layout(justify_content='center'))
        
        # 设置内部回调
        self._setup_button_callbacks()
    
    def _setup_button_callbacks(self) -> None:
        """设置按钮的内部回调"""
        self.confirm_button.on_click(self._internal_on_confirm)
        self.cancel_button.on_click(self._internal_on_cancel)
    
    def _internal_on_confirm(self, button) -> None:
        """内部确认回调，处理状态和调用外部回调"""
        try:
            # 更新状态
            self.is_confirmed = True
            self.is_cancelled = False
            
            # 调用子类的确认动作
            self._on_confirm_action(button)

            # 调用外部注册的确认回调
            for callback in self.confirm_callbacks:
                try:
                    callback(self)
                except Exception as e:
                    print(f"⚠️ 确认回调执行失败: {e}")

            # 如果启用自动关闭，则关闭弹窗
            if self.auto_close_on_action:
                self.close()
                    
        except Exception as e:
            print(f"❌ 确认操作失败: {e}")
            import traceback
            traceback.print_exc()
    
    def _internal_on_cancel(self, button) -> None:
        """内部取消回调，处理状态和调用外部回调"""
        try:
            # 更新状态
            self.is_cancelled = True
            self.is_confirmed = False
            
            # 调用子类的取消动作
            self._on_cancel_action(button)

            # 调用外部注册的取消回调
            for callback in self.cancel_callbacks:
                try:
                    callback(self, button)
                except Exception as e:
                    print(f"⚠️ 取消回调执行失败: {e}")

            # 如果启用自动关闭，则关闭弹窗
            if self.auto_close_on_action:
                self.close()
                    
        except Exception as e:
            print(f"❌ 取消操作失败: {e}")
            import traceback
            traceback.print_exc()
    
    @abstractmethod
    def _on_confirm_action(self, button) -> None:
        """
        子类需要实现的确认动作
        
        Args:
            button: 按钮widget实例
        """
        pass
    
    @abstractmethod
    def _on_cancel_action(self, button) -> None:
        """
        子类需要实现的取消动作
        
        Args:
            button: 按钮widget实例
        """
        pass
    
    def register_confirm_callback(self, callback: Callable) -> None:
        """
        注册确认按钮的回调函数
        
        Args:
            callback: 回调函数，接收button参数
        """
        self.confirm_callbacks.append(callback)
    
    def register_cancel_callback(self, callback: Callable) -> None:
        """
        注册取消按钮的回调函数
        
        Args:
            callback: 回调函数，接收button参数
        """
        self.cancel_callbacks.append(callback)
    
    def remove_confirm_callback(self, callback: Callable) -> bool:
        """
        移除确认回调函数
        
        Args:
            callback: 要移除的回调函数
            
        Returns:
            True如果成功移除，False如果回调不存在
        """
        try:
            self.confirm_callbacks.remove(callback)
            return True
        except ValueError:
            return False
    
    def remove_cancel_callback(self, callback: Callable) -> bool:
        """
        移除取消回调函数
        
        Args:
            callback: 要移除的回调函数
            
        Returns:
            True如果成功移除，False如果回调不存在
        """
        try:
            self.cancel_callbacks.remove(callback)
            return True
        except ValueError:
            return False
    
    def clear_confirm_callbacks(self) -> None:
        """清除所有确认回调函数"""
        self.confirm_callbacks.clear()
    
    def clear_cancel_callbacks(self) -> None:
        """清除所有取消回调函数"""
        self.cancel_callbacks.clear()
    
    def reset_state(self) -> None:
        """重置确认/取消状态"""
        self.is_confirmed = False
        self.is_cancelled = False
    
    def get_button_box(self) -> widgets.HBox:
        """
        获取按钮容器widget
        
        Returns:
            包含确认和取消按钮的HBox容器
        """
        return self.button_box
    
    def set_button_enabled(self, confirm_enabled: bool = True, cancel_enabled: bool = True) -> None:
        """
        设置按钮的启用状态
        
        Args:
            confirm_enabled: 确认按钮是否启用
            cancel_enabled: 取消按钮是否启用
        """
        self.confirm_button.disabled = not confirm_enabled
        self.cancel_button.disabled = not cancel_enabled
    
    def set_button_descriptions(self, confirm_text: Optional[str] = None, cancel_text: Optional[str] = None) -> None:
        """
        设置按钮文本
        
        Args:
            confirm_text: 确认按钮文本，None表示不修改
            cancel_text: 取消按钮文本，None表示不修改
        """
        if confirm_text is not None:
            self.confirm_button.description = confirm_text
        if cancel_text is not None:
            self.cancel_button.description = cancel_text
    
    def get_status(self) -> str:
        """
        获取当前状态描述

        Returns:
            状态描述字符串
        """
        if self.is_closed:
            return "已关闭"
        elif self.is_confirmed:
            return "已确认"
        elif self.is_cancelled:
            return "已取消"
        else:
            return "等待用户操作"

    def close(self) -> None:
        """
        关闭弹窗/组件

        子类可以重写此方法来实现自定义的关闭逻辑
        """
        if not self.is_closed:
            self.is_closed = True
            self._close_widget()

    def _close_widget(self) -> None:
        """
        实际的关闭操作，子类可以重写

        默认实现：如果有main_container且支持close方法，则调用close
        """
        if self.main_container and hasattr(self.main_container, 'close'):
            try:
                self.main_container.close()
            except Exception as e:
                print(f"⚠️ 关闭组件时出错: {e}")

    def set_auto_close(self, auto_close: bool) -> None:
        """
        设置是否在确认/取消后自动关闭

        Args:
            auto_close: 是否自动关闭
        """
        self.auto_close_on_action = auto_close

    def set_main_container(self, container: widgets.Widget) -> None:
        """
        设置主容器widget

        Args:
            container: 主容器widget，用于关闭操作
        """
        self.main_container = container

    def is_widget_closed(self) -> bool:
        """
        检查组件是否已关闭

        Returns:
            True如果已关闭，False如果仍然打开
        """
        return self.is_closed


class ConfirmCancelWidget(ConfirmCancelMixin):
    """
    独立的确认取消按钮组件
    
    可以作为独立的widget使用，也可以作为其他组件的一部分。
    """
    
    def __init__(self, 
                 confirm_text: str = '确认',
                 cancel_text: str = '取消',
                 on_confirm: Optional[Callable] = None,
                 on_cancel: Optional[Callable] = None,
                 **kwargs):
        """
        初始化独立的确认取消按钮组件
        
        Args:
            confirm_text: 确认按钮文本
            cancel_text: 取消按钮文本
            on_confirm: 确认回调函数
            on_cancel: 取消回调函数
            **kwargs: 传递给父类的其他参数
        """
        super().__init__(confirm_text=confirm_text, cancel_text=cancel_text, **kwargs)
        
        # 设置主容器为按钮容器（独立组件）
        self.set_main_container(self.button_box)

        # 注册外部回调
        if on_confirm:
            self.register_confirm_callback(on_confirm)
        if on_cancel:
            self.register_cancel_callback(on_cancel)
    
    def _on_confirm_action(self, button) -> None:
        """确认动作实现"""
        print(f"✅ 确认操作")
    
    def _on_cancel_action(self, button) -> None:
        """取消动作实现"""
        print(f"❌ 取消操作")
    
    def display(self):
        """显示按钮组件"""
        from IPython.display import display
        display(self.button_box)
        return self
