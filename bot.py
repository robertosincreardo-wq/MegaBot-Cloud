import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def saltar_ouo(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 30)
        
        # --- ETAPA 1: El formulario de Cloudflare/Captcha ---
        print(f"[*] Etapa 1 - URL: {driver.current_url}")
        
        # Esperamos a que el widget de Cloudflare cargue (15-20 seg)
        print("[...] Esperando a que el captcha invisible se resuelva solo...")
        time.sleep(15) 
        
        try:
            # En la etapa 1, a veces no hay botón visible, hay que enviar el formulario
            # Buscamos el formulario con id 'form-captcha' que me pasaste
            print("[*] Intentando enviar formulario de etapa 1...")
            driver.execute_script("document.getElementById('form-captcha').submit();")
            print("[+] Formulario enviado.")
        except:
            # Si el submit falla, intentamos clic en cualquier botón del form
            driver.execute_script("document.querySelector('#form-captcha button, button').click();")

        # --- ETAPA 2: El contador y el Get Link ---
        time.sleep(10) # Tiempo para que cargue la redirección
        print(f"[*] Etapa 2 - URL: {driver.current_url}")
        
        # Esperamos los 5-10 segundos del contador que mencionaste
        print(f"[...] Esperando contador de 10 segundos...")
        time.sleep(10)
        
        try:
            # Buscamos el botón final que me pasaste: id="btn-main"
            boton_final = wait.until(EC.presence_of_element_located((By.ID, "btn-main")))
            driver.execute_script("arguments.scrollIntoView();", boton_final)
            time.sleep(2)
            driver.execute_script("arguments.click();", boton_final)
            print("[+ Success] ¡Botón Get Link pulsado!")
        except:
            print("[!] No se pudo pulsar el botón final. Probable bloqueo.")

        # Verificación final
        time.sleep(5)
        print(f"[*] URL Final: {driver.current_url}")
        if "youtube" in driver.current_url or "youtu.be" in driver.current_url:
            print("[!!!] ¡VISTA COMPLETADA CON EXITO!")

    except Exception as e:
        print(f"[-] Error durante el proceso: {e}")

if __name__ == "__main__":
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # User agent de iPhone para evitar captchas pesados
    options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1')

    # Iniciamos el navegador (Ubuntu en GitHub usa la versión 146 habitualmente)
    driver = uc.Chrome(options=options, version_main=146)

    try:
        with open("links.txt", "r") as f:
            links = [l.strip() for l in f if "ouo" in l]
    except:
        links = []

    for link in links:
        print(f"\n--- Iniciando Ouo: {link} ---")
        saltar_ouo(driver, link)
        time.sleep(5)

    driver.quit()
