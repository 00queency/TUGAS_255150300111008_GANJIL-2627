%% TUGAS 2 SISTEM LINEAR - BAGIAN (b) dan (c)i
% Simulasi theta(t): model non-linear vs linear (ode45) + error maksimum
clear; clc; close all;

%% 1. Parameter dan model
A = [  0   1;
     -10  -2];

% Model non-linear: x1' = x2 ; x2' = -2*x2 - 10*sin(x1)   (u = 0)
f_nl  = @(t, x) [ x(2);
                 -2*x(2) - 10*sin(x(1)) ];

% Model linear: x' = A*x   (u = 0)
f_lin = @(t, x) A*x;

%% 2. Pengaturan simulasi
t_end = 10;                          % lama simulasi (detik)
t     = linspace(0, t_end, 2001);    % grid waktu yang sama untuk kedua model
opts  = odeset('RelTol', 1e-8, 'AbsTol', 1e-10);

% Dua skenario kondisi awal [theta0; omega0]
x0_set = [0.1, 0;      % skenario 1: perpindahan kecil
          1.5, 0];     % skenario 2: perpindahan besar
judul  = {'Skenario 1: \theta(0) = 0.1 rad (kecil)', ...
          'Skenario 2: \theta(0) = 1.5 rad (besar)'};

e_max = zeros(2, 1);

%% 3. Simulasi tiap skenario
figure('Name', 'Perbandingan theta(t)', 'Position', [100 100 900 700]);

for k = 1:2
    x0 = x0_set(k, :)';

    % Simulasi non-linear dan linear dengan ode45
    [~, X_nl]  = ode45(f_nl,  t, x0, opts);
    [~, X_lin] = ode45(f_lin, t, x0, opts);

    theta_nl  = X_nl(:, 1);
    theta_lin = X_lin(:, 1);

    % (c)i  Error maksimum
    err      = abs(theta_nl - theta_lin);
    e_max(k) = max(err);
    [~, idx] = max(err);

    fprintf('%s\n', erase(judul{k}, '\'));
    fprintf('   e_max = %.6f rad (terjadi di t = %.3f s)\n\n', e_max(k), t(idx));

    % Plot theta(t)
    subplot(2, 2, k);
    plot(t, theta_nl,  'b-',  'LineWidth', 1.8); hold on;
    plot(t, theta_lin, 'r--', 'LineWidth', 1.8);
    grid on; xlabel('t (s)'); ylabel('\theta (rad)');
    title(judul{k});
    legend('Non-linear', 'Linear', 'Location', 'best');

    % Plot error |theta_nl - theta_lin|
    subplot(2, 2, k + 2);
    plot(t, err, 'k-', 'LineWidth', 1.5); hold on;
    plot(t(idx), e_max(k), 'ro', 'MarkerFaceColor', 'r');
    grid on; xlabel('t (s)'); ylabel('|error| (rad)');
    title(sprintf('Error absolut (e_{max} = %.4f rad)', e_max(k)));
end

%% 4. Ringkasan untuk laporan
fprintf('==== RINGKASAN ====\n');
fprintf('theta0 = 0.1 rad -> e_max = %.6f rad\n', e_max(1));
fprintf('theta0 = 1.5 rad -> e_max = %.6f rad\n', e_max(2));
fprintf('Rasio e_max (besar/kecil) = %.1f kali\n', e_max(2) / e_max(1));
