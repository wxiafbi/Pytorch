import torch
import matplotlib.pyplot as plt

a = torch.linspace(-10, 10, 1000)
b = torch.sin(a)
c = torch.cos(b)
# fig, ax = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(9, 6))
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

plt.title(r'$\alpha > \beta$')
ax.scatter(a, b, c, marker="o")

ax.set_xlabel('a')
ax.set_ylabel('b')
# plt.plot(a, b, scalex=True, color='yellow')
# plt.grid()
# plt.xlim(-10, 10)
# plt.ylim(-1, 1)
# fig.colorbar(shrink=0.5, aspect=5)
plt.show()
