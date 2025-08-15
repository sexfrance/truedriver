import asyncio

import truedriver as td


async def main() -> None:
    browser = await td.start()
    page = await browser.get(
        "https://cdpdriver.github.io/examples/login-page.html",
    )

    # TODO: Sign-up and login

    await browser.stop()


if __name__ == "__main__":
    asyncio.run(main())
