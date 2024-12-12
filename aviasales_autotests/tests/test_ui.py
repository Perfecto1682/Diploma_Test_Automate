import pytest
from ..config.settings import BASE_URL_UI, get_random_search_term
from ..pages.search_page import SearchPage

@pytest.fixture(scope="module")
def driver():
    from ..utils.webdriver_manager import get_driver
    driver = get_driver()
    yield driver
    driver.quit()

@pytest.fixture
def search_page(driver):
    page = SearchPage(driver)
    page.open_url(BASE_URL_UI)
    return page

def test_search_with_departure_and_return_date(search_page):
    """
    Проверка поиска с датой отправления и обратного рейса.
    """
    origin = get_random_search_term("valid_origin")
    destination = get_random_search_term("valid_destination")
    departure_date = "24.12.2024"
    return_date = "25.12.2024"

    search_page.search_flight(origin, destination, departure_date, return_date)
    results = search_page.get_results()
    assert len(results) > 0, "Результаты поиска не найдены"

def test_search_with_departure_only(search_page):
    """
    Проверка поиска только с датой отправления.
    """
    origin = get_random_search_term("valid_origin")
    destination = get_random_search_term("valid_destination")
    departure_date = "24.12.2024"

    search_page.search_flight(origin, destination, departure_date)
    results = search_page.get_results()
    assert len(results) > 0, "Результаты поиска не найдены"

def test_search_invalid_departure_date(search_page):
    """
    Проверка поиска с недоступной датой отправления.
    """
    origin = get_random_search_term("valid_origin")
    destination = get_random_search_term("valid_destination")
    invalid_date = "11.12.2024"

    with pytest.raises(ValueError, match=f"Дата отправления {invalid_date} недоступна!"):
        search_page.search_flight(origin, destination, invalid_date)

def test_search_with_passengers(search_page):
    """
    Проверка поиска с выбором количества пассажиров.
    """
    origin = get_random_search_term("valid_origin")
    destination = get_random_search_term("valid_destination")
    departure_date = "24.12.2024"

    search_page.search_flight(origin, destination, departure_date)
    search_page.select_passenger_and_class(adults=2)
    results = search_page.get_results()
    assert len(results) > 0, "Результаты поиска не найдены для указанного количества пассажиров"
