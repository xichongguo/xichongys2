导入requests requests
import sys

def main():
    target_url = "http://www.52top.com.cn:678/downloads/migu.txt"
    # 依然保留代理作为双重保险
    proxy_url = f"https://api.allorigins.win/raw?url={target_url}"

    print(f"🚀 正在获取直播源...", flush=True)

    try:
        response = requests.get(proxy_url, timeout=30)
        if response.status_code == 200:
            content = response.text
            with open("output.m3u", "w", encoding="utf-8") as f:
                f.write(content)
            print("✅ 获取成功并已保存", flush=True)
        else:
            print(f"❌ 获取失败，状态码: {response.status_code}", flush=True)
            sys.exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}", flush=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
