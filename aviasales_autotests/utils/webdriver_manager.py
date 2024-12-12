from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')  # Отключаем использование GPU
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver
