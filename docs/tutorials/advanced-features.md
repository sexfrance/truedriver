# Advanced Features: Iframes and Proxies

This tutorial covers two of Truedriver's most powerful features: iframe interaction and proxy support. These features make Truedriver ideal for complex automation tasks involving embedded content and network routing.

## Iframe Interaction

Iframes are commonly used for embedded content like payment forms, captchas (hCaptcha, reCaptcha), social media widgets, and third-party services. Traditional browser automation tools struggle with iframe context switching, but Truedriver makes it seamless.

### Understanding Iframe Context

When you switch to an iframe, all subsequent operations (finding elements, clicking, typing, executing JavaScript) happen within that iframe's context until you switch back to the main frame or another iframe.

```python
import asyncio
import truedriver as td

async def iframe_basics():
    browser = await td.start()
    tab = await browser.get('https://example.com/page-with-iframes')
    
    # Get all frames on the page
    frames = await tab.get_frames()
    print(f"Found {len(frames)} frames on the page")
    
    # Print frame information
    for i, frame in enumerate(frames):
        print(f"Frame {i}: {frame.url}")
        if frame.name:
            print(f"  Name: {frame.name}")
    
    await browser.stop()

if __name__ == '__main__':
    asyncio.run(iframe_basics())
```

### Finding and Switching to Iframes

#### Method 1: By URL Pattern

This is the most reliable method, especially for third-party services:

```python
async def switch_by_url():
    browser = await td.start()
    tab = await browser.get('https://example.com')
    
    # Find hCaptcha iframe
    hcaptcha_frame = await tab.find_frame_by_url(r'.*hcaptcha\.com.*')
    if hcaptcha_frame:
        await tab.switch_to_frame(hcaptcha_frame)
        print(f"Switched to hCaptcha frame: {hcaptcha_frame.url}")
        
        # Interact with hCaptcha elements
        checkbox = await tab.find('#checkbox', timeout=5)
        if checkbox:
            await checkbox.click()
        
        # Switch back to main frame
        await tab.switch_to_main_frame()
    
    await browser.stop()
```

#### Method 2: By Frame Name

If the iframe has a name attribute:

```python
async def switch_by_name():
    browser = await td.start()
    tab = await browser.get('https://example.com')
    
    # Find iframe by name
    payment_frame = await tab.find_frame_by_name('payment-iframe')
    if payment_frame:
        await tab.switch_to_frame(payment_frame)
        
        # Fill payment form
        card_number = await tab.find('input[name="cardNumber"]')
        await card_number.send_keys('4111111111111111')
        
        await tab.switch_to_main_frame()
    
    await browser.stop()
```

#### Method 3: By Iframe Element

When you have a reference to the iframe element itself:

```python
async def switch_by_element():
    browser = await td.start()
    tab = await browser.get('https://example.com')
    
    # Find iframe element
    iframe_element = await tab.find('iframe[src*="payment"]')
    if iframe_element:
        await tab.switch_to_frame(iframe_element)
        
        # Work within the iframe
        submit_btn = await tab.find('button[type="submit"]')
        await submit_btn.click()
        
        await tab.switch_to_main_frame()
    
    await browser.stop()
```

### Real-World Example: hCaptcha Automation

```python
import asyncio
import truedriver as td

async def handle_hcaptcha():
    """
    Example of handling hCaptcha iframes
    """
    browser = await td.start(headless=False)
    tab = await browser.get('https://accounts.hcaptcha.com/demo')
    
    try:
        # Wait for page to load
        await asyncio.sleep(3)
        
        # Find the main hCaptcha iframe
        hcaptcha_frame = await tab.find_frame_by_url(r'.*hcaptcha\.com.*')
        
        if hcaptcha_frame:
            print(f"Found hCaptcha iframe: {hcaptcha_frame.url}")
            
            # Switch to hCaptcha iframe
            await tab.switch_to_frame(hcaptcha_frame)
            
            # Look for the checkbox
            checkbox = await tab.find('#checkbox', timeout=10)
            if checkbox:
                print("Found hCaptcha checkbox")
                await checkbox.click()
                
                # Wait to see if challenge appears
                await asyncio.sleep(2)
                
                # Check for challenge iframe
                challenge_frame = await tab.find_frame_by_url(r'.*challenge.*hcaptcha\.com.*')
                if challenge_frame:
                    print("Challenge iframe appeared")
                    await tab.switch_to_frame(challenge_frame)
                    
                    # Handle challenge (implement your solving logic here)
                    print("Challenge iframe active - implement solving logic")
                    
                    # Switch back to main hCaptcha frame
                    await tab.switch_to_frame(hcaptcha_frame)
            
            # Switch back to main page
            await tab.switch_to_main_frame()
            print("Returned to main frame")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await browser.stop()

if __name__ == '__main__':
    asyncio.run(handle_hcaptcha())
```

### Debugging Iframe Issues

Common debugging techniques:

```python
async def debug_iframes():
    browser = await td.start()
    tab = await browser.get('https://example.com')
    
    # List all frames with details
    frames = await tab.get_frames()
    for i, frame in enumerate(frames):
        print(f"Frame {i}:")
        print(f"  URL: {frame.url}")
        print(f"  Name: {frame.name}")
        print(f"  Security Origin: {frame.security_origin}")
        print(f"  MIME Type: {frame.mime_type}")
        print()
    
    # Check current frame
    current = await tab.get_current_frame()
    if current:
        print(f"Currently in frame: {current.url}")
    else:
        print("Currently in main frame")
    
    # Switch to a frame and verify
    if len(frames) > 1:
        await tab.switch_to_frame_by_index(1)
        current = await tab.get_current_frame()
        print(f"After switching: {current.url if current else 'main frame'}")
    
    await browser.stop()
```

## Proxy Support

Truedriver's proxy support is designed to be simple and reliable, using URL-based authentication that works consistently across Chrome, Brave, and Edge browsers.

### Basic Proxy Configuration

#### Simple Proxy (No Authentication)

```python
import asyncio
import truedriver as td

async def simple_proxy():
    # IP:Port format
    browser = await td.start(proxy="proxy.example.com:8080")
    
    # With protocol
    browser = await td.start(proxy="http://proxy.example.com:8080")
    
    # SOCKS5 proxy
    browser = await td.start(proxy="socks5://proxy.example.com:1080")
    
    tab = await browser.get('https://httpbin.org/ip')
    content = await tab.get_content()
    print(content)  # Should show proxy IP
    
    await browser.stop()

if __name__ == '__main__':
    asyncio.run(simple_proxy())
```

#### Authenticated Proxy

```python
import asyncio
import truedriver as td

async def authenticated_proxy():
    # String format with credentials
    browser = await td.start(proxy="username:password@proxy.example.com:8080")
    
    # With protocol
    browser = await td.start(proxy="http://username:password@proxy.example.com:8080")
    
    # Dict format (more readable for complex configurations)
    proxy_config = {
        "server": "proxy.example.com:8080",
        "username": "myuser",
        "password": "mypass"
    }
    browser = await td.start(proxy=proxy_config)
    
    tab = await browser.get('https://httpbin.org/ip')
    await browser.stop()

if __name__ == '__main__':
    asyncio.run(authenticated_proxy())
```

### Advanced Proxy Usage

#### Proxy Rotation

```python
import asyncio
import random
import truedriver as td

class ProxyRotator:
    def __init__(self, proxy_file='proxies.txt'):
        self.proxies = self.load_proxies(proxy_file)
    
    def load_proxies(self, filename):
        try:
            with open(filename, 'r') as f:
                proxies = [line.strip() for line in f if line.strip()]
                return proxies
        except FileNotFoundError:
            print(f"Proxy file {filename} not found")
            return []
    
    def get_random_proxy(self):
        return random.choice(self.proxies) if self.proxies else None
    
    async def test_proxy(self, proxy):
        """Test if a proxy is working"""
        try:
            browser = await td.start(proxy=proxy, headless=True)
            tab = await browser.get('https://httpbin.org/ip', timeout=10)
            content = await tab.get_content()
            await browser.stop()
            return True
        except:
            return False

async def rotate_proxies():
    rotator = ProxyRotator()
    
    for i in range(5):  # Try 5 different proxies
        proxy = rotator.get_random_proxy()
        if not proxy:
            print("No proxies available")
            break
        
        print(f"Attempt {i+1}: Testing proxy {proxy}")
        
        try:
            browser = await td.start(proxy=proxy, headless=True)
            tab = await browser.get('https://httpbin.org/ip')
            
            # Extract IP from response
            content = await tab.get_content()
            print(f"Success! IP: {content}")
            
            await browser.stop()
            break
            
        except Exception as e:
            print(f"Proxy {proxy} failed: {e}")
            continue

if __name__ == '__main__':
    asyncio.run(rotate_proxies())
```

#### Combining Proxies with Stealth Features

```python
import asyncio
import truedriver as td

async def stealth_proxy_session():
    """
    Combine proxy usage with stealth features for maximum anonymity
    """
    
    # Custom user agent and browser arguments for stealth
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    browser_args = [
        "--disable-blink-features=AutomationControlled",
        "--disable-dev-shm-usage",
        "--no-first-run",
        "--disable-extensions",
        "--disable-plugins",
        "--disable-images",  # Faster loading
        "--disable-javascript",  # For scraping static content
    ]
    
    browser = await td.start(
        proxy="username:password@proxy.example.com:8080",
        user_agent=user_agent,
        browser_args=browser_args,
        headless=True
    )
    
    # Verify setup
    tab = await browser.get('https://httpbin.org/headers')
    headers = await tab.get_content()
    print("Headers:", headers)
    
    # Check IP
    tab = await browser.get('https://httpbin.org/ip')
    ip_info = await tab.get_content()
    print("IP Info:", ip_info)
    
    # Scrape target site
    tab = await browser.get('https://example.com')
    title = await tab.find('title')
    print("Page title:", await title.text_content())
    
    await browser.stop()

if __name__ == '__main__':
    asyncio.run(stealth_proxy_session())
```

### Proxy Best Practices

1. **Always test proxies** before using them in production
2. **Use proxy rotation** to avoid rate limiting
3. **Combine with user agent rotation** for better anonymity
4. **Handle proxy failures gracefully** with fallback options
5. **Use HTTPS proxies** when possible for better security
6. **Monitor proxy performance** and replace slow/unreliable proxies

### Troubleshooting Proxies

Common issues and solutions:

```python
async def proxy_troubleshooting():
    proxy = "username:password@proxy.example.com:8080"
    
    try:
        browser = await td.start(proxy=proxy, headless=True)
        
        # Test basic connectivity
        tab = await browser.get('https://httpbin.org/ip', timeout=15)
        print("Proxy working!")
        
    except asyncio.TimeoutError:
        print("Proxy timeout - check proxy server and credentials")
    except Exception as e:
        print(f"Proxy error: {e}")
        
        # Try without proxy
        browser = await td.start(headless=True)
        tab = await browser.get('https://httpbin.org/ip')
        print("Direct connection working")
    
    finally:
        try:
            await browser.stop()
        except:
            pass
```

## Combining Iframes and Proxies

Real-world automation often requires both iframe handling and proxy usage:

```python
import asyncio
import truedriver as td

async def advanced_automation():
    """
    Example combining proxy usage with iframe interaction
    for complex automation tasks
    """
    
    # Start browser with proxy
    browser = await td.start(
        proxy="username:password@proxy.example.com:8080",
        headless=False,  # Visible for debugging
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    
    try:
        # Navigate to target page
        tab = await browser.get('https://example.com/protected-form')
        
        # Handle main page interactions
        login_btn = await tab.find('Login')
        await login_btn.click()
        
        # Wait for iframe to load
        await asyncio.sleep(2)
        
        # Find and switch to authentication iframe
        auth_frame = await tab.find_frame_by_url(r'.*auth\.example\.com.*')
        if auth_frame:
            await tab.switch_to_frame(auth_frame)
            
            # Fill authentication form inside iframe
            username_field = await tab.find('input[name="username"]')
            await username_field.send_keys('myuser')
            
            password_field = await tab.find('input[name="password"]')
            await password_field.send_keys('mypass')
            
            submit_btn = await tab.find('button[type="submit"]')
            await submit_btn.click()
            
            # Wait for authentication
            await tab.find('Authentication successful', timeout=10)
            
            # Switch back to main frame
            await tab.switch_to_main_frame()
        
        # Continue with main page flow
        success_msg = await tab.find('Welcome', timeout=10)
        print("Login successful!")
        
    except Exception as e:
        print(f"Automation failed: {e}")
    finally:
        await browser.stop()

if __name__ == '__main__':
    asyncio.run(advanced_automation())
```

This combination of iframe handling and proxy support makes Truedriver incredibly powerful for complex automation scenarios involving embedded content, authentication systems, and network routing requirements.
