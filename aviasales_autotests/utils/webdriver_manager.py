from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Открытие браузера в развернутом виде
    options.add_argument("--headless")  # Режим без графического интерфейса
    options.add_argument('--ignore-certificate-errors')  # Игнорирование ошибок сертификатов
    options.add_argument('--ignore-ssl-errors')  # Игнорирование ошибок SSL
    options.add_argument('--disable-gpu')  # Отключение GPU
    options.add_argument('--disable-software-rasterizer')  # Отключение софтверного рендеринга
    options.add_argument('--disable-webrtc')  # Отключение WebRTC
    options.add_argument('--disable-features=PageLoadMetrics')  # Отключение метрик загрузки страницы
    options.add_argument('--log-level=3')  # Уменьшение уровня логов браузера

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver
