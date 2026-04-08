import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import requests
import re

def obtener_lista_proxies():
    print("[*] Descargando lista de proxies reales...")
    # Usamos fuentes directas de texto plano
    urls = [
        "https://githubusercontent.com",
        "https://proxyscrape.com"
    ]
    ips_finales = []
    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            ips = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)
            ips_finales.extend(ips)
        except:
            continue
    return list(set(ips_finales)) # Eliminar duplicados

def procesar_capa(driver):
    wait = WebDriverWait(driver, 25)
    try:
        url_actual = driver.current_url
        print(f"[*] URL: {url_actual}")

        if "hotmart.com" in url_actual:
            print("[!!!] ¡EXITO EN HOTMART!")
            return "FIN"

        # Etapa 1: Captcha Invisible
        if driver.find_elements(By.ID, "form-captcha"):
            print("[...] Etapa 1 detectada. Esperando 15s...")
            time.sleep(15)
            driver.execute_script("document.getElementById('form-captcha').submit();")
            return "SIGUE"

        # Etapa 2: Botón Get Link
        elif driver.find_elements(By.ID, "btn-main"):
            print("[...] Etapa 2 detectada. Esperando 10s...")
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
    lista_ips = obtener_lista_proxies()
    if not lista_ips:
        print("[X] No se pudieron descargar proxies. Abortando.")
        exit(1)
        
    random.shuffle(lista_ips)
    print(f"[+] Total de proxies listos: {len(lista_ips)}")

    with open("links.txt", "r") as f:
        enlaces = [l.strip() for l in f if l.strip()]

    for url in enlaces:
        exito = False
        intentos = 0
        while not exito and intentos < 10: # Intentamos con hasta 10 proxies
            proxy = lista_ips[intentos]
            print(f"\n--- Intento {intentos + 1} con Proxy: {proxy} ---")
            
            opts = uc.ChromeOptions()
            opts.add_argument('--headless')
            opts.add_argument('--no-sandbox')
            opts.add_argument(f'--proxy-server={proxy}')
            
            driver = None
            try:
                driver = uc.Chrome(options=opts, version_main=146)
                driver.set_page_load_timeout(35)
                driver.get(url)
                
                # Intentamos saltar hasta 12 capas (la cadena de 5 links)
                for _ in range(12):
                    status = procesar_capa(driver)
                    if status == "FIN":
                        exito = True
                        break
                    time.sleep(5)
                
                if exito: break
            except Exception as e:
                print(f"[!] Error de conexión con este proxy.")
            finally:
                if driver: 
                    try: driver.quit()
                    except: pass
                intentos += 1
