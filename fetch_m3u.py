import requests
import sys

def fetch_m3u_via_proxy(url, output_file):
    # 定义几个常用的 CORS 代理 (如果第一个不行，换第二个)
    proxies = [
        f"https://corsproxy.io/?{url}",
        f"https://api.codetabs.com/v1/proxy?quest={url}"
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    content = None
    used_proxy = ""

    # 循环尝试不同的代理
    for proxy_url in proxies:
        try:
            print(f"🚀 正在尝试通过代理获取: {proxy_url[:50]}...")
            response = requests.get(proxy_url, headers=headers, timeout=15)

            if response.status_code == 200:
                used_proxy = proxy_url
                # --- 核心修复：强制使用 GBK 解码 ---
                # 国内老旧接口通常使用 GBK 或 GB2312 编码
                try:
                    content = response.content.decode('gbk')
                    print("✅ 使用 GBK 编码解码成功！")
                except UnicodeDecodeError:
                    # 如果 GBK 失败，回退到自动检测
                    response.encoding = response.apparent_encoding
                    content = response.text
                    print(f"⚠️ GBK 失败，已切换至自动检测编码: {response.encoding}")

                break  # 获取成功，跳出循环
            else:
                print(f"⚠️ 代理返回状态码: {response.status_code}，尝试下一个...")

        except Exception as e:
            print(f"❌ 当前代理连接失败: {e}")
            continue

    # 写入文件
    if content:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"💾 文件已成功保存为: {output_file}")
    else:
        # 如果所有代理都失败了，抛出异常让 Actions 变红
        raise Exception("所有代理均无法连接到目标地址，请检查源链接是否失效。")

# 你的原始目标地址
target_url = "http://www.52top.com.cn:678/downloads/migu.txt"

try:
    fetch_m3u_via_proxy(target_url, "migu.m3u")
except Exception as e:
    print(f"\n🔴 致命错误: {e}")
    sys.exit(1)  # 强制退出并报错
