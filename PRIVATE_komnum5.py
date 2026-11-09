"""
Program Pencari Akar Persamaan (VERSI BERKOMENTAR)
Metode 1: Biseksi          (metode tertutup / bracketing)
Metode 2: Newton-Raphson   (metode terbuka)

Contoh input fungsi: x^10 - 1 | cos(x) - x | exp(-x) - x | x**3 - 2*x - 5
"""
import math  # pustaka matematika bawaan Python (sin, cos, exp, dll)
import time  # dipakai untuk mengukur lama waktu tiap metode berjalan

# ==========================================================
# BAGIAN 1: Mengubah teks persamaan menjadi fungsi Python
# ==========================================================

# Buat "daftar nama yang boleh dipakai" dari semua fungsi di math (sin, cos, sqrt, ...)
# Syarat "not k.startswith('_')" membuang nama internal yang diawali garis bawah
SAFE = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
# Tambah nama lain: abs = nilai mutlak, ln = log natural, e dan pi = konstanta
SAFE.update({"abs": abs, "ln": math.log, "e": math.e, "pi": math.pi})


def buat_fungsi(teks):  # menerima teks, misal "x^3 - 2*x - 5"
    ekspresi = teks.replace("^", "**")  # Python pakai ** untuk pangkat, jadi ^ diganti
    kode = compile(ekspresi, "<fungsi>", "eval")  # ubah teks jadi kode siap hitung (sekali saja, biar cepat)
    # kembalikan fungsi mini: diberi x, dia menghitung hasil persamaan
    # "__builtins__": {} mematikan fitur Python berbahaya, hanya SAFE yang boleh dipakai
    return lambda x: eval(kode, {"__builtins__": {}}, {**SAFE, "x": x})


def turunan_numerik(f, x, h=1e-6):  # h = jarak kecil untuk menghitung kemiringan
    # kemiringan kurva di titik x = (nilai kanan - nilai kiri) / lebar jarak
    return (f(x + h) - f(x - h)) / (2 * h)


# ==========================================================
# BAGIAN 2: Metode Biseksi (tertutup)
# ==========================================================
def biseksi(f, a, b, tol, maks_iter):
    # Syarat biseksi: f(a) dan f(b) harus beda tanda (artinya ada akar di antaranya)
    if f(a) * f(b) > 0:  # hasil kali positif = tanda sama = tidak ada akar terkurung
        raise ValueError("f(a) dan f(b) harus berbeda tanda (tidak ada akar terkurung).")
    riwayat = []  # daftar untuk mencatat tiap iterasi (buat ditampilkan di tabel)
    c_lama = None  # tebakan sebelumnya, awalnya belum ada
    for i in range(1, maks_iter + 1):  # ulangi dari iterasi 1 sampai batas maksimum
        c = (a + b) / 2  # titik tengah interval = tebakan akar

        # error relatif (%) = seberapa beda tebakan sekarang dari yang lama
        # di iterasi pertama belum ada pembanding, jadi diisi None
        err = abs((c - c_lama) / c) * 100 if c_lama is not None and c != 0 else None

        riwayat.append((i, c, f(c), err))  # note: nomor iterasi, x, f(x), error

        # berhenti kalau: f(c) pas nol, ATAU error sudah kecil, ATAU interval sudah sangat sempit
        if f(c) == 0 or (err is not None and err < tol) or (b - a) / 2 < tol * 1e-4:
            return c, riwayat, True  # True = berhasil konvergen
        
        if f(a) * f(c) < 0:  # akar ada di antara a dan c (tanda beda)
            b = c  # buang tepi kanan (b), batas atas jadi c
        else:  # selain itu akar ada di antara c dan b
            a = c  # buang tepi kiri (a), batas bawah jadi c
            
        c_lama = c  # simpan tebakan ini untuk perbandingan iterasi berikutnya
    return c, riwayat, False  # kalau loop habis tanpa konvergen, False


# ==========================================================
# BAGIAN 3: Metode Newton-Raphson (terbuka)
# ==========================================================
def newton_raphson(f, x0, tol, maks_iter):
    riwayat = []  # catatan tiap iterasi
    x = x0  # mulai dari tebakan awal
    for i in range(1, maks_iter + 1):  # ulangi sampai batas maksimum
        d = turunan_numerik(f, x)  # hitung kemiringan kurva di titik x sekarang
        if abs(d) < 1e-14:  # kemiringan hampir nol = kurva datar
            # rumus Newton membagi dengan d, jadi kalau d ~ 0 hasilnya meledak
            raise ZeroDivisionError(f"f'(x) ~ 0 di x = {x:.6f}; pilih tebakan awal lain.")
        x_baru = x - f(x) / d  # RUMUS NEWTON: geser x mengikuti garis singgung ke sumbu-x
        # error relatif (%) antara tebakan baru dan lama; kalau x_baru = 0 pakai selisih biasa
        err = abs((x_baru - x) / x_baru) * 100 if x_baru != 0 else abs(x_baru - x)
        riwayat.append((i, x_baru, f(x_baru), err))  # catat iterasi ini
        x = x_baru  # tebakan baru jadi titik awal iterasi berikutnya
        if err < tol or f(x) == 0:  # error sudah kecil atau tepat nol
            return x, riwayat, True  # berhasil konvergen
    return x, riwayat, False  # sampai iterasi maksimum belum konvergen


# ==========================================================
# BAGIAN 4: Menampilkan tabel iterasi
# ==========================================================
def cetak_tabel(judul, riwayat, maks_baris=15):  # maks_baris = batas baris yang dicetak
    print(f"\n=== {judul} ===")  # judul tabel
    # judul kolom; ">5" artinya rata kanan dengan lebar 5 karakter, biar kolom lurus
    print(f"{'Iter':>5} {'x':>18} {'f(x)':>16} {'Error (%)':>14}")
    # kalau data sedikit tampilkan semua; kalau banyak: 12 baris awal + penanda None + 2 baris akhir
    tampil = riwayat if len(riwayat) <= maks_baris else riwayat[:maks_baris - 3] + [None] + riwayat[-2:]
    for r in tampil:  # cetak baris demi baris
        if r is None:  # None = penanda "ada baris yang dilewati"
            print(f"{'...':>5}")  # cetak titik-titik
            continue  # lompat ke baris berikutnya
        i, x, fx, err = r  # bongkar isi satu catatan iterasi
        es = "-" if err is None else f"{err:.6e}"  # error kosong ditulis "-", selain itu format ilmiah
        print(f"{i:>5} {x:>18.10f} {fx:>16.6e} {es:>14}")  # cetak satu baris tabel


# ==========================================================
# BAGIAN 5: Menjalankan kedua metode
# ==========================================================
def jalankan(f, a, b, x0, tol, maks_iter):
    hasil = {}  # kamus untuk menyimpan ringkasan hasil tiap metode
    # daftar 2 metode + cara memanggilnya; dibuat loop supaya kode tidak diulang dua kali
    for nama, fungsi in (
        ("Biseksi (tertutup)", lambda: biseksi(f, a, b, tol, maks_iter)),
        ("Newton-Raphson (terbuka)", lambda: newton_raphson(f, x0, tol, maks_iter)),
    ):
        try:  # coba jalankan; kalau error, program tidak langsung crash
            t0 = time.perf_counter()  # catat waktu mulai
            akar, riw, konv = fungsi()  # jalankan metode: dapat akar, riwayat, status konvergen
            waktu = (time.perf_counter() - t0) * 1000  # lama berjalan, diubah ke milidetik
            cetak_tabel(nama, riw)  # tampilkan tabel iterasinya
            # simpan ringkasan: akar, jumlah iterasi, |f(akar)| (makin kecil makin bagus), status, waktu
            hasil[nama] = dict(akar=akar, iter=len(riw), fx=abs(f(akar)), konv=konv, waktu=waktu)
        except (ValueError, ZeroDivisionError, OverflowError) as err:  # error yang mungkin terjadi
            print(f"\n=== {nama} ===\nGAGAL: {err}")  # tampilkan alasan gagal
            hasil[nama] = None  # tandai metode ini gagal
    return hasil  # kembalikan ringkasan kedua metode


# ==========================================================
# BAGIAN 6: Analisis perbandingan
# ==========================================================
def analisis(hasil):
    print("\n" + "=" * 70)  # garis pembatas
    print("PERBANDINGAN HASIL")
    print("=" * 70)
    # judul kolom tabel perbandingan
    print(f"{'Metode':<26}{'Akar':>16}{'Iterasi':>9}{'|f(akar)|':>14}{'Waktu(ms)':>11}")
    for nama, h in hasil.items():  # satu baris per metode
        if h is None:  # metode gagal
            print(f"{nama:<26}{'gagal':>16}")
        else:  # metode berhasil, cetak angka-angkanya
            print(f"{nama:<26}{h['akar']:>16.10f}{h['iter']:>9}{h['fx']:>14.3e}{h['waktu']:>11.3f}"
                  + ("" if h["konv"] else "  (tdk konvergen)"))  # beri catatan kalau tidak konvergen

    b = hasil["Biseksi (tertutup)"]  # ambil hasil biseksi (singkatan b)
    n = hasil["Newton-Raphson (terbuka)"]  # ambil hasil Newton (singkatan n)
    print("\nANALISIS:")
    if b and n:  # KASUS 1: kedua metode berhasil
        print(f"- Selisih kedua akar        : {abs(b['akar'] - n['akar']):.3e}")  # seberapa beda kedua akar
        if n["iter"] < b["iter"]:  # Newton lebih sedikit iterasi
            print(f"- Kecepatan                 : Newton-Raphson lebih cepat ({n['iter']} vs {b['iter']} iterasi), "
                  "karena konvergensi kuadratik; biseksi hanya linier (galat dibagi 2 tiap iterasi).")
        elif n["iter"] > b["iter"]:  # biseksi lebih sedikit iterasi
            print(f"- Kecepatan                 : Biseksi lebih sedikit iterasi ({b['iter']} vs {n['iter']}); "
                  "tebakan awal Newton kemungkinan jauh dari akar atau akar berulang.")
        else:  # jumlah iterasi sama
            print("- Kecepatan                 : Jumlah iterasi sama.")
        # bandingkan ketelitian: yang |f(akar)|-nya lebih kecil = lebih teliti
        print(f"- Ketelitian |f(akar)|      : {'Newton-Raphson' if n['fx'] < b['fx'] else 'Biseksi'} lebih kecil.")
    elif b and not n:  # KASUS 2: biseksi berhasil, Newton gagal
        print("- Newton-Raphson gagal sedangkan biseksi berhasil: bukti metode terbuka tidak menjamin konvergen,\n"
              "  sedangkan metode tertutup selalu konvergen selama akar terkurung.")
    elif n and not b:  # KASUS 3: Newton berhasil, biseksi gagal
        print("- Biseksi gagal (akar tidak terkurung / tanda sama), Newton-Raphson tetap bisa jalan dari tebakan awal.")
    # kesimpulan umum, selalu dicetak
    print("- Umum: biseksi pasti konvergen tetapi lambat & butuh interval berbeda tanda; Newton-Raphson cepat,\n"
          "  hanya butuh 1 tebakan awal, tetapi bisa divergen/macet bila f'(x) ~ 0 atau tebakan awal buruk.")


# ==========================================================
# BAGIAN 7: Membaca input dari pengguna
# ==========================================================
def baca_float(prompt, default=None):  # prompt = teks pertanyaan, default = nilai kalau cuma Enter
    while True:  # ulangi terus sampai input valid
        s = input(prompt).strip()  # baca ketikan, buang spasi di tepi
        if not s and default is not None:  # kalau kosong (Enter saja) dan ada default
            return default  # pakai nilai default
        try:
            # eval supaya bisa mengetik "pi/2" atau "2*e", bukan hanya angka biasa
            return float(eval(s, {"__builtins__": {}}, SAFE))
        except Exception:  # kalau gagal diubah jadi angka
            print("  Input tidak valid, coba lagi.")  # minta ulang


# ==========================================================
# BAGIAN 8: Program utama
# ==========================================================
def main():
    print("PROGRAM AKAR PERSAMAAN: Biseksi vs Newton-Raphson")
    while True:  # loop luar: supaya bisa coba persamaan lain tanpa menjalankan ulang program
        while True:  # loop kecil: minta persamaan sampai valid
            teks = input("\nMasukkan f(x) (contoh: x^3 - 2*x - 5): ")  # baca persamaan
            try:
                f = buat_fungsi(teks)  # ubah teks jadi fungsi
                f(1.0)  # tes: coba hitung di x = 1, kalau salah ketik langsung ketahuan
                break  # lolos tes, keluar dari loop kecil
            except Exception as err:  # kalau error (salah ketik)
                print(f"  Fungsi tidak valid ({err}). Gunakan variabel x.")  # minta ulang
        a = baca_float("Batas bawah a (biseksi): ")  # batas kiri interval
        b = baca_float("Batas atas  b (biseksi): ")  # batas kanan interval
        # tebakan awal Newton; kalau Enter saja, dipakai titik tengah a dan b
        x0 = baca_float("Tebakan awal x0 (Newton) [Enter = titik tengah a,b]: ", default=(a + b) / 2)
        tol = baca_float("Toleransi error (%) [Enter = 1e-6]: ", default=1e-6)  # batas error untuk berhenti
        maks = int(baca_float("Iterasi maksimum [Enter = 100]: ", default=100))  # int = bilangan bulat
        analisis(jalankan(f, a, b, x0, tol, maks))  # jalankan kedua metode, lalu tampilkan perbandingannya
        # tanya mau lanjut atau tidak; selain "y" berarti berhenti
        if input("\nCoba persamaan lain? (y/n): ").strip().lower() != "y":
            break  # keluar dari loop luar, program selesai


# Artinya: kalau file ini dijalankan langsung, panggil main().
# Kalau file ini hanya di-import dari file lain, main() tidak otomatis jalan.
if __name__ == "__main__":
    main()