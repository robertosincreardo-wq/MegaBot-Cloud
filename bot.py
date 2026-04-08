import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import requests

def obtener_proxy():
    print("[*] Buscando IP...")
    try:
        r = requests.get("https://proxyscrape.com", timeout=5)
        return random.choice(r.text.splitlines())
    except:
        return None

def saltar(driver):
    wait = WebDriverWait(driver, 15)
    for i in range(5):
        time.sleep(10) # Tiempo para que cargue la publicidad
        print(f"[*] Capa {i+1} - URL: {driver.current_url}")

        if "youtube.com" in driver.current_url:
            print("[!!!] ¡EXITO!")
            return True

        # Verificar si hay CAPTCHA bloqueando
        if "captcha" in driver.page_source.lower():
            print("[X] Captcha detectado. IP bloqueada.")
            return False

        try:
            # BUSQUEDA MULTIPLE DE BOTONES (Ouo y Shink)
            selectores = [
                "button#btn-main", ".btn-primary", "button[type='submit']", 
                "a.btn", "button", "#invisibleCaptchaShortlink"
            ]
            
            encontrado = False
            for selector in selectores:
                try:
                    boton = driver.find_element(By.CSS_SELECTOR, selector)
                    if boton.is_displayed():
                        driver.execute_script("arguments[0].click();", boton)
                        print(f"[+] Clic en {selector}")
                        encontrado = True
                        break
                except:
                    continue
            
            if not encontrado:
                print("[-] No se hallaron botones de salto.")
                break

        except Exception as e:
            print(f"[-] Error: {e}")
            break
    return False

if __name__ == "__main__":
    with open("links.txt", "r") as f:
        links = [l.strip() for l in f if l.strip()]

    for url in links:
        print(f"\n--- Link: {url} ---")
        proxy = obtener_proxy()
        opts = uc.ChromeOptions()
        opts.add_argument('--headless')
        opts.add_argument('--no-sandbox')
        if proxy:
            print(f"[!] Usando Proxy: {proxy}")
            opts.add_argument(f'--proxy-server={proxy}')

        try:
            driver = uc.Chrome(options=opts, version_main=146)
            driver.get(url)
            saltar(driver)
            driver.quit()
        except:
            print("[X] Error de carga")
            if 'driver' in locals(): driver.quit()
