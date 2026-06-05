import requests
import sys

def fetch_m3u_via_proxy(url, output_file):
    # 替换为更多备用代理，或使用你自己的代理
    proxies = [
        f"https://corsproxy.io/?{url}",
        f"https://api.allorigins.win/raw?url={url}",
        f"https://thingproxy.freeboard.io/fetch/{url}"
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    content = None
    for proxy_url in proxies:
        try:
            print(f"🚀 正在尝试通过代理获取: {proxy_url[:60]}...")
            # 增加 timeout 的元组形式：(连接超时, 读取超时)
            response = requests.get(proxy_url, headers=headers, timeout=(5, 15))

            if response.status_code == 200:
                try:
                    content = response.content.decode('gbk')
                    print("✅ 使用 GBK 编码解码成功！")
                except UnicodeDecodeError:
                    response.encoding = response.apparent_encoding
                    content = response.text
                    print(f"⚠️ GBK 失败，已切换至自动检测编码: {response.encoding}")
                break
            else:
                print(f"⚠️ 代理返回状态码: {response.status_code}，尝试下一个...")

        except requests.exceptions.Timeout:
            print(f"❌ 代理连接或读取超时，尝试下一个...")
            continue
        except Exception as e:
            print(f"❌ 当前代理连接失败: {e}，尝试下一个...")
            continue

    if content:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"💾 文件已成功保存为: {output_file}")
    else:
        raise Exception("所有代理均无法连接到目标地址，请检查源链接是否失效或更换代理。")

target_url = "http://fn.gcl.de5.net:5908/gsh950428"
try:
    fetch_m3u_via_proxy(target_url, "migu.m3u")
except Exception as e:
    print(f"\n🔴 致命错误: {e}")
    sys.exit(1)
