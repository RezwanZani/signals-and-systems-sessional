% EXERCISE 01: Dynamic Continuous-Time System Analyzer
clc; clear; close all;

%% 1. Setup & System Definition
fs = 1000;          % Sampling frequency
dt = 1/fs;          % Time step
t = 0:dt:2;         % Time vector from 0 to 2 seconds
N = length(t);      % Number of samples
tol = 1e-6;         % Error tolerance for floating-point math

% Define the System Equation HERE. 
% Currently set to Differentiator: y(t) = dx(t)/dt
sys = @(x) [0, diff(x)/dt]; 

fprintf('--- EXERCISE 1: CONTINUOUS-TIME SYSTEM ANALYSIS ---\n\n');

%% (a) Linearity Test
x1 = sin(2*pi*2*t);
x2 = sin(2*pi*5*t);
a = 2; b = 3;

% Test superposition: sys(a*x1 + b*x2) == a*sys(x1) + b*sys(x2)
y_combo = sys(a*x1 + b*x2);
y_sum = a*sys(x1) + b*sys(x2);
linear_error = max(abs(y_combo - y_sum));

fprintf('(a) Linearity: ');
if linear_error < tol
    fprintf('LINEAR (Error: %e)\n', linear_error);
else
    fprintf('NONLINEAR (Error: %e)\n', linear_error);
end

%% (b) Causality Test
n0 = round(N/2);
xA = zeros(1,N); xB = zeros(1,N);
% Identical past
xA(1:n0) = sin(2*pi*3*t(1:n0));
xB(1:n0) = xA(1:n0);
% Different future
xA(n0+1:end) = 0;
xB(n0+1:end) = randn(1, N-n0);

yA = sys(xA); yB = sys(xB);
causal_error = max(abs(yA(1:n0) - yB(1:n0)));

fprintf('(b) Causality: ');
if causal_error < tol
    fprintf('CAUSAL (Output matched in identical past)\n');
else
    fprintf('NON-CAUSAL (Future input affected past output)\n');
end

%% (c) Static or Dynamic (Memory Test)
k = round(N/2);
xc1 = zeros(1,N); xc2 = zeros(1,N);
% Same current input, different previous input
xc1(k) = 0; xc2(k) = 0;
xc1(k-1) = 0; xc2(k-1) = 1;

yc1 = sys(xc1); yc2 = sys(xc2);
memory_diff = abs(yc1(k) - yc2(k));

fprintf('(c) Memory: ');
if memory_diff > tol
    fprintf('DYNAMIC / HAS MEMORY (Output changed based on past input)\n');
else
    fprintf('STATIC / MEMORYLESS\n');
end

%% (d) Time-Invariance Test
xTI = randn(1,N); xTI(1) = 0;
k_shift = 150;

y_original = sys(xTI);
% Shift input, then apply system
x_shifted = [zeros(1, k_shift), xTI(1:end-k_shift)];
y_from_shifted_input = sys(x_shifted);
% Apply system, then shift output
y_shifted_output = [zeros(1, k_shift), y_original(1:end-k_shift)];

ti_error = max(abs(y_from_shifted_input - y_shifted_output));

fprintf('(d) Time Invariance: ');
if ti_error < tol
    fprintf('TIME INVARIANT\n');
else
    fprintf('TIME VARIANT\n');
end

%% (e) Stability Test (BIBO)
% Bounded step input
u_step = double(t >= 0.5); 
y_step = sys(u_step);
% If max output is massively larger than max input (e.g. 50x), it's unstable
stability_ratio = max(abs(y_step)) / max(abs(u_step));

fprintf('(e) Stability: ');
if stability_ratio > 50 
    fprintf('UNSTABLE (Bounded input caused unbounded/massive output spike)\n');
else
    fprintf('STABLE (Output remained strictly bounded)\n');
end

%% (f) Invertibility Test
% Check if two different inputs yield the same output (many-to-one mapping)
x_inv1 = sin(2*pi*2*t);
x_inv2 = x_inv1 + 5; % Shifted by a constant

y_inv1 = sys(x_inv1);
y_inv2 = sys(x_inv2);
inv_output_diff = max(abs(y_inv1 - y_inv2));
inv_input_diff = max(abs(x_inv1 - x_inv2));

fprintf('(f) Invertibility: ');
if inv_output_diff < tol && inv_input_diff > tol
    fprintf('NOT INVERTIBLE (Different inputs produced identical outputs)\n\n');
else
    fprintf('INVERTIBLE (One-to-one mapping detected for test case)\n\n');
end

%% Plotting Logic (Input vs Output & Stability Proof)
figure('Name', 'Continuous System Logic Analysis');
subplot(2,1,1);
plot(t, x1, 'k', 'DisplayName', 'Input x(t)'); hold on;
plot(t, sys(x1), 'r--', 'LineWidth', 1.5, 'DisplayName', 'System Output y(t)');
grid on; xlabel('Time (s)'); ylabel('Amplitude'); title('System Response to Sine Wave'); legend;

subplot(2,1,2);
plot(t, u_step, 'k', 'DisplayName', 'Bounded Step Input'); hold on;
plot(t, y_step, 'r', 'DisplayName', 'System Output');
grid on; xlabel('Time (s)'); ylabel('Amplitude'); title('BIBO Stability Test'); legend;