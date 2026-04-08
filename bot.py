import asyncio
from playwright.async_api import async_playwright
import random
import time

# --- PEGA TUS PROXIES AQUÍ ---
LISTA_PROXIES = [
    "194.102.38.53:80",
    "129.226.81.110:7890",
    "182.53.202.208:8080",
    "152.32.190.98:3128",
    "185.76.240.21:10001"
]

async def saltar_ouo(page, url):
    print(f"[*] Iniciando cadena: {url}")
    try:
        # Tiempo de espera largo para la carga inicial
        await page.goto(url, wait_until="load", timeout=90000)
        
        # 25 intentos para asegurar que pase los 5 acortadores (2 clics por cada uno + margen)
        for i in range(25):
            await asyncio.sleep(15) # Ouo requiere que el contador llegue a 0
            url_actual = page.url
            print(f"[*] Paso {i+1} - URL: {url_actual}")

            # Condición de éxito: Llegar a Hotmart
            if "hotmart" in url_actual:
                print("[!!!] ¡ÉXITO TOTAL! Hemos llegado a Hotmart.")
                return True

            try:
                # Caso A: Etapa de "Get Link" (Botón btn-main)
                # Usamos JavaScript para el clic porque es más efectivo contra bloqueos
                btn_exists = await page.query_selector("#btn-main")
                if btn_exists:
                    print("[+] Detectado botón 'Get Link'. Ejecutando clic...")
                    await page.evaluate("document.getElementById('btn-main').click();")
                    continue

                # Caso B: Etapa de Captcha Invisible (form-captcha)
                form_exists = await page.query_selector("#form-captcha")
                if form_exists:
                    print("[+] Detectada etapa de Captcha. Enviando formulario...")
                    await page.evaluate("document.getElementById('form-captcha').submit();")
                    continue
                
                # Si no detecta nada pero sigue en Ouo, intentamos un clic de emergencia
                if "ouo.io" in url_actual:
                    print("[?] Reintentando forzar botones internos...")
                    await page.evaluate("if(document.getElementById('btn-main')) document.getElementById('btn-main').click();")
                    await page.evaluate("if(document.getElementById('form-captcha')) document.getElementById('form-captcha').submit();")

            except Exception:
                pass
                
    except Exception as e:
        print(f"[!] Error de conexión o tiempo agotado: {e}")

async def main():
    # Mezclamos tus proxies para rotar
    proxies = LISTA_PROXIES
    random.shuffle(proxies)

    async with async_playwright() as p:
        for i, proxy_actual in enumerate(proxies):
            print(f"\n--- Intento {i+1} con tu Proxy: {proxy_actual} ---")
            
            try:
                # Lanzamos el navegador con tu proxy
                browser = await p.chromium.launch(
                    headless=True, 
                    proxy={'server': f'http://{proxy_actual}'}
                )
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                )
                page = await context.new_page()

                # Leemos tu link principal del archivo
                try:
                    with open("links.txt", "r") as f:
                        links = [l.strip() for l in f if l.strip()]
                except:
                    links = ["https://ouo.io"]

                for link in links:
                    await saltar_ouo(page, link)
                
                await browser.close()
            except Exception as e:
                print(f"[!] Falló la conexión con {proxy_actual}")
                continue

if __name__ == "__main__":
    asyncio.run(main())
