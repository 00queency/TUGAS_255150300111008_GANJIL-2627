import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0.9, 1.2, 300)
y = x**10 - 1
plt.plot(x, y, 'b-')
plt.axhline(y=0, color='r')
plt.grid(True); plt.xlabel('X'); plt.ylabel('Y')
plt.title('f(x) = x^10 - 1')
plt.show()