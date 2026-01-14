#!/bin/bash
# GLM产品分析Skill（使用临时文件）

GLM_API_KEY="b3711c0052914e28abfa035b70e0e59e.Q7gu5Sb6tdILkCsk"
GLM_MODEL="glm-4-flash"
GLM_API_URL="https://open.bigmodel.cn/api/paas/v4/chat/completions"

# 创建临时文件存储请求数据
TEMP_FILE=$(mktemp)

# 生成请求数据
cat > "$TEMP_FILE" << EOF
{
  "model": "$GLM_MODEL",
  "messages": [
    {
      "role": "system",
      "content": "你是一个专业的产品经理和产品分析师。请从市场定位、竞争优势、功能建议、数据指标、风险应对等方面分析产品。使用emoji让内容更易读。"
    },
    {
      "role": "user",
      "content": "请分析以下产品：\n\n$@\n\n请从以下几个方面进行分析：\n1. 市场定位与目标用户\n2. 核心竞争优势\n3. 功能建议\n4. 数据指标建议\n5. 风险与应对"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 3000
}
EOF

# 替换产品信息
if [ -n "$1" ]; then
    sed -i '' "s|@|$1|g" "$TEMP_FILE"
else
    echo "使用方法: $0 \"产品信息\""
    echo "示例: $0 \"产品名称：智能客服，核心功能：自动回复\""
    rm "$TEMP_FILE"
    exit 1
fi

# 调用API
echo "📊 正在分析产品..."
echo ""

RESPONSE=$(curl -s -X POST "$GLM_API_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GLM_API_KEY" \
  -d @"$TEMP_FILE")

# 清理临时文件
rm "$TEMP_FILE"

# 解析响应
echo "$RESPONSE" | python3 -c "
import sys, json

try:
    data = json.load(sys.stdin)

    if 'error' in data:
        print('❌ 调用失败:')
        print(data['error'].get('message', '未知错误'))
        sys.exit(1)

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
        print('❌ API返回格式异常')
        print(json.dumps(data, indent=2, ensure_ascii=False))

except Exception as e:
    print(f'❌ 解析失败: {e}')
    print('原始响应:')
    print(sys.stdin.read())
"
