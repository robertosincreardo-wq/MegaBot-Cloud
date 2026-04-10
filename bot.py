import time
import random
import os
import undetected_chromedriver as uc
from stem import Signal
from stem.control import Controller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIG ---
RUTA_EXT = os.path.abspath("./extension")
PROXY = "socks5://127.0.0.1:9050"

def cambiar_ip():
    try:
        with Controller.from_port(port=9051) as c:
            c.authenticate()
            c.signal(Signal.NEWNYM)
        print("[!] IP Rotada")
    except:
        print("[X] Tor no responde")

def procesar():
    # Parche para Python 3.14: Evitar que el deallocator rompa todo
    options = uc.ChromeOptions()
    options.add_argument(f'--proxy-server={PROXY}')
    options.add_argument(f'--load-extension={RUTA_EXT}')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = None
    try:
        # Forzamos la version 146 para que coincida con tu Chrome
        driver = uc.Chrome(options=options, version_main=146)
        driver.get("https://ouo.io") # Prueba con un link real
        
        print("[*] Navegador abierto. Esperando 10 seg...")
        time.sleep(10)
        
        # Aquí iría el resto de clics...
        
    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        if driver:
            try:
                driver.close()
                driver.quit()
            except:
                pass # Ignorar el error de controlador invalido de Python 3.14

if __name__ == "__main__":
    while True:
        cambiar_ip()
        procesar()
        time.sleep(5)
