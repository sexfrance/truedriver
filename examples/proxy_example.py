"""
Simple proxy usage examples for truedriver.

This example shows how to use proxies with truedriver in various formats.
Proxy authentication is handled via URL encoding (like Playwright) for maximum compatibility.
"""

import asyncio
import truedriver as uc


async def example_simple_proxy():
    """Example using a simple proxy without authentication"""
    print("Example 1: Simple proxy without authentication")
    
    # Simple format: ip:port
    browser = await uc.start(proxy="proxy.example.com:8080")
    
    # Or with protocol
    # browser = await uc.start(proxy="http://proxy.example.com:8080")
    
    tab = await browser.get("https://httpbin.org/ip")
    await asyncio.sleep(2)
    await browser.stop()


async def example_authenticated_proxy_string():
    """Example using authenticated proxy with string format"""
    print("Example 2: Authenticated proxy (string format)")
    
    # String format with auth: user:pass@ip:port
    browser = await uc.start(proxy="username:password@proxy.example.com:8080")
    
    # Or with protocol
    # browser = await uc.start(proxy="http://username:password@proxy.example.com:8080")
    
    tab = await browser.get("https://httpbin.org/ip")
    await asyncio.sleep(2)
    await browser.stop()


async def example_authenticated_proxy_dict():
    """Example using authenticated proxy with dict format"""
    print("Example 3: Authenticated proxy (dict format)")
    
    proxy_config = {
        "server": "proxy.example.com:8080",
        "username": "myuser",
        "password": "mypass"
    }
    
    browser = await uc.start(proxy=proxy_config)
    tab = await browser.get("https://httpbin.org/ip")
    await asyncio.sleep(2)
    await browser.stop()


async def example_working_with_your_code():
    """Example showing how to adapt your existing code"""
    print("Example 4: Adapting your existing proxy function")
    
    def get_proxy_for_truedriver():
        """Your existing function can be simplified"""
        try:
            with open('input/proxies.txt') as f:
                proxies = [line.strip() for line in f if line.strip()]
                if not proxies:
                    return None
                
                import random
                proxy_choice = random.choice(proxies)
                
                # Return proxy as-is - truedriver will handle the format
                return proxy_choice
                
        except FileNotFoundError:
            print("Proxy file not found. Running without proxy.")
            return None
    
    # Get proxy from your function
    proxy = get_proxy_for_truedriver()
    
    if proxy:
        browser = await uc.start(proxy=proxy)
        print(f"Using proxy: {proxy}")
    else:
        browser = await uc.start()
        print("Running without proxy")
    
    tab = await browser.get("https://httpbin.org/ip")
    await asyncio.sleep(2)
    await browser.stop()


async def example_multiple_proxy_formats():
    """Example showing different proxy formats that work"""
    print("Example 5: Multiple proxy formats")
    
    proxy_formats = [
        # Simple formats
        "proxy.example.com:8080",
        "http://proxy.example.com:8080",
        "socks5://proxy.example.com:1080",
        
        # With authentication
        "user:pass@proxy.example.com:8080",
        "http://user:pass@proxy.example.com:8080",
        "socks5://user:pass@proxy.example.com:1080",
        
        # Dict format
        {"server": "proxy.example.com:8080"},
        {"server": "proxy.example.com:8080", "username": "user", "password": "pass"},
    ]
    
    for i, proxy in enumerate(proxy_formats):
        print(f"Format {i+1}: {proxy}")
        
        # Note: Don't actually run these as the proxies don't exist
        # browser = await uc.start(proxy=proxy)
        # tab = await browser.get("https://httpbin.org/ip")
        # await browser.stop()


async def main():
    """Run all examples"""
    print("=== TrueDriver Proxy Examples ===\n")
    
    # Note: These examples use fake proxy addresses
    # Replace with your actual proxy details
    
    print("Proxy formats supported:")
    print("1. Simple: 'ip:port'")
    print("2. With protocol: 'http://ip:port'")  
    print("3. With auth: 'user:pass@ip:port'")
    print("4. Dict: {'server': 'ip:port', 'username': 'user', 'password': 'pass'}")
    print()
    
    # Uncomment to test with real proxies:
    # await example_simple_proxy()
    # await example_authenticated_proxy_string()
    # await example_authenticated_proxy_dict()
    # await example_working_with_your_code()
    
    await example_multiple_proxy_formats()


if __name__ == "__main__":
    asyncio.run(main())
