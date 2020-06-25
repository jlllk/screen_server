import logging
import os
import sys

from requests import post
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(
    format=FORMAT,
    level=10,
    filename='logs/screenshoter/screen.log',
    filemode='a',
)


def send_image(id, screen, token, request_url):
    data = {
        'id': id,
        'token': token
    }
    files = {
        'screen': screen
    }
    r = post(
        url=request_url + '/save/screenshot',
        data=data,
        files=files
    )
    return r.status_code


def get_screenshot(id, url, token, request_url):
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

    status = send_image(id, screen, token, request_url)
    logging.info(
        'Скрин отправлен на {url}. Статус ответа: {st}'.format(
            st=status, url=request_url
        )
    )


if __name__ == '__main__':
    args = sys.argv
    get_screenshot(id=args[1], url=args[2], token=args[3])
