import requests
import json

def fetch_m3u_direct():
    # 目标原始网址
    target_url = "http://www.52top.com.cn:678/downloads/migu.txt"
    # 中转服务 API
    proxy_api = "https://api.allorigins.win/get"
    
    try:
        print(f"🚀 正在通过中转服务获取直播源: {target_man}", flush=True)
        
        # 构造请求参数
        params = {
            'url': target_url,
            'charset': 'UTF-8',
            'lang': 'zh-CN'
        }
        
        # 发送请求到中转服务
        response = requests.get(proxy_api, params=params, timeout=30)
        response.raise_for_status()
        
        # 解析 JSON 响应
        data = response.json()
        m3u_content = data['contents']
        
        # 写入文件
        output_file = "migu.m3u"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(m3u_content)
            
        print(f"✅ 恭喜！直播源获取成功，已保存为: {output_file}", flush=True)
        
    except Exception as e:
        print(f"❌ 获取直播源失败: {e}", flush=True)
        exit(1)

if __name__ == '__main__':
    fetch_m3u_direct()
