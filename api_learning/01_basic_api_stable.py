"""
API学习 - 稳定版本
使用多个可靠的免费API
日期: 2025-02-08
"""

import requests
import urllib3

# 禁用SSL警告（学习阶段临时使用）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def test_joke_api():
    """
    练习1：获取随机笑话（程序员专属）
    """
    print("=" * 60)
    print("练习1：调用笑话API")
    print("=" * 60)

    url = "https://official-joke-api.appspot.com/random_joke"

    try:
        response = requests.get(url, timeout=10, verify=False)

        if response.status_code == 200:
            data = response.json()
            print(f"✓ 请求成功！状态码: {response.status_code}")
            print(f"\n😄 {data['setup']}")
            print(f"👉 {data['punchline']}\n")
            print(f"类型: {data['type']}")
        else:
            print(f"✗ 请求失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"✗ 请求失败: {e}")


def test_random_user_api():
    """
    练习2：获取随机用户信息
    """
    print("\n" + "=" * 60)
    print("练习2：调用随机用户API")
    print("=" * 60)

    url = "https://randomuser.me/api/"

    try:
        response = requests.get(url, timeout=10, verify=False)

        if response.status_code == 200:
            data = response.json()
            user = data['results'][0]

            print(f"✓ 请求成功！")
            print(f"\n👤 随机生成的用户信息:")
            print(f"  姓名: {user['name']['first']} {user['name']['last']}")
            print(f"  性别: {user['gender']}")
            print(f"  邮箱: {user['email']}")
            print(f"  国家: {user['location']['country']}")
            print(f"  城市: {user['location']['city']}")
        else:
            print(f"✗ 请求失败")
    except Exception as e:
        print(f"✗ 请求失败: {e}")


def test_cat_fact_api():
    """
    练习3：获取猫咪小知识
    """
    print("\n" + "=" * 60)
    print("练习3：调用猫咪知识API")
    print("=" * 60)

    url = "https://catfact.ninja/fact"

    try:
        response = requests.get(url, timeout=10, verify=False)

        if response.status_code == 200:
            data = response.json()
            print(f"✓ 请求成功！")
            print(f"\n🐱 猫咪小知识:")
            print(f"  {data['fact']}")
            print(f"  (长度: {data['length']} 字符)")
        else:
            print(f"✗ 请求失败")
    except Exception as e:
        print(f"✗ 请求失败: {e}")


def test_api_with_parameters():
    """
    练习4：带参数的API请求 - 获取多个笑话
    """
    print("\n" + "=" * 60)
    print("练习4：使用参数获取多个笑话")
    print("=" * 60)

    # 获取编程类笑话
    url = "https://official-joke-api.appspot.com/jokes/programming/random"

    try:
        response = requests.get(url, timeout=10, verify=False)

        if response.status_code == 200:
            jokes = response.json()
            print(f"✓ 获取了 {len(jokes)} 个编程笑话:\n")

            for i, joke in enumerate(jokes[:3], 1):  # 只显示前3个
                print(f"{i}. {joke['setup']}")
                print(f"   👉 {joke['punchline']}\n")
        else:
            print(f"✗ 请求失败")
    except Exception as e:
        print(f"✗ 请求失败: {e}")


def test_ip_api():
    """
    练习5：获取你的IP地址和位置信息
    """
    print("\n" + "=" * 60)
    print("练习5：获取你的IP信息")
    print("=" * 60)

    url = "https://ipapi.co/json/"

    try:
        response = requests.get(url, timeout=10, verify=False)

        if response.status_code == 200:
            data = response.json()
            print(f"✓ 请求成功！")
            print(f"\n🌍 你的网络信息:")
            print(f"  IP地址: {data.get('ip', 'N/A')}")
            print(f"  城市: {data.get('city', 'N/A')}")
            print(f"  地区: {data.get('region', 'N/A')}")
            print(f"  国家: {data.get('country_name', 'N/A')}")
            print(f"  运营商: {data.get('org', 'N/A')}")
        else:
            print(f"✗ 请求失败")
    except Exception as e:
        print(f"✗ 请求失败: {e}")


def analyze_api_response():
    """
    练习6：深入分析API响应结构
    """
    print("\n" + "=" * 60)
    print("练习6：分析API响应的结构")
    print("=" * 60)

    url = "https://official-joke-api.appspot.com/random_joke"

    try:
        response = requests.get(url, timeout=10, verify=False)

        print(f"\n📊 响应分析:")
        print(f"  状态码: {response.status_code}")
        print(f"  响应时间: {response.elapsed.total_seconds():.2f} 秒")
        print(f"  内容类型: {response.headers.get('Content-Type')}")
        print(f"  响应大小: {len(response.content)} 字节")

        print(f"\n📦 返回的JSON数据:")
        data = response.json()
        import json
        print(json.dumps(data, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"✗ 请求失败: {e}")


if __name__ == "__main__":
    print("\n" + "🚀" * 30)
    print("开始API学习之旅！")
    print("🚀" * 30 + "\n")

    # 运行所有练习
    test_joke_api()
    test_random_user_api()
    test_cat_fact_api()
    test_api_with_parameters()
    test_ip_api()
    analyze_api_response()

    # 总结
    print("\n" + "=" * 60)
    print("📚 今天学到的核心概念:")
    print("=" * 60)
    print("""
1. ✅ API就是一个URL，你发请求，它返回数据
2. ✅ 使用 requests.get(url) 发送GET请求
3. ✅ 使用 response.json() 解析返回的JSON数据
4. ✅ 检查 response.status_code 判断请求是否成功
5. ✅ 需要用 try-except 处理网络异常
6. ✅ 可以传递 params 参数来筛选数据
7. ✅ API响应包含状态码、头信息、内容等多种信息

💡 下一步学习计划:
   - 学习POST请求（不只是GET）
   - 学习需要API Key的认证方式
   - 学习处理分页、限流等问题
    """)
    print("=" * 60)