import asyncio
from playwright.async_api import async_playwright
import random
import requests
import re

async def obtener_proxy():
    print("[*] Buscando IP...")
    try:
        r = requests.get("https://proxyscrape.com", timeout=5)
        ips = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)
        if ips:
            p = random.choice(ips)
            print(f"[!] Proxy seleccionado: {p}")
            return p
    except: pass
    return None

async def saltar_capas(page, url):
    try:
        print(f"[*] Navegando a: {url}")
        # Espera a que la red esté tranquila (networkidle)
        await page.goto(url, wait_until="networkidle", timeout=60000)
        
        for i in range(12): # Soporta las 5 capas de tu cadena
            await asyncio.sleep(5)
            url_actual = page.url
            print(f"[*] Capa {i+1} - URL: {url_actual}")

            if "hotmart.com" in url_actual:
                print("[!!!] EXITOSO: Llegamos a Hotmart.")
                return True

            try:
                # ESPERA ACTIVA: Espera a que el botón aparezca en el código (DOM)
                # Buscamos por ID (ouo) o por texto de botón (shink/otros)
                print("[...] Buscando botón de salto...")
                
                # Intentamos esperar a cualquiera de estos elementos
                boton = await page.wait_for_selector("#btn-main, button:has-text('Get Link'), button:has-text('Continue'), .btn-main", timeout=20000)
                
                # Tiempo de espera humano (contador de 5-10 seg)
                await asyncio.sleep(random.randint(10, 15))
                
                # Clic real
                await boton.click()
                print(f"[+] Clic realizado en capa {i+1}")
                
            except Exception:
                print("[-] No se vio el botón. Intentando recargar página...")
                await page.reload(wait_until="networkidle")
                
    except Exception as e:
        print(f"[X] Error en el proceso: {e}")

async def main():
    async with async_playwright() as p:
        proxy_ip = await obtener_proxy()
        
        # Configuración del navegador (Humanizado)
        launch_args = ["--no-sandbox", "--disable-setuid-sandbox"]
        proxy_settings = None
        if proxy_ip:
            proxy_settings = {'server': f'http://{proxy_ip}'}

        browser = await p.chromium.launch(headless=True, args=launch_args, proxy=proxy_settings)
        
        # Fingerprint humanizada
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080},
            locale="es-ES"
        )
        
        page = await context.new_page()

        # Leer tus links
        try:
            with open("links.txt", "r") as f:
                links = [l.strip() for l in f if l.strip()]
        except:
            links = []

        for link in links:
            print(f"\n--- Iniciando Cadena: {link} ---")
            await saltar_capas(page, link)
            await asyncio.sleep(10)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
