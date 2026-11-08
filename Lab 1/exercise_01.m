%% Continuous-time signal x1(t) = cos(pi*t)
t = linspace(-2, 2, 500); % time from -2 to 2
x1 = cos(pi*t);
figure;
plot(t, x1, 'b', 'LineWidth', 1.5);
grid on;
xlabel('t'); ylabel('x1(t)');
title('Continuous-time signal x1(t) = cos(\pi t)');

%% Discrete-time signal x2[n] = cos(pi*n)
n = -10:10; % discrete time indices
x2 = cos(pi*n);
figure;
stem(n, x2, 'r', 'filled'); % stem plot for discrete signals
grid on;
xlabel('n'); ylabel('x2[n]');
title('Discrete-time signal x2[n] = cos(\pi n)');

%% Real and Imag part of x(t) = e^{j 3\pi t}
T = 2/3; % fundamental period
t2 = linspace(0, 2*T, 500); % two periods (0 to 4/3)
x = exp(1j*3*pi*t2);

figure;
plot(t2, real(x), 'b', 'LineWidth', 1.5); hold on;
plot(t2, imag(x), '--', 'LineWidth', 1.5);
grid on;
xlabel('t'); ylabel('Value');
title('Real and Imag parts of x(t) = e^{j 3\pi t}');
legend('Re\{x(t)\} = cos(3\pi t)', 'Im\{x(t)\} = sin(3\pi t)');