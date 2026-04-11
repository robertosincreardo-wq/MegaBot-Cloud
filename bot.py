import asyncio
import random
import os
from playwright.async_api import async_playwright

UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
]

async def procesar_ouo(proxy_line, url):
    try:
        partes = proxy_line.split(':')
        ip = partes[0]
        if len(partes) == 4:
            proxy_config = {"server": f"http://{partes[0]}:{partes[1]}", "username": partes[2], "password": partes[3]}
        else:
            proxy_config = {"server": f"http://{partes[0]}:{partes[1]}"}
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-blink-features=AutomationControlled'])
            
            # AJUSTE: Añadimos Referer de YouTube para que el proxy pase el filtro
            context = await browser.new_context(
                proxy=proxy_config, 
                user_agent=random.choice(UA_LIST),
                extra_http_headers={"Referer": "https://youtube.com"}
            )
            page = await context.new_page()

            print(f"[*] IP {ip}: Navegando a {url}")
            await page.goto(url, wait_until="commit", timeout=60000)
            await asyncio.sleep(8) # Más tiempo inicial para proxies lentos

            btn_main = "button#btn-main"
            try:
                # Si no aparece el botón, intentamos recargar una vez
                if not await page.is_visible(btn_main):
                    await page.reload()
                    await asyncio.sleep(10)

                await page.wait_for_selector(btn_main, state="visible", timeout=25000)
                print(f"    [+] Botón detectado en {ip}. Esperando 15s...")
                await page.mouse.wheel(0, random.randint(200, 500))
                await asyncio.sleep(15)
                await page.click(btn_main, force=True)
                await asyncio.sleep(8)
                
                # Etapa 2
                if "ouo.io/press" in page.url:
                    await page.go_back()
                    await asyncio.sleep(5)

                await page.wait_for_selector(btn_main, state="visible", timeout=25000)
                print(f"    [+] Etapa 2 OK. Esperando 12s...")
                await asyncio.sleep(12)
                await page.click(btn_main, force=True)
                await asyncio.sleep(10)
                print(f"[SUCCESS] IP {ip}: Vista completada.")

            except:
                print(f"    [!] Error: El proxy {ip} sigue bloqueado por ouo.io.")

            await browser.close()
    except Exception as e:
        print(f"[!] IP {proxy_line.split(':')[0]} falló.")

async def main():
    if not os.path.exists('links.txt'): return
    with open('links.txt', 'r') as f:
        enlaces = [line.strip() for line in f if line.strip()]
    
    # Probando con el archivo de 100 proxies
    archivo_proxies = 'proxyscrape_premium_http_proxies.txt'
    if not os.path.exists(archivo_proxies): return

    with open(archivo_proxies, 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]

    for url in enlaces:
        for p_line in proxies:
            await procesar_ouo(p_line, url)
            await asyncio.sleep(random.randint(5, 10))

if __name__ == "__main__":
    asyncio.run(main())
