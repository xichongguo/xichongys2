import requests

def fetch_m3u_direct(url, output_file):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        # 加上 flush=True 可以让打印内容在日志或终端中实时显示
        print(f"正在获取直播源: {url}", flush=True)
        
        response = requests.get(url, headers=headers, timeout=10)
        
        # 检查 HTTP 状态码（如 404, 500 等）
        response.raise_for_status()
        
        # 自动识别编码，如果识别失败则默认使用 utf-8
        response.encoding = response.apparent_encoding or 'utf-8'
        m3u_content = response.text
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(m3u_content)
            
        print(f"✅ 获取成功！m3u 文件已保存为: {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求发生错误: {e}")
    except Exception as e:
        print(f"❌ 发生未知错误: {e}")

if __name__ == '__main__':
    # 替换成你的直播源链接
    url = "http://www.52top.com.cn:678/downloads/migu.txt"
    fetch_m3u_direct(url, "migu.m3u")
