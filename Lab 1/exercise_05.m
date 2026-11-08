clc;
clear;
close all;

%% Define unit step function
u = @(t) double(t >= 0);

%% Define original signal
% x(t) = t[u(t) - u(t-5)]
x = @(t) t .* (u(t) - u(t-5));

%% Time axis
t = linspace(-8, 10, 5000);

%% Generate transformed signals
xa = x(-t);         % (a) Time reversal
xb = x(4*t);        % (b) Compression by 4
xc = x(0.3*t);      % (c) Expansion by 1/0.3
xd = x(t+2);        % (d) Shift left by 2
xe = x(t-3);        % (e) Shift right by 3
xf = x(1-3*t);      % (f) Reflection + compression + shift

%% Plot all signals
figure('Color', 'w');

% Plot (a)
subplot(3, 2, 1)
plot(t, xa, 'LineWidth', 1.5);
grid on;
xlabel('t'); ylabel('x(-t)');
title('(a) x(-t)');

% Plot (b)
subplot(3, 2, 2)
plot(t, xb, 'LineWidth', 1.5);
grid on;
xlabel('t'); ylabel('x(4t)');
title('(b) x(4t)');

% Plot (c)
subplot(3, 2, 3)
plot(t, xc, 'LineWidth', 1.5);
grid on;
xlabel('t'); ylabel('x(0.3t)');
title('(c) x(0.3t)');

% Plot (d)
subplot(3, 2, 4)
plot(t, xd, 'LineWidth', 1.5);
grid on;
xlabel('t'); ylabel('x(t+2)');
title('(d) x(t+2)');

% Plot (e)
subplot(3, 2, 5)
plot(t, xe, 'LineWidth', 1.5);
grid on;
xlabel('t'); ylabel('x(t-3)');
title('(e) x(t-3)');

% Plot (f)
subplot(3, 2, 6)
plot(t, xf, 'LineWidth', 1.5);
grid on;
xlabel('t'); ylabel('x(1-3t)');
title('(f) x(1-3t)');

sgtitle('Time Transformations of x(t)=t[u(t)-u(t-5)]');