import numpy as np

fx = lambda x: np.sin(10*x) + np.cos(3*x)

#biseksi sesuai program soal (a = 3.7, b = 3.8)
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

#pemindaian bracket dan semua akar pada [3, 6]
def cari_bracket(h):
    """Kembalikan semua [a, b] (lebar h) pada [3, 6] yang f(a)*f(b) < 0."""
    xs = np.arange(3.0, 6.0 + h/2, h)
    ys = fx(xs)
    return [(xs[i], xs[i+1]) for i in range(len(xs)-1) if ys[i]*ys[i+1] < 0]

def biseksi(a, b, tol=1e-6):
    """Biseksi sampai lebar interval <= tol. Kembalikan (akar, jumlah iterasi)."""
    n = 0
    while abs(b - a) > tol:
        c = (a + b) / 2
        if fx(a)*fx(c) < 0:
            b = c
        else:
            a = c
        n += 1
    return (a + b) / 2, n

print("\nJumlah bracket menurut increment grid:")
for h in [0.1, 0.01, 0.001]:
    print("increment %-6s -> %d bracket" % (h, len(cari_bracket(h))))

print("\nTabel bracket (grid 0.1):")
print("%-14s %-12s %-8s %-10s" % ("Bracket", "Akar", "Iterasi", "f(akar)"))
for (p, q) in cari_bracket(0.1):
    r, it = biseksi(p, q)
    print("[%.1f, %.1f]   %-12.6f %-8d %.2e" % (p, q, r, it, fx(r)))

print("\nSemua akar pada [3, 6] (grid 0.001):")
for (p, q) in cari_bracket(0.001):
    print("%.6f" % biseksi(p, q)[0])