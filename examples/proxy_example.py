import asyncio
import truedriver as td

async def test_proxy(proxy_url):
    """Test a proxy by printing the IP address as seen by httpbin.org/ip"""
    try:
        browser = await td.start(proxy=proxy_url, headless=False, timeout=30)
        tab = await browser.get("https://httpbin.org/ip", timeout=15)
        await asyncio.sleep(2)
        content = await tab.get_content()
        import json
        try:
            data = json.loads(content)
            print(f"Proxy IP: {data.get('origin', 'unknown')}")
        except Exception:
            print(f"Response: {content[:100]}...")
        await browser.stop()
    except Exception as e:
        print(f"Proxy test failed: {e}")

if __name__ == "__main__":
    # Replace with your proxy in format: username:password@server:port
    proxy = "your-username:your-password@your-proxy-server:port"
    asyncio.run(test_proxy(proxy))