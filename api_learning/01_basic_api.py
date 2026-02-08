"""
API学习 - 第一课：理解API的基本概念
作者: Chuyuan
日期: 2025-02-08
目标: 通过实际代码理解什么是API和API Key
"""

import requests
import json


def test_free_api():
    """
    练习1：调用免费API（不需要Key）
    使用JSONPlaceholder - 一个提供假数据的API，专门用来学习
    """
    print("=" * 60)
    print("练习1：调用免费API - 获取博客文章")
    print("=" * 60)

    # API地址（就像餐厅地址）
    url = "https://jsonplaceholder.typicode.com/posts/1"

    print(f"📡 正在请求: {url}")

    # 发送GET请求（就像你去餐厅点菜）
    response = requests.get(url)

    # 检查请求是否成功（200表示成功）
    if response.status_code == 200:
        data = response.json()
        print(f"✓ 请求成功！状态码: {response.status_code}")
        print(f"\n返回的数据:")
        print(f"  用户ID: {data['userId']}")
        print(f"  文章ID: {data['id']}")
        print(f"  标题: {data['title']}")
        print(f"  内容: {data['body'][:100]}...")  # 只显示前100个字符
    else:
        print(f"✗ 请求失败，状态码：{response.status_code}")


def test_multiple_requests():
    """
    练习2：发送多个请求 - 获取多篇文章
    """
    print("\n" + "=" * 60)
    print("练习2：批量获取数据")
    print("=" * 60)

    # 获取前5篇文章
    for i in range(1, 6):
        url = f"https://jsonplaceholder.typicode.com/posts/{i}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print(f"{i}. {data['title'][:40]}...")


def test_api_with_parameters():
    """
    练习3：带参数的API请求
    """
    print("\n" + "=" * 60)
    print("练习3：使用参数过滤数据")
    print("=" * 60)

    # 获取用户ID为1的所有文章
    url = "https://jsonplaceholder.typicode.com/posts"
    params = {'userId': 1}  # 参数：只要用户1的文章

    print(f"📡 请求URL: {url}")
    print(f"📋 参数: {params}")

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        print(f"✓ 找到 {len(data)} 篇文章")
        print(f"前3篇标题:")
        for i, post in enumerate(data[:3], 1):
            print(f"  {i}. {post['title']}")


def test_weather_api():
    """
    练习4：调用需要API Key的天气API

    ⚠️ 这个需要先注册：https://openweathermap.org/api
    注册后会得到一个免费的API Key（每天可以调用1000次）
    """
    print("\n" + "=" * 60)
    print("练习4：调用天气API（需要Key）")
    print("=" * 60)

    # TODO: 把这里替换成你自己的API Key
    api_key = "your_api_key_here"

    if api_key == "your_api_key_here":
        print("⚠️  还没有设置API Key")
        print("📝 步骤:")
        print("   1. 访问 https://openweathermap.org/api")
        print("   2. 点击 'Sign Up' 注册免费账号")
        print("   3. 在 'API keys' 页面复制你的key")
        print("   4. 把key粘贴到这个代码里")
        return

    # 查询重庆天气
    city = "Chongqing"
    url = "https://api.openweathermap.org/data/2.5/weather"

    # 注意：这里的appid参数就是API Key
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',  # 使用摄氏度
        'lang': 'zh_cn'  # 中文描述
    }

    print(f"📡 查询城市: {city}")

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        print(f"✓ 请求成功！")
        print(f"\n📍 {data['name']}")
        print(f"🌡️  温度: {data['main']['temp']}°C")
        print(f"🤔 体感: {data['main']['feels_like']}°C")
        print(f"☁️  天气: {data['weather'][0]['description']}")
        print(f"💨 风速: {data['wind']['speed']} m/s")
    else:
        print(f"✗ 请求失败")
        error = response.json()
        print(f"错误: {error.get('message', '未知错误')}")


if __name__ == "__main__":
    print("\n🚀 开始API学习之旅！\n")

    # 练习1: 基础GET请求
    test_free_api()

    # 练习2: 批量请求
    test_multiple_requests()

    # 练习3: 带参数的请求
    test_api_with_parameters()

    # 练习4: 需要API Key的请求
    test_weather_api()

    # 总结
    print("\n" + "=" * 60)
    print("📚 今天学到的核心概念:")
    print("=" * 60)
    print("1. API = 一个网址，你发请求，它返回数据")
    print("2. GET请求 = 向服务器要数据")
    print("3. 参数 = 告诉API你想要什么样的数据")
    print("4. API Key = 证明你身份的密码，防止别人滥用")
    print("5. 状态码 200 = 成功，401 = 没权限，404 = 没找到")
    print("=" * 60)

    print("\n💡 下一步:")
    print("   1. 安装requests库: pip install requests")
    print("   2. 运行这个文件看效果")
    print("   3. 去注册天气API的免费Key试试练习4")