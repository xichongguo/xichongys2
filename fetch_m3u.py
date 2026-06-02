导入 请求
导入 系统

定义 获取_m3u直接(网址, 输出文件):
    尝试:
        # 强制实时输出，避免 GitHub Actions 缓冲导致看不到日志
        打印(f"正在获取直播源: {url}", 冲洗=True)
        
        头部 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # 如果请求返回 404 或 500 等错误，直接抛出异常
        响应。编码 = 响应。感知编码
        
        m3u_content = response.文本
        
        以 打开(输出文件, 'w', 编码='utf-8') 作为 f:
            f.写(m3u内容)
            
        打印(f"✅ 获取成功！m3u 文件已保存为: {输出文件}", 冲洗=True)

    除了 异常 之外 作为 e:
        打印(f"❌ 发生错误: {e}", 冲洗=True)
        系统.退出(1) # 发生错误时退出并返回状态码 1，让 GitHub Actions 知道任务失败了

如果 __name__ == "__main__":
    # 替换成你的链接
    url = "http://www.52top.com.cn:678/downloads/migu.txt"
    fetch_m3u_direct(url, "migu.m3u")
