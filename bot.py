import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

def saltar_acortador(driver):
    wait = WebDriverWait(driver, 20)
    
    for i in range(5):
        time.sleep(random.randint(7, 10)) # Más tiempo para que carguen los scripts
        url_actual = driver.current_url
        print(f"[*] Capa {i+1} - URL actual: {url_actual}")

        if "youtube.com" in url_actual or "youtu.be" in url_actual:
            print("[!!!] ¡EXITO! Llegamos al destino.")
            return True

        try:
            # LIMPIEZA DE COOKIES EN CADA CAPA PARA EVITAR RASTREO
            driver.delete_all_cookies()

            if "ouo" in url_actual:
                print("[>] Intentando Ouo...")
                # Ouo a veces cambia el ID. Buscamos el botón principal por CSS
                boton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button#btn-main, .btn-main, button")))
                # MOVER EL MOUSE AL BOTÓN ANTES DE CLICKEAR (Humaniza el bot)
                action = ActionChains(driver)
                action.move_to_element(boton).pause(1).click().perform()
                continue

            elif "shrink" in url_actual or "shink" in url_actual:
                print("[>] Intentando Shink/ShrinkMe...")
                # ShinkMe es sensible. Intentamos encontrar el botón por XPATH que diga "Continue"
                boton = wait.until(EC.element_to_be_clickable((By.XPATH, "//button | //a")))
                driver.execute_script("arguments[0].scrollIntoView();", boton)
                time.sleep(2)
                boton.click()
                continue

        except Exception:
            # Si falla el clic normal, intentamos un clic forzado por JS
            try:
                driver.execute_script("document.querySelector('button').click();")
                print("[!] Clic forzado por JS ejecutado.")
            except:
                print("[X] No se pudo interactuar con la página.")
                break
    return False

if __name__ == "__main__":
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # User Agent de una versión de Chrome muy común
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
    
    # IMPORTANTE: Desactivar la detección de automatización
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = uc.Chrome(options=options, version_main=146)

    with open("links.txt", "r") as f:
        enlaces = [l.strip() for l in f if l.strip()]

    for url in enlaces:
        print(f"\n--- Iniciando: {url} ---")
        driver.get(url)
        # Inyectar script para ocultar que es un bot
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        saltar_acortador(driver)
    
    driver.quit()
