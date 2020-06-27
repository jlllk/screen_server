import logging
import os

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
    if screen:
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
    return 'Не получилось создать скриншот'


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
    except WebDriverException as e:
        logging.exception(f'Web driver exceptions: {e}')
    finally:
        driver.quit()

    status = send_image(id, screen, token, request_url)
    logging.info(
        'Скрин отправлен на {url}. Статус ответа: {st}'.format(
            st=status, url=request_url
        )
    )
