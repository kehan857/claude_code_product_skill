#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zipfile
import os
import re
from html.parser import HTMLParser
import shutil

def modify_html_numbering(html_content):
    """修改HTML中的编号格式"""

    # 1. 将 1.1 改为 1.（仅限h4标题）
    # <h4>1.1 基础信息管理系统定义与目标</h4>
    html_content = re.sub(
        r'<h4>(\d+)\.(\d+)\s+',
        r'<h4>\1. ',
        html_content
    )

    # 2. 将 1.1.1 改为 (1)
    # 需要追踪计数，确保正确排序
    def replace_1_1_1(match):
        number = match.group(1)  # 捕获最后一组数字
        return f'({number}) '

    html_content = re.sub(
        r'<h4>(\d+)\.(\d+)\.(\d+)\s+',
        lambda m: f'<h4>({m.group(3)}) ',
        html_content
    )

    # 3. 处理列表项中的项目符号
    # 将 · 改为 ①②③...
    # 需要在每个ol/ul标签组内独立计数

    # 处理有序列表
    def process_ol_list(match):
        ol_content = match.group(1)
        lines = ol_content.split('<li>')

        counter = 1
        circle_nums = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩',
                       '⑪', '⑫', '⑬', '⑭', '⑮', '⑯', '⑰', '⑱', '⑲', '⑳']

        result = '<ol>'
        for line in lines:
            if line.strip():
                # 移除原有的编号（如果有）
                line = re.sub(r'^\d+\.\s*', '', line.strip())
                # 添加圆圈数字
                circle_num = circle_nums[(counter - 1) % len(circle_nums)]
                result += f'<li>{circle_num} {line}'
                counter += 1

        result += '</ol>'
        return result

    # 处理项目符号列表
    def process_ul_list(match):
        ul_content = match.group(1)
        lines = ul_content.split('<li>')

        counter = 1
        circle_nums = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩',
                       '⑪', '⑫', '⑬', '⑭', '⑮', '⑯', '⑰', '⑱', '⑲', '⑳']

        result = '<ul>'
        for line in lines:
            if line.strip():
                # 移除原有的项目符号（如果有）
                line = re.sub(r'^[•·●○]\s*', '', line.strip())
                # 添加圆圈数字
                circle_num = circle_nums[(counter - 1) % len(circle_nums)]
                result += f'<li>{circle_num} {line}'
                counter += 1

        result += '</ul>'
        return result

    # 应用替换
    html_content = re.sub(
        r'<ol>(.*?)</ol>',
        process_ol_list,
        html_content,
        flags=re.DOTALL
    )

    html_content = re.sub(
        r'<ul>(.*?)</ul>',
        process_ul_list,
        html_content,
        flags=re.DOTALL
    )

    return html_content

# 打开文档
doc_path = "/Users/kexiaobin/Downloads/数字工厂V2.0优化版.docx"
temp_dir = "/tmp/modify_docx"
os.makedirs(temp_dir, exist_ok=True)

# 解压docx
with zipfile.ZipFile(doc_path, 'r') as zip_ref:
    zip_ref.extractall(temp_dir)

# 读取MHT文件
mht_path = os.path.join(temp_dir, "word", "afchunk.mht")
with open(mht_path, 'r', encoding='utf-8') as f:
    mht_content = f.read()

# 提取HTML部分
html_start = mht_content.find('<html>')
html_end = mht_content.find('</html>')

if html_start != -1 and html_end != -1:
    html_part = mht_content[html_start:html_end+7]
    header_part = mht_content[:html_start]
    footer_part = mht_content[html_end+7:]

    # 修改HTML内容
    modified_html = modify_html_numbering(html_part)

    # 重新组合MHT内容
    new_mht_content = header_part + modified_html + footer_part

    # 保存修改后的MHT文件
    with open(mht_path, 'w', encoding='utf-8') as f:
        f.write(new_mht_content)

    print("✓ 已修改编号格式")
    print("  - 1.1 → 1.")
    print("  - 1.1.1 → (1)")
    print("  - • → ①②③...")

# 重新打包为docx
output_path = "/Users/kexiaobin/Desktop/其他/claude code/数字工厂V2.0优化版-已修改.docx"

with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as docx:
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, temp_dir)
            docx.write(file_path, arcname)

print(f"\n✅ 文档修改完成！")
print(f"📄 保存位置：{output_path}")

# 清理临时文件
shutil.rmtree(temp_dir)

# 显示修改示例
print("\n=== 修改示例 ===")
print("修改前: <h4>1.1 基础信息管理系统定义与目标</h4>")
print("修改后: <h4>1. 基础信息管理系统定义与目标</h4>")
print("\n修改前: <h4>1.1.1 子标题</h4>")
print("修改后: <h4>(1) 子标题</h4>")
print("\n修改前: <li>• 第一项</li>")
print("修改后: <li>① 第一项</li>")
