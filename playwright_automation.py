from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from tools import Response, list_flattened, user_agents, export_sheet, TryExcept, load_selectors
from session_management import Cookies
from dotenv import load_dotenv
import asyncio
import os


async def go_automation(url, headless):
    # Loading environment variable to avoid the leaking of sensitive credentials:
    load_dotenv()
    user_email = os.getenv('user_email')
    user_password = os.getenv('user_password')

    # Initializing HTML (CSS) selectors:
    selector = await load_selectors('html_selectors')

    # Intilializing playwright automation:
    async with async_playwright() as play:
        browser = await play.chromium.launch(headless = headless)
        context = await browser.new_context(user_agent = await user_agents())

        # Cookies management:
        cookies = Cookies(context, 'cookies.json')

        page = await context.new_page()
        await page.goto(url)

        # Loading cookies if there's any:
        await cookies.load_cookies()
        await page.reload()

        try:
            # Finding a login button:
            login_button = await page.wait_for_selector(selector['login_button'])
            await login_button.click()
            print("Login button clicked.")
            await asyncio.sleep(3)

            # Finding a username section:
            username_placeholder = await page.wait_for_selector(selector['username_placeholder'])
            await username_placeholder.click()
            print("Username section clicked.")
            await asyncio.sleep(3)
            await username_placeholder.type(user_email)

            # Finding a password section:
            password = await page.query_selector(selector['password_placeholder'])
            await asyncio.sleep(3)
            await password.click()
            await asyncio.sleep(3)
            await password.type(user_password)
            print("Password section clicked.")

            # Finding a login button:
            submit_button = await page.query_selector(selector['submit_button'])
            await submit_button.click()
            print("Succesfully logged in")
            await asyncio.sleep(3)

            # Saving cookies:
            await cookies.save_cookies()

        except Exception as e:
            print(str(e))
            print("Already logged in.")

        await asyncio.sleep(3)

        await browser.close()

