fx = lambda x: x**3 - 2*(x**2) + 6*x - 4.0

a = 0.0
b = 1.0

if fx(a) * fx(b) < 0:
    n = 0
    print("Iterasi\t a\t\t b\t\t Nilai Tengah")
    print("-" * 50)
    while abs(fx(a) * fx(b)) > 0.000001:
        c = (a + b) / 2
        print("%d\t %f\t %f\t %f" % (n, a, b, c))
        if fx(a) * fx(c) < 0.0:
            b = c
        else:
            a = c
        n += 1
    print("Akar persamaan adalah %f" % (c))
else:
    print("penentuan a dan b salah ")