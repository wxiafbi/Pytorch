import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 1000)
y1 = np.sin(x)
y2 = np.cos(x)

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()

ax1.plot(x, y1, 'g-', label='sin')
ax2.plot(x, y2, 'b-', label='cos')

ax1.set_xlabel('X')
ax1.set_ylabel('sin', color='g')
ax2.set_ylabel('cos', color='b')

plt.show()
