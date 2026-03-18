# AutoBGI - 自动化应用程序操作工具

## 项目概述

AutoBGI 是一个基于图像识别技术的自动化工具，专门用于自动启动应用程序并在其界面上执行重复性点击操作。该工具利用OpenCV进行图像识别，结合PyAutoGUI实现自动化控制，适用于需要重复性操作的应用场景。

## 功能特性

- **智能启动**: 自动启动指定的应用程序
- **图像识别**: 利用OpenCV识别界面元素，精准定位操作目标
- **自动点击**: 循环点击预设的目标图标
- **窗口管理**: 自动确保目标应用位于最前端
- **时间控制**: 支持设置运行时间段限制
- **错误处理**: 包含截图记录和恢复机制
- **多应用支持**: 可同时启动多个应用程序

## 技术栈

- Python 3.x
- OpenCV - 图像识别
- PyAutoGUI - 自动化控制
- NumPy - 数值计算
- PyGetWindow - 窗口管理
- Pillow - 图像处理

## 系统要求

- Windows 10/11 或其他兼容操作系统
- Python 3.6+
- 管理员权限（可能需要）

## 安装与部署

### 1. 环境准备

```bash
pip install opencv-python pyautogui pillow numpy pygetwindow
```

### 2. 依赖安装

确保安装以下Python库：
- opencv-python
- pyautogui
- pillow
- numpy
- pygetwindow

### 3. 配置文件

在使用前需要准备以下文件：
- ready_icon.png - 用于确认应用已就绪的图标
- target_icon.png - 需要持续点击的目标图标

## 配置参数

在 test.py 文件中可配置以下参数：

- APP_PATH - 目标应用程序路径
- APP_PATH_2 - 第二个应用程序路径（可选）
- READY_ICON - 应用程序就绪状态的图标
- TARGET_ICON - 需要点击的目标图标
- CONFIDENCE - 图像识别置信度 (0.0-1.0)
- CHECK_INTERVAL - 搜索目标图标的间隔时间
- MAX_WAIT_TIME - 等待应用程序启动的最大时间
- CLICK_COUNT_LIMIT - 最大点击次数（0表示无限制）
- START_HOUR - 开始运行的小时
- END_HOUR - 结束运行的小时

## 使用方法

### 直接运行Python脚本

```bash
python test.py
```

### 打包成EXE文件

```bash
python build_exe.py
```

或运行批处理脚本：

```bash
build.bat
```

### 打包后的EXE使用

1. 将生成的 AutoBGI.exe 与其他资源文件放在同一目录
2. 确保 ready_icon.png 和 target_icon.png 存在于同目录下
3. 双击运行 AutoBGI.exe

## 项目结构

```
AutoBGI/
│
├── test.py              # 主程序文件
├── build.bat            # Windows打包脚本
├── build_exe.py         # PyInstaller打包脚本
├── README.md            # 项目说明文档
├── USAGE.md             # 使用说明文档
├── PYINSTALLER_README.md # PyInstaller打包说明
├── ready_icon.png       # 应用就绪图标
├── ready_icon_1.png     # 备用就绪图标
├── ready_icon_2.png     # 备用就绪图标
├── target_icon.png      # 目标点击图标
├── error_screenshots/   # 错误截图存储目录
├── dist/                # 打包输出目录
├── build/               # PyInstaller临时目录
└── AutoBGI.spec         # PyInstaller配置文件
```

## 安全功能

- **FAILSAFE机制**: pyautogui.FAILSAFE = True，将鼠标移至屏幕左上角可紧急停止程序
- **时间限制**: 可设置程序运行的时间范围
- **错误截图**: 当识别失败时自动保存截图便于调试

## 故障排除

1. **无法启动应用程序**: 检查 APP_PATH 是否正确配置
2. **图标识别失败**: 调整 CONFIDENCE 值或更新图标文件
3. **点击位置不准确**: 确保屏幕缩放比例为100%且应用程序窗口尺寸正常
4. **权限问题**: 尝试以管理员身份运行程序

## 自定义开发

您可以根据需求修改以下方面：

1. 更改应用程序路径
2. 调整点击频率和次数
3. 设置不同的运行时间范围
4. 添加更多的图像识别目标
5. 扩展多应用支持

## 许可证

该项目仅供学习和参考使用，请确保遵守相关法律法规，合理使用自动化工具。