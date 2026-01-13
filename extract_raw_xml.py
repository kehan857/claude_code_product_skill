#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from docx.oxml import parse_xml
from docx import Document
import zipfile
import os

# 打开文档
doc_path = "/Users/kexiaobin/Downloads/数字工厂V2.0优化版.docx"

# 解压docx文件
temp_dir = "/tmp/extracted_docx"
if os.path.exists(temp_dir):
    import shutil
    shutil.rmtree(temp_dir)

os.makedirs(temp_dir, exist_ok=True)

with zipfile.ZipFile(doc_path, 'r') as zip_ref:
    zip_ref.extractall(temp_dir)

# 读取document.xml
document_xml_path = os.path.join(temp_dir, "word", "document.xml")

with open(document_xml_path, 'rb') as f:
    content = f.read()

# 尝试解码
try:
    text = content.decode('utf-8')
except:
    text = content.decode('gbk')

# 查找文本内容
print("=== 文档内容预览 ===\n")

# 提取所有<w:t>标签中的文本
import re
text_tags = re.findall(r'<w:t[^>]*>([^<]*)</w:t>', text)

print(f"找到 {len(text_tags)} 个文本标签\n")

# 显示前50个文本片段
for i, txt in enumerate(text_tags[:50]):
    if txt.strip():
        print(f"{i+1}. {txt}")

# 清理临时文件
import shutil
shutil.rmtree(temp_dir)
