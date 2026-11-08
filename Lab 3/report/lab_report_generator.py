import os
import json
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import re

# ==========================================
# CONFIGURATION
# ==========================================
# Set the target folder path containing the report.json and MATLAB (.m) files.
# Use raw string (r"...") or forward slashes to avoid escape character issues.
LAB_FOLDER_PATH = r"./"  # Default to current directory. Update this path!
JSON_FILENAME = os.path.join(LAB_FOLDER_PATH, "report", "report.json")
OUTPUT_FILENAME = "Final_Lab_Report_3.docx"

# ==========================================
# STYLE DEFINITIONS
# ==========================================
COLOR_PRIMARY = RGBColor(0, 51, 102)     # Deep Navy
COLOR_SECONDARY = RGBColor(70, 130, 180) # Steel Blue
COLOR_TEXT = RGBColor(40, 40, 40)        # Charcoal
COLOR_MUTED = RGBColor(120, 120, 120)    # Gray
HEX_PRIMARY_BG = "EBF3FA"
HEX_CODE_BG = "F8F9FA"
HEX_BOX_BG = "FAFAFA"
HEX_ANSWER_BG = "F0F7F4"                 # Soft Green for answers

def set_cell_background(cell, fill_hex):
    """Sets the background color of a table cell."""
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets the internal margins of a table cell."""
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
    """Sets individual borders for a table cell."""
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

# ==========================================
# SYNTAX HIGHLIGHTING
# ==========================================
KEYWORDS = {
    'clc', 'clear', 'close', 'all', 'hold', 'on', 'off', 'grid', 'figure', 
    'if', 'else', 'elseif', 'end', 'for', 'while', 'return', 'function',
    'table', 'fitlm', 'predict', 'optimset', 'lsqcurvefit'
}
BUILTINS = {
    'linspace', 'cos', 'sin', 'exp', 'stem', 'plot', 'xlabel', 'ylabel', 
    'title', 'legend', 'subplot', 'sgtitle', 'xlim', 'ylim', 'ones', 
    'size', 'ceil', 'floor', 'double', 'abs', 'real', 'imag', 'trapz', 
    'fprintf', 'max', 'isfinite', 'filter', 'conv', 'length', 'zeros', 'pi',
    'disp', 'corrcoef', 'scatter', 'sqrt', 'mean', 'sum', 'min'
}

def highlight_matlab_code_in_cell(cell, code_text):
    """Parses MATLAB code and applies colored formatting run-by-run."""
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
        
        # Tokenizer regex
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

# ==========================================
# MAIN GENERATOR FUNCTION
# ==========================================
def generate_report():
    print(f"Starting report generation from folder: {LAB_FOLDER_PATH}")
    
    # Check if JSON exists
    json_path = os.path.join(LAB_FOLDER_PATH, JSON_FILENAME)
    if not os.path.exists(json_path):
        print(f"Error: Could not find '{JSON_FILENAME}' in '{LAB_FOLDER_PATH}'")
        print("Please create the JSON file and specify the correct folder path.")
        return

    # Load data
    with open(json_path, 'r', encoding='utf-8') as f:
        exercises = json.load(f)

    doc = docx.Document()

    # Page setup - Margins (0.8 inches on all sides)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    header_p = doc.add_paragraph()
    header_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    header_p.paragraph_format.space_after = Pt(2)
    run_sub = header_p.add_run("DEPARTMENT OF AVIONICS ENGINEERING\nLABORATORY REPORT")
    run_sub.font.name = 'Calibri'
    run_sub.font.size = Pt(11)
    run_sub.font.bold = True
    run_sub.font.color.rgb = COLOR_SECONDARY

    # Add a generic title (can be customized later or pulled from JSON metadata if added)
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_after = Pt(16)
    run_title = title_p.add_run("Automated Laboratory Submission")
    run_title.font.name = 'Calibri'
    run_title.font.size = Pt(18)
    run_title.font.bold = True
    run_title.font.color.rgb = COLOR_PRIMARY

    info_table = doc.add_table(rows=2, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_table.autofit = False

    info_data = [
        [("Course Code & Title:", " ______________________"), ("Date of Performance:", " ______________________")],
        [("Lab Title:", " ______________________"), ("Student Name / ID:", " ______________________")]
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

    for ex in exercises:
        ex_num = ex.get("num", "Exercise")
        ex_title = ex.get("title", "Untitled Problem")
        
        # 1. Heading
        h_p = doc.add_paragraph()
        h_p.paragraph_format.space_before = Pt(14)
        h_p.paragraph_format.space_after = Pt(2)
        h_p.paragraph_format.keep_with_next = True
        
        r_num = h_p.add_run(f"{ex_num}: ")
        r_num.font.name = 'Calibri'
        r_num.font.size = Pt(13)
        r_num.font.bold = True
        r_num.font.color.rgb = COLOR_PRIMARY
        
        r_t = h_p.add_run(ex_title)
        r_t.font.name = 'Calibri'
        r_t.font.size = Pt(13)
        r_t.font.bold = True
        r_t.font.color.rgb = COLOR_SECONDARY

        has_details = "details" in ex and ex["details"].strip()
        has_bullets = "bullets" in ex and isinstance(ex["bullets"], list) and len(ex["bullets"]) > 0
        
        if has_details or has_bullets:
            # Problem Statement Box
            desc_table = doc.add_table(rows=1, cols=1)
            desc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
            desc_table.autofit = False
            c_desc = desc_table.rows[0].cells[0]
            c_desc.width = Inches(6.8)
            set_cell_background(c_desc, HEX_PRIMARY_BG)
            set_cell_margins(c_desc, top=80, bottom=80, left=120, right=120)
            set_cell_borders(c_desc, left="single", color="003366", sz="18")
            
            if has_details:
                p_desc = c_desc.paragraphs[0]
                p_desc.paragraph_format.space_after = Pt(4) if has_bullets else Pt(0)
                p_desc.paragraph_format.line_spacing = Pt(13)
                r_desc = p_desc.add_run(ex["details"])
                r_desc.font.name = 'Calibri'
                r_desc.font.size = Pt(10)
                r_desc.font.color.rgb = COLOR_TEXT

            if has_bullets:
                for idx, bullet in enumerate(ex["bullets"]):
                    # If details were omitted, we need to populate the first paragraph instead of adding a new one
                    if not has_details and idx == 0:
                        p_bull = c_desc.paragraphs[0]
                    else:
                        p_bull = c_desc.add_paragraph()
                    
                    p_bull.style = 'List Bullet'
                    p_bull.paragraph_format.space_after = Pt(2)
                    p_bull.paragraph_format.line_spacing = Pt(13)
                    
                    # Hack for docx list bullet indent inside tables
                    p_bull.paragraph_format.left_indent = Inches(0.25)
                    
                    r_bull = p_bull.add_run(bullet)
                    r_bull.font.name = 'Calibri'
                    r_bull.font.size = Pt(10)
                    r_bull.font.color.rgb = COLOR_TEXT

        matlab_file = ex.get("matlab_file")
        if matlab_file:
            m_path = os.path.join(LAB_FOLDER_PATH, matlab_file)
            
            code_text = ""
            if os.path.exists(m_path):
                with open(m_path, 'r', encoding='utf-8') as mf:
                    code_text = mf.read()
            else:
                code_text = f"% WARNING: File '{matlab_file}' not found in '{LAB_FOLDER_PATH}'\n% Please check your configuration."

            # Code Heading
            c_head = doc.add_paragraph()
            c_head.paragraph_format.space_before = Pt(8)
            c_head.paragraph_format.space_after = Pt(2)
            c_head.paragraph_format.keep_with_next = True
            r_ch = c_head.add_run(f"MATLAB Implementation ({matlab_file}):")
            r_ch.font.name = 'Calibri'
            r_ch.font.size = Pt(10.5)
            r_ch.font.bold = True
            r_ch.font.color.rgb = COLOR_PRIMARY

            # Code Block with Syntax Highlighting
            code_table = doc.add_table(rows=1, cols=1)
            code_table.alignment = WD_TABLE_ALIGNMENT.CENTER
            code_table.autofit = False
            c_code = code_table.rows[0].cells[0]
            c_code.width = Inches(6.8)
            set_cell_background(c_code, HEX_CODE_BG)
            set_cell_margins(c_code, top=100, bottom=100, left=120, right=120)
            set_cell_borders(c_code, top="single", bottom="single", left="single", right="single", color="D0D5DD", sz="4")
            
            highlight_matlab_code_in_cell(c_code, code_text)

        if "answers" in ex and ex["answers"].strip():
            ans_head = doc.add_paragraph()
            ans_head.paragraph_format.space_before = Pt(8)
            ans_head.paragraph_format.space_after = Pt(2)
            r_ah = ans_head.add_run("Analytical Answers / Results:")
            r_ah.font.name = 'Calibri'
            r_ah.font.size = Pt(10.5)
            r_ah.font.bold = True
            r_ah.font.color.rgb = COLOR_PRIMARY

            ans_table = doc.add_table(rows=1, cols=1)
            ans_table.alignment = WD_TABLE_ALIGNMENT.CENTER
            ans_table.autofit = False
            c_ans = ans_table.rows[0].cells[0]
            c_ans.width = Inches(6.8)
            set_cell_background(c_ans, HEX_ANSWER_BG)
            set_cell_margins(c_ans, top=80, bottom=80, left=120, right=120)
            set_cell_borders(c_ans, left="single", color="3C887E", sz="12")
            
            p_ans = c_ans.paragraphs[0]
            p_ans.paragraph_format.space_after = Pt(0)
            p_ans.paragraph_format.line_spacing = Pt(13)
            r_ans = p_ans.add_run(ex["answers"])
            r_ans.font.name = 'Calibri'
            r_ans.font.size = Pt(10)
            r_ans.font.color.rgb = COLOR_TEXT

        out_head = doc.add_paragraph()
        out_head.paragraph_format.space_before = Pt(8)
        out_head.paragraph_format.space_after = Pt(2)
        out_head.paragraph_format.keep_with_next = True
        r_oh = out_head.add_run("Simulation Output Plot:")
        r_oh.font.name = 'Calibri'
        r_oh.font.size = Pt(10.5)
        r_oh.font.bold = True
        r_oh.font.color.rgb = COLOR_PRIMARY

        # Blank Output Box
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
        
        out_lbl = ex.get("output_label", f"Output for {ex_num}")
        r_ph = p_box.add_run(f"[ Insert Output Plot Image Here ]\n{out_lbl}")
        r_ph.font.name = 'Calibri'
        r_ph.font.size = Pt(10.5)
        r_ph.font.italic = True
        r_ph.font.color.rgb = COLOR_MUTED

        # Spacer between problems
        spacer = doc.add_paragraph()
        spacer.paragraph_format.space_after = Pt(12)

    final_out_path = os.path.join(LAB_FOLDER_PATH, "report",OUTPUT_FILENAME)
    doc.save(final_out_path)
    print(f"\nSuccess! Document saved to: {final_out_path}")

if __name__ == "__main__":
    generate_report()