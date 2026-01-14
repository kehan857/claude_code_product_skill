#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLM模型调用Skill
可以直接调用智谱AI的GLM模型进行对话和分析
"""

import os
import sys
import json

try:
    from zhipuai import ZhipuAI
except ImportError:
    print("❌ 请先安装zhipuai库: pip install zhipuai")
    sys.exit(1)

# GLM API配置
GLM_API_KEY = "b3711c0052914e28abfa035b70e0e59e.Q7gu5Sb6tdILkCsk"

# 默认配置
DEFAULT_MODEL = "glm-4-flash"  # 使用快速且经济的模型
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2000

class GLMSkill:
    """GLM模型调用技能类"""

    def __init__(self, api_key=None):
        """初始化GLM客户端"""
        self.api_key = api_key or GLM_API_KEY
        self.client = ZhipuAI(api_key=self.api_key)

    def chat(self, message, system_prompt=None, model=None, temperature=None, max_tokens=None):
        """
        与GLM模型对话

        Args:
            message: 用户消息
            system_prompt: 系统提示词（可选）
            model: 模型名称（默认：glm-4-flash）
            temperature: 温度参数（默认：0.7）
            max_tokens: 最大token数（默认：2000）

        Returns:
            str: 模型响应
        """
        try:
            # 构建消息列表
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": message})

            # 调用GLM API
            response = self.client.chat.completions.create(
                model=model or DEFAULT_MODEL,
                messages=messages,
                temperature=temperature or DEFAULT_TEMPERATURE,
                max_tokens=max_tokens or DEFAULT_MAX_TOKENS,
            )

            # 返回结果
            result = response.choices[0].message.content

            # 显示token使用情况
            usage = response.usage
            print(f"\n📊 Token使用: {usage.total_tokens} (输入: {usage.prompt_tokens}, 输出: {usage.completion_tokens})")

            return result

        except Exception as e:
            return f"❌ 调用失败: {str(e)}"

    def analyze_product(self, product_info):
        """分析产品"""
        system_prompt = """你是一个专业的产品经理和产品分析师，擅长：
1. 市场分析和竞品研究
2. 用户需求分析
3. 产品功能设计
4. 数据指标制定
5. 产品规划建议

请以专业、客观的角度进行分析，给出具体可行的建议。"""

        message = f"""请分析以下产品：

{product_info}

请从以下几个方面进行分析：
1. 市场定位与目标用户
2. 核心竞争优势
3. 功能建议
4. 数据指标建议
5. 风险与应对"""

        return self.chat(message, system_prompt)

    def generate_product_doc(self, product_name, description):
        """生成产品文档"""
        system_prompt = """你是一个专业的产品文档编写专家，熟悉产品详细设计文档的编写规范。
文档应该符合中文学术格式，包括：
- 产品概述
- 市场分析
- 用户分析
- 产品功能
- 功能详细设计
- 数据指标
- 运营规划
- 风险与应对
- 产品路线图"""

        message = f"""请为以下产品生成详细设计文档大纲：

产品名称：{product_name}
产品描述：{description}

请生成完整的产品详细设计文档，包含九大核心模块。"""

        return self.chat(message, system_prompt, max_tokens=4000)

    def improve_requirement(self, requirement_text):
        """优化需求描述"""
        system_prompt = """你是一个产品需求分析专家，擅长将模糊的需求转化为清晰、可执行的产品需求。
你会：
1. 理解用户的核心诉求
2. 识别需求中的关键点
3. 补充缺失的信息
4. 优化需求表达
5. 给出可行性建议"""

        message = f"""请帮我优化以下需求描述：

{requirement_text}

请提供：
1. 需求分析
2. 优化后的需求描述
3. 需求拆解（如果有多个子需求）
4. 实现建议"""

        return self.chat(message, system_prompt)


def main():
    """主函数：命令行交互"""
    print("=" * 60)
    print("🤖 GLM模型调用Skill")
    print("=" * 60)

    # 初始化GLM Skill
    glm = GLMSkill()

    print("\n请选择功能：")
    print("1. 💬 普通对话")
    print("2. 📊 产品分析")
    print("3. 📝 生成产品文档")
    print("4. ✨ 优化需求描述")
    print("5. 🚪 退出")

    while True:
        choice = input("\n请输入选项 (1-5): ").strip()

        if choice == "1":
            # 普通对话
            message = input("请输入你的消息: ").strip()
            if message:
                response = glm.chat(message)
                print(f"\n🤖 GLM回复:\n{response}\n")

        elif choice == "2":
            # 产品分析
            print("\n请输入产品信息（输入完成后按回车）：")
            product_info = input().strip()
            if product_info:
                response = glm.analyze_product(product_info)
                print(f"\n📊 产品分析:\n{response}\n")

        elif choice == "3":
            # 生成产品文档
            product_name = input("请输入产品名称: ").strip()
            description = input("请输入产品描述: ").strip()
            if product_name and description:
                response = glm.generate_product_doc(product_name, description)
                print(f"\n📝 产品文档:\n{response}\n")

        elif choice == "4":
            # 优化需求
            print("\n请输入需求描述（输入完成后按回车）：")
            requirement = input().strip()
            if requirement:
                response = glm.improve_requirement(requirement)
                print(f"\n✨ 优化后的需求:\n{response}\n")

        elif choice == "5":
            print("\n👋 再见！")
            break

        else:
            print("\n❌ 无效选项，请重新输入")


if __name__ == "__main__":
    # 如果有命令行参数，直接处理
    if len(sys.argv) > 1:
        glm = GLMSkill()

        if sys.argv[1] == "chat" and len(sys.argv) > 2:
            # 直接对话
            message = " ".join(sys.argv[2:])
            response = glm.chat(message)
            print(response)

        elif sys.argv[1] == "analyze" and len(sys.argv) > 2:
            # 分析产品
            product_info = " ".join(sys.argv[2:])
            response = glm.analyze_product(product_info)
            print(response)

        elif sys.argv[1] == "doc" and len(sys.argv) > 3:
            # 生成文档
            product_name = sys.argv[2]
            description = " ".join(sys.argv[3:])
            response = glm.generate_product_doc(product_name, description)
            print(response)

        else:
            print("用法:")
            print("  python glm_skill.py chat <消息>")
            print("  python glm_skill.py analyze <产品信息>")
            print("  python glm_skill.py doc <产品名称> <产品描述>")
            print("  python glm_skill.py  # 交互模式")
    else:
        # 交互模式
        main()
