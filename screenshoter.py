import os
from selenium import webdriver


def get_screenshot(url):
    # формируем путь до драйвера,
    # который лежит в одной папке с запускаемым скриптом
    current_path = os.path.dirname(os.path.abspath(__file__))
    geckodriver_path = os.path.join(current_path, 'geckodriver')
    # задаем опции для вебдрайвера
    options = webdriver.FirefoxOptions()
    options.headless = True
    # инстанцируем вебдрайвер
    driver = webdriver.Firefox(executable_path=geckodriver_path, options=options)
    # переходим на сайт и делаем скриншот
    driver.get(url)
    screen = driver.get_screenshot_as_png()
    driver.quit()
    return screen