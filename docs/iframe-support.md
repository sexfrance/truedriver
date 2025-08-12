# iframe Support

Truedriver provides comprehensive support for interacting with iframes, making it easy to solve hCaptcha, reCaptcha, and other iframe-based challenges. This document covers all the iframe-related functionality.

## Overview

Many modern web applications use iframes to embed third-party content like captchas, payment forms, and widgets. Truedriver's iframe support allows you to seamlessly switch between the main frame and iframe contexts to interact with embedded content.

## Core Methods

### `switch_to_frame(frame_element)`

Switch the execution context to an iframe. All subsequent operations will be performed within the iframe context until you switch back to the main frame.

**Parameters:**
- `frame_element` (Union[Element, str, FrameId, None]): 
  - `Element`: An iframe element obtained via `query_selector`
  - `str`: CSS selector for the iframe
  - `FrameId`: Chrome DevTools Protocol frame ID
  - `None`: Switch back to the main frame

**Examples:**

```python
# Switch to iframe by element
iframe = await tab.query_selector('iframe[src*="hcaptcha"]')
await tab.switch_to_frame(iframe)

# Switch to iframe by CSS selector
await tab.switch_to_frame('iframe[src*="challenge"]')

# Switch back to main frame
await tab.switch_to_frame(None)
```

### `find_hcaptcha_iframe()`

Automatically locate hCaptcha iframes on the page using common selectors and patterns.

**Returns:** `Element | None` - The hCaptcha iframe element or None if not found

**Example:**

```python
hcaptcha_iframe = await tab.find_hcaptcha_iframe()
if hcaptcha_iframe:
    await tab.switch_to_frame(hcaptcha_iframe)
```

### `solve_hcaptcha(timeout=30.0)`

Automated hCaptcha challenge solver that combines iframe detection, context switching, and challenge interaction.

**Parameters:**
- `timeout` (float): Maximum time to wait for solution completion

**Returns:** `bool` - True if solved successfully, False otherwise

**Example:**

```python
success = await tab.solve_hcaptcha(timeout=30.0)
if success:
    print("hCaptcha solved successfully!")
```

### `get_frames()`

Get information about all frames on the current page.

**Returns:** `List[Frame]` - List of frame objects with metadata

**Example:**

```python
frames = await tab.get_frames()
for frame in frames:
    print(f"Frame ID: {frame.id_}, URL: {frame.url}")
```

## Usage Patterns

### Basic iframe Interaction

```python
import asyncio
import truedriver as td

async def basic_iframe_example():
    browser = await td.start()
    tab = await browser.get("https://example.com")
    
    # Find and switch to iframe
    iframe = await tab.query_selector('iframe#my-iframe')
    await tab.switch_to_frame(iframe)
    
    # Interact with content inside iframe
    button = await tab.query_selector('.button-in-iframe')
    await button.click()
    
    # Switch back to main frame
    await tab.switch_to_frame(None)
    
    await browser.close()
```

### hCaptcha Challenge Solving

```python
async def solve_hcaptcha_challenge():
    browser = await td.start()
    tab = await browser.get("https://accounts.hcaptcha.com/demo")
    
    # Method 1: Built-in solver
    if await tab.solve_hcaptcha():
        print("Challenge solved with built-in method!")
        return
    
    # Method 2: Manual approach
    hcaptcha_iframe = await tab.find_hcaptcha_iframe()
    if hcaptcha_iframe:
        await tab.switch_to_frame(hcaptcha_iframe)
        
        # Look for checkbox
        checkbox = await tab.query_selector('div[role="checkbox"]')
        if checkbox:
            await checkbox.click()
            await asyncio.sleep(2)  # Wait for response
            
        await tab.switch_to_frame(None)
    
    await browser.close()
```

### Multiple iframe Navigation

```python
async def multiple_iframe_example():
    browser = await td.start()
    tab = await browser.get("https://example-with-nested-iframes.com")
    
    # Get all frames
    frames = await tab.get_frames()
    print(f"Found {len(frames)} frames")
    
    # Switch to specific iframe by URL pattern
    for frame in frames:
        if "captcha" in frame.url:
            await tab.switch_to_frame(frame.id_)
            # Do work in captcha iframe
            await tab.switch_to_frame(None)
            break
    
    await browser.close()
```

## Advanced Features

### Context-Aware Operations

When you switch to an iframe context, all subsequent operations automatically work within that frame:

```python
# Switch to iframe
await tab.switch_to_frame('iframe[src*="payment"]')

# These operations now work within the iframe
form = await tab.query_selector('form.payment-form')
card_input = await tab.query_selector('input[name="card"]')
await card_input.type("4111111111111111")

# JavaScript evaluation also works in iframe context
result = await tab.evaluate('document.title')
print(f"iframe title: {result}")

# Switch back to main frame
await tab.switch_to_frame(None)
```

### Error Handling

```python
async def robust_iframe_interaction():
    browser = await td.start()
    tab = await browser.get("https://example.com")
    
    try:
        # Attempt to find and switch to iframe
        iframe = await tab.query_selector('iframe.challenge', timeout=10)
        if not iframe:
            raise Exception("Challenge iframe not found")
            
        await tab.switch_to_frame(iframe)
        
        # Perform operations in iframe
        await tab.query_selector('.challenge-button').click()
        
    except Exception as e:
        print(f"Error during iframe interaction: {e}")
        
    finally:
        # Always ensure we switch back to main frame
        try:
            await tab.switch_to_frame(None)
        except:
            pass
        
        await browser.close()
```

## Common Selectors

### hCaptcha

```python
# Common hCaptcha iframe selectors
selectors = [
    'iframe[src*="hcaptcha.com"]',
    'iframe[src*="newassets.hcaptcha.com"]',
    'iframe[data-hcaptcha-widget-id]',
    'iframe[title*="hCaptcha"]',
    '.h-captcha iframe',
    '[data-sitekey] iframe'
]
```

### reCaptcha

```python
# Common reCaptcha iframe selectors
selectors = [
    'iframe[src*="recaptcha"]',
    'iframe[title="reCAPTCHA"]',
    '.g-recaptcha iframe',
    'iframe[name^="a-"][src*="recaptcha"]'
]
```

## Best Practices

1. **Always switch back to main frame**: Use `await tab.switch_to_frame(None)` when done with iframe operations
2. **Use try/finally blocks**: Ensure frame switching happens even if errors occur
3. **Wait for iframe loading**: Add appropriate delays after switching to allow iframe content to load
4. **Check iframe existence**: Always verify iframe elements exist before switching
5. **Use specific selectors**: Be as specific as possible when selecting iframes to avoid conflicts

## Troubleshooting

### iframe Not Found
- Verify the iframe selector is correct
- Wait for the iframe to load before switching
- Check if the iframe is dynamically created after page load

### Operations Not Working in iframe
- Ensure you've successfully switched to the iframe context
- Verify the iframe has fully loaded its content
- Check that elements exist within the iframe

### Context Issues
- Always switch back to the main frame when done
- Use `get_frames()` to debug frame hierarchy
- Check execution context with `tab.evaluate('window.location.href')`

## Examples

See the complete working examples in:
- `examples/hcaptcha_iframe_example.py` - Comprehensive hCaptcha solving examples
- `examples/demo.py` - Basic iframe interaction patterns

## API Reference

For complete API documentation, see the docstrings in the source code or generate documentation with:

```bash
python -m pydoc truedriver.core.tab.Tab.switch_to_frame
python -m pydoc truedriver.core.tab.Tab.solve_hcaptcha
```
