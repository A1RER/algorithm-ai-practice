"""
V2RayN 代理配置测试
"""

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def test_v2ray_configs():
    """测试V2RayN的多种可能配置"""

    print("🚀 测试 V2RayN 代理配置\n")

    # V2RayN可能的配置组合
    configs = [
        {
            'name': 'SOCKS5 - 端口5001',
            'proxies': {
                'http': 'socks5://127.0.0.1:5001',
                'https': 'socks5://127.0.0.1:5001',
            }
        },
        {
            'name': 'SOCKS5H - 端口5001 (DNS通过代理)',
            'proxies': {
                'http': 'socks5h://127.0.0.1:5001',
                'https': 'socks5h://127.0.0.1:5001',
            }
        },
        {
            'name': 'HTTP - 端口10809',
            'proxies': {
                'http': 'http://127.0.0.1:10809',
                'https': 'http://127.0.0.1:10809',
            }
        },
        {
            'name': 'HTTP - 端口10808',
            'proxies': {
                'http': 'http://127.0.0.1:10808',
                'https': 'http://127.0.0.1:10808',
            }
        },
    ]

    working_config = None

    for config in configs:
        print("=" * 60)
        print(f"测试配置: {config['name']}")
        print("=" * 60)
        print(f"proxies = {config['proxies']}\n")

        try:
            response = requests.get(
                'https://httpbin.org/ip',
                proxies=config['proxies'],
                timeout=10,
                verify=False
            )

            if response.status_code == 200:
                data = response.json()
                print(f"✓ 成功！")
                print(f"   你的代理IP: {data['origin']}")
                working_config = config
                break  # 找到可用的就停止
            else:
                print(f"✗ 失败，状态码: {response.status_code}")

        except Exception as e:
            print(f"✗ 失败: {type(e).__name__}")
            print(f"   {str(e)[:100]}\n")

    if working_config:
        print("\n" + "=" * 60)
        print("🎉 找到可用配置！")
        print("=" * 60)

        # 测试实际API
        print("\n正在用这个配置测试实际API...\n")

        test_apis = [
            ("https://official-joke-api.appspot.com/random_joke", "笑话API"),
            ("https://randomuser.me/api/", "随机用户API"),
            ("https://catfact.ninja/fact", "猫咪知识API"),
        ]

        success_count = 0

        for url, name in test_apis:
            print(f"测试 {name}...", end=" ")
            try:
                response = requests.get(
                    url,
                    proxies=working_config['proxies'],
                    timeout=10,
                    verify=False
                )
                if response.status_code == 200:
                    print("✓ 成功")
                    success_count += 1
                else:
                    print(f"✗ 失败 ({response.status_code})")
            except Exception as e:
                print(f"✗ 失败 ({type(e).__name__})")

        print(f"\n成功: {success_count}/{len(test_apis)}")

        # 推荐配置
        print("\n" + "=" * 60)
        print("💾 推荐配置代码:")
        print("=" * 60)
        print(f"""
# 在你的代码开头添加:
proxies = {working_config['proxies']}

# 使用方法:
response = requests.get(url, proxies=proxies, verify=False)
        """)

    else:
        print("\n" + "=" * 60)
        print("✗ 所有配置都失败了")
        print("=" * 60)
        print("\n请检查:")
        print("1. V2RayN 是否正在运行？")
        print("2. 点击 V2RayN 的'设置'标签，查看HTTP代理端口")
        print("3. 截图'设置'页面给我看")


if __name__ == "__main__":
    test_v2ray_configs()