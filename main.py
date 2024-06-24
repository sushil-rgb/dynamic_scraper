# from playwright_automation import go_automation
from selenium_automation import go_automation
import asyncio


async def main():
    headless_mode = True
    return await go_automation('https://booksmandala.com/', headless_mode)


if __name__ == "__main__":
    asyncio.run(main())

