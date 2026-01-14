#!/bin/bash
# GLM产品分析Skill
# 使用方法: ./glm_product_skill.sh [产品信息]

GLM_API_KEY="b3711c0052914e28abfa035b70e0e59e.Q7gu5Sb6tdILkCsk"
GLM_MODEL="glm-4-flash"
GLM_API_URL="https://open.bigmodel.cn/api/paas/v4/chat/completions"

# 产品分析提示词
SYSTEM_PROMPT="你是一个专业的产品经理和产品分析师，擅长：
1. 市场分析和竞品研究
2. 用户需求分析
3. 产品功能设计
4. 数据指标制定
5. 产品规划建议

请以专业、客观的角度进行分析，给出具体可行的建议。
输出格式要清晰，使用emoji让内容更易读。"

# 获取产品信息
if [ -z "$1" ]; then
    echo "请提供产品信息"
    echo "使用方法: $0 \"产品名称：XXX，核心功能：XXX，目标用户：XXX\""
    exit 1
fi

PRODUCT_INFO="$1"

# 调用GLM API进行产品分析
curl -s -X POST "$GLM_API_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GLM_API_KEY" \
  -d "{
    \"model\": \"$GLM_MODEL\",
    \"messages\": [
      {\"role\": \"system\", \"content\": \"$SYSTEM_PROMPT\"},
      {\"role\": \"user\", \"content\": \"请分析以下产品：\\n\\n$PRODUCT_INFO\\n\\n请从以下几个方面进行分析：\\n1. 📊 市场定位与目标用户\\n2. 🎯 核心竞争优势\\n3. ⚡ 功能建议\\n4. 📈 数据指标建议\\n5. ⚠️  风险与应对\"}
    ],
    \"temperature\": 0.7,
    \"max_tokens\": 3000
  }" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'choices' in data and len(data['choices']) > 0:
        content = data['choices'][0]['message']['content']
        print('=' * 60)
        print('📊 产品分析报告')
        print('=' * 60)
        print()
        print(content)
        print()
        print('=' * 60)
        if 'usage' in data:
            usage = data['usage']
            print(f\"📊 Token使用: {usage['total_tokens']} (输入: {usage['prompt_tokens']}, 输出: {usage['completion_tokens']})\")
        print('=' * 60)
    else:
        print('❌ API返回格式异常', file=sys.stderr)
        print(json.dumps(data, indent=2, ensure_ascii=False), file=sys.stderr)
except Exception as e:
    print(f'❌ 解析响应失败: {e}', file=sys.stderr)
"
