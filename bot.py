import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def procesar_capa(driver):
    wait = WebDriverWait(driver, 25)
    url_actual = driver.current_url
    print(f"[*] URL Actual: {url_actual}")

    # SI LLEGAMOS A HOTMART, HEMOS TERMINADO LA CADENA
    if "hotmart.com" in url_actual:
        print("[!!!] ¡EXITO! Llegamos a la página final de Hotmart.")
        return "FIN"

    try:
        # CASO 1: ETAPA DE CAPTCHA (form-captcha)
        if driver.find_elements(By.ID, "form-captcha"):
            print("[...] Detectada Etapa 1 (Captcha). Esperando 15s...")
            time.sleep(15) # Tiempo para que Cloudflare se resuelva solo
            driver.execute_script("document.getElementById('form-captcha').submit();")
            print("[+] Formulario Captcha enviado.")
            return "CONTINUE"

        # CASO 2: ETAPA DE GET LINK (form-go / btn-main)
        elif driver.find_elements(By.ID, "btn-main"):
            print("[...] Detectada Etapa 2 (Contador). Esperando 10s...")
            time.sleep(10) # Esperar el contador de 5-10 segundos
            boton = wait.until(EC.element_to_be_clickable((By.ID, "btn-main")))
            driver.execute_script("arguments.click();", boton)
            print("[+] Botón Get Link pulsado.")
            return "CONTINUE"
        
        else:
            print("[?] No se detectaron elementos conocidos. Esperando redirección...")
            time.sleep(5)
            return "CONTINUE"

    except Exception as e:
        print(f"[-] Error en esta capa: {e}")
        return "ERROR"

if __name__ == "__main__":
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1')

    driver = uc.Chrome(options=options, version_main=146)

    with open("links.txt", "r") as f:
        links = [l.strip() for l in f if l.strip()]

    for link in links:
        print(f"\n--- Iniciando Cadena: {link} ---")
        driver.get(link)
        
        # Intentar saltar hasta 12 capas (porque dices que son 5 links encadenados)
        for i in range(12):
            resultado = procesar_capa(driver)
            if resultado == "FIN":
                break
            if resultado == "ERROR":
                # Si hay error, refrescamos por si se trabó
                driver.refresh()
                time.sleep(5)
            time.sleep(5) # Pausa entre capas

    driver.quit()
