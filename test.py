import subprocess
import time
import os
import sys
import pyautogui
import cv2 # 用于图片处理
import numpy as np
import pygetwindow as gw  # 用于窗口管理 (需安装: pip install pygetwindow)
from datetime import datetime # 用于获取当前时间
# pyinstaller --onefile --name="AutoBGI" --add-data="ready_icon.png;." --add-data="target_icon.png;." test.py

# conda activate autobgi
# ================= 配置区域 =================
# 1. 软件路径 (Windows示例，Mac/Linux需调整)
# 注意：路径中的反斜杠 \ 需要转义为 \\ 或者使用 r"..." 原始字符串
APP_PATH_2 = r"C:\Users\24805\Desktop\胡桃 1.18.4.0.lnk"
time.sleep(20)
APP_PATH = r"G:\betterGI\BetterGI.exe"  # 这里以计算器为例，请替换为你的软件路径
time.sleep(10)  # 给软件一些时间启动，后续会通过图标确认是否完全加载
# 2. 图片模板路径
# 启动后用来确认软件已就绪的图标 (例如软件的主界面Logo或第一个按钮)
READY_ICON = 'ready_icon_2.png' 
# 需要持续点击的目标图标
TARGET_ICON = 'target_icon.png'

# 3. 参数设置
CONFIDENCE = 0.6          # 识别置信度
CHECK_INTERVAL = 10      # 搜索间隔 (秒)
MAX_WAIT_TIME = 60        # 等待软件启动的最大时间 (秒)
CLICK_COUNT_LIMIT = 5   # 限制点击次数 (设为 0 表示无限循环)
CLICK_DELAY = 1.0        # 点击target_icon后的等待时间 (秒)

START_HOUR = 8           # 开始运行的小时 (8点)
END_HOUR = 23            # 结束运行的小时 (23点，即晚上11点)

# 新增配置参数
SCREENSHOT_DIR = "error_screenshots"

# ===========================================

def create_screenshot_dir():
    """创建截图保存目录"""
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
        print(f"创建截图目录: {SCREENSHOT_DIR}")

def take_screenshot(filename=None):
    """截图并保存到指定目录"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
    
    filepath = os.path.join(SCREENSHOT_DIR, filename)
    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)
    print(f"截图已保存至: {filepath}")
    return filepath

def ensure_app_on_top(app_path):
    """确保打开的应用在最顶层"""
    app_filename = os.path.basename(app_path)
    app_name = os.path.splitext(app_filename)[0]
    
    # 尝试通过进程名查找窗口
    windows = gw.getWindowsWithTitle(app_name)
    if not windows:
        # 如果没找到精确匹配，尝试模糊匹配
        all_windows = gw.getAllWindows()
        for window in all_windows:
            if app_name.lower() in window.title.lower():
                windows.append(window)
    
    if windows:
        # 获取第一个匹配的窗口
        window = windows[0]
        try:
            # 激活窗口并置于顶层
            window.activate()
            print(f"已激活窗口: {window.title}")
            return True
        except Exception as e:
            print(f"激活窗口失败: {e}")
            try:
                # 如果activate失败，尝试show和focus
                window.restore()
                window.focus()
                print(f"已尝试恢复并聚焦窗口: {window.title}")
                return True
            except Exception as e2:
                print(f"窗口操作失败: {e2}")
                return False
    else:
        print(f"未找到标题包含 '{app_name}' 的窗口")
        create_screenshot_dir()
        take_screenshot(f"target_icon_fail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        return False


def launch_application(path):
    """启动应用程序"""
    if not os.path.exists(path):
        print(f"错误: 找不到软件路径 {path}")
        return False
    
    print(f"正在启动软件: {path} ...")
    try:
        # subprocess.Popen 启动程序而不阻塞当前脚本
        subprocess.Popen(path)
        print("先等10秒")
        time.sleep(10)  # 给软件一些时间启动，后续会通过图标确认是否完全加载
        return True
    except Exception as e:
        print(f"启动失败: {e}")
        return False

def wait_for_window_and_icon(icon_path, timeout=60):
    """
    等待软件启动并出现指定图标，确保窗口在前台
    """
    print(f"等待软件加载并识别 '{icon_path}' ...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        ensure_app_on_top(APP_PATH)
        # 识别图标
        location = locate_image_on_screen(icon_path, CONFIDENCE)
        
        if location:
            print(">>> 软件已就绪，检测到目标界面！")
            x, y, w, h = location
            center_x = x + w // 2
            center_y = y + h // 2
            print(f"准备点击 {icon_path} 图标，坐标: ({center_x}, {center_y})")
         
            # 可选：点击一下确认图标以确保窗口获得焦点
            pyautogui.click(center_x, center_y)
            print(f"已点击 {icon_path} 图标")
            time.sleep(5)
            return True
        
        print(f"等待中... ({int(time.time() - start_time)}s)")
        time.sleep(1.0)
        
        
    print("错误: 超时，未检测到软件界面。请检查图片或软件是否卡死。")
    create_screenshot_dir()
    take_screenshot(f"ready_icon_fail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

    print(">>> 开始执行恢复操作...")
    time.sleep(5)
    print(f"点击坐标 (593, 455)")
    pyautogui.click(593, 455)
    time.sleep(5)
    print(f"点击坐标 (858, 295)")
    pyautogui.click(858, 295)

    return False

def locate_image_on_screen(image_path, threshold):
    """封装图像识别逻辑"""
    if not os.path.exists(image_path):
        print(f"错误: 找不到图片模板 {image_path}")
        create_screenshot_dir()
        take_screenshot(f"target_icon_fail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

        print(">>> 开始执行恢复操作...")
        time.sleep(5)
        print(f"点击坐标 (664, 455)")
        pyautogui.click(664, 455)
        time.sleep(5)
        print(f"点击坐标 (858, 295)")
        pyautogui.click(858, 295)

        sys.exit(1)
        
    template = cv2.imread(image_path)
    if template is None:
        return None
        
    h, w = template.shape[:2]
    
    screenshot = pyautogui.screenshot()
    screen_np = np.array(screenshot)
    screen_cv = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
    
    result = cv2.matchTemplate(screen_cv, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    if max_val >= threshold:
        return (max_loc[0], max_loc[1], w, h) # 返回 x, y, w, h
    return None


def check_time_range():
    """检查当前时间是否在设定的时间范围内，如果是则退出程序"""
    current_time = datetime.now()
    current_hour = current_time.hour
    
    print(f"当前时间: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 如果当前时间在8:00-23:59之间，则退出程序
    if START_HOUR <= current_hour <= END_HOUR:
        print(f"当前时间在 {START_HOUR}:00 - {END_HOUR}:59 之间，程序将退出。")
        sys.exit(0)  # 正常退出程序
    else:
        print(f"当前时间不在限制范围内，程序将继续运行。")



def main():
    print(READY_ICON)
    print(TARGET_ICON)

    # 开启故障保护 (鼠标移到左上角停止)
    pyautogui.FAILSAFE = True
    check_time_range()
    print("--- 自动化流程开始 ---")

        # 创建截图目录
    create_screenshot_dir()

    if not launch_application(APP_PATH_2):
        print("签到应用程序启动失败")
    else:
        print("签到应用程序已启动")
    
    time.sleep(30)
    
    # 步骤 1: 启动软件
    if not launch_application(APP_PATH):
        return
    print("软件启动命令已发送，正在等待")
    print("等待10秒")
    time.sleep(10)  # 给软件一些时间启动，后续会通过图标确认是否完全加载

    # 步骤 2: 等待软件完全加载并出现特征图
    # 这一步非常关键，确保后续操作在正确的上下文中
    if not wait_for_window_and_icon(READY_ICON, MAX_WAIT_TIME):
        print("流程终止：未能确认软件启动。")
        return

    # 步骤 3: 开始循环点击目标
    print(f"开始执行自动点击任务：{TARGET_ICON}")
    click_count = 0
    
    try:
        while True:
            ensure_app_on_top(APP_PATH)
            loc = locate_image_on_screen(TARGET_ICON, CONFIDENCE)
            print(loc)
            if not loc:
                print("未找到目标图标，请检查图片或软件是否卡死。")
                 # 识别失败时保存截图
                create_screenshot_dir()
                take_screenshot(f"target_icon_fail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                print(">>> 开始执行恢复操作...")
                time.sleep(5)
                print(f"点击坐标 (664, 455)")
                pyautogui.click(664, 455)
                time.sleep(5)
                print(f"点击坐标 (858, 295)")
                pyautogui.click(858, 295)

                
                break
            if loc:
                x, y, w, h = loc
                center_x = x + w // 2
                center_y = y + h // 2
                
                print(f"[{click_count+1}] 发现目标，点击坐标: ({center_x}, {center_y})")
                pyautogui.moveTo(center_x, center_y)
                time.sleep(5) 
                ensure_app_on_top(APP_PATH)
                # 执行点击
                pyautogui.click(center_x, center_y)
                pyautogui.click()
                click_count += 1
                
                # 如果设置了点击次数限制
                if CLICK_COUNT_LIMIT > 0 and click_count >= CLICK_COUNT_LIMIT:
                    print(f"已达到最大点击次数 ({CLICK_COUNT_LIMIT})，任务结束。")
                    break
                
                # 点击后等待一小会儿，模拟人类操作或等待界面刷新
                time.sleep(CLICK_DELAY)
            else:
                # 如果目标暂时消失（例如弹窗、加载动画），可以选择等待或重试
                # print("目标暂时未找到，继续搜索...")
                time.sleep(CHECK_INTERVAL)
                
    except KeyboardInterrupt:
        print("\n用户中断，程序停止。")

if __name__ == "__main__":
    # 依赖检查提示
    try:
        import pygetwindow
    except ImportError:
        print("提示: 建议安装 pygetwindow 以获得更好的窗口控制能力: pip install pygetwindow")
        
    main()