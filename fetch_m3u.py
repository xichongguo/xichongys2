import requests
import sys

def main():
    # 原始目标地址 (GitHub 无法直连)
    target_url = "http://www.52top.com.cn:678/downloads/migu.txt"

    # 【核心修改】使用 AllOrigins 公共代理来抓取数据，绕过网络限制
    proxy_url = f"https://api.allorigins.win/raw?url={target_url}"

    print(f"🚀 正在尝试通过代理获取直播源...", flush=True)
    print(f"🔗 真实目标: {target_url}", flush=True)

    try:
        # 设置超时时间，防止卡死
        response = requests.get(proxy_url, timeout=30)

        # 检查状态码
        if response.status_code == 200:
            content = response.text

            # 简单校验内容是否包含 m3u 特征
            if "#EXTM3U" in content or "#EXTINF" in content:
                print("✅ 获取成功！正在写入文件...", flush=True)
                with open("migu.m3u", "w", encoding="utf-8") as f:
                    f.write(content)
                print("💾 文件已保存为 migu.m3u", flush=True)
            else:
                print("❌ 获取的内容格式似乎不对，不是标准的 M3U 文件。", flush=True)
                sys.exit(1)
        else:
            print(f"❌ 请求失败，状态码: {response.status_code}", flush=True)
            sys.exit(1)

    except Exception as e:
        print(f"❌ 发生致命错误: {e}", flush=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
