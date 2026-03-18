import os
import subprocess
import sys
from PyInstaller.__main__ import run as pyinstaller_run

def create_exe():
    """
    将test.py打包成exe文件
    """
    print("开始打包AutoBGI自动化工具...")
    
    # 检查test.py是否存在
    if not os.path.exists('test.py'):
        print("错误：找不到test.py文件")
        return
    
    # PyInstaller参数
    args = [
        '--onefile',           # 打包成单个exe文件
        '--windowed',          # 不显示控制台窗口（如果不需要控制台输出可以使用）
        '--name=AutoBGI',      # 输出的exe文件名
        '--icon=',             # 可以指定图标文件路径，例如'icon.ico'
        '--add-data=ready_icon.png;.',  # 添加需要的图片资源
        '--add-data=target_icon.png;.',  # 添加需要的图片资源
        'test.py'
    ]
    
    # 移除不需要的参数（如果不需要窗口模式）
    args.remove('--windowed')
    
    # 如果有图标文件，取消下面几行的注释并修改图标路径
    # icon_path = 'icon.ico'  # 替换为你的图标文件路径
    # if os.path.exists(icon_path):
    #     for i, arg in enumerate(args):
    #         if arg.startswith('--icon='):
    #             args[i] = f'--icon={icon_path}'
    #             break
    
    # 查找png文件并添加它们
    for file in os.listdir('.'):
        if file.endswith('.png'):
            args.append(f'--add-data={file};.')
    
    print(f"执行PyInstaller命令: {' '.join(args)}")
    
    try:
        # 运行PyInstaller
        pyinstaller_run(args)
        print("打包成功！生成的exe文件位于dist目录下。")
    except Exception as e:
        print(f"打包失败: {str(e)}")

def create_batch_script():
    """
    创建一个批处理脚本，用于快速打包
    """
    script_content = '''@echo off
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
    dir /b dist\\*.exe
) else (
    echo.
    echo 打包过程中发生错误
)

pause
'''
    
    with open('build.bat', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("已创建build.bat批处理脚本，双击即可重新打包。")

if __name__ == '__main__':
    create_batch_script()
    create_exe()