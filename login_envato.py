import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ------------------------------------------------------------------------------
# Ajusta tus credenciales (correo y contraseña) y la URL del recurso:
# ------------------------------------------------------------------------------
ENVATO_EMAIL = "diseno@peusac.com.pe"
ENVATO_PASSWORD = "Motivate28@"
ITEM_URL = "https://elements.envato.com/es/text-animation-toolkit-D8HAYMX"
# ------------------------------------------------------------------------------


def login_and_download():
    # 1) Inicia WebDriver con webdriver_manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # 2) Abre Envato Elements
    driver.get("https://elements.envato.com/")
    time.sleep(3)

    # 3) Buscar "Sign In" o "Iniciar sesión" (según tu idioma)
    try:
        sign_in_button = driver.find_element(By.LINK_TEXT, "Sign In")
    except:
        sign_in_button = driver.find_element(By.LINK_TEXT, "Iniciar sesión")
    sign_in_button.click()
    time.sleep(3)

    # 4) Escribe el correo
    email_input = driver.find_element(By.ID, "username")
    email_input.send_keys(ENVATO_EMAIL)
    time.sleep(1)

    # 5) Escribe la contraseña
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(ENVATO_PASSWORD)
    password_input.send_keys(Keys.ENTER)
    time.sleep(8)  # Esperamos un rato para que cargue el dashboard

    # 6) Ir al ítem que deseamos descargar
    driver.get(ITEM_URL)
    time.sleep(5)

    # 7) Clic en el botón de descarga (data-testid='button-download')
    try:
        download_btn = driver.find_element(By.CSS_SELECTOR, "button[data-testid='button-download']")
        download_btn.click()
        time.sleep(3)
    except Exception as e:
        print("ERROR: No se encontró el botón con data-testid='button-download':", e)
        driver.quit()
        return

    # 8) En el modal “Añadir a proyecto”, seleccionamos la opción "Bot"
    #    (la que tiene <input ... value="Bot">).
    try:
        bot_radio = driver.find_element(By.XPATH, "//input[@type='radio' and @value='Bot']")
        bot_radio.click()
        time.sleep(2)
    except Exception as e:
        print("No encontré la opción 'Bot' en el modal:", e)
        driver.quit()
        return

    # 9) Clic en “Añadir y descargar” (data-testid="add-download-button")
    try:
        add_and_download_btn = driver.find_element(By.CSS_SELECTOR, "button[data-testid='add-download-button']")
        add_and_download_btn.click()
        time.sleep(5)
    except Exception as e:
        print("No encontré el botón 'Añadir y descargar':", e)
        driver.quit()
        return

    # 10) Opcional: buscar si hay un enlace "envatousercontent.com"
    all_links = driver.find_elements(By.TAG_NAME, "a")
    final_link = None
    for link in all_links:
        href = link.get_attribute("href")
        if href and "envatousercontent.com" in href:
            final_link = href
            break

    if final_link:
        print("Enlace de descarga encontrado:", final_link)
    else:
        print("No se encontró un enlace con 'envatousercontent.com'. "
              "Es posible que la descarga se haya iniciado directamente.")

    # 11) Cerrar navegador
    driver.quit()
    print("Proceso terminado con éxito.")


if __name__ == "__main__":
    login_and_download()
