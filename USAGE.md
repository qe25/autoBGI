# AutoBGI 使用说明

## 概述
AutoBGI 是一个基于图像识别的自动化工具，用于自动启动应用程序并在其界面上执行点击操作。

## 打包好的程序如何使用

1. **准备文件**：
   - 将 [AutoBGI.exe](file:///G:/AutoBGI/dist/AutoBGI.exe) 复制到一个新文件夹中
   - 将 [ready_icon.png](file:///G:/AutoBGI/ready_icon.png) 和 [target_icon.png](file:///G:/AutoBGI/target_icon.png) 图片文件复制到同一文件夹中
   - 根据需要修改 [APP_PATH](file:///G:/AutoBGI/test.py#L9-L9) 配置（如果需要不同应用路径）

2. **运行程序**：
   - 双击 [AutoBGI.exe](file:///G:/AutoBGI/dist/AutoBGI.exe) 运行
   - 程序将自动启动指定的应用程序
   - 等待应用程序加载完成
   - 开始自动点击 [target_icon.png](file:///G:/AutoBGI/target_icon.png) 定义的图标

## 配置参数说明

在原始的 [test.py](file:///G:/AutoBGI/test.py) 文件中，你可以修改以下参数：

- [APP_PATH](file:///G:/AutoBGI/test.py#L9-L9): 目标应用程序路径
- [READY_ICON](file:///G:/AutoBGI/test.py#L14-L14): 用于确认应用已就绪的图标
- [TARGET_ICON](file:///G:/AutoBGI/test.py#L16-L16): 需要持续点击的目标图标
- [CONFIDENCE](file:///G:/AutoBGI/test.py#L19-L19): 图像识别的置信度 (0.0-1.0)
- [CHECK_INTERVAL](file:///G:/AutoBGI/test.py#L20-L20): 搜索目标图标的时间间隔（秒）
- [MAX_WAIT_TIME](file:///G:/AutoBGI/test.py#L21-L21): 等待应用程序启动的最大时间（秒）
- [CLICK_COUNT_LIMIT](file:///G:/AutoBGI/test.py#L22-L22): 最大点击次数（0表示无限制）

## 重要提醒

1. **安全机制**：程序包含 `pyautogui.FAILSAFE = True`，将鼠标移动到屏幕左上角可以紧急停止程序。

2. **图像文件**：确保 [ready_icon.png](file:///G:/AutoBGI/ready_icon.png) 和 [target_icon.png](file:///G:/AutoBGI/target_icon.png) 图像清晰，对比度高，以便准确识别。

3. **权限问题**：在某些系统上可能需要以管理员身份运行。

4. **屏幕缩放**：如果屏幕缩放不是100%，可能会影响图像识别准确性。

## 重新打包

如果你修改了 [test.py](file:///G:/AutoBGI/test.py) 中的配置，可以通过以下方式重新打包：

1. 运行 [build.bat](file:///G:/AutoBGI/build.bat) 文件
2. 或者在命令行中执行：
   ```
   pyinstaller --onefile --name="AutoBGI" --add-data="ready_icon.png;." --add-data="target_icon.png;." test.py
   ```

## 故障排除

- 如果无法启动应用程序，请检查 [APP_PATH](file:///G:/AutoBGI/test.py#L9-L9) 是否正确
- 如果无法识别图标，请调整 [CONFIDENCE](file:///G:/AutoBGI/test.py#L19-L19) 值或更新图像文件
- 如果点击位置不准确，请确保截图时应用程序处于正常大小且没有缩放