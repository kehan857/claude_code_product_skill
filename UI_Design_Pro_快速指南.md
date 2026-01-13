# UI Design Pro - 快速开始指南

## 🎯 三种使用方式

### 方式1：CLI交互工具（最简单）

```bash
python3 ~/.claude/skills/ui-design-pro/ui-cli.py
```

你会看到：
```
╔════════════════════════════════════════════════════════════╗
║                                                              ║
║   UI Design Pro - 专业UI/UX设计智能助手                      ║
║   Design Intelligence for Modern Web Applications           ║
║                                                              ║
╚════════════════════════════════════════════════════════════╝

请选择操作：

1. 🔍 搜索设计资源
2. 📊 生成设计系统
3. 🎨 查看配色方案
4. ✨ 查看UI样式
5. 🔤 查看字体配对
6. 📦 查看组件库
7. 📖 查看UX指南
8. 💡 获取推荐
0. 退出
```

### 方式2：命令行搜索

```bash
# 搜索特定关键词
python3 ~/.claude/skills/ui-design-pro/search.py saas dashboard

# 搜索配色
python3 ~/.claude/skills/ui-design-pro/search.py blue gradient

# 搜索字体
python3 ~/.claude/skills/ui-design-pro/search.py modern serif
```

### 方式3：在Claude Code中使用（推荐）

直接在对话中说：
- "创建一个现代SaaS登录页面"
- "设计一个电商仪表盘"
- "构建一个作品集网站"

我会自动调用UI Design Pro skill！

## 📊 快速示例

### 示例1：为SaaS项目生成设计系统

```bash
# 1. 打开CLI工具
python3 ~/.claude/skills/ui-design-pro/ui-cli.py

# 2. 选择 2. 生成设计系统
# 3. 选择项目类型 1. SaaS
# 4. 输入技术栈（默认html）

# 输出：
设计系统 - SAAS
技术栈：html

## UI样式
**Glassmorphism**
毛玻璃效果，半透明背景配合模糊

## 配色方案
**Professional Blue**
- 主色：#2563eb
- 次色：#3b82f6
- 强调色：#60a5fa
- 背景色：#ffffff
- 文本色：#1e293b

## 字体系统
**Modern Clean**
- 标题：Inter
- 正文：Inter
- 代码：JetBrains Mono

## 推荐组件
- **Top Navigation Bar**
- **Basic Card**
- **Text Input**

## UX指南
- **WCAG 2.1 Level AA**
- **Mobile First**
- **Loading Performance**
```

### 示例2：搜索设计资源

```bash
python3 ~/.claude/skills/ui-design-pro/search.py ecommerce modern
```

输出：
```
================================================================================
UI设计搜索结果
================================================================================

## COLORS
### Vibrant Shopping
描述: 活力橙色，激发购买欲望

### Elegant Luxury
描述: 优雅奢华，适合高端品牌

## STYLES
### Minimalism
描述: 极简主义，少即是多
```

## 🎨 实际应用案例

### 案例1：SaaS产品着陆页

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My SaaS Product</title>
    <!-- 字体导入 -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            /* 配色方案 - Professional Blue */
            --primary: #2563eb;
            --secondary: #3b82f6;
            --accent: #60a5fa;
            --background: #ffffff;
            --text: #1e293b;

            /* Glassmorphism效果 */
            --glass-bg: rgba(255, 255, 255, 0.1);
            --glass-border: rgba(255, 255, 255, 0.2);
            --glass-blur: blur(10px);
        }

        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: var(--text);
            margin: 0;
            padding: 0;
        }

        .hero {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }

        .card {
            background: var(--glass-bg);
            backdrop-filter: var(--glass-blur);
            border: 1px solid var(--glass-border);
            border-radius: 1rem;
            padding: 3rem;
            max-width: 600px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }

        h1 {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .btn {
            background: var(--primary);
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 0.5rem;
            border: none;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .btn:hover {
            background: var(--secondary);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }
    </style>
</head>
<body>
    <div class="hero">
        <div class="card">
            <h1>欢迎使用我们的SaaS产品</h1>
            <p>基于Glassmorphism设计风格，使用Professional Blue配色方案</p>
            <button class="btn">开始使用</button>
        </div>
    </div>
</body>
</html>
```

## 💡 专业提示

1. **项目类型匹配**
   - SaaS → Glassmorphism + Professional Blue
   - 电商 → Minimalism + Vibrant Orange
   - 仪表盘 → Bento Grid + Modern Gradient

2. **技术栈选择**
   - 快速原型：HTML + Tailwind
   - 生产应用：React / Next.js
   - 企业应用：Vue / Nuxt.js

3. **可访问性优先**
   - 确保文字对比度≥4.5:1
   - 使用语义化HTML
   - 添加ARIA标签

4. **性能优化**
   - 图片懒加载
   - 代码分割
   - CDN加速

## 📚 常见问题

**Q: 如何选择合适的UI样式？**
A: 根据项目类型和目标用户。SaaS产品适合Glassmorphism，电商适合Minimalism。

**Q: 可以自定义配色方案吗？**
A: 可以！系统提供的是推荐方案，你可以根据品牌需求调整。

**Q: 支持哪些前端框架？**
A: HTML/Tailwind（默认）、React、Vue、Next.js、Nuxt.js等。

**Q: 如何确保响应式设计？**
A: 系统遵循Mobile First原则，提供标准断点：640px, 768px, 1024px, 1280px。

---

**现在就开始使用UI Design Pro，创建专业美观的UI设计！** 🚀
