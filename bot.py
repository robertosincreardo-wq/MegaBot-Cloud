import asyncio
import random
import os
from playwright.async_api import async_playwright

async def ejecutar_sesion():
    if not os.path.exists('Webshare 10 proxies.txt') or not os.path.exists('links.txt'):
        print("[!] Archivos no encontrados.")
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

            # Browser con resolución estándar
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
            context = await browser.new_context(
                proxy=proxy_config,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                viewport={'width': 1280, 'height': 720}
            )
            page = await context.new_page()

            print(f"\n[*] ENTRANDO A: {url} | PROXY: {ip}")

            try:
                # 1. Carga inicial con tiempo de espera forzado para scripts
                await page.goto(url, wait_until="load", timeout=90000)
                await asyncio.sleep(10) # Espera técnica inicial

                for paso in range(1, 4):
                    # Manejo de redirección basura
                    if "ouo.io/press" in page.url or "google.com" in page.url:
                        print("    [!] Redirección detectada. Volviendo...")
                        await page.go_back()
                        await asyncio.sleep(5)

                    # Esperar específicamente al botón btn-main
                    try:
                        # Forzamos a que espere a que el botón esté en el DOM y sea visible
                        btn = await page.wait_for_selector("button#btn-main", timeout=20000)
                        
                        if paso == 1:
                            print("    [+] Paso 1: I'm human. Esperando 15s...")
                            await asyncio.sleep(15)
                        else:
                            print(f"    [+] Paso {paso}: Contador Get Link. Esperando 12s...")
                            await asyncio.sleep(12) # Superamos los 10s del contador

                        # Scroll y clic forzado vía JS para asegurar impacto
                        await btn.scroll_into_view_if_needed()
                        await btn.click(force=True)
                        print(f"    [*] Clic paso {paso} realizado.")
                        await asyncio.sleep(8) # Espera para que el servidor procese el POST

                    except:
                        print(f"    [-] No se encontró botón en paso {paso}. URL actual: {page.url[:40]}")
                        break

                print(f"[SUCCESS] Ciclo terminado para {url}")

            except Exception as e:
                print(f"[!] Error crítico: {str(e)[:50]}")
            finally:
                await browser.close()

if __name__ == "__main__":
    asyncio.run(ejecutar_sesion())
