import random, time, tracemalloc
 
def buat_sistem(n, seed=42):
    """Matriks diagonal dominan (menjamin Gauss-Seidel konvergen)."""
    random.seed(seed)
    A = [[random.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        A[i][i] = sum(abs(x) for x in A[i]) + 1.0
    x_asli = [1.0] * n
    b = [sum(A[i][j] * x_asli[j] for j in range(n)) for i in range(n)]
    return A, b
 
def residual(A, x, b):
    """Norma-infinity dari b - Ax."""
    n = len(b)
    return max(abs(b[i] - sum(A[i][j] * x[j] for j in range(n))) for i in range(n))
 
#a. Eliminasi Gauss dan partial pivoting 
def gauss(A, b):
    n = len(b)
    A = [r[:] for r in A]; b = b[:]
    ops = 0
    for k in range(n - 1):
        p = max(range(k, n), key=lambda i: abs(A[i][k]))
        if p != k:
            A[k], A[p] = A[p], A[k]; b[k], b[p] = b[p], b[k]
        for i in range(k + 1, n):
            f = A[i][k] / A[k][k]; ops += 1
            for j in range(k, n):
                A[i][j] -= f * A[k][j]; ops += 2
            b[i] -= f * b[k]; ops += 2
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = sum(A[i][j] * x[j] for j in range(i + 1, n))
        ops += 2 * (n - 1 - i)
        x[i] = (b[i] - s) / A[i][i]; ops += 2
    return x, ops
 
#b. Gauss-Seidel
def gauss_seidel(A, b, tol, maks=10000):
    n = len(b)
    x = [0.0] * n
    ops = 0
    for it in range(1, maks + 1):
        galat = 0.0
        for i in range(n):
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            baru = (b[i] - s) / A[i][i]
            ops += 2 * (n - 1) + 2
            galat = max(galat, abs(baru - x[i]))
            x[i] = baru
        if galat < tol:
            break
    return x, it, ops
 
def ukur(fungsi, *args):
    tracemalloc.start()
    t0 = time.perf_counter()
    hasil = fungsi(*args)
    dt = time.perf_counter() - t0
    _, puncak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return hasil, dt, puncak / 1024
 
if __name__ == "__main__":
    n = 100
    A, b = buat_sistem(n)
    print(f"Ukuran sistem: {n}x{n}\n")
 
    (x, ops), dt, mem = ukur(gauss, A, b)
    print("== (a) Eliminasi Gauss (partial pivoting) ==")
    print(f"Waktu eksekusi : {dt*1000:.3f} ms")
    print(f"Memori puncak  : {mem:.1f} KiB (tambahan di luar A,b asli)")
    print(f"Operasi aritm. : {ops}  (teori ~ 2n^3/3 = {int(2*n**3/3)})")
    print(f"Residual akhir : {residual(A, x, b):.3e}\n")
 
    print("== (b) Gauss-Seidel ==")
    print(f"{'Toleransi':>10} {'Iterasi':>8} {'Residual':>12} {'Waktu(ms)':>10} {'Operasi':>10}")
    for tol in (1e-2, 1e-4, 1e-6):
        (x, it, ops), dt, mem = ukur(gauss_seidel, A, b, tol)
        print(f"{tol:>10.0e} {it:>8} {residual(A, x, b):>12.3e} {dt*1000:>10.3f} {ops:>10}")
 