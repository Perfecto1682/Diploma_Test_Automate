import allure
import requests
from ..config.settings import BASE_URL_API, MY_HEADERS


@allure.title("Поиск билета в одну сторону - позитивная проверка")
@allure.feature("GET")
@allure.severity("blocker")
def test_get_oneway_positive() -> str:
    city1 = "MOW"
    city2 = "STW"
    date = "2024-12-15"
    with allure.step("Получение списка билетов в одну сторону"):
        tickets_list = requests.get(
            BASE_URL_API + f'origin_iata={city1}&destination_iata={city2}&'
                           f'depart_start={date}&depart_range=6&return_range=6&affiliate=false&market=ru',
            headers=MY_HEADERS  # Используем MY_HEADERS из settings.py
        )

    lst = tickets_list.json()

    with allure.step("Проверка"):
        assert len(lst) > 0, "Результаты поиска не найдены"


@allure.title("Поиск билета в одну сторону с некорректными параметрами - негативная проверка")
@allure.feature("GET")
@allure.severity("blocker")
def test_get_oneway_negative() -> str:
    city1 = "MOW"
    city2 = "XXX"  # Некорректный город
    date = "2024-12-15"
    with allure.step("Получение списка билетов с некорректными параметрами"):
        tickets_list = requests.get(
            BASE_URL_API + f'origin_iata={city1}&destination_iata={city2}&depart_start={date}'
                           f'&depart_range=6&return_range=6&affiliate=false&market=ru',
            headers=MY_HEADERS  # Используем MY_HEADERS из settings.py
        )

    lst = tickets_list.json()

    with allure.step("Проверка наличия ошибки для некорректного города"):
        assert 'errors' in lst, "Ошибки не найдены для некорректного города"
        assert lst['errors'].get('destination_iata') == 'Unknown city iata: "XXX", try \'MOW\'', \
            f"Ошибка: {lst['errors'].get('destination_iata')}"


@allure.title("Поиск билета с корректной датой - позитивная проверка")
@allure.feature("GET")
@allure.severity("normal")
def test_get_oneway_date_positive() -> str:
    city1 = "MOW"
    city2 = "STW"
    date = "2024-12-15"  # Корректная дата
    with allure.step("Получение списка билетов с корректной датой"):
        tickets_list = requests.get(
            BASE_URL_API + f'origin_iata={city1}&destination_iata={city2}&depart_start={date}&depart_range=6'
                           f'&return_range=6&affiliate=false&market=ru',
            headers=MY_HEADERS  # Используем MY_HEADERS из settings.py
        )

    # Проверяем статус ответа
    assert tickets_list.status_code == 200, f"Ошибка при запросе: {tickets_list.status_code}"

    lst = tickets_list.json()

    with allure.step("Вывод данных ответа для анализа структуры"):
        print(lst)  # Это поможет вам понять структуру данных и найти нужные поля

    with allure.step("Проверка наличия данных в ответе"):
        # Проверка, что в ответе есть хотя бы один билет
        assert len(lst['prices']) > 0, "Список билетов пуст"

    with allure.step("Проверка правильности данных о билетах"):
        # Проверяем, что каждый элемент в списке содержит необходимые данные
        for ticket in lst['prices']:
            assert 'value' in ticket, "Отсутствует цена в билете"
            assert 'depart_date' in ticket, "Отсутствует дата вылета в билете"
            assert 'gate' in ticket, "Отсутствует информация о gate в билете"


@allure.title("Поиск билета туда и обратно - позитивная проверка")
@allure.feature("GET")
@allure.severity("normal")
def test_get_roundtrip_positive() -> str:
    city1 = "MOW"
    city2 = "STW"
    date = "2024-12-15"
    return_date = "2024-12-22"
    with allure.step("Получение списка билетов туда и обратно"):
        tickets_list = requests.get(
            BASE_URL_API + f'origin_iata={city1}&destination_iata={city2}&depart_start={date}&depart_range=6'
                           f'&return_start={return_date}&return_range=6&affiliate=false&market=ru',
            headers=MY_HEADERS  # Используем MY_HEADERS из settings.py
        )

    lst = tickets_list.json()

    with allure.step("Проверка"):
        assert len(lst) > 0, "Результаты поиска не найдены для билетов туда и обратно"


@allure.title("Поиск билета с параметрами по умолчанию - позитивная проверка")
@allure.feature("GET")
@allure.severity("blocker")
def test_get_default_search() -> str:
    city1 = "MOW"
    city2 = "STW"
    date = "2024-12-15"
    with allure.step("Получение списка билетов с параметрами по умолчанию"):
        tickets_list = requests.get(
            BASE_URL_API + f'origin_iata={city1}&destination_iata={city2}&depart_start={date}&depart_range=6'
                           f'&return_range=6&affiliate=false&market=ru',
            headers=MY_HEADERS  # Используем MY_HEADERS из settings.py
        )

    lst = tickets_list.json()

    with allure.step("Проверка"):
        assert len(lst) > 0, "Результаты поиска не найдены с параметрами по умолчанию"
