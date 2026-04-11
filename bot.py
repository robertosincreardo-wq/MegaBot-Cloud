import asyncio
import random
import os
from playwright.async_api import async_playwright

async def generar_dinero(proxy_line, ad_url):
    datos = proxy_line.split(':')
    if len(datos) != 4: return
    ip, puerto, user, password = datos
    
    proxy_config = {"server": f"http://{ip}:{puerto}", "username": user, "password": password}

    async with async_playwright() as p:
        browser = None
        try:
            # Lanzamos con argumentos para que parezca un Windows real
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
            
            # El "context" es lo que Adsterra vigila. Le damos un User Agent de Windows Chrome.
            context = await browser.new_context(
                proxy=proxy_config,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                viewport={'width': 1366, 'height': 768}
            )
            page = await context.new_page()
            
            # Aumentamos el tiempo de espera para que el proxy lento no de error de protocolo
            page.set_default_timeout(90000)

            print(f"\n[*] IP {ip}: Cargando anuncio...")
            
            # Navegación lenta y segura
            await page.goto(ad_url, wait_until="commit")
            await asyncio.sleep(10) # Espera a que carguen los scripts de Adsterra

            # SIMULACIÓN HUMANA (Vital para que paguen)
            print(f"[*] IP {ip}: Simulando actividad...")
            for _ in range(3):
                await page.mouse.wheel(0, random.randint(200, 500))
                await asyncio.sleep(random.randint(2, 5))
            
            # CLIC ALEATORIO (Para activar el pago del CPM)
            await page.mouse.click(random.randint(100, 600), random.randint(100, 500))
            
            print(f"[SUCCESS] IP {ip}: Visita registrada correctamente.")
            await asyncio.sleep(5)
            
        except Exception as e:
            print(f"[!] IP {ip} error: {str(e)[:50]}")
        finally:
            if browser:
                await browser.close()

async def main():
    # Pon tu Direct Link aquí
    MI_LINK = "https://highrevenuegate.com" 
    
    if not os.path.exists('Webshare 10 proxies.txt'):
        print("Archivo de proxies no encontrado.")
        return

    with open('Webshare 10 proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]

    # IMPORTANTE: Los corremos uno por uno para evitar el "Protocol Error"
    # y para que Adsterra no vea 10 visitas al mismo segundo (sospechoso)
    while True:
        random.shuffle(proxies)
        for p_line in proxies:
            await generar_dinero(p_line, MI_LINK)
            # Espera de 1 a 2 minutos entre cada visita para que parezca tráfico real
            espera = random.randint(60, 120)
            print(f"[*] Esperando {espera}s para la siguiente visita...")
            await asyncio.sleep(espera)

if __name__ == "__main__":
    asyncio.run(main())
