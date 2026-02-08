"""
API学习 - 完美配置版（支持V2RayN代理）
作者: Chuyuan
日期: 2025-02-08
"""

import requests
import urllib3
import socket
import time

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============ V2RayN 代理配置 ============
USE_PROXY = True  # 改成False可以关闭代理
PROXY_HOST = "127.0.0.1"
PROXY_PORT = 10808
TIMEOUT = 20  # 请求超时时间（秒）
MAX_RETRIES = 2  # 失败后最多重试次数


def check_proxy_available(host, port):
    """检测代理端口是否可用"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False


# 启动时自动检测代理
if USE_PROXY:
    if check_proxy_available(PROXY_HOST, PROXY_PORT):
        proxies = {
            'http': f'http://{PROXY_HOST}:{PROXY_PORT}',
            'https': f'http://{PROXY_HOST}:{PROXY_PORT}',
        }
        print(f"🔧 使用代理: V2RayN (HTTP {PROXY_PORT}端口)\n")
    else:
        proxies = None
        print(f"⚠️  代理端口 {PROXY_PORT} 不可用，已自动切换为直连模式\n")
else:
    proxies = None
    print("🔧 直连模式（不使用代理）\n")


# =========================================


def api_request(url, description, retries=MAX_RETRIES):
    """
    通用API请求函数
    自动处理代理、重试和异常
    """
    print("=" * 60)
    print(f"请求: {description}")
    print("=" * 60)
    print(f"🌐 URL: {url}")

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(
                url,
                proxies=proxies,
                verify=False,
                timeout=TIMEOUT
            )

            if response.status_code == 200:
                print(f"✓ 成功！状态码: {response.status_code}")
                print(f"⏱️  响应时间: {response.elapsed.total_seconds():.2f}秒")
                return response.json()
            elif response.status_code == 429:
                print(f"⚠️  触发速率限制 (429)，等待后重试...")
                time.sleep(3)
                continue
            elif response.status_code == 403:
                print(f"✗ 被拒绝 (403): 可能是API调用次数用完了")
                return None
            else:
                print(f"✗ 失败，状态码: {response.status_code}")
                return None

        except requests.exceptions.Timeout:
            print(f"✗ 第{attempt}次请求超时（>{TIMEOUT}秒）", end="")
        except requests.exceptions.ProxyError:
            print(f"✗ 第{attempt}次代理连接失败，请检查V2RayN是否运行", end="")
        except requests.exceptions.ConnectionError as e:
            print(f"✗ 第{attempt}次连接失败: {e}", end="")
        except requests.exceptions.JSONDecodeError:
            print(f"✗ 返回的不是合法JSON，可能API服务异常")
            return None
        except Exception as e:
            print(f"✗ 第{attempt}次请求失败: {type(e).__name__}: {e}", end="")

        # 还有重试机会就等一下再试
        if attempt < retries:
            wait = attempt * 2
            print(f"，{wait}秒后重试...")
            time.sleep(wait)
        else:
            print(f"，已达到最大重试次数")

    return None


def test_joke_api():
    """练习1：获取编程笑话"""
    data = api_request(
        "https://official-joke-api.appspot.com/jokes/programming/random",
        "编程笑话API"
    )

    if data:
        print(f"\n😄 笑话:")
        for joke in data[:2]:  # 显示2个
            print(f"   Q: {joke['setup']}")
            print(f"   A: {joke['punchline']}\n")


def test_random_user_api():
    """练习2：获取随机用户（之前失败的）"""
    data = api_request(
        "https://randomuser.me/api/",
        "随机用户API（之前失败的）"
    )

    if data:
        user = data['results'][0]
        print(f"\n👤 随机用户:")
        print(f"   姓名: {user['name']['first']} {user['name']['last']}")
        print(f"   性别: {user['gender']}")
        print(f"   邮箱: {user['email']}")
        print(f"   国家: {user['location']['country']}")
        print(f"   城市: {user['location']['city']}\n")


def test_cat_fact_api():
    """练习3：猫咪小知识"""
    data = api_request(
        "https://catfact.ninja/fact",
        "猫咪知识API"
    )

    if data:
        print(f"\n🐱 猫咪小知识:")
        print(f"   {data['fact']}\n")


def test_ip_info_api():
    """练习4：获取IP信息（有每日调用限制）"""
    data = api_request(
        "https://ipapi.co/json/",
        "IP信息API（注意：免费版有每日调用限制）"
    )

    if data:
        if 'error' in data:
            print(f"\n⚠️  API返回错误: {data.get('reason', '未知原因')}（可能今日额度用完）")
        else:
            print(f"\n🌍 网络信息:")
            print(f"   IP地址: {data.get('ip', 'N/A')}")
            print(f"   城市: {data.get('city', 'N/A')}")
            print(f"   地区: {data.get('region', 'N/A')}")
            print(f"   国家: {data.get('country_name', 'N/A')}")
            org = data.get('org', 'N/A')
            print(f"   运营商: {org[:50]}{'...' if len(org) > 50 else ''}\n")


def test_github_api():
    """练习5：GitHub用户信息（无需认证，但限60次/小时）"""
    # 查询GitHub用户
    username = "torvalds"  # Linux创始人

    data = api_request(
        f"https://api.github.com/users/{username}",
        f"GitHub API - 查询用户 {username}（注意：未认证限60次/小时）"
    )

    if data:
        if 'message' in data and 'rate limit' in data.get('message', '').lower():
            print(f"\n⚠️  GitHub API 调用次数用完了，需要等一会儿再试")
        else:
            print(f"\n💻 GitHub用户: {data['login']}")
            print(f"   姓名: {data.get('name', 'N/A')}")
            print(f"   粉丝: {data['followers']}")
            print(f"   仓库数: {data['public_repos']}")
            bio = data.get('bio') or '无简介'
            print(f"   简介: {bio}\n")


def test_crypto_price_api():
    """练习6：加密货币价格"""
    data = api_request(
        "https://api.coinbase.com/v2/exchange-rates?currency=BTC",
        "比特币价格API"
    )

    if data:
        rates = data['data']['rates']
        print(f"\n💰 比特币价格:")
        print(f"   USD: ${float(rates['USD']):,.2f}")
        print(f"   CNY: ¥{float(rates['CNY']):,.2f}\n")


if __name__ == "__main__":
    print("\n" + "🚀" * 30)
    print("API实战练习 - V2RayN配置版")
    print("🚀" * 30 + "\n")

    # 运行所有练习
    test_joke_api()
    test_random_user_api()
    test_cat_fact_api()
    test_ip_info_api()
    test_github_api()
    test_crypto_price_api()

    # 总结
    print("\n" + "=" * 60)
    print("🎉 代理问题解决！")
    print("=" * 60)
    print("""
✅ 成功配置: HTTP代理 127.0.0.1:10808
✅ 可以访问之前失败的API了
✅ 理解了API和API Key的概念
✅ 掌握了代理配置方法

📚 今天学到的核心技能:
1. API的本质 - 就是一个URL，发请求得数据
2. 代理配置 - V2RayN的HTTP端口是10808
3. 错误处理 - try-except捕获网络异常
4. JSON解析 - response.json() 获取数据

💡 下一步学习:
1. 学习POST请求（创建数据）
2. 学习API认证（需要API Key的接口）
3. 学习API限流和分页
4. 开始LeetCode刷题（算法准备）
    """)
    print("=" * 60)
