import json


class Cookies:
    
    def __init__(self, browser, filepath):
        self.browser = browser
        self.filepath = filepath

    async def save_cookies(self):
        with open(self.filepath, 'w') as file:
            try:
                # For the Selenium cookies management:
                json.dump(self.browser.get_cookies(), file)
            except Exception as e:
                # For the Playwright cookies management:
                json.dump(await self.browser.cookies(), file)
        print(f"Cookies are saved to {self.filepath}")

    async def load_cookies(self):
        try:
            with open(self.filepath, 'r') as file:
                cookies = json.load(file)
                for cookie in cookies:
                    self.browser.add_cookie(cookie)
        except Exception as e:
            print("No cookies found. The script will create a new cookie.")

