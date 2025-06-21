import numpy as np
from multiprocessing.connection import Listener, Connection, Client
from typing import Any, Tuple, Union


class DataTransfer:
    """
    一个用于接收和发送数据包的类。
    """

    def __init__(
        self,
        address: Tuple[str, int] = ("localhost", 6000),
        authKey: bytes = b"mySecretDebugKey",
    ):
        """
        初始化数据传输器。

        参数:
            address (Tuple[str, int]): 监听和连接的地址 (主机名, 端口号)。
            authKey (bytes): 用于连接认证的密钥。
        """
        self.serverAddress: Tuple[str, int] = address
        self.authKey: bytes = authKey

    def receiveSingleData(self) -> Union[Any, None]:
        """
        启动监听器，等待一个生产者连接，接收单个数据包，并返回其 'value'。
        此方法会阻塞，直到接收到数据或发生错误。

        返回:
            Union[Any, None]: 接收到的数据包中的 'value'，如果接收失败则返回 None。
        """
        listener = Listener(self.serverAddress, authkey=self.authKey)
        print(f"数据传输器: 正在监听地址 {self.serverAddress} ...")
        receivedValue: Union[Any, None] = None
        try:
            print("数据传输器: 等待发送者连接...")
            clientConn: Connection = listener.accept()
            print("数据传输器: 已接受来自发送者的连接。")
            try:
                msg: Any = clientConn.recv()
                print(f"数据传输器: 接收到数据: {msg}")
                receivedValue = msg # 直接接收数据
            except EOFError:
                print("数据传输器: 发送者已断开连接。")
            except ConnectionResetError:
                print("数据传输器: 连接被发送者重置。")
            except Exception as e:
                print(f"数据传输器: 接收数据时发生错误: {e}")
            finally:
                clientConn.close()
                print("数据传输器: 与发送者的连接已关闭。")

        except Exception as e:
            print(f"数据传输器: 监听器发生错误或被中断: {e}")
        finally:
            listener.close()
            print("数据传输器: 监听器已关闭。")

        return receivedValue

    def sendData(
        self,
        value: Any,
    ) -> None:
        """
        连接到监听器并发送数据。

        参数:
            value (Any): 要发送的数据 (必须是可pickle化的)。
            message (str): 附加的调试信息。
            id (int): 数据的唯一标识符。
        """
        # 直接发送 value，而不是封装成字典
        data: Any = value
        try:
            conn = Client(self.serverAddress, authkey=self.authKey)
            conn.send(data)
            print(f"数据传输器: 已发送数据: {data}")
            conn.close()
        except ConnectionRefusedError:
            print(
                f"数据传输器: 连接被拒绝。请确保接收方正在运行并且监听地址 {self.serverAddress}。"
            )
        except Exception as e:
            print(f"数据传输器: 发送数据时发生错误: {e}")


if __name__ == "__main__":
    # 实例化 DataTransfer 类
    dataTransfer = DataTransfer()

    # 示例：作为消费者接收数据
    # print("\n--- 作为消费者接收数据 ---")
    # receivedDebugValue: Union[Any, None] = dataTransfer.receiveSingleData()
    # if receivedDebugValue is not None:
    #     print(f"\n接收结果: 成功接收到 value。类型: {type(receivedDebugValue)}")
    #     if isinstance(receivedDebugValue, np.ndarray):
    #         print(f"形状: {receivedDebugValue.shape}")
    # else:
    #     print("\n接收结果: 未能接收到 value。")

    # 示例：作为生产者发送数据
    print("\n--- 作为生产者发送数据 ---")
    dataTransfer.sendData(
        value=np.random.rand(512, 512, 100),
        # message="来自数据传输器的调试信息！", # 这些参数现在不会被使用
        # id=1,
    )
    print("数据传输器: 数据发送完毕。")


def assignin_global(data_dict: dict) -> None:
    """
    将字典中的所有键值对分配到全局命名空间中，类似 MATLAB 的 assignin('base', ...)
    
    参数:
        data_dict (dict): 包含变量名和值的字典
    """
    globals().update(data_dict)
    print(f"已将 {len(data_dict)} 个变量分配到全局命名空间: {list(data_dict.keys())}")


def assignin_caller(data_dict: dict, caller_globals: dict) -> None:
    """
    将字典中的所有键值对分配到调用者的命名空间中
    
    参数:
        data_dict (dict): 包含变量名和值的字典
        caller_globals (dict): 调用者的全局命名空间 (通常传入 globals())
    """
    caller_globals.update(data_dict)
    print(f"已将 {len(data_dict)} 个变量分配到调用者命名空间: {list(data_dict.keys())}")


def load_and_assign_h5_data(file_path: str, target_globals: dict = None) -> None:
    """
    加载 H5 数据并直接分配到指定的命名空间中
    
    参数:
        file_path (str): H5 文件路径
        target_globals (dict): 目标命名空间，如果为 None 则使用全局命名空间
    """
    # 这里假设你有 loadH5DataAll 函数
    # from pynbgui.fcn_file_nudft import loadH5DataAll
    # data, dataSetlist, listKey = loadH5DataAll(file_path)
    
    # 示例数据
    data = {
        'dataset1': np.random.rand(100, 100),
        'dataset2': np.random.rand(50, 50, 10),
        'metadata': {'info': 'test data'}
    }
    
    if target_globals is None:
        globals().update(data)
    else:
        target_globals.update(data)
    
    print(f"已加载并分配 H5 数据: {list(data.keys())}")


def load_h5_to_jupyter_variables(file_path: str) -> None:
    """
    专门用于 ipywidgets 按钮回调的函数
    读取 H5 数据并将结果直接传到 Jupyter 的变量空间中
    
    参数:
        file_path (str): H5 文件路径
    """
    try:
        # 导入 fcn_file_nudft 中的函数
        from pynbgui.fcn_file_nudft import loadH5DataAll
        
        print(f"正在加载 H5 文件: {file_path}")
        
        # 加载 H5 数据
        data, dataSetlist, listKey = loadH5DataAll(file_path)
        
        # 获取 IPython 实例
        try:
            ip = get_ipython()
            if ip is not None:
                # 将每个数据集分配到 Jupyter 变量空间
                for key, value in data.items():
                    ip.user_ns[key] = value
                
                print(f"✅ 成功加载 {len(data)} 个数据集到 Jupyter 变量空间:")
                for i, dataset_name in enumerate(dataSetlist, 1):
                    if isinstance(data[dataset_name], np.ndarray):
                        print(f"  {i}. {dataset_name}: {data[dataset_name].shape} ({data[dataset_name].dtype})")
                    else:
                        print(f"  {i}. {dataset_name}: {type(data[dataset_name])}")
                        
                print("\n💡 现在您可以在 Jupyter 变量浏览器中看到这些变量了！")
                
            else:
                print("❌ 错误: 未检测到 IPython 环境")
                
        except NameError:
            print("❌ 错误: 无法获取 IPython 实例")
            
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
    except Exception as e:
        print(f"❌ 加载 H5 文件时发生错误: {e}")


def create_h5_loader_widget(default_path: str = "") -> None:
    """
    创建一个包含文件选择和加载按钮的 ipywidgets 界面
    
    参数:
        default_path (str): 默认的文件路径
    """
    try:
        import ipywidgets as widgets
        from IPython.display import display
        
        # 创建文件路径输入框
        file_path_input = widgets.Text(
            value=default_path,
            placeholder='输入 H5 文件路径...',
            description='H5 文件:',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='500px')
        )
        
        # 创建加载按钮
        load_button = widgets.Button(
            description='📁 加载 H5 数据到变量空间',
            button_style='primary',
            layout=widgets.Layout(width='200px')
        )
        
        # 创建输出区域
        output = widgets.Output()
        
        # 定义按钮点击回调函数
        def on_load_button_clicked(b):
            with output:
                output.clear_output()
                file_path = file_path_input.value.strip()
                if file_path:
                    load_h5_to_jupyter_variables(file_path)
                else:
                    print("❌ 请先输入 H5 文件路径")
        
        # 绑定按钮点击事件
        load_button.on_click(on_load_button_clicked)
        
        # 显示界面
        display(widgets.VBox([
            widgets.HBox([file_path_input, load_button]),
            output
        ]))
        
    except ImportError:
        print("❌ 错误: 需要安装 ipywidgets 库")
        print("请运行: uv add ipywidgets")
