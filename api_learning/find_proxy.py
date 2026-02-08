"""
自动扫描代理端口
"""

import socket
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def check_port_open(port):
    """检查端口是否开放"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0


def test_proxy_port(port, proxy_type='http'):
    """测试指定端口是否是可用的代理"""
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

    try:
        response = requests.get(
            'https://httpbin.org/ip',
            proxies=proxies,
            timeout=3,
            verify=False
        )
        if response.status_code == 200:
            return True
    except:
        pass

    return False


def scan_ports():
    """扫描常见代理端口"""

    print("🔍 正在扫描常见代理端口...\n")

    # 常见代理端口列表（扩展版）
    common_ports = [
        1080, 1081, 1082, 1087,  # SOCKS常见端口
        7890, 7891, 7892,  # Clash常见端口
        10808, 10809,  # V2Ray常见端口
        8080, 8081, 8888,  # HTTP代理常见端口
        5000, 5001, 5002,  # 你说的5001
        9050, 9150,  # Tor端口
        3128,  # Squid端口
    ]

    open_ports = []
    working_proxies = []

    # 第一步：检查哪些端口开放
    print("=" * 60)
    print("步骤1: 检查开放的端口")
    print("=" * 60)

    for port in common_ports:
        if check_port_open(port):
            open_ports.append(port)
            print(f"✓ 端口 {port} 开放")

    if not open_ports:
        print("✗ 没有找到开放的常见代理端口")
        print("\n请检查:")
        print("1. 代理软件是否正在运行？")
        print("2. 打开代理软件查看具体端口号")
        return

    # 第二步：测试哪些端口是可用的代理
    print("\n" + "=" * 60)
    print("步骤2: 测试哪些端口是可用的代理")
    print("=" * 60)

    for port in open_ports:
        print(f"\n测试端口 {port}...")

        # 测试HTTP代理
        if test_proxy_port(port, 'http'):
            print(f"  ✓ HTTP代理可用!")
            working_proxies.append({
                'port': port,
                'type': 'http',
                'config': {
                    'http': f'http://127.0.0.1:{port}',
                    'https': f'http://127.0.0.1:{port}',
                }
            })
            continue  # 找到HTTP就跳过SOCKS测试

        # 测试SOCKS5代理
        if test_proxy_port(port, 'socks5'):
            print(f"  ✓ SOCKS5代理可用!")
            working_proxies.append({
                'port': port,
                'type': 'socks5',
                'config': {
                    'http': f'socks5://127.0.0.1:{port}',
                    'https': f'socks5://127.0.0.1:{port}',
                }
            })

    # 显示结果
    print("\n" + "=" * 60)
    print("📊 扫描结果")
    print("=" * 60)

    if working_proxies:
        print(f"\n✓ 找到 {len(working_proxies)} 个可用代理:\n")

        for i, proxy in enumerate(working_proxies, 1):
            print(f"{i}. 端口 {proxy['port']} ({proxy['type'].upper()})")
            print(f"   配置: proxies = {proxy['config']}\n")

        # 推荐配置
        best = working_proxies[0]
        print("=" * 60)
        print("💡 推荐使用配置:")
        print("=" * 60)
        print(f"""
# 复制下面的代码到你的脚本开头
proxies = {best['config']}

# 使用方法:
response = requests.get(url, proxies=proxies, verify=False)
        """)

    else:
        print("\n✗ 没有找到可用的代理")
        print("\n可能的原因:")
        print("1. 代理软件可能使用了其他端口")
        print("2. 代理可能需要认证")
        print("3. 代理配置可能有问题")
        print("\n建议:")
        print("→ 打开代理软件，查看实际使用的端口")
        print("→ 或者截图代理软件的设置给我看")


if __name__ == "__main__":
    print("\n" + "🚀" * 30)
    print("代理端口自动扫描工具")
    print("🚀" * 30 + "\n")

    scan_ports()

    print("\n" + "=" * 60)
    print("如果没找到，请:")
    print("1. 打开你的代理软件")
    print("2. 截图设置页面给我看")
    print("3. 或者告诉我代理软件的名字和端口号")
    print("=" * 60)