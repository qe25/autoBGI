@echo off
chcp 65001 >nul
echo 开始打包AutoBGI自动化工具...
echo.

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python环境
    pause
    exit /b 1
)

REM 执行打包命令
pyinstaller --onefile --name="AutoBGI" --add-data="ready_icon.png;." --add-data="target_icon.png;." test.py

if %errorlevel% == 0 (
    echo.
    echo 打包成功完成！
    echo 生成的exe文件位于dist文件夹中
    dir /b dist\*.exe
) else (
    echo.
    echo 打包过程中发生错误
)

pause
