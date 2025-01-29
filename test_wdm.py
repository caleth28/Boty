from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_selenium_wdm():
    # WebDriver Manager intentará descargar la versión de ChromeDriver
    # compatible con la versión de Chrome instalada en tu sistema
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get("https://www.google.com")
    time.sleep(5)  # Espera 5 segundos
    driver.quit()

if __name__ == "__main__":
    test_selenium_wdm()
