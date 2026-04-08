import asyncio
from playwright.async_api import async_playwright
import random
import requests
import re

async def obtener_proxies_frescos():
    print("[*] Descargando lista de IPs nuevas...")
    # Usamos una fuente de proxies SOCKS5 que suelen saltar mejor los bloqueos
    url = "https://proxyscrape.com"
    try:
        r = requests.get(url, timeout=10)
        return re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)
    except: return []

async def saltar_ouo(page, url):
    print(f"[*] Iniciando: {url}")
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        
        for i in range(12):
            await asyncio.sleep(10)
            url_actual = page.url
            print(f"[*] Capa {i+1} - URL: {url_actual}")

            if "hotmart" in url_actual:
                print("[!!!] ¡EXITO TOTAL! Llegamos a Hotmart.")
                return True

            # Si nos quedamos trabados en la misma URL, intentamos forzar
            try:
                # 1. Intentamos enviar el formulario de captcha (Etapa 1)
                await page.evaluate("if(document.getElementById('form-captcha')) document.getElementById('form-captcha').submit();")
                
                # 2. Si hay botón de "Get Link" (Etapa 2), le damos clic
                boton = await page.query_selector("#btn-main")
                if boton:
                    await asyncio.sleep(5)
                    await boton.click()
                    print("[+] Clic en Get Link realizado.")
            except:
                pass
                
    except Exception as e:
        print(f"[X] Error: {e}")

async def main():
    ips = await obtener_proxies_frescos()
    if not ips:
        print("[X] No se encontraron proxies. Abortando para evitar baneo.")
        return

    async with async_playwright() as p:
        for i in range(5): # Intentaremos con 5 proxies diferentes
            proxy_actual = random.choice(ips)
            print(f"\n--- Intento {i+1} con Proxy: {proxy_actual} ---")
            
            browser = await p.chromium.launch(headless=True, proxy={'server': f'http://{proxy_actual}'})
            context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            page = await context.new_page()

            with open("links.txt", "r") as f:
                links = [l.strip() for l in f if l.strip()]

            for link in links:
                await saltar_ouo(page, link)
            
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
