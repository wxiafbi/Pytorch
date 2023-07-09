import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax3 = plt.axes(projection='3d')

plt.rcParams['font.sans-serif'] = ['FangSong']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 定义三维数据
xx = np.arange(-5, 5, 0.5)
yy = np.arange(-5, 5, 0.5)
X, Y = np.meshgrid(xx, yy)
Z = np.sin(X)+np.cos(Y)

# 作图
ax3.plot_surface(X, Y, Z, cmap='rainbow')
# 改变cmap参数可以控制三维曲面的颜色组合, 一般我们见到的三维曲面就是 rainbow 的

plt.show()
