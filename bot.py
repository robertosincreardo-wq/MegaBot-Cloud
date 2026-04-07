import undetected_chromedriver as uc
import time

def iniciar_bot():
    options = uc.ChromeOptions()
    options.add_argument('--headless') # En la nube tiene que ser headless
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = uc.Chrome(options=options)
    
    links = ["https://ouo.io", "https://ouo.io"]
    
    for link in links:
        print(f"Visitando: {link}")
        driver.get(link)
        time.sleep(10) # Esperar a que cargue
        # Aquí puedes añadir los clics automáticos
        
    driver.quit()

if __name__ == "__main__":
    iniciar_bot()
