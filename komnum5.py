import math
import time

# Perubahan input pengguna
SAFE = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
SAFE.update({"abs": abs, "ln": math.log, "e": math.e, "pi": math.pi})


def buat_fungsi(teks):
    ekspresi = teks.replace("^", "**")
    kode = compile(ekspresi, "<fungsi>", "eval")
    return lambda x: eval(kode, {"__builtins__": {}}, {**SAFE, "x": x})


def turunan_numerik(f, x, h=1e-6):
    return (f(x + h) - f(x - h)) / (2 * h)  # selisih tengah


# Metode tertutup: biseksi
def biseksi(f, a, b, tol, maks_iter):
    if f(a) * f(b) > 0:
        raise ValueError("f(a) dan f(b) harus berbeda tanda (tidak ada akar terkurung).")
    riwayat, c_lama = [], None
    for i in range(1, maks_iter + 1):
        c = (a + b) / 2
        err = abs((c - c_lama) / c) * 100 if c_lama is not None and c != 0 else None
        riwayat.append((i, c, f(c), err))
        if f(c) == 0 or (err is not None and err < tol) or (b - a) / 2 < tol * 1e-4:
            return c, riwayat, True
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
        c_lama = c
    return c, riwayat, False


# Metode terbuka: newton-raphson
def newton_raphson(f, x0, tol, maks_iter):
    riwayat, x = [], x0
    for i in range(1, maks_iter + 1):
        d = turunan_numerik(f, x)
        if abs(d) < 1e-14:
            raise ZeroDivisionError(f"f'(x) ~ 0 di x = {x:.6f}; pilih tebakan awal lain.")
        x_baru = x - f(x) / d
        err = abs((x_baru - x) / x_baru) * 100 if x_baru != 0 else abs(x_baru - x)
        riwayat.append((i, x_baru, f(x_baru), err))
        x = x_baru
        if err < tol or f(x) == 0:
            return x, riwayat, True
    return x, riwayat, False


# Display
def cetak_tabel(judul, riwayat, maks_baris=15):
    print(f"\n==={judul}===")
    print(f"{'Iter':>5} {'x':>18} {'f(x)':>16} {'Error (%)':>14}")
    tampil = riwayat if len(riwayat) <= maks_baris else riwayat[:maks_baris - 3] + [None] + riwayat[-2:]
    for r in tampil:
        if r is None:
            print(f"{'...':>5}")
            continue
        i, x, fx, err = r
        es = "-" if err is None else f"{err:.6e}"
        print(f"{i:>5} {x:>18.10f} {fx:>16.6e} {es:>14}")


def jalankan(f, a, b, x0, tol, maks_iter):
    hasil = {}
    for nama, fungsi in (
        ("Biseksi (tertutup)", lambda: biseksi(f, a, b, tol, maks_iter)),
        ("Newton-Raphson (terbuka)", lambda: newton_raphson(f, x0, tol, maks_iter)),
    ):
        try:
            t0 = time.perf_counter()
            akar, riw, konv = fungsi()
            waktu = (time.perf_counter() - t0) * 1000
            cetak_tabel(nama, riw)
            hasil[nama] = dict(akar=akar, iter=len(riw), fx=abs(f(akar)), konv=konv, waktu=waktu)
        except (ValueError, ZeroDivisionError, OverflowError) as err:
            print(f"\n==={nama}===\nGAGAL: {err}")
            hasil[nama] = None
    return hasil


def analisis(hasil):
    print("\n" + "=" * 10 + "PERBANDINGAN HASIL" + "=" * 10)
    print(f"{'Metode':<26}{'Akar':>16}{'Iterasi':>9}{'|f(akar)|':>14}{'Waktu(ms)':>11}")
    for nama, h in hasil.items():
        if h is None:
            print(f"{nama:<26}{'gagal':>16}")
        else:
            print(f"{nama:<26}{h['akar']:>16.10f}{h['iter']:>9}{h['fx']:>14.3e}{h['waktu']:>11.3f}"
                  + ("" if h["konv"] else "  (tdk konvergen)"))

    b, n = hasil["Biseksi (tertutup)"], hasil["Newton-Raphson (terbuka)"]
    print("\nANALISIS:")
    if b and n:
        print(f"- Selisih kedua akar        : {abs(b['akar'] - n['akar']):.3e}")
        if n["iter"] < b["iter"]:
            print(f"- Kecepatan                 : Newton-Raphson lebih cepat ({n['iter']} vs {b['iter']} iterasi), karena konvergensi kuadratik; biseksi hanya linier (galat dibagi 2 tiap iterasi).")
        elif n["iter"] > b["iter"]:
            print(f"- Kecepatan                 : Biseksi lebih sedikit iterasi ({b['iter']} vs {n['iter']}). Tebakan awal Newton kemungkinan jauh dari akar atau akar berulang.")
        else:
            print("- Kecepatan                 : Jumlah iterasi sama.")
        print(f"- Ketelitian |f(akar)|      : {'Newton-Raphson' if n['fx'] < b['fx'] else 'Biseksi'} lebih kecil.")
    elif b and not n:
        print("- Newton-Raphson gagal sedangkan biseksi berhasil: bukti metode terbuka tidak menjamin konvergen, sedangkan metode tertutup selalu konvergen selama akar terkurung.")
    elif n and not b:
        print("- Biseksi gagal (akar tidak terkurung / tanda sama), Newton-Raphson tetap bisa jalan dari tebakan awal.")
    print("- Biseksi pasti konvergen tetapi lambat & butuh interval berbeda tanda. Newton-Raphson cepat, hanya butuh 1 tebakan awal, tetapi bisa divergen/macet bila f'(x) ~ 0 atau tebakan awal buruk.")


def baca_float(prompt, default=None):
    while True:
        s = input(prompt).strip()
        if not s and default is not None:
            return default
        try:
            return float(eval(s, {"__builtins__": {}}, SAFE))
        except Exception:
            print("  Input tidak valid, coba lagi.")


def main():
    print("PROGRAM AKAR PERSAMAAN: Biseksi vs Newton-Raphson")
    while True:
        while True:
            teks = input("\nMasukkan f(x) (contoh: x^3 - 2*x - 5): ")
            try:
                f = buat_fungsi(teks)
                f(1.0)
                break
            except Exception as err:
                print(f"  Fungsi tidak valid ({err}). Gunakan variabel x.")
        a = baca_float("Batas bawah a (biseksi): ")
        b = baca_float("Batas atas  b (biseksi): ")
        x0 = baca_float("Tebakan awal x0 (Newton) [Enter = titik tengah a,b]: ", default=(a + b) / 2)
        tol = baca_float("Toleransi error (%) [Enter = 1e-6]: ", default=1e-6)
        maks = int(baca_float("Iterasi maksimum [Enter = 100]: ", default=100))
        analisis(jalankan(f, a, b, x0, tol, maks))
        if input("\nCoba persamaan lain? (y/n): ").strip().lower() != "y":
            break


if __name__ == "__main__":
    main()