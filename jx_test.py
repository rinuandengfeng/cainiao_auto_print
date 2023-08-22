from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="./auth/cainiao_state.json")

    # Open new page
    page = context.new_page()

    # Go to https://auth.wms.cainiao.com/console/login?redirectURL=http://cwoutprod.cainiao.com/pickbill
    page.goto("https://cwoutprod.cainiao.com/waveanalysis")


    # Click text=快递公司请选择 >> i
    page.click("text=快递公司请选择 >> i")

    # Click [placeholder="请输入查询"]
    page.click("[placeholder=\"请输入查询\"]")

    # Fill [placeholder="请输入查询"]
    page.fill("[placeholder=\"请输入查询\"]", "东莞圆通")

    # Check text=D东莞圆通 >> input[type="checkbox"]
    page.check("text=D东莞圆通 >> input[type=\"checkbox\"]")

    # Click button:has-text("查询")
    page.click("button:has-text(\"查询\")")

    test_locator = page.locator("text=已选")
    text = test_locator.evaluate("e => e.textContent")
    print(text)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
