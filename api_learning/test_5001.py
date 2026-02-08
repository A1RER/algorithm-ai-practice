"""
测试5001端口的代理配置
"""

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def test_port_5001():
    """测试5001端口"""

    port = 5001
    test_url = "https://httpbin.org/ip"

    print("=" * 60)
    print("测试5001端口 - HTTP代理")
    print("=" * 60)

    proxies_http = {
        'http': f'http://127.0.0.1:{port}',
        'https': f'http://127.0.0.1:{port}',
    }

    try:
        response = requests.get(test_url, proxies=proxies_http, timeout=10, verify=False)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ HTTP代理成功！")
            print(f"   你的IP: {data['origin']}")
            print(f"   推荐配置: proxies = {proxies_http}")
            return 'http', True
        else:
            print(f"✗ HTTP失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"✗ HTTP失败: {type(e).__name__}")
        print(f"   {str(e)[:100]}")

    print("\n" + "=" * 60)
    print("测试5001端口 - SOCKS5代理")
    print("=" * 60)

    proxies_socks5 = {
        'http': f'socks5://127.0.0.1:{port}',
        'https': f'socks5://127.0.0.1:{port}',
    }

    try:
        response = requests.get(test_url, proxies=proxies_socks5, timeout=10, verify=False)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ SOCKS5代理成功！")
            print(f"   你的IP: {data['origin']}")
            print(f"   推荐配置: proxies = {proxies_socks5}")
            return 'socks5', True
        else:
            print(f"✗ SOCKS5失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"✗ SOCKS5失败: {type(e).__name__}")
        print(f"   {str(e)[:100]}")

    return None, False


def test_apis_with_5001():
    """用5001端口测试之前失败的API"""

    print("\n" + "🚀" * 30)
    print("用5001端口测试实际API")
    print("🚀" * 30)

    # 先测试哪种代理类型可用
    proxy_type, success = test_port_5001()

    if not success:
        print("\n✗ 5001端口不可用，请检查:")
        print("  1. 代理软件是否正在运行")
        print("  2. 端口是否正确（5001）")
        print("  3. 代理类型是HTTP还是SOCKS5")
        return

    # 配置代理
    port = 5001
    if proxy_type == 'http':
        proxies = {
            'http': f'http://127.0.0.1:{port}',
            'https': f'http://127.0.0.1:{port}',
        }
    else:  # socks5
        proxies = {
            'http': f'socks5://127.0.0.1:{port}',
            'https': f'socks5://127.0.0.1:{port}',
        }

    print(f"\n✓ 使用配置: {proxies}\n")

    # 测试之前失败的API
    apis = [
        ("https://official-joke-api.appspot.com/random_joke", "笑话API"),
        ("https://catfact.ninja/fact", "猫咪知识API"),
        ("https://randomuser.me/api/", "随机用户API (之前失败)"),
        ("https://ipapi.co/json/", "IP信息API (之前失败)"),
    ]

    success_count = 0

    for url, name in apis:
        print("=" * 60)
        print(f"测试: {name}")
        print("=" * 60)

        try:
            response = requests.get(url, proxies=proxies, timeout=10, verify=False)

            if response.status_code == 200:
                data = response.json()
                print(f"✓ 成功！")
                success_count += 1

                # 显示部分数据
                if 'setup' in data:  # 笑话
                    print(f"   {data['setup']}")
                    print(f"   👉 {data['punchline']}")
                elif 'fact' in data:  # 猫咪知识
                    print(f"   🐱 {data['fact']}")
                elif 'results' in data:  # 随机用户
                    user = data['results'][0]
                    print(f"   👤 {user['name']['first']} {user['name']['last']}")
                    print(f"   📧 {user['email']}")
                elif 'ip' in data:  # IP信息
                    print(f"   🌍 IP: {data.get('ip')}")
                    print(f"   📍 {data.get('city')}, {data.get('country_name')}")
            else:
                print(f"✗ 失败，状态码: {response.status_code}")

        except Exception as e:
            print(f"✗ 失败: {type(e).__name__}")
            print(f"   {str(e)[:100]}")

        print()

    print("=" * 60)
    print(f"📊 成功: {success_count}/{len(apis)} 个API")
    print("=" * 60)


if __name__ == "__main__":
    test_apis_with_5001()

    print("\n" + "=" * 60)
    print("💾 如果测试成功，把这个配置保存到你的代码里:")
    print("=" * 60)
    print("""
# 在你的API代码开头添加:
proxies = {
    'http': 'http://127.0.0.1:5001',    # 如果是HTTP代理
    'https': 'http://127.0.0.1:5001',
}

# 或者 (如果是SOCKS5代理):
proxies = {
    'http': 'socks5://127.0.0.1:5001',
    'https': 'socks5://127.0.0.1:5001',
}

# 然后在每个requests.get()里加上proxies参数:
response = requests.get(url, proxies=proxies, verify=False)
    """)