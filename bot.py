import asyncio
from playwright.async_api import async_playwright
import random
import time
import os

# --- CONFIGURACIÓN DE WEBSHARE ROTATIVO ---
# Usa los datos que me pasaste antes. 
# El usuario con "-rotate" es la clave para que la IP cambie sola.
WS_PROXY = "http://webshare.io"
WS_USER = "inrjymkc-rotate"
WS_PASS = "kyhwkgls9xnq"
PROXY_URL = f"http://{WS_USER}:{WS_PASS}@p.webshare.io:80"

async def saltar_ouo(page, url_objetivo):
    try:
        # Cargamos el link
        await page.goto(url_objetivo, wait_until="domcontentloaded", timeout=40000)
        
        for i in range(20): # Máximo 20 pasos para no perder tiempo
            await asyncio.sleep(11) # Tiempo justo para el contador de Ouo
            url_actual = page.url
            print(f"      [Paso {i+1}] -> {url_actual[:45]}")

            # DETECCIÓN DE DESTINO (Si llegamos a Hotmart o YouTube o cualquier final)
            acortadores = ["ouo.io", "ouo.press", "shrink", "shink", "xreallcygo"]
            if not any(x in url_actual.lower() for x in acortadores):
                print(f"      [!!!] DESTINO ALCANZADO.")
                return True

            if "ouo.press" in url_actual:
                await page.go_back()
                continue

            # Clic o Submit rápido
            try:
                await page.evaluate("""
                    let b = document.getElementById('btn-main') || document.querySelector('button');
                    if(b) b.click();
                    let f = document.getElementById('form-captcha') || document.getElementById('form-go');
                    if(f) f.submit();
                """)
            except: pass
    except:
        print("      [!] Error en esta IP.")
    return False

async def main():
    # Cargar tus links
    if os.path.exists("links.txt"):
        with open("links.txt", "r") as f:
            links = [l.strip() for l in f if l.strip()]
    else:
        print("[X] No hay links.txt"); return

    async with async_playwright() as p:
        # VAMOS A HACER 40 SESIONES POR CADA EJECUCIÓN
        # Cada sesión forzará a Webshare a darnos una IP distinta
        for i in range(40):
            link_elegido = random.choice(links)
            print(f"\n[Sincronizando Sesión {i+1}/40] Obteniendo IP nueva...")
            
            browser = None
            try:
                # Al abrir el browser con el proxy rotativo, Webshare asigna IP nueva
                browser = await p.chromium.launch(headless=True, proxy={"server": PROXY_URL})
                
                # Variamos el User-Agent para que Ouo crea que son personas distintas
                user_agents = [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/123.0.0.0",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/122.0.0.0",
                    "Mozilla/5.0 (X11; Linux x86_64) Chrome/121.0.0.0"
                ]
                
                context = await browser.new_context(user_agent=random.choice(user_agents))
                page = await context.new_page()
                
                # Ejecutar el salto
                # Ponemos un tiempo límite de 3 minutos por IP para no estancarnos
                try:
                    await asyncio.wait_for(saltar_ouo(page, link_elegido), timeout=180)
                except asyncio.TimeoutError:
                    print("      [!] Sesión lenta, saltando a la siguiente IP...")

            except Exception as e:
                print(f"      [X] Fallo de conexión: {e}")
            finally:
                if browser:
                    await browser.close()
            
            # Pausa de 2 segundos para que Webshare procese el cambio de IP
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())
