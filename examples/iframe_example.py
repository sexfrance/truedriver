"""
General iframe interaction example.

This example demonstrates how to:
1. Find and list all iframes on a page
2. Switch between different iframe contexts
3. Interact with elements inside iframes
4. Handle nested iframes
5. Use different methods to locate iframes

This can be applied to various use cases including:
- Forms embedded in iframes
- Captcha widgets (hCaptcha, reCAPTCHA, etc.)
- Payment processing widgets
- Social media embeds
- Third-party content widgets
"""

import asyncio
import truedriver as uc


async def demonstrate_iframe_methods():
    """Demonstrate various ways to work with iframes"""
    browser = await uc.start()
    
    # Create a test page with multiple iframes
    html_content = """
    <!DOCTYPE html>
    <html>
    <head><title>Iframe Test Page</title></head>
    <body>
        <h1>Main Page Content</h1>
        <p>This is the main page.</p>
        
        <!-- First iframe with a name -->
        <iframe name="form-iframe" src="data:text/html,
            <h2>Form Iframe</h2>
            <form>
                <input type='text' name='username' placeholder='Username'>
                <input type='password' name='password' placeholder='Password'>
                <button type='submit'>Login</button>
            </form>
        " width="400" height="200"></iframe>
        
        <!-- Second iframe with an id -->
        <iframe id="content-iframe" src="data:text/html,
            <h2>Content Iframe</h2>
            <p>This is content inside an iframe.</p>
            <button onclick='alert(\"Button clicked!\")'>Click Me</button>
        " width="400" height="200"></iframe>
        
        <!-- Third iframe (nested content) -->
        <iframe src="data:text/html,
            <h2>Nested Container</h2>
            <iframe src='data:text/html,<h3>Deeply Nested Content</h3><input type=\"text\" value=\"nested-input\">' width='300' height='100'></iframe>
        " width="400" height="250"></iframe>
    </body>
    </html>
    """
    
    tab = await browser.get("data:text/html," + html_content.replace('\n', '').replace(' ' * 4, ''))
    
    try:
        # Wait for iframes to load
        await asyncio.sleep(2)
        
        print("=== Iframe Demonstration ===\n")
        
        # 1. List all frames
        print("1. Listing all frames:")
        frames = await tab.get_frames()
        for i, frame in enumerate(frames):
            print(f"   Frame {i}: {frame.url[:80]}...")
            if frame.name:
                print(f"   Name: {frame.name}")
        print(f"   Total frames found: {len(frames)}\n")
        
        # 2. Switch to frame by name
        print("2. Switching to frame by name:")
        form_frame = await tab.find_frame_by_name("form-iframe")
        if form_frame:
            await tab.switch_to_frame(form_frame)
            print("   Switched to form iframe")
            
            # Interact with form elements
            username_field = await tab.find("input[name='username']", timeout=3)
            if username_field:
                await username_field.send_keys("testuser")
                print("   Filled username field")
            
            password_field = await tab.find("input[name='password']", timeout=3)
            if password_field:
                await password_field.send_keys("testpass")
                print("   Filled password field")
            
            # Switch back to main frame
            await tab.switch_to_main_frame()
            print("   Switched back to main frame\n")
        
        # 3. Switch to frame by element
        print("3. Switching to frame by element:")
        iframe_element = await tab.find("iframe#content-iframe", timeout=3)
        if iframe_element:
            await tab.switch_to_frame(iframe_element)
            print("   Switched to content iframe using element")
            
            # Interact with content
            button = await tab.find("button", timeout=3)
            if button:
                print("   Found button in iframe")
                # Note: This would trigger an alert, so we'll just log it
                print("   (Would click button here)")
            
            await tab.switch_to_main_frame()
            print("   Switched back to main frame\n")
        
        # 4. Switch to frame by index
        print("4. Switching to frames by index:")
        for i in range(1, min(len(frames), 4)):  # Skip main frame (index 0)
            try:
                await tab.switch_to_frame_by_index(i)
                current_frame = await tab.get_current_frame()
                if current_frame:
                    print(f"   Switched to frame {i}: {current_frame.url[:50]}...")
                
                # Try to find some content
                try:
                    headings = await tab.find_all("h2,h3", timeout=1)
                    for heading in headings:
                        text = await heading.text_content()
                        print(f"   Found heading: '{text}'")
                except:
                    print(f"   No headings found in frame {i}")
                
                await tab.switch_to_main_frame()
            except Exception as e:
                print(f"   Error with frame {i}: {e}")
        
        print("\n=== Advanced: Working with nested iframes ===")
        
        # 5. Handle nested iframes
        await asyncio.sleep(1)  # Let nested iframes load
        
        frames = await tab.get_frames()
        print(f"Total frames (including nested): {len(frames)}")
        
        # Find the deepest nested frame
        nested_frames = [f for f in frames if "nested" in f.url.lower()]
        if nested_frames:
            deepest_frame = nested_frames[-1]  # Last one is usually deepest
            await tab.switch_to_frame(deepest_frame)
            print("Switched to deepest nested frame")
            
            # Try to interact with nested content
            try:
                nested_input = await tab.find("input", timeout=2)
                if nested_input:
                    value = await nested_input.get_attribute("value")
                    print(f"Found nested input with value: '{value}'")
                    await nested_input.clear()
                    await nested_input.send_keys("modified in nested frame")
                    print("Modified nested input value")
            except Exception as e:
                print(f"Could not interact with nested content: {e}")
            
            await tab.switch_to_main_frame()
            print("Switched back to main frame")
        
    except Exception as e:
        print(f"Error during demonstration: {e}")
    finally:
        await browser.stop()


async def real_world_example():
    """Example of handling a real website with embedded content"""
    browser = await uc.start()
    
    try:
        # Example: A page that might have embedded forms or widgets
        tab = await browser.get("https://www.w3schools.com/html/html_iframe.asp")
        await asyncio.sleep(3)
        
        print("=== Real World Example ===")
        
        # Find iframes on the page
        frames = await tab.get_frames()
        print(f"Found {len(frames)} frames on W3Schools iframe example page")
        
        # Look for iframes that might contain interactive content
        for i, frame in enumerate(frames):
            if i == 0:  # Skip main frame
                continue
                
            print(f"\nFrame {i}: {frame.url}")
            
            try:
                await tab.switch_to_frame(frame)
                
                # Check what's inside this frame
                title = await tab.evaluate("document.title")
                print(f"  Frame title: {title}")
                
                # Look for interactive elements
                links = await tab.find_all("a", timeout=1)
                buttons = await tab.find_all("button", timeout=1)
                inputs = await tab.find_all("input", timeout=1)
                
                print(f"  Interactive elements: {len(links)} links, {len(buttons)} buttons, {len(inputs)} inputs")
                
                await tab.switch_to_main_frame()
                
            except Exception as e:
                print(f"  Error inspecting frame: {e}")
                await tab.switch_to_main_frame()
    
    except Exception as e:
        print(f"Error in real world example: {e}")
    finally:
        await browser.stop()


async def main():
    """Run iframe demonstrations"""
    print("Starting iframe interaction examples...\n")
    
    # Run the general demonstration
    await demonstrate_iframe_methods()
    
    print("\n" + "="*50 + "\n")
    
    # Run real-world example
    await real_world_example()
    
    print("\nIframe examples completed!")


if __name__ == "__main__":
    asyncio.run(main())