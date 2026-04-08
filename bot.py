import asyncio
from playwright.async_api import async_playwright
import random
import requests
import re

async def obtener_proxy():
    try:
        # Fuente más estable de proxies
        r = requests.get("https://proxyscrape.com", timeout=10)
        ips = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)
        return random.choice(ips) if ips else None
    except: return None

async def saltar_capas(page, url):
    try:
        print(f"[*] Navegando a: {url}")
        # Cambiamos a 'domcontentloaded' para no esperar la publicidad infinita
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        
        for i in range(12):
            await asyncio.sleep(5)
            url_actual = page.url
            print(f"[*] Capa {i+1} - URL: {url_actual}")

            if "hotmart.com" in url_actual:
                print("[!!!] EXITOSO: Llegamos a Hotmart.")
                return True

            try:
                # Esperar al botón de Ouo o cualquier botón de salto
                print("[...] Esperando botón...")
                boton = await page.wait_for_selector("#btn-main, button:has-text('Get Link'), button:has-text('Continue')", timeout=20000)
                
                await asyncio.sleep(random.randint(10, 15))
                await boton.click()
                print(f"[+] Clic realizado.")
                
            except Exception:
                # Si no hay botón, intentamos enviar el formulario de captcha directamente
                try:
                    await page.evaluate("if(document.getElementById('form-captcha')) document.getElementById('form-captcha').submit();")
                    print("[+] Formulario forzado enviado.")
                except:
                    print("[-] Sin respuesta. Recargando...")
                    await page.reload(wait_until="domcontentloaded")
                
    except Exception as e:
        print(f"[X] Error: {e}")

async def main():
    async with async_playwright() as p:
        proxy_ip = await obtener_proxy()
        browser_args = ["--no-sandbox", "--disable-setuid-sandbox"]
        
        # Bloqueador de anuncios básico para acelerar carga
        browser = await p.chromium.launch(headless=True, args=browser_args)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            proxy={'server': f'http://{proxy_ip}'} if proxy_ip else None
        )
        
        page = await context.new_page()

        # Leer links
        try:
            with open("links.txt", "r") as f:
                links = [l.strip() for l in f if l.strip()]
        except: links = []

        for link in links:
            await saltar_capas(page, link)
            await asyncio.sleep(5)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
