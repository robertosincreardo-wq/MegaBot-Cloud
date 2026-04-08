import asyncio
from playwright.async_api import async_playwright
import random
import requests
import re

async def obtener_proxies_github():
    print("[*] Descargando lista de IPs desde GitHub Raw...")
    # Usamos una lista de proxies HTTP actualizada que vive en GitHub
    url = "https://githubusercontent.com"
    try:
        r = requests.get(url, timeout=10)
        ips = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)
        if ips:
            print(f"[!] Se encontraron {len(ips)} IPs.")
            return ips
    except:
        pass
    return []

async def saltar_ouo(page, url):
    print(f"[*] Iniciando: {url}")
    try:
        # Cargamos la página
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        
        for i in range(12):
            await asyncio.sleep(10)
            url_actual = page.url
            print(f"[*] Capa {i+1} - URL: {url_actual}")

            if "hotmart" in url_actual:
                print("[!!!] ¡EXITO TOTAL! Llegamos a Hotmart.")
                return True

            # Intentamos las dos formas de saltar que tiene Ouo
            try:
                # 1. Enviar el formulario invisible (Etapa 1)
                await page.evaluate("if(document.getElementById('form-captcha')) document.getElementById('form-captcha').submit();")
                
                # 2. Click en el botón físico (Etapa 2)
                boton = await page.query_selector("#btn-main")
                if boton:
                    await boton.click()
                    print("[+] Clic en Get Link enviado.")
            except:
                pass
                
    except Exception as e:
        print(f"[X] Error: {e}")

async def main():
    ips = await obtener_proxies_github()
    if not ips:
        print("[X] No se pudo obtener ninguna IP. Revisa la conexión.")
        return

    async with async_playwright() as p:
        # Probaremos con 10 proxies diferentes para asegurar que uno pase
        for i in range(10):
            proxy_actual = random.choice(ips)
            print(f"\n--- Intento {i+1} - Usando Proxy: {proxy_actual} ---")
            
            try:
                browser = await p.chromium.launch(
                    headless=True, 
                    proxy={'server': f'http://{proxy_actual}'}
                )
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                )
                page = await context.new_page()
                page.set_default_timeout(45000) # 45 seg de espera por proxy lento

                with open("links.txt", "r") as f:
                    links = [l.strip() for l in f if l.strip()]

                for link in links:
                    await saltar_ouo(page, link)
                
                await browser.close()
            except:
                print(f"[!] El proxy {proxy_actual} falló o es muy lento. Saltando...")
                continue

if __name__ == "__main__":
    asyncio.run(main())
