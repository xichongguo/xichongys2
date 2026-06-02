import requests
import sys

def fetch_m3u_direct(url, output_file):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Encoding': 'identity'  # 关键：防止服务器返回 gzip 压缩数据导致乱码
        }

        print(f"正在获取直播源: {url}")
        response = requests.get(url, headers=headers, timeout=15)

        # --- 核心修复逻辑开始 ---
        content = None

        # 策略1：优先尝试 GBK/GB2312 (国内网站最常用的中文编码)
        try:
            content = response.content.decode('gbk')
            print("🔍 使用 GBK 编码解码成功")
        except (UnicodeDecodeError, LookupError):
            pass

        # 策略2：如果 GBK 失败，尝试 UTF-8
        if not content:
            try:
                content = response.content.decode('utf-8')
                print("🔍 使用 UTF-8 编码解码成功")
            except UnicodeDecodeError:
                pass

        # 策略3：最后兜底，使用 apparent_encoding (自动检测)
        if not content:
            try:
                response.encoding = response.apparent_encoding
                content = response.text
                print(f"🔍 使用自动检测编码 ({response.encoding}) 解码")
            except Exception:
                pass

        # 如果以上都失败，使用 errors='ignore' 强制转换，防止报错中断
        if not content:
            content = response.content.decode('utf-8', errors='ignore')
            print("⚠️ 所有编码尝试失败，已强制忽略错误字符")
        # --- 核心修复逻辑结束 ---

        # 写入文件 (必须显式指定 utf-8，确保 GitHub 仓库显示正常)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ 获取成功！文件已保存为: {output_file}")
        # 打印前几行确认是否正常
        print("--- 预览前3行 ---")
        for line in content.split('\n')[:3]:
            print(line)

    except Exception as e:
        print(f"❌ 发生致命错误: {e}")
        # 让 Actions 知道出错了，变红而不是假绿
        sys.exit(1)

# 你的链接
url = "http://www.52top.com.cn:678/downloads/migu.txt"
fetch_m3u_direct(url, "migu.m3u")
