#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLM产品分析Skill（Python版本，不需要SDK）
"""

import json
import urllib.request
import urllib.error
import sys

# GLM API配置
GLM_API_KEY = "b3711c0052914e28abfa035b70e0e59e.Q7gu5Sb6tdILkCsk"
GLM_MODEL = "glm-4-flash"
GLM_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

def call_glm_api(messages, model=GLM_MODEL, temperature=0.7, max_tokens=3000):
    """调用GLM API"""

    # 构建请求数据
    request_data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    # 创建请求
    req = urllib.request.Request(
        GLM_API_URL,
        data=json.dumps(request_data).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {GLM_API_KEY}'
        }
    )

    try:
        # 发送请求
        with urllib.request.urlopen(req) as response:
            response_data = json.load(response)

            if 'choices' in response_data and len(response_data['choices']) > 0:
                content = response_data['choices'][0]['message']['content']
                usage = response_data.get('usage', {})
                return content, usage
            else:
                return None, response_data

    except urllib.error.HTTPError as e:
        error_msg = e.read().decode('utf-8')
        try:
            error_json = json.loads(error_msg)
            return None, error_json
        except:
            return None, {"error": {"message": error_msg}}
    except Exception as e:
        return None, {"error": {"message": str(e)}}


def analyze_product(product_info):
    """分析产品"""

    system_prompt = """你是一个专业的产品经理和产品分析师，擅长：
1. 市场分析和竞品研究
2. 用户需求分析
3. 产品功能设计
4. 数据指标制定
5. 产品规划建议

请以专业、客观的角度进行分析，给出具体可行的建议。
输出格式要清晰，使用emoji让内容更易读。"""

    user_message = f"""请分析以下产品：

{product_info}

请从以下几个方面进行分析：
1. 📊 市场定位与目标用户
2. 🎯 核心竞争优势
3. ⚡ 功能建议
4. 📈 数据指标建议
5. ⚠️  风险与应对"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    result, usage = call_glm_api(messages)

    if result:
        print("=" * 60)
        print("📊 产品分析报告")
        print("=" * 60)
        print()
        print(result)
        print()
        print("=" * 60)
        if usage:
            print(f"📊 Token使用: {usage.get('total_tokens', 0)} (输入: {usage.get('prompt_tokens', 0)}, 输出: {usage.get('completion_tokens', 0)})")
        print("=" * 60)
        return True
    else:
        print("❌ 调用失败:")
        print(json.dumps(usage, indent=2, ensure_ascii=False))
        return False


def main():
    """主函数"""

    if len(sys.argv) < 2:
        print("GLM产品分析Skill")
        print("=" * 60)
        print("\n使用方法:")
        print("  python3 glm_product_skill.py \"产品信息\"")
        print("\n示例:")
        print("  python3 glm_product_skill.py \"产品名称：智能客服，核心功能：自动回复\"")
        print()
        return

    # 获取产品信息
    product_info = " ".join(sys.argv[1:])

    # 分析产品
    analyze_product(product_info)


if __name__ == "__main__":
    main()
