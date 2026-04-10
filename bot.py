import asyncio
import random
import os
from playwright.async_api import async_playwright

async def ejecutar_sesion():
    if not os.path.exists('Webshare 10 proxies.txt') or not os.path.exists('links.txt'):
        print("[!] Faltan archivos .txt")
        return

    with open('Webshare 10 proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]
    with open('links.txt', 'r') as f:
        enlaces = [line.strip() for line in f if line.strip()]

    async with async_playwright() as p:
        for url in enlaces:
            proxy_line = random.choice(proxies)
            try:
                ip, puerto, user, password = proxy_line.split(':')
                proxy_config = {"server": f"http://{ip}:{puerto}", "username": user, "password": password}
            except: continue

            # Usamos un User Agent real de Chrome para evitar sospechas
            ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
            
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
            context = await browser.new_context(proxy=proxy_config, user_agent=ua)
            page = await context.new_page()

            print(f"\n[*] PROCESANDO: {url} | PROXY: {ip}")

            try:
                # 1. Carga inicial
                await page.goto(url, wait_until="networkidle", timeout=60000)
                
                # Intentamos hasta 3 pasos (a veces hay publicidad intermedia)
                for paso in range(1, 4):
                    if "ouo.io/press" in page.url:
                        print(f"    [!] Error en /press. Regresando...")
                        await page.go_back()
                        await asyncio.sleep(5)

                    # Buscamos el botón btn-main
                    btn = page.locator("button#btn-main")
                    
                    if await btn.is_visible():
                        print(f"    [+] Paso {paso}: Botón detectado. Esperando 15s para que el token sea válido...")
                        await asyncio.sleep(15) # Tiempo vital para que el script de ouo cargue
                        
                        # Clic real simulando humano
                        await btn.click()
                        print(f"    [*] Clic realizado en Paso {paso}. Esperando respuesta del servidor...")
                        
                        # ESPERA POST-CLIC: Vital para que la vista cuente
                        await asyncio.sleep(10) 
                    else:
                        print(f"    [-] No se ve más botones en paso {paso}. Finalizando.")
                        break

                print(f"[SUCCESS] Proceso terminado para {url}")

            except Exception as e:
                print(f"[!] Error: {str(e)[:50]}")
            finally:
                # Espera final antes de destruir el contexto
                await asyncio.sleep(2)
                await browser.close()

if __name__ == "__main__":
    asyncio.run(ejecutar_sesion())
