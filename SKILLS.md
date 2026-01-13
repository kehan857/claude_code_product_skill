# Claude Code 技能集合

> 个人开发的各种自动化技能脚本集合

## 📋 技能分类

### 🎯 文档处理类

#### 1. 文档分析与修改
- **analyze_doc.py** - Word文档分析
- **analyze_bom_doc.py** - BOM文档分析
- **modify_document.py** - 文档修改（第一版）
- **modify_document_v2.py** - 文档修改（第二版）
- **modify_document_v3.py** - 文档修改（第三版）
- **modify_numbering.py** - 编号修改
- **fill_authorization.py** - 授权信息填充

#### 2. 内容提取
- **extract_form.py** - 表单内容提取
- **extract_altchunk.py** - AltChunk提取
- **extract_raw_xml.py** - 原始XML提取
- **read_doc_content.py** - 文档内容读取
- **read_docx.py** - DOCX文件读取

#### 3. 文档检查
- **check_doc_structure.py** - 文档结构检查
- **analyze_numbering.py** - 编号分析（第一版）
- **analyze_numbering_v2.py** - 编号分析（第二版）

### 📊 表格处理类

#### 1. Excel生成
- **create_excel.py** - Excel表格生成
- **generate_vc_form_excel.py** - VC表单Excel生成

#### 2. 飞书多维表格
- **feishu_table_manager.py** - ⭐ 飞书表格一键管理（推荐）
- **导入飞书表格.py** - 飞书表格导入

### 🔍 搜索与分析类

- **search_bom_examples.py** - BOM示例搜索
- **show_bom_preview.py** - BOM预览显示
- **modify_bom_example.py** - BOM示例修改

### 🧪 测试工具类

- **test_ui_design_skill.py** - UI设计技能测试

---

## 🌟 核心技能

### 1. 飞书表格一键管理 ⭐⭐⭐⭐⭐

**文件**: `feishu_table_manager.py`

**功能**:
- ✅ 一键创建飞书多维表格
- ✅ 自动创建优化的8个字段
- ✅ 导入17条自媒体账号数据
- ✅ 删除默认的多余字段
- ✅ 转移表格所有权

**使用方法**:
```bash
python3 feishu_table_manager.py
```

**适用场景**:
- 需要快速创建飞书多维表格
- 需要导入结构化数据
- 需要表格所有权转移

---

## 📖 使用指南

### 基础使用

所有Python脚本都支持直接运行：

```bash
python3 <脚本名>.py
```

### 配置说明

大多数脚本需要在文件顶部配置相关参数：

```python
# 配置区域
PARAMETER_1 = "值1"
PARAMETER_2 = "值2"
```

---

## 🛠️ 技术栈

- **语言**: Python 3
- **主要库**:
  - `requests` - HTTP请求
  - `openpyxl` - Excel处理
  - `python-docx` - Word文档处理
  - `lxml` - XML解析

---

## 📝 版本历史

### v1.0 (2025-01-13)
- 初始版本
- 包含文档处理、表格生成、飞书集成等技能
- 重点推荐：飞书表格一键管理技能

---

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

## 📄 许可证

MIT License

---

**创建者**: kehan857
**最后更新**: 2025-01-13
