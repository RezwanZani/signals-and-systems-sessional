import os
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

def set_cell_borders(cell, top="none", bottom="none", left="none", right="none", color="CCCCCC", sz="4"):
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
    'if', 'else', 'elseif', 'end', 'for', 'while', 'return', 'function', 'true', 'false'
}
BUILTINS = {
    'linspace', 'cos', 'sin', 'exp', 'xlabel', 'ylabel', 'title', 'legend', 
    'xlim', 'ylim', 'ones', 'zeros', 'size', 'ceil', 'floor', 'double', 'abs', 
    'real', 'imag', 'trapz', 'fprintf', 'max', 'min', 'isfinite', 'conv', 'length', 
    'filter', 'num2str', 'mean', 'std', 'sum', 'randn', 'rand', 'rng', 'sqrt', 
    'histogram', 'scatter', 'categorical', 'bar', 'xline', 'bsxfun', 'atan2', 'mod', 'angle', 'stem', 'subplot'
}

def highlight_matlab_code_in_cell(cell, code_text):
    C_KEYWORD = RGBColor(0, 0, 255)      # Blue
    C_BUILTIN = RGBColor(0, 110, 140)    # Teal / Deep Cyan
    C_STRING  = RGBColor(163, 21, 21)    # Red/Maroon
    C_COMMENT = RGBColor(34, 139, 34)    # Forest Green
    C_NUMBER  = RGBColor(128, 0, 128)    # Purple
    C_DEFAULT = RGBColor(30, 30, 30)     # Dark

    lines = code_text.strip().split('\n')
    for line in lines:
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
run_title = title_p.add_run("LABORATORY REPORT 04\nFourier Series Approximations & Line Spectra")
run_title.font.name = 'Calibri'
run_title.font.size = Pt(18)
run_title.font.bold = True
run_title.font.color.rgb = COLOR_PRIMARY

# Meta Table
info_table = doc.add_table(rows=2, cols=2)
info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
info_table.autofit = False

info_data = [
    [("Course Code & Title:", " AVE 4502: Signals and Systems Sessional"), ("Date of Performance:", " 01 November 2026")],
    [("Lab Title:", " Lab 04 - Fourier Series Representations"), ("Student Name / ID:", " Rezwan Shajib / _________________")]
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

# --- Read MATLAB File ---
matlab_filepath = r"C:\Users\Rezwan Shajib\Documents\MATLAB\Signal and Systems\Lab 4\exercise_1.m"
try:
    with open(matlab_filepath, "r", encoding="utf-8") as f:
        matlab_code = f.read()
except FileNotFoundError:
    matlab_code = "% Error: The file exercise_1.m was not found at the specified path.\n% Please ensure the file exists."

# --- Write Exercise Section ---
# 1. Heading
h_p = doc.add_paragraph()
h_p.paragraph_format.space_before = Pt(14)
h_p.paragraph_format.space_after = Pt(2)
h_p.paragraph_format.keep_with_next = True

r_num = h_p.add_run("Lab Exercise: ")
r_num.font.name = 'Calibri'
r_num.font.size = Pt(13)
r_num.font.bold = True
r_num.font.color.rgb = COLOR_PRIMARY

r_t = h_p.add_run("Comprehensive Fourier Series Analysis")
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
desc_text = (
    "A periodic trapezoidal signal x(t) with period T=3 is given by:\n"
    "    x(t) = t for 0 ≤ t ≤ 1\n"
    "    x(t) = 1 for 1 ≤ t ≤ 2\n"
    "    x(t) = 3 - t for 2 ≤ t ≤ 3\n\n"
    "Compute and plot approximations of x(t) using 3, 11, and 51 terms for:\n"
    "    • 3, 11, and 51 terms of the complex exponential Fourier series.\n"
    "    • 3, 11, and 51 terms of the trigonometric Fourier series.\n"
    "    • 3, 11, and 51 terms of the Fourier series in cosine with phase form.\n"
    "    • Each time also plot the corresponding Fourier series coefficients.\n"
    "    • Each time compute the approximation percentage.\n"
    "    • Plot the line spectra.\n"
    "    • Finally, plot the three ‘‘good’’ approximations in time of five periods."
)
r_desc = p_desc.add_run(desc_text)
r_desc.font.name = 'Calibri'
r_desc.font.size = Pt(10)
r_desc.font.color.rgb = COLOR_TEXT

# 3. Code Heading
c_head = doc.add_paragraph()
c_head.paragraph_format.space_before = Pt(12)
c_head.paragraph_format.space_after = Pt(2)
c_head.paragraph_format.keep_with_next = True
r_ch = c_head.add_run("MATLAB Implementation Code (exercise_1.m):")
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

highlight_matlab_code_in_cell(c_code, matlab_code)

# 5. Output Heading
out_head = doc.add_paragraph()
out_head.paragraph_format.space_before = Pt(12)
out_head.paragraph_format.space_after = Pt(2)
out_head.paragraph_format.keep_with_next = True
r_oh = out_head.add_run("Simulation Output Plot & Command Window Results:")
r_oh.font.name = 'Calibri'
r_oh.font.size = Pt(10.5)
r_oh.font.bold = True
r_oh.font.color.rgb = COLOR_PRIMARY

# 6. Blank Output Box with dashed border
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
p_box.paragraph_format.space_before = Pt(100)
p_box.paragraph_format.space_after = Pt(100)
r_ph = p_box.add_run("[ Insert Output Plots & Command Window Image Here ]\nUnified Output: Multi-Period Plot, Line Spectra & Percentages")
r_ph.font.name = 'Calibri'
r_ph.font.size = Pt(10.5)
r_ph.font.italic = True
r_ph.font.color.rgb = COLOR_MUTED

doc.add_paragraph().paragraph_format.space_after = Pt(8)

output_filename = "Lab_04_Signals_and_Systems_Report.docx"
doc.save(output_filename)
print(f"Report saved successfully to: {output_filename}")