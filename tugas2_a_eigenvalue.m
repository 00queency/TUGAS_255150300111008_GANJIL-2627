%% TUGAS 2 SISTEM LINEAR - BAGIAN (a)iii
% Eigenvalue matriks A dan analisis kestabilan titik setimbang [0; 0]
clear; clc; close all;

% Matriks hasil linearisasi (dari hitungan tangan bagian a-ii)
A = [  0   1;
     -10  -2];
B = [0; 1];

% Hitung eigenvalue
lambda = eig(A);

disp('Matriks A =');
disp(A);
disp('Eigenvalue (lambda) =');
disp(lambda);

% Cek kestabilan: semua bagian real harus negatif
if all(real(lambda) < 0)
    disp('KESIMPULAN: Semua Re(lambda) < 0 -> stabil asimtotik (lokal).');
elseif any(real(lambda) > 0)
    disp('KESIMPULAN: Ada Re(lambda) > 0 -> tidak stabil.');
else
    disp('KESIMPULAN: Ada Re(lambda) = 0 -> marginal, perlu analisis lanjut.');
end

% Info tambahan (opsional, untuk analisis)
wn   = sqrt(10);        % frekuensi natural (rad/s)
zeta = 2/(2*wn);        % rasio redaman
fprintf('wn = %.4f rad/s, zeta = %.4f (underdamped karena zeta < 1)\n', wn, zeta);

% Cek karakteristik polinomial (harus sama dengan hitungan tangan)
disp('Polinomial karakteristik poly(A) = [1 2 10] -> lambda^2 + 2*lambda + 10');
disp(poly(A));
