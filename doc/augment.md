## 说明

- 此文档用于提示augment插件完成这个项目

## 项目目标
- 完成一个在ipynb中的二维/三维数据的查看工具
  - 将np:ndarray三维数据沿着维度0拆分成多个二维数据显示
  - 二维数据可以调整亮度对比度
- 功能通过ipynb实现 方便数据查看 需要支持ssh调试查看 所以gui功能受限于ipynb支持的
  - 主要ui通过Jupyter Widgets
- 通过ROI工具剪裁数据
  - JupyterArraySelector上方添加按钮 按下后激活PILROISelector
    - PILROISelector显示当前self.imageSequence中正在显示的图像
    - 按照
  - 注意gui功能受限于ipynb支持的
- 实现多种加载方式 包括h5 tiff 以及图片序列
- 支持直接读取ipynb中的np:ndarray
  - 需求
    - 通过ipywidgets的Dropdown选取
    - 点击时获取ipynb工作区的np:ndarray数据名称
    - ImageSequenceViewer类中的数据改为该数据
## 文档整理
  - 梳理create_interactive_viewer的函数关系, 用md的无序号列表分级， 显示建函数关系的树形图，类似下面，并在函数后面添加必要的注释
    - a() #
      - b() #
        - d() #
      - c() #
- 支持调试时从进程间通过multiprocessing传输过来查看
- 方便添加图像处理功能 (缩放、旋转、滤波)
## BUG
- 从ImageSequenceViewer的selectWidget切换图像时，ImageContrastViewer的sizeSlider的放大倍数没有对新显示的图像生效
- ImageSequenceViewer中应该针对self.imageSequence固定一个灰度范围, 灰度范围不要依据每张图重新自适应