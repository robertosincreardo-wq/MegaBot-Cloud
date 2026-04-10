import asyncio
import random
import os
from playwright.async_api import async_playwright

# Disfraces de navegadores para variar las visitas
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
]

async def ejecutar_sesion():
    # Carga de archivos
    with open('Webshare 10 proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]
    with open('links.txt', 'r') as f:
        enlaces = [line.strip() for line in f if line.strip()]

    async with async_playwright() as p:
        for url in enlaces:
            # 1. Configurar Proxy (ip:puerto:user:pass)
            proxy_line = random.choice(proxies)
            try:
                ip, puerto, user, password = proxy_line.split(':')
                proxy_config = {
                    "server": f"http://{ip}:{puerto}",
                    "username": user,
                    "password": password
                }
            except Exception:
                print(f"[!] Salto de línea de proxy inválida")
                continue

            ua = random.choice(USER_AGENTS)
            print(f"\n[*] PROCESANDO: {url}")
            print(f"[*] USANDO IP: {ip} | NAVEGADOR: {ua[:40]}...")

            # 2. Lanzar Navegador (Solo Chromium para evitar fallos de instalación)
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
            context = await browser.new_context(proxy=proxy_config, user_agent=ua)
            page = await context.new_page()

            try:
                # 3. Navegación y espera de 20 segundos
                await page.goto(url, wait_until="commit", timeout=60000)
                print(f"[+] Página cargada. Esperando 20 segundos...")
                
                await asyncio.sleep(20)
                
                print(f"[SUCCESS] Finalizado con éxito")

            except Exception as e:
                print(f"[!] Error en link: {str(e)[:50]}")
            
            finally:
                await browser.close()

if __name__ == "__main__":
    asyncio.run(ejecutar_sesion())
