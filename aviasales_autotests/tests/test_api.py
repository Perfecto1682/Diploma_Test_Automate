import requests
import allure
from ..config.settings import BASE_URL_API, API_KEY

# Feature: Получение данных о рейсах — Позитивный тест
@allure.feature("API Tests")
@allure.story("Получение данных о рейсах — Позитивный тест")
def test_api_get_flights():
    params = {"origin": "MOW", "destination": "LED"}
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(f"{BASE_URL_API}/v1/search", params=params, headers=headers)  # Убедитесь, что используете правильную конечную точку
    assert response.status_code == 200, f"API вернул ошибку: {response.status_code}"
    assert "data" in response.json(), "Ответ не содержит данных о рейсах"

# Негативный тест
@allure.story("Получение данных о рейсах — Негативный тест")
def test_api_invalid_request():
    params = {"origin": "XXX", "destination": "YYY"}
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(f"{BASE_URL_API}/v1/search", params=params, headers=headers)  # Правильная конечная точка
    assert response.status_code == 200, f"API вернул ошибку: {response.status_code}"
    assert len(response.json().get("data", [])) == 0, "Рейсы найдены, хотя не должны"

# Позитивный тест: Фильтрация по времени
@allure.story("Фильтрация рейсов по времени — Позитивный тест")
def test_api_filter_by_time():
    params = {"origin": "MOW", "destination": "LED", "departure_time": "morning"}
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(f"{BASE_URL_API}/v1/search", params=params, headers=headers)  # Правильная конечная точка
    assert response.status_code == 200, f"API вернул ошибку: {response.status_code}"
    flights = response.json().get("data", [])
    assert all(flight["departure_time"] == "morning" for flight in flights), "Фильтр по времени не сработал"

# Негативный тест: Пустые параметры
@allure.story("Проверка с пустыми параметрами — Негативный тест")
def test_api_empty_params():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(f"{BASE_URL_API}/v1/search", params={}, headers=headers)  # Правильная конечная точка
    assert response.status_code == 400, f"API не вернул ошибку на пустые параметры: {response.status_code}"

# Сложный запрос: рейсы с пересадками
@allure.story("Сложный запрос: рейсы с пересадками — Позитивный тест")
def test_api_complex_request_with_transfers():
    params = {"origin": "MOW", "destination": "LED", "transfers": "1"}
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(f"{BASE_URL_API}/v1/search", params=params, headers=headers)  # Правильная конечная точка
    assert response.status_code == 200, f"API вернул ошибку: {response.status_code}"
    flights = response.json().get("data", [])
    assert all(flight.get("transfers") == 1 for flight in flights), "Фильтр по пересадкам не работает"
