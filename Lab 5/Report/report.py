import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def add_code_block(doc, code_text):
    """Adds a highlighted block for MATLAB code."""
    table = doc.add_table(rows=1, cols=1)
    table.autofit = True
    cell = table.cell(0, 0)
    
    # Set a light gray background for the code block
    tcPr = cell._tc.get_or_add_tcPr()
    shading = OxmlElement('w:shd')
    shading.set(qn('w:val'), 'clear')
    shading.set(qn('w:color'), 'auto')
    shading.set(qn('w:fill'), 'F4F4F4')
    tcPr.append(shading)
    
    paragraph = cell.paragraphs[0]
    run = paragraph.add_run(code_text)
    run.font.name = 'Courier New'
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0, 0, 128)
    
    # Add a little spacing after the table
    doc.add_paragraph()

def add_plot_placeholder(doc, label):
    """Adds a dashed box placeholder for inserting graphs."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(f"\n[ INSERT {label} HERE ]\n")
    run.font.name = 'Arial'
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(128, 128, 128)
    run.bold = True
    doc.add_paragraph()

def main():
    doc = Document()
    
    # --- Title Page / Header ---
    title = doc.add_heading('Signals and Systems Sessional', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    subtitle = doc.add_heading('Lab 05 Report', 1)
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    student_info = doc.add_paragraph()
    student_info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    student_info.add_run('Name: Rezwan Shajib\n').bold = True
    student_info.add_run('Course: AVE 4502\n')
    doc.add_page_break()

    # ==========================================
    # EXERCISE 01
    # ==========================================
    doc.add_heading('Exercise 01: Discrete-Time System Frequency & System Response', level=2)
    
    doc.add_heading('Problem Statement', level=3)
    p = doc.add_paragraph("Suppose that a discrete-time system is described by the frequency response:\n\n")
    p.add_run("H(ω) = (4 + 2e^{-2jω}) / (3 + 5e^{-jω})\n\n").bold = True
    p.add_run("Plot the frequency response H(ω). Also, compute and plot the system response to the discrete-time input signal:\n\n")
    p.add_run("x[n] = 2cos(4n + π/6)").bold = True
    
    doc.add_heading('MATLAB Code', level=3)
    ex1_code = """clc;
clear;
close all;

%% Part 1: Frequency Response H(w)
% Define frequency range
w = linspace(-pi, pi, 2000);

% Define system frequency response
H = (4 + 2*exp(-1j*2*w)) ./ (3 + 5*exp(-1j*w));

% Plot Magnitude and Phase Response
figure(1);

subplot(2,1,1);
plot(w, abs(H), 'b', 'LineWidth', 1.5);
grid on;
xlabel('Frequency (rad/sample)');
ylabel('|H(w)|');
title('Magnitude Response');

subplot(2,1,2);
plot(w, unwrap(angle(H)), 'r', 'LineWidth', 1.5);
grid on;
xlabel('Frequency (rad/sample)');
ylabel('Phase (radians)');
title('Phase Response');


%% Part 2: System Response to Input x[n]
% Time index and input signal parameters
n = 0:40;
x = 2 * cos(4*n + pi/6);
w0 = 4;

% System response at frequency w0 = 4
H0 = (4 + 2*exp(-1j*2*w0)) / (3 + 5*exp(-1j*w0));

% Output magnitude and phase
A = 2 * abs(H0);
phi = pi/6 + angle(H0);

% Compute output signal y[n]
y = A * cos(w0*n + phi);

% Display numerical results
fprintf('H(4) = %.6f + %.6fj\\n', real(H0), imag(H0));
fprintf('Magnitude of H(4) = %.6f\\n', abs(H0));
fprintf('Phase of H(4) = %.6f radians\\n', angle(H0));
fprintf('Output amplitude = %.6f\\n', A);
fprintf('Output phase = %.6f radians\\n', phi);

% Plot Input and Output signals
figure(2);

subplot(2,1,1);
stem(n, x, 'filled', 'b');
grid on;
xlabel('n');
ylabel('x[n]');
title('Input Signal x[n]');

subplot(2,1,2);
stem(n, y, 'filled', 'r');
grid on;
xlabel('n');
ylabel('y[n]');
title('Output Signal y[n]');"""
    add_code_block(doc, ex1_code)

    doc.add_heading('Numerical Outputs', level=3)
    out1 = doc.add_paragraph()
    out1.add_run("• H(4): ").bold = True
    out1.add_run("-0.589430 - 0.938397j\n")
    out1.add_run("• Magnitude |H(4)|: ").bold = True
    out1.add_run("1.108159\n")
    out1.add_run("• Phase ∠H(4): ").bold = True
    out1.add_run("-2.131640 radians\n")
    out1.add_run("• Output Amplitude (A): ").bold = True
    out1.add_run("2.216318\n")
    out1.add_run("• Output Phase (φ): ").bold = True
    out1.add_run("-1.608041 radians")

    add_plot_placeholder(doc, "FIGURE 1: MAGNITUDE & PHASE RESPONSE")
    add_plot_placeholder(doc, "FIGURE 2: INPUT AND OUTPUT SIGNALS")
    
    doc.add_page_break()

    # ==========================================
    # EXERCISE 02
    # ==========================================
    doc.add_heading('Exercise 02: Unilateral Laplace Transform', level=2)
    
    doc.add_heading('Problem Statement', level=3)
    p2 = doc.add_paragraph("Compute the unilateral Laplace transform of the following functions:\n")
    p2.add_run("2(a): δ(t)\n2(b): u(t)\n2(c): e^{-3t}u(t)\n2(d): cos(2πt)u(t)")
    
    doc.add_heading('MATLAB Code', level=3)
    ex2_code = """clc;
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
disp('2(d):'); disp(F4);"""
    add_code_block(doc, ex2_code)

    doc.add_heading('Analytical Results', level=3)
    out2 = doc.add_paragraph()
    out2.add_run("• 2(a) ℒ{δ(t)}: ").bold = True
    out2.add_run("1\n")
    out2.add_run("• 2(b) ℒ{u(t)}: ").bold = True
    out2.add_run("1 / s\n")
    out2.add_run("• 2(c) ℒ{e^{-3t}u(t)}: ").bold = True
    out2.add_run("1 / (s + 3)\n")
    out2.add_run("• 2(d) ℒ{cos(2πt)u(t)}: ").bold = True
    out2.add_run("s / (s² + 4π²)")

    # Save Document
    filename = "Lab_05_Signals_and_Systems_Report.docx"
    doc.save(filename)
    print(f"Success! {filename} has been generated in your current directory.")

if __name__ == "__main__":
    main()