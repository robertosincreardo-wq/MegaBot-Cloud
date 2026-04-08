import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def saltar_acortador(driver):
    wait = WebDriverWait(driver, 25)
    
    for i in range(5):
        url_actual = driver.current_url
        print(f"[*] Capa {i+1} - URL actual: {url_actual}")

        if "youtube.com" in url_actual or "youtu.be" in url_actual:
            print("[!!!] ¡ÉXITO! Llegamos al video de YouTube.")
            return True

        try:
            # LÓGICA PARA OUO
            if "ouo.io" in url_actual or "ouo.press" in url_actual:
                print("[>] Detectado Ouo.io - Buscando botón...")
                time.sleep(random.randint(5, 7))
                boton = wait.until(EC.element_to_be_clickable((By.ID, "btn-main")))
                boton.click()
                continue 

            # LÓGICA PARA SHINK
            elif "shink" in url_actual or "shrink" in url_actual:
                print("[>] Detectado Shink - Buscando botón...")
                time.sleep(random.randint(6, 8))
                boton = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#continue, .btn-primary, #invisibleCaptchaShortlink")))
                boton.click()
                continue

            else:
                print("[?] Sitio desconocido o redireccionando...")
                time.sleep(5)

        except Exception as e:
            print(f"[!] No se encontró botón: {url_actual}")
            break
    return False

if __name__ == "__main__":
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--blink-settings=imagesEnabled=false')
    
    # --- CAMBIO CRÍTICO: Forzamos la versión 146 ---
    try:
        driver = uc.Chrome(options=options, version_main=146)
    except Exception as e:
        print(f"[X] Error iniciando Chrome: {e}")
        exit(1)

    try:
        with open("links.txt", "r") as f:
            enlaces_principales = [line.strip() for line in f if line.strip()]
    except:
        enlaces_principales = []

    for url in enlaces_principales:
        print(f"\n--- Iniciando cadena para: {url} ---")
        driver.get(url)
        saltar_acortador(driver)
        time.sleep(5)

    driver.quit()
