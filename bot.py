import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def saltar_acortador(driver):
    wait = WebDriverWait(driver, 25)
    
    # Bucle para intentar saltar hasta 5 capas de acortadores
    for i in range(5):
        url_actual = driver.current_url
        print(f"[*] Capa {i+1} - URL actual: {url_actual}")

        # SI LLEGAMOS A YOUTUBE, TERMINAMOS
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
                continue # Revisa la siguiente URL tras el clic

            # LÓGICA PARA SHINK (Shrink.me / Shink.in / Shink.me)
            elif "shink" in url_actual or "shrink" in url_actual:
                print("[>] Detectado Shink - Buscando botón...")
                time.sleep(random.randint(6, 8))
                # Shink suele usar clases como 'btn-primary' o IDs específicos
                # Intentamos encontrar el botón de "Continue" o "Get Link"
                boton = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#continue, .btn-primary, #invisibleCaptchaShortlink")))
                boton.click()
                continue

            else:
                # Si no es ninguno, esperamos un poco por si hay redirección automática
                print("[?] Sitio desconocido o redireccionando...")
                time.sleep(5)
                if i == 4: print("[-] No se pudo identificar más botones.")

        except Exception as e:
            print(f"[!] No se encontró botón o requiere Captcha manual: {url_actual}")
            break
    return False

if __name__ == "__main__":
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--blink-settings=imagesEnabled=false') # Ahorra datos
    
    driver = uc.Chrome(options=options)

    # Cargar los 2 links principales de tu links.txt
    try:
        with open("links.txt", "r") as f:
            enlaces_principales = [line.strip() for line in f if line.strip()]
    except:
        print("[X] No se encontró links.txt")
        enlaces_principales = []

    for url in enlaces_principales:
        print(f"\n--- Iniciando cadena para: {url} ---")
        driver.get(url)
        saltar_acortador(driver)
        time.sleep(5)

    driver.quit()
    print("\n[FIN] Proceso terminado.")
