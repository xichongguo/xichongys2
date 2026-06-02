import requests

def fetch_m3u_direct(url, output_file):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        print(f"正在获取直播源: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = response.apparent_encoding
        
        # 直接将获取到的文本内容作为 m3u 内容
        m3u_content = response.text
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(m3u_content)
            
        print(f"✅ 获取成功！m3u 文件已保存为: {output_file}")

    except Exception as e:
        print(f"❌ 发生错误: {e}")

# 替换成你的链接
url = "http://www.52top.com.cn:678/downloads/migu.txt"
fetch_m3u_direct(url, "migu.m3u")
