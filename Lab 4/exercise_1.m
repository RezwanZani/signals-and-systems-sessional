clear;
clc;
close all;

% 1. BASIC INFORMATION
T = 3; % Period
w0 = 2*pi/T; % Fundamental angular frequency

% Total number of complex exponential terms
termCounts = [3 11 51]; 
Klist = (termCounts - 1)/2; 

% Time vector for one period
t = linspace(0,T,6001); 

% 2. ORIGINAL SIGNAL OVER ONE PERIOD
x = zeros(size(t)); 
% 0 <= t < 1
index1 = (t >= 0) & (t < 1); 
x(index1) = t(index1); 
% 1 <= t < 2
index2 = (t >= 1) & (t < 2); 
x(index2) = 1; 
% 2 <= t <= 3
index3 = (t >= 2) & (t <= 3); 
x(index3) = 3 - t(index3); 

% Plot original signal
figure;
plot(t,x, 'k', 'LineWidth',2); 
grid on;
xlabel('Time t');
ylabel('x(t)');
title('Original Signal x(t)');
xlim([0 3]);
ylim([-0.1 1.2]); 

% FOURIER COEFFICIENTS
% Arrays used to save approximations
complexApprox = cell(1, length(termCounts)); 
trigApprox = cell(1, length(termCounts)); 
phaseApprox = cell(1, length(termCounts)); 

% Approximation percentages
PctComplex = zeros(size(termCounts)); 
PctTrig = zeros(size(termCounts)); 
PctPhase = zeros(size(termCounts)); 

% Energy of the original signal
signalEnergy = trapz(t,x.^2); 

%% PART (a): COMPLEX EXPONENTIAL FOURIER SERIES
fprintf('\n');
fprintf(' PART (a): COMPLEX EXPONENTIAL FOURIER SERIES\n'); 

for q = 1:length(termCounts) 
    M = termCounts(q); 
    K = Klist(q); 
    
    % Harmonic indices
    k = -K:K; 
    
    % Calculate C_k
    Ck = zeros(size(k)); 
    % DC coefficient
    Ck(k==0) = 2/3; 
    
    % Nonzero harmonics
    nz = (k~=0); 
    Ck(nz) = 3*(cos(2*pi*k(nz)/3)-1) ./ (2*pi^2*k(nz).^2); 
    
    % Construct Fourier series approximation
    E = exp(1i*(k(:)*w0)*t); 
    x_complex = real(Ck * E); 
    
    % Save result
    complexApprox{q} = x_complex; 
    
    % Approximation percentage
    errorEnergy = trapz(t, (x - x_complex).^2); 
    PctComplex(q) = 100*(1 - errorEnergy/signalEnergy); 
    
    fprintf('%2d terms: %.6f %% approximation\n', M, PctComplex(q)); 
    
    % Plot approximation and coefficients
    figure('Name', sprintf('Complex Fourier Series %d Terms', M)); 
    
    % Approximation
    subplot(3,1,1);
    plot(t,x, 'k', 'LineWidth', 2); 
    hold on;
    plot(t,x_complex, 'r--', 'LineWidth',1.5); 
    grid on;
    xlabel('Time t');
    ylabel('Amplitude');
    title(sprintf('Complex Exponential FS - %d Terms, Approximation = %.6f%%', M, PctComplex(q))); 
    legend('Original x(t)', 'Fourier approximation');
    xlim([0 T]);
    ylim([-0.1 1.2]); 
    
    % Magnitude of C_k
    subplot(3,1,2);
    stem(k, abs(Ck), 'filled'); 
    grid on;
    xlabel('Harmonic index k');
    ylabel('|C_k|');
    title('Magnitude of Complex Fourier Coefficients'); 
    
    % Phase of C_k
    phaseC = angle(Ck); 
    % Phase of zero coefficients is undefined, so set it to zero for plotting
    phaseC(abs(Ck)<1e-12) = 0; 
    subplot(3,1,3);
    stem(k,phaseC, 'filled'); 
    grid on;
    xlabel('Harmonic index k');
    ylabel('\angle C_k (rad)');
    title('Phase of Complex Fourier Coefficients'); 
end

%% PART (b): TRIGONOMETRIC FOURIER SERIES
fprintf('\n');
fprintf(' PART (b): TRIGONOMETRIC FOURIER SERIES\n'); 

for q = 1:length(termCounts) 
    M = termCounts(q); 
    K = Klist(q); 
    
    % Positive harmonics
    n = 1:K; 
    
    % Trigonometric Fourier coefficients
    a0 = 4/3; 
    an = 3*(cos(2*pi*n/3)-1) ./ (pi^2*n.^2); 
    
    % Because the periodic signal is even
    bn = zeros(size(n)); 
    
    % Construct approximation
    theta = (n(:)*w0)*t; 
    x_trig = a0/2 + an*cos(theta) + bn*sin(theta); 
    
    trigApprox{q} = x_trig; 
    
    % Approximation percentage
    errorEnergy = trapz(t, (x - x_trig).^2); 
    PctTrig(q) = 100*(1 - errorEnergy/signalEnergy); 
    
    fprintf('%2d terms: %.6f %% approximation\n', M, PctTrig(q)); 
    
    % Plot
    figure('Name', sprintf('Trigonometric Fourier Series %d Terms', M)); 
    
    % Approximation
    subplot(3,1,1);
    plot(t,x,'k', 'LineWidth',2); 
    hold on;
    plot(t,x_trig, 'b--', 'LineWidth',1.5); 
    grid on;
    xlabel('Time t');
    ylabel('Amplitude');
    title(sprintf('Trigonometric FS - %d Terms, Approximation = %.6f%%', M, PctTrig(q))); 
    legend('Original x(t)', 'Fourier approximation'); 
    xlim([0 T]); 
    ylim([-0.1 1.2]); 
    
    % a_n coefficients
    subplot(3,1,2);
    stem([0 n], [a0 an], 'filled'); 
    grid on;
    xlabel('n');
    ylabel('a_n');
    title('Cosine Coefficients a_n (including a_0)'); 
    
    % bn coefficients
    subplot(3,1,3);
    stem([0 n], [0 bn], 'filled'); 
    grid on;
    xlabel('n');
    ylabel('b_n');
    title('Sine Coefficients b_n'); 
end

%% PART (c): COSINE WITH PHASE FOURIER SERIES
fprintf('\n');
fprintf(' PART (c): COSINE WITH PHASE FOURIER SERIES\n'); 

for q = 1:length(termCounts) 
    M = termCounts(q); 
    K = Klist(q); 
    n = 1:K; 
    
    % Trigonometric coefficients
    a0 = 4/3; 
    an = 3*(cos(2*pi*n/3)-1) ./ (pi^2*n.^2); 
    bn = zeros(size(n)); 
    
    % Convert to magnitude-phase form
    An = sqrt(an.^2 + bn.^2); 
    phi_n = atan2(-bn,an); 
    
    % Phase is undefined if amplitude = 0
    phi_n(An<1e-12) = 0; 
    
    % Construct approximation
    theta = (n(:)*w0)*t; 
    
    % Add one phase to every corresponding harmonic row
    thetaPhase = bsxfun(@plus,theta,phi_n(:)); 
    x_phase = a0/2 + An*cos(thetaPhase); 
    phaseApprox{q} = x_phase; 
    
    % Approximation percentage
    errorEnergy = trapz(t, (x - x_phase).^2); 
    PctPhase(q) = 100*(1 - errorEnergy/signalEnergy); 
    
    fprintf('%2d terms: %.6f %% approximation\n', M, PctPhase(q)); 
    
    % Plot
    figure('Name', sprintf('Cosine Phase Fourier Series %d Terms', M)); 
    
    % Approximation
    subplot(3,1,1);
    plot(t,x, 'k', 'LineWidth', 2); 
    hold on;
    plot(t,x_phase, 'm--', 'LineWidth',1.5); 
    grid on;
    xlabel('Time t');
    ylabel('Amplitude');
    title(sprintf('Cosine-Phase FS - %d Terms, Approximation = %.6f%%', M, PctPhase(q))); 
    legend('Original x(t)', 'Fourier approximation');
    xlim([0 T]);
    ylim([-0.1 1.2]); 
    
    % Amplitude coefficients
    subplot(3,1,2);
    stem(n,An, 'filled'); 
    grid on;
    xlabel('n');
    ylabel('A_n');
    title('Amplitude Coefficients A_n'); 
    
    % Phase coefficients
    subplot(3,1,3);
    stem(n,phi_n, 'filled'); 
    grid on;
    xlabel('n');
    ylabel('\phi_n (rad)');
    title('Phase Coefficients \phi_n'); 
end

%% PART (d) AND PART (e): SUMMARY OF APPROXIMATION PERCENTAGES
fprintf('\n\n');
fprintf(' APPROXIMATION SUMMARY\n'); 
fprintf(' Terms    Trigonometric FS    Cosine-Phase FS    Complex FS\n'); 

for q = 1:length(termCounts) 
    fprintf('%5d      %10.6f %%      %10.6f %%      %10.6f %%\n', termCounts(q), PctTrig(q), PctPhase(q), PctComplex(q)); 
end

% Plot 3, 11 and 51 term approximations together
figure('Name', 'Comparison of 3, 11 and 51 Terms'); 
plot(t,x, 'k', 'LineWidth',2); 
hold on;
plot(t,complexApprox{1}, 'r--', 'LineWidth',1.3); 
plot(t,complexApprox{2},'b-.', 'LineWidth',1.3); 
plot(t,complexApprox{3},'m:', 'LineWidth',1.8); 
grid on;
xlabel('Time t');
ylabel('x(t)');
title('Comparison of 3, 11 and 51-Term Fourier Approximations'); 
legend('Original', '3 terms', '11 terms', '51 terms'); 
xlim([0 T]);
ylim([-0.1 1.2]); 

%% PART (f): LINE SPECTRA
K = 25; 
k = -K:K; 
Ck = zeros(size(k)); 
Ck(k==0) = 2/3; 
nz = (k~=0); 
Ck(nz) = 3*(cos(2*pi*k(nz)/3)-1) ./ (2*pi^2*k(nz).^2); 

% Frequency location of every spectral line
omega = k*w0; 
% Magnitude
Cmag = abs(Ck); 
% Phase
Cphase = angle(Ck); 

% Remove meaningless phase values for zero coefficients
Cphase(Cmag < 1e-12) = 0; 

figure('Name', 'Complex Fourier Series Line Spectrum'); 
% Magnitude line spectrum
subplot(2,1,1);
stem(omega, Cmag, 'filled'); 
grid on;
xlabel('\omega = k\omega_0 (rad/s)');
ylabel('|C_k|');
title('Magnitude Line Spectrum'); 

% Phase line spectrum
subplot(2,1,2);
stem(omega, Cphase, 'filled'); 
grid on;
xlabel('\omega = k\omega_0 (rad/s)');
ylabel('\angle C_k (rad)');
title('Phase Line Spectrum'); 

%% PART (g): THREE "GOOD" APPROXIMATIONS OVER FIVE PERIODS
t5 = linspace(0,5*T,15001); 
% Convert t5 into one-period variable
tau = mod(t5,T); 

% Original periodic signal over five periods
x5 = zeros(size(tau)); 
index1 = (tau >= 0) & (tau < 1); 
x5(index1) = tau(index1); 
index2 = (tau >= 1) & (tau < 2); 
x5(index2) = 1; 
index3 = (tau >= 2) & (tau <= 3); 
x5(index3) = 3 - tau(index3); 

% 51-term Complex Exponential FS
K = 25; 
k = -K:K; 
Ck = zeros(size(k)); 
Ck(k==0) = 2/3; 
nz = (k~=0); 
Ck(nz) = 3*(cos(2*pi*k(nz)/3)-1) ./ (2*pi^2*k(nz).^2); 
E5 = exp(1i*(k(:)*w0)*t5); 
xComplex5 = real(Ck*E5); 

% 51-term Trigonometric FS
n = 1:K; 
a0 = 4/3; 
an = 3*(cos(2*pi*n/3)-1) ./ (pi^2*n.^2); 
bn = zeros(size(n)); 
theta5 = (n(:)*w0)*t5; 
xTrig5 = a0/2 + an*cos(theta5) + bn*sin(theta5); 

% 51-term Cosine-with-Phase FS
An = sqrt(an.^2 + bn.^2); 
phi_n = atan2(-bn,an); 
phi_n(An < 1e-12) = 0; 
thetaPhase5 = bsxfun(@plus, theta5, phi_n(:)); 
xPhase5 = a0/2 + An*cos(thetaPhase5); 

% Plot all three good approximations over five periods
figure('Name', 'Three Good Approximations Over Five Periods'); 

% Complex exponential
subplot(3,1,1);
plot(t5,x5, 'k', 'LineWidth', 1.5); 
hold on;
plot(t5, xComplex5, 'r--', 'LineWidth', 1.2); 
grid on;
xlabel('Time t');
ylabel('x(t)');
title('51-Term Complex Exponential Fourier Series'); 
legend('Original', 'Complex FS'); 
xlim([0 5*T]); 
ylim([-0.1 1.2]); 

% Trigonometric
subplot(3,1,2);
plot(t5,x5, 'k', 'LineWidth', 1.5); 
hold on;
plot(t5,xTrig5, 'b--', 'LineWidth',1.2); 
grid on;
xlabel('Time t');
ylabel('x(t)');
title('51-Term Trigonometric Fourier Series'); 
legend('Original', 'Trigonometric FS'); 
xlim([0 5*T]); 
ylim([-0.1 1.2]); 

% Cosine with phase
subplot(3,1,3);
plot(t5,x5, 'k', 'LineWidth',1.5); 
hold on;
plot(t5, xPhase5, 'm--', 'LineWidth',1.2); 
grid on;
xlabel('Time t'); 
ylabel('x(t)'); 
title('51-Term Cosine-with-Phase Fourier Series'); 
legend('Original', 'Cosine-Phase FS'); 
xlim([0 5*T]); 
ylim([-0.1 1.2]); 

% FINAL CHECK
% The three representations must produce practically the same 51-term approximation.
difference1 = max(abs(xComplex5 - xTrig5)); 
difference2 = max(abs(xComplex5 - xPhase5)); 

fprintf('\n'); 
fprintf(' FINAL NUMERICAL CHECK\n'); 
fprintf('Max difference: Complex vs Trigonometric = %.3e\n', difference1); 
fprintf('Max difference: Complex vs Cosine-Phase = %.3e\n', difference2);