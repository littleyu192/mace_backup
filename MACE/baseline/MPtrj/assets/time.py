import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def plot(log_file):
    # 存储时间戳的列表
    timestamps = []

    # 解析日志文件
    with open(log_file, 'r') as file:
        for line in file:
            if 'INFO' in line and 'MAE_E_per_atom' in line:
                # 提取时间戳部分
                timestamp_str = line.split(' INFO')[0]
                # 转换为 datetime 对象
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
                timestamps.append(timestamp)

    # 计算时间间隔
    time_intervals = []
    for i in range(2, len(timestamps)):
        interval = (timestamps[i] - timestamps[i - 1]).total_seconds()
        time_intervals.append(interval)

    # 将时间间隔转换为 DataFrame
    df = pd.DataFrame(time_intervals, columns=['Time Interval (seconds)'])


    # 或者绘制时间间隔的折线图
    plt.plot(df['Time Interval (seconds)'], label=log_file, marker='o')

plt.figure(figsize=(10, 6))

plot('logs/L0_hpc_1node.log')
plot('logs/L0_ustc_1node.log')
plot('logs/L0_ustc_2node.log')
plot('logs/L0_wh_1node.log')
plot('logs/L0_wh_4node.log')
plot('logs/L0_dcu_2node.log')
plot('logs/L1_ustc_2node.log')

plt.xlabel('Interval Index')
plt.ylabel('Time Interval (seconds)')
plt.title('Time Intervals Between INFO Entries')
plt.grid(True)
plt.legend()
plt.savefig('time.png')
