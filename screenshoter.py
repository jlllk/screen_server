import logging
import os
import sys

from requests import post
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

LIBRARY = 'https://08748c27f5ef.ngrok.io/save/screenshot'

FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(
    format=FORMAT,
    level=10,
    filename='logs/screenshoter/screen.log',
    filemode='a',
)


def send_image(id, screen, token):
    data = {
        'id': id,
        'token': token
    }
    files = {
        'screen': screen
    }
    r = post(
        url=LIBRARY,
        data=data,
        files=files
    )
    return r.status_code


def get_screenshot(id, url, token):
    current_path = os.path.dirname(os.path.abspath(__file__))
    geckodriver_path = os.path.join(current_path, 'geckodriver')

    options = webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(
        executable_path=geckodriver_path,
        options=options
    )

    try:
        driver.get(url)
        screen = driver.get_screenshot_as_png()
        driver.quit()
    except WebDriverException:
        logging.exception('Web driver exceptions')

    status = send_image(id, screen, token)
    logging.info(f'Скрин отправлен. Статус ответа: {status}')


if __name__ == '__main__':
    args = sys.argv
    get_screenshot(id=args[1], url=args[2], token=args[3])
