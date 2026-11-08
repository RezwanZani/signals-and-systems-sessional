clc; clear; close all;

fprintf('--- Discrete-Time System Response Analysis ---\n\n');

% 1. Extract System Coefficients
% For y[n] + 0.1y[n-1] - y[n-2] = x[n] + 2x[n-1]
b = [1, 2];          % Numerator (x coefficients)
a = [1, 0.1, -1];    % Denominator (y coefficients)

% ---> ADDED: Print extracted system properties
fprintf('System Coefficients Extracted:\n');
fprintf('Numerator (b)   : [%s]\n', num2str(b));
fprintf('Denominator (a) : [%s]\n\n', num2str(a));

% --- Part A & B: Impulse and Step Responses ---
N1 = 0:30; % Time index 0 to 30

% Generate Inputs
delta = [1, zeros(1, length(N1)-1)]; % Impulse input
u = ones(1, length(N1));             % Step input

fprintf('Calculating Impulse and Step Responses (n = %d to %d)...\n', N1(1), N1(end));

% Calculate Outputs using filter
h = filter(b, a, delta); % Part A: Impulse response
r = filter(b, a, u);     % Part B: Step response

% ---> ADDED: Print analytical outputs for Impulse and Step responses
fprintf('Impulse Response (h[n]) - Max: %.4f, Min: %.4f\n', max(h), min(h));
fprintf('Step Response (r[n])    - Max: %.4f, Min: %.4f\n\n', max(r), min(r));

% --- Part C: Response to custom signal ---
N2 = 0:50; % Time index 0 to 50

% Generate Input (Element-wise operations are required)
x = (0.8 .^ N2) .* cos(N2); % Custom input x[n]

fprintf('Calculating Custom Signal Response (n = %d to %d)...\n', N2(1), N2(end));

% Calculate Output
y = filter(b, a, x); % Part C output

% ---> ADDED: Print analytical outputs for Custom Response
fprintf('Custom Response (y[n])  - Max: %.4f, Min: %.4f\n', max(y), min(y));
fprintf('--------------------------------------------------\n');
fprintf('Generating plots...\n\n');

% --- Plotting Results ---
% ---> MODIFIED: Added a descriptive window name
figure('Color', 'w', 'Name', 'Discrete-Time System Responses');

% Plot A: Impulse Response
subplot(3, 1, 1);
stem(N1, h, 'filled'); grid on;
title('Impulse Response h[n]'); xlabel('n'); ylabel('Amplitude');

% Plot B: Step Response
subplot(3, 1, 2);
stem(N1, r, 'filled'); grid on;
title('Step Response r[n]'); xlabel('n'); ylabel('Amplitude');

% Plot C: Custom Response
subplot(3, 1, 3);
stem(N2, y, 'filled'); grid on;
title('Output y[n] for x[n] = 0.8^n cos(n)'); xlabel('n'); ylabel('Amplitude');