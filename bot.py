import asyncio
from playwright.async_api import async_playwright
import random
import time
import os

# --- REEMPLAZA CON TUS PROXIES FRESCOS ---
LISTA_PROXIES = [
    "152.32.190.98:3128", 
    "185.76.240.21:10001",
    "182.53.202.208:8080",
    "194.102.38.53:80",
    "129.226.81.110:7890"
]

async def saltar_ouo(page, url):
    print(f"[*] Iniciando cadena: {url}")
    try:
        # Cargamos tu link real
        await page.goto(url, wait_until="domcontentloaded", timeout=90000)
        
        for i in range(25):
            await asyncio.sleep(15)
            url_actual = page.url
            print(f"[*] Paso {i+1} - URL: {url_actual}")

            # 1. SI LLEGAMOS AL DESTINO FINAL
            if "hotmart" in url_actual:
                print("[!!!] ¡EXITO TOTAL! Llegamos a Hotmart.")
                return True

            # 2. SI CAE EN LA TRAMPA DE PRESS, VOLVER ATRÁS
            if "ouo.press" in url_actual:
                print("[!] Detectado ouo.press. Volviendo atrás...")
                await page.go_back()
                continue

            try:
                # 3. BUSCAR BOTÓN PRINCIPAL
                btn = await page.query_selector("#btn-main")
                if btn:
                    print("[+] Clic en btn-main detectado")
                    await page.evaluate("document.getElementById('btn-main').click();")
                    continue

                # 4. ENVIAR FORMULARIO (CAPTCHA/GO)
                form = await page.query_selector("form[id*='captcha'], form[id*='go']")
                if form:
                    print("[+] Enviando formulario interno")
                    await page.evaluate("document.querySelector('form[id*=\"captcha\"], form[id*=\"go\"]').submit();")
                    continue

            except:
                pass
                
    except Exception as e:
        print(f"[!] Error de navegación: {e}")

async def main():
    # Mezclamos tus proxies
    proxies = LISTA_PROXIES
    random.shuffle(proxies)

    async with async_playwright() as p:
        for i, proxy_actual in enumerate(proxies):
            print(f"\n--- Intento {i+1} - Proxy: {proxy_actual} ---")
            
            try:
                browser = await p.chromium.launch(
                    headless=True, 
                    proxy={'server': f'http://{proxy_actual}'}
                )
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                )
                page = await context.new_page()
                
                # --- LEER TU LINK REAL DEL ARCHIVO ---
                enlace_para_bot = ""
                if os.path.exists("links.txt"):
                    with open("links.txt", "r") as f:
                        enlace_para_bot = f.readline().strip()
                
                # Si por alguna razón falla el archivo, usa este de respaldo (TU LINK)
                if not enlace_para_bot:
                    enlace_para_bot = "https://ouo.io"

                await saltar_ouo(page, enlace_para_bot)
                await browser.close()
            except:
                continue

if __name__ == "__main__":
    asyncio.run(main())
