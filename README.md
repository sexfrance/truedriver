# Truedriver ✌️

[![License](https://img.shields.io/github/license/sexfrance/truedriver)](LICENSE)
[![Pypi Version](https://img.shields.io/pypi/v/truedriver)](https://pypi.org/project/truedriver/)
[![Issues](https://img.shields.io/github/issues/sexfrance/truedriver)]()
[![Pull Requests](https://img.shields.io/github/issues-pr/sexfrance/truedriver)]()
[![codecov](https://codecov.io/github/sexfrance/truedriver/branch/main/graph/badge.svg?token=F7K641TYFZ)](https://codecov.io/github/sexfrance/truedriver)
[![Downloads](https://img.shields.io/pypi/dm/logmagix?style=for-the-badge&labelColor=black&color=f429ff&logo=IOTA)()]

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
- **Easy debugging** - Descriptive `repr` for elements, which represents the element as HTML, makes debugging much easier.

## Installation

To install, simply use `pip` (or your favorite package manager):

```sh
pip install truedriver
# or uv add truedriver, poetry add truedriver, etc.
```

## Usage

Example for visiting [https://www.browserscan.net/bot-detection](https://www.browserscan.net/bot-detection) and saving a screenshot of the results:

```python
import asyncio

import truedriver as zd


async def main():
    browser = await zd.start()
    page = await browser.get("https://www.browserscan.net/bot-detection")
    await page.save_screenshot("browserscan.png")
    await browser.stop()


if __name__ == "__main__":
    asyncio.run(main())
```

Check out the [Quickstart](https://zendriver.dev/quickstart/) for more information and examples.

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
