import asyncio
import random
import os
from playwright.async_api import async_playwright

async def ejecutar_sesion():
    # Cargar archivos
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

            browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
            context = await browser.new_context(proxy=proxy_config)
            page = await context.new_page()

            print(f"\n[*] PROCESANDO: {url} | PROXY: {ip}")

            try:
                await page.goto(url, wait_until="commit", timeout=60000)
                
                # Bucle para pasar las etapas del acortador
                pasos_completados = 0
                while pasos_completados < 2:
                    # 1. Detectar si caímos en /press y volver atrás
                    if "ouo.io/press" in page.url:
                        print("[!] Detectado ouo.io/press. Regresando...")
                        await page.go_back()
                        await asyncio.sleep(3)

                    # 2. Intentar clic en el botón actual (I'm a human o Get Link)
                    btn_selector = "button#btn-main"
                    if await page.is_visible(btn_selector):
                        print(f"[+] Botón detectado. Esperando 15s antes de clicar...")
                        await asyncio.sleep(15) # Espera solicitada
                        
                        await page.click(btn_selector)
                        print("[*] Clic realizado.")
                        pasos_completados += 1
                        await asyncio.sleep(5) # Espera post-clic para carga
                    else:
                        # Si no ve el botón, quizás ya terminó o hubo error
                        break
                
                print(f"[SUCCESS] Link finalizado.")

            except Exception as e:
                print(f"[!] Error: {str(e)[:50]}")
            finally:
                await browser.close()

if __name__ == "__main__":
    asyncio.run(ejecutar_sesion())
