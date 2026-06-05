import requests
import sys

def fetch_m3u(url, output_file):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # 优先直连，其次使用备用代理
    urls_to_try = [
        url,  # 1. 优先尝试直接访问
        f"https://api.allorigins.win/raw?url={url}",  # 2. 备用代理1
        f"https://corsproxy.io/?{url}"  # 3. 备用代理2
    ]

    content = None
    for target in urls_to_try:
        try:
            print(f"🚀 正在尝试获取: {target[:60]}...")
            response = requests.get(target, headers=headers, timeout=(5, 15))

            if response.status_code == 200:
                # 处理国内老旧接口常见的 GBK 编码问题
                try:
                    content = response.content.decode('gbk')
                    print("✅ 获取成功，使用 GBK 编码解码！")
                except UnicodeDecodeError:
                    response.encoding = response.apparent_encoding
                    content = response.text
                    print(f"⚠️ GBK 失败，已切换至自动检测编码: {response.encoding}")
                break
            else:
                print(f"⚠️ 返回状态码: {response.status_code}，尝试下一个...")

        except requests.exceptions.Timeout:
            print(f"❌ 连接或读取超时，尝试下一个...")
            continue
        except Exception as e:
            print(f"❌ 当前连接失败: {e}，尝试下一个...")
            continue

    # 保存文件
    if content:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"💾 文件已成功保存为: {output_file}")
    else:
        raise Exception("所有方式均无法获取数据，请检查源链接是否失效。")

# 你的原始目标地址
target_url = "http://fn.gcl.de5.net:5908/gsh950428"

try:
    fetch_m3u(target_url, "migu.m3u")
except Exception as e:
    print(f"\n🔴 致命错误: {e}")
    sys.exit(1)  # 强制退出并报错
