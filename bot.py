import asyncio
import random
import os
from playwright.async_api import async_playwright

async def ejecutar_sesion():
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

            # Lanzamos con argumentos para ocultar la automatización
            browser = await p.chromium.launch(headless=True, args=[
                '--no-sandbox', 
                '--disable-blink-features=AutomationControlled'
            ])
            
            # Simulamos un navegador Windows real con lenguaje español
            context = await browser.new_context(
                proxy=proxy_config,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                locale="es-ES",
                extra_http_headers={"Referer": "https://google.com"}
            )
            page = await context.new_page()

            print(f"\n[*] PROBANDO: {url} | PROXY: {ip}")

            try:
                # Navegar y esperar a que el contenido básico cargue
                response = await page.goto(url, wait_until="domcontentloaded", timeout=60000)
                
                if response.status >= 400:
                    print(f"    [!] Error HTTP {response.status}. Proxy posiblemente bloqueado.")
                
                # --- PASO 1: ESPERA AGRESIVA POR EL BOTÓN ---
                try:
                    # Esperamos hasta 40 segundos. Si no aparece, es bloqueo total.
                    boton = await page.wait_for_selector("button#btn-main", state="visible", timeout=40000)
                    print("    [+] Botón I'm Human detectado. Esperando 15s...")
                    await asyncio.sleep(15)
                    await boton.click(force=True)
                    
                    # --- PASO 2: GET LINK ---
                    await asyncio.sleep(5)
                    boton_get = await page.wait_for_selector("button#btn-main", state="visible", timeout=30000)
                    print("    [+] Botón Get Link detectado. Esperando 15s...")
                    await asyncio.sleep(15)
                    await boton_get.click(force=True)
                    
                    await asyncio.sleep(10) # Tiempo para que cuente la vista
                    print(f"[SUCCESS] ¡Vista completada!")
                except:
                    print(f"    [!] Bloqueo detectado. Título de página: {await page.title()}")

            except Exception as e:
                print(f"    [!] Error de red: {str(e)[:40]}")
            finally:
                await browser.close()

if __name__ == "__main__":
    asyncio.run(ejecutar_sesion())
