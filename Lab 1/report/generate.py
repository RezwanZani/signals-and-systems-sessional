import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import re

# Initialize document
doc = docx.Document()

# Page setup - Margins (0.8 inches on all sides)
for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# Color Palette Definitions
COLOR_PRIMARY = RGBColor(0, 51, 102)     # Deep Navy
COLOR_SECONDARY = RGBColor(70, 130, 180) # Steel Blue
COLOR_TEXT = RGBColor(40, 40, 40)        # Charcoal
COLOR_MUTED = RGBColor(120, 120, 120)    # Gray
HEX_PRIMARY_BG = "EBF3FA"
HEX_CODE_BG = "F8F9FA"
HEX_BOX_BG = "FAFAFA"

def set_cell_background(cell, fill_hex):
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def set_cell_borders(cell, top="none", bottom="none", left="none", right="none", 
                     color="CCCCCC", sz="4"):
    def border_tag(side, val):
        if val == "none":
            return f'<w:{side} {nsdecls("w")} w:val="none"/>'
        return f'<w:{side} {nsdecls("w")} w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
    
    borders_xml = f'''
        <w:tcBorders {nsdecls("w")}>
            {border_tag("top", top)}
            {border_tag("left", left)}
            {border_tag("bottom", bottom)}
            {border_tag("right", right)}
        </w:tcBorders>
    '''
    cell._tc.get_or_add_tcPr().append(parse_xml(borders_xml))

# MATLAB Keywords and Built-in Functions
KEYWORDS = {
    'clc', 'clear', 'close', 'all', 'hold', 'on', 'off', 'grid', 'figure', 
    'if', 'else', 'elseif', 'end', 'for', 'while', 'return', 'function'
}
BUILTINS = {
    'linspace', 'cos', 'sin', 'exp', 'stem', 'plot', 'xlabel', 'ylabel', 
    'title', 'legend', 'subplot', 'sgtitle', 'xlim', 'ylim', 'ones', 
    'size', 'ceil', 'floor', 'double', 'abs', 'real', 'imag', 'trapz', 
    'fprintf', 'max', 'isfinite'
}

def highlight_matlab_code_in_cell(cell, code_text):
    C_KEYWORD = RGBColor(0, 0, 255)      # Blue
    C_BUILTIN = RGBColor(0, 110, 140)    # Teal / Deep Cyan
    C_STRING  = RGBColor(163, 21, 21)    # Red/Maroon
    C_COMMENT = RGBColor(34, 139, 34)    # Forest Green
    C_NUMBER  = RGBColor(128, 0, 128)    # Purple
    C_DEFAULT = RGBColor(30, 30, 30)     # Dark

    lines = code_text.strip().split('\n')
    for line_idx, line in enumerate(lines):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1.5)
        p.paragraph_format.line_spacing = Pt(12)
        
        token_pattern = re.compile(
            r'(%.*$)|'                         
            r"('(?:''|[^'\n])*')|"             
            r'("(?:""|[^"\n])*")|'             
            r'(\b[A-Za-z_][A-Za-z0-9_]*\b)|'  
            r'(\b\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\b)|' 
            r'(\s+)|'                          
            r'(.)'                             
        )
        
        for match in token_pattern.finditer(line):
            comment, str1, str2, word, num, space, other = match.groups()
            run = p.add_run()
            run.font.name = 'Consolas'
            run.font.size = Pt(9.5)
            
            if comment:
                run.text = comment
                run.font.color.rgb = C_COMMENT
            elif str1:
                run.text = str1
                run.font.color.rgb = C_STRING
            elif str2:
                run.text = str2
                run.font.color.rgb = C_STRING
            elif word:
                run.text = word
                if word in KEYWORDS:
                    run.font.color.rgb = C_KEYWORD
                    run.font.bold = True
                elif word in BUILTINS:
                    run.font.color.rgb = C_BUILTIN
                    run.font.bold = True
                else:
                    run.font.color.rgb = C_DEFAULT
            elif num:
                run.text = num
                run.font.color.rgb = C_NUMBER
            elif space:
                run.text = space
                run.font.color.rgb = C_DEFAULT
            elif other:
                run.text = other
                run.font.color.rgb = C_DEFAULT

# --- Document Header & Title ---
header_p = doc.add_paragraph()
header_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
header_p.paragraph_format.space_after = Pt(2)
run_sub = header_p.add_run("DEPARTMENT OF AVIONICS ENGINEERING\nAVE 4502: SIGNALS AND SYSTEMS SESSIONAL")
run_sub.font.name = 'Calibri'
run_sub.font.size = Pt(11)
run_sub.font.bold = True
run_sub.font.color.rgb = COLOR_SECONDARY

title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_p.paragraph_format.space_after = Pt(16)
run_title = title_p.add_run("LABORATORY REPORT 01\nBasic Signals, Operations & Signal Properties")
run_title.font.name = 'Calibri'
run_title.font.size = Pt(18)
run_title.font.bold = True
run_title.font.color.rgb = COLOR_PRIMARY

# Meta Table (Student & Course Info)
info_table = doc.add_table(rows=2, cols=2)
info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
info_table.autofit = False

info_data = [
    [("Course Code & Title:", " AVE 4502: Signals and Systems Sessional"), ("Date of Performance:", " 30 August 2026")],
    [("Lab Title:", " Lab 01 - Signal Generation & Transformations"), ("Student Name / ID:", " ______________________")]
]

for row_idx, row in enumerate(info_table.rows):
    for col_idx, cell in enumerate(row.cells):
        cell.width = Inches(3.4)
        set_cell_background(cell, HEX_PRIMARY_BG)
        set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
        set_cell_borders(cell, top="single", bottom="single", left="single", right="single", color="B0C4DE", sz="4")
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        lbl, val = info_data[row_idx][col_idx]
        r1 = p.add_run(lbl)
        r1.font.name = 'Calibri'
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_PRIMARY
        r2 = p.add_run(val)
        r2.font.name = 'Calibri'
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_TEXT

doc.add_paragraph().paragraph_format.space_after = Pt(12)

# Exercises Definitions
exercises = [
    {
        "num": "Exercise 01",
        "title": "Continuous & Discrete-Time Signals and Complex Exponentials",
        "desc": "Define and plot:\n"
                "a) The continuous-time signal x₁(t) = cos(πt)\n"
                "b) The discrete-time signal x₂[n] = cos(πn)\n"
                "c) The real part and the imaginary part of the signal x(t) = e^(j3πt) in time of two periods.",
        "code": r"""%% Continuous-time signal x1(t) = cos(pi*t)
t = linspace(-2, 2, 500); % time from -2 to 2
x1 = cos(pi*t);
figure;
plot(t, x1, 'b', 'LineWidth', 1.5);
grid on;
xlabel('t'); ylabel('x1(t)');
title('Continuous-time signal x1(t) = cos(\pi t)');

%% Discrete-time signal x2[n] = cos(pi*n)
n = -10:10; % discrete time indices
x2 = cos(pi*n);
figure;
stem(n, x2, 'r', 'filled'); % stem plot for discrete signals
grid on;
xlabel('n'); ylabel('x2[n]');
title('Discrete-time signal x2[n] = cos(\pi n)');

%% Real and Imag part of x(t) = e^{j 3\pi t}
T = 2/3; % fundamental period
t2 = linspace(0, 2*T, 500); % two periods (0 to 4/3)
x = exp(1j*3*pi*t2);

figure;
plot(t2, real(x), 'b', 'LineWidth', 1.5); hold on;
plot(t2, imag(x), '--', 'LineWidth', 1.5);
grid on;
xlabel('t'); ylabel('Value');
title('Real and Imag parts of x(t) = e^{j 3\pi t}');
legend('Re\{x(t)\} = cos(3\pi t)', 'Im\{x(t)\} = sin(3\pi t)');""",
        "output_label": "Output Plot 01: Continuous, Discrete, and Complex Exponential Signals"
    },
    {
        "num": "Exercise 02",
        "title": "Basic Elementary Signals and Combinations",
        "desc": "Plot in the time interval -5 ≤ t ≤ 10 the following signals:\n"
                "a) u(t),  b) u(t+3),  c) u(t-2) - u(t+3),  d) e^(-t)u(t+2)\n"
                "e) δ(t),  f) δ(t-2),  g) δ(t-1) + δ(t+2)\n"
                "h) r(t),  i) r(t-1),  j) r(t) - r(t-2) - r(t-5) + r(t-7)\n"
                "k) p₄(t) = ∑ δ(t - 4k),  l) p₂(t-1) = ∑ δ(t - 1 - 2k)",
        "code": r"""clc;
clear;
close all;

%% Time axis
t = linspace(-5, 10, 3001); % Time interval -5 <= t <= 10

%% Basic signals
u = @(x) double(x >= 0); % Unit step function
r = @(x) x .* u(x);      % Unit ramp function

% (a) u(t)
xa = u(t);

% (b) u(t+3)
xb = u(t+3);

% (c) u(t-2) - u(t+3)
xc = u(t-2) - u(t+3);

% (d) e^{-t}u(t+2)
xd = exp(-t) .* u(t+2);

%% Impulse signals
% (e) delta(t)
delta1_time = 0;

% (f) delta(t-2)
delta2_time = 2;

% (g) delta(t-1) + delta(t+2)
delta_sum_time = [-2 1];

% (h) r(t)
xh = r(t);

% (i) r(t-1)
xi = r(t-1);

% (j) r(t) - r(t-2) - r(t-5) + r(t-7)
xj = r(t) - r(t-2) - r(t-5) + r(t-7);

%% (k) p4(t) = sum delta(t-4k)
k4 = ceil(-5/4) : floor(10/4);
p4_time = 4 * k4;

%% (l) p2(t-1) = sum delta(t-1-2k)
k2 = ceil((-5-1)/2) : floor((10-1)/2);
p2_time = 1 + 2 * k2;

%% Plot all signals (Example of plotting a few subplots)
figure('Color', 'w');
subplot(4, 3, 1)
plot(t, xa, 'LineWidth', 1.5)
grid on
title('(a) u(t)')
xlabel('t')
ylabel('Amplitude')""",
        "output_label": "Output Plot 02: 12-Subplot Matrix of Elementary Signals in [-5, 10]"
    },
    {
        "num": "Exercise 03",
        "title": "Even and Odd Symmetry Decomposition",
        "desc": "Determine if the signal x(t) = t·cos(t) is symmetric, and if yes what kind of symmetry.\n"
                "Also, decompose x(t) into its even and odd parts and confirm your analytical result via MATLAB simulation.",
        "code": r"""clc;
clear;
close all;

%% Time axis
t = linspace(-6, 6, 2000);

%% Original signal x(t) = t cos(t)
x = t .* cos(t);

%% Calculate x(-t)
x_neg = (-t) .* cos(-t);

%% Even and Odd decomposition
xe = 0.5 * (x + x_neg); % Even part
xo = 0.5 * (x - x_neg); % Odd part

%% Verification
fprintf('Maximum value of even part = %.2e\n', max(abs(xe)));
fprintf('Maximum difference between x(t) and odd part = %.2e\n', max(abs(x-xo)));

%% Plotting
figure;
plot(t, x, 'k', 'LineWidth', 1.5);
hold on;
plot(t, xe, 'r--', 'LineWidth', 1.5);
plot(t, xo, 'b-.', 'LineWidth', 1.5);
grid on;
xlabel('t');
ylabel('Amplitude');
title('Even/Odd decomposition of x(t)=t cos(t)');
legend('x(t)=t cos(t)', 'Even part x_e(t)', 'Odd part x_o(t)');""",
        "output_label": "Output Plot 03: Even/Odd Signal Decomposition and Reconstruction"
    },
    {
        "num": "Exercise 04",
        "title": "Signal Classification: Energy and Power Signals",
        "desc": "Determine whether the signal x(t) = t[u(t) - u(t-8)] is an energy or power signal by calculating total energy E and average power P.",
        "code": r"""clc;
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
end""",
        "output_label": "Output Plot 04: Truncated Ramp Signal x(t) = t[u(t) - u(t-8)]"
    },
    {
        "num": "Exercise 05",
        "title": "Time Transformations on Continuous-Time Signals",
        "desc": "Consider the signal x(t) = t[u(t) - u(t-5)]. Implement and plot the following transformations:\n"
                "(a) x(-t) [Time Reversal],  (b) x(4t) [Compression],  (c) x(0.3t) [Expansion]\n"
                "(d) x(t+2) [Time Advance],  (e) x(t-3) [Time Delay],  (f) x(1-3t) [Combined Scaling & Shift]",
        "code": r"""clc;
clear;
close all;

%% Define unit step function
u = @(t) double(t >= 0);

%% Define original signal
% x(t) = t[u(t) - u(t-5)]
x = @(t) t .* (u(t) - u(t-5));

%% Time axis
t = linspace(-8, 10, 5000);

%% Generate transformed signals
xa = x(-t);         % (a) Time reversal
xb = x(4*t);        % (b) Compression by 4
xc = x(0.3*t);      % (c) Expansion by 1/0.3
xd = x(t+2);        % (d) Shift left by 2
xe = x(t-3);        % (e) Shift right by 3
xf = x(1-3*t);      % (f) Reflection + compression + shift

%% Plot all signals
figure('Color', 'w');

% Plot (a)
subplot(3, 2, 1)
plot(t, xa, 'LineWidth', 1.5);
grid on;
xlabel('t'); ylabel('x(-t)');
title('(a) x(-t)');

% Plot (b)
subplot(3, 2, 2)
plot(t, xb, 'LineWidth', 1.5);
grid on;
xlabel('t'); ylabel('x(4t)');
title('(b) x(4t)');

% Plot (c)
subplot(3, 2, 3)
plot(t, xc, 'LineWidth', 1.5);
grid on;
xlabel('t'); ylabel('x(0.3t)');
title('(c) x(0.3t)');

% Plot (d)
subplot(3, 2, 4)
plot(t, xd, 'LineWidth', 1.5);
grid on;
xlabel('t'); ylabel('x(t+2)');
title('(d) x(t+2)');

% Plot (e)
subplot(3, 2, 5)
plot(t, xe, 'LineWidth', 1.5);
grid on;
xlabel('t'); ylabel('x(t-3)');
title('(e) x(t-3)');

% Plot (f)
subplot(3, 2, 6)
plot(t, xf, 'LineWidth', 1.5);
grid on;
xlabel('t'); ylabel('x(1-3t)');
title('(f) x(1-3t)');

sgtitle('Time Transformations of x(t)=t[u(t)-u(t-5)]');""",
        "output_label": "Output Plot 05: 6-Subplot Transformation Suite of x(t) = t[u(t) - u(t-5)]"
    }
]

# Build Exercises into DOCX
for ex in exercises:
    # 1. Heading
    h_p = doc.add_paragraph()
    h_p.paragraph_format.space_before = Pt(14)
    h_p.paragraph_format.space_after = Pt(2)
    h_p.paragraph_format.keep_with_next = True
    
    r_num = h_p.add_run(f"{ex['num']}: ")
    r_num.font.name = 'Calibri'
    r_num.font.size = Pt(13)
    r_num.font.bold = True
    r_num.font.color.rgb = COLOR_PRIMARY
    
    r_t = h_p.add_run(ex['title'])
    r_t.font.name = 'Calibri'
    r_t.font.size = Pt(13)
    r_t.font.bold = True
    r_t.font.color.rgb = COLOR_SECONDARY

    # 2. Problem Statement Box
    desc_table = doc.add_table(rows=1, cols=1)
    desc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    desc_table.autofit = False
    c_desc = desc_table.rows[0].cells[0]
    c_desc.width = Inches(6.8)
    set_cell_background(c_desc, HEX_PRIMARY_BG)
    set_cell_margins(c_desc, top=80, bottom=80, left=120, right=120)
    set_cell_borders(c_desc, left="single", color="003366", sz="18")
    
    p_desc = c_desc.paragraphs[0]
    p_desc.paragraph_format.space_after = Pt(0)
    p_desc.paragraph_format.line_spacing = Pt(13)
    r_desc = p_desc.add_run(ex['desc'])
    r_desc.font.name = 'Calibri'
    r_desc.font.size = Pt(10)
    r_desc.font.color.rgb = COLOR_TEXT

    # 3. Code Heading
    c_head = doc.add_paragraph()
    c_head.paragraph_format.space_before = Pt(8)
    c_head.paragraph_format.space_after = Pt(2)
    c_head.paragraph_format.keep_with_next = True
    r_ch = c_head.add_run("MATLAB Implementation Code:")
    r_ch.font.name = 'Calibri'
    r_ch.font.size = Pt(10.5)
    r_ch.font.bold = True
    r_ch.font.color.rgb = COLOR_PRIMARY

    # 4. Code Block with Syntax Highlighting
    code_table = doc.add_table(rows=1, cols=1)
    code_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    code_table.autofit = False
    c_code = code_table.rows[0].cells[0]
    c_code.width = Inches(6.8)
    set_cell_background(c_code, HEX_CODE_BG)
    set_cell_margins(c_code, top=100, bottom=100, left=120, right=120)
    set_cell_borders(c_code, top="single", bottom="single", left="single", right="single", color="D0D5DD", sz="4")
    
    highlight_matlab_code_in_cell(c_code, ex['code'])

    # 5. Output Heading
    out_head = doc.add_paragraph()
    out_head.paragraph_format.space_before = Pt(8)
    out_head.paragraph_format.space_after = Pt(2)
    out_head.paragraph_format.keep_with_next = True
    r_oh = out_head.add_run("Simulation Output Plot:")
    r_oh.font.name = 'Calibri'
    r_oh.font.size = Pt(10.5)
    r_oh.font.bold = True
    r_oh.font.color.rgb = COLOR_PRIMARY

    # 6. Blank Output Box with dashed border for manual plot insertion
    out_table = doc.add_table(rows=1, cols=1)
    out_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    out_table.autofit = False
    c_out = out_table.rows[0].cells[0]
    c_out.width = Inches(6.8)
    set_cell_background(c_out, HEX_BOX_BG)
    set_cell_margins(c_out, top=200, bottom=200, left=150, right=150)
    set_cell_borders(c_out, top="dashed", bottom="dashed", left="dashed", right="dashed", color="999999", sz="6")
    
    p_box = c_out.paragraphs[0]
    p_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_box.paragraph_format.space_before = Pt(60)
    p_box.paragraph_format.space_after = Pt(60)
    r_ph = p_box.add_run(f"[ Insert Output Plot Image Here ]\n{ex['output_label']}")
    r_ph.font.name = 'Calibri'
    r_ph.font.size = Pt(10.5)
    r_ph.font.italic = True
    r_ph.font.color.rgb = COLOR_MUTED

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(8)

output_filename = "Lab_01_Signals_and_Systems_Report.docx"
doc.save(output_filename)
print(f"Report saved to: {output_filename}")