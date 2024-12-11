from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open_url(self, url):
        self.driver.get(url)

    def find_element(self, by, locator):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by, locator)))

    def find_elements(self, by, locator):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((by, locator)))
