clc;
clear;
close all;

%% Define time axis
t = linspace(-2, 10, 5000);

%% Define unit step function
u = @(t) double(t >= 0);

%% Define the signal x(t)
x = t .* (u(t) - u(t-8));

%% Plot the signal
figure;
plot(t, x, 'LineWidth', 1.5);
grid on;
xlabel('Time t');
ylabel('x(t)');
title('Signal x(t)=t[u(t)-u(t-8)]');

%% Calculate Energy
energy_density = abs(x).^2;
E = trapz(t, energy_density);
fprintf('Energy E = %.2f\n', E);

%% Calculate Average Power
T = 1000; % Large time interval
t_power = linspace(-T, T, 100000);
x_power = t_power .* (u(t_power) - u(t_power-8));
P = (1/(2*T)) * trapz(t_power, abs(x_power).^2);
fprintf('Average Power P = %.6f\n', P);

%% Classification
if E > 0 && isfinite(E)
    fprintf('Classification: ENERGY SIGNAL\n');
elseif P > 0 && isfinite(P)
    fprintf('Classification: POWER SIGNAL\n');
else
    fprintf('Classification: Neither Energy nor Power Signal\n');
end