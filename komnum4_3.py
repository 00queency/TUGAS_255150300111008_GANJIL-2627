f = lambda x: x**10 - 1

def false_position(a, b, Es):
    cp, Er, n = a, 100, 0
    print("Iter\ta\t\tb\t\tc\t\tf(c)\t\tEr(%)")
    while abs(Er) > Es:
        c = b - f(b) * (a - b) / (f(a) - f(b))
        if n > 0: Er = abs((c - cp) / c * 100)
        print(f"{n}\t{a:.6f}\t{b:.6f}\t{c:.6f}\t{f(c):.6f}\t{Er:.4f}")
        cp = c; n += 1
        if f(a) * f(c) < 0: b = c
        else: a = c
    return c, n

akar, n = false_position(0.9, 1.2, 0.1)