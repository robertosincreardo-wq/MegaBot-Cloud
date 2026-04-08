import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def saltar_acortador(driver):
    wait = WebDriverWait(driver, 20)
    
    for i in range(5):
        time.sleep(random.randint(5, 8)) # Espera aleatoria para engañar
        url_actual = driver.current_url
        print(f"[*] Capa {i+1} - URL actual: {url_actual}")

        if "youtube.com" in url_actual or "youtu.be" in url_actual:
            print("[!!!] ¡ÉXITO! Llegamos al video.")
            return True

        try:
            # LÓGICA PARA OUO (Busca el botón btn-main o cualquier botón que diga "I'm a human")
            if "ouo" in url_actual:
                print("[>] Intentando Ouo...")
                boton = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button, #btn-main")))
                driver.execute_script("arguments[0].click();", boton) # Clic por JS para saltar bloqueos
                continue

            # LÓGICA PARA SHINK / SHRINKME
            elif "shink" in url_actual or "shrink" in url_actual:
                print("[>] Intentando Shink/ShrinkMe...")
                # ShinkMe suele pedir un captcha antes de mostrar el botón. 
                # Intentamos buscar el botón de "Continue" por texto
                botones = driver.find_elements(By.TAG_NAME, "button")
                for b in botones:
                    if "Continue" in b.text or "Next" in b.text:
                        driver.execute_script("arguments[0].click();", b)
                        break
                continue

        except Exception as e:
            print(f"[!] No se pudo clicar. Probable CAPTCHA o Cloudflare bloqueando.")
            # Tomar captura de pantalla para depurar (opcional)
            driver.save_screenshot(f"error_capa_{i}.png")
            break
    return False

if __name__ == "__main__":
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # USER AGENT REAL: Esto es clave para que no te bloquee Cloudflare
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = uc.Chrome(options=options, version_main=146)

    try:
        with open("links.txt", "r") as f:
            enlaces = [line.strip() for line in f if line.strip()]
    except:
        enlaces = []

    for url in enlaces:
        print(f"\n--- Cadena: {url} ---")
        driver.get(url)
        saltar_acortador(driver)
    
    driver.quit()
