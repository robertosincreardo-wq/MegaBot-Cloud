import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import requests

def obtener_proxy():
    print("[*] Buscando IP para evadir bloqueo...")
    try:
        # Intentamos obtener un proxy HTTP/S que funcione
        r = requests.get("https://proxyscrape.com", timeout=5)
        return random.choice(r.text.splitlines())
    except:
        return None

def procesar_capa(driver):
    wait = WebDriverWait(driver, 25)
    url_actual = driver.current_url
    print(f"[*] URL Actual: {url_actual}")

    if "hotmart.com" in url_actual:
        print("[!!!] ¡EXITO! Llegamos a Hotmart.")
        return "FIN"

    try:
        # Detectar Formulario de Captcha
        if driver.find_elements(By.ID, "form-captcha"):
            print("[...] Etapa 1 detectada. Esperando carga...")
            time.sleep(12)
            driver.execute_script("document.getElementById('form-captcha').submit();")
            print("[+] Formulario enviado.")
            return "CONTINUE"

        # Detectar Botón Get Link
        elif driver.find_elements(By.ID, "btn-main"):
            print("[...] Etapa 2 detectada. Esperando contador...")
            time.sleep(10)
            boton = wait.until(EC.element_to_be_clickable((By.ID, "btn-main")))
            driver.execute_script("arguments.click();", boton)
            print("[+] Click en Get Link.")
            return "CONTINUE"
        
        else:
            # Si no hay nada, quizá la página no cargó por la IP
            print("[-] No se detectan botones. Reintentando carga...")
            driver.refresh()
            time.sleep(8)
            return "CONTINUE"

    except Exception as e:
        print(f"[-] Error: {e}")
        return "ERROR"

if __name__ == "__main__":
    # 1. Obtener un proxy antes de iniciar
    proxy = obtener_proxy()
    
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    if proxy:
        print(f"[!] Usando Proxy: {proxy}")
        options.add_argument(f'--proxy-server={proxy}')

    driver = uc.Chrome(options=options, version_main=146)

    try:
        with open("links.txt", "r") as f:
            links = [l.strip() for l in f if l.strip()]
        
        for link in links:
            print(f"\n--- Iniciando Cadena: {link} ---")
            driver.get(link)
            for i in range(12): # Soporta las 5 capas de la cadena
                res = procesar_capa(driver)
                if res == "FIN": break
                time.sleep(5)
    finally:
        driver.quit()
