clc;
clear;
close all;

% Define symbolic variables
syms t s

% 2(a): Laplace Transform of Dirac delta function
f1 = dirac(t);
F1 = laplace(f1, t, s);

% 2(b): Laplace Transform of Heaviside step function u(t)
f2 = heaviside(t);
F2 = laplace(f2, t, s);

% 2(c): Laplace Transform of exp(-3t)*u(t)
f3 = exp(-3*t) * heaviside(t);
F3 = laplace(f3, t, s);

% 2(d): Laplace Transform of cos(2*pi*t)*u(t)
f4 = cos(2*pi*t) * heaviside(t);
F4 = laplace(f4, t, s);

% Display results

disp('2(a):'); disp(F1);
disp('2(b):'); disp(F2);
disp('2(c):'); disp(F3);
disp('2(d):'); disp(F4);
