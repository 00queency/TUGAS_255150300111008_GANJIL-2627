import numpy as np
import matplotlib.pyplot as plt

x = np.arange(3.0, 6.0, 0.01)
y = np.sin(10*x) + np.cos(3*x)

plt.plot(x, y, '-')
plt.grid(True); plt.axhline(y=0, color='r')
plt.xlabel("x"); plt.ylabel("f(x)")
plt.show()