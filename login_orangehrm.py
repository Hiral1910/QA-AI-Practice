
import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import time

async def run():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            # Maximize the browser window
            await page.set_viewport_size({"width": 1920, "height": 1080})
            await page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
            await page.fill('input[name="username"]', "Admin")
            await page.fill('input[name="password"]', "admin123")
            await page.click('button[type="submit"]')
            try:
                await page.wait_for_selector('div.oxd-topbar-header-title', timeout=10000)
                # Assertion: Check if login was successful by checking the page title
                title = await page.title()
                assert "OrangeHRM" in title, "Assertion failed: Login did not reach OrangeHRM dashboard."
            except PlaywrightTimeoutError:
                raise AssertionError("Assertion failed: Chrome did not execute the script or login failed.")
            time.sleep(3)  # Hold for 2 seconds before closing
            await browser.close()
    except Exception as e:
        print(f"Test failed: {e}")

asyncio.run(run())
