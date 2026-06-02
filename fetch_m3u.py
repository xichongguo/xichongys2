import requests
import sys

def fetch_m3u_direct(url, output_file):
    try:
        # 强制实时输出，避免 GitHub Actions 缓冲导致看不到日志
        print(f"正在获取直播源: {url}", flush=True)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # 如果请求返回 404 或 500 等错误，直接抛出异常
        response.encoding = response.apparent_encoding
        
        m3u_content = response.text
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(m3u_content)
            
        print(f"✅ 获取成功！m3u 文件已保存为: {output_file}", flush=True)

    except Exception as e:
        print(f"❌ 发生错误: {e}", flush=True)
        sys.exit(1) # 发生错误时退出并返回状态码 1，让 GitHub Actions 知道任务失败了

if __name__ == "__main__":
    # 替换成你的链接
    url = "http://www.52top.com.cn:678/downloads/migu.txt"
    fetch_m3u_direct(url, "migu.m3u")
