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

            # Lanzamos con camuflaje extra
            browser = await p.chromium.launch(headless=True, args=[
                '--no-sandbox', 
                '--disable-blink-features=AutomationControlled',
                '--use-fake-ui-for-media-stream'
            ])
            
            context = await browser.new_context(
                proxy=proxy_config,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                viewport={'width': 1366, 'height': 768}
            )
            page = await context.new_page()

            print(f"\n[*] PROCESANDO: {url} | PROXY: {ip}")

            try:
                # 1. Carga inicial
                await page.goto(url, wait_until="networkidle", timeout=60000)
                
                # --- PASO 1: I'M HUMAN ---
                boton_1 = await page.wait_for_selector("button#btn-main", state="visible", timeout=35000)
                print("    [+] Etapa 1 detectada. Esperando 15s...")
                await asyncio.sleep(15)
                await boton_1.click(force=True)
                
                # --- PASO 2: GET LINK ---
                await asyncio.sleep(8)
                if "ouo.io/press" in page.url:
                    await page.go_back()
                    await asyncio.sleep(5)

                boton_2 = await page.wait_for_selector("button#btn-main", state="visible", timeout=35000)
                print("    [+] Etapa 2 (Get Link) detectada. Esperando 20s para asegurar vista...")
                # Esperamos 20s: 10 del contador + 10 de seguridad para el servidor
                await asyncio.sleep(20)
                
                await boton_2.click(force=True)
                print("    [*] Clic final realizado. Manteniendo conexión 10s más...")
                
                # ESPERA FINAL CRÍTICA para que el servidor registre el redireccionamiento
                await asyncio.sleep(10)
                print(f"[SUCCESS] Proceso completo para {url}")

            except Exception as e:
                titulo = await page.title()
                print(f"    [!] Fallo o Bloqueo. Título: {titulo}")
            finally:
                await browser.close()

if __name__ == "__main__":
    asyncio.run(ejecutar_sesion())
