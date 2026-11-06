import math

def biseksi(f, a, b, Es):
    cp, Er, n, rows = a, 100, 0, []
    while abs(Er) > Es:
        c = (a + b) / 2
        if n > 0: Er = abs((c - cp) / c * 100)
        rows.append((n, a, b, c, f(c), Er))
        cp = c; n += 1
        if f(a) * f(c) < 0: b = c
        else: a = c
    return rows

def false_position(f, a, b, Es):
    cp, Er, n, rows = a, 100, 0, []
    while abs(Er) > Es:
        c = b - f(b) * (a - b) / (f(a) - f(b))
        if n > 0: Er = abs((c - cp) / c * 100)
        rows.append((n, a, b, c, f(c), Er))
        cp = c; n += 1
        if f(a) * f(c) < 0: b = c
        else: a = c
    return rows

def cetak(nama, rows):
    print(f"\n{nama}")
    print("Iter\ta\t\tb\t\tc\t\tf(c)\t\tEr(%)")
    for n, a, b, c, fc, Er in rows:
        print(f"{n}\t{a:.6f}\t{b:.6f}\t{c:.6f}\t{fc:.6f}\t{Er:.4f}")

Es = 0.1
fungsi = [
    ("f(x) = x^3 - 2x^2 + 6x - 4", lambda x: x**3 - 2*x**2 + 6*x - 4, 0, 1),
    ("f(x) = cos(x) - x",          lambda x: math.cos(x) - x,          0, 1),
]

ringkasan = []
for nama, f, a, b in fungsi:
    if f(a) * f(b) >= 0:
        print(f"{nama}: pemilihan a dan b salah"); continue
    print("=" * 60); print(nama, f"| interval [{a}, {b}]")
    rb = biseksi(f, a, b, Es)
    rf = false_position(f, a, b, Es)
    cetak("Biseksi", rb)
    cetak("False-Position", rf)
    ringkasan.append((nama, len(rb), rb[-1][3], len(rf), rf[-1][3]))

print("\n" + "=" * 60)
print("RINGKASAN (Es = 0.1%)")
print(f"{'Fungsi':30}{'Iter Bis':>9}{'Akar Bis':>12}{'Iter FP':>9}{'Akar FP':>12}")
for nama, ib, ab, ifp, afp in ringkasan:
    print(f"{nama:30}{ib:>9}{ab:>12.6f}{ifp:>9}{afp:>12.6f}")