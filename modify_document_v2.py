#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from copy import deepcopy

def set_cell_font(cell, font_name='宋体', font_size=9):
    """设置表格单元格内所有文本的字体为宋体小5号（9磅）"""
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            run.font.name = font_name
            run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
            run.font.size = Pt(font_size)

def modify_numbering(doc):
    """修改文档的编号定义"""

    # 获取编号部分
    numbering = doc.part.numbering_part
    if numbering is None:
        print("  ⚠ 文档没有编号定义")
        return

    root = numbering.numbering_definitions._element

    # 遍历所有的编号定义
    for abstract_num in root.findall(qn('w:abstractNum')):
        abstract_num_id = abstract_num.get(qn('w:abstractNumId'))

        # 遍历每个层级
        for lvl in abstract_num.findall(qn('w:lvl')):

            lvl_id = lvl.get(qn('w:ilvl'))

            # 获取当前的格式
            num_fmt = lvl.find(qn('w:numFmt'))
            lvl_text = lvl.find(qn('w:lvlText'))

            if num_fmt is not None and lvl_text is not None:
                current_format = num_fmt.get(qn('w:val'))
                current_text = lvl_text.get(qn('w:val'))

                print(f"  找到编号定义 - 抽象ID: {abstract_num_id}, 层级: {lvl_id}")
                print(f"    当前格式: {current_format}, 文本: {current_text}")

                # 根据层级设置不同的格式
                if lvl_id == '0':
                    # 第一层：使用括号 (1)
                    lvl_text.set(qn('w:val'), '(%1)')
                    num_fmt.set(qn('w:val'), 'decimal')
                    print(f"    → 修改为括号格式: (%1)")

                elif lvl_id == '1':
                    # 第二层：使用圆圈数字 ①
                    # Word不支持直接在编号格式中使用圆圈数字
                    # 我们需要使用符号或保持原有格式
                    num_fmt.set(qn('w:val'), 'decimal')
                    # 注意：这里设置为 %1，后面会在文本前添加圆圈符号
                    lvl_text.set(qn('w:val'), '%1')
                    print(f"    → 修改为数字格式: %1")

# 打开文档
doc_path = "/Users/kexiaobin/Downloads/数字工厂概要设计V2.0版.docx"
doc = Document(doc_path)

print("开始处理文档...\n")

# 1. 处理所有表格：设置字体为宋体小5号（9磅）
print("1. 处理表格字体...")
table_count = 0
for table in doc.tables:
    table_count += 1
    for row in table.rows:
        for cell in row.cells:
            set_cell_font(cell, font_name='宋体', font_size=9)

print(f"✓ 已处理 {table_count} 个表格的字体（宋体 小5号）\n")

# 2. 修改编号定义
print("2. 修改编号格式...")
try:
    modify_numbering(doc)
except Exception as e:
    print(f"⚠ 修改编号时出错: {e}")
    print("  将尝试通过段落处理...")

    # 如果编号定义修改失败，则处理段落
    circle_symbols = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩']

    for paragraph in doc.paragraphs:
        pPr = paragraph._element.pPr
        if pPr is not None:
            numPr = pPr.find(qn('w:numPr'))
            if numPr is not None:
                ilvl_elem = numPr.find(qn('w:ilvl'))
                if ilvl_elem is not None:
                    level = int(ilvl_elem.get(qn('w:val')))

                    # 第0层：保持默认（实心点或其他）
                    # 第1层：添加圆圈符号
                    if level == 1:
                        # 在段落文本前添加圆圈符号
                        text = paragraph.text
                        if text and text[0] not in circle_symbols:
                            # 找到编号的位置
                            for run in paragraph.runs:
                                if run.text.strip():
                                    # 检查是否是数字开头
                                    if run.text[0].isdigit():
                                        # 提取数字
                                        match = re.match(r'^(\d+)', run.text)
                                        if match:
                                            num = int(match.group(1)) % 10
                                            symbol = circle_symbols[num]
                                            run.text = symbol + ' ' + run.text[len(match.group(1)):]
                                            break

# 保存文档
output_path = "/Users/kexiaobin/Desktop/其他/claude code/数字工厂概要设计V2.0版-已修改.docx"
doc.save(output_path)

print(f"\n✅ 文档处理完成！")
print(f"📄 保存位置：{output_path}")
print("\n修改内容：")
print("  ✓ 所有表格内字体调整为：宋体 小5号（9磅）")
print("  ✓ 编号格式已调整")
print("\n注意：")
print("  • Word的编号格式可能需要在Word中手动调整")
print("  • 第一层编号已设置为括号格式 (1)")
print("  • 第二层可能需要在Word中手动设置为圆圈数字")
