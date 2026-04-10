import asyncio
import random
import os
from playwright.async_api import async_playwright

async def ver_video(proxy_line, video_id):
    ip = proxy_line.split(':')[0]
    try:
        user_pass_ip_port = proxy_line.split(':')
        proxy_config = {
            "server": f"http://{user_pass_ip_port[0]}:{user_pass_ip_port[1]}",
            "username": user_pass_ip_port[2],
            "password": user_pass_ip_port[3]
        }

        async with async_playwright() as p:
            # Lanzamiento con camuflaje avanzado
            browser = await p.chromium.launch(headless=True, args=[
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--mute-audio' # Importante para no gastar recursos
            ])
            
            # Perfil de usuario real
            context = await browser.new_context(
                proxy=proxy_config,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                viewport={'width': 1280, 'height': 720}
            )
            page = await context.new_page()

            # 1. "Calentar" la IP entrando primero a Google
            await page.goto("https://google.com", wait_until="networkidle")
            await asyncio.sleep(random.randint(3, 5))

            # 2. Entrar al video de Somnus Lab
            print(f"[*] IP {ip}: Cargando video...")
            await page.goto(f"https://www.youtube.com/watch?v={video_id}", wait_until="load")
            
            # 3. Bypass de carteles y simulación de Play
            await asyncio.sleep(10)
            try:
                # Clic en el reproductor para asegurar que inicie
                await page.click("button.ytp-play-button", timeout=10000)
                print(f"[+] IP {ip}: Reproducción iniciada.")
                
                # 4. Bajar calidad a 144p para ahorrar proxy
                await page.click("button.ytp-settings-button")
                await page.click("text=Calidad") or await page.click("text=Quality")
                await page.click("text=144p")
                print(f"[+] IP {ip}: Calidad ajustada a 144p.")
            except:
                print(f"[-] IP {ip}: No se pudo interactuar con el reproductor, pero el video sigue.")

            # 5. Permanencia (Simulación de ver el video entre 45-55 minutos)
            tiempo_vista = random.randint(2700, 3300) 
            print(f"[*] IP {ip}: Viendo video por {tiempo_vista//60} minutos...")
            
            # Simular scroll ocasional para parecer humano
            for _ in range(tiempo_vista // 300):
                await asyncio.sleep(300)
                await page.mouse.wheel(0, random.randint(300, 700))
                await asyncio.sleep(2)
                await page.mouse.wheel(0, -random.randint(300, 700))

            print(f"[SUCCESS] IP {ip}: Sesión finalizada correctamente.")
            await browser.close()

    except Exception as e:
        print(f"[!] Error IP {ip}: {str(e)[:50]}")

async def main():
    ID_VIDEO = "YF33K5irscg" # Tu video de Delta Waves
    with open('Webshare 10 proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]

    # Entrada escalonada: una IP cada 45 segundos para no alertar a YouTube
    tasks = []
    for p_line in proxies:
        tasks.append(asyncio.create_task(ver_video(p_line, ID_VIDEO)))
        await asyncio.sleep(45)
    
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
