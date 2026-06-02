import requests
import os

def main():
    # 目标地址
    target_url = "http://www.52top.com.cn:678/downloads/migu.txt"

    # 【核心】使用 AllOrigins 代理，解决 GitHub Actions 无法访问国内非标准端口的问题
    proxy_url = f"https://api.allorigins.win/raw?url={target_url}"

    print(f"正在尝试通过代理获取: {target_url}")

    try:
        response = requests.get(proxy_url, timeout=30)
        response.raise_for_status()

        content = response.text

        # 简单的校验，防止下载到空文件或HTML报错页面
        if len(content) < 100 or "EXTM3U" not in content:
            raise Exception("下载的内容似乎无效或不是M3U格式")

        # 写入文件
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(content)

        print("✅ 成功更新 playlist.m3u")

    except Exception as e:
        print(f"❌ 失败: {e}")
        # 如果失败，不退出代码1，防止整个Action标红（可选）
        # exit(1)

if __name__ == "__main__":
    main()
