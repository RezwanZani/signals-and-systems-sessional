clc;
clear;
close all;

%% Part 1: Frequency Response H(w)
% Define frequency range
w = linspace(-pi, pi, 2000);

% Define system frequency response
H = (4 + 2*exp(-1j*2*w)) ./ (3 + 5*exp(-1j*w));

% Plot Magnitude and Phase Response
figure(1);

subplot(2,1,1);
plot(w, abs(H), 'b', 'LineWidth', 1.5);
grid on;
xlabel('Frequency (rad/sample)');
ylabel('|H(w)|');
title('Magnitude Response');

subplot(2,1,2);
plot(w, unwrap(angle(H)), 'r', 'LineWidth', 1.5);
grid on;
xlabel('Frequency (rad/sample)');
ylabel('Phase (radians)');
title('Phase Response');


%% Part 2: System Response to Input x[n]
% Time index and input signal parameters
n = 0:40;
x = 2 * cos(4*n + pi/6);
w0 = 4;

% System response at frequency w0 = 4
H0 = (4 + 2*exp(-1j*2*w0)) / (3 + 5*exp(-1j*w0));

% Output magnitude and phase
A = 2 * abs(H0);
phi = pi/6 + angle(H0);

% Compute output signal y[n]
y = A * cos(w0*n + phi);

% Display numerical results
fprintf('H(4) = %.6f + %.6fj\n', real(H0), imag(H0));
fprintf('Magnitude of H(4) = %.6f\n', abs(H0));
fprintf('Phase of H(4) = %.6f radians\n', angle(H0));
fprintf('Output amplitude = %.6f\n', A);
fprintf('Output phase = %.6f radians\n', phi);

% Plot Input and Output signals
figure(2);

subplot(2,1,1);
stem(n, x, 'filled', 'b');
grid on;
xlabel('n');
ylabel('x[n]');
title('Input Signal x[n]');

subplot(2,1,2);
stem(n, y, 'filled', 'r');
grid on;
xlabel('n');
ylabel('y[n]');
title('Output Signal y[n]');
