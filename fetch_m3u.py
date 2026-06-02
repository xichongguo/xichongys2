import requests
import sys
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def fetch_m3u_direct(url, output_file, max_retries=3):
    try:
        print(f"正在获取直播源: {url}", flush=True)
        
        # 创建带重试机制的会话
        session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/plain,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        # 尝试多种超时设置
        for timeout in [10, 15, 20]:
            try:
                response = session.get(url, headers=headers, timeout=timeout)
                response.raise_for_status()
                break
            except requests.exceptions.Timeout:
                print(f"超时设置 {timeout} 秒失败，尝试更长的超时...", flush=True)
                continue
        
        response.encoding = response.apparent_encoding or 'utf-8'
        m3u_content = response.text
        
        # 验证内容是否为有效的 M3U 格式
        if not m3u_content.strip().startswith('#EXTM3U'):
            print("⚠️  警告：获取的内容可能不是标准的 M3U 格式", flush=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(m3u_content)
            
        print(f"✅ 获取成功！文件已保存为: {output_file}", flush=True)
        print(f"文件大小: {len(m3u_content)} 字符", flush=True)
        
        # 显示前几行内容预览
        lines = m3u_content.split('\n')[:5]
        print("内容预览:", flush=True)
        for line in lines:
            if line.strip():
                print(f"  {line[:100]}..." if len(line) > 100 else f"  {line}", flush=True)

    except requests.exceptions.ConnectionError as e:
        print(f"❌ 连接错误: {e}", flush=True)
        print("&zwnj;**建议检查：**&zwnj;", flush=True)
        print("1. 网络连接是否正常", flush=True)
        print("2. 目标服务器是否可访问", flush=True)
        print("3. 防火墙是否允许访问端口 678", flush=True)
        sys.exit(1)
        
    except requests.exceptions.Timeout:
        print("❌ 请求超时：服务器响应时间过长", flush=True)
        print("&zwnj;**建议：**&zwnj;", flush=True)
        print("1. 检查网络速度", flush=True)
        print("2. 尝试更换网络环境", flush=True)
        print("3. 联系资源提供方确认服务状态", flush=True)
        sys.exit(1)
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP 错误: {e}", flush=True)
        print(f"状态码: {response.status_code if 'response' in locals() else '未知'}", flush=True)
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ 发生未知错误: {e}", flush=True)
        sys.exit(1)

if __name__ == "__main__":
    # 可以尝试多个备选源
    url_sources = [
        "http://www.52top.com.cn:678/downloads/migu.txt",
        # 添加其他备选源
    ]
    
    for url in url_sources:
        print(f"尝试源: {url}", flush=True)
        try:
            fetch_m3u_direct(url, "migu.m3u")
            break  # 成功则退出循环
        except SystemExit:
            print(f"源 {url} 失败，尝试下一个...", flush=True)
            continue
