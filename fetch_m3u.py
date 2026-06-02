import requests
import sys
import os

# 定义目标原始链接
target_url = "http://www.52top.com.cn:678/downloads/migu.txt"

# 定义备用代理列表 (如果一个不行，试另一个)
proxies = [
    f"https://corsproxy.io/?{target_url}",
    f"https://api.codetabs.com/v1/proxy?quest={target_url}"
]

def download_content():
    content = None

    # 轮询尝试所有代理
    for proxy_url in proxies:
        print(f"正在尝试通过代理获取: {proxy_url}")
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(proxy_url, headers=headers, timeout=15)

            # 检查状态码是否为 200 OK
            if response.status_code == 200:
                text = response.text.strip()
                if len(text) > 100:  # 简单校验内容长度，防止下载到空页面或报错页
                    print("✅ 获取成功！")
                    return text
                else:
                    print(f"⚠️ 内容过短，可能获取失败 (长度: {len(text)})")
            else:
                print(f"⚠️ 状态码异常: {response.status_code}")

        except Exception as e:
            print(f"❌ 该代理请求失败: {str(e)}")
            continue

    # 如果循环结束还没拿到内容，说明全挂了
    raise Exception("所有代理均无法获取目标文件，请检查源地址是否存活。")

# --- 主程序入口 ---
if __name__ == "__main__":
    try:
        m3u_content = download_content()

        # 写入文件
        output_file = "migu.m3u" # 或者是你想保存的文件名
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(m3u_content)

        print(f"💾 文件已保存至: {output_file}")

    except Exception as e:
        # 关键：这里必须用 sys.exit(1) 告诉 GitHub 任务失败了
        print(f"\n\n🔴 致命错误: {e}")
        sys.exit(1)
