import truedriver as td


async def test_browserscan(browser: td.Browser) -> None:
    page = await browser.get("https://www.browserscan.net/bot-detection")

    # wait for the page to fully load
    await page.wait_for_ready_state("complete")

    # give the javascript some time to finish executing
    await page.wait(2)

    element = await page.find_element_by_text("Test Results:")
    assert (
        element is not None
        and element.parent is not None
        and isinstance(element.parent.children[-1], td.Element)
    )
    assert element.parent.children[-1].text == "Normal"
