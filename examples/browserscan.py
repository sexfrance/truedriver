import asyncio

import truedriver as td

async def main() -> None:
    browser = await td.start()
    page = await browser.get("https://www.browserscan.net/bot-detection")
    await page.wait_for_ready_state("complete")
    await page.save_screenshot("browserscan.png")
    await browser.stop()


if __name__ == "__main__":
    asyncio.run(main())
