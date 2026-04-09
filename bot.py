import asyncio
from playwright.async_api import async_playwright
import random
import time
import os

# --- DATOS DE ROTACIÓN WEBSHARE (Tu cuenta) ---
WS_USER = "inrjymkc-rotate"
WS_PASS = "kyhwkgls9xnq"
WS_SERVER = "p.webshare.io:80" 
PROXY_URL = f"http://{WS_USER}:{WS_PASS}@{WS_SERVER}"

async def saltar_ouo(page, link_objetivo):
    print(f"[*] Navegando a: {link_objetivo}")
    try:
        # Cargamos el link (60 segundos de espera máximo)
        await page.goto(link_objetivo, wait_until="domcontentloaded", timeout=60000)
        
        for i in range(25):
            await asyncio.sleep(12) # Espera del contador de Ouo
            url_actual = page.url
            print(f"   [Paso {i+1}] URL: {url_actual[:50]}")

            # 1. ÉXITO: Si la URL ya no es de Ouo
            if "ouo" not in url_actual.lower() and "http" in url_actual:
                print(f"[!!!] DESTINO ALCANZADO: {url_actual}")
                return True

            # 2. TRUCO QUE TE FUNCIONÓ: Si cae en .press, volver atrás
            if "ouo.press" in url_actual:
                print("[!] Trampa detectada. Volviendo atrás...")
                await page.go_back()
                continue

            try:
                # 3. ACCIÓN: Clic en botón o Enviar formulario
                btn = await page.query_selector("#btn-main")
                if btn:
                    await page.evaluate("document.getElementById('btn-main').click();")
                    print("   [+] Clic en Get Link")
                    continue
                
                form = await page.query_selector("#form-captcha")
                if form:
                    await page.evaluate("document.getElementById('form-captcha').submit();")
                    print("   [+] Formulario enviado")
                    continue
            except:
                pass
    except Exception as e:
        print(f"[X] Error de carga con esta IP: {e}")
    return False

async def main():
    # Leer links.txt
    links = []
    if os.path.exists("links.txt"):
        with open("links.txt", "r") as f:
            links = [line.strip() for line in f if line.strip()]
    
    if not links:
        links = ["https://ouo.io"] # Link de respaldo

    async with async_playwright() as p:
        # Haremos 30 sesiones. En cada una, Webshare ROTARÁ la IP.
        for i in range(30):
            link_actual = random.choice(links)
            print(f"\n--- SESIÓN {i+1}/30 | Usando IP Rotativa ---")
            
            browser = None
            try:
                # Lanzamos navegador con el proxy de Webshare
                browser = await p.chromium.launch(
                    headless=True,
                    proxy={"server": PROXY_URL}
                )
                
                # Contexto con huella humana (Stealth)
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                )
                page = await context.new_page()

                # Ejecutamos el salto del link
                await saltar_ouo(page, link_actual)
                
            except Exception as e:
                print(f"[!] Fallo al iniciar sesión: {e}")
            finally:
                if browser:
                    await browser.close() # Cerramos para limpiar cookies y cambiar IP
            
            # Pausa breve entre sesiones
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())
