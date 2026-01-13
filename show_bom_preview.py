#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from docx import Document

# 打开修改后的文档
doc_path = "/Users/kexiaobin/Desktop/其他/claude code/数字工厂设计V2.0-已修改.docx"
doc = Document(doc_path)

print("=" * 60)
print("BOM展开示例预览")
print("=" * 60)
print()

for i, paragraph in enumerate(doc.paragraphs):
    text = paragraph.text.strip()
    if "产品A（1套）" in text and "物料B（2个）" in text:
        print("找到修改后的BOM示例：\n")
        print(text)
        print()
        print("=" * 60)
        print("说明：")
        print("  ✓ 使用树形结构展示BOM层次关系")
        print("  ✓ 清晰显示父子物料关系")
        print("  ✓ 包含MPS计划的需求计算示例")
        print("  ✓ 标注了外购物料")
        print("=" * 60)
        break
