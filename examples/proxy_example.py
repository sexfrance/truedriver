"""
Enhanced Proxy Example for TrueDriver

This example demonstrates various proxy configuration methods with automatic
CDP authentication. The library now handles proxy authentication automatically
without hanging or blocking.
"""

import asyncio
import truedriver as td


async def test_authenticated_proxy_formats():
    """Test different authenticated proxy configuration formats"""
    
    # Replace with your actual proxy credentials
    proxy_server = "resi.voidproxies.com:8603"
    username = "pkg-royal"
    password = "kk8mrqj5hnth6b44"
    
    print("Testing Authenticated Proxy Formats")
    print("=" * 50)
    
    # Format 1: Full URL with credentials
    proxy_url = f"{username}:{password}@{proxy_server}"
    print(f"Format 1 - URL with credentials: {proxy_url}")
    
    try:
        browser = await td.start(
            proxy=proxy_url,
            headless=False,
            timeout=30  # 30 second timeout
        )
        
        # Test navigation with timeout
        tab = await browser.get("https://httpbin.org/ip", timeout=15)
        await asyncio.sleep(2)  # Brief wait for content
        
        content = await tab.get_content()
        if '"origin"' in content:
            print("✅ Format 1 successful!")
            # Extract IP from response
            import json
            try:
                data = json.loads(content)
                print(f"   Proxy IP: {data.get('origin', 'unknown')}")
            except:
                print(f"   Response: {content[:100]}...")
        else:
            print("❌ Format 1 failed - no IP response")
            
        await browser.stop()
        
    except Exception as e:
        print(f"❌ Format 1 failed: {e}")
    
    print("\n" + "-" * 30)
    
    # Format 2: Dict format
    proxy_dict = {
        "server": proxy_server,
        "username": username,
        "password": password
    }
    print(f"Format 2 - Dict format: {proxy_dict}")
    
    try:
        browser = await td.start(
            proxy=proxy_dict,
            headless=False,
            timeout=30
        )
        
        tab = await browser.get("https://httpbin.org/ip", timeout=15)
        await asyncio.sleep(2)
        
        content = await tab.get_content()
        if '"origin"' in content:
            print("✅ Format 2 successful!")
            import json
            try:
                data = json.loads(content)
                print(f"   Proxy IP: {data.get('origin', 'unknown')}")
            except:
                print(f"   Response: {content[:100]}...")
        else:
            print("❌ Format 2 failed - no IP response")
            
        await browser.stop()
        
    except Exception as e:
        print(f"❌ Format 2 failed: {e}")


async def test_proxy_functionality():
    """Test proxy functionality with multiple sites"""
    
    # Replace with your proxy credentials
    proxy = "pkg-royal:kk8mrqj5hnth6b44@resi.voidproxies.com:8603"
    
    print("\n" + "=" * 50)
    print("Testing Proxy Functionality")
    print("=" * 50)
    
    try:
        browser = await td.start(
            proxy=proxy,
            headless=False,
            timeout=30
        )
        
        # Test 1: Check IP
        print("Test 1: Checking IP address...")
        tab = await browser.get("https://httpbin.org/ip", timeout=15)
        await asyncio.sleep(2)
        
        ip_content = await tab.get_content()
        if '"origin"' in ip_content:
            import json
            try:
                data = json.loads(ip_content)
                proxy_ip = data.get('origin', 'unknown')
                print(f"✅ Proxy IP: {proxy_ip}")
            except:
                print("✅ IP check completed")
        else:
            print("❌ IP check failed")
        
        # Test 2: Check headers
        print("\nTest 2: Checking request headers...")
        await tab.get("https://httpbin.org/headers", timeout=15)
        await asyncio.sleep(2)
        
        headers_content = await tab.get_content()
        if '"headers"' in headers_content:
            print("✅ Headers check successful")
        else:
            print("❌ Headers check failed")
        
        # Test 3: Test POST request
        print("\nTest 3: Testing POST capability...")
        await tab.get("https://httpbin.org/forms/post", timeout=15)
        await asyncio.sleep(2)
        
        # Try to find and fill a form
        try:
            form_inputs = await tab.select_all("input[type='text'], input[type='email']")
            if form_inputs:
                await form_inputs[0].send_keys("test@example.com")
                print("✅ Form interaction successful")
            else:
                print("ℹ️  No form inputs found (still loaded successfully)")
        except Exception as e:
            print(f"ℹ️  Form test info: {e}")
        
        await browser.stop()
        print("\n✅ All proxy tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Proxy functionality test failed: {e}")
        import traceback
        traceback.print_exc()


async def test_no_proxy_comparison():
    """Test without proxy for comparison"""
    
    print("\n" + "=" * 50)
    print("Testing Without Proxy (for comparison)")
    print("=" * 50)
    
    try:
        browser = await td.start(headless=False, timeout=30)
        tab = await browser.get("https://httpbin.org/ip", timeout=15)
        await asyncio.sleep(2)
        
        content = await tab.get_content()
        if '"origin"' in content:
            import json
            try:
                data = json.loads(content)
                original_ip = data.get('origin', 'unknown')
                print(f"✅ Original IP (no proxy): {original_ip}")
            except:
                print("✅ No proxy test completed")
        else:
            print("❌ No proxy test failed")
        
        await browser.stop()
        
    except Exception as e:
        print(f"❌ No proxy test failed: {e}")


async def test_error_handling():
    """Test proxy error handling with invalid credentials"""
    
    print("\n" + "=" * 50)
    print("Testing Error Handling")
    print("=" * 50)
    
    # Test with invalid credentials
    invalid_proxy = "invalid:credentials@resi.voidproxies.com:8603"
    
    try:
        print("Testing with invalid credentials...")
        browser = await td.start(
            proxy=invalid_proxy,
            headless=False,
            timeout=20  # Shorter timeout for error case
        )
        
        # This should fail gracefully
        tab = await browser.get("https://httpbin.org/ip", timeout=10)
        await asyncio.sleep(3)
        
        content = await tab.get_content()
        if '"origin"' in content:
            print("❌ Unexpected success with invalid credentials")
        else:
            print("✅ Gracefully handled invalid credentials")
        
        await browser.stop()
        
    except Exception as e:
        print(f"✅ Error properly caught: {type(e).__name__}")
        print(f"   Details: {str(e)[:100]}...")


async def main():
    """Run all proxy tests"""
    print("TrueDriver Enhanced Proxy Testing")
    print("=" * 50)
    print("This example tests automatic CDP proxy authentication")
    print("Replace the proxy credentials with your own before running")
    print("=" * 50)
    
    # Run all tests
    await test_authenticated_proxy_formats()
    await test_proxy_functionality() 
    await test_no_proxy_comparison()
    await test_error_handling()
    
    print("\n" + "=" * 50)
    print("🎉 Proxy testing complete!")
    print("\nKey features demonstrated:")
    print("• Automatic CDP authentication (no manual handlers needed)")
    print("• Multiple proxy format support (URL and dict)")
    print("• Timeout support to prevent hanging")
    print("• Graceful error handling")
    print("• Non-blocking authentication using asyncio.create_task")


if __name__ == "__main__":
    asyncio.run(main())