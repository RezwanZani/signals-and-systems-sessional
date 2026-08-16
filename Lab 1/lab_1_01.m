%% Section 1: Continuous-Time Signal
% linspace(start, end, n) generates 'n' linearly spaced points between 'start' and 'end'.
% Here, we create an array of 500 points from -2 to 2 to simulate continuous time.
t = linspace(-2, 2, 500);

% cos() computes the cosine of the input array element-by-element.
% 'pi' is a built-in MATLAB constant representing the mathematical constant π.
x1 = cos(pi*t);

% figure creates a new, blank plotting window. Without it, the next plot 
% would overwrite any existing plot.
figure;

% plot(X, Y) creates a 2D line plot of the data in Y versus the corresponding values in X.
% 'LineWidth', 1.5 is a Name-Value pair that thickens the plot line for better visibility.
plot(t, x1, 'LineWidth', 1.5)

% grid on adds grid lines to the plot background to make reading values easier.
grid on;

% xlabel() and ylabel() add text labels to the x-axis and y-axis.
xlabel('t');
ylabel('x1(t)');

% title() adds a heading to the plot. MATLAB's text interpreter understands 
% basic TeX formatting, so '\pi' will be rendered as the actual Greek letter π.
title('Continuous Time Signal x1(t) = cos(\pi t)');


%% Section 2: Discrete-Time Signal
% The colon operator (start:end) creates an array of integers with a default step of 1.
% This creates a discrete sequence [-10, -9, ..., 9, 10].
n = -10:10;

% Evaluate the cosine function at these discrete integer points.
x2 = cos(pi*n);

figure;

% stem(X, Y) creates a plot with vertical lines terminating in markers (lollipops).
% It is the standard way to visualize discrete/digital signals.
% 'r' makes the stems and markers red.
% "filled" fills the circular markers with solid color instead of leaving them hollow.
stem(n, x2, 'r', "filled")

grid on;
xlabel('n');
ylabel('x2(n)');
title('Discrete Time Signal x2(n) = cos(\pi n)');


%% Section 3: Complex Exponential Signal
% Define the fundamental period of the signal. The frequency is 3*pi, 
% so Omega = 3*pi, and Period T = 2*pi / Omega = 2/3.
T = 2/3;

% Create a time vector that spans exactly two periods (from 0 to 2*T).
t2 = linspace(0, 2*T, 500);

% exp() is the exponential function (e^x). 
% '1j' is the preferred MATLAB syntax for the imaginary unit (√-1). Using '1j' 
% is safer and faster than just 'j' because 'j' might be overwritten as a loop variable.
% This generates the complex signal: e^(j*3*pi*t)
x = exp(1j*3*pi*t2);

figure;

% real(x) extracts the real part of the complex array.
% 'b' specifies a solid blue line.
plot(t2, real(x), 'b', 'LineWidth', 1.5); 

% hold on retains the current plot and axes properties so that subsequent 
% plotting commands add to the existing graph rather than overwriting it.
hold on;

% imag(x) extracts the imaginary part of the complex array.
% 'r--' is a line specification string: 'r' for red, '--' for a dashed line.
plot(t2, imag(x), 'r--', 'LineWidth', 1.5);

grid on;
xlabel('t'); 
ylabel('Value');
title('Real and Imaginary Parts of x(t)');

% legend() creates a box identifying each line plotted. The strings are assigned 
% in the exact order the plots were created (real part first, then imaginary).
% Note: '\{' and '\}' are used to escape the curly braces so they render literally in TeX mode.
legend('Re\{x(t)\} = cos(3\pi t)', 'Im\{x(t)\} = sin(3\pi t)');