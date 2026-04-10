import asyncio
import random
import os
from playwright.async_api import async_playwright

async def ver_video(proxy_line, video_id):
    datos = proxy_line.split(':')
    if len(datos) != 4: return
    ip, puerto, user, password = datos
    
    # Intentamos con el formato estándar que suele funcionar en Webshare
    proxy_config = {
        "server": f"http://{ip}:{puerto}",
        "username": user,
        "password": password
    }

    async with async_playwright() as p:
        try:
            # Emulamos un iPhone 13 para saltar bloqueos de Datacenter de escritorio
            iphone_13 = p.devices['iPhone 13']
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
            
            context = await browser.new_context(
                **iphone_13,
                proxy=proxy_config,
                ignore_https_errors=True # Salta errores de túnel SSL
            )
            
            page = await context.new_page()
            # Timeout largo de 2 minutos
            page.set_default_timeout(120000)

            print(f"[*] IP {ip}: Intentando entrar como móvil...")
            
            # Navegar al video (URL de móvil es la misma, pero el contexto cambia)
            await page.goto(f"https://youtube.com{video_id}", wait_until="commit")
            
            await asyncio.sleep(15)
            
            # En móvil, el botón de play es un poco distinto, lo buscamos
            try:
                await page.click(".ytp-large-play-button", timeout=10000)
                print(f"[+] IP {ip}: Play presionado.")
            except:
                # Si no está el botón grande, intentamos clic en el centro
                await page.mouse.click(200, 200)

            print(f"[SUCCESS] IP {ip}: Dentro del video. Manteniendo sesión...")
            
            # Ver por 50 minutos
            await asyncio.sleep(3000)
            await browser.close()

        except Exception as e:
            print(f"[!] IP {ip}: Error -> {str(e)[:45]}")
            if browser: await browser.close()

async def main():
    ID_VIDEO = "YF33K5irscg"
    if not os.path.exists('Webshare 10 proxies.txt'): return
    with open('Webshare 10 proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]

    print(f"[*] Lanzando {len(proxies)} hilos en modo Mobile Bypass...")
    tasks = [asyncio.create_task(ver_video(p, ID_VIDEO)) for p in proxies]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
