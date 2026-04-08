import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import requests
import re

def obtener_proxy_real():
    print("[*] Buscando IP válida...")
    fuente = "https://proxyscrape.com"
    try:
        r = requests.get(fuente, timeout=10)
        # Usamos una expresión regular para extraer solo IPs reales (formato 0.0.0.0:0000)
        ips = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)
        if ips:
            seleccionada = random.choice(ips)
            print(f"[!] IP encontrada y validada: {seleccionada}")
            return seleccionada
    except:
        pass
    print("[?] No se encontró proxy limpio, usando IP directa.")
    return None

def procesar_capa(driver):
    wait = WebDriverWait(driver, 25)
    try:
        url_actual = driver.current_url
        print(f"[*] URL: {url_actual}")

        if "hotmart.com" in url_actual:
            print("[!!!] ¡EXITO TOTAL EN HOTMART!")
            return "FIN"

        # Etapa 1: Captcha Invisible
        if driver.find_elements(By.ID, "form-captcha"):
            print("[...] Etapa 1. Esperando 15s...")
            time.sleep(15)
            driver.execute_script("document.getElementById('form-captcha').submit();")
            return "SIGUE"

        # Etapa 2: Botón Get Link
        elif driver.find_elements(By.ID, "btn-main"):
            print("[...] Etapa 2. Esperando 10s...")
            time.sleep(10)
            boton = wait.until(EC.element_to_be_clickable((By.ID, "btn-main")))
            driver.execute_script("arguments.click();", boton)
            return "SIGUE"
        
        else:
            print("[-] Sin botones. Reintentando...")
            driver.refresh()
            time.sleep(8)
            return "SIGUE"
    except Exception as e:
        print(f"[-] Error en capa: {e}")
        return "ERROR"

if __name__ == "__main__":
    proxy = obtener_proxy_real()
    
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')

    # Iniciar navegador con manejo de errores
    try:
        driver = uc.Chrome(options=options, version_main=146)
    except:
        # Si falla con proxy, iniciamos sin él
        driver = uc.Chrome(options=options.remove_argument(f'--proxy-server={proxy}') if proxy else options, version_main=146)

    try:
        with open("links.txt", "r") as f:
            enlaces = [l.strip() for l in f if l.strip()]
        
        for link in enlaces:
            print(f"\n--- Iniciando: {link} ---")
            driver.get(link)
            for _ in range(12): # Para las 5 capas
                status = procesar_capa(driver)
                if status == "FIN": break
                time.sleep(5)
    finally:
        driver.quit()
