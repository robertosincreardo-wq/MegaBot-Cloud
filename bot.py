import asyncio
import random
import os
from playwright.async_api import async_playwright

# Lista de perfiles para engañar a ouo.io (Safari, Chrome, Edge)
USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1", # Safari iPhone
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15",          # Safari Mac
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",    # Edge Windows
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"                             # Chrome Linux
]

async def ejecutar_sesion():
    if not os.path.exists('Webshare 10 proxies.txt') or not os.path.exists('links.txt'):
        print("[!] ERROR: Archivos .txt no encontrados")
        return

    with open('Webshare 10 proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]
    with open('links.txt', 'r') as f:
        enlaces = [line.strip() for line in f if line.strip()]

    async with async_playwright() as p:
        for url in enlaces:
            proxy_actual = random.choice(proxies)
            ua_actual = random.choice(USER_AGENTS) # Elegimos navegador al azar
            
            print(f"\n[*] NAVEGANDO A: {url}")
            print(f"[*] USANDO PROXY: {proxy_actual}")
            print(f"[*] EMULANDO: {ua_actual[:50]}...")

            # Lanzamos Chromium pero lo disfrazamos con el User Agent
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
            
            # Configuramos el contexto con el navegador elegido y el proxy
            context = await browser.new_context(
                user_agent=ua_actual,
                proxy={"server": f"http://{proxy_actual}"},
                viewport={'width': 1280, 'height': 720}
            )
            
            page = await context.new_page()

            try:
                # Timeout de 90s y carga inicial
                await page.goto(url, wait_until="commit", timeout=90000)
                
                # ESPERA DE 20 SEGUNDOS (Tu requerimiento)
                print(f"[+] Página abierta. Esperando 20 segundos para validar...")
                await asyncio.sleep(20)
                
                print(f"[SUCCESS] {url} completado.")

            except Exception as e:
                print(f"[!] Error: {str(e)[:50]}")
            
            finally:
                await context.close()
                await browser.close()

if __name__ == "__main__":
    asyncio.run(ejecutar_sesion())
