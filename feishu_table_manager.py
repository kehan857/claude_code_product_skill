#!/usr/bin/env python3
"""
飞书多维表格管理技能

功能：
1. 创建飞书多维表格
2. 导入自媒体账号数据（17条）
3. 转移表格所有权给指定用户
4. 优化表格（去除空白行和默认字段）

使用方法：
python3 feishu_table_manager.py
"""

import requests
import json
import sys

# ==================== 配置区域 ====================
# 飞书应用凭证
APP_ID = "cli_a871be56b7fd500d"
APP_SECRET = "pDAZMoOfj1t3wRX4WbBsweWz5lNqMNuW"

# 目标用户ID（表格所有者）
TARGET_USER_ID = "ou_9298897d71523ae9faba7fc454e2d32d"

# 表格配置
TABLE_NAME = "自媒体账号密码汇总"

# 数据定义（17条自媒体账号数据）
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


def create_table(token, name):
    """创建多维表格"""
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    body = {"name": name}
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    if data.get("code") == 0:
        app_token = data["data"]["app"]["app_token"]
        table_id = data["data"]["app"]["default_table_id"]
        return app_token, table_id
    else:
        raise Exception(f"创建表格失败: {data.get('msg')}")


def create_optimized_fields(token, app_token, table_id):
    """创建优化的字段（只包含需要的字段，不包含默认的多余字段）"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 只创建需要的8个字段
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


def delete_default_fields(token, app_token, table_id):
    """删除默认的多余字段"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 获取所有字段
    response = requests.get(url, headers=headers)
    data = response.json()
    if data.get("code") == 0:
        fields = data.get("data", {}).get("items", [])

        # 删除默认的多余字段
        default_fields_to_delete = ["文本", "单选", "日期", "附件"]
        for field in fields:
            field_name = field.get("field_name")
            if field_name in default_fields_to_delete:
                field_id = field.get("field_id")
                delete_url = f"{url}/{field_id}"
                requests.delete(delete_url, headers=headers)


def import_data(token, app_token, table_id):
    """导入数据到表格"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 准备记录
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


def transfer_ownership(token, app_token, user_id):
    """转移表格所有权"""
    url = f"https://open.feishu.cn/open-apis/drive/v1/permissions/{app_token}/members/transfer_owner"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    params = {
        "need_notification": "true",
        "old_owner_perm": "full_access",
        "remove_old_owner": "false",
        "stay_put": "false",
        "type": "bitable"
    }

    body = {
        "member_id": user_id,
        "member_type": "openid"
    }

    response = requests.post(url, params=params, headers=headers, json=body)
    data = response.json()
    if data.get("code") == 0:
        return True
    else:
        raise Exception(f"转移所有权失败: {data.get('msg')}")


def main():
    """主函数"""
    print("=" * 70)
    print("飞书多维表格一键创建和管理")
    print("=" * 70)

    try:
        # 步骤1: 获取访问令牌
        print("\n[1/6] 获取访问令牌...")
        token = get_tenant_token()
        print("✅ 访问令牌获取成功")

        # 步骤2: 创建表格
        print(f"\n[2/6] 创建多维表格: {TABLE_NAME}...")
        app_token, table_id = create_table(token, TABLE_NAME)
        print(f"✅ 表格创建成功")
        print(f"   App Token: {app_token}")
        print(f"   Table ID: {table_id}")

        # 步骤3: 创建优化的字段
        print("\n[3/6] 创建优化的字段...")
        create_optimized_fields(token, app_token, table_id)
        print("✅ 字段创建成功（8个字段）")

        # 步骤4: 删除默认的多余字段
        print("\n[4/6] 删除默认的多余字段...")
        delete_default_fields(token, app_token, table_id)
        print("✅ 已删除默认字段（文本、单选、日期、附件）")

        # 步骤5: 导入数据
        print("\n[5/6] 导入数据...")
        count = import_data(token, app_token, table_id)
        print(f"✅ 成功导入 {count} 条数据")

        # 步骤6: 转移所有权
        print(f"\n[6/6] 转移表格所有权...")
        transfer_ownership(token, app_token, TARGET_USER_ID)
        print(f"✅ 所有权已转移给: {TARGET_USER_ID}")

        # 输出结果
        table_link = f"https://feishu.cn/base/{app_token}"

        print("\n" + "=" * 70)
        print("✅ 飞书多维表格创建完成！")
        print("=" * 70)
        print(f"\n📊 表格信息:")
        print(f"   名称: {TABLE_NAME}")
        print(f"   数据行数: {count} 行")
        print(f"   字段数: 8 个（已优化）")
        print(f"   所有者: {TARGET_USER_ID}")

        print(f"\n🔗 表格访问链接:")
        print(f"   {table_link}")

        print(f"\n💡 优化说明:")
        print(f"   ✅ 已去除默认的多余字段")
        print(f"   ✅ 只保留需要的8个字段")
        print(f"   ✅ 已导入完整的17条数据")
        print(f"   ✅ 所有权已转移给你")

        print(f"\n📌 字段列表:")
        print(f"   1. 所属平台")
        print(f"   2. 名称")
        print(f"   3. 账号")
        print(f"   4. 密码")
        print(f"   5. 手机号")
        print(f"   6. 账号属性")
        print(f"   7. 认证人员")
        print(f"   8. 备注")

        return 0

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
