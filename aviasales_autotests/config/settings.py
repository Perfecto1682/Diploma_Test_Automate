import os
from dotenv import load_dotenv
import random


# Загружаем .env файл
load_dotenv()

# URL для UI и API
BASE_URL_UI = os.getenv("BASE_URL_UI", "https://www.aviasales.ru")
BASE_URL_API = os.getenv("BASE_URL_API", "https://api.travelpayouts.com/aviasales/")

# API Token для авторизации
API_KEY = os.getenv("API_KEY", "")

SEARCH_TERMS = {
    "valid_origin": ["Москва", "Санкт-Петербург", "Казань", "Новосибирск", "Екатеринбург"],
    "valid_destination": ["Петербург", "Москва", "Калуга", "Владивосток", "Краснодар"],
    "invalid_origin": ["НевалидныйГород", "НеправильныйГород", "НеСуществует", "ГородБезНазвания"],
    "invalid_destination": ["НевалидныйГород", "НеправильныйГород", "НеСуществует", "ГородБезНазвания"],
    "valid_date": ["2024-12-15", "2024-12-20", "2024-12-25", "2024-12-30", "2025-01-10"],
    "invalid_date": ["2024-02-30", "2024-13-01", "2024-00-10", "2024-02-31"],
}


# Функция для случайного выбора значений из словаря
def get_random_search_term(term_type):
    return random.choice(SEARCH_TERMS[term_type])
