import requests
import sys
import time

def fetch_m3u(url, output_file):
    # 模拟更真实的浏览器请求头，防止被国内老旧服务器拦截
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Referer': url,  # 添加 Referer 头，很多 IPTV 源需要这个
        'Host': url.split('/')  # 明确指定 Host 头
    }<websource>source_group_web_1</websource>

    # 尝试直连，并加入重试机制（应对 GitHub 到国内的网络波动）
    max_retries = 3
    content = None

    for attempt in range(max_retries):
        try:
            print(f"🚀 [尝试 {attempt + 1}/{max_retries}] 正在从 GitHub 服务器直连获取: {url}")
            response = requests.get(url, headers=headers, timeout=30)  # 跨境网络建议超时设长一点

            if response.status_code == 200:
                print("✅ 请求成功！状态码: 200")
                # 处理编码
                try:
                    content = response.content.decode('gbk')
                    print("✅ 使用 GBK 编码解码成功！")
                except UnicodeDecodeError:
                    response.encoding = response.apparent_encoding
                    content = response.text
                    print(f"⚠️ GBK 失败，已切换至自动检测编码: {response.encoding}")
                break
            else:
                print(f"⚠️ 返回状态码: {response.status_code}")
        except Exception as e:
            print(f"❌ 连接失败: {e}")
        
        if attempt < max_retries - 1:
            print("⏳ 等待 5 秒后重试...")
            time.sleep(5)

    # 写入文件
    if content:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"💾 文件已成功保存为: {output_file}")
        return True
    else:
        return False

target_url = "http://www.52top.com.cn:678/downloads/migu.txt"
print(f"📡 开始更新播放列表: {target_url}")

try:
    success = fetch_m3u(target_url, "migu.m3u")
    if not success:
        raise Exception("直连目标地址失败。可能是源站已关闭，或 GitHub 服务器无法连通该国内节点。")
except Exception as e:
    print(f"\n🔴 致命错误: {e}")
    sys.exit(1)
