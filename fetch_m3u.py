import requests
import sys

def fetch_m3u_via_vercel(output_file):
    # 【关键】替换为你自己的 Vercel 部署地址
    vercel_proxy_url = "https://你的项目名.vercel.app/api/proxy"

    print(f"🚀 正在通过 Vercel 私有代理获取数据...")

    try:
        response = requests.get(vercel_proxy_url, timeout=15)

        if response.status_code == 200:
            content = response.text
            # 强制转码处理，防止乱码
            try:
                content = content.encode('utf-8').decode('utf-8')
            except:
                pass

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ 获取成功！文件大小: {len(content)} bytes")
            print(f"💾 已保存至: {output_file}")
        else:
            raise Exception(f"Vercel 返回错误状态码: {response.status_code}")

    except Exception as e:
        print(f"❌ 失败: {e}")
        sys.exit(1)

# 执行
fetch_m3u_via_vercel("migu.m3u")
