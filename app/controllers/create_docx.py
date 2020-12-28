import os.path
import io
from random import randint

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Inches, Cm, Pt, RGBColor, Mm
from docx.enum.table import WD_ALIGN_VERTICAL, WD_ROW_HEIGHT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX

# /// Document "margins to all document" block
document = Document()
sections = document.sections
for section in sections:
    section.page_height = Mm(297)
    section.page_width = Mm(210)
    section.left_margin = Cm(1)
    section.right_margin = Cm(1)
    section.top_margin = Cm(1.34)
    section.bottom_margin = Cm(2.54)
    # section.header_distance = Mm(12.7)
    # section.footer_distance = Mm(12.7) 

# document = Document()
# section = document.sections[0]
# section.left_margin = Cm(1)
# section.right_margin = Cm(1)
# section.top_margin = Mm(25.4)
# section.bottom_margin = Mm(25.4)
# section.header_distance = Mm(12.7)
# section.footer_distance = Mm(12.7)
 
# /// endblock

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_TO_IMG = BASE_DIR + '\images'
PATH_TO_SAVE_FILE = os.path.dirname(BASE_DIR) + '\\test_docx_files'
print(PATH_TO_IMG, PATH_TO_SAVE_FILE, os.path, sep='\n\n')

# IMG = os.path.join(BASE_DIR, '\images')???


# export this function to controller
def write_to_docx(insert=False, cell_paragraph=None, content='', font_name='Arial', font_size=12, font_bold=False, font_italic=False, font_underline=False, color = RGBColor(0, 0, 0),
                  before_spacing=5, after_spacing=5, line_spacing=1.34, keep_together=True, keep_with_next=False, page_break_before=False,
                  widow_control=False, left_indent=None, right_indent=None, align='left', style=''):
    '''
    parametr 'cell_paragraph' is not the _cell Object, but paragraph Object!
    '''

    if insert:
        font = cell_paragraph.add_run(content)
        paragraph = cell_paragraph
        paragraph_format = cell_paragraph.paragraph_format
    else:
        if cell_paragraph:
            paragraph = cell_paragraph.add_paragraph(str(content))
        else:
            paragraph = document.add_paragraph(str(content))
        paragraph.style = document.styles.add_style(style, WD_STYLE_TYPE.PARAGRAPH)
        font = paragraph.style.font
        paragraph_format = paragraph.paragraph_format

    paragraph_format.left_indent = left_indent
    paragraph_format.right_indent = right_indent
    paragraph_format.space_before = Pt(before_spacing)
    paragraph_format.space_after = Pt(after_spacing)
    paragraph_format.line_spacing = line_spacing
    paragraph_format.keep_together = keep_together
    paragraph_format.keep_with_next = keep_with_next
    paragraph_format.page_break_before = page_break_before
    paragraph_format.widow_control = widow_control

    if align.lower() == 'left':
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    elif align.lower() == 'center':
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align.lower() == 'right':
        paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    elif align.lower() == 'justify':
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    else:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT

    font.name = font_name
    font.size = Pt(font_size)
    font.bold = font_bold
    font.italic = font_italic
    font.underline = font_underline

    if not insert:
        font.color.rgb = color

# /// endblock
print(BASE_DIR, PATH_TO_IMG, sep='\n')

# ////// Begin to create document
document.add_picture(f'{PATH_TO_IMG}\logo_pdf.png', width=Cm(6.91), height=Cm(2.64))

date = document.add_table(rows=1, cols=2)
row = date.rows[0]
row.height_rule = WD_ROW_HEIGHT.EXACTLY
row.height = Pt(15)
cell = row.cells[1]
cell.paragraphs[0].clear()
print(cell.paragraphs, 'cell.paragraphs[0].text', sep='\n')

paragraph_text = cell.paragraphs[0].add_run(f'{" "*43}05/26/20')
paragraph_text.bold = True

# paragraph.alignment=WD_ALIGN_PARAGRAPH.LEFT
# paragraph.style = document.styles.add_style("Style Name", WD_STYLE_TYPE.PARAGRAPH)
# font = paragraph.style.font
# font.bold = True

table = document.add_table(rows=1, cols=2)
table.autofit = True
row = table.rows[0]
hdr_cells = row.cells
cell_paragraph_1 = hdr_cells[0].add_paragraph(f'Client{" "*6}')
write_to_docx(insert=True, cell_paragraph=cell_paragraph_1, content='Client name', font_bold=True)
cell_paragraph_2 = hdr_cells[1].add_paragraph(f'{" "*24}Project')
cell_paragraph_2.alignment=WD_ALIGN_PARAGRAPH.LEFT
write_to_docx(insert=True, cell_paragraph=cell_paragraph_2, content=f'{" "*5}Transaction Window & Sink', font_bold=True)

for i in range(4):
    row = table.add_row()
    row.height_rule = WD_ROW_HEIGHT.EXACTLY
    row.height = Pt(15)
    row.cells[0].text = f'{" "*17}75 Montgomery'
    paragraph = row.cells[1].paragraphs[0]
    paragraph.text = f'{" "*43}right_cell'
    paragraph.alignment=WD_ALIGN_PARAGRAPH.LEFT
    if i == 3:
        paragraph.runs[0].text = f'{" "*43}'
        paragraph.add_run('Quote # B-20-034 R1')
        paragraph.runs[1].font.highlight_color = WD_COLOR_INDEX.YELLOW
        # print(paragraph.runs, paragraph.runs[1].text, sep='\n')
    # row.SetLeftIndent()

# begin Section A (work_items) block
document.add_paragraph()
document.add_picture(f'{PATH_TO_IMG}\Section_A.png', width=Cm(18.99), height=Cm(0.65))
write_to_docx(
    content='Please find our detailed Quote for the above referenced project as outlined below:',
    font_size=12.5,
    font_bold = True,
    after_spacing = 20
    )

work_item_table = document.add_table(rows=0, cols=3)

for i in range(1):
    row = work_item_table.add_row()
    row.height_rule = WD_ROW_HEIGHT.AT_LEAST
    row.height = Cm(0.55)
    for i, cell in enumerate(row.cells):
        if i == 2:
            write_to_docx(
                insert=True,
                cell_paragraph=cell.paragraphs[0],
                content='$440.36',
                font_size=10.5,
                font_bold=True,
                right_indent=Cm(0.65),
                align='right',
                style='bold_workitem_subtotal'
            )
            paragraph_format = cell.paragraphs[0].paragraph_format
        else:    
            write_to_docx(
                insert=True,
                cell_paragraph=cell.paragraphs[0],
                content='0.0',
                font_size=10.5,
                font_bold=True,
                style='bold_workitem'
            )
        print(cell.paragraphs[0].runs[0].text)


# / bid_subtotal on this section
bid_subtotal_table = document.add_table(rows=0, cols=3)
for i, column in enumerate(bid_subtotal_table.columns): 
    if i == 1:
        column.width = Cm(5.695)
    elif i == 2:
        column.width = Cm(2.805)
    else:
        column.width = Cm(10.5)

db = {
    'Subtotal:': '$880.72',
    'Permit/Filing Free:': '$70.46',
    'General Conditions:': '$44.04',
    'Insurance/Tax:': '$44.04',
    'Overhead:': '$44.04',
    'Profit:': '$44.04',
    'Bond:': '$44.04',
    'Grand Total:': '$1171.38'
}

for i, j in enumerate(db):
    bid_subtotal_table.add_row()
    cell_paragraph_1 = bid_subtotal_table.columns[1].cells[i]
    cell_paragraph_2 = bid_subtotal_table.columns[2].cells[i]
    write_to_docx(
        cell_paragraph=cell_paragraph_1,
        content=j,
        font_bold = True,
        font_size=10.5,
        align='left',
        left_indent=Cm(3),
        style=f'bid_data_{j.lower()}'
    )
    write_to_docx(
        cell_paragraph=cell_paragraph_2,
        content=db[j],
        font_bold = True,
        align='right',
        font_size=10.5,
        style=f'bid_data_{db[j]}_{i}'
    )

for column in bid_subtotal_table.columns:  
    print(column.cells[0])
print(3420110, bid_subtotal_table.columns[0].width)
print(
     f'This is the first column width: {bid_subtotal_table.columns[0].width}',
     f'This is the second column width: {bid_subtotal_table.columns[1].width}',
     sep='\n'
    )


# Section B
document.add_picture(f'{PATH_TO_IMG}\Section_B.png', width=Cm(18.99), height=Cm(0.65))
write_to_docx(
    content='Unless expressly stated, the following exclusions apply:',
    font_size=12.5,
    font_bold = True,
    after_spacing = 50,
    style='exclusion_style_name'
    )
document.add_picture(f'{PATH_TO_IMG}\Section_C.png', width=Cm(18.99), height=Cm(0.65))
write_to_docx(
    content='Please note the following clarifications:',
    font_size=12.5,
    font_bold = True,
    after_spacing = 50,
    style='clarification_style_name'
    )
document.add_picture(f'{PATH_TO_IMG}\Section_D.png', width=Cm(18.99), height=Cm(0.65))
write_to_docx(
    after_spacing = 50,
    style='alternates_style_name'
    )
document.add_picture(f'{PATH_TO_IMG}\Section_E_F.png', width=Cm(18.99), height=Cm(0.79))

document.add_page_break()
