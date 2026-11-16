<<<<<<< HEAD
import math

f = lambda x: x**4 - 11*x**2 + 7
g = lambda x: math.sqrt((x**4 + 7) / 11)

x_lama = 1.0          #x0
batas = 1e-6          #batasan f(x) mendekati 0

print(f"{'n':>2} {'x':>12} {'galat':>12} {'f(x)':>14}")
print(f"{0:>2} {x_lama:12.8f} {'-':>12} {f(x_lama):14.8f}")

n = 0
while True:
    n += 1
    x_baru = g(x_lama)
    galat = abs(x_baru - x_lama)
    print(f"{n:>2} {x_baru:12.8f} {galat:12.8f} {f(x_baru):14.8f}")
    if abs(f(x_baru)) < batas or n >= 100:
        break
    x_lama = x_baru

=======
import math

f = lambda x: x**4 - 11*x**2 + 7
g = lambda x: math.sqrt((x**4 + 7) / 11)

x_lama = 1.0          #x0
batas = 1e-6          #batasan f(x) mendekati 0

print(f"{'n':>2} {'x':>12} {'galat':>12} {'f(x)':>14}")
print(f"{0:>2} {x_lama:12.8f} {'-':>12} {f(x_lama):14.8f}")

n = 0
while True:
    n += 1
    x_baru = g(x_lama)
    galat = abs(x_baru - x_lama)
    print(f"{n:>2} {x_baru:12.8f} {galat:12.8f} {f(x_baru):14.8f}")
    if abs(f(x_baru)) < batas or n >= 100:
        break
    x_lama = x_baru

>>>>>>> 20b5519af957a4ca6ff5eefcce46a2797aad1c2e
print("Akar pendekatan:", x_baru)