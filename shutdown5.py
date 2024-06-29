import os
from pynput import mouse, keyboard
import tkinter as tk
from tkinter import font, messagebox
import threading
import subprocess
import platform
from datetime import datetime, time
import time


# 开机运行提示
def show_custom_message_box():
    # 创建自定义的Tkinter窗口
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    # 创建顶级窗口作为信息框
    top = tk.Toplevel(root)
    top.overrideredirect(True)  # 移除窗口边框
    top.title("自动关机小程序")
    top.attributes('-fullscreen', False)  # 移除全屏模式
    top.attributes('-topmost', True)  # 窗口置顶
    top.overrideredirect(False)  # 在设置属性后再关闭overrideredirect

    # 设置窗口背景色为黑色
    top.configure(bg='black')

    # 设置字体
    font_size = 18  # 字体大小
    custom_font = font.Font(family='黑体', size=font_size, weight='bold')

    # 创建标签并设置分段文本、字体和背景色
    text = """
    触碰动态检测从12：10 和 21：35 开始，若5分钟内无操作，则    
    电脑会在中午12：15分和晚上21：40分自动关机。
    要想关闭则打开任务管理器，找到shutdown.py文件，然后右键结束进程即可。
    请在电脑操作的同学记得将自己的东西传进自己的u盘或者网盘。
    有建议 or 问题的可以联系QQ：2982607287，备注来意。
————————————————————————————————————————————————————————————————
        亲爱的旅院同学们：
    如果您对学习编程有兴趣，却不知道从何入手，欢迎加入咱们团队：

    Lead Fire"领灯者"团队

    另外，如果您对计算机类竞赛，有兴趣的话，也可以加入咱们团队，团队将会提供资源。

    注：
    本团队是大学生自发组织的团队
    主要目的是为了提升自身的编程能力，
    为将来的就业，考研，学习等增加资本。
————————————————————————————————————————————————————————————————
    团队Q群：759089890 （备注来意）
    创建者Q：2982607287 （备注来意）
    """

    label = tk.Label(top, text=text, font=custom_font, justify='left', bg='black',
                     fg='cyan')  # 设置前景色为白色
    label.pack(pady=500)  # pady添加垂直填充

    # 创建确定按钮，并设置背景色和前景色
    ok_button = tk.Button(top, text="确定", command=top.destroy, bg='black', fg='cyan')
    ok_button.pack(side=tk.BOTTOM, pady=10)  # pady添加底部填充

    label.pack(pady=50, padx=10, fill='x', expand=True)

    # 进入Tkinter的事件循环，等待用户交互
    top.mainloop()


# 在新线程中显示自定义消息框
threading.Thread(target=show_custom_message_box).start()

# 设置超时时间（秒）
timeout = 300  # 5分钟 300

# 设置剩余5min提醒
time_ten = 300  # 5分钟 300

# 用来定义剩余10分钟是否触发过
show_message_if = False

# 定义一个变量来跟踪是否有活动
is_active = False


# 定义一个函数，在鼠标或键盘事件触发时设置is_active为True
def on_event(event):
    global is_active
    is_active = True


def on_move(x, y):
    global is_active
    is_active = True


def on_click(x, y, button, pressed):
    global is_active
    is_active = True


def show_message():
    global show_message_if
    messagebox.showinfo("提示", "若无操作则5分钟后自动关机")


# 创建提示窗口
root = tk.Tk()
root.withdraw()  # 隐藏主窗口

now_if = datetime.now()
current_hour1 = now_if.hour
if current_hour1 >= 13:
    # 获取当前时间
    now = datetime.now()
    target_time = datetime.combine(now.date(),
                                   datetime.min.time().replace(hour=21, minute=35, second=0, microsecond=0))  # 21：35

    while True:  # 让这个一直循环直到时间到晚上9点35以后
        now_1 = datetime.now()
        if now_1 >= target_time:
            break
        else:
            time.sleep(1)

    # 使用pynput监听鼠标和键盘事件
    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
    keyboard_listener = keyboard.Listener(on_press=on_event)

    # 启动监听器
    mouse_listener.start()
    keyboard_listener.start()
    # 计时器
    start_time = time.time()

    while True:
        if time.time() - start_time > time_ten and show_message_if == False:
            threading.Thread(target=show_message).start()
            show_message_if = True

        if is_active:  # 如果有操作了，就重置时间
            # 重置计时器和状态
            start_time = time.time()
            is_active = False
            show_message_if = False

        elif time.time() - start_time > timeout:
            # 执行关机命令
            os.system("shutdown /s /t 1")  # Windows系统关机命令

            continue
        time.sleep(1)  # 每秒检查一次
else:
    now = datetime.now()
    target_time = datetime.combine(now.date(),
                                   datetime.min.time().replace(hour=12, minute=10, second=0, microsecond=0))  # 12:10

    while True:  # 让这个一直循环直到时间到中午12：10分点半以后
        now_1 = datetime.now()
        if now_1 >= target_time:
            break
        else:
            time.sleep(1)

    # 使用pynput监听鼠标和键盘事件
    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
    keyboard_listener = keyboard.Listener(on_press=on_event)

    # 启动监听器
    mouse_listener.start()
    keyboard_listener.start()
    # 计时器
    start_time = time.time()

    while True:
        if time.time() - start_time > time_ten and show_message_if == False:
            threading.Thread(target=show_message).start()
            show_message_if = True

        if is_active:
            # 重置计时器和状态
            start_time = time.time()
            is_active = False
            show_message_if = False

        elif time.time() - start_time > timeout:
            # 执行关机命令
            os.system("shutdown /s /t 1")  # Windows系统关机命令

            continue
        time.sleep(1)  # 每秒检查一次

# 停止监听器
mouse_listener.stop()
keyboard_listener.stop()

# 确保监听器不再运行
mouse_listener.join()
keyboard_listener.join()

