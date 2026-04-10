import asyncio
import random
import os
from playwright.async_api import async_playwright

async def ver_video(proxy_line, video_id):
    # Separar correctamente: ip:puerto:usuario:contraseña
    datos = proxy_line.split(':')
    if len(datos) != 4:
        print(f"[!] Formato de proxy incorrecto: {proxy_line}")
        return
    
    ip, puerto, user, password = datos
    proxy_config = {
        "server": f"http://{ip}:{puerto}",
        "username": user,
        "password": password
    }

    async with async_playwright() as p:
        try:
            print(f"[*] IP {ip}: Iniciando navegador...")
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
            context = await browser.new_context(
                proxy=proxy_config,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
            )
            page = await context.new_page()

            # Aumentamos el tiempo de espera a 120 segundos para proxies lentos
            page.set_default_timeout(120000)

            print(f"[*] IP {ip}: Cargando video (Timeout 120s)...")
            # Usamos wait_until="commit" para que no espere a que carguen todos los anuncios
            await page.goto(f"https://youtube.com{video_id}", wait_until="commit")
            
            await asyncio.sleep(15) # Espera a que el JS se asiente
            
            # Intentar dar Play si no arrancó solo
            try:
                await page.click("button.ytp-play-button", timeout=15000)
                print(f"[+] IP {ip}: Reproducción activada.")
            except:
                pass

            # Simular que ve el video por 45-55 minutos
            tiempo = random.randint(2700, 3300)
            print(f"[SUCCESS] IP {ip}: Viendo video por {tiempo//60} min...")
            
            # Dividimos la espera en ciclos para mantener el bot vivo
            for _ in range(tiempo // 60):
                await asyncio.sleep(60)
                # Pequeño scroll para que YouTube no piense que la pestaña se durmió
                await page.mouse.wheel(0, 100)
                await page.mouse.wheel(0, -100)

            await browser.close()
        except Exception as e:
            print(f"[!] Error IP {ip}: {str(e)[:60]}")

async def main():
    ID_VIDEO = "YF33K5irscg"
    if not os.path.exists('Webshare 10 proxies.txt'):
        print("[!] No existe el archivo de proxies.")
        return

    with open('Webshare 10 proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]

    print(f"[*] Lanzando {len(proxies)} espectadores escalonados...")
    
    tasks = []
    for p_line in proxies:
        tasks.append(asyncio.create_task(ver_video(p_line, ID_VIDEO)))
        await asyncio.sleep(40) # Espera entre cada IP para no saturar la CPU de GitHub
    
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
