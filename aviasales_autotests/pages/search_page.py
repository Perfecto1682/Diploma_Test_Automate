from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SearchPage(BasePage):
    FROM_FIELD = (By.CSS_SELECTOR, "input[data-test-id='origin-input']")
    TO_FIELD = (By.CSS_SELECTOR, "input[data-test-id='destination-input']")
    DATE_FIELD = (By.CSS_SELECTOR, "div[data-test-id='start-date-value']")
    AVAILABLE_DATE = "div[data-test-id='date-{date}']"
    UNAVAILABLE_DATE = "div[aria-label='{aria_label}']"
    NO_RETURN_BUTTON = (By.CSS_SELECTOR, "button[data-test-id='calendar-action-button']")
    RETURN_DATE_FIELD = (By.CSS_SELECTOR, "div[data-test-id='return-date-value']")
    SEARCH_SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[data-test-id='form-submit']")
    RESULT_ITEMS = (By.CSS_SELECTOR, "div[data-test-id='search-results-items-list']")
    PASSENGER_SELECTOR = (By.CSS_SELECTOR, "button[data-test-id='passenger-selector']")
    PASSENGER_OPTION = "button[data-test-id='passenger-{option}']"
    CLASS_OPTION = "button[data-test-id='class-{travel_class}']"
    SUGGESTED_CITY = "li[data-test-id='suggested-city-{code}']"
    NEW_TAB_CHECKBOX = (By.CSS_SELECTOR, "input[data-test-id='checkbox']")

    CITY_CODES = {
        "Москва": "MOW",
        "Санкт-Петербург": "LED",
        "Казань": "KZN",
        "Новосибирск": "OVB",
        "Екатеринбург": "SVX",
        "Калуга": "KLF",
        "Владивосток": "VVO",
        "Краснодар": "KRR"
    }

    def search_flight(self, origin, destination, departure_date, return_date=None):
        origin_field = self.find_element(*self.FROM_FIELD)
        origin_field.click()
        origin_field.clear()
        origin_field.send_keys(origin)
        origin_field.send_keys(Keys.ENTER)

        destination_field = self.find_element(*self.TO_FIELD)
        destination_field.click()
        destination_field.clear()
        destination_field.send_keys(destination)

        city_code = self.CITY_CODES.get(destination)
        if not city_code:
            raise ValueError(f"Город назначения {destination} недоступен!")

        suggested_city_locator = (By.CSS_SELECTOR, self.SUGGESTED_CITY.format(code=city_code))
        try:
            self.wait_for_element_clickable(suggested_city_locator).click()
        except Exception as e:
            raise ValueError(f"Город назначения {destination} недоступен по причине: {str(e)}")

        date_field = self.find_element(*self.DATE_FIELD)
        date_field.click()

        departure_locator = (By.CSS_SELECTOR, self.AVAILABLE_DATE.format(date=departure_date))
        try:
            self.wait_for_element_clickable(departure_locator).click()
        except Exception as e:
            raise ValueError(f"Дата отправления {departure_date} недоступна по причине: {str(e)}")

        if return_date:
            return_locator = (By.CSS_SELECTOR, self.AVAILABLE_DATE.format(date=return_date))
            try:
                self.wait_for_element_clickable(return_locator).click()
            except Exception as e:
                raise ValueError(f"Дата обратного рейса {return_date} недоступна по причине: {str(e)}")
        else:
            self.wait_for_element_clickable(self.NO_RETURN_BUTTON).click()

        new_tab_checkbox = self.find_element(*self.NEW_TAB_CHECKBOX)
        if new_tab_checkbox.is_selected():
            new_tab_checkbox.click()

        self.wait_for_element_clickable(self.SEARCH_SUBMIT_BUTTON).click()

    def select_passenger_and_class(self, passengers, travel_class):
        self.find_element(*self.PASSENGER_SELECTOR).click()
        passenger_locator = (By.CSS_SELECTOR, self.PASSENGER_OPTION.format(option=passengers))
        self.wait_for_element_clickable(passenger_locator).click()
        class_locator = (By.CSS_SELECTOR, self.CLASS_OPTION.format(travel_class=travel_class))
        self.wait_for_element_clickable(class_locator).click()

    def get_results(self):
        return self.find_elements(*self.RESULT_ITEMS)

    def wait_for_element_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
