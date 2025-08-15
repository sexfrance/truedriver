import asyncio

import truedriver as td


async def main() -> None:
    browser = await td.start()
    tab = browser.main_tab
    await tab.set_user_agent("My user agent", accept_language="de", platform="Win32")

    print(await tab.evaluate("navigator.userAgent"))  # My user agent
    print(await tab.evaluate("navigator.language"))  # de
    print(await tab.evaluate("navigator.platform"))  # Win32

    await browser.stop()


if __name__ == "__main__":
    asyncio.run(main())
