import requests

def fetch_m3u_direct(url, output_file):
    try:
        # 构造 jsDelivr 中转地址
        # 原理：让 jsDelivr 服务器去请求目标网站，然后我们从 jsDelivr 下载
        cdn_url = f"https://cdn.jsdelivr.net/gh/xichongguo/xichongys2@main/{url.split('/')[-1]}"

        # 如果原地址不是 github raw 格式，这里使用通用的代理抓取逻辑
        # 针对你这个特定端口被封的情况，我们尝试使用公共代理服务或更换 UA
        # 但最稳妥的方式是：既然这是你的仓库，建议你把 migu.txt 放到一个能访问的地方
        # 或者使用下面的 "AllOrigins" 免费代理接口来穿透防火墙

        proxy_url = f"https://api.allorigins.win/raw?url={requests.utils.quote(url)}"

        print(f"正在通过代理获取直播源...", flush=True)
        print(f"目标地址: {url}", flush=True)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        # 尝试使用代理接口获取
        response = requests.get(proxy_url, headers=headers, timeout=20)

        if response.status_code == 200:
            content = response.text
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 获取成功！已保存为: {output_file}", flush=True)
        else:
            raise Exception(f"代理返回错误状态码: {response.status_code}")

    except Exception as e:
        print(f"❌ 获取失败: {str(e)}", flush=True)
        raise e

if __name__ == "__main__":
    target_url = "http://www.52top.com.cn:678/downloads/migu.txt"
    output_name = "migu.m3u"
    fetch_m3u_direct(target_url, output_name)
