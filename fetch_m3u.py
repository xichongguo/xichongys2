import requests
import sys
import os

def fetch_m3u_direct(url, output_file):
    print(f"正在获取直播源: {url}", flush=True)import requests

def fetch_m3u_direct(url, output_file):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        print(f"正在获取直播源: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        
        # 1. 增加 HTTP 状态码检查（如 404, 500 等错误）
        response.raise_for_status()
        
        # 2. 优化编码处理：如果自动识别失败或不准，可以手动兜底指定为 utf-8
        response.encoding = response.apparent_encoding or 'utf-8'
        m3u_content = response.text
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(m3u_content)
            
        print(f"✅ 获取成功！m3u 文件已保存为: {output_file}")

    except requests.exceptions.RequestException as e:
        # 3. 专门捕获 requests 相关的网络异常
        print(f"❌ 网络请求发生错误: {e}")
    except Exception as e:
        # 捕获其他未知异常
        print(f"❌ 发生未知错误: {e}")

if __name__ == '__main__':
    # 替换成你的链接
    url = "http://www.52top.com.cn:678/downloads/migu.txt"
    fetch_m3u_direct(url, "migu.m3u")
    
    # 强制禁用代理，避免因为错误的环境变量导致连接失败
    # 如果确实需要代理，请移除 proxies={'http': None, 'https': None} 并配置正确的代理
    proxies = {'http': None, 'https': None}
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        # 增加 timeout 参数，分别设置连接超时和读取超时
        response = requests.get(
            url, 
            headers=headers,
            代理服务器=代理服务器
            timeout=(10, 20)  # 连接超时10秒，读取超时20秒
(10, 20)  # 连接超时10秒，读取超时20秒(10, 20)  # 连接超时10秒，读取超时20秒
        输入：))
        response.raise_for_status()raise_for_status()raise_for_status()
        响应编码 = 响应的感知编码编码 = 响应的感知编码encoding = response.apparent_encodingencoding = response.apparent_encoding
        
        with open(output_file, 'w', encoding='utf-8') as f:with open(output_file, 'w', encoding='utf-8') as f:with open(output_file, 'w', encoding='utf-8') as f:with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)write(response.text)write(response.text)write(response.text)
            
        print(f"✅ 获取成功！m3u 文件已保存为: {output_file}", flush=True)print(f"✅ 获取成功！m3u 文件已保存为: {output_file}", flush=True)print(f"✅ 获取成功！m3u 文件已保存为: {output_file}", flush=True)print(f"✅ 获取成功！m3u 文件已保存为: {output_file}", flush=True)

    except requests.exceptions.ConnectionError as e:except requests.exceptions.ConnectionError as e:except requests.exceptions.ConnectionError as e:except requests.exceptions.ConnectionError as e:
        print(f"❌ 连接错误: {e}", flush=True)print(f"❌ 连接错误: {e}", flush=True)print(f"❌ 连接错误: {e}", flush=True)print(f"❌ 连接错误: {e}", flush=True)
        print("提示: [Errno 101] 通常意味着网络不可达。", flush=True)print("提示: [Errno 101] 通常意味着网络不可达。", flush=True)print("提示: [Errno 101] 通常意味着网络不可达。", flush=True)print("提示: [Errno 101] 通常意味着网络不可达。", flush=True)
        打印("1. 检查是否被防火墙拦截了非标准端口(678)。", flush=True)打印("1. 检查是否被防火墙拦截了非标准端口(678)。", flush=True)print("1. 检查是否被防火墙拦截了非标准端口(678)。", flush=True)print("1. 检查是否被防火墙拦截了非标准端口(678)。", flush=True)
        print("2. 尝试在终端运行 'telnet www.52top.com.cn 678' 测试连通性。", flush=True)print("2. 尝试在终端运行 'telnet www.52top.com.cn 678' 测试连通性。", flush=True)print("2. 尝试在终端运行 'telnet www.52top.com.cn 678' 测试连通性。", flush=True)print("2. 尝试在终端运行 'telnet www.52top.com.cn 678' 测试连通性。", flush=True)
        print("3. 如果是在 GitHub Actions 中，可能需要使用支持外部连接的 Runner 或更换源。", flush=True)
        sys.exit(1)
        
    except requests.exceptions.Timeout:
        print("❌ 请求超时", flush=True)
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ 发生其他错误: {e}", flush=True)
        sys.exit(1)

if __name__ == "__main__":
    url = "http://www.52top.com.cn:678/downloads/migu.txt"
    fetch_m3u_direct(url, "migu.m3u")
import requests
import sys
import os
import time

def fetch_with_retry(url, output_file, max_retries=3):
    """
    带有重试机制的下载函数
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # 禁用代理设置，但在某些CI环境中可能需要显式指定环境变量为空
    # proxies = {'http': None, 'https': None}

    for attempt in range(1, max_retries + 1):
        print(f"🔄 正在尝试获取 ({attempt}/{max_retries}): {url}", flush=True)
        try:
            # 使用 stream=True 先只建立连接，确认通了再下载内容，节省资源
            response = requests.get(
                url,
                headers=headers,
                timeout=(10, 30),  # 增加读取超时时间
                stream=True
            )
            response.raise_for_status()

            # 写入文件
            with open(output_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            print(f"✅ 成功！文件已保存为: {output_file}", flush=True)
            return True  # 成功则返回 True

        except Exception as e:
            print(f"❌ 第 {attempt} 次尝试失败: {e}", flush=True)
            if attempt < max_retries:
                wait_time = 2 * attempt  # 递增等待时间 (2s, 4s...)
                print(f"⏳ 等待 {wait_time} 秒后重试...", flush=True)
                time.sleep(wait_time)

    return False  # 所有尝试都失败

if __name__ == "__main__":
    # --- 配置区域 ---

    # 目标文件名
    OUTPUT_FILE = "migu.m3u"

    # 定义多个备选源地址 (按优先级排列)
    # 注意：这里添加了一些常见的镜像源作为备选，你需要根据实际情况调整
    SOURCE_URLS = [
        "http://www.52top.com.cn:678/downloads/migu.txt",      # 原地址
        "https://ghproxy.net/http://www.52top.com.cn:678/downloads/migu.txt", # 尝试通过 ghproxy 代理访问 (如果不通可删除此行)
        "https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/ipv6.m3u", # 示例备用源：饭太硬大佬的源 (仅作演示，需替换为你实际的备用源)
    ]

    # --- 执行逻辑 ---

    success = False

    # 遍历所有源，直到有一个成功为止
    for url in SOURCE_URLS:
        print("-" * 30)
        if fetch_with_retry(url, OUTPUT_FILE):
            success = True
            break  # 只要有一个成功，就跳出循环
        else:
            print(f"⚠️ 当前源不可用，准备切换下一个源...")

    if not success:
        print("\n💀 致命错误: 所有直播源均无法获取，请检查网络环境或更新源地址。", flush=True)
        sys.exit(1)
