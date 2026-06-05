import requests
import sys
import time

def fetch_m3u(url, output_file):
    """
    通过 Cloudflare Worker 中转获取 M3U 文件
    :param url: Cloudflare Worker 的地址
    :param output_file: 保存的文件名
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    max_retries = 3
    content = None

    for attempt in range(max_retries):
        try:
            print(f"🚀 [尝试 {attempt + 1}/{max_retries}] 正在通过中转站获取数据...")
            # 这里的 url 应该是你的 Cloudflare Worker 地址
            response = requests.get(url, headers=headers, timeout=30)

            if response.status_code == 200:
                content = response.text
                print(f"✅ 获取成功！数据长度: {len(content)} 字符")
                break
            else:
                print(f"⚠️ 状态码异常: {response.status_code}")

        except Exception as e:
            print(f"❌ 连接失败: {e}")
            if attempt < max_retries - 1:
                print("⏳ 等待 5 秒后重试...")
                time.sleep(5)

    if content:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"💾 文件已保存至: {output_file}")
        return True
    else:
        print("🔴 致命错误: 所有尝试均失败，请检查 Cloudflare Worker 是否部署正确。")
        return False

if __name__ == "__main__":
    # 【重要】请将下面的 URL 替换为你第一步中获得的 Cloudflare Worker 地址
    WORKER_URL = "https://你的-worker-名称.你的账户名.workers.dev"

    OUTPUT_FILE = "migu_playlist.m3u"

    success = fetch_m3u(WORKER_URL, OUTPUT_FILE)
    if not success:
        sys.exit(1)
