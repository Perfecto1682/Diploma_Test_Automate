import allure
from ..pages.main_page import MainPage
from ..config.settings import SEARCH_TERMS
from ..utils.webdriver_manager import get_driver


# Позитивные проверки
@allure.title("Позитивная проверка: Заполнение поля 'Откуда'")
@allure.severity("critical")
def test_fill_origin():
    with allure.step("Настроить WebDriver"):
        driver = get_driver()  # Используем get_driver из webdriver_manager
        driver.implicitly_wait(10)

    try:
        with allure.step("Открыть главную страницу"):
            main_page = MainPage(driver)

        with allure.step("Очистить поле 'Откуда' и заполнить его новым значением"):
            origin = SEARCH_TERMS["valid_origin"][0]  # Используем значение из SEARCH_TERMS
            main_page.fill_origin(origin)

        with allure.step("Проверить, что поле 'Откуда' заполнено корректно"):
            actual_value = driver.find_element(*main_page.origin_locator).get_attribute("value")
            assert actual_value == origin, f"Ожидалось '{origin}', но найдено '{actual_value}'"
    finally:
        driver.quit()


@allure.title("Позитивная проверка: Заполнение поля 'Куда'")
@allure.severity("critical")
def test_fill_destination():
    with allure.step("Настроить WebDriver"):
        driver = get_driver()  # Используем get_driver из webdriver_manager
        driver.implicitly_wait(10)

    try:
        with allure.step("Открыть главную страницу"):
            main_page = MainPage(driver)

        with allure.step("Заполнить поле 'Куда'"):
            destination = SEARCH_TERMS["valid_destination"][0]  # Используем значение из SEARCH_TERMS
            main_page.fill_destination(destination)

        with allure.step("Проверить, что поле 'Куда' заполнено корректно"):
            actual_value = driver.find_element(*main_page.destination_locator).get_attribute("value")
            assert actual_value == destination, f"Ожидалось '{destination}', но найдено '{actual_value}'"
    finally:
        driver.quit()


# Негативные проверки
@allure.title("Негативная проверка: Пустое значение в поле 'Откуда'")
@allure.severity("major")
def test_empty_origin():
    with allure.step("Настроить WebDriver"):
        driver = get_driver()  # Используем get_driver из webdriver_manager
        driver.implicitly_wait(10)

    try:
        with allure.step("Открыть главную страницу"):
            main_page = MainPage(driver)

        with allure.step("Очистить поле 'Откуда' и оставить его пустым"):
            main_page.fill_origin("")

        with allure.step("Проверить, что поле 'Откуда' пустое"):
            actual_value = driver.find_element(*main_page.origin_locator).get_attribute("value")
            assert actual_value == "", f"Поле 'Откуда' не очистилось: '{actual_value}'"
    finally:
        driver.quit()


@allure.title("Негативная проверка: Пустое значение в поле 'Куда'")
@allure.severity("major")
def test_empty_destination():
    with allure.step("Настроить WebDriver"):
        driver = get_driver()  # Используем get_driver из webdriver_manager
        driver.implicitly_wait(10)

    try:
        with allure.step("Открыть главную страницу"):
            main_page = MainPage(driver)

        with allure.step("Очистить поле 'Куда'"):
            main_page.fill_destination("")

        with allure.step("Проверить, что поле 'Куда' пустое"):
            actual_value = driver.find_element(*main_page.destination_locator).get_attribute("value")
            assert actual_value == "", f"Поле 'Куда' не очистилось: '{actual_value}'"
    finally:
        driver.quit()


@allure.title("Негативная проверка: Поля сбрасываются после обновления страницы")
@allure.severity("minor")
def test_fields_reset_after_refresh():
    with allure.step("Настроить WebDriver"):
        driver = get_driver()  # Используем get_driver из webdriver_manager
        driver.implicitly_wait(10)

    try:
        with allure.step("Открыть главную страницу"):
            main_page = MainPage(driver)

        with allure.step("Заполнить поля 'Откуда' и 'Куда'"):
            origin = SEARCH_TERMS["valid_origin"][0]  # Используем значение из SEARCH_TERMS
            destination = SEARCH_TERMS["valid_destination"][0]  # Используем значение из SEARCH_TERMS
            main_page.fill_origin(origin)
            main_page.fill_destination(destination)

        with allure.step("Получить начальное значение поля 'Откуда' после автоматического заполнения"):
            initial_origin_value = driver.find_element(*main_page.origin_locator).get_attribute("value")

        with allure.step("Обновить страницу"):
            driver.refresh()

        with allure.step("Проверить, что поле 'Куда' сбросилось, а 'Откуда' соответствует автоматическому значению"):
            reset_origin_value = driver.find_element(*main_page.origin_locator).get_attribute("value")
            reset_destination_value = driver.find_element(*main_page.destination_locator).get_attribute("value")

            assert reset_origin_value == initial_origin_value, (
                f"Поле 'Откуда' не соответствует ожиданиям: "
                f"'{reset_origin_value}' != '{initial_origin_value}'"
            )

            assert reset_destination_value == "", f"Поле 'Куда' не сбросилось: '{reset_destination_value}'"
    finally:
        driver.quit()
