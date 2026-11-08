clc;
clear;
close all;

%% Time axis
t = linspace(-5, 10, 3001); % Time interval -5 <= t <= 10

%% Basic signals
u = @(x) double(x >= 0); % Unit step function
r = @(x) x .* u(x);      % Unit ramp function

% (a) u(t)
xa = u(t);

% (b) u(t+3)
xb = u(t+3);

% (c) u(t-2) - u(t+3)
xc = u(t-2) - u(t+3);

% (d) e^{-t}u(t+2)
xd = exp(-t) .* u(t+2);

%% Impulse signals
% (e) delta(t)
delta1_time = 0;

% (f) delta(t-2)
delta2_time = 2;

% (g) delta(t-1) + delta(t+2)
delta_sum_time = [-2 1];

% (h) r(t)
xh = r(t);

% (i) r(t-1)
xi = r(t-1);

% (j) r(t) - r(t-2) - r(t-5) + r(t-7)
xj = r(t) - r(t-2) - r(t-5) + r(t-7);

%% (k) p4(t) = sum delta(t-4k)
k4 = ceil(-5/4) : floor(10/4);
p4_time = 4 * k4;

%% (l) p2(t-1) = sum delta(t-1-2k)
k2 = ceil((-5-1)/2) : floor((10-1)/2);
p2_time = 1 + 2 * k2;

%% Plot all signals (Example of plotting a few subplots)
figure('Color', 'w');
subplot(4, 3, 1)
plot(t, xa, 'LineWidth', 1.5)
grid on
title('(a) u(t)')
xlabel('t')
ylabel('Amplitude')

% Note: Proceed with subplot(4,3,2) up to subplot(4,3,12) for the remaining signals using 'plot' for continuous and 'stem' for impulses.