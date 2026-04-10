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
            ip, puerto, user, password = proxy_line.split(':')
            
            proxy_config = {
                "server": f"http://{ip}:{puerto}",
                "username": user,
                "password": password
            }

            # Selección de motor (Damos prioridad a Chromium si los otros fallan)
            motores = [p.chromium, p.firefox, p.webkit]
            random.shuffle(motores) # Mezclamos para variar

            for browser_type in motores:
                browser = None
                try:
                    print(f"\n[*] INTENTANDO LINK: {url}")
                    print(f"[*] MOTOR: {browser_type.name} | PROXY: {ip}")

                    # Lanzar navegador con argumentos de compatibilidad
                    browser = await browser_type.launch(
                        headless=True, 
                        args=['--no-sandbox'] if browser_type == p.chromium else []
                    )
                    
                    context = await browser.new_context(
                        proxy=proxy_config,
                        viewport={'width': 1280, 'height': 720},
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                    )
                    
                    page = await context.new_page()
                    await page.goto(url, wait_until="commit", timeout=60000)
                    
                    print(f"[+] Cargado con éxito. Esperando 20 segundos...")
                    await asyncio.sleep(20)
                    
                    print(f"[SUCCESS] Finalizado con {browser_type.name}")
                    await browser.close()
                    break # Si funcionó, salimos del bucle de motores y vamos al siguiente link

                except Exception as e:
                    print(f"[!] Fallo con {browser_type.name}: Reintentando con otro motor...")
                    if browser:
                        await browser.close()
                    continue # Intenta con el siguiente motor disponible

if __name__ == "__main__":
    asyncio.run(ejecutar_sesion())
