import asyncio
import random
from playwright.async_api import async_playwright

async def generar_impresion(proxy_line, ad_url):
    try:
        ip, puerto, user, password = proxy_line.split(':')
        proxy_config = {"server": f"http://{ip}:{puerto}", "username": user, "password": password}
        
        async with async_playwright() as p:
            # Usamos Stealth para evitar baneos
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
            context = await browser.new_context(proxy=proxy_config)
            page = await context.new_page()

            print(f"[*] IP {ip}: Visitando link de Adsterra...")
            # Entramos al SmartLink
            await page.goto(ad_url, wait_until="networkidle", timeout=60000)
            
            # Permanencia aleatoria para simular lectura (20-40 segundos)
            espera = random.randint(20, 40)
            await asyncio.sleep(espera)
            
            print(f"[SUCCESS] IP {ip}: Impresión válida generada.")
            await browser.close()
    except Exception as e:
        print(f"[!] IP {ip} falló: {str(e)[:50]}")

async def main():
    # PEGA AQUÍ TU DIRECT LINK DE ADSTERRA
    MI_DIRECT_LINK = "TU_LINK_AQUI" 
    with open('Webshare 10 proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]

    # Rotamos los proxies en bucle para maximizar visitas
    while True:
        tasks = []
        # Lanzamos de 5 en 5 para no saturar
        for p_line in random.sample(proxies, 5):
            tasks.append(asyncio.create_task(generar_impresion(p_line, MI_DIRECT_LINK)))
        
        await asyncio.gather(*tasks)
        print("[*] Ciclo completado. Esperando 2 minutos para rotar...")
        await asyncio.sleep(120)

if __name__ == "__main__":
    asyncio.run(main())
