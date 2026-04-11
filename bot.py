import asyncio
import random
import os
from playwright.async_api import async_playwright

# Disfraces de navegación para evitar bloqueos
UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
]

async def procesar_ouo(proxy_line, url):
    try:
        # Separar datos del proxy
        ip, puerto, user, password = proxy_line.split(':')
        proxy_config = {"server": f"http://{ip}:{puerto}", "username": user, "password": password}
        
        async with async_playwright() as p:
            # Lanzamos navegador con la configuración que funcionó en Adsterra
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-blink-features=AutomationControlled'])
            context = await browser.new_context(proxy=proxy_config, user_agent=random.choice(UA_LIST))
            page = await context.new_page()

            print(f"[*] IP {ip}: Navegando a {url}")
            
            # 1. Carga inicial (esperando a que los scripts se asienten)
            await page.goto(url, wait_until="commit", timeout=60000)
            await asyncio.sleep(5)

            # --- ETAPA 1: Botón "I'm a human" ---
            btn_main = "button#btn-main"
            try:
                # Esperamos que el botón aparezca
                await page.wait_for_selector(btn_main, state="visible", timeout=20000)
                print(f"    [+] Botón 'I'm a human' detectado. Esperando 15s...")
                
                # Simulación de scroll como en Adsterra
                await page.mouse.wheel(0, random.randint(200, 500))
                await asyncio.sleep(15)
                
                # Clic de activación
                await page.click(btn_main, force=True)
                print(f"    [*] Clic etapa 1 realizado.")
                await asyncio.sleep(8)
            except:
                print(f"    [!] No se vio el botón en Etapa 1.")

            # --- ETAPA 2: Botón "Get Link" (Contador 10s) ---
            try:
                # Verificamos si estamos en /press (basura) para volver
                if "ouo.io/press" in page.url:
                    await page.go_back()
                    await asyncio.sleep(5)

                await page.wait_for_selector(btn_main, state="visible", timeout=20000)
                print(f"    [+] Botón 'Get Link' detectado. Esperando 12s...")
                
                # Espera del contador (10s + 2s de margen)
                await asyncio.sleep(12)
                
                # Clic final
                await page.click(btn_main, force=True)
                print(f"    [*] Clic etapa 2 realizado.")
                
                # ESPERA FINAL (Vital para que cuente la vista)
                await asyncio.sleep(10)
                print(f"[SUCCESS] IP {ip}: Vista completada.")

            except:
                print(f"    [!] Error en Etapa 2 o ya finalizado.")

            await browser.close()
    except Exception as e:
        print(f"[!] Error IP {proxy_line.split(':')[0]}: {str(e)[:40]}")

async def main():
    # Cargar enlaces y proxies
    if not os.path.exists('links.txt'): return
    with open('links.txt', 'r') as f:
        enlaces = [line.strip() for line in f if line.strip()]
    with open('proxyscrape_premium_http_proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]

    # Ejecución uno por uno para asegurar que el proxy no colapse
    for url in enlaces:
        for p_line in proxies:
            await procesar_ouo(p_line, url)
            # Pequeño descanso entre proxies para no quemar el link
            await asyncio.sleep(random.randint(10, 20))

if __name__ == "__main__":
    asyncio.run(main())
