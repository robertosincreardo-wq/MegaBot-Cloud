import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import requests

def obtener_proxy_valido():
    print("[*] Buscando IP residencial gratuita...")
    # Usamos una fuente de SOCKS5 que suelen ser más limpios
    fuentes = [
        "https://proxyscrape.com",
        "https://proxy-list.download"
    ]
    try:
        r = requests.get(random.choice(fuentes), timeout=10)
        proxies = [p.strip() for p in r.text.splitlines() if "." in p]
        return random.choice(proxies)
    except:
        return None

def saltar_acortador(driver, url_inicial):
    wait = WebDriverWait(driver, 25)
    for i in range(7): # Subimos a 7 capas por si hay redirecciones largas
        time.sleep(random.randint(10, 15))
        url_actual = driver.current_url
        print(f"[*] Capa {i+1} - URL: {url_actual}")

        if "youtube.com" in url_actual or "youtu.be" in url_actual:
            print("[!!!] ¡EXITO TOTAL! Llegamos a YouTube.")
            return True

        # Si después de 2 clics la URL sigue siendo la misma, el proxy está quemado
        if i >= 2 and url_actual == url_inicial:
            print("[X] Bucle detectado (IP Bloqueada). Abortando este intento.")
            return False

        try:
            # Buscamos el botón de forma más agresiva
            boton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button#btn-main, .btn-primary, button[type='submit'], #invisibleCaptchaShortlink")))
            driver.execute_script("arguments.scrollIntoView();", boton)
            time.sleep(2)
            driver.execute_script("arguments.click();", boton)
            print(f"[+] Clic enviado.")
        except:
            print("[?] Intentando clic forzado en cualquier botón disponible...")
            driver.execute_script("document.querySelector('button').click();")

    return False

if __name__ == "__main__":
    with open("links.txt", "r") as f:
        enlaces = [l.strip() for l in f if l.strip()]

    for url in enlaces:
        print(f"\n--- Iniciando Cadena: {url} ---")
        proxy = obtener_proxy_valido()
        
        options = uc.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        if proxy:
            print(f"[!] Usando Proxy SOCKS5: {proxy}")
            options.add_argument(f'--proxy-server=socks5://{proxy}')

        try:
            driver = uc.Chrome(options=options, version_main=146)
            driver.get(url)
            saltar_acortador(driver, url)
        except Exception as e:
            print(f"[-] Error de conexión: {e}")
        finally:
            try: driver.quit()
            except: pass
