import sys
from playwright.sync_api import sync_playwright

def fetch_m3u_with_browser(url, output_file):
    print(f"🚀 正在启动浏览器获取: {url}")
    
    with sync_playwright() as p:
        # 启动无头浏览器
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # 访问目标地址，设置合理的超时时间
            response = page.goto(url, timeout=30000, wait_until="networkidle")
            
            if response and response.status == 200:
                # 获取页面渲染后的完整文本内容
                content = page.inner_text("body")
                
                # 如果接口返回的是纯文本（如 m3u 格式），inner_text 可能不够，
                # 我们可以尝试获取原始响应体
                raw_content = response.text()
                
                # 优先使用原始响应体，处理国内老旧接口常见的 GBK 编码问题
                try:
                    final_content = raw_content.encode('latin1').decode('gbk')
                    print("✅ 获取成功，使用 GBK 编码解码！")
                except Exception:
                    final_content = raw_content
                    print("✅ 获取成功，使用默认编码！")

                # 保存为 m3u 文件
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(final_content)
                print(f"💾 文件已成功保存为: {output_file}")
            else:
                status = response.status if response else "No Response"
                raise Exception(f"浏览器请求失败，状态码: {status}")

        except Exception as e:
            print(f"❌ 浏览器获取发生异常: {e}")
            raise
        finally:
            browser.close()

target_url = "http://fn.gcl.de5.net:5908/gsh950428"

try:
    fetch_m3u_with_browser(target_url, "migu.m3u")
except Exception as e:
    print(f"\n🔴 致命错误: {e}")
    sys.exit(1)
