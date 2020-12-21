from playwright.browser import Browser

import asyncio
from playwright import async_playwright
import random

BASE_URL = 'https://qamania.org/'
PAGES = (('Home', 'QA Mania'), ('Blog', 'Blog'), ('Useful links', 'Useful links'))


# тут можна передати логін/пароль
# here you can pass login/password to test function
async def open_test(browser: Browser, data: tuple, id: int):
    print(f'start #{id} thread')
    context = await browser.newContext()
    page = await context.newPage()
    await page.goto(BASE_URL)
    await page.click(f'text={data[0]}')
    title = await page.title()
    result = 'ok' if data[1] in title else 'not ok'
    print(f'Thread #{id}: result for page {data[0]} --> {result}')
    await page.close()
    await context.close()


async def main():
    print('start main')
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        tasks = list()
        for thread in range(10):
            tasks.append(open_test(browser, random.choice(PAGES), thread))
        await asyncio.gather(*tasks)
        await browser.close()


asyncio.run(main())
