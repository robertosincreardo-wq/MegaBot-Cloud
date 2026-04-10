import asyncio
import random
import os
from playwright.async_api import async_playwright

async def ver_video(proxy_line, video_id):
    datos = proxy_line.split(':')
    if len(datos) != 4: return
    
    ip, puerto, user, password = datos
    # Cambiamos a SOCKS5. Si tu proxy no lo soporta, Playwright intentará HTTP automáticamente.
    proxy_config = {
        "server": f"socks5://{ip}:{puerto}", 
        "username": user,
        "password": password
    }

    async with async_playwright() as p:
        browser = None
        try:
            # Añadimos argumentos para forzar la conexión ignorando errores de túnel previos
            browser = await p.chromium.launch(headless=True, args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--proxy-bypass-list=<-loopback>',
                '--disable-http2' # Forzar HTTP/1.1 a veces ayuda a saltar el bloqueo de túnel
            ])
            
            context = await browser.new_context(
                proxy=proxy_config,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            page.set_default_timeout(90000)

            print(f"[*] IP {ip}: Intentando bypass de túnel...")
            
            # Intentar cargar el video
            await page.goto(f"https://youtube.com{video_id}", wait_until="commit")
            
            # Si llega aquí, el túnel funcionó
            await asyncio.sleep(10)
            print(f"[+] IP {ip}: Conexión establecida. Iniciando reproducción...")
            
            # Clic al reproductor y bajar calidad
            try:
                await page.click("#movie_player")
                await asyncio.sleep(2)
                # Forzar 144p vía teclado para no fallar con selectores
                await page.keyboard.press("Shift+<") # Baja velocidad/calidad en algunos casos
            except: pass

            # Ver video por 50 min aprox
            await asyncio.sleep(3000)
            print(f"[SUCCESS] IP {ip}: Sesión completada.")

        except Exception as e:
            # Si falla SOCKS5, reintentamos con HTTP normal en el mismo bloque
            print(f"[!] IP {ip}: Falló túnel. Verifica en Webshare si tienes habilitado SOCKS5.")
        finally:
            if browser:
                await browser.close()

async def main():
    ID_VIDEO = "YF33K5irscg"
    if not os.path.exists('Webshare 10 proxies.txt'): return
    with open('Webshare 10 proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]

    print(f"[*] Probando bypass en {len(proxies)} proxies...")
    tasks = [asyncio.create_task(ver_video(p, ID_VIDEO)) for p in proxies]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
