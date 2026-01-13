#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

# 添加skill目录到Python路径
skill_dir = Path.home() / ".claude" / "skills" / "ui-design-pro"
sys.path.insert(0, str(skill_dir))

from search import UIDesignSearch
import json

def test_search():
    """测试搜索功能"""
    print("=" * 80)
    print("测试1：搜索功能")
    print("=" * 80)

    searcher = UIDesignSearch()
    keywords = ["saas", "dashboard", "modern"]
    results = searcher.search_by_keywords(keywords)

    print(f"\n搜索关键词：{', '.join(keywords)}")
    print(f"\n找到结果：")
    for category, items in results.items():
        if items:
            print(f"\n{category.upper()}: {len(items)}个结果")
            for item in items[:3]:
                print(f"  - {item.get('name')}")

def test_recommendation():
    """测试推荐功能"""
    print("\n" + "=" * 80)
    print("测试2：智能推荐")
    print("=" * 80)

    searcher = UIDesignSearch()

    project_types = ["saas", "ecommerce", "dashboard"]

    for project_type in project_types:
        print(f"\n项目类型：{project_type}")
        design_system = searcher.generate_design_system(project_type)

        print(f"  UI样式：{design_system.get('ui_style', {}).get('name')}")
        print(f"  配色：{design_system.get('color_palette', {}).get('name')}")
        print(f"  字体：{design_system.get('typography', {}).get('name')}")

def test_database_loading():
    """测试数据库加载"""
    print("\n" + "=" * 80)
    print("测试3：数据库加载")
    print("=" * 80)

    searcher = UIDesignSearch()

    print(f"\n✓ UI样式：{sum(len(styles) for styles in searcher.ui_styles.get('ui_styles', {}).values())}种")
    print(f"✓ 配色方案：{sum(len(palettes) for palettes in searcher.color_palettes.get('color_palettes', {}).values())}个")
    print(f"✓ 字体配对：{len(searcher.typography.get('font_pairings', {}))}种")
    print(f"✓ 组件：{sum(len(components) for components in searcher.components.get('components', {}).values())}个")
    print(f"✓ UX指南：{sum(len(guides) for guides in searcher.ux_guidelines.get('ux_guidelines', {}).values())}条")

def generate_sample_design_system():
    """生成示例设计系统"""
    print("\n" + "=" * 80)
    print("测试4：生成完整设计系统")
    print("=" * 80)

    searcher = UIDesignSearch()
    design_system = searcher.generate_design_system("saas", "html")

    # 保存到文件
    output_path = Path.home() / "Desktop" / "其他" / "claude code" / "sample_design_system.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(design_system, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 示例设计系统已生成：{output_path}")
    print(f"\n设计系统包含：")
    print(f"  - UI样式：{design_system.get('ui_style', {}).get('name')}")
    print(f"  - 配色方案：{design_system.get('color_palette', {}).get('name')}")
    print(f"  - 字体系统：{design_system.get('typography', {}).get('name')}")
    print(f"  - 推荐组件：{len(design_system.get('components', []))}个")
    print(f"  - UX指南：{len(design_system.get('ux_guidelines', []))}条")

def main():
    """主函数"""
    try:
        test_database_loading()
        test_search()
        test_recommendation()
        generate_sample_design_system()

        print("\n" + "=" * 80)
        print("✅ 所有测试通过！")
        print("=" * 80)
        print("\n使用方法：")
        print("1. CLI工具：python3 ~/.claude/skills/ui-design-pro/ui-cli.py")
        print("2. 搜索脚本：python3 ~/.claude/skills/ui-design-pro/search.py <关键词>")
        print("3. 在Claude Code中直接使用skill")

    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
