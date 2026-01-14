#!/bin/bash
# GLM模型调用脚本（Shell版本）
# 使用方法: ./glm_chat.sh "你的消息"

GLM_API_KEY="b3711c0052914e28abfa035b70e0e59e.Q7gu5Sb6tdILkCsk"
GLM_MODEL="glm-4-flash"
GLM_API_URL="https://open.bigmodel.cn/api/paas/v4/chat/completions"

# 默认消息
MESSAGE=${1:-"你好"}

# 调用GLM API
curl -s -X POST "$GLM_API_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GLM_API_KEY" \
  -d "{
    \"model\": \"$GLM_MODEL\",
    \"messages\": [
      {\"role\": \"user\", \"content\": \"$MESSAGE\"}
    ],
    \"temperature\": 0.7,
    \"max_tokens\": 2000
  }" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'choices' in data and len(data['choices']) > 0:
        content = data['choices'][0]['message']['content']
        print(content)
        if 'usage' in data:
            print(f\"\n📊 Token使用: {data['usage']['total_tokens']}\", file=sys.stderr)
    else:
        print('❌ API返回格式异常', file=sys.stderr)
        print(json.dumps(data, indent=2, ensure_ascii=False), file=sys.stderr)
except Exception as e:
    print(f'❌ 解析响应失败: {e}', file=sys.stderr)
"
