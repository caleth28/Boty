import time
import os
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Credenciales de Envato
ENVATO_EMAIL = "diseno@peusac.com.pe"
ENVATO_PASSWORD = "Motivate28@"

def get_envato_link(item_url: str) -> str:
    """
    Descarga el recurso de Envato Elements en modo headless.
    """

    # Configurar la carpeta de descargas
    download_dir = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Configurar opciones de Chrome en modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Modo headless
    chrome_options.add_argument("--disable-gpu")  # Desactivar GPU
    chrome_options.add_argument("--no-sandbox")  # Desactivar sandbox
    chrome_options.add_argument("--disable-dev-shm-usage")  # Evitar problemas de memoria
    chrome_options.add_argument("--window-size=1920,1080")  # Simular pantalla completa
    chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})
    
    # Preferencias de descarga
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    # Configurar Selenium con WebDriver Manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # 1) Ir a la homepage de Envato
        driver.get("https://elements.envato.com/")
        time.sleep(5)

        # 2) **Abrir el menú si el botón de inicio de sesión no está visible**
        try:
            sign_in = driver.find_element(By.CSS_SELECTOR, "a[data-testid='header-sign-in']")
        except:
            # Si no encuentra el botón de "Iniciar sesión", intenta abrir el menú
            try:
                menu_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='toggle-navigation-drawer']")
                menu_button.click()
                time.sleep(2)
                sign_in = driver.find_element(By.CSS_SELECTOR, "a[data-testid='header-sign-in']")
            except:
                return "No se pudo encontrar el botón de 'Iniciar sesión'."

        sign_in.click()
        time.sleep(3)

        # 3) **Ingresar credenciales**
        email_input = driver.find_element(By.ID, "username")
        email_input.send_keys(ENVATO_EMAIL)
        time.sleep(1)

        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys(ENVATO_PASSWORD)
        password_input.send_keys(Keys.ENTER)
        time.sleep(8)

        # 4) **Ir al ítem**
        driver.get(item_url)
        time.sleep(5)

        # 5) **Botón "Download"**
        try:
            download_btn = driver.find_element(By.CSS_SELECTOR, "button[data-testid='button-download']")
            download_btn.click()
            time.sleep(3)
        except Exception as e:
            return f"ERROR: No encontré el botón Download en {item_url} - {e}"

        # 6) **Seleccionar la opción "Bot"**
        try:
            bot_radio = driver.find_element(By.XPATH, "//input[@type='radio' and @value='Bot']")
            bot_radio.click()
            time.sleep(2)
        except:
            return "No encontré la opción 'Bot' en el modal de proyectos."

        # 7) **Botón "Añadir y descargar"**
        try:
            add_download_btn = driver.find_element(By.CSS_SELECTOR, "button[data-testid='add-download-button']")
            add_download_btn.click()
            time.sleep(5)
        except:
            return "No encontré el botón 'Añadir y descargar'."

        # 8) **Esperar hasta que la descarga se complete**
        download_complete = False
        start_time = time.time()
        while not download_complete:
            time.sleep(1)
            files = os.listdir(download_dir)
            if any(file.endswith(".crdownload") for file in files):
                continue  # Archivo aún en progreso
            elif len(files) > 0:
                download_complete = True
            if time.time() - start_time > 120:
                return "Descarga no se completó en el tiempo esperado."

        # 9) **Retornar enlace si está disponible**
        all_links = driver.find_elements(By.TAG_NAME, "a")
        final_link = None
        for link in all_links:
            href = link.get_attribute("href")
            if href and "envatousercontent.com" in href:
                final_link = href
                break

        if final_link:
            return final_link
        else:
            return f"Descarga completada. Revisa la carpeta: {download_dir}"
    
    finally:
        driver.quit()

# **Para probar localmente**
if __name__ == "__main__":
    test_url = "https://elements.envato.com/es/text-animation-toolkit-D8HAYMX"
    link = get_envato_link(test_url)
    print("Link obtenido:", link)
