import asyncio
import random
import os
import re
from playwright.async_api import async_playwright

UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
]

async def procesar_ouo(proxy_config, url):
    ip = proxy_config["server"].split("//")[-1]
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-blink-features=AutomationControlled'])
            # Usamos el proxy extraído del TXT
            context = await browser.new_context(proxy=proxy_config, user_agent=random.choice(UA_LIST))
            page = await context.new_page()

            print(f"[*] IP {ip}: Navegando...")
            await page.goto(url, wait_until="commit", timeout=60000)
            await asyncio.sleep(5)

            btn_main = "button#btn-main"
            # ETAPA 1
            try:
                await page.wait_for_selector(btn_main, state="visible", timeout=15000)
                await page.mouse.wheel(0, random.randint(200, 500))
                await asyncio.sleep(15)
                await page.click(btn_main, force=True)
                await asyncio.sleep(8)
            except: pass

            # ETAPA 2
            try:
                if "ouo.io/press" in page.url:
                    await page.go_back()
                    await asyncio.sleep(5)

                await page.wait_for_selector(btn_main, state="visible", timeout=15000)
                print(f"    [+] Etapa 2 para {ip}. Esperando contador...")
                await asyncio.sleep(12)
                await page.click(btn_main, force=True)
                await asyncio.sleep(10)
                print(f"[SUCCESS] IP {ip}: Vista completada.")
            except: pass

            await browser.close()
    except Exception as e:
        print(f"[!] Error IP {ip}: Proxy lento o caído.")

def extraer_proxies_mil():
    lista_final = []
    if not os.path.exists('Free_Proxy_List.txt'): return []
    
    with open('Free_Proxy_List.txt', 'r') as f:
        for linea in f:
            # Limpiamos la línea de comillas y espacios
            partes = linea.replace('"', '').split(',')
            if len(partes) > 10:
                ip = partes[0]
                protocolo = partes[8] # socks4, socks5, etc
                puerto = partes[9]
                
                # Construimos el formato para Playwright
                lista_final.append({
                    "server": f"{protocolo}://{ip}:{puerto}"
                })
    return lista_final

async def main():
    if not os.path.exists('links.txt'): return
    with open('links.txt', 'r') as f:
        enlaces = [line.strip() for line in f if line.strip()]
    
    # Extraer los 1,000 proxies del nuevo formato
    proxies = extraer_proxies_mil()
    print(f"[*] Cargados {len(proxies)} proxies del archivo Free_Proxy_List.txt")

    # Ejecución masiva controlada
    for url in enlaces:
        # Mezclamos los proxies para no usar siempre los mismos primeros
        random.shuffle(proxies)
        # Procesamos en grupos de 3 para ir rápido pero seguro
        for i in range(0, len(proxies), 3):
            batch = proxies[i:i+3]
            tareas = [procesar_ouo(p, url) for p in batch]
            await asyncio.gather(*tareas)
            # Espera entre tandas
            await asyncio.sleep(random.randint(5, 10))

if __name__ == "__main__":
    asyncio.run(main())
