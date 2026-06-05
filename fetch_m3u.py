import requests
import sys
import json
import time

def fetch_m3u_smart(url, output_file):
    # 定义请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # 策略列表：
    # 1. AllOrigins JSON API (通常比 raw 模式更稳定，能穿透部分防火墙)
    # 2. Corsproxy.io (备选)
    # 3. 直连 (虽然大概率失败，但作为最后兜底)
    strategies = [
        {
            "name": "AllOrigins (JSON)",
            "url": f"https://api.allorigins.win/get?url={requests.utils.quote(url)}"
        },
        {
            "name": "Corsproxy.io",
            "url": f"https://corsproxy.io/?{url}"
        },
        {
            "name": "Direct Connection",
            "url": url
        }
    ]

    content = None

    for strategy in strategies:
        print(f"\n🚀 正在尝试策略: [{strategy['name']}]")
        try:
            response = requests.get(strategy['name'] == "Direct Connection" and url or strategy['url'], headers=headers, timeout=20)

            if response.status_code == 200:
                # 针对 AllOrigins JSON 模式的特殊处理
                if strategy['name'] == "AllOrigins (JSON)":
                    data = response.json()
                    if data.get('status') and data['status'].get('http_code') == 200:
                        content = data['contents']
                        print("✅ AllOrigins JSON 解析成功！")
                    else:
                        print(f"⚠️ AllOrigins 返回了错误状态: {data}")
                        continue
                else:
                    # 普通模式直接获取文本
                    # 尝试检测编码，防止中文乱码
                    response.encoding = response.apparent_encoding
                    content = response.text
                    print(f"✅ [{strategy['name']}] 获取成功！")

                break  # 成功则跳出循环
            else:
                print(f"⚠️ 状态码异常: {response.status_code}")

        except Exception as e:
            print(f"❌ 连接失败: {e}")
            continue

    # 写入文件逻辑
    if content:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n💾 文件已保存: {output_file} (大小: {len(content)} 字符)")
    else:
        raise Exception("所有策略均失败。该源在 GitHub Actions 环境下可能完全不可达。")

# --- 主程序入口 ---
target_url = "http://www.52top.com.cn:678/downloads/migu.txt"

try:
    fetch_m3u_smart(target_url, "migu.m3u")
except Exception as e:
    print(f"\n🔴 致命错误: {e}")
    sys.exit(1)
