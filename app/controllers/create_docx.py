import os
# from io import StringIO
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Cm, Pt, RGBColor
from docx.enum.table import WD_ROW_HEIGHT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH_TO_IMG = os.path.join(BASE_DIR, "static/images/docx/")


def create_docx():
    # /// Document "margins to all document" block

    # with open('foobar.docx', 'rb') as f:
    #     source_stream = StringIO(f.read())
    # document = Document(source_stream)
    # source_stream.close()

    document = Document()
    sections = document.sections
    for section in sections:
        section.top_margin = Cm(1.34)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(0.99)
        section.right_margin = Cm(1.02)

    # export this function to controller
    def write_to_docx(insert=False, cell=None, content='', font_name='Arial', font_size=12, font_bold=False,
                      font_underline=False, color=RGBColor(0, 0, 0), font_italic=False,
                      before_spacing=5, after_spacing=5, line_spacing=1.34, keep_together=True, keep_with_next=False,
                      page_break_before=False, widow_control=False, align='left', style=''):
        '''
        parametr 'cell' is not the _cell Object, but paragraph Object!
        '''

        if insert:
            font = cell.add_run(content)
        else:
            paragraph = document.add_paragraph(str(content))
            paragraph.style = document.styles.add_style(style, WD_STYLE_TYPE.PARAGRAPH)
            font = paragraph.style.font
            paragraph_format = paragraph.paragraph_format
            paragraph_format.space_before = Pt(before_spacing)
            paragraph_format.space_after = Pt(after_spacing)
            paragraph.line_spacing = line_spacing
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

    # ////// Begin to create document
    document.add_picture(f'{PATH_TO_IMG}logo_pdf.png', width=Cm(6.91), height=Cm(2.64))

    date = document.add_table(rows=1, cols=2)
    row = date.rows[0]
    row.height_rule = WD_ROW_HEIGHT.EXACTLY
    row.height = Pt(15)
    cell = row.cells[1]
    cell.paragraphs[0].clear()

    paragraph_text = cell.paragraphs[0].add_run(f'{" "*43}05/26/20')
    paragraph_text.bold = True

    table = document.add_table(rows=1, cols=2)
    table.autofit = True
    row = table.rows[0]
    hdr_cells = row.cells
    cell_1 = hdr_cells[0].add_paragraph(f'Client{" "*6}')
    write_to_docx(insert=True, cell=cell_1, content='Client name', font_bold=True)
    cell_2 = hdr_cells[1].add_paragraph(f'{" "*24}Project')
    cell_2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    write_to_docx(insert=True, cell=cell_2, content=f'{" "*5}Transaction Window & Sink', font_bold=True)

    for i in range(4):
        row = table.add_row()
        row.height_rule = WD_ROW_HEIGHT.EXACTLY
        row.height = Pt(15)
        row.cells[0].text = f'{" "*17}75 Montgomery'
        paragraph = row.cells[1].paragraphs[0]
        paragraph.text = f'{" "*43}right_cell'
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        if i == 3:
            paragraph.runs[0].text = f'{" "*43}'
            paragraph.add_run('Quote # B-20-034 R1')
            paragraph.runs[1].font.highlight_color = WD_COLOR_INDEX.YELLOW

    document.add_paragraph()
    document.add_picture(f'{PATH_TO_IMG}Section_A.png', width=Cm(18.99), height=Cm(0.65))
    write_to_docx(
        content='Please find our detailed Quote for the above referenced project as outlined below:',
        font_name='Arial',
        font_size=11.5,
        font_bold=True,
        after_spacing=50
    )
    document.add_picture(f'{PATH_TO_IMG}Section_B.png', width=Cm(18.99), height=Cm(0.65))
    write_to_docx(
        content='Unless expressly stated, the following exclusions apply:',
        font_name='Arial',
        font_size=11.5,
        font_bold=True,
        after_spacing=50,
        style='exclusion_style_name'
    )
    document.add_picture(f'{PATH_TO_IMG}Section_C.png', width=Cm(18.99), height=Cm(0.65))
    write_to_docx(
        content='Please note the following clarifications:',
        font_name='Arial',
        font_size=11.5,
        font_bold=True,
        after_spacing=50,
        style='clarification_style_name'
    )
    document.add_picture(f'{PATH_TO_IMG}Section_D.png', width=Cm(18.99), height=Cm(0.65))
    write_to_docx(
        after_spacing=50,
        style='alternates_style_name'
    )
    document.add_picture(f'{PATH_TO_IMG}Section_E_F.png', width=Cm(18.99), height=Cm(0.79))

    document.add_page_break()
    # target_stream = StringIO()
    document.save('test_docx.docx')
