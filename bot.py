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
        # Los proxies de ProxyScrape Premium suelen ser ip:puerto o ip:puerto:user:pass
        partes = proxy_line.split(':')
        ip = partes[0]
        
        if len(partes) == 4:
            # Formato ip:puerto:user:pass
            proxy_config = {"server": f"http://{partes[0]}:{partes[1]}", "username": partes[2], "password": partes[3]}
        else:
            # Formato ip:puerto (sin contraseña)
            proxy_config = {"server": f"http://{partes[0]}:{partes[1]}"}
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-blink-features=AutomationControlled'])
            context = await browser.new_context(proxy=proxy_config, user_agent=random.choice(UA_LIST))
            page = await context.new_page()

            print(f"[*] IP {ip}: Navegando a {url}")
            
            await page.goto(url, wait_until="commit", timeout=60000)
            await asyncio.sleep(5)

            # --- ETAPA 1: Botón "I'm a human" ---
            btn_main = "button#btn-main"
            try:
                await page.wait_for_selector(btn_main, state="visible", timeout=20000)
                print(f"    [+] Botón 'I'm a human' detectado en {ip}. Esperando 15s...")
                await page.mouse.wheel(0, random.randint(200, 500))
                await asyncio.sleep(15)
                await page.click(btn_main, force=True)
                print(f"    [*] Clic etapa 1 realizado.")
                await asyncio.sleep(8)
            except:
                print(f"    [!] No se vio el botón en Etapa 1 para {ip}.")

            # --- ETAPA 2: Botón "Get Link" ---
            try:
                if "ouo.io/press" in page.url:
                    await page.go_back()
                    await asyncio.sleep(5)

                await page.wait_for_selector(btn_main, state="visible", timeout=20000)
                print(f"    [+] Botón 'Get Link' detectado. Esperando 12s...")
                await asyncio.sleep(12)
                await page.click(btn_main, force=True)
                print(f"    [*] Clic etapa 2 realizado.")
                
                await asyncio.sleep(10)
                print(f"[SUCCESS] IP {ip}: Vista completada.")

            except:
                print(f"    [!] Error en Etapa 2 para {ip}.")

            await browser.close()
    except Exception as e:
        print(f"[!] Error IP {proxy_line.split(':')[0]}: Proxy lento o bloqueado.")

async def main():
    # 1. Cargar enlaces
    if not os.path.exists('links.txt'): return
    with open('links.txt', 'r') as f:
        enlaces = [line.strip() for line in f if line.strip()]
    
    # 2. Cargar los 1,000 proxies de ProxyScrape
    archivo_proxies = 'proxyscrape_premium_http_proxies.txt'
    if not os.path.exists(archivo_proxies):
        print(f"[!] No existe el archivo {archivo_proxies}")
        return
        
    with open(archivo_proxies, 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]
    
    print(f"[*] Cargados {len(proxies)} proxies. Iniciando proceso masivo...")

    for url in enlaces:
        # Procesamos en grupos de 3 para ir rápido sin colapsar el sistema
        for i in range(0, len(proxies), 3):
            batch = proxies[i:i+3]
            tareas = [procesar_ouo(p, url) for p in batch]
            await asyncio.gather(*tareas)
            
            # Pequeño descanso entre tandas
            await asyncio.sleep(random.randint(5, 10))

if __name__ == "__main__":
    asyncio.run(main())
