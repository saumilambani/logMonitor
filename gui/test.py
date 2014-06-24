import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def animate(frameno):
    x = mu + sigma * np.random.randn(10000)
    n, _ = np.histogram(x, bins, normed=True)
    for rect, h in zip(patches, n):
        rect.set_height(h)

mu, sigma = 100, 15
fig, ax = plt.subplots()
x = mu + sigma * np.random.randn(10000)
n, bins, patches = plt.hist(x, 50, normed=1, facecolor='green', alpha=0.75)

ani = animation.FuncAnimation(fig, animate, blit=False, interval=10,
                              repeat=True)
plt.show()
