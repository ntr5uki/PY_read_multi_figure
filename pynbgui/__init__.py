"""
PynbGUI - Interactive image viewer for Jupyter notebooks
"""

from .h5_file_loader import H5FileLoader, create_h5_loader, refresh_jupyter_variables
from .image_sequence_viewer import ImageSequenceViewer
from .image_contrast_viewer import ImageContrastViewer
from .jupyter_array_selector import JupyterArraySelector, get_jupyter_numpy_arrays
from .interactive_image_viewer import InteractiveImageViewer, create_interactive_viewer
from .data_transfer import DataTransfer
__version__ = "0.1.0"

__all__ = [
    'H5FileLoader',
    'create_h5_loader',
    'refresh_jupyter_variables',
    'ImageSequenceViewer',
    'ImageContrastViewer',
    'JupyterArraySelector',
    'get_jupyter_numpy_arrays',
    'InteractiveImageViewer',
    'create_interactive_viewer',
    'DataTransfer',
]

# 便捷函数
def create_viewer(useRangeSlider: bool = True, showSizeControl: bool = True) -> InteractiveImageViewer:
    """
    创建交互式图像查看器的便捷函数
    
    Args:
        useRangeSlider: 是否使用范围滑块，默认为True
        showSizeControl: 是否显示图像大小控制，默认为True
        
    Returns:
        InteractiveImageViewer实例
    """
    return create_interactive_viewer(useRangeSlider, showSizeControl)
