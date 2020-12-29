import os.path
# import io

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Cm, Pt, RGBColor
from docx.enum.table import WD_ALIGN_VERTICAL, WD_ROW_HEIGHT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH_TO_IMG = os.path.join(BASE_DIR, 'static/images/docx')
# PATH_TO_SAVE_FILE = os.path.dirname(BASE_DIR) + '\\test_docx_files'

db_subtotal_data = {
    'Subtotal:': '$880.72',
    'Permit/Filing Free:': '$70.46',
    'General Conditions:': '$44.04',
    'Insurance/Tax:': '$44.04',
    'Overhead:': '$44.04',
    'Profit:': '$44.04',
    'Bond:': '$44.04',
    'Grand Total:': '$1171.38'
}
management_head_list = [
    ('DDB Contracting, LLC', 'management_style_submit'),
    ('Premier Project Management', 'management_style_approve')
]
management_info_list = [f'By{" "*10}', f'Name{" "*4}', f'Date{" "*6}']


def create_docx():
    # export this function to controller
    def write_to_docx(insert=False, cell_paragraph=None, edit_first_paragraph=False, content='', font_name='Arial',
                      font_size=12, font_bold=False, font_italic=False, font_underline=False, color=RGBColor(0, 0, 0),
                      before_spacing=5, after_spacing=5, line_spacing=1.34, keep_together=True, keep_with_next=False,
                      page_break_before=False, widow_control=False, left_indent=None, right_indent=None, align='left',
                      style=''):
        if insert:
            if cell_paragraph:
                font = cell_paragraph.add_run(content)
                paragraph = cell_paragraph
                paragraph_format = cell_paragraph.paragraph_format
            else:
                pass  # put here log_info
        else:
            if cell_paragraph:
                if edit_first_paragraph:
                    paragraph = cell_paragraph.paragraphs[0]
                    cell_paragraph.style = document.styles.add_style(style, WD_STYLE_TYPE.PARAGRAPH)
                    paragraph.text = str(content)
                else:
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

        return paragraph

    # /// Document "margins to all document" block
    document = Document()
    sections = document.sections
    for section in sections:
        section.page_height = Cm(29.7)
        section.page_width = Cm(21.0)
        section.left_margin = Cm(1)
        section.right_margin = Cm(1)
        section.top_margin = Cm(1.34)
        section.bottom_margin = Cm(2.54)
        # section.header_distance = Mm(12.7)
        # section.footer_distance = Mm(12.7)

    # /// endblock

    # ////// Begin to create document
    document.add_picture(f'{PATH_TO_IMG}/logo_pdf.png', width=Cm(6.91), height=Cm(2.64))

    date = document.add_table(rows=1, cols=2)
    row = date.rows[0]
    row.height_rule = WD_ROW_HEIGHT.EXACTLY
    row.height = Pt(15)
    cell = row.cells[1]
    cell.paragraphs[0].clear()
    print(cell.paragraphs, 'cell.paragraphs[0].text', sep='\n')

    paragraph_text = cell.paragraphs[0].add_run(f'{" "*43}05/26/20')
    paragraph_text.bold = True

    table = document.add_table(rows=1, cols=2)
    table.autofit = True
    row = table.rows[0]
    hdr_cells = row.cells
    cell_paragraph_1 = hdr_cells[0].add_paragraph(f'Client{" "*6}')
    write_to_docx(insert=True, cell_paragraph=cell_paragraph_1, content='Client name', font_bold=True)
    cell_paragraph_2 = hdr_cells[1].add_paragraph(f'{" "*24}Project')
    cell_paragraph_2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    write_to_docx(insert=True, cell_paragraph=cell_paragraph_2,
                  content=f'{" "*5}Transaction Window & Sink', font_bold=True)

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

        # row.SetLeftIndent()

    # begin Section A (work_items) block
    document.add_paragraph()
    document.add_picture(f'{PATH_TO_IMG}/Section_A.png', width=Cm(18.99), height=Cm(0.65))
    write_to_docx(
        content='Please find our detailed Quote for the above referenced project as outlined below:',
        font_size=12.5,
        font_bold=True,
        after_spacing=20
    )

    work_item_table = document.add_table(rows=0, cols=3)
    work_item_table.columns[0].width = Cm(10.5)
    work_item_table.columns[1].width = Cm(5.695)
    work_item_table.columns[2].width = Cm(3.18)
    for i in range(1):
        row = work_item_table.add_row()
        row.height_rule = WD_ROW_HEIGHT.AT_LEAST
        row.height = Cm(0.55)
        paragraph_1 = row.cells[0].paragraphs[0]
        paragraph_2 = row.cells[2].paragraphs[0]
        write_to_docx(
            insert=True,
            cell_paragraph=paragraph_2,
            content='$440.36',
            font_size=10.5,
            font_bold=True,
            align='right',
            style='bold_workitem_subtotal'
        )

        write_to_docx(
            insert=True,
            cell_paragraph=paragraph_1,
            content='0.0',
            font_size=10.5,
            font_bold=True,
            style='bold_workitem_id'
        )
        paragraph_1.runs[0].add_tab()
        write_to_docx(
            insert=True,
            cell_paragraph=paragraph_1,
            content='Work Item',
            font_size=10.5,
            font_bold=True,
            style='bold_workitem_name'
        )

    # / bid_subtotal on this section
    bid_subtotal_table = document.add_table(rows=0, cols=3)
    bid_subtotal_table.autofit = False
    bid_subtotal_table.columns[0].width = Cm(10.5)
    bid_subtotal_table.columns[1].width = Cm(5.695)
    bid_subtotal_table.columns[2].width = Cm(3.18)

    for i, j in enumerate(db_subtotal_data):
        row = bid_subtotal_table.add_row()
        row.height_rule = WD_ROW_HEIGHT.AT_LEAST
        row.height = Cm(0.55)
        for cell in row.cells:
            cell.vertical_alignment = WD_ALIGN_VERTICAL.BOTTOM
        cell_1 = row.cells[1]
        cell_1.width = Cm(5.695)  # 2050415
        cell_2 = row.cells[2]
        cell_2.width = Cm(3.18)
        write_to_docx(
            cell_paragraph=cell_1,
            edit_first_paragraph=True,
            content=j,
            font_bold=True,
            font_size=10.5,
            align='left',
            left_indent=Cm(1),
            style=f'bid_data_{j.lower()}'
        )
        write_to_docx(
            cell_paragraph=cell_2,
            edit_first_paragraph=True,
            content=db_subtotal_data[j],
            font_bold=True,
            align='right',
            font_size=10.5,
            style=f'bid_data_{db_subtotal_data[j]}_{i}'
        )

    # begin Section B block
    document.add_picture(f'{PATH_TO_IMG}/Section_B.png', width=Cm(18.99), height=Cm(0.65))
    write_to_docx(
        content='Unless expressly stated, the following exclusions apply:',
        font_size=12.5,
        font_bold=True,
        after_spacing=20,
        style='exclusion_style_heading'
    )

    exclusion_paragraph = write_to_docx(
        content=' ',
        font_size=9.5,
        after_spacing=20,
        style='exclusion_style_first_paraprgaph'
    )
    for i in range(3):
        write_to_docx(
            insert=True,
            cell_paragraph=exclusion_paragraph,
            content=f'Exclusion {i}, ',
            font_size=9.5,
            after_spacing=20,
            style=f'exclusion_style_title_{i}'
        )
    # endblock

    # begin Section C block
    document.add_picture(f'{PATH_TO_IMG}/Section_C.png', width=Cm(18.99), height=Cm(0.65))
    write_to_docx(
        content='Please note the following clarifications:',
        font_size=12.5,
        font_bold=True,
        after_spacing=20,
        style='clarification_style_heading'
    )

    clarification_paragraph = write_to_docx(
        content=' ',
        font_size=9.5,
        after_spacing=10,
        style='clarification_style_first_paraprgaph'
    )
    for i in range(3):
        write_to_docx(
            insert=True,
            cell_paragraph=clarification_paragraph,
            content=f'Clarification {i}, ',
            font_size=9.5,
            style=f'clarification_style_title_{i}'
        )
    # endblock

    # document.add_page_break()

    # begin Section D block
    document.add_picture(f'{PATH_TO_IMG}/Section_D.png', width=Cm(18.99), height=Cm(0.65))
    write_to_docx(
        after_spacing=20,
        style='alternates_style_name'
    )
    # endblock

    # begin Section E_F block
    document.add_picture(f'{PATH_TO_IMG}/Section_E_F.png', width=Cm(18.99), height=Cm(0.79))

    management_table = document.add_table(rows=0, cols=2)
    management_table_row_head = management_table.add_row()
    for i, cell in enumerate(management_table_row_head.cells):
        write_to_docx(
            insert=True,
            content=management_head_list[i][0],
            cell_paragraph=cell.paragraphs[0],
            font_size=10.5,
            font_bold=True,
            align='center',
            after_spacing=20,
            style=management_head_list[i][1]
        )

    for i in range(3):
        management_table_row_info = management_table.add_row()
        for j, cell in enumerate(management_table_row_info.cells):
            paragraph = cell.paragraphs[0]
            write_to_docx(
                insert=True,
                content=management_info_list[i],
                cell_paragraph=paragraph,
                font_size=10,
                before_spacing=5,
                left_indent=Cm(1),
                # style='management'
            )
            paragraph.add_run()
            if i == 1 and j == 0:
                write_to_docx(
                    insert=True,
                    content='Edward Albanese',
                    cell_paragraph=paragraph,
                    font_size=10,
                    before_spacing=5,
                    left_indent=Cm(1)
                    # style='management'
                )
            elif i == 2 and j == 0:
                write_to_docx(
                    insert=True,
                    content='05/26.2020',
                    cell_paragraph=paragraph,
                    font_size=10,
                    before_spacing=5,
                    left_indent=Cm(1)
                    # style='management'
                )
            else:
                paragraph.runs[1].add_picture(f'{PATH_TO_IMG}/underline.png', width=Cm(3.75), height=Cm(0.05))
    # endblock

    document.add_page_break()
