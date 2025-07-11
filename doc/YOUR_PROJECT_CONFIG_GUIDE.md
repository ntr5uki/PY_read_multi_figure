# 您的项目 pyproject.toml 配置详解

本文档详细解释了您的 `py-read-multi-figure` 项目中 `pyproject.toml` 的每个配置项。

## 📋 当前配置分析

### 1. 项目基本信息

```toml
[project]
name = "py-read-multi-figure"
version = "0.1.0"
description = "Interactive image viewer for Jupyter notebooks with ROI selection"
readme = "README.md"
requires-python = ">=3.13"
```

**说明**：
- `name`: 包名，在 PyPI 上必须唯一
- `version`: 当前版本，遵循语义化版本规范
- `description`: 简短描述，会显示在 PyPI 上
- `readme`: 指向 README.md 文件，提供详细说明
- `requires-python`: 要求 Python 3.13+

### 2. 依赖配置

```toml
dependencies = [
    "numpy>=2.3.0",
    "ipywidgets>=8.0.0",
    "ipykernel>=6.29.5",
    "pillow>=11.2.1",
    "h5py>=3.14.0",
    "ipyfilechooser>=0.6.0",
    "matplotlib>=3.10.3",
    "ipympl>=0.9.7",
    "simpleeval>=1.0.3",
    "scipy>=1.16.0",
]
```

**说明**：
- 这些是运行时必需的依赖
- 使用 `>=` 指定最低版本要求
- 安装包时会自动安装这些依赖

### 3. 作者和许可证信息

```toml
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
license = {text = "MIT"}
```

**说明**：
- `authors`: 作者信息，可以有多个作者
- `license`: 许可证类型，MIT 是常用的开源许可证

### 4. 分类标签

```toml
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.13",
    "Topic :: Scientific/Engineering :: Visualization",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
```

**说明**：
- 这些标签帮助用户在 PyPI 上找到您的包
- 标明了开发状态、目标用户、许可证等信息

### 5. 入口点配置

```toml
[project.entry-points."pynbgui"]
interactive_viewer = "pynbgui.interactive_image_viewer:InteractiveImageViewer"
```

**说明**：
- 创建了一个自定义入口点组 `pynbgui`
- 其他项目可以通过入口点发现您的类
- 格式：`名称 = "模块路径:类名"`

### 6. URL 链接

```toml
[project.urls]
Homepage = "https://github.com/yourusername/py-read-multi-figure"
Repository = "https://github.com/yourusername/py-read-multi-figure"
Issues = "https://github.com/yourusername/py-read-multi-figure/issues"
```

**说明**：
- 提供项目相关的链接
- 用户可以通过这些链接找到源码、报告问题等

### 7. 构建系统配置

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**说明**：
- 使用 `hatchling` 作为构建后端
- `hatchling` 是现代的、快速的构建工具

### 8. 包内容配置

```toml
[tool.hatch.build.targets.wheel]
packages = ["pynbgui"]

[tool.hatch.build.targets.sdist]
include = [
    "/pynbgui",
    "/README.md",
    "/pyproject.toml",
]
```

**说明**：
- `packages = ["pynbgui"]`: 指定要打包的 Python 包目录
- `include`: 在源码分发包中包含的文件

## 🔧 常用修改场景

### 1. 更新版本号

```toml
[project]
version = "0.2.0"  # 功能更新
# 或
version = "0.1.1"  # 错误修复
# 或
version = "1.0.0"  # 稳定版本
```

### 2. 添加可选依赖

```toml
[project.optional-dependencies]
dev = [
    "pytest>=6.0",
    "black",
    "flake8",
]
test = [
    "pytest>=6.0",
    "pytest-cov",
]
docs = [
    "sphinx",
    "sphinx-rtd-theme",
]
```

**使用方式**：
```bash
# 安装开发依赖
pip install "py-read-multi-figure[dev]"

# 安装多个可选依赖
pip install "py-read-multi-figure[dev,test]"
```

### 3. 添加命令行工具

```toml
[project.scripts]
pynbgui-viewer = "pynbgui.cli:main"
image-viewer = "pynbgui.interactive_image_viewer:cli_main"
```

**说明**：安装包后，用户可以在命令行直接运行这些命令

### 4. 支持更多 Python 版本

```toml
[project]
requires-python = ">=3.8"  # 支持 Python 3.8+

classifiers = [
    # 添加更多 Python 版本
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]
```

### 5. 排除测试文件

```toml
[tool.hatch.build.targets.sdist]
include = [
    "/pynbgui",
    "/README.md",
    "/pyproject.toml",
]
exclude = [
    "/tests",
    "/docs",
    "/.git",
    "/__pycache__",
    "*.pyc",
    "*.pyo",
]
```

## 🚀 构建和发布流程

### 1. 本地构建

```bash
# 构建包
uv build

# 检查生成的文件
ls dist/
# py_read_multi_figure-0.1.0-py3-none-any.whl
# py_read_multi_figure-0.1.0.tar.gz
```

### 2. 本地测试

```bash
# 在虚拟环境中测试
python -m venv test_env
source test_env/bin/activate  # Linux/Mac
# test_env\Scripts\activate   # Windows

# 安装构建的包
pip install dist/py_read_multi_figure-0.1.0-py3-none-any.whl

# 测试导入
python -c "from pynbgui import create_viewer; print('Success!')"
```

### 3. 发布到 PyPI（可选）

```bash
# 安装发布工具
pip install twine

# 检查包
twine check dist/*

# 上传到测试 PyPI
twine upload --repository testpypi dist/*

# 上传到正式 PyPI
twine upload dist/*
```

## 📋 检查清单

在构建包之前，请确认：

- [ ] ✅ 项目名称在 PyPI 上唯一
- [ ] ✅ 版本号正确且遵循语义化版本
- [ ] ✅ 所有依赖版本测试过
- [ ] ✅ README.md 文档完整
- [ ] ✅ 许可证文件存在
- [ ] ✅ 作者信息正确
- [ ] ✅ 包结构正确（pynbgui/ 目录）
- [ ] ✅ 入口点路径正确
- [ ] ✅ 分类标签合适
- [ ] ✅ URL 链接正确

## 🔍 调试技巧

### 检查包内容

```bash
# 查看 wheel 包内容
python -m zipfile -l dist/py_read_multi_figure-0.1.0-py3-none-any.whl

# 或使用 unzip
unzip -l dist/py_read_multi_figure-0.1.0-py3-none-any.whl
```

### 验证元数据

```bash
# 安装包后检查元数据
pip show py-read-multi-figure

# 检查入口点
python -c "
import pkg_resources
for ep in pkg_resources.iter_entry_points('pynbgui'):
    print(f'{ep.name}: {ep.module_name}:{ep.attrs[0]}')
"
```

## 🎯 最佳实践

1. **版本管理**: 使用语义化版本，主版本.次版本.修订版本
2. **依赖管理**: 指定最低版本，避免过于严格的版本约束
3. **文档**: 保持 README.md 和 docstring 的更新
4. **测试**: 在不同环境中测试包的安装和使用
5. **许可证**: 选择合适的开源许可证
6. **分类**: 使用准确的 PyPI 分类标签

---

**提示**: 您的配置已经很完善了！主要需要更新的是作者信息和 URL 链接。 