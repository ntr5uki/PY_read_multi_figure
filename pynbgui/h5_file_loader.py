import ipywidgets as widgets
from IPython.display import display
from IPython import get_ipython
import ipyfilechooser
import numpy as np
from typing import Optional


class H5FileLoader:
    """
    H5文件加载器类，提供图形界面选择和加载H5文件到Jupyter变量空间
    """
    
    def __init__(self, default_path: str = ""):
        """
        初始化H5文件加载器
        
        Args:
            default_path: 默认的文件路径
        """
        self.default_path = default_path
        self.file_chooser: Optional[ipyfilechooser.FileChooser] = None
        self.load_button: Optional[widgets.Button] = None
        self.output: Optional[widgets.Output] = None
        self.main_widget: Optional[widgets.Widget] = None
        
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """创建界面控件"""
        # 创建文件选择器
        self.file_chooser = ipyfilechooser.FileChooser(
            path=self.default_path if self.default_path else ".",
            filename='',
            title='选择H5文件:',
            select_desc='选择',
            change_desc='更改'
        )
        
        # 设置文件过滤器，只显示.h5文件
        self.file_chooser.filter_pattern = '*.h5'
        
        # 创建加载按钮
        self.load_button = widgets.Button(
            description='📁 加载H5数据',
            button_style='primary',
            tooltip='将选择的H5文件加载到Jupyter变量空间',
            layout=widgets.Layout(width='150px', height='35px')
        )
        
        # 创建输出区域
        self.output = widgets.Output()
        
        # 绑定按钮点击事件
        self.load_button.on_click(self._on_load_button_clicked)
        
        # 创建主界面布局
        self.main_widget = widgets.VBox([
            self.file_chooser,
            widgets.HBox([
                self.load_button,
                widgets.HTML(value="<span style='margin-left: 10px; line-height: 35px;'>选择.h5文件后点击加载</span>")
            ]),
            self.output
        ])
    
    def _on_load_button_clicked(self, button: widgets.Button) -> None:
        """
        加载按钮点击回调函数
        
        Args:
            button: 被点击的按钮控件
        """
        with self.output:
            self.output.clear_output()
            
            # 获取选择的文件路径
            selected_file = self.file_chooser.selected
            
            if not selected_file:
                print("❌ 请先选择一个H5文件")
                return
            
            if not selected_file.endswith('.h5'):
                print("❌ 请选择一个.h5文件")
                return
            
            # 加载H5数据
            self._load_h5_data(selected_file)
    
    def _load_h5_data(self, file_path: str) -> None:
        """
        加载H5数据到Jupyter变量空间
        
        Args:
            file_path: H5文件路径
        """
        try:
            # 导入H5加载函数
            from .fcn_file_nudft import loadH5DataAll
            
            print(f"🔄 正在加载H5文件: {file_path}")
            
            # 加载H5数据
            data, dataSetlist, listKey = loadH5DataAll(file_path)
            
            # 获取IPython实例
            ip = get_ipython()
            if ip is None:
                print("❌ 错误: 未检测到IPython环境")
                return
            
            # 将数据分配到Jupyter变量空间
            variable_count = 0
            for key, value in data.items():
                ip.user_ns[key] = value
                variable_count += 1
            
            # 输出加载结果
            print(f"✅ 成功加载 {variable_count} 个数据集到Jupyter变量空间:")
            print("-" * 50)
            
            for i, dataset_name in enumerate(dataSetlist, 1):
                if isinstance(data[dataset_name], np.ndarray):
                    shape_str = " × ".join(map(str, data[dataset_name].shape))
                    print(f"  {i:2d}. {dataset_name:10s}: [{shape_str}] ({data[dataset_name].dtype})")
                else:
                    print(f"  {i:2d}. {dataset_name:10s}: {type(data[dataset_name]).__name__}")
            
            print("-" * 50)
            print(f"💡 现在您可以直接使用这些变量名称: {', '.join(dataSetlist)}")
            
            
        except ImportError as e:
            print(f"❌ 导入错误: {e}")
            print("请确保 fcn_file_nudft 模块可用")
        except Exception as e:
            print(f"❌ 加载H5文件时发生错误: {e}")
    
    def display(self) -> None:
        """显示文件加载器界面"""
        display(self.main_widget)
    
   
    def get_selected_file(self) -> Optional[str]:
        """
        获取当前选择的文件路径
        
        Returns:
            选择的文件路径，如果没有选择则返回None
        """
        return self.file_chooser.selected if self.file_chooser else None
    
    def set_path(self, path: str) -> None:
        """
        设置文件选择器的路径
        
        Args:
            path: 新的路径
        """
        if self.file_chooser:
            self.file_chooser.reset(path=path)
    
def create_h5_loader(default_path: str = "") -> H5FileLoader:
    """
    创建并返回H5文件加载器实例
    
    Args:
        default_path: 默认路径
        
    Returns:
        H5FileLoader实例
    """
    return H5FileLoader(default_path)


def refresh_jupyter_variables() -> None:
    """
    独立函数：强制刷新Jupyter变量浏览器
    
    用法:
        from pynbgui import refresh_jupyter_variables
        refresh_jupyter_variables()
    """
    try:
        ip = get_ipython()
        if ip is not None:
            # 执行多种刷新策略
            try:
                ip.run_line_magic('who', '')
            except:
                pass
            
            try:
                # 创建并删除临时变量来触发刷新
                ip.user_ns['_temp_refresh'] = "refresh"
                del ip.user_ns['_temp_refresh']
            except:
                pass
            
            print("🔄 Jupyter变量浏览器刷新完成")
        else:
            print("❌ 未检测到IPython环境")
    except Exception as e:
        print(f"⚠️ 刷新失败: {e}")
        print("💡 提示: 运行任意代码行可手动刷新变量浏览器")


# 使用示例
if __name__ == "__main__":
    # 创建H5文件加载器
    loader = H5FileLoader()
    
    # 显示界面
    loader.display() 