import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import datetime

interval = 30


# 全部書き換えちゃうよ
def format_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        content = content.replace("\t", " ")
        content = content.replace("][", "] [")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


# でーたをよみとるよ
def read_data(file_path):
    data = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip() and not line.startswith("2024"):
                time_str, _, _, _, _, date_str = line.split(" ")
                time = datetime.datetime.strptime(time_str, "%H:%M").time()
                day_offset = int(date_str.split("]")[0].split("+")[1].replace("日", ""))
                hour = int(date_str.split("]")[1].split("時")[0])
                data.append((time, day_offset, hour))
    return data


# いい感じにしちゃうよ
def aggregate_data(data, interval=30):
    aggregated_data = {}
    for time, day_offset, hour in data:
        time_slot = (time.hour * 60 + time.minute) // interval
        day_slot = day_offset * 24 + hour
        if (time_slot, day_slot) not in aggregated_data:
            aggregated_data[(time_slot, day_slot)] = 0
        aggregated_data[(time_slot, day_slot)] += 1
    return aggregated_data


# グラフ作っちゃうよ
def plot_3d_graph(aggregated_data, interval=30):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    x = []
    y = []
    z = []

    for (time_slot, day_slot), count in aggregated_data.items():
        x.append(time_slot * interval)
        y.append(day_slot)
        z.append(count)

    ax.bar3d(x, y, np.zeros(len(z)), interval, 1, z, shade=True)

    ax.set_xlabel("Time (minutes)")
    ax.set_ylabel("Day Offset (hours)")
    ax.set_zlabel("Count")

    plt.show()


# ここだよ
file_path = "data20241214.txt"
format_file(file_path)
data = read_data(file_path)
aggregated_data = aggregate_data(data, interval=interval)
plot_3d_graph(aggregated_data, interval=interval)
