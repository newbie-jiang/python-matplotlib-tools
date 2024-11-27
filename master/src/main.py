import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
import datetime as dt
import os
from matplotlib.widgets import Slider

# 获取当前脚本所在目录，并构建文件路径
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'serial_log.txt')

# 初始时间和数据
times = []
values = []

# 读取日志文件并解析
def read_data():
    global times, values
    file_size = os.path.getsize(file_path)

    # 如果文件不为空
    if file_size > 0:
        with open(file_path, 'r') as file:
            lines = file.readlines()

            # 只处理新增的行
            new_lines = lines[len(times):]
            for line in new_lines:
                # 分割时间和数据
                parts = line.strip().split("] ")
                if len(parts) != 2:
                    continue  # 跳过格式不正确的行
                time_str = parts[0][1:]  # 去掉前后的 [ ]
                try:
                    value = float(parts[1])  # 转为浮点数
                except ValueError:
                    continue  # 跳过无法转换为浮点数的行

                # 转换时间为 datetime 对象
                try:
                    time_obj = dt.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue  # 跳过无法解析的时间格式

                # 存储新的时间和数据
                times.append(time_obj)
                values.append(value)

# 动态更新图表
def update_plot(frame):
    global slider_position, time_range
    read_data()  # 读取新数据
    ax.clear()  # 清除当前的图表

    # 如果没有数据，直接返回
    if not times:
        return

    # 控制显示时间窗口的起始位置和结束位置
    start_index = int(slider_position)
    end_time = times[0] + dt.timedelta(seconds=slider_position + slider_val)

    # 获取可显示的数据范围
    display_times = []
    display_values = []
    for t, v in zip(times, values):
        if times[start_index] <= t <= end_time:
            display_times.append(t)
            display_values.append(v)

    # 绘制图表
    ax.plot(display_times, display_values, marker='o', linestyle='-', color='b', label="Data")

    # 设置x轴的范围
    ax.set_xlim(times[start_index], end_time)

    ax.set_title("Time vs Data", fontsize=16)
    ax.set_ylabel("Value", fontsize=14)
    ax.grid(True)

    # 设置 x 轴为日期格式
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())

    # 自动旋转日期标签
    plt.setp(ax.get_xticklabels(), rotation=0, ha='right')

    ax.legend()

    # 更新 time_range 并更新滑块最大值
    time_range = calculate_time_range()
    if time_range > slider_position_slider.valmax:
        slider_position_slider.valmax = time_range
        slider_position_slider.ax.set_xlim(slider_position_slider.valmin, slider_position_slider.valmax)
        slider_position_slider.ax.figure.canvas.draw_idle()

# 计算日志文件中记录的时间差（单位：秒）
def calculate_time_range():
    if len(times) < 2:  # 确保有至少两个数据点
        print("数据点不足，无法计算时间差。")
        return 0  # 返回0表示时间差为0

    # 计算时间差并返回
    time_range = (times[-1] - times[0]).total_seconds()
    print(f"计算的时间差: {time_range} 秒")  # 输出时间差，帮助调试

    return time_range  # 返回时间差

# 更新滑块值时调整显示窗口
def update_slider(val):
    global slider_val
    slider_val = val
    update_plot(None)

# 更新滚动时间段
def update_slider_position(val):
    global slider_position
    slider_position = val
    update_plot(None)

# 创建绘图对象
fig, ax = plt.subplots(figsize=(10, 5))

# 去掉默认的 "Figure 1" 标题
plt.gcf().canvas.manager.set_window_title("中科生物")

# 首先调用一次 read_data() 来初始化数据
read_data()

# 初始化滑块位置
slider_position = 0
slider_val = 60  # 默认显示60秒的数据

# 添加第一个滑块控件来调整时间窗口
ax_slider = plt.axes([0.25, 0.03, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Time Window (sec)', 10, 600, valinit=slider_val, valstep=10)
slider.on_changed(update_slider)

# 初始时，计算时间差
time_range = calculate_time_range()
print(f"初始计算的时间差: {time_range} 秒")  # 输出时间差，帮助调试

# 如果时间差为 0，设置一个默认的最大值，例如 100
time_range = time_range if time_range > 0 else 100

# 添加第二个滑块控件来滚动显示时间段
ax_slider_position = plt.axes([0.25, 0.01, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider_position_slider = Slider(ax_slider_position, 'Scroll Time (sec)', 0, time_range, valinit=slider_position, valstep=1)
slider_position_slider.on_changed(update_slider_position)

# 动态更新图表，每隔1秒检查一次文件更新
ani = animation.FuncAnimation(fig, update_plot, interval=1000)

# 显示图表
plt.tight_layout()
plt.show()
