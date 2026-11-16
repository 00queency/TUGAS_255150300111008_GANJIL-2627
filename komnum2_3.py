import numpy as np

fx = lambda x: np.sin(10*x) + np.cos(3*x)
a = 3.7
b = 3.8

if (fx(a)*fx(b)) < 0:
    n = 0
    print("%-8s %-12s %-12s %-12s" % ("Iterasi", "a", "b", "Nilai Tengah"))
    print("-" * 48)
    while abs(fx(a)*fx(b)) > 0.000001:
        c = (a+b)/2
        print("%-8d %-12.6f %-12.6f %-12.6f" % (n, a, b, c))
        if (fx(a)*fx(c)) < 0.0:
            b = c
        else:
            a = c
        n += 1
    print("Akar persamaan adalah %f" % (c))
else:
    print("penentuan a dan b salah ")