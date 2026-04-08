import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import requests

def obtener_proxy():
    print("[*] Buscando proxy vivo...")
    try:
        # Obtenemos una lista de proxies gratuitos
        r = requests.get("https://proxyscrape.com")
        if r.status_code == 200:
            lista = r.text.splitlines()
            return random.choice(lista)
    except:
        return None
    return None

def saltar_acortador(driver):
    wait = WebDriverWait(driver, 25)
    for i in range(5):
        time.sleep(random.randint(8, 12))
        url_actual = driver.current_url
        print(f"[*] Capa {i+1} - URL: {url_actual}")

        if "youtube.com" in url_actual or "youtu.be" in url_actual:
            print("[!!!] ¡EXITO! Llegamos al video.")
            return True

        try:
            # Intentamos clic por todos los medios (ID, Clase, Texto)
            boton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button#btn-main, .btn-primary, button")))
            driver.execute_script("arguments[0].scrollIntoView();", boton)
            time.sleep(2)
            driver.execute_script("arguments[0].click();", boton)
            print(f"[+] Clic ejecutado en Capa {i+1}")
        except:
            print("[X] Botón no interactuable.")
            break
    return False

if __name__ == "__main__":
    proxy = obtener_proxy()
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    if proxy:
        print(f"[!] Usando Proxy: {proxy}")
        options.add_argument(f'--proxy-server={proxy}')

    # Intentamos abrir el navegador
    try:
        driver = uc.Chrome(options=options, version_main=146)
        # Ocultar que es un bot
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    except Exception as e:
        print(f"Error Chrome: {e}")
        exit(1)

    with open("links.txt", "r") as f:
        enlaces = [l.strip() for l in f if l.strip()]

    for url in enlaces:
        print(f"\n--- Iniciando: {url} ---")
        try:
            driver.get(url)
            saltar_acortador(driver)
        except:
            print("[-] Error cargando la URL")
    
    driver.quit()
