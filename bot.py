import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import requests
import re

def obtener_lista_proxies():
    print("[*] Descargando lista de proxies frescos...")
    url = "https://proxyscrape.com"
    try:
        r = requests.get(url, timeout=15)
        ips = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)
        return ips
    except:
        return []

def procesar_capa(driver):
    wait = WebDriverWait(driver, 25)
    try:
        url_actual = driver.current_url
        print(f"[*] URL: {url_actual}")

        if "hotmart.com" in url_actual:
            print("[!!!] EXITOSO EN HOTMART")
            return "FIN"

        # Etapa 1: Captcha Invisible (form-captcha)
        if driver.find_elements(By.ID, "form-captcha"):
            print("[...] Etapa 1 detectada. Esperando 15s...")
            time.sleep(15)
            driver.execute_script("document.getElementById('form-captcha').submit();")
            return "SIGUE"

        # Etapa 2: Botón Get Link (btn-main)
        elif driver.find_elements(By.ID, "btn-main"):
            print("[...] Etapa 2 detectada. Esperando 10s...")
            time.sleep(10)
            boton = wait.until(EC.element_to_be_clickable((By.ID, "btn-main")))
            driver.execute_script("arguments.click();", boton)
            return "SIGUE"
        
        else:
            print("[-] No se ven botones. Reintentando...")
            driver.refresh()
            time.sleep(8)
            return "SIGUE"
    except Exception as e:
        print(f"[-] Error en capa: {e}")
        return "ERROR"

if __name__ == "__main__":
    lista_ips = obtener_lista_proxies()
    random.shuffle(lista_ips) # Mezclamos para no usar siempre los mismos

    with open("links.txt", "r") as f:
        enlaces = [l.strip() for l in f if l.strip()]

    for url in enlaces:
        exito = False
        intentos_proxy = 0
        
        # Intentamos con hasta 5 proxies diferentes por cada link
        while not exito and intentos_proxy < 5:
            proxy = lista_ips[intentos_proxy] if intentos_proxy < len(lista_ips) else None
            print(f"\n--- Intento {intentos_proxy + 1} con Proxy: {proxy} ---")
            
            opts = uc.ChromeOptions()
            opts.add_argument('--headless')
            opts.add_argument('--no-sandbox')
            if proxy: opts.add_argument(f'--proxy-server={proxy}')
            
            driver = None
            try:
                driver = uc.Chrome(options=opts, version_main=146)
                driver.set_page_load_timeout(30)
                driver.get(url)
                
                for _ in range(12):
                    status = procesar_capa(driver)
                    if status == "FIN": 
                        exito = True
                        break
                    time.sleep(5)
                
                if exito: break
            except Exception as e:
                print(f"[!] Error con este proxy: {e}")
            finally:
                if driver: driver.quit()
                intentos_proxy += 1
