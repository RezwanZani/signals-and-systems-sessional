clc;
clear;
close all;

%% Time axis
t = linspace(-6, 6, 2000);

%% Original signal x(t) = t cos(t)
x = t .* cos(t);

%% Calculate x(-t)
x_neg = (-t) .* cos(-t);

%% Even and Odd decomposition
xe = 0.5 * (x + x_neg); % Even part
xo = 0.5 * (x - x_neg); % Odd part

%% Verification
fprintf('Maximum value of even part = %.2e\n', max(abs(xe)));
fprintf('Maximum difference between x(t) and odd part = %.2e\n', max(abs(x-xo)));

%% Plotting
figure;
plot(t, x, 'k', 'LineWidth', 1.5);
hold on;
plot(t, xe, 'r--', 'LineWidth', 1.5);
plot(t, xo, 'b-.', 'LineWidth', 1.5);
grid on;
xlabel('t');
ylabel('Amplitude');
title('Even/Odd decomposition of x(t)=t cos(t)');
legend('x(t)=t cos(t)', 'Even part x_e(t)', 'Odd part x_o(t)');