#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from playwright.sync_api import sync_playwright
import json
import time

def extract_feishu_form(url):
    """提取飞书表单的内容"""

    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=False)  # headless=False 可以看到浏览器操作
        page = browser.new_page()

        print(f"正在访问: {url}")
        page.goto(url, wait_until="networkidle", timeout=30000)

        # 等待页面加载
        time.sleep(3)

        # 尝试提取表单内容
        form_data = []

        try:
            # 方法1: 尝试查找表单字段
            # 飞书表单通常使用特定的class名称
            fields = page.query_selector_all("[class*='field'], [class*='form'], [class*='item']")

            print(f"\n找到 {len(fields)} 个可能字段")

            # 提取页面文本内容
            page_text = page.inner_text("body")

            print("\n=== 页面文本内容 ===")
            print(page_text[:2000])  # 打印前2000字符

            # 尝试提取所有文本节点
            all_text = page.evaluate("""
                () => {
                    // 获取所有文本内容
                    const body = document.body;
                    const walker = document.createTreeWalker(
                        body,
                        NodeFilter.SHOW_TEXT,
                        null,
                        false
                    );

                    let textNodes = [];
                    let node;
                    while(node = walker.nextNode()) {
                        const text = node.textContent.trim();
                        if(text.length > 0) {
                            textNodes.push(text);
                        }
                    }
                    return textNodes;
                }
            """)

            print("\n=== 提取的文本节点 ===")
            for i, text in enumerate(all_text[:50]):  # 只打印前50个
                print(f"{i+1}. {text}")

            # 保存到文件
            output_file = "/Users/kexiaobin/Desktop/其他/claude code/form_data.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({
                    "url": url,
                    "page_title": page.title(),
                    "all_text": all_text,
                    "page_html": page.content()
                }, f, ensure_ascii=False, indent=2)

            print(f"\n✅ 数据已保存到: {output_file}")

        except Exception as e:
            print(f"❌ 提取出错: {e}")

        # 等待一段时间以便查看
        print("\n浏览器将在5秒后关闭...")
        time.sleep(5)

        browser.close()
        return all_text

if __name__ == "__main__":
    url = "https://bytedance.larkoffice.com/share/base/form/shrcnYLnkkzKj7i0Gr1ZD67t9ie"
    extract_feishu_form(url)
