import h5py
import numpy as np
from IPython.display import display
import inspect
from ipyfilechooser import FileChooser


def select_h5_file(multiple=False):
    # Jupyter下的本地文件选择器
    fc = FileChooser(".")
    fc.title = "请选择h5文件" + ("（可多选）" if multiple else "")
    fc.filter_pattern = "*.h5"
    fc.use_dir_icons = True
    fc.show_hidden = False

    if multiple:
        # 启用多选模式
        fc.multiple = True
        print("多选+提示：按住 Ctrl 键（Windows/Linux）或 Cmd 键（Mac）点击多个文件")

    display(fc)
    return fc


# 打印出h5文件下的dataset信息
def printH5Dataset(file_path) -> list:
    listFile = []
    with h5py.File(file_path, "r") as f:
        for key in f.keys():
            listFile.append(key)
    return listFile


def loadH5Data(file_path, dataset_name: str) -> np.ndarray:
    print(f"尝试加载数据集: {dataset_name}, 类型: {type(dataset_name)}")
    with h5py.File(file_path, "r") as f:
        data: np.ndarray = f[dataset_name][:]
        return data


def listH5Dataset(file_path) -> tuple[list, list]:
    listFile = []
    listKey = []
    with h5py.File(file_path, "r") as f:
        for key in f.keys():
            if isinstance(f[key], h5py.Dataset):
                listFile.append(key)
            else:
                listKey.append(key)

    return listFile, listKey


def loadH5DataAll(file_path) -> tuple[dict, list, list]:
    data = {}
    dataSetlist, listKey = listH5Dataset(file_path)
    for fname in dataSetlist:
        data[fname] = loadH5Data(file_path, fname)
    return data, dataSetlist, listKey


def getVarName():
    """自动获取调用者环境中的numpy数组变量"""
    # 获取调用者的frame
    caller_frame = inspect.currentframe().f_back
    caller_globals = caller_frame.f_globals

    # 过滤出所有numpy数组
    numpy_vars = {
        k: v
        for k, v in caller_globals.items()
        if isinstance(v, np.ndarray) and not k.startswith("_")
    }

    print("NumPy数组变量:")
    if numpy_vars:
        print(f"{'变量名':<20} | {'形状':<15} | {'数据类型':<10} | {'内存(MB)':<10}")
        print("-" * 65)
        for name, array in numpy_vars.items():
            memory_mb = array.nbytes / (1024 * 1024)
            print(
                f"{name:<20} | {str(array.shape):<15} | {str(array.dtype):<10} | {memory_mb:.2f}"
            )
    else:
        print("没有找到numpy数组变量")

    return numpy_vars


def mat2gray(data):
    return np.interp(data, (data.min(), data.max()), (0, 1))


if __name__ == "__main__":
    # 使用文件选择对话框
    # file_path = select_h5_file()
    file_path = "dataset/data.h5"
    if file_path:
        print(f"选择的文件: {file_path}")
        printH5Dataset(file_path)
        dataRaw = loadH5Data(file_path, "RAW")
    else:
        print("未选择文件")
