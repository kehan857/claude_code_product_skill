#!/usr/bin/env python3
"""
飞书多维表格一键导入脚本
用于将自媒体账号数据导入到飞书多维表格
"""

import requests
import json

# ==================== 配置区域 ====================
# 飞书应用凭证
APP_ID = "cli_a871be56b7fd500d"
APP_SECRET = "pDAZMoOfj1t3wRX4WbBsweWz5lNqMNuW"

# 如果已存在表格，填写APP_TOKEN和TABLE_ID；留空则创建新表格
EXISTING_APP_TOKEN = ""  # 例如: "A7fabm4uiaMaRzsJMJ8cnUcrnzg"
EXISTING_TABLE_ID = ""  # 例如: "tbljZp3HFqbUBx3P"

# 表格名称（创建新表格时使用）
TABLE_NAME = "自媒体账号密码汇总"

# 数据定义
DATA_ROWS = [
    {'platform': '微信公众号', 'name': '福泽鑫', 'account': 'tbhioxxu613@outlook.com', 'password': 'knu131057', 'phone': '13811957827', 'type': '个人', 'auth_person': '辰川', 'remark': ''},
    {'platform': '微信公众号', 'name': '云启辰', 'account': 'gygpngx601@outlook.com', 'password': 'lhf054487', 'phone': '13581953791', 'type': '企业', 'auth_person': '北京智泽网络科技有限公司', 'remark': ''},
    {'platform': '微信公众号', 'name': '金戊智创', 'account': 'jmvtweb499@outlook.com', 'password': 'tkz051566', 'phone': '13581953791', 'type': '企业', 'auth_person': '北京智泽网络科技有限公司', 'remark': ''},
    {'platform': '微信公众号', 'name': '垚仓食代', 'account': 'dsdyqro164@outlook.com', 'password': 'szj845744', 'phone': '13811957827', 'type': '企业', 'auth_person': '思味特(北京)餐饮管理有限公司', 'remark': ''},
    {'platform': '头条号', 'name': '幸福看房X', 'account': '', 'password': '', 'phone': '15300222499', 'type': '个人', 'auth_person': '', 'remark': ''},
    {'platform': '头条号', 'name': '开心看房Vlog', 'account': '', 'password': '', 'phone': '18301114761', 'type': '个人', 'auth_person': '', 'remark': ''},
    {'platform': '头条号', 'name': '', 'account': '', 'password': 'v@h@aQud4Z@ZZyp', 'phone': '15710076120', 'type': '个人', 'auth_person': '', 'remark': ''},
    {'platform': '头条号', 'name': '', 'account': '', 'password': '@BZg7b@H9SaeM2V', 'phone': '15537926489', 'type': '个人', 'auth_person': '', 'remark': ''},
    {'platform': '知乎', 'name': '', 'account': '', 'password': 'Kxb13071706603', 'phone': '15710076120', 'type': '个人', 'auth_person': '', 'remark': ''},
    {'platform': '知乎', 'name': '', 'account': '', 'password': 'B8.67KLr3Xp68vb', 'phone': '15537926489', 'type': '个人', 'auth_person': '', 'remark': ''},
    {'platform': '知乎', 'name': '知乎机构号', 'account': 'kexiaobin@sbzytech.cn', 'password': '9iyQfezQTSR5j.M', 'phone': '', 'type': '企业', 'auth_person': '', 'remark': ''},
    {'platform': '腾讯内容开放平台', 'name': '', 'account': '', 'password': '', 'phone': '', 'type': '', 'auth_person': '', 'remark': '添加运营者链接：http://m.om.qq.com/mobile/invite?optoken=69646b43ae6ed'},
    {'platform': '微信视频号', 'name': '', 'account': '', 'password': '', 'phone': '', 'type': '', 'auth_person': '', 'remark': '视频号ID: sph0HbBGIUWvg2X，需先关注视频号，后台可添加运营者'},
    {'platform': '百家号', 'name': '', 'account': '', 'password': '', 'phone': '', 'type': '', 'auth_person': '', 'remark': ''},
    {'platform': '腾讯新闻', 'name': '', 'account': '', 'password': '', 'phone': '', 'type': '', 'auth_person': '', 'remark': ''},
    {'platform': '小红书', 'name': '', 'account': '', 'password': '', 'phone': '', 'type': '', 'auth_person': '', 'remark': ''},
    {'platform': '抖音', 'name': '', 'account': '', 'password': '', 'phone': '', 'type': '', 'auth_person': '', 'remark': ''},
]
# ================================================


def get_tenant_token():
    """获取租户访问令牌"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    response = requests.post(url, json={
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    })
    data = response.json()
    if data.get("code") == 0:
        return data.get("tenant_access_token")
    else:
        raise Exception(f"获取令牌失败: {data.get('msg')}")


def create_table(token):
    """创建新的多维表格"""
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    body = {"name": TABLE_NAME}
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    if data.get("code") == 0:
        app_token = data["data"]["app"]["app_token"]
        table_id = data["data"]["app"]["default_table_id"]
        return app_token, table_id
    else:
        raise Exception(f"创建表格失败: {data.get('msg')}")


def create_fields(token, app_token, table_id):
    """创建表格字段"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    fields = [
        {"field_name": "所属平台", "type": 1},
        {"field_name": "名称", "type": 1},
        {"field_name": "账号", "type": 1},
        {"field_name": "密码", "type": 1},
        {"field_name": "手机号", "type": 1},
        {"field_name": "账号属性", "type": 3},
        {"field_name": "认证人员", "type": 1},
        {"field_name": "备注", "type": 1}
    ]

    for field in fields:
        requests.post(url, headers=headers, json=field)


def import_data(token, app_token, table_id):
    """导入数据到表格"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    records = []
    for row in DATA_ROWS:
        record = {
            "fields": {
                "所属平台": row["platform"],
                "名称": row["name"],
                "账号": row["account"],
                "密码": row["password"],
                "手机号": row["phone"],
                "账号属性": row["type"],
                "认证人员": row["auth_person"],
                "备注": row["remark"]
            }
        }
        records.append(record)

    body = {"records": records}
    response = requests.post(url, headers=headers, json=body)
    data = response.json()

    if data.get("code") == 0:
        return len(data.get("data", {}).get("records", []))
    else:
        raise Exception(f"导入数据失败: {data.get('msg')}")


def main():
    """主函数"""
    print("=" * 70)
    print("飞书多维表格一键导入脚本")
    print("=" * 70)

    try:
        # 1. 获取访问令牌
        print("\n[1/4] 获取访问令牌...")
        token = get_tenant_token()
        print("✅ 访问令牌获取成功")

        # 2. 确定使用哪个表格
        if EXISTING_APP_TOKEN and EXISTING_TABLE_ID:
            print(f"\n[2/4] 使用现有表格...")
            app_token = EXISTING_APP_TOKEN
            table_id = EXISTING_TABLE_ID
            print(f"✅ App Token: {app_token}")
            print(f"✅ Table ID: {table_id}")
        else:
            print(f"\n[2/4] 创建新表格: {TABLE_NAME}...")
            app_token, table_id = create_table(token)
            print(f"✅ 表格创建成功")
            print(f"✅ App Token: {app_token}")
            print(f"✅ Table ID: {table_id}")

            # 3. 创建字段
            print(f"\n[3/4] 创建表格字段...")
            create_fields(token, app_token, table_id)
            print("✅ 字段创建成功")

        # 4. 导入数据
        print(f"\n[4/4] 导入数据...")
        count = import_data(token, app_token, table_id)
        print(f"✅ 成功导入 {count} 条数据")

        # 输出结果
        table_link = f"https://feishu.cn/base/{app_token}"
        print("\n" + "=" * 70)
        print("✅ 导入完成！")
        print("=" * 70)
        print(f"\n📊 表格名称: {TABLE_NAME}")
        print(f"📈 数据行数: {count} 行")
        print(f"\n🔗 访问链接:")
        print(f"   {table_link}")
        print(f"\n💡 提示:")
        print(f"   - 点击链接即可在浏览器中打开表格")
        print(f"   - 保存 APP_TOKEN 和 TABLE_ID 可复用该表格:")
        print(f"     APP_TOKEN = \"{app_token}\"")
        print(f"     TABLE_ID = \"{table_id}\"")

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
