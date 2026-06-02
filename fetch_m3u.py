import requests
import sys
import os

def fetch_m3u_direct(url, output_file):
    print(f"正在获取直播源: {url}", flush=True)
    
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
            proxies=proxies,
            timeout=(10, 20)  # 连接超时10秒，读取超时20秒
        )
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        print(f"✅ 获取成功！m3u 文件已保存为: {output_file}", flush=True)

    except requests.exceptions.ConnectionError as e:
        print(f"❌ 连接错误: {e}", flush=True)
        print("提示: [Errno 101] 通常意味着网络不可达。", flush=True)
        print("1. 检查是否被防火墙拦截了非标准端口(678)。", flush=True)
        print("2. 尝试在终端运行 'telnet www.52top.com.cn 678' 测试连通性。", flush=True)
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
