# Quickstart

## Installation

To install, simply use `pip` (or your favorite package manager):

```sh
pip install truedriver
# or uv add truedriver, poetry add truedriver, etc.
```

## Basic usage

Open a browser, navigate to a page, and scrape the content:

```python
import asyncio
import truedriver as zd

async def main():
    browser = await zd.start()
    page = await browser.get('https://example.com')

    # get HTML content of the page as a string
    content = await page.get_content()

    # save a screenshot
    await page.save_screenshot()

    # close the browser window
    await browser.stop()


if __name__ == '__main__':
    asyncio.run(main())
```

## More complete example

```python
import asyncio
import truedriver as zd

async def main():
    browser = await zd.start()
    page = await browser.get('https://zendriver.dev/')

    elems = await page.select_all('*[src]')

    for elem in elems:
        await elem.flash()

    page2 = await browser.get('https://twitter.com', new_tab=True)
    page3 = await browser.get('https://github.com/ultrafunkamsterdam/nodriver', new_window=True)

    for p in (page, page2, page3):
        await p.bring_to_front()
        await p.scroll_down(200)
        await p   # wait for events to be processed
        await p.reload()
        if p != page3:
            await p.close()

if __name__ == '__main__':
    asyncio.run(main())
```

I'll leave out the async boilerplate here

```python
import truedriver as zd

browser = await zd.start(
    headless=False,
    user_data_dir="/path/to/existing/profile",  # by specifying it, it won't be automatically cleaned up when finished
    browser_executable_path="/path/to/some/other/browser",
    browser_args=['--some-browser-arg=true', '--some-other-option'],
    lang="en-US"   # this could set iso-language-code in navigator, not recommended to change
)
tab = await browser.get('https://somewebsite.com')
```

## Alternative custom options

I'll leave out the async boilerplate here

```python
import truedriver as zd

config = zd.Config()
config.headless = False
config.user_data_dir="/path/to/existing/profile",  # by specifying it, it won't be automatically cleaned up when finished
config.browser_executable_path="/path/to/some/other/browser",
config.browser_args=['--some-browser-arg=true', '--some-other-option'],
config.lang="en-US"   # this could set iso-language-code in navigator, not recommended to change
```

On Windows, we recommend using `WindowsSelectorEventLoopPolicy` for better compatibility with asyncio:

```python
import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
```

A more concrete example, which can be found in the ./example/ folder,
shows a script for uploading an image to imgur.

```python
import asyncio
from pathlib import Path
import truedriver as zd

# interesting, this is a typical site which runs completely on javascript, and that causes
# this script to be faster than the js can present the elements. This may be one of the downsides
# of this fast beast. You have to carefully consider timing.
DELAY = 2

async def main():
    browser = await zd.start()
    tab = await browser.get("https://imgur.com")

    # now we first need an image to upload, lets make a screenshot of the project page
    save_path = Path("screenshot.jpg").resolve()
    # create new tab with the project page
    temp_tab = await browser.get(
        "https://github.com/ultrafunkamsterdam/undetected-chromedriver", new_tab=True
    )

    # wait page to load
    await temp_tab
    # save the screenshot to the previously declared path of screenshot.jpg (which is just current directory)
    await temp_tab.save_screenshot(save_path)
    # done, discard the temp_tab
    await temp_tab.close()

    # accept goddamn cookies
    # the best_match flag will filter the best match from
    # matching elements containing "consent" and takes the
    # one having most similar text length
    consent = await tab.find("Consent", best_match=True)
    await consent.click()

    # shortcut
    await (await tab.find("new post", best_match=True)).click()

    file_input = await tab.select("input[type=file]")
    await file_input.send_file(save_path)
    # since file upload takes a while , the next buttons are not available yet

    await tab.wait(DELAY)

    # wait until the grab link becomes clickable, by waiting for the toast message
    await tab.select(".Toast-message--check")

    # this one is tricky. we are trying to find a element by text content
    # usually. the text node itself is not needed, but it's enclosing element.
    # in this case however, the text is NOT a text node, but an "placeholder" attribute of a span element.
    # so for this one, we use the flag return_enclosing_element and set it to False
    title_field = await tab.find("give your post a unique title", best_match=True)
    print(title_field)
    await title_field.send_keys("undetected truedriver")

    grab_link = await tab.find("grab link", best_match=True)
    await grab_link.click()

    # there is a delay for the link sharing popup.
    # let's pause for a sec
    await tab.wait(DELAY)

    # get inputs of which the value starts with http
    input_thing = await tab.select("input[value^=https]")

    my_link = input_thing.attrs.value

    print(my_link)
    await browser.stop()


if __name__ == "__main__":
    asyncio.run(main())
```

## Working with iframes

Truedriver provides comprehensive support for interacting with iframe content. This is particularly useful for embedded widgets like captchas, forms, or third-party content.

### Basic iframe switching

```python
import asyncio
import truedriver as zd

async def main():
    browser = await zd.start()
    tab = await browser.get('https://example.com/page-with-iframes')
    
    # Method 1: Find iframe by URL pattern
    iframe = await tab.find_frame_by_url(r'.*captcha\.com.*')
    if iframe:
        await tab.switch_to_frame(iframe)
        # Now interact with elements inside the iframe
        button = await tab.find('button')
        await button.click()
        # Switch back to main frame
        await tab.switch_to_main_frame()
    
    # Method 2: Find iframe by name
    iframe = await tab.find_frame_by_name('captcha-frame')
    if iframe:
        await tab.switch_to_frame(iframe)
        # Interact with iframe content
        await tab.switch_to_main_frame()
    
    # Method 3: Find iframe element and switch to it
    iframe_element = await tab.find('iframe[src*="captcha"]')
    if iframe_element:
        await tab.switch_to_frame(iframe_element)
        # Interact with iframe content
        await tab.switch_to_main_frame()
    
    # Method 4: Switch by index (useful for multiple iframes)
    frames = await tab.get_frames()
    if len(frames) > 1:
        await tab.switch_to_frame_by_index(1)  # Switch to second frame
        # Interact with iframe content
        await tab.switch_to_main_frame()

if __name__ == '__main__':
    asyncio.run(main())
```

### Real-world example: Working with embedded forms

```python
import asyncio
import truedriver as zd

async def handle_embedded_form():
    browser = await zd.start()
    tab = await browser.get('https://example.com/contact')
    
    # Find the embedded form iframe
    form_iframe = await tab.find_frame_by_url(r'.*forms\.example\.com.*')
    
    if form_iframe:
        # Switch to the form iframe
        await tab.switch_to_frame(form_iframe)
        
        # Fill out the form inside the iframe
        name_field = await tab.find('input[name="name"]')
        await name_field.send_keys('John Doe')
        
        email_field = await tab.find('input[name="email"]')
        await email_field.send_keys('john@example.com')
        
        submit_button = await tab.find('button[type="submit"]')
        await submit_button.click()
        
        # Wait for submission confirmation
        await tab.find('Success', timeout=10)
        
        # Switch back to main frame
        await tab.switch_to_main_frame()
        
        print('Form submitted successfully')
    
    await browser.stop()

if __name__ == '__main__':
    asyncio.run(handle_embedded_form())
```

### Tips for iframe interaction

- Always switch back to the main frame when done with iframe content
- Use `get_current_frame()` to check which frame you're currently in
- Use `get_frames()` to list all available frames for debugging
- Frame switching affects all subsequent element operations (find, click, etc.)
- Some iframes may take time to load - use appropriate timeouts
