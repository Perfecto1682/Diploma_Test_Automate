from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from ..config.settings import BASE_URL_UI

class MainPage:

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.driver.get(BASE_URL_UI)  # Используем URL из настроек
        self.driver.maximize_window()

        # Локаторы
        self.origin_locator = (By.ID, "avia_form_origin-input")
        self.destination_locator = (By.ID, "avia_form_destination-input")

    def fill_origin(self, origin: str) -> None:
        """Заполнение поля Откуда"""
        element_origin = self.driver.find_element(*self.origin_locator)
        element_origin.clear()
        element_origin.send_keys(Keys.CONTROL + "a")  # Выделить всё
        element_origin.send_keys(Keys.BACKSPACE)  # Удалить выделенное
        element_origin.send_keys(origin)

    def fill_destination(self, destination: str) -> None:
        """Заполнение поля Куда"""
        element_destination = self.driver.find_element(*self.destination_locator)
        element_destination.clear()
        element_destination.send_keys(Keys.CONTROL + "a")  # Выделить всё
        element_destination.send_keys(Keys.BACKSPACE)  # Удалить выделенное
        element_destination.send_keys(destination)
