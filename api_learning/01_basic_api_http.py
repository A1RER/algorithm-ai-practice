"""
API学习 - 使用HTTP协议（避免SSL问题）
"""

import requests


def test_http_api():
    """
    使用HTTP协议的API（不需要SSL证书）
    """
    print("=" * 60)
    print("练习1：调用HTTP API - 获取随机用户")
    print("=" * 60)

    # 这个API支持HTTP协议
    url = "http://api.open-notify.org/astros.json"

    print(f"📡 正在请求: {url}")

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f"✓ 请求成功！")
        print(f"\n当前在太空中的宇航员数量: {data['number']}")
        print(f"宇航员列表:")
        for person in data['people']:
            print(f"  - {person['name']} (在 {person['craft']})")
    else:
        print(f"✗ 请求失败")


def test_joke_api():
    """
    获取随机笑话
    """
    print("\n" + "=" * 60)
    print("练习2：获取随机笑话")
    print("=" * 60)

    url = "https://official-joke-api.appspot.com/random_joke"

    try:
        response = requests.get(url, timeout=10, verify=False)

        if response.status_code == 200:
            data = response.json()
            print(f"✓ 请求成功！")
            print(f"\n{data['setup']}")
            print(f"👉 {data['punchline']}")
    except Exception as e:
        print(f"请求失败: {e}")


if __name__ == "__main__":
    print("\n🚀 开始API学习！\n")

    test_http_api()
    test_joke_api()

    print("\n" + "=" * 60)
    print("📚 学到的知识:")
    print("1. API请求可能会遇到网络问题")
    print("2. HTTP和HTTPS的区别（HTTPS更安全但可能有证书问题）")
    print("3. 实际工作中需要处理各种网络异常")
    print("=" * 60)