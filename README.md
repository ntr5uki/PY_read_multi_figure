# PynbGUI - Interactive Image Viewer

一个专为Jupyter Notebook设计的交互式图像查看器，支持多维数组浏览和ROI选择。

## 功能特性

- 🖼️ **多维数组支持**: 支持2D、3D、4D numpy数组
- 🎛️ **交互式控制**: 滑块控制图像序列浏览
- 📐 **ROI选择**: 支持矩形区域选择
- 🔍 **图像调整**: 支持对比度调整和尺寸控制
- 📊 **变量选择器**: 自动检测Jupyter环境中的numpy数组
- 🎨 **现代界面**: 基于ipywidgets的美观UI

## 安装

### 方法1: 从源码构建安装

```bash
# 克隆仓库
git clone <your-repo-url>
cd py-read-multi-figure

# 使用uv构建和安装
uv build
uv pip install dist/*.whl

# 或者使用构建脚本
python build_package.py
```

### 方法2: 开发模式安装

```bash
cd py-read-multi-figure
uv pip install -e .
```

## 快速开始

### 在Jupyter Notebook中使用

```python
# 启用widget后端
%matplotlib widget

# 导入库
from pynbgui import create_viewer
import numpy as np

# 创建测试数据
test_2d = np.random.rand(100, 100)
test_3d = np.random.rand(10, 100, 100)

# 创建查看器
viewer = create_viewer()
viewer.display()
```

### 基本用法

```python
from pynbgui import InteractiveImageViewer, create_interactive_viewer

# 方法1: 使用便捷函数
viewer = create_interactive_viewer(
    useRangeSlider=True,    # 启用范围滑块
    showSizeControl=True    # 显示尺寸控制
)

# 方法2: 直接创建实例
viewer = InteractiveImageViewer(
    useRangeSlider=True,
    showSizeControl=True
)

# 显示查看器
viewer.display()

# 刷新可用数组列表
viewer.refresh_arrays()
```

### 高级用法

```python
from pynbgui import ImageSequenceViewer, JupyterArraySelector
import numpy as np

# 直接使用图像序列查看器
data = np.random.rand(10, 100, 100)  # 10帧100x100图像
seq_viewer = ImageSequenceViewer(data, useRangeSlider=True)
seq_viewer.display()

# 使用数组选择器
def on_array_selected(name, array):
    print(f"选择了数组: {name}, 形状: {array.shape}")

array_selector = JupyterArraySelector(on_selection_change=on_array_selected)
array_selector.display()
```

## API 参考

### InteractiveImageViewer

主要的交互式图像查看器类。

```python
class InteractiveImageViewer:
    def __init__(self, useRangeSlider: bool = True, showSizeControl: bool = True):
        """
        Args:
            useRangeSlider: 是否使用范围滑块
            showSizeControl: 是否显示图像大小控制
        """
    
    def display(self) -> None:
        """显示查看器界面"""
    
    def refresh_arrays(self) -> None:
        """刷新可用的numpy数组列表"""
    
    def get_current_viewer(self) -> Optional[ImageSequenceViewer]:
        """获取当前的图像序列查看器"""
```

### 便捷函数

```python
def create_viewer(useRangeSlider: bool = True, showSizeControl: bool = True) -> InteractiveImageViewer:
    """创建交互式图像查看器的便捷函数"""

def create_interactive_viewer(useRangeSlider: bool = True, showSizeControl: bool = True) -> InteractiveImageViewer:
    """创建交互式图像查看器"""
```

## 依赖要求

- Python >= 3.13
- numpy >= 2.3.0
- ipywidgets >= 8.0.0
- matplotlib >= 3.10.3
- ipympl >= 0.9.7
- 其他依赖见 `pyproject.toml`

## 开发

### 项目结构

```
py-read-multi-figure/
├── pynbgui/                    # 主包
│   ├── __init__.py            # 包初始化和导出
│   ├── interactive_image_viewer.py  # 主要查看器
│   ├── image_sequence_viewer.py     # 图像序列查看器
│   ├── jupyter_array_selector.py    # 数组选择器
│   └── ...                    # 其他模块
├── pyproject.toml             # 项目配置
├── README.md                  # 说明文档
└── build_package.py           # 构建脚本
```

### 构建和测试

```bash
# 构建包
uv build

# 安装开发版本
uv pip install -e .

# 运行构建脚本
python build_package.py
```

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！ 