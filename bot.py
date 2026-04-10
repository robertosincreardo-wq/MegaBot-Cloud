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

            # Usamos Chromium con argumentos para evitar detección
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-web-security'])
            context = await browser.new_context(proxy=proxy_config, viewport={'width': 1280, 'height': 720})
            page = await context.new_page()

            print(f"\n[*] INICIANDO: {url} | PROXY: {ip}")

            try:
                # Carga inicial
                await page.goto(url, wait_until="domcontentloaded", timeout=90000)
                
                # --- PASO 1: I'M HUMAN ---
                print("    [*] Esperando botón 'I'm a human'...")
                try:
                    # Espera hasta 30 segundos a que el botón aparezca en el HTML
                    boton = await page.wait_for_selector("button#btn-main", state="visible", timeout=30000)
                    print("    [+] Botón detectado. Esperando 15s de seguridad...")
                    await asyncio.sleep(15)
                    
                    await boton.hover() # Simular movimiento
                    await boton.click(force=True)
                    print("    [OK] Clic en 'I'm a human' realizado.")
                except:
                    print("    [!] No se pudo dar clic en el Paso 1 (Captcha no cargó).")
                    await browser.close()
                    continue

                # --- PASO 2: GET LINK (Contador de 10s) ---
                await asyncio.sleep(5) # Espera a que cargue la segunda página
                print("    [*] Esperando contador de 'Get Link' (Etapa 2)...")
                try:
                    # Esperamos a que el botón de Get Link aparezca
                    boton_get = await page.wait_for_selector("button#btn-main", state="visible", timeout=30000)
                    
                    # Esperamos 15 segundos (10 del contador + 5 de margen)
                    print("    [+] Segundo botón detectado. Esperando 15s para que el contador llegue a cero...")
                    await asyncio.sleep(15)
                    
                    await boton_get.hover()
                    await boton_get.click(force=True)
                    print("    [OK] Clic en 'Get Link' realizado.")
                    
                    # MUY IMPORTANTE: Esperar 10s adicionales después del último clic para que el servidor registre la IP
                    await asyncio.sleep(10)
                    print(f"[SUCCESS] Vista completada para: {url}")
                except:
                    print("    [!] Error en el Paso 2 (Get Link no apareció).")

            except Exception as e:
                print(f"[!] Error de conexión: {str(e)[:50]}")
            finally:
                await browser.close()

if __name__ == "__main__":
    asyncio.run(ejecutar_sesion())
