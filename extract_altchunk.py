#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from docx import Document
from docx.oxml import register_element_cls
from docx.oxml.ns import qn
import zipfile
import os
import re

# 打开文档
doc_path = "/Users/kexiaobin/Downloads/数字工厂V2.0优化版.docx"

# 解压docx文件（它实际上是个zip）
temp_dir = "/tmp/extracted_docx"
os.makedirs(temp_dir, exist_ok=True)

with zipfile.ZipFile(doc_path, 'r') as zip_ref:
    zip_ref.extractall(temp_dir)

# 查找document.xml
document_xml_path = os.path.join(temp_dir, "word", "document.xml")

# 读取并显示内容
with open(document_xml_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("=== 查找 altChunk 内容 ===\n")

# 查找altChunk标签
import xml.etree.ElementTree as ET

# 移除命名空间以简化处理
content_clean = re.sub(r'xmlns[^"]*"[^"]*"', '', content)

# 查找所有altChunk
alt_chunks = re.findall(r'<w:altChunk[^>]*>.*?</w:altChunk>', content_clean, re.DOTALL)

print(f"找到 {len(alt_chunks)} 个 altChunk")

if alt_chunks:
    for i, chunk in enumerate(alt_chunks):
        # 提取r:id属性
        rid_match = re.search(r'r:id="([^"]*)"', chunk)
        if rid_match:
            rid = rid_match.group(1)
            print(f"\nAltChunk {i+1} - r:id = {rid}")

            # 查找对应的嵌入文件
            # 在relationships中查找
            rels_path = os.path.join(temp_dir, "word", "_rels", "document.xml.rels")
            if os.path.exists(rels_path):
                with open(rels_path, 'r', encoding='utf-8') as f:
                    rels_content = f.read()

                # 查找对应的relationship
                rel_match = re.search(f'<Relationship Id="{rid}"[^>]*Target="([^"]*)"', rels_content)
                if rel_match:
                    target = rel_match.group(1)
                    print(f"  目标文件: {target}")

                    # 如果是嵌入的HTML或XML，尝试读取
                    if target.startswith('http'):
                        print(f"  外部链接: {target}")
                    else:
                        # 尝试读取嵌入文件
                        embed_path = os.path.join(temp_dir, "word", target)
                        if os.path.exists(embed_path):
                            with open(embed_path, 'r', encoding='utf-8') as embed_file:
                                embed_content = embed_file.read()

                            # 显示前500个字符
                            print(f"  内容预览:\n{embed_content[:500]}...")

# 清理临时文件
import shutil
shutil.rmtree(temp_dir)
