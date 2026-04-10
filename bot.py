import asyncio
import random
import os
from playwright.async_api import async_playwright

async def ejecutar_sesion():
    # Leer archivos
    with open('Webshare 10 proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]
    with open('links.txt', 'r') as f:
        enlaces = [line.strip() for line in f if line.strip()]

    async with async_playwright() as p:
        for url in enlaces:
            # 1. Extraer datos del proxy (ip:puerto:user:pass)
            proxy_line = random.choice(proxies)
            ip, puerto, user, password = proxy_line.split(':')
            
            proxy_config = {
                "server": f"http://{ip}:{puerto}",
                "username": user,
                "password": password
            }

            # 2. Rotación de Navegador Real (Chrome, Firefox o Safari)
            browser_type = random.choice([p.chromium, p.firefox, p.webkit])
            print(f"\n[*] LINK: {url}")
            print(f"[*] MOTOR: {browser_type.name} | PROXY: {ip}")

            # 3. Lanzar navegador
            browser = await browser_type.launch(headless=True, args=['--no-sandbox'] if browser_type == p.chromium else [])
            
            # 4. Configurar contexto (Disfraz de dispositivo)
            context = await browser.new_context(
                proxy=proxy_config,
                viewport={'width': 1920, 'height': 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
            )
            
            page = await context.new_page()

            try:
                # 5. Navegar y esperar 20 segundos
                await page.goto(url, wait_until="commit", timeout=90000)
                print(f"[+] Cargado. Esperando 20 segundos...")
                await asyncio.sleep(20)
                
                # Opcional: Tomar foto para ver si cargó bien
                # await page.screenshot(path=f"evidencia_{ip}.png")
                
                print(f"[SUCCESS] Finalizado link con {browser_type.name}")

            except Exception as e:
                print(f"[!] Error: {str(e)[:50]}")
            
            finally:
                await browser.close()

if __name__ == "__main__":
    asyncio.run(ejecutar_sesion())
