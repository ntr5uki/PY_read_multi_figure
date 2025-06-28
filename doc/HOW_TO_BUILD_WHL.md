# 如何配置 pyproject.toml 构建 WHL 包

本文档详细说明了如何配置 `pyproject.toml` 文件来将 Python 项目打包成 `.whl` 文件。

## 📋 目录

1. [基本项目信息配置](#基本项目信息配置)
2. [依赖管理配置](#依赖管理配置)
3. [构建系统配置](#构建系统配置)
4. [包内容配置](#包内容配置)
5. [入口点配置](#入口点配置)
6. [元数据配置](#元数据配置)
7. [构建命令](#构建命令)
8. [常见问题](#常见问题)

## 基本项目信息配置

### 必需字段

```toml
[project]
name = "your-package-name"           # 包名，必须唯一
version = "0.1.0"                    # 版本号，遵循语义化版本
description = "Your package description"  # 简短描述
requires-python = ">=3.8"           # Python版本要求
```

### 可选但推荐的字段

```toml
[project]
readme = "README.md"                 # README文件路径
license = {text = "MIT"}            # 许可证
keywords = ["jupyter", "image", "viewer"]  # 关键词
```

## 依赖管理配置

### 运行时依赖

```toml
[project]
dependencies = [
    "numpy>=1.20.0",                # 指定最低版本
    "matplotlib>=3.5.0,<4.0.0",    # 指定版本范围
    "ipywidgets>=8.0.0",            # 固定主版本
]
```

### 可选依赖

```toml
[project.optional-dependencies]
dev = [
    "pytest>=6.0",
    "black",
    "flake8",
]
docs = [
    "sphinx",
    "sphinx-rtd-theme",
]
```

## 构建系统配置

### 使用 Hatchling（推荐）

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### 使用 Setuptools

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"
```

### 使用 Poetry

```toml
[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## 包内容配置

### Hatchling 包配置

```toml
[tool.hatch.build.targets.wheel]
packages = ["your_package"]         # 指定要包含的包目录

[tool.hatch.build.targets.sdist]
include = [
    "/your_package",                # 包含源码包
    "/README.md",                   # 包含文档
    "/LICENSE",                     # 包含许可证
    "/pyproject.toml",             # 包含配置文件
]
exclude = [
    "/.git",                       # 排除git文件
    "/tests",                      # 排除测试文件
    "/__pycache__",               # 排除缓存文件
]
```

### Setuptools 包配置

```toml
[tool.setuptools.packages.find]
where = ["."]                      # 搜索包的根目录
include = ["your_package*"]        # 包含的包模式
exclude = ["tests*"]               # 排除的包模式

[tool.setuptools.package-data]
your_package = ["*.txt", "*.json"] # 包含数据文件
```

## 入口点配置

### 命令行入口点

```toml
[project.scripts]
your-cli = "your_package.cli:main"          # 命令行工具
another-tool = "your_package.tools:run"     # 另一个工具
```

### GUI 入口点

```toml
[project.gui-scripts]
your-gui = "your_package.gui:main"          # GUI应用程序
```

### 自定义入口点

```toml
[project.entry-points."your_plugin_group"]
plugin1 = "your_package.plugins:Plugin1"    # 插件系统
plugin2 = "your_package.plugins:Plugin2"    # 另一个插件
```

## 元数据配置

### 作者信息

```toml
[project]
authors = [
    {name = "Your Name", email = "your.email@example.com"},
    {name = "Another Author", email = "another@example.com"},
]
maintainers = [
    {name = "Maintainer Name", email = "maintainer@example.com"},
]
```

### 分类信息

```toml
[project]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Scientific/Engineering",
]
```

### URL链接

```toml
[project.urls]
Homepage = "https://github.com/username/project"
Documentation = "https://project.readthedocs.io"
Repository = "https://github.com/username/project"
Issues = "https://github.com/username/project/issues"
Changelog = "https://github.com/username/project/blob/main/CHANGELOG.md"
```

## 完整示例

以下是一个完整的 `pyproject.toml` 配置示例：

```toml
[project]
name = "my-awesome-package"
version = "1.0.0"
description = "An awesome Python package for data processing"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
keywords = ["data", "processing", "analysis"]
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "numpy>=1.20.0",
    "pandas>=1.3.0",
    "matplotlib>=3.5.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=6.0",
    "black",
    "flake8",
    "mypy",
]
docs = [
    "sphinx>=4.0",
    "sphinx-rtd-theme",
]

[project.scripts]
my-tool = "my_package.cli:main"

[project.entry-points."my_plugin_group"]
default_plugin = "my_package.plugins:DefaultPlugin"

[project.urls]
Homepage = "https://github.com/username/my-awesome-package"
Documentation = "https://my-awesome-package.readthedocs.io"
Repository = "https://github.com/username/my-awesome-package"
Issues = "https://github.com/username/my-awesome-package/issues"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["my_package"]

[tool.hatch.build.targets.sdist]
include = [
    "/my_package",
    "/README.md",
    "/LICENSE",
    "/pyproject.toml",
]
exclude = [
    "/.git",
    "/tests",
    "/__pycache__",
    "*.pyc",
]
```

## 构建命令

### 使用 build 工具（推荐）

```bash
# 安装构建工具
pip install build

# 构建包
python -m build

# 只构建 wheel
python -m build --wheel

# 只构建源码包
python -m build --sdist
```

### 使用 uv（现代工具）

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 构建包
uv build

# 构建并安装
uv pip install .
```

### 使用 pip

```bash
# 构建 wheel
pip wheel .

# 安装开发版本
pip install -e .
```

## 常见问题

### 1. 包找不到模块

**问题**: `ModuleNotFoundError: No module named 'your_package'`

**解决方案**: 检查包配置
```toml
[tool.hatch.build.targets.wheel]
packages = ["your_package"]  # 确保包名正确
```

### 2. 依赖版本冲突

**问题**: 依赖版本不兼容

**解决方案**: 使用更宽松的版本约束
```toml
dependencies = [
    "numpy>=1.20.0,<2.0.0",  # 使用范围而不是固定版本
]
```

### 3. 数据文件丢失

**问题**: 包中的数据文件没有包含

**解决方案**: 明确包含数据文件
```toml
[tool.hatch.build.targets.wheel]
packages = ["your_package"]

[tool.hatch.build.targets.wheel.shared-data]
"your_package/data" = "your_package/data"
```

### 4. 入口点不工作

**问题**: 命令行工具无法找到

**解决方案**: 检查入口点路径
```toml
[project.scripts]
your-tool = "your_package.cli:main"  # 确保路径正确
```

### 5. 版本号管理

**问题**: 手动更新版本号容易出错

**解决方案**: 使用动态版本
```toml
[project]
dynamic = ["version"]

[tool.hatch.version]
path = "your_package/__init__.py"
```

## 📋 检查清单

构建 WHL 包前的检查清单：

- [ ] ✅ 项目名称唯一且符合 PyPI 规范
- [ ] ✅ 版本号遵循语义化版本规范
- [ ] ✅ 依赖版本约束合理
- [ ] ✅ 包结构正确配置
- [ ] ✅ 入口点路径正确
- [ ] ✅ 元数据信息完整
- [ ] ✅ 许可证文件存在
- [ ] ✅ README 文档完整
- [ ] ✅ 测试通过
- [ ] ✅ 构建成功无错误

## 🔧 调试技巧

### 检查包内容

```bash
# 解压 wheel 文件查看内容
unzip -l dist/your_package-1.0.0-py3-none-any.whl

# 使用 wheel 工具
pip install wheel
wheel unpack dist/your_package-1.0.0-py3-none-any.whl
```

### 验证安装

```bash
# 在虚拟环境中测试安装
python -m venv test_env
source test_env/bin/activate  # Linux/Mac
# test_env\Scripts\activate   # Windows
pip install dist/your_package-1.0.0-py3-none-any.whl
python -c "import your_package; print(your_package.__version__)"
```

---

**提示**: 建议使用现代构建工具如 `uv` 或 `build`，它们提供更好的依赖解析和构建性能。 