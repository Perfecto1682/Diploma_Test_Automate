
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


def test_search_valid_origin(search_page):
    origin = get_random_search_term("valid_origin")
    destination = get_random_search_term("valid_destination")
    search_page.search_flight(origin, destination)
    results = search_page.get_results()
    assert len(results) > 0, "Результаты поиска не найдены"


def test_search_invalid_origin(search_page):
    origin = get_random_search_term("invalid_origin")
    destination = get_random_search_term("invalid_destination")
    search_page.search_flight(origin, destination)
    results = search_page.get_results()
    assert len(results) == 0, "Найдены результаты для несуществующего пункта отправления"


def test_search_with_passengers_and_class(search_page):
    origin = get_random_search_term("valid_origin")
    destination = get_random_search_term("valid_destination")
    search_page.search_flight(origin, destination)
    search_page.select_passenger_and_class(adults=2)
    results = search_page.get_results()
    assert len(results) > 0, "Результаты не найдены с выбранными параметрами пассажиров и класса"


def test_search_invalid_date(search_page):
    origin = get_random_search_term("valid_origin")
    destination = get_random_search_term("valid_destination")
    search_page.search_flight(origin, destination)
    invalid_date_locator = ("css selector", "div[data-test-id='invalid-date']")
    with pytest.raises(Exception):
        search_page.wait_for_element_clickable(invalid_date_locator, timeout=5).click()
    results = search_page.get_results()
    assert len(results) == 0, "Результаты найдены для недоступной даты"


def test_check_search_results_display(search_page):
    origin = get_random_search_term("valid_origin")
    destination = get_random_search_term("valid_destination")
    search_page.search_flight(origin, destination)
    results = search_page.get_results()
    assert len(results) > 0, "Результаты поиска не отображаются"
    assert all(result.is_displayed() for result in results), "Не все результаты поиска отображаются корректно"
