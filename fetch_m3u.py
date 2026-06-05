import requests
import time
import sys

def fetch_m3u_direct(url, output_file, max_retries=3):
    """
    下载 M3U 直播源并保存，包含重试机制以应对网络不稳定
    :param url: 直播源链接
    :param output_file: 保存的文件名
    :param max_retries: 最大重试次数
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # 循环重试逻辑
    for attempt in range(1, max_retries + 1):
        try:
            print(f"🚀 [第 {attempt} 次尝试] 正在获取直播源: {url}", flush=True)

            # 发起请求，设置超时时间为 15 秒
            response = requests.get(url, headers=headers, timeout=15)

            # 检查 HTTP 状态码 (如 404, 500)
            response.raise_for_status()

            # 自动识别编码，防止中文乱码
            response.encoding = response.apparent_encoding or 'utf-8'
            m3u_content = response.text

            # 写入文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(m3u_content)

            print(f"✅ 获取成功！m3u 文件已保存为: {output_file}", flush=True)
            return True  # 成功后直接返回，不再重试

        except requests.exceptions.ConnectionError as e:
            print(f"⚠️ [连接错误] 无法连接到服务器: {e}", flush=True)
        except requests.exceptions.Timeout:
            print(f"⚠️ [超时错误] 请求超时，服务器响应太慢", flush=True)
        except requests.exceptions.HTTPError as e:
            print(f"❌ [HTTP错误] 服务器返回错误状态码: {e}", flush=True)
            break  # 如果是 404 这种硬伤，重试也没用，直接跳出
        except Exception as e:
            print(f"❌ [未知错误] 发生异常: {e}", flush=True)

        # 如果不是最后一次尝试，则等待几秒后重试
        if attempt < max_retries:
            wait_time = 5 * attempt  # 递增等待时间 (5s, 10s...)
            print(f"💤 等待 {wait_time} 秒后重试...", flush=True)
            time.sleep(wait_time)

    print("💀 最终结果: 经过多次尝试仍无法获取直播源，任务失败。", flush=True)
    return False

if __name__ == '__main__':
    # 配置区域
    SOURCE_URL = "http://www.52top.com.cn:678/downloads/migu.txt"
    OUTPUT_FILE = "migu.m3u"

    # 执行下载
    success = fetch_m3u_direct(SOURCE_URL, OUTPUT_FILE)

    # 根据结果设置退出码 (用于 GitHub Actions 判断任务是否成功)
    if not success:
        sys.exit(1)
