# create_interactive_viewer 函数关系架构文档

## 📋 概览

`create_interactive_viewer` 是一个便捷函数，用于创建交互式图像查看器。本文档详细梳理了该函数及其相关组件的完整架构关系。

## 🌳 函数关系树形图

- create_interactive_viewer(useRangeSlider: bool = True, showSizeControl: bool = True) # 便捷函数，创建交互式图像查看器实例
  - InteractiveImageViewer.__init__(useRangeSlider: bool, showSizeControl: bool) # 主要的交互式图像查看器类初始化
    - widgets.HTML() # **创建状态显示标签**
    - widgets.VBox([]) # **创建图像查看器容器**
    - widgets.VBox([...]) # **创建主界面布局**
    - JupyterArraySelector(on_selection_change=self._on_array_selected) # **创建数组选择器**
      - JupyterArraySelector.__init__(on_selection_change) # 数组选择器初始化
        - self._create_widgets() # 创建选择器界面控件
          - widgets.Dropdown() # 数组选择下拉框
          - widgets.Button() # 刷新按钮
          - widgets.HTML() # 信息显示区域
          - widgets.VBox([...]) # 选择器主界面布局
        - self._refresh_arrays() # 刷新工作区中的numpy数组列表
          - get_jupyter_numpy_arrays() # 获取Jupyter工作区中的所有numpy数组
            - get_ipython() # 获取IPython实例
            - inspect.currentframe() # 备用方案：从调用者的全局命名空间获取
            - 过滤条件检查 # 过滤出2D以上的numpy数组，排除私有变量
        - array_dropdown.observe(self._on_array_selection_change) # 绑定下拉框选择事件
        - refresh_button.on_click(self._on_refresh_clicked) # 绑定刷新按钮点击事件
        - _on_array_selection_change(change: dict) # 数组选择变化回调
          - get_array_info(array) # 获取数组信息字符串（形状、类型、内存大小）
          - self.on_selection_change(name, array) # 触发父级回调函数
        - _on_refresh_clicked(button) # 刷新按钮点击回调
          - self._refresh_arrays() # 重新扫描工作区数组
        - get_selected_array() # 获取当前选择的数组
        - display() # 显示选择器界面
    - _on_array_selected(name: str, array: np.ndarray) # **数组选择回调函数**
      - 数组维度检查 # 检查2D/3D/4D数组并进行相应处理
      - self.status_label.value更新 # 更新状态显示
      - self._create_or_update_viewer(array) # 创建或更新图像查看器
    - _create_or_update_viewer(array: np.ndarray) # **创建或更新图像查看器**
      - ImageSequenceViewer(array, self.useRangeSlider, self.showSizeControl) # 创建新的图像序列查看器
      - self.imageViewer.updateImageSequence(array) # 更新现有查看器的数据
    - _clear_viewer() # 清除图像查看器
      - self.imageViewer = None # 清空查看器引用
      - self.viewer_container.children = [] # 清空容器内容
    - display() # 显示交互式图像查看器
      - display(self.main_widget) # 显示主界面
    - refresh_arrays() # 刷新可用的numpy数组列表
      - self.arraySelector._refresh_arrays() # 调用选择器的刷新方法
    - get_current_viewer() # 获取当前的图像序列查看器

## 🔗 ImageSequenceViewer 详细架构

- ImageSequenceViewer(imageSequence: np.ndarray, useRangeSlider: bool = True, showSizeControl: bool = True) # 图像序列查看器类初始化
  - 数据管理初始化 # 设置基本属性
    - 数组维度处理 # 支持2D和3D数组，2D自动转换为3D
    - self.imageSequence = imageSequence # 存储图像序列数据
    - self.numImages = imageSequence.shape[0] # 计算图像帧数
    - self.useRangeSlider = useRangeSlider # 存储滑块类型设置
    - self.showSizeControl = showSizeControl # 存储大小控制设置
  - _createSelectWidget() # 创建图像选择控件
    - widgets.Select() # 创建帧选择列表控件
    - self.selectWidget.observe(self._onValueChange) # 绑定选择变化事件
  - _createImageViewer() # 创建图像查看器
    - currentImageData = self.imageSequence[0] # 获取第一帧图像数据
    - ImageContrastViewer(currentImageData) # 创建图像对比度查看器
    - self.imageViewer.display(useRangeSlider, showSizeControl) # 显示图像查看器并获取widget
  - widgets.HBox([self.selectWidget, self.imageViewerWidget]) # 创建水平布局组合控件
  - _onValueChange(change: dict) # 帧选择变化回调函数
    - selected_index = change['new'] # 获取新选择的帧索引
    - newImageData = self.imageSequence[selected_index] # 获取对应帧的图像数据
    - self.imageViewer.updateImageData(newImageData) # 更新图像查看器的数据
    - self._triggerImageUpdate() # 触发图像更新
  - _triggerImageUpdate() # 触发图像查看器的更新
    - self.imageViewer._onRangeSliderChange({...}) # 范围滑块模式下的更新
    - self.imageViewer._onSeparateSlidersChange({...}) # 独立滑块模式下的更新
  - updateImageSequence(newImageSequence: np.ndarray) # 更新图像序列数据
    - 维度检查和转换 # 2D数组转换为3D，验证数组维度
    - 数据更新 # 更新imageSequence和numImages属性
    - self._createSelectWidget() # 重新创建选择控件以适应新的帧数
    - self.imageViewer.updateImageData(currentImageData) # 更新图像查看器数据
    - self.combinedWidget.children更新 # 更新组合控件的子组件
    - self._triggerImageUpdate() # 触发图像更新
  - display() # 显示图像序列查看器
    - display(self.combinedWidget) # 显示组合控件
  - getCurrentImage() # 获取当前选中的图像
    - return self.imageSequence[self.selectWidget.value] # 返回当前选择帧的图像数据
  - setCurrentIndex(index: int) # 设置当前选中的图像索引
    - 索引范围验证 # 检查索引是否在有效范围内
    - self.selectWidget.value = index # 设置选择控件的值

## 🎨 ImageContrastViewer 详细架构

- ImageContrastViewer(data: np.ndarray) # 图像对比度查看器类初始化
  - 数据处理初始化 # 处理输入的图像数据
    - self.data = data.squeeze() # 确保数据是2维的，移除大小为1的维度
    - self.dataDisplay = np.interp(...) # 将数据归一化到0-255范围
    - widgets.Image(format="jpeg") # 创建用于显示图像的Image控件
    - widgets.Output() # 创建输出区域用于包裹图像控件
  - 滑块属性初始化 # 初始化滑块相关属性
    - self.useRangeSlider: bool # 是否使用范围滑块的标志
    - self.rangeSlider: Optional[IntRangeSlider] # 范围滑块控件
    - self.vminSlider: Optional[FloatSlider] # 最小值滑块控件
    - self.vmaxSlider: Optional[FloatSlider] # 最大值滑块控件
    - self.sizeSlider: Optional[FloatSlider] # 图像大小控制滑块
    - self.originalDataDisplay: np.ndarray # 保存原始显示数据用于缩放
  - display(useRangeSlider: bool = False, showSizeControl: bool = True) # 显示交互式图像对比度调节界面
    - self._createRangeSlider() # 创建范围滑块（如果useRangeSlider为True）
    - self._createSeparateSliders() # 创建独立滑块（如果useRangeSlider为False）
    - self._createSizeSlider() # 创建图像大小控制滑块（如果showSizeControl为True）
    - self._updateContrastImage(...) # 初始显示图像
    - display(self.imageWidget) # 显示图像控件
    - return widgets.VBox([...]) # 返回包含所有控件和图像的垂直布局
  - _createRangeSlider() # 创建范围滑块
    - IntRangeSlider(value=[0, 255], min=0, max=255, ...) # 创建范围滑块控件
    - self.rangeSlider.observe(self._onRangeSliderChange) # 绑定值变化事件
  - _createSeparateSliders() # 创建独立滑块
    - FloatSlider(min=0, max=100, value=0, ...) # 创建最小值滑块
    - FloatSlider(min=155, max=255, value=255, ...) # 创建最大值滑块
    - self.vminSlider.observe(self._onSeparateSlidersChange) # 绑定最小值滑块事件
    - self.vmaxSlider.observe(self._onSeparateSlidersChange) # 绑定最大值滑块事件
  - _createSizeSlider() # 创建图像大小控制滑块
    - FloatSlider(min=0.1, max=10.0, value=1.0, ...) # 创建大小控制滑块（0.1x-10x）
    - self.sizeSlider.observe(self._onSizeSliderChange) # 绑定大小滑块事件
  - _onRangeSliderChange(change) # 范围滑块值变化回调
    - vmin, vmax = change["new"] # 获取新的范围值
    - self._updateContrastImage(vmin, vmax) # 更新图像对比度
  - _onSeparateSlidersChange(change) # 独立滑块值变化回调
    - vmin = self.vminSlider.value # 获取最小值滑块的值
    - vmax = self.vmaxSlider.value # 获取最大值滑块的值
    - self._updateContrastImage(vmin, vmax) # 更新图像对比度
  - _onSizeSliderChange(change) # 图像大小滑块变化回调
    - size_ratio = change["new"] # 获取新的缩放比例
    - self._resizeImage(size_ratio) # 调整图像大小
    - 重新应用对比度设置 # 缩放后重新应用当前的对比度设置
  - _updateContrastImage(vmin: float, vmax: float) # 根据对比度范围更新并显示图像
    - 参数验证 # 确保vmin < vmax
    - np.interp(self.dataDisplay, [vmin, vmax], [0, 255]) # 调整图像对比度
    - Image.fromarray(adjusted_data, mode="L") # 创建PIL图像
    - BytesIO() # 创建字节流缓冲区
    - img.save(buffered, format="jpeg") # 将图像保存为JPEG格式
    - self.imageWidget.value = buffered.getvalue() # 更新图像控件的值
  - _resizeImage(size_ratio: float) # 根据缩放比例调整图像大小
    - 参数验证 # 确保缩放比例有效
    - 计算新尺寸 # 根据原始尺寸和缩放比例计算新尺寸
    - PIL图像缩放 # 使用LANCZOS插值进行高质量缩放
    - self.dataDisplay更新 # 更新显示数据为缩放后的图像
  - updateImageData(newData: np.ndarray) # 更新图像数据
    - self.data = newData.squeeze() # 更新原始数据
    - self.dataDisplay = np.interp(...) # 重新归一化显示数据
    - self.originalDataDisplay = self.dataDisplay.copy() # 保存原始显示数据
  - imResize(sizeRatio) # 调整图像大小
    - 参数处理 # 处理不同格式的缩放比例参数
    - Image.fromarray(...).resize(...) # 使用PIL进行图像缩放
    - self.dataDisplay更新 # 更新显示数据
  - saveImage(filename: str) # 保存当前显示的图像到文件
    - Image.fromarray(self.dataDisplay, mode="L") # 创建PIL图像
    - img.save(filename) # 保存图像文件

## 📋 核心工具函数

- get_jupyter_numpy_arrays() # 获取Jupyter工作区中的所有numpy数组变量
  - get_ipython() # 获取IPython实例，用于访问用户命名空间
  - inspect.currentframe() # 备用方案：从调用者的全局命名空间获取
  - 数组过滤逻辑 # 过滤出符合条件的numpy数组
    - not name.startswith('_') # 排除私有变量
    - isinstance(value, np.ndarray) # 确保是numpy数组
    - value.ndim >= 2 # 确保是2维或以上的数组
  - 异常处理 # 捕获异常并返回空字典
- get_array_info(array: np.ndarray) # 获取数组的信息字符串
  - array.nbytes / (1024 * 1024) # 计算内存大小（MB）
  - 格式化字符串 # 返回包含形状、数据类型和内存大小的信息
- create_interactive_viewer(useRangeSlider: bool = True, showSizeControl: bool = True) # 创建交互式图像查看器的便捷函数
  - InteractiveImageViewer(useRangeSlider, showSizeControl) # 直接返回InteractiveImageViewer实例

## 🔄 数据流程图

- 用户操作流程 # 完整的用户交互流程
  - create_interactive_viewer() # 用户调用便捷函数
    - InteractiveImageViewer实例创建 # 创建主要的交互式图像查看器
  - 自动初始化组件 # 系统自动完成的初始化步骤
    - 状态标签和容器创建 # 创建UI基础组件
    - JupyterArraySelector创建 # 创建数组选择器
      - get_jupyter_numpy_arrays() # 扫描工作区numpy数组
      - 下拉菜单选项填充 # 将找到的数组填充到下拉菜单
    - 主界面布局构建 # 组装所有UI组件
  - 用户选择数组 # 用户通过下拉菜单选择数组
    - _on_array_selection_change() # 下拉菜单选择变化触发
      - 信息显示更新 # 更新数组信息显示
      - InteractiveImageViewer._on_array_selected() # 调用主查看器的回调
        - 数组维度检查 # 检查2D/3D/4D数组类型
        - 状态标签更新 # 更新状态显示信息
        - _create_or_update_viewer() # 创建或更新图像查看器
  - 图像查看器创建/更新 # 根据选择的数组创建或更新查看器
    - 首次创建分支 # 如果是第一次创建查看器
      - ImageSequenceViewer(array, useRangeSlider) # 创建图像序列查看器
        - 帧选择控件创建 # 创建用于选择不同帧的控件
        - ImageContrastViewer创建 # 创建图像对比度查看器
          - 数据预处理 # 对图像数据进行预处理
          - 对比度滑块创建 # 创建对比度调节滑块
    - 更新现有分支 # 如果查看器已存在，则更新
      - imageViewer.updateImageSequence(array) # 更新现有查看器的数据
        - 数据更新 # 更新图像序列数据
        - 选择控件重建 # 重新创建帧选择控件
        - 图像显示更新 # 更新图像显示
  - 用户交互阶段 # 用户与查看器进行交互
    - 帧选择交互 # 用户选择不同的图像帧
      - ImageSequenceViewer._onValueChange() # 帧选择变化回调
        - 图像数据更新 # 更新当前显示的图像数据
    - 对比度调节交互 # 用户调节图像对比度
      - 范围滑块模式 # 使用范围滑块调节对比度
        - _onRangeSliderChange() # 范围滑块变化回调
      - 独立滑块模式 # 使用独立的最小值和最大值滑块
        - _onSeparateSlidersChange() # 独立滑块变化回调
      - _updateContrastImage() # 实时更新图像显示

## 🎯 关键接口和回调

### 主要回调函数链

- 回调函数调用链 # 完整的回调函数调用序列
  - JupyterArraySelector._on_array_selection_change(change) # 数组选择器的选择变化回调
    - self.on_selection_change(selected_name, selected_array) # 触发注册的回调函数
  - InteractiveImageViewer._on_array_selected(name, array) # 主查看器的数组选择回调
    - 数组维度分析和处理 # 分析数组维度并进行相应处理
    - self._create_or_update_viewer(array) # 创建或更新图像查看器
  - ImageSequenceViewer创建/更新 # 图像序列查看器的创建或更新
    - __init__() # 初始化新的图像序列查看器
    - updateImageSequence() # 更新现有查看器的图像序列
    - _createImageViewer() # 创建内部的图像查看器
  - ImageContrastViewer创建 # 图像对比度查看器的创建
    - __init__(currentImageData) # 使用当前图像数据初始化
    - display(useRangeSlider) # 显示对比度调节界面
  - 用户交互回调 # 用户操作触发的回调函数
    - ImageSequenceViewer._onValueChange() # 帧选择变化回调
    - ImageContrastViewer._onRangeSliderChange() # 范围滑块变化回调
    - ImageContrastViewer._onSeparateSlidersChange() # 独立滑块变化回调

### 数据传递接口

- 数据传递路径 # 数据在组件间的传递路径
  - numpy数组(工作区) # 起始点：用户工作区中的numpy数组
    - get_jupyter_numpy_arrays() # 扫描并获取所有符合条件的numpy数组
      - JupyterArraySelector.arrays # 存储在选择器的arrays属性中
        - 用户选择操作 # 用户通过下拉菜单选择特定数组
          - (name, array)传递 # 将选择的数组名称和数据传递给回调
            - InteractiveImageViewer._on_array_selected() # 主查看器接收数组数据
              - 维度处理 # 根据数组维度进行相应的处理
                - processed_array # 处理后的数组数据
                  - ImageSequenceViewer(processed_array) # 传递给图像序列查看器
                    - ImageContrastViewer(frame_data) # 传递单帧数据给对比度查看器
                      - self.dataDisplay # 转换为显示用的数据格式
                        - 对比度调整 # 根据滑块值调整对比度
                          - adjusted_data # 调整后的图像数据
                            - PIL.Image # 转换为PIL图像对象
                              - JPEG bytes # 转换为JPEG字节流
                                - widgets.Image.value # 最终显示在Image控件中

## 🛠️ 组件依赖关系

### 导入依赖

- 模块依赖树 # 各模块之间的导入依赖关系
  - pynbgui/ # 主包目录
    - interactive_image_viewer.py # 交互式图像查看器模块
      - from .jupyter_array_selector import JupyterArraySelector # 导入数组选择器
      - from .image_sequence_viewer import ImageSequenceViewer # 导入图像序列查看器
    - jupyter_array_selector.py # Jupyter数组选择器模块
      - import ipywidgets as widgets # 导入ipywidgets库
      - from IPython.display import display # 导入IPython显示功能
      - from IPython import get_ipython # 导入IPython实例获取功能
      - import numpy as np # 导入numpy库
      - import inspect # 导入inspect模块用于获取调用者信息
    - image_sequence_viewer.py # 图像序列查看器模块
      - import ipywidgets as widgets # 导入ipywidgets库
      - from IPython.display import display # 导入IPython显示功能
      - import numpy as np # 导入numpy库
      - from .image_contrast_viewer import ImageContrastViewer # 导入图像对比度查看器
    - image_contrast_viewer.py # 图像对比度查看器模块
      - import numpy as np # 导入numpy库
      - from ipywidgets import FloatSlider, Output, IntRangeSlider, widgets # 导入各种ipywidgets控件
      - from IPython.display import display # 导入IPython显示功能
      - from PIL import Image # 导入PIL图像处理库
      - from io import BytesIO # 导入字节流处理

### 运行时依赖

- 运行时对象关系 # 运行时各对象之间的包含和依赖关系
  - InteractiveImageViewer # 主要的交互式图像查看器对象
    - arraySelector: JupyterArraySelector # 数组选择器对象
      - array_dropdown: widgets.Dropdown # 数组选择下拉框控件
      - refresh_button: widgets.Button # 刷新按钮控件
      - info_label: widgets.HTML # 信息显示标签控件
      - main_widget: widgets.VBox # 选择器主界面垂直布局控件
    - status_label: widgets.HTML # 状态显示标签控件
    - viewer_container: widgets.VBox # 图像查看器容器控件
    - main_widget: widgets.VBox # 主界面垂直布局控件
    - imageViewer: Optional[ImageSequenceViewer] # 可选的图像序列查看器对象
      - selectWidget: widgets.Select # 帧选择列表控件
      - imageViewer: ImageContrastViewer # 图像对比度查看器对象
        - imageWidget: widgets.Image # 图像显示控件
        - plotOutput: widgets.Output # 输出区域控件
        - rangeSlider: Optional[IntRangeSlider] # 可选的范围滑块控件
        - vminSlider: Optional[FloatSlider] # 可选的最小值滑块控件
        - vmaxSlider: Optional[FloatSlider] # 可选的最大值滑块控件
      - imageViewerWidget: widgets.VBox # 图像查看器垂直布局控件
      - combinedWidget: widgets.HBox # 组合控件水平布局

## ⚠️ 错误处理机制

### 异常处理层级

- 错误处理架构 # 多层次的错误处理机制
  - 顶层异常处理 # 最外层的异常处理
    - create_interactive_viewer() # 便捷函数的异常包装
      - try-catch包装整个创建过程 # 捕获创建过程中的所有异常
  - 组件级异常处理 # 各个组件内部的异常处理
    - InteractiveImageViewer._on_array_selected() # 数组选择回调的异常处理
      - hasattr(self, 'status_label') # 属性存在性检查，防止AttributeError
      - 数组维度验证 # 验证数组维度是否符合要求
      - 异常捕获 -> 状态标签更新 # 捕获异常并更新状态显示
    - JupyterArraySelector._on_array_selection_change() # 选择器回调的异常处理
      - 回调函数异常捕获 # 捕获回调函数执行中的异常
      - print错误信息 # 输出错误信息到控制台
    - ImageSequenceViewer.updateImageSequence() # 图像序列更新的异常处理
      - 维度检查和转换 # 检查并转换数组维度
      - ValueError抛出 # 对于无效维度抛出ValueError
  - 数据层异常处理 # 数据获取和处理的异常处理
    - get_jupyter_numpy_arrays() # 数组获取函数的异常处理
      - IPython环境检查 # 检查是否在IPython环境中
      - 备用方案(inspect.currentframe) # 使用备用方案获取数组
      - 异常捕获 -> 返回空字典 # 捕获所有异常并返回空字典
    - ImageContrastViewer._updateContrastImage() # 图像更新的异常处理
      - 参数验证(vmin < vmax) # 验证对比度参数的有效性
      - PIL图像处理异常 # 处理PIL图像操作中的异常

### 降级策略

- 功能降级路径 # 当主要功能失败时的处理方案
  - 部分功能降级 # 部分功能失效时的处理
    - 对比度滑块失败 -> 固定对比度 # 使用固定的对比度设置
    - 帧选择失败 -> 显示第一帧 # 只显示第一帧图像
    - 状态更新失败 -> 控制台输出 # 将状态信息输出到控制台
    - 数组检测失败 -> 手动刷新 # 用户手动点击刷新按钮
    - 图像显示失败 -> 错误信息显示 # 在状态标签中显示错误信息

## 🎯 使用最佳实践

### 推荐使用模式

```python
# 1. 基本使用
from pynbgui import create_interactive_viewer
import numpy as np

# 创建测试数据
data_2d = np.random.rand(100, 100) * 255
data_3d = np.random.rand(10, 100, 100) * 255

# 创建查看器
viewer = create_interactive_viewer(useRangeSlider=True)
viewer.display()

# 2. 错误处理
try:
    viewer = create_interactive_viewer()
    viewer.display()
except Exception as e:
    print(f"查看器创建失败: {e}")
    # 重启内核并重试

# 3. 自定义回调
def custom_array_handler(name, array):
    print(f"处理数组: {name}, 形状: {array.shape}")

from pynbgui import JupyterArraySelector
selector = JupyterArraySelector(on_selection_change=custom_array_handler)
selector.display()
```

### 故障排除指南

- 常见问题解决 # 常见问题的解决方案
  - AttributeError: 'object' has no attribute 'status_label' # 属性错误
    - 原因: 初始化顺序问题 # 对象初始化顺序导致的问题
    - 解决: 重启内核，使用最新版本 # 重启Jupyter内核并确保使用最新代码
  - 找不到numpy数组 # 数组检测失败
    - 检查: 数组是否为2D以上 # 确保数组维度符合要求
    - 检查: 变量名是否以下划线开头 # 确保变量名不是私有变量
    - 解决: 点击刷新按钮 # 手动刷新数组列表
  - ipywidgets渲染错误 # 控件渲染问题
    - 检查: Jupyter扩展是否安装 # 确保ipywidgets扩展正确安装
    - 重启: Jupyter内核 # 重启内核解决状态问题
    - 重新安装: uv add ipywidgets --upgrade # 升级ipywidgets版本
  - 图像显示异常 # 图像显示问题
    - 检查: 数组数据类型和范围 # 确保数据类型和数值范围正确
    - 检查: PIL库是否正常 # 确保PIL图像处理库正常工作
    - 调试: 使用matplotlib直接显示 # 使用matplotlib进行调试

## 🆕 最新更新和修复

### 已修复的问题

- **问题1**: 直接读取2维数据会提示要3维数据 # 修复了ImageSequenceViewer对2D数组的支持
  - 解决方案: 在__init__方法中添加2D到3D的自动转换 # 与updateImageSequence方法保持一致
  - 影响范围: ImageSequenceViewer.__init__() # 现在支持(y,x)和(z,y,x)两种格式

### 新增功能

- **图像大小控制**: 实时缩放显示图像 # 新增的图像大小调节功能
  - 缩放范围: 0.1x - 10.0x（10% - 1000%） # 支持大幅度缩放
  - 高质量插值: 使用LANCZOS算法 # 保证缩放质量
  - 基于原始数据: 避免累积误差 # 每次缩放都基于原始图像数据
  - 可选控制: showSizeControl参数 # 可以选择是否显示大小控制

### 参数更新

- **create_interactive_viewer()**: 新增showSizeControl参数 # 控制是否显示图像大小滑块
- **InteractiveImageViewer**: 新增showSizeControl属性 # 传递给子组件
- **ImageSequenceViewer**: 新增showSizeControl参数 # 传递给ImageContrastViewer
- **ImageContrastViewer.display()**: 新增showSizeControl参数 # 控制大小滑块的显示

## 📚 相关文档

- `README.md` # 项目概览和快速开始指南
- `debug_test.ipynb` # 调试和测试指南
- `final_test.ipynb` # 完整功能演示
- `simple_test.ipynb` # 基础功能测试
- `test_image_size_control.ipynb` # 图像大小控制功能演示

## 🔧 使用示例更新

```python
# 基本使用（默认启用大小控制）
viewer = create_interactive_viewer()
viewer.display()

# 自定义配置
viewer = create_interactive_viewer(
    useRangeSlider=True,    # 使用范围滑块
    showSizeControl=True    # 显示图像大小控制
)
viewer.display()

# 不显示大小控制
viewer = create_interactive_viewer(
    useRangeSlider=False,   # 使用独立滑块
    showSizeControl=False   # 隐藏图像大小控制
)
viewer.display()
```

---

*本文档详细描述了 `create_interactive_viewer` 的完整架构，使用md无序号列表分级显示函数关系树形图，并为每个函数添加了必要的注释说明。包含最新的功能更新和问题修复。*
```
```
