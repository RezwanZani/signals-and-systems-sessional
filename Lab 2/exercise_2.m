% EXERCISE 02: Dynamic Discrete-Time System Analyzer
clc; clear; close all;

%% 1. Setup & System Definition
N = 50;           % Number of samples
n = 0:N-1;        % Discrete time index
tol = 1e-9;       % Error tolerance

% Define the Discrete System Equation HERE. 
% Currently set to First-Difference: y[n] = x[n] - x[n-1]
sys = @(x) [x(1), diff(x)]; 

fprintf('--- EXERCISE 2: DISCRETE-TIME SYSTEM ANALYSIS ---\n\n');

rng(42);
x1 = randn(1, N);
x2 = randn(1, N);

%% (a) Linearity Test
a = 0.5; b = -1.5;
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
xA(1:n0) = sin(2*pi*5*(1:n0)/N);
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

%% (d) Shift-Invariance Test
k_shift = 5; 
y_original = sys(x1);

% Shift input then apply system
x1_shifted = [zeros(1, k_shift), x1(1:end-k_shift)];
y_from_shifted_input = sys(x1_shifted);

% Apply system then shift output
y_shifted_output = [zeros(1, k_shift), y_original(1:end-k_shift)];

shift_error = max(abs(y_from_shifted_input - y_shifted_output));

fprintf('(d) Shift Invariance: ');
if shift_error < tol
    fprintf('SHIFT INVARIANT (Error: %e)\n\n', shift_error);
else
    fprintf('SHIFT VARIANT (Error: %e)\n\n', shift_error);
end

%% Plotting Logic
figure('Name', 'Discrete System Logic Analysis');
subplot(2,1,1);
stem(n, x1, 'k', 'filled', 'DisplayName', 'Input x[n]'); hold on;
stem(n, sys(x1), 'r', 'DisplayName', 'Output y[n]');
grid on; xlabel('Sample n'); ylabel('Amplitude'); title('Discrete System Response'); legend;

subplot(2,1,2);
stem(n, y_from_shifted_input, 'b', 'filled', 'DisplayName', 'System applied to shifted input'); hold on;
stem(n, y_shifted_output, 'rX', 'MarkerSize', 8, 'DisplayName', 'Shift applied to system output');
grid on; xlabel('Sample n'); ylabel('Amplitude'); title('Shift Invariance Check (Visual Overlap)'); legend;