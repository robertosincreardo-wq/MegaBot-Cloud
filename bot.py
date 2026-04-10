import asyncio
import random
from playwright.async_api import async_playwright

async def procesar_enlaces():
    # 1. Cargar proxies y enlaces desde tus archivos TXT
    try:
        with open('Webshare 10 proxies.txt', 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]
        with open('links.txt', 'r') as f:
            enlaces = [line.strip() for line in f if line.strip()]
    except FileNotFoundError as e:
        print(f"[!] Error: No se encontró el archivo: {e.filename}")
        return

    async with async_playwright() as p:
        for url in enlaces:
            exito = False
            # Usar un proxy aleatorio de tus 10 nuevos para cada link
            proxy_seleccionado = random.choice(proxies)
            
            print(f"\n[*] Intentando: {url}")
            print(f"[*] Usando Proxy: {proxy_seleccionado}")

            # Configurar el navegador con el proxy
            # Formato esperado en el txt: ip:puerto:user:pass o ip:puerto
            browser = await p.chromium.launch(headless=True, proxy={"server": f"http://{proxy_seleccionado}"})
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            )
            page = await context.new_page()

            try:
                # Navegar con timeout largo para evitar el error anterior
                await page.goto(url, wait_until="domcontentloaded", timeout=90000)
                
                # ESPERA DE 20 SEGUNDOS (Solicitada para que cargue todo)
                print(f"[+] Página alcanzada. Esperando 20 segundos para carga completa...")
                await asyncio.sleep(20)
                
                print(f"[#] Título actual: {await page.title()}")
                
                # --- AQUÍ PUEDES AGREGAR CLICS SI ES NECESARIO ---
                # Ejemplo: await page.click('text=Confirmar') 
                
                exito = True
                print(f"[SUCCESS] Proceso terminado para: {url}")

            except Exception as e:
                print(f"[!] Error durante la navegación en {url}: {e}")
            
            finally:
                await browser.close()

# ESTA LÍNEA ES VITAL PARA QUE EL BOT ARRANQUE
if __name__ == "__main__":
    asyncio.run(procesar_enlaces())
