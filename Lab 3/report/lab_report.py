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
    'if', 'else', 'elseif', 'end', 'for', 'while', 'return', 'function', 'subplot', 'stem', 'plot'
}
BUILTINS = {
    'linspace', 'cos', 'sin', 'exp', 'xlabel', 'ylabel', 'title', 'legend', 
    'xlim', 'ylim', 'ones', 'zeros', 'size', 'ceil', 'floor', 'double', 'abs', 
    'real', 'imag', 'trapz', 'fprintf', 'max', 'min', 'isfinite', 'conv', 'length', 'filter', 'num2str'
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
run_title = title_p.add_run("LABORATORY REPORT 03\nContinuous and Discrete-Time System Responses")
run_title.font.name = 'Calibri'
run_title.font.size = Pt(18)
run_title.font.bold = True
run_title.font.color.rgb = COLOR_PRIMARY

# Meta Table (Student & Course Info)
info_table = doc.add_table(rows=2, cols=2)
info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
info_table.autofit = False

info_data = [
    [("Course Code & Title:", " AVE 4502: Signals and Systems Sessional"), ("Date of Performance:", " ______________________")],
    [("Lab Title:", " Lab 03 - Convolution and System Responses"), ("Student Name / ID:", " Rezwan Shajib / ___________")]
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

# Exercises Definitions (Hardcoded Lab 03 Data)
exercises = [
    {
        "num": "Exercise 01",
        "title": "System Response to a Continuous-Time Signal",
        "desc": "Suppose that a system is described by the impulse response h(t) = sin(3πt)[u(t) - u(t-5)]. Compute and plot the system response to the input signal x(t) = cos(2πt)[u(t) - u(t-5)].",
        "code": r"""% 1. Define the continuous time approximation
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
grid on;""",
        "output_label": "Plot 01: System Response Computation"
    },
    {
        "num": "Exercise 02",
        "title": "Continuous-Time Convolution of Exponential and Trigonometric Signals",
        "desc": "Compute and plot the convolution between the signals x(t) = cos(πt)[u(t+2) - u(t-3)] and h(t) = 5e^{-t}u(t).",
        "code": r"""clc;
clear;
close all;

fprintf('--- Continuous-Time Convolution Analysis ---\n\n');

% 1. Define the continuous time approximation
dt = 0.001;          % Very small time step
t = -2:dt:8;         % Time vector covering before and after the signals
fprintf('Time step (dt) set to: %.3f seconds\n', dt);

% 2. Define the window: [u(t) - u(t-5)]
% This creates an array of 1s between 0 and 5, and 0s elsewhere
window = (t >= 0) & (t <= 5);

% 3. Generate x(t) and h(t)
x = cos(2*pi*t) .* window; 
h = sin(3*pi*t) .* window; 
fprintf('Signals x(t) and h(t) generated successfully for t = [0, 5].\n');
fprintf('Calculating continuous convolution approximation...\n');

% 4. Compute the continuous convolution approximation
y = conv(x, h) * dt; 

% 5. Determine the output time vector
% The output time starts at the sum of the input start times
t_start = t(1) + t(1); 
ty = t_start : dt : t_start + (length(y)-1)*dt;

% ---> ADDED: Print useful analytical outputs from the convolution to the Command Window
fprintf('Convolution complete.\n');
fprintf('--------------------------------------------------\n');
fprintf('Output Time Range          : [%.2f, %.2f] seconds\n', ty(1), ty(end));
fprintf('Maximum Output Amplitude   : %.4f\n', max(y));
fprintf('Minimum Output Amplitude   : %.4f\n', min(y));
fprintf('Output Vector Length       : %d samples\n', length(y));
fprintf('--------------------------------------------------\n');
fprintf('Generating plot...\n\n');

% 6. Visualize the continuous signals
% ---> MODIFIED: Added 'Color', 'w' for a clean white background for lab reports
figure('Color', 'w', 'Name', 'Continuous-Time Convolution');

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
grid on;""",
        "output_label": "Plot 02: Exponential Convolution"
    },
    {
        "num": "Exercise 03",
        "title": "Discrete-Time Difference Equation Responses",
        "desc": "Consider the system described by the difference equation y[n] + 0.1y[n-1] - y[n-2] = x[n] + 2x[n-1] and assume zero initial conditions. Compute and plot for 0 ≤ n ≤ 30:\na. The impulse response h[n] of the system.\nb. The step response r[n] of the system.\nc. Finally, compute and plot the response y[n] of the system to the input signal: x[n] = 0.8^n cos(n), 0 ≤ n ≤ 50.",
        "code": r"""clc; clear; close all;

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
title('Output y[n] for x[n] = 0.8^n cos(n)'); xlabel('n'); ylabel('Amplitude');""",
        "output_label": "Plot 03: Discrete-Time System Responses"
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
    r_oh = out_head.add_run("Simulation Output Plot & Command Window:")
    r_oh.font.name = 'Calibri'
    r_oh.font.size = Pt(10.5)
    r_oh.font.bold = True
    r_oh.font.color.rgb = COLOR_PRIMARY

    # 6. Blank Output Box with dashed border for manual plot/command insertion
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

output_filename = "Lab_03_Signals_and_Systems_Report.docx"
doc.save(output_filename)
print(f"Report saved to: {output_filename}")