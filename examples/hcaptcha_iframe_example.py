"""
hCaptcha iframe interaction example

This example demonstrates how to interact with hCaptcha challenges
that are embedded in iframes using the new iframe switching functionality.
"""

import asyncio
import truedriver as td


async def solve_hcaptcha_example():
    """
    Example of solving hCaptcha by switching to iframe context
    """
    browser = await td.start()
    tab = await browser.get("https://accounts.hcaptcha.com/demo")
    
    try:
        # Wait for the page to load
        await asyncio.sleep(2)
        
        # Method 1: Use the built-in hCaptcha solver
        print("Attempting to solve hCaptcha using built-in solver...")
        success = await tab.solve_hcaptcha(timeout=30.0)
        
        if success:
            print("✓ hCaptcha solved successfully!")
        else:
            print("✗ Failed to solve hCaptcha with built-in method")
            
            # Method 2: Manual iframe switching approach
            print("Trying manual iframe switching approach...")
            
            # Find hCaptcha iframe
            hcaptcha_iframe = await tab.find_hcaptcha_iframe()
            if hcaptcha_iframe:
                print("Found hCaptcha iframe")
                
                # Switch to iframe context
                await tab.switch_to_frame(hcaptcha_iframe)
                print("Switched to iframe context")
                
                # Look for checkbox in iframe
                checkbox = await tab.query_selector('div[role="checkbox"]')
                if checkbox:
                    print("Found checkbox in iframe, clicking...")
                    await checkbox.click()
                    
                    # Wait for challenge to complete
                    await asyncio.sleep(5)
                    
                # Switch back to main frame
                await tab.switch_to_frame(None)
                print("Switched back to main frame")
        
        # Keep browser open for inspection
        await asyncio.sleep(5)
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        await browser.close()


async def generic_iframe_example():
    """
    Example of generic iframe switching functionality
    """
    browser = await td.start()
    tab = await browser.get("https://example.com")  # Replace with actual site with iframes
    
    try:
        # Method 1: Switch to iframe by CSS selector
        await tab.switch_to_frame('iframe[src*="target-iframe"]')
        
        # Now all operations work within the iframe context
        element_in_iframe = await tab.query_selector('.some-element')
        if element_in_iframe:
            await element_in_iframe.click()
        
        # Switch back to main frame
        await tab.switch_to_frame(None)
        
        # Method 2: Switch to iframe by element
        iframe_element = await tab.query_selector('iframe#my-iframe')
        if iframe_element:
            await tab.switch_to_frame(iframe_element)
            
            # Do work in iframe
            await tab.evaluate('console.log("Working in iframe context")')
            
            # Switch back
            await tab.switch_to_frame(None)
        
        # Method 3: Get all frames information
        frames = await tab.get_frames()
        print(f"Found {len(frames)} frames on the page:")
        for frame in frames:
            print(f"  Frame ID: {frame.id_}, URL: {frame.url}")
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        await browser.close()


if __name__ == "__main__":
    # Run the hCaptcha example
    asyncio.run(solve_hcaptcha_example())
    
    # Uncomment to run the generic iframe example
    # asyncio.run(generic_iframe_example())
