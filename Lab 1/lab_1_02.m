%% 1. Time Vector Setup
% linspace(start, end, n) generates an array of 'n' evenly spaced points.
% We use 3001 points to ensure t=0 is exactly computed (since 10 - (-5) = 15, 
% 15 * 200 = 3000 intervals, meaning 3001 points hits every 0.005 step precisely).
t = linspace(-5, 10, 3001); 

%% 2. Fundamental Anonymous Functions (Lambda Functions)
% @(x) creates an "anonymous function" (a quick, one-line function).
% (x >= 0) creates a logical array of 1s (true) and 0s (false).
% double() converts these logical values into standard numeric values so we can do math with them.
% This mathematically represents the Unit Step Function: u(t) = 1 for t >= 0, and 0 otherwise.
u = @(x) double(x >= 0);    

% r(t) is the Unit Ramp Function.
% '.*' is crucial here: it means "element-wise multiplication". 
% It multiplies each element of array 'x' by the corresponding element of 'u(x)'.
r = @(x) x .* u(x);         

%% 3. Generating Continuous Signals
xa = u(t);                             % (a) Unit step: u(t)
xb = u(t+3);                           % (b) u(t) shifted left by 3
xc = u(t-2) - u(t+3);                  % (c) Rectangular pulse from t=-3 to t=2

% exp(-t) is e^(-t). We must use '.*' because we are multiplying two arrays 
% (the exponential decay curve and the shifted unit step) point-by-point.
xd = exp(-t) .* u(t+2);                % (d) Decaying exponential starting at t=-2

xh = r(t);                             % (h) Unit ramp: r(t)
xi = r(t-1);                           % (i) Ramp shifted right by 1

% (j) A combination of ramps that forms a custom piecewise shape.
xj = r(t) - r(t-2) - r(t-5) + r(t-7);  

%% 4. Defining Discrete Impulse Locations
% MATLAB cannot plot a true continuous Dirac delta function (which is infinitely high and infinitesimally narrow).
% Instead, we define the exact time instants where the impulses occur so we can plot them as distinct "stems".
delta1_time = 0;                       % (e) Impulse at t=0
delta2_time = 2;                       % (f) Impulse at t=2
delta_sum_time = [-2, 1];              % (g) Two impulses, located at t=-2 and t=1

%% 5. Generating Impulse Trains
% (k) p_4(t) represents an impulse train with period 4.
% We need to find all integer multiples of 4 within our interval [-5, 10].
% ceil() rounds towards positive infinity. floor() rounds towards negative infinity.
% The colon operator ':' creates an integer sequence between these bounds.
k4 = ceil(-5/4) : floor(10/4);         % Finds k = [-1, 0, 1, 2]
p4_time = 4 * k4;                      % Locations: [-4, 0, 4, 8]

% (l) p_2(t-1) represents an impulse train with period 2, shifted right by 1.
k2 = ceil((-5-1)/2) : floor((10-1)/2); % Adjusts bounds for the shift and period
p2_time = 1 + 2 * k2;                  % Calculates exact time locations

%% 6. Plotting and Visualization
% figure() creates a new window.
% 'Color', 'w' is a Name-Value pair that sets the background color of the window to white (instead of the default gray).
figure('Color', 'w');

% subplot(rows, columns, position) divides the figure into a 4x3 grid.
% Position 1 is the top-left corner.
subplot(4,3,1);
plot(t, xa, 'LineWidth', 1.5);
grid on;
xlabel('t');
ylabel('Amplitude');

subplot(4,3,2) 
plot(t,xb,'LineWidth',1.5) 
grid on 
title('(b) u(t+3)') 
xlabel('t') 

subplot(4,3,3) 
plot(t,xc,'LineWidth',1.5) 
grid on 
title('(c) u(t-2)-u(t+3)') 
xlabel('t') 

subplot(4,3,4) 
plot(t,xd,'LineWidth',1.5) 
grid on 
% '^{-t}' is MATLAB's TeX interpreter rendering the '-t' as a superscript.
title('(d) e^{-t}u(t+2)') 
xlabel('t') 

% --- Impulse Plots (Using stem instead of plot) ---
subplot(4,3,5) 
% stem() draws a vertical line with a marker at the top.
% 'delta1_time' is the x-axis location, '1' is the height of the impulse.
% 'filled' colors in the circle marker.
stem(delta1_time,1,'filled','LineWidth',1.5) 
grid on 
% xlim locks the x-axis limits. Without this, MATLAB would zoom in on the single point at t=0.
xlim([-5 10]) 
% ylim gives the impulse some visual headroom above the marker.
ylim([0 1.5]) 
% '\delta' uses the TeX interpreter to draw the Greek letter δ.
title('(e) \delta(t)') 
xlabel('t') 

subplot(4,3,6) 
stem(delta2_time,1,'filled','LineWidth',1.5) 
grid on 
xlim([-5 10]) 
ylim([0 1.5]) 
title('(f) \delta(t-2)') 
xlabel('t') 

subplot(4,3,7) 
% [1 1] provides an array of heights matching the two locations in 'delta_sum_time'.
stem(delta_sum_time,[1 1],'filled','LineWidth',1.5) 
grid on 
xlim([-5 10]) 
ylim([0 1.5]) 
title('(g) \delta(t-1)+\delta(t+2)') 
xlabel('t') 

% --- Back to Continuous Plots ---
subplot(4,3,8) 
plot(t,xh,'LineWidth',1.5) 
grid on 
title('(h) r(t)') 
xlabel('t') 

subplot(4,3,9) 
plot(t,xi,'LineWidth',1.5) 
grid on 
title('(i) r(t-1)') 
xlabel('t') 

subplot(4,3,10) 
plot(t,xj,'LineWidth',1.5) 
grid on 
title('(j) r(t)-r(t-2)-r(t-5)+r(t-7)') 
xlabel('t') 

% --- Impulse Train Plots ---
subplot(4,3,11) 
% ones() creates an array of 1s. 
% size(p4_time) ensures this array of 1s is the exact same length as the number of impulses.
stem(p4_time,ones(size(p4_time)),'filled','LineWidth',1.5) 
grid on 
xlim([-5 10]) 
ylim([0 1.5]) 
title('(k) p_4(t)') 
xlabel('t') 

subplot(4,3,12) 
stem(p2_time,ones(size(p2_time)),'filled','LineWidth',1.5) 
grid on 
xlim([-5 10]) 
ylim([0 1.5]) 
title('(l) p_2(t-1)') 
xlabel('t') 

%% Master Title
% sgtitle ("Super Grid Title") centers a single main title above all the subplots.
% '\leq' renders the "less than or equal to" mathematical symbol (≤).
sgtitle('Signals in the interval -5 \leq t \leq 10')