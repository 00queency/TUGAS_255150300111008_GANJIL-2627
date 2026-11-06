import numpy as np
import matplotlib.pyplot as plt

f = lambda x: x**10 - 1
a0, b0, Es = 0.9, 1.2, 0.1

def biseksi(a, b, Es):
    cp, Er, n, rows = a, 100, 0, []
    while abs(Er) > Es:
        c = (a + b) / 2
        if n > 0: Er = abs((c - cp) / c * 100)
        rows.append((a, b, c, Er)); cp = c; n += 1
        if f(a) * f(c) < 0: b = c
        else: a = c
    return rows

def false_position(a, b, Es):
    cp, Er, n, rows = a, 100, 0, []
    while abs(Er) > Es:
        c = b - f(b) * (a - b) / (f(a) - f(b))
        if n > 0: Er = abs((c - cp) / c * 100)
        rows.append((a, b, c, Er)); cp = c; n += 1
        if f(a) * f(c) < 0: b = c
        else: a = c
    return rows

rb = biseksi(a0, b0, Es)
rf = false_position(a0, b0, Es)

x = np.linspace(0.9, 1.2, 300)
fig, ax = plt.subplots(1, 3, figsize=(17, 5))

# false-position: garis lurus tiap iterasi
ax[0].plot(x, f(x), 'b-', label='f(x)')
ax[0].axhline(0, color='r')
warna = plt.cm.viridis(np.linspace(0, 0.9, 4))
for i in range(4):
    a, b, c, _ = rf[i]
    ax[0].plot([a, b], [f(a), f(b)], '--', color=warna[i], label=f'iterasi {i}')
    ax[0].plot(c, 0, 'o', color=warna[i])
ax[0].axvline(1, color='g', ls=':', label='akar x=1')
ax[0].set_title('False-position: b tetap di 1.2,\nc merayap dari kiri')
ax[0].set_xlabel('x'); ax[0].set_ylabel('f(x)'); ax[0].grid(True); ax[0].legend(fontsize=8)

# biseksi: selang yang terus dibelah dua
ax[1].plot(x, f(x), 'b-')
ax[1].axhline(0, color='r')
for i in range(5):
    a, b, c, _ = rb[i]
    ax[1].hlines(-1.2 - 0.35 * i, a, b, color='orange', lw=3)
    ax[1].plot(c, -1.2 - 0.35 * i, 'ko')
ax[1].axvline(1, color='g', ls=':')
ax[1].set_title('Biseksi: selang dibelah dua\ntiap iterasi (iterasi 0-4)')
ax[1].set_xlabel('x'); ax[1].set_ylabel('f(x) / selang'); ax[1].grid(True)

# konvergensi galat relatif
ax[2].semilogy(range(1, len(rb)), [r[3] for r in rb[1:]], 'o-', label='Biseksi')
ax[2].semilogy(range(1, len(rf)), [r[3] for r in rf[1:]], 's-', label='False-position')
ax[2].axhline(Es, color='r', ls='--', label='Es = 0.1%')
ax[2].set_title(f'Galat relatif per iterasi\n(biseksi {len(rb)} iter, false-position {len(rf)} iter)')
ax[2].set_xlabel('iterasi'); ax[2].set_ylabel('Er (%)'); ax[2].grid(True, which='both'); ax[2].legend()

plt.tight_layout()
plt.show()