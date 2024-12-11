from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SearchPage(BasePage):
    # Локаторы для элементов на странице
    FROM_FIELD = (By.CSS_SELECTOR, "input[data-test-id='origin-input']")
    TO_FIELD = (By.CSS_SELECTOR, "input[data-test-id='destination-input']")
    DATE_FIELD = (By.CSS_SELECTOR, "div[data-test-id='start-date-value']")
    AVAILABLE_DATE = (By.CSS_SELECTOR, "div[data-test-id='date-24.12.2024']")
    SEARCH_SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(), 'Найти билеты')]")
    RESULT_ITEMS = (By.CSS_SELECTOR, "div[data-test-id='search-results-items-list']")

    # Локаторы для настроек пассажиров
    PASSENGERS_SETTINGS_BUTTON = (By.CSS_SELECTOR, "div[data-test-id='passenger-numbers']")
    ADD_ADULT_BUTTON = (By.CSS_SELECTOR, "button[data-test-id='increase-button']")

    def search_flight(self, origin, destination):
        # Клик по полю Откуда, очистка и ввод нового значения
        origin_field = self.find_element(*self.FROM_FIELD)
        origin_field.click()  # Клик на поле
        origin_field.clear()  # Очистка поля
        origin_field.send_keys(origin)  # Вводим пункт отправления
        origin_field.send_keys(Keys.ENTER)  # Нажатие Enter для подтверждения ввода

        # Клик по полю Куда, очистка и ввод нового значения
        destination_field = self.find_element(*self.TO_FIELD)
        destination_field.click()  # Клик на поле
        destination_field.clear()  # Очистка поля
        destination_field.send_keys(destination)  # Вводим пункт назначения
        destination_field.send_keys(Keys.ENTER)  # Нажатие Enter для подтверждения ввода

        # Клик по полю даты
        date_field = self.find_element(*self.DATE_FIELD)
        date_field.click()  # Открываем календарь

        # Выбираем доступную дату
        available_date = self.wait_for_element_clickable(self.AVAILABLE_DATE)
        available_date.click()

        # Нажимаем кнопку поиска
        self.wait_for_element_clickable(self.SEARCH_SUBMIT_BUTTON).click()

    def get_results(self):
        # Получаем все результаты поиска
        return self.find_elements(*self.RESULT_ITEMS)

    def select_passenger_and_class(self, adults=1):
        # Открытие настроек пассажиров и добавление взрослых
        self.find_element(*self.PASSENGERS_SETTINGS_BUTTON).click()
        for _ in range(adults - 1):  # Добавляем взрослых
            self.find_element(*self.ADD_ADULT_BUTTON).click()
        # Применяем настройки пассажиров
        self.find_element(*self.PASSENGERS_SETTINGS_BUTTON).click()

    def wait_for_element_clickable(self, locator, timeout=10):
        # Ожидание, пока элемент не станет кликабельным
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
