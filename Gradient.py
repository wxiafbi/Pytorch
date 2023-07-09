import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# 创建数据
x = np.linspace(0, 10, 100)  # x轴数据范围
y = np.sin(x)  # y轴数据，可以根据需要自定义

# 创建图形对象
fig, ax = plt.subplots()
ax.set_ylim(-2,2)
# 创建初始折线，将所有数据点的y值设置为0
line, = ax.plot(x, np.zeros_like(x))

# 更新折线函数，逐渐显示数据
def update_line(num):
    line.set_ydata(np.sin(x) * np.exp(-0.1 * num))  # 可根据需要自定义更新方式
    return line,

# 创建动画
ani = animation.FuncAnimation(fig, update_line, frames=range(100), interval=500, blit=True)

# 显示图形
plt.show()
