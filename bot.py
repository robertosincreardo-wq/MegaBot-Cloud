import asyncio
from playwright.async_api import async_playwright
import random
import requests
import re

async def obtener_proxy():
    try:
        r = requests.get("https://proxyscrape.com", timeout=5)
        ips = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)
        return random.choice(ips) if ips else None
    except: return None

async def saltar_ouo(page, url):
    print(f"[*] Navegando a: {url}")
    await page.goto(url, wait_until="networkidle", timeout=60000)
    
    for i in range(12): # Capas de la cadena
        print(f"[*] Capa {i+1} - URL: {page.url}")
        if "hotmart.com" in page.url:
            print("[!!!] ¡EXITO EN HOTMART!")
            return True

        # ESPERA ACTIVA: Esperamos a que el botón aparezca en el DOM
        try:
            # Buscamos botones de Ouo (btn-main) o Shink
            boton = await page.wait_for_selector("#btn-main, button, .btn-primary", timeout=15000)
            
            # Simulamos pensamiento humano
            await asyncio.sleep(random.randint(10, 15))
            
            # Click real simulando mouse
            await boton.click()
            print(f"[+] Click realizado en capa {i+1}")
        except:
            print("[-] Botón no apareció. Reintentando carga...")
            await page.reload()
    return False

async def main():
    async with async_playwright() as p:
        proxy_ip = await obtener_proxy()
        browser_args = {}
        if proxy_ip:
            print(f"[!] Usando Proxy: {proxy_ip}")
            browser_args['proxy'] = {'server': f'http://{proxy_ip}'}

        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()

        with open("links.txt", "r") as f:
            links = [l.strip() for l in f if l.strip()]

        for link in links:
            await saltar_ouo(page, link)
            await asyncio.sleep(5)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
