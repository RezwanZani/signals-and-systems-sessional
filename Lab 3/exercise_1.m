% 1. Define the continuous time approximation
dt = 0.001;          % Very small time step
t = -2:dt:8;         % Time vector covering before and after the signals

% ---> ADDED: Clear command window and print setup information
clc;
fprintf('--- Continuous-Time Convolution Analysis ---\n');
fprintf('Time step (dt) set to: %.3f\n', dt);

% 2. Define the window: [u(t) - u(t-5)]
% This creates an array of 1s between 0 and 5, and 0s elsewhere
window = (t >= 0) & (t <= 5);

% 3. Generate x(t) and h(t)
x = cos(2*pi*t) .* window; 
h = sin(3*pi*t) .* window; 

% ---> ADDED: Print signal status
fprintf('Signals x(t) and h(t) generated successfully for t = [0, 5].\n');
fprintf('Calculating continuous convolution approximation...\n');

% 4. Compute the continuous convolution approximation
y = conv(x, h) * dt; 

% 5. Determine the output time vector
% The output time starts at the sum of the input start times
t_start = t(1) + t(1); 
ty = t_start : dt : t_start + (length(y)-1)*dt;

% ---> ADDED: Print useful analytical outputs from the convolution
fprintf('Convolution complete.\n');
fprintf('--------------------------------------------------\n');
fprintf('Output Time Range          : [%.2f, %.2f] seconds\n', ty(1), ty(end));
fprintf('Maximum Output Amplitude   : %.4f\n', max(y));
fprintf('Minimum Output Amplitude   : %.4f\n', min(y));
fprintf('Output Vector Length       : %d samples\n', length(y));
fprintf('--------------------------------------------------\n');
fprintf('Generating plot...\n\n');

% 6. Visualize the continuous signals
figure('Name', 'Continuous-Time Convolution');
subplot(3, 1, 1);
plot(t, x, 'LineWidth', 1.5);
title('Input Signal x(t)');
xlabel('Time t'); ylabel('Amplitude');
grid on;

subplot(3, 1, 2);
plot(t, h, 'LineWidth', 1.5, 'Color', 'r');
title('System Impulse Response h(t)');
xlabel('Time t'); ylabel('Amplitude');
grid on;

subplot(3, 1, 3);
plot(ty, y, 'LineWidth', 1.5, 'Color', 'g');
title('Output System Response y(t)');
xlabel('Time t'); ylabel('Amplitude');
xlim([-2 12]); % Focus the view on the relevant time frame
grid on;