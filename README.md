# Truedriver ✌️

[![License](https://img.shields.io/github/license/sexfrance/truedriver)](LICENSE)
[![Pypi Version](https://img.shields.io/pypi/v/truedriver)](https://pypi.org/project/truedriver/)
[![Issues](https://img.shields.io/github/issues/sexfrance/truedriver)]()
[![Pull Requests](https://img.shields.io/github/issues-pr/sexfrance/truedriver)]()
[![codecov](https://codecov.io/github/sexfrance/truedriver/branch/main/graph/badge.svg?token=F7K641TYFZ)](https://codecov.io/github/sexfrance/truedriver)
[![Downloads](https://img.shields.io/pypi/dm/truedriverlogo=IOTA)()]
  <a href="https://discord.cyberious.xyz">💬 Discord</a>
    ·
    <a href="https://github.com/sexfrance/truedriver/issues">⚠️ Report Bug</a>
    ·
    <a href="https://github.com/sexfrance/truedriver/issues">💡 Request Feature</a>

> This package is a fork of [`cdpdriver/zendriver`](https://github.com/cdpdriver/zendriver/), which itself is a fork of [`ultrafunkamsterdam/nodriver`](https://github.com/ultrafunkamsterdam/nodriver/), created to add new features, compile unmerged bugfixes, and increase community engagement.

- **Documentation:** [zendriver.dev](https://zendriver.dev)
- **AI-generated wiki:** [deepwiki.com/cdpdriver/zendriver](https://deepwiki.com/cdpdriver/zendriver)

Truedriver is a blazing fast, async-first, undetectable webscraping/web automation framework implemented using the Chrome Devtools Protocol. Visit websites, scrape content, and run JavaScript using a real browser (no Selenium/Webdriver) all with just a few lines of Python.

**Docker support is here!** Check out [`cdpdriver/truedriver-docker`](https://github.com/cdpdriver/truedriver-docker) for an example of how to run Truedriver with a real, GPU-accelerated browser (not headless) in a Docker container. (Linux-only)

## Features

- **Undetectable** - Truedriver uses the Chrome Devtools Protocol instead of Selenium/WebDriver, making it (almost) impossible to detect
- **Blazing fast** - Chrome Devtools Protocol is _fast_, much faster than previous Selenium/WebDriver solutions. CDP combined with an async Python API makes Truedriver highly performant.
- **Feature complete and easy to use** - Packed with allowing you to get up and running in just a few lines of code.
- **First-class Docker support** - Traditionally, browser automation has been incredibly difficult to package with Docker, especially if you want to run real, GPU-accelerated Chrome (not headless). Now, deploying with Docker is easier than ever using the officially supported [truedriver-docker project template](https://github.com/cdpdriver/truedriver-docker).
- **Automatic cookie and profile management** - By default, uses fresh profile on each run, cleaning up on exit. Or, save and load cookies to a file to avoid repeating tedious login steps.
- **Smart element lookup** - Find elements selector or text, including iframe content. This could also be used as wait condition for a element to appear, since it will retry for the duration of `timeout` until found. Single element lookup by text using `tab.find()` accepts a `best_match flag`, which will not naively return the first match, but will match candidates by closest matching text length.
- **Full iframe support** - Switch between iframe contexts to interact with embedded content like hCaptcha, forms, or any other iframe-based widgets. Supports finding frames by URL, name, element, or index.
- **Simple proxy support** - Easy proxy configuration with multiple formats including authenticated proxies. Works reliably with Chrome, Brave, and Edge using URL-based authentication (like Playwright).
- **Easy debugging** - Descriptive `repr` for elements, which represents the element as HTML, makes debugging much easier.

## Installation

To install, simply use `pip` (or your favorite package manager):

```sh
pip install truedriver
# or uv add truedriver, poetry add truedriver, etc.
```

## Usage

### Basic Example

Example for visiting [https://www.browserscan.net/bot-detection](https://www.browserscan.net/bot-detection) and saving a screenshot of the results:

```python
import asyncio

import truedriver as td


async def main():
    browser = await td.start()
    page = await browser.get("https://www.browserscan.net/bot-detection")
    await page.save_screenshot("browserscan.png")
    await browser.stop()


if __name__ == "__main__":
    asyncio.run(main())
```

### Iframe Interaction

Interact with embedded content like hCaptcha, forms, or widgets:

```python
import asyncio
import truedriver as td

async def main():
    browser = await td.start()
    tab = await browser.get("https://example.com/page-with-iframe")

    # Find iframe by URL pattern
    hcaptcha_frame = await tab.find_frame_by_url(r".*hcaptcha\.com.*")
    if hcaptcha_frame:
        # Switch to the iframe
        await tab.switch_to_frame(hcaptcha_frame)

        # Now interact with elements inside the iframe
        checkbox = await tab.find("#checkbox")
        await checkbox.click()

        # Switch back to main frame
        await tab.switch_to_main_frame()

    await browser.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

### Proxy Support

Truedriver supports proxies in multiple formats, including authenticated proxies. Just pass the `proxy` argument to `td.start()`:

**Supported formats:**

- Simple: `"ip:port"` or `"http://ip:port"`
- Authenticated (string): `"username:password@ip:port"` or `"http://username:password@ip:port"`
- Authenticated (dict): `{ "server": "ip:port", "username": "user", "password": "pass" }`

**Example:**
```python
import asyncio
import truedriver as td

async def main():
    # Simple proxy
    browser = await td.start(proxy="proxy.example.com:8080")


    # Authenticated proxy (string format)
    browser = await td.start(proxy="your-username:your-password@proxy.example.com:8080")

    # Authenticated proxy (dict format)
    proxy_config = {
        "server": "proxy.example.com:8080",
        "username": "your-username",
        "password": "your-password"
    }
    browser = await td.start(proxy=proxy_config)


    tab = await browser.get("https://httpbin.org/ip")
    print(await tab.get_content())
    await browser.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

> **Note:** Replace `your-username`, `your-password`, and `proxy.example.com:8080` with your actual proxy credentials. Truedriver automatically handles proxy authentication using the Chrome DevTools Protocol—no manual CDP handlers required.

### Advanced Configuration

Example with multiple features:

```python
import asyncio
import truedriver as td

async def main():
    # Start browser with proxy and custom user agent
    browser = await td.start(
        headless=False,
        proxy="user:pass@proxy.example.com:8080",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        browser_args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-web-security"
        ]
    )

    tab = await browser.get("https://example.com")

    # Work with iframes if needed
    frames = await tab.get_frames()
    print(f"Found {len(frames)} frames")

    # Find and interact with elements
    element = await tab.find("Click me")
    await element.click()

    await browser.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

Check out the [Quickstart](https://zendriver.dev/quickstart/) for more information and examples.

## What's New in Truedriver

Truedriver enhances the original zendriver with powerful new features for advanced web automation:

### 🎯 **Full Iframe Support**

- **Switch between iframe contexts** with ease using `tab.switch_to_frame()`
- **Find frames by URL, name, or element** using `tab.find_frame_by_url()`, `tab.find_frame_by_name()`
- **Frame-aware operations** - all element finding and JavaScript execution works within the current frame
- **Perfect for hCaptcha, forms, and embedded widgets**

### 🌐 **Simple Proxy Support**

- **Multiple configuration formats**:
  - Simple: `"ip:port"`
  - Authenticated: `"user:pass@ip:port"`
  - Dict: `{"server": "ip:port", "username": "user", "password": "pass"}`
- **URL-based authentication** (like Playwright) - no complex CDP auth handlers
- **Works reliably** with Chrome, Brave, and Edge

### 🥷 **Enhanced Stealth**

- **Advanced anti-detection techniques** for bypassing sophisticated bot detection
- **Improved fingerprint randomization** and user agent handling
- **Optimized browser arguments** for maximum undetectability
- **Better evasion** of modern anti-bot solutions

### 📦 **Easy Migration from zendriver**

All zendriver code works with truedriver - just change your import:

```python
# Old
import zendriver as td

# New
import truedriver as td
```

### 🚀 **Real-World Examples**

- **Discord account creation** with proxy rotation and iframe handling
- **hCaptcha solving** using iframe switching
- **Complex form automation** across multiple frames
- **Stealth scraping** with enhanced undetection

## Rationale for the fork

Truedriver remains committed to `zendriver`'s goals of staying undetected for all modern anti-bot solutions and also keeps with the batteries-included approach of its predecessor. This project is a specialized fork of [`zendriver`](https://github.com/cdpdriver/zendriver/) which itself was forked from the original [`nodriver` repo](https://github.com/ultrafunkamsterdam/nodriver/).

Truedriver aims to provide enhanced stealth capabilities by:

1. Implementing advanced anti-detection techniques
2. Fine-tuning browser arguments for maximum stealth
3. Maintaining compatibility with zendriver's API while focusing on undetectability
4. Providing specialized builds for bypassing sophisticated bot detection systems

## Credits

- Original [`nodriver`](https://github.com/ultrafunkamsterdam/nodriver/) by ultrafunkamsterdam
- [`zendriver`](https://github.com/cdpdriver/zendriver/) by cdpdriver team
- Truedriver enhancements and stealth improvements by the current maintainer

With these enhancements, we hope to further the development of state-of-the-art open-source web automation tools, helping to make the web truly accessible for automation purposes.

## Contributing

Contributions of all types are always welcome! Please see [CONTRIBUTING.md](https://github.com/cdpdriver/truedriver/blob/main/CONTRIBUTING.md) for details on how to contribute.

### Getting additional help

If you have a question, bug report, or want to make a general inquiry about the project, please create a new GitHub issue. If you are having a problem with Truedriver, please make sure to include your operating system, Chrome version, code example demonstrating the issue, and any other information that may be relevant.

Questions directed to any personal accounts outside of GitHub will be ignored.
