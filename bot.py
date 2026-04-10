import asyncio
import random
import os
from playwright.async_api import async_playwright

async def ver_video(proxy_line, video_id):
    datos = proxy_line.split(':')
    if len(datos) != 4: return
    
    ip, puerto, user, password = datos
    # Forzamos el esquema http para el túnel
    proxy_config = {
        "server": f"http://{ip}:{puerto}",
        "username": user,
        "password": password
    }

    async with async_playwright() as p:
        browser = None
        try:
            # Añadimos flags para forzar la compatibilidad del túnel
            browser = await p.chromium.launch(headless=True, args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--ignore-certificate-errors',
                '--proxy-bypass-list=<-loopback>'
            ])
            
            context = await browser.new_context(
                proxy=proxy_config,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            page.set_default_timeout(120000)

            print(f"[*] IP {ip}: Intentando conectar a YouTube...")
            
            # Intentamos la carga. Si el túnel falla, saltará al except
            await page.goto(f"https://youtube.com{video_id}", wait_until="commit")
            
            # Espera técnica para que el reproductor se estabilice
            await asyncio.sleep(15)

            # Intentar click en el centro del reproductor para asegurar el Play
            try:
                await page.click("#movie_player", timeout=10000)
                print(f"[+] IP {ip}: Reproducción forzada.")
            except:
                pass

            # Simulación de visualización (45-55 min)
            tiempo = random.randint(2700, 3300)
            print(f"[SUCCESS] IP {ip}: Viendo video ({tiempo//60} min).")
            
            for _ in range(tiempo // 60):
                await asyncio.sleep(60)
                if page.is_closed(): break
                await page.mouse.wheel(0, 50)

        except Exception as e:
            if "ERR_TUNNEL_CONNECTION_FAILED" in str(e):
                print(f"[!] IP {ip}: El proxy rechazó la conexión (Túnel fallido).")
            else:
                print(f"[!] IP {ip}: Error -> {str(e)[:50]}")
        finally:
            if browser:
                await browser.close()

async def main():
    ID_VIDEO = "YF33K5irscg"
    if not os.path.exists('Webshare 10 proxies.txt'): return

    with open('Webshare 10 proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]

    print(f"[*] Iniciando sesión de {len(proxies)} proxies...")
    
    # Ejecución escalonada para no saturar los túneles
    tasks = []
    for p_line in proxies:
        tasks.append(asyncio.create_task(ver_video(p_line, ID_VIDEO)))
        await asyncio.sleep(30)
    
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
