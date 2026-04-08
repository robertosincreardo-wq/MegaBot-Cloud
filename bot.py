import asyncio
from playwright.async_api import async_playwright
import random
import time

# LISTA DE PROXIES HARDCODED (Para que no dependa de internet para bajarlos)
# Estos son proxies publicos que rotan mucho, si fallan los cambiaremos.
LISTA_PROXIES = [
    "194.102.38.53:80",
    "129.226.81.110:7890",
    "182.53.202.208:8080",
    "152.32.190.98:3128",
    "185.76.240.21:10001"
]


async def saltar_ouo(page, url):
    print(f"[*] Iniciando: {url}")
    try:
        # Cargamos la página con un tiempo de espera largo
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        
        for i in range(12):
            await asyncio.sleep(12)
            url_actual = page.url
            print(f"[*] Capa {i+1} - URL: {url_actual}")

            if "hotmart" in url_actual:
                print("[!!!] ¡EXITO TOTAL! Llegamos a Hotmart.")
                return True

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
        print(f"[X] Error en navegación: {e}")

async def main():
    # Mezclamos la lista interna
    proxies = LISTA_PROXIES
    random.shuffle(proxies)

    async with async_playwright() as p:
        # Probaremos con los proxies de la lista
        for i, proxy_actual in enumerate(proxies[:5]):
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

                try:
                    with open("links.txt", "r") as f:
                        links = [l.strip() for l in f if l.strip()]
                except:
                    links = ["https://ouo.io"]

                for link in links:
                    await saltar_ouo(page, link)
                
                await browser.close()
            except Exception as e:
                print(f"[!] Fallo con proxy {proxy_actual}")
                continue

if __name__ == "__main__":
    asyncio.run(main())
