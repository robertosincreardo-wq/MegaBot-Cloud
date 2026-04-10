import asyncio
from playwright.async_api import async_playwright

# 1. Carga aquí tus 10 proxies nuevos (formato ip:puerto:user:pass o ip:puerto)
NUEVOS_PROXIES = [
    # "http://usuario:password@ip:puerto",
    # ... pega aquí las líneas de tu archivo txt
]

async def navegar_con_prioridad_proxy():
    async with async_playwright() as p:
        for proxy_url in NUEVOS_PROXIES:
            print(f"[*] Probando con proxy: {proxy_url}")
            
            # Configuración del navegador con el proxy actual
            browser = await p.chromium.launch(headless=True, proxy={"server": proxy_url})
            context = await browser.new_context()
            page = await context.new_page()

            try:
                # Aumentamos el timeout a 90s para dar margen a la carga con proxy
                await page.goto("https://ouo.io", wait_until="domcontentloaded", timeout=90000)
                print("[+] Conexión exitosa a ouo.io")
                
                # Aquí puedes añadir la lógica de interacción que usamos la primera vez
                # ...
                
                await browser.close()
                break # Si funciona, salimos del bucle
                
            except Exception as e:
                print(f"[!] Error con proxy {proxy_url}: {e}")
                await browser.close()

# Ejecutar el script
# asyncio.run(navegar_con_prioridad_proxy())
