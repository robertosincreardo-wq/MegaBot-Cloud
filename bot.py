import asyncio
from playwright.async_api import async_playwright

async def procesar_todos_los_links():
    # 1. Cargamos los proxies y los links desde tus archivos
    with open('Webshare 10 proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]
    
    with open('links.txt', 'r') as f:
        enlaces = [line.strip() for line in f if line.strip()]

    async with async_playwright() as p:
        for url in enlaces:
            exito = False
            print(f"\n[*] Procesando link: {url}")
            
            # Intentamos cada link con la lista de proxies hasta que uno funcione
            for proxy_url in proxies:
                print(f"  [-] Intentando con proxy: {proxy_url}")
                browser = None
                try:
                    # Configuramos el proxy (ajusta el formato si es ip:puerto:user:pass)
                    browser = await p.chromium.launch(headless=True, proxy={"server": f"http://{proxy_url}"})
                    context = await browser.new_context()
                    page = await context.new_page()
                    
                    # Timeout de 90s para evitar el error anterior
                    await page.goto(url, wait_until="domcontentloaded", timeout=90000)
                    
                    print(f"  [+] ¡Éxito en {url}!")
                    # --- AQUÍ VA TU LÓGICA DE CLICS O INTERACCIÓN ---
                    
                    exito = True
                    await browser.close()
                    break # Pasamos al siguiente link de links.txt
                    
                except Exception as e:
                    print(f"  [!] Falló proxy {proxy_url}: {e}")
                    if browser:
                        await browser.close()
            
            if not exito:
                print(f"[!!!] No se pudo procesar el link {url} con ningún proxy.")

# Ejecutar proceso
# asyncio.run(procesar_todos_los_links())
