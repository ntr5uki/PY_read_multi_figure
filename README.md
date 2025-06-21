# PY Read Multi Figure

一个用于在Jupyter Notebook中交互式查看和处理多图像数据的Python工具包。

## ✨ 新功能

### 🎯 交互式图像查看器
- **直接从Jupyter工作区选择numpy数组**: 通过下拉菜单选择当前工作区中的任何numpy数组
- **智能数组处理**: 自动处理2D、3D、4D数组，支持多种数据格式
- **实时图像查看**: 支持图像序列浏览和对比度调节
- **一键刷新**: 动态更新可用数组列表

## 🚀 快速开始

### 安装依赖
```bash
uv add numpy ipywidgets ipykernel pillow h5py ipyfilechooser matplotlib
```

### 基本使用

#### 交互式图像查看器
```python
from pynbgui import create_interactive_viewer
import numpy as np

# 创建一些测试数据
test_image = np.random.rand(100, 100) * 255
test_sequence = np.random.rand(10, 100, 100) * 255

# 创建交互式查看器（默认配置）
viewer = create_interactive_viewer()
viewer.display()

# 或者自定义配置
viewer_custom = create_interactive_viewer(
    useRangeSlider=True,    # 使用范围滑块
    showSizeControl=True    # 显示图像大小控制
)
viewer_custom.display()
```

#### 2. H5文件加载器
```python
from pynbgui import H5FileLoader

# 创建H5文件加载器
loader = H5FileLoader("path/to/your/data/")
loader.display()
```

#### 3. 直接使用图像序列查看器
```python
from pynbgui import ImageSequenceViewer
import numpy as np

# 创建3D图像数据
image_sequence = np.random.rand(15, 200, 200) * 255

# 创建查看器
viewer = ImageSequenceViewer(image_sequence)
viewer.display()
```

## 📋 功能特性

### 🔍 图像查看功能
- **多维数组支持**: 2D、3D、4D numpy数组
- **图像序列浏览**: 通过列表选择不同帧
- **对比度调节**: 双滑块或独立滑块模式
- **图像大小控制**: 实时缩放显示大小（0.1x - 10.0x）
- **实时更新**: 动态切换数据源

### 📁 数据加载功能
- **H5文件支持**: 图形界面选择和加载H5文件
- **自动变量分配**: 直接加载到Jupyter变量空间
- **数据类型检测**: 智能识别和处理不同数据格式

### 🎛️ 交互式控件
- **数组选择器**: 下拉菜单选择工作区数组
- **文件选择器**: 图形界面文件浏览
- **对比度控制**: 实时图像调节
- **大小控制**: 图像缩放滑块（可选）
- **状态显示**: 详细的操作反馈

## 📖 使用示例

查看以下notebook获取完整的使用示例：
- `debug_test.ipynb` - 基本功能测试（推荐开始）
- `final_test.ipynb` - 完整功能演示
- `simple_test.ipynb` - 简化测试
- `test_image_size_control.ipynb` - 图像大小控制功能演示

## 🔧 故障排除

### 常见问题

#### 1. ipywidgets渲染错误
```
Error rendering output item using 'jupyter-ipywidget-renderer'
Cannot read properties of undefined (reading 'ipywidgetsKernel')
```

**解决方案：**
```bash
# 方案1：重新安装ipywidgets
uv add ipywidgets --upgrade

# 方案2：重启Jupyter内核
```

#### 2. 找不到numpy数组
```
⚠️ 工作区中没有找到numpy数组
```

**解决方案：**
```python
# 确保数组已创建且为2D或以上
import numpy as np
test_array = np.random.rand(100, 100)

# 点击刷新按钮或重新运行查看器
from pynbgui import create_interactive_viewer
viewer = create_interactive_viewer()
viewer.refresh_arrays()
```

#### 3. AttributeError问题
如果遇到属性错误，请：
1. 重启Jupyter内核
2. 使用 `debug_test.ipynb` 进行测试
3. 确保使用最新版本的代码

## 🛠️ 开发环境

- Python 3.13+
- Jupyter Notebook/Lab
- 依赖包管理: uv

## 📦 项目结构

```
pynbgui/
├── __init__.py                    # 模块导出
├── h5_file_loader.py             # H5文件加载器
├── image_contrast_viewer.py      # 图像对比度查看器
├── image_sequence_viewer.py      # 图像序列查看器
├── jupyter_array_selector.py     # Jupyter数组选择器
├── interactive_image_viewer.py   # 交互式图像查看器
├── fcn_file_nudft.py            # H5数据处理函数
└── data_transfer.py             # 数据传输工具
```

## 🎯 适用场景

- 医学影像数据分析
- 科学数据可视化
- 图像序列处理
- 多维数据探索
- 实验数据查看