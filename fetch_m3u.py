import requests
import sys

def fetch_data():
    # 【重要】请将下面的链接替换为你在 Cloudflare 获取的真实链接
    # 必须包含 https:// 开头，且以 .workers.dev/ 结尾
    proxy_url = "https://你的项目名.你的账户名.workers.dev/"

    print(f"正在尝试通过中转站获取数据: {proxy_url} ...")

    try:
        # 发起请求，设置超时时间为 15 秒
        response = requests.get(proxy_url, timeout=15)

        # 检查状态码是否为 200 (成功)
        if response.status_code == 200:
            content = response.text
            print("✅ 获取成功！数据长度:", len(content))

            # 这里可以将 content 写入文件，例如：
            with open("migu.txt", "w", encoding="utf-8") as f:
                f.write(content)
            print("💾 已保存到 migu.txt")
            return True
        else:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            return False

    except requests.exceptions.MissingSchema:
        print("❌ 致命错误：URL 格式不正确！")
        print("   请检查是否包含了 'https://' 开头。")
        print(f"   当前填写的 URL: '{proxy_url}'")
        return False

    except requests.exceptions.ConnectionError as e:
        print(f"❌ 连接失败 (DNS 解析错误或网络不通): {e}")
        print("   请检查 Cloudflare Worker 是否已保存并部署。")
        print("   请检查 URL 是否复制完整，不要包含多余空格。")
        return False

    except Exception as e:
        print(f"❌ 发生未知错误: {e}")
        return False

if __name__ == "__main__":
    success = fetch_data()
    if not success:
        sys.exit(1)
