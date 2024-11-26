import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime as dt
import os
from matplotlib.widgets import Slider

# 获取当前脚本所在目录，并构建文件路径
file_path = os.path.join(os.path.dirname(__file__), 'serial_log.txt')

# 初始时间和数据
times = []
values = []

# 将时间转换为秒
def time_to_seconds(time_obj):
    return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second

# 读取日志文件并解析
def read_data():
    global times, values
    file_size = os.path.getsize(file_path)
    
    # 如果文件不为空并且有更新的内容
    if file_size > 0:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            
            # 只处理新增的行
            new_lines = lines[len(times):]
            for line in new_lines:
                # 分割时间和数据
                parts = line.split("] ")
                time_str = parts[0][1:]  # 去掉前后的 [ ]
                value = float(parts[1])  # 转为浮点数
                
                # 转换时间为 datetime 对象，只保留时间（时:分:秒）
                time_obj = dt.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").time()
                
                # 存储新的时间和数据
                times.append(time_obj)
                values.append(value)

# 动态更新图表
def update_plot(frame):
    read_data()  # 读取新数据
    ax.clear()  # 清除当前的图表
    
    # 将时间转换为秒，方便处理
    times_in_seconds = [time_to_seconds(t) for t in times]
    
    # 控制显示时间窗口
    start_time = times_in_seconds[slider_position] if slider_position < len(times_in_seconds) else times_in_seconds[-1]
    end_time = start_time + slider_val
    
    ax.plot(times_in_seconds, values, marker='o', linestyle='-', color='b', label="Data")
    
    # 设置x轴的范围，使用时间的秒数来设置
    ax.set_xlim(start_time, end_time)
    
    ax.set_title("Time vs Data", fontsize=16)
    # ax.set_xlabel("Time (hh:mm:ss)", fontsize=14)
    ax.set_ylabel("Value", fontsize=14)
    ax.grid(True)
    
    # 重新设置时间刻度
    ax.xaxis.set_major_locator(plt.MaxNLocator(6))  # 每次显示最多6个时间刻度
    ax.set_xticks([start_time + i * (end_time - start_time) / 5 for i in range(6)])
    
    # 设置自定义的时间格式
    ax.set_xticklabels([str(dt.timedelta(seconds=int(i))) for i in ax.get_xticks()])

    ax.legend()

# 创建绘图对象
fig, ax = plt.subplots(figsize=(10, 5))

# 去掉默认的 "Figure 1" 标题
plt.gcf().canvas.manager.set_window_title("中科生物")

# 添加第一个滑块控件来调整时间窗口
# ax_slider = plt.axes([0.25, 0.01, 0.65, 0.03], facecolor='lightgoldenrodyellow')
ax_slider = plt.axes([0.25, 0.00, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider_val = 60  # 默认显示60秒的数据
slider = Slider(ax_slider, 'Time Window (sec)', 10, 600, valinit=slider_val, valstep=10)

# 更新滑块值时调整显示窗口
def update_slider(val):
    global slider_val
    slider_val = val
    update_plot(None)

slider.on_changed(update_slider)

# 添加第二个滑块控件来滚动显示时间段
ax_slider_position = plt.axes([0.25, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider_position = 0  # 默认显示从数据的第一个点开始
slider_position_slider = Slider(ax_slider_position, 'Scroll Time', 0, 100, valinit=slider_position, valstep=1)

# 更新滚动时间段
def update_slider_position(val):
    global slider_position
    slider_position = int(val)
    update_plot(None)

slider_position_slider.on_changed(update_slider_position)

# 动态更新图表，每隔1秒检查一次文件更新
ani = animation.FuncAnimation(fig, update_plot, interval=1000)

# 显示图表
plt.tight_layout()
plt.show()

