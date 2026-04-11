import asyncio
import random
from playwright.async_api import async_playwright

async def trabajar_link(proxy_line, link):
    datos = proxy_line.split(':')
    if len(datos) != 4: return
    ip, puerto, user, password = datos
    
    proxy_config = {"server": f"http://{ip}:{puerto}", "username": user, "password": password}

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
            context = await browser.new_context(proxy=proxy_config, user_agent="Mozilla/5.0...")
            page = await context.new_page()

            print(f"[*] IP {ip}: Generando dinero...")
            await page.goto(link, wait_until="networkidle", timeout=60000)
            
            # SIMULACIÓN HUMANA PARA QUE PAGUEN:
            # 1. Espera aleatoria
            await asyncio.sleep(random.randint(15, 25))
            
            # 2. Scroll para simular lectura
            await page.mouse.wheel(0, random.randint(400, 900))
            
            # 3. EL TRUCO: Clic en cualquier parte para activar el anuncio
            await page.mouse.click(random.randint(100, 500), random.randint(100, 500))
            print(f"[+] IP {ip}: Clic de activación realizado.")
            
            await asyncio.sleep(10)
            await browser.close()
            print(f"[SUCCESS] IP {ip}: Tarea completada.")

        except:
            if browser: await browser.close()

async def main():
    # Pon aquí tu SmartLink de Monetag o Adsterra
    MI_LINK = "https://www.profitablecpmratenetwork.com/x458ti0i?key=b90007f89e492911f0d12049a4118dd6" 
    with open('Webshare 10 proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]

    while True:
        # Ejecutamos las 10 IPs en ráfagas para que parezca tráfico real
        tasks = [asyncio.create_task(trabajar_link(p, MI_LINK)) for p in proxies]
        await asyncio.gather(*tasks)
        
        # Espera de 10 minutos para que no sospechen de las mismas IPs
        print("[*] Ciclo terminado. Esperando 10 min para limpiar IPs...")
        await asyncio.sleep(600)

if __name__ == "__main__":
    asyncio.run(main())
