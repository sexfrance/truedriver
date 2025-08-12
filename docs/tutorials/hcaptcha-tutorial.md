# hCaptcha Tutorial

This tutorial will walk you through solving hCaptcha challenges using Truedriver's iframe support functionality.

## What is hCaptcha?

hCaptcha is a popular CAPTCHA service that helps websites protect against bots. It typically presents challenges in an iframe, requiring users to identify objects in images or simply check a box to prove they're human.

## Prerequisites

- Truedriver installed (`pip install truedriver`)
- Basic understanding of async/await in Python
- A website with hCaptcha for testing (we'll use the official demo)

## Step 1: Basic Setup

First, let's set up a basic script to navigate to the hCaptcha demo page:

```python
import asyncio
import truedriver as td

async def main():
    # Start browser
    browser = await td.start()
    
    # Navigate to hCaptcha demo
    tab = await browser.get("https://accounts.hcaptcha.com/demo")
    
    # Wait for page to load
    await asyncio.sleep(2)
    
    print("Navigated to hCaptcha demo page")
    
    # Keep browser open for inspection
    await asyncio.sleep(10)
    
    await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Step 2: Using the Built-in Solver

Truedriver provides a built-in hCaptcha solver that handles all the complexity for you:

```python
import asyncio
import truedriver as td

async def solve_with_builtin():
    browser = await td.start()
    tab = await browser.get("https://accounts.hcaptcha.com/demo")
    
    await asyncio.sleep(2)
    
    print("Attempting to solve hCaptcha...")
    success = await tab.solve_hcaptcha(timeout=30.0)
    
    if success:
        print("✓ hCaptcha solved successfully!")
    else:
        print("✗ Failed to solve hCaptcha")
    
    await asyncio.sleep(5)  # Observe the result
    await browser.close()

if __name__ == "__main__":
    asyncio.run(solve_with_builtin())
```

## Step 3: Manual iframe Approach

For more control, you can manually handle the iframe switching:

```python
import asyncio
import truedriver as td

async def solve_manually():
    browser = await td.start()
    tab = await browser.get("https://accounts.hcaptcha.com/demo")
    
    await asyncio.sleep(2)
    
    try:
        # Find the hCaptcha iframe
        print("Looking for hCaptcha iframe...")
        hcaptcha_iframe = await tab.find_hcaptcha_iframe()
        
        if not hcaptcha_iframe:
            print("No hCaptcha iframe found")
            return
        
        print("Found hCaptcha iframe, switching context...")
        
        # Switch to the iframe context
        await tab.switch_to_frame(hcaptcha_iframe)
        
        # Wait for iframe content to load
        await asyncio.sleep(1)
        
        # Look for the checkbox within the iframe
        print("Looking for checkbox in iframe...")
        checkbox_selectors = [
            'div[role="checkbox"]',
            '.check-box',
            'input[type="checkbox"]'
        ]
        
        checkbox = None
        for selector in checkbox_selectors:
            try:
                checkbox = await tab.query_selector(selector)
                if checkbox:
                    print(f"Found checkbox with selector: {selector}")
                    break
            except:
                continue
        
        if checkbox:
            print("Clicking checkbox...")
            await checkbox.click()
            
            # Wait for challenge to process
            await asyncio.sleep(3)
            
            # Check if solved (this is simplified)
            print("Challenge submitted!")
        else:
            print("Could not find checkbox in iframe")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Always switch back to main frame
        await tab.switch_to_frame(None)
        print("Switched back to main frame")
    
    await asyncio.sleep(5)
    await browser.close()

if __name__ == "__main__":
    asyncio.run(solve_manually())
```

## Step 4: Advanced iframe Detection

Sometimes you need to work with multiple iframes or detect them dynamically:

```python
import asyncio
import truedriver as td

async def advanced_detection():
    browser = await td.start()
    tab = await browser.get("https://accounts.hcaptcha.com/demo")
    
    await asyncio.sleep(2)
    
    # Get all frames on the page
    frames = await tab.get_frames()
    print(f"Found {len(frames)} frames on the page:")
    
    for i, frame in enumerate(frames):
        print(f"  Frame {i+1}: {frame.url}")
        if "hcaptcha" in frame.url.lower():
            print(f"    ^ This looks like an hCaptcha frame!")
    
    # Alternative: Find all iframes and inspect them
    print("\nLooking for iframe elements...")
    iframes = await tab.query_selector_all('iframe')
    
    for i, iframe in enumerate(iframes):
        src = iframe.attrs.get('src', '')
        title = iframe.attrs.get('title', '')
        print(f"  iframe {i+1}: src='{src}', title='{title}'")
        
        if 'hcaptcha' in src.lower() or 'hcaptcha' in title.lower():
            print(f"    ^ This is likely the hCaptcha iframe!")
            
            # Switch to this iframe and explore
            await tab.switch_to_frame(iframe)
            
            # Get the page title within the iframe
            try:
                iframe_title = await tab.evaluate('document.title')
                iframe_url = await tab.evaluate('window.location.href')
                print(f"    iframe title: '{iframe_title}'")
                print(f"    iframe URL: '{iframe_url}'")
            except Exception as e:
                print(f"    Error getting iframe info: {e}")
            
            # Switch back to main frame
            await tab.switch_to_frame(None)
    
    await browser.close()

if __name__ == "__main__":
    asyncio.run(advanced_detection())
```

## Step 5: Error Handling and Robustness

Production code should handle various edge cases:

```python
import asyncio
import truedriver as td

async def robust_solver():
    browser = await td.start()
    
    try:
        tab = await browser.get("https://accounts.hcaptcha.com/demo")
        await asyncio.sleep(2)
        
        # Try built-in solver first
        print("Trying built-in solver...")
        if await tab.solve_hcaptcha(timeout=20.0):
            print("✓ Solved with built-in method!")
            return True
        
        print("Built-in solver failed, trying manual approach...")
        
        # Manual approach with error handling
        iframe = await tab.find_hcaptcha_iframe()
        if not iframe:
            # Last resort: try to find any iframe with captcha-like attributes
            all_iframes = await tab.query_selector_all('iframe')
            for iframe in all_iframes:
                src = iframe.attrs.get('src', '').lower()
                if any(keyword in src for keyword in ['captcha', 'challenge', 'verify']):
                    break
            else:
                raise Exception("No captcha iframe found")
        
        await tab.switch_to_frame(iframe)
        
        # Try multiple checkbox selectors
        checkbox_selectors = [
            'div[role="checkbox"]',
            'input[type="checkbox"]',
            '.checkbox',
            '[data-cy="checkbox"]',
            '.check-box',
            '.hcaptcha-checkbox'
        ]
        
        checkbox = None
        for selector in checkbox_selectors:
            try:
                checkbox = await tab.query_selector(selector, timeout=2)
                if checkbox:
                    break
            except:
                continue
        
        if not checkbox:
            raise Exception("No checkbox found in iframe")
        
        await checkbox.click()
        
        # Wait and check for success indicators
        for _ in range(10):  # Wait up to 5 seconds
            try:
                # Check for various success indicators
                success_indicators = [
                    '.hcaptcha-success',
                    '[aria-checked="true"]',
                    '.challenge-success'
                ]
                
                for indicator in success_indicators:
                    if await tab.query_selector(indicator, timeout=0.1):
                        print("✓ Challenge appears to be solved!")
                        return True
            except:
                pass
            
            await asyncio.sleep(0.5)
        
        print("? Challenge status unclear")
        return False
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
        
    finally:
        # Cleanup
        try:
            await tab.switch_to_frame(None)
        except:
            pass
        await browser.close()

if __name__ == "__main__":
    success = asyncio.run(robust_solver())
    print(f"Final result: {'Success' if success else 'Failed'}")
```

## Tips and Best Practices

1. **Always use timeouts**: iframe content can take time to load
2. **Handle errors gracefully**: Network issues and page changes are common
3. **Switch back to main frame**: Always return to the main context when done
4. **Test with different sites**: Different implementations may vary
5. **Respect rate limits**: Don't hammer captcha services
6. **Check for updates**: Captcha services frequently change their implementations

## Common Issues and Solutions

### Issue: iframe not found
**Solution**: Wait longer for page load, check selectors, verify the site actually uses hCaptcha

### Issue: Checkbox not clickable
**Solution**: Ensure iframe is fully loaded, try different selectors, check if checkbox is already solved

### Issue: Operations not working in iframe
**Solution**: Verify you've switched contexts, check that iframe content has loaded

### Issue: Can't switch back to main frame
**Solution**: Use try/finally blocks to ensure cleanup happens

## Next Steps

- Explore the full API documentation
- Try with different captcha services
- Integrate with your web scraping projects
- Contribute improvements back to the project

This tutorial covers the basics of hCaptcha solving with Truedriver. The iframe support is flexible and can be adapted to work with many different types of embedded content beyond just captchas.
