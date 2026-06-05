import requests
import os

def fetch_m3u_direct(url, output_file):
    """
    下载 M3U 直播源并保存
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        # flush=True 确保在 GitHub Actions 或 Docker 中能立即看到打印信息
        print(f"🚀 [开始] 正在获取直播源: {url}", flush=True)

        response = requests.get(url, headers=headers, timeout=15)

        # 检查 HTTP 状态码（如 404, 500 等）
        response.raise_for_status()

        # 自动识别编码，防止中文乱码
        # apparent_encoding 比 chardet 更准确，如果失败则回退到 utf-8
        response.encoding = response.apparent_encoding or 'utf-8'
        m3u_content = response.text

        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(m3u_content)

        file_size = os.path.getsize(output_file)
        print(f"✅ [成功] m3u 文件已保存为: {output_file} (大小: {file_size} bytes)", flush=True)
        return True

    except requests.exceptions.RequestException as e:
        print(f"❌ [网络错误] 请求发生异常: {e}", flush=True)
    except Exception as e:
        print(f"❌ [未知错误] 发生异常: {e}", flush=True)

    return False

# --- 主执行逻辑 ---
# 为了保证在任何环境（包括 GitHub Actions）下都能运行，
# 我们将配置放在这里，并显式调用函数。

if __name__ == '__main__':
    # 目标链接 (来自你的原始代码)
    target_url = "http://www.52top.com.cn:678/downloads/migu.txt"
    # 保存文件名 (参考截图中的 migu.m3u)
    save_name = "migu.m3u"

    # 执行下载
    success = fetch_m3u_direct(target_url, save_name)

    if not success:
        # 在某些 CI 环境中，返回非 0 退出码可以标记任务失败
        exit(1)
