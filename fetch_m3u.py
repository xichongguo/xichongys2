import requests
import sys

def fetch_m3u_content():
    # 原始目标地址
    target_url = "http://www.52top.com.cn:678/downloads/migu.txt"

    # 使用 AllOrigins 作为代理中转，解决 GitHub Actions 无法访问特定端口的问题
    proxy_url = f"https://api.allorigins.win/raw?url={target_url}"

    print(f"🚀 正在尝试获取直播源...", flush=True)
    print(f"🔗 目标地址: {target_url}", flush=True)

    try:
        # 设置超时时间，防止卡死
        response = requests.get(proxy_url, timeout=30)

        # 检查状态码
        if response.status_code == 200:
            content = response.text
            # 简单的校验，确保下载到了类似 m3u 的内容
            if len(content) > 100:
                print(f"✅ 成功获取内容，长度: {len(content)} 字符", flush=True)
                return content
            else:
                print("❌ 获取到的内容过短，可能下载失败", flush=True)
                return None
        else:
            print(f"❌ 代理服务器返回错误状态码: {response.status_code}", flush=True)
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求发生异常: {e}", flush=True)
        return None

if __name__ == "__main__":
    content = fetch_m3u_content()

    if content:
        output_file = "migu.m3u"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"💾 文件已保存至: {output_file}", flush=True)
    else:
        print("⚠️ 未能获取有效内容，脚本将退出并报错", flush=True)
        sys.exit(1)
