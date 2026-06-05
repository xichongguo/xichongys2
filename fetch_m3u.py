import requests
import sys
import time

def fetch_m3u_via_proxy(url, output_file):
    # 推荐代理列表：按稳定性排序
    # 1. allorigins: 对国内站点兼容性较好，支持 raw 模式直接返回内容
    # 2. corsproxy.io: 备选
    # 3. thingproxy: 备选
    proxies = [
        f"https://api.allorigins.win/raw?url={url}",
        f"https://corsproxy.io/?{url}",
        f"https://thingproxy.freeboard.io/fetch/{url}"
    ]

    # 增强 Header 伪装，模拟真实浏览器行为
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': url,  # 重要：部分服务器校验 Referer
        'Connection': 'keep-alive',
    }

    content = None
    
    for proxy_url in proxies:
        try:
            print(f"🚀 正在尝试代理: {proxy_url[:60]}...")
            # 增加 timeout 到 30秒，GitHub Actions 网络有时波动
            response = requests.get(proxy_url, headers=headers, timeout=30)
            
            # 检查状态码
            if response.status_code == 200:
                # 额外检查：防止代理返回了“禁止访问”的 HTML 页面而不是 m3u 内容
                if 'm3u' in response.text.lower() or '#EXTM3U' in response.text or len(response.text) > 100:
                    used_proxy = proxy_url
                    print(f"✅ 代理连接成功，状态码: 200")
                    
                    # 编码处理
                    try:
                        # 先尝试 GBK，因为国内老旧站点常用
                        content = response.content.decode('gbk')
                        print("✅ 使用 GBK 解码成功")
                    except UnicodeDecodeError:
                        try:
                            content = response.content.decode('utf-8')
                            print("✅ 使用 UTF-8 解码成功")
                        except UnicodeDecodeError:
                            # 最后兜底
                            response.encoding = response.apparent_encoding
                            content = response.text
                            print(f"⚠️ 使用自动检测编码: {response.encoding}")
                    
                    break # 成功则跳出循环
                else:
                    print("⚠️ 返回内容疑似错误页面或为空，尝试下一个代理...")
            else:
                print(f"⚠️ 状态码: {response.status_code}，尝试下一个...")
                
        except Exception as e:
            print(f"❌ 连接失败: {type(e).__name__}: {str(e)[:100]}")
            continue

    if content:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"💾 文件已保存: {output_file} (大小: {len(content)} 字符)")
    else:
        raise Exception("所有代理均失败。可能原因：目标服务器屏蔽了所有已知代理IP，或源链接已失效。")

# 目标地址
target_url = "http://www.52top.com.cn:678/downloads/migu.txt"

if __name__ == "__main__":
    try:
        fetch_m3u_via_proxy(target_url, "migu.m3u")
    except Exception as e:
        print(f"\n🔴 致命错误: {e}")
        sys.exit(1)
