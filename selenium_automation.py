from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

from bs4 import BeautifulSoup
from dotenv import load_dotenv

from tools import load_selectors, TryExcept, user_agents
from session_management import Cookies
import asyncio
import os


async def driver(headless = False):
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={await user_agents()}")
    options.add_argument("--window-size=1920, 1200")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--verbose")

    if headless:
        options.add_argument("--headless")
    else:
        pass

    browser = webdriver.Chrome(options = options)
    return browser


async def go_automation(url, headless = False):
    # Loading environment variable to avoid the leaking of sensitive credentials:
    load_dotenv()
    user_email = os.getenv('user_email')
    user_password = os.getenv('user_password')

    # Initilazing HTML (CSS) selectors
    selector = await load_selectors('html_selectors')

    # Initiating Selenium automation
    browser = await driver(headless)
    browser.get(url)

    # Loading cookies if there's any:
    cookies = Cookies(browser, 'cookies.json')
    await cookies.load_cookies()
    browser.refresh()

    try:
        # Finding a login button
        login_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector['login_button'])))
        login_button.click()
        print("Login button clicked")
        await asyncio.sleep(3)

        # Finding a username section:
        username_placeholder = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector['username_placeholder'])))
        username_placeholder.click()
        print("Username section clicked")
        await asyncio.sleep(3)
        username_placeholder.send_keys(user_email)

        # Finding a password section:
        password = browser.find_element(By.CSS_SELECTOR, selector['password_placeholder'])
        await asyncio.sleep(3)
        password.click()
        await asyncio.sleep(3)
        password.send_keys(user_password)
        print("Password section clicked")

        # Finding a login button:
        submit_button = browser.find_element(By.CSS_SELECTOR, selector['submit_button'])
        submit_button.click()
        print("Succesfully logged in")
        await asyncio.sleep(3)

        # Saving cookies
        await cookies.save_cookies()

    except Exception as e:
        print("Already logged in")
    await asyncio.sleep(3)

    browser.quit()

