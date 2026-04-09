import asyncio
from playwright.async_api import async_playwright
import os
import time

# --- DATOS DE ROTACIÓN WEBSHARE ---
WS_USER = "inrjymkc-rotate"
WS_PASS = "kyhwkgls9xnq"
WS_SERVER = "p.webshare.io:80" 
PROXY_URL = f"http://{WS_USER}:{WS_PASS}@{WS_SERVER}"

async def saltar_ouo(page):
    # Enlace forzado para que no haya fallos
    enlace = "https://ouo.io"
    print(f"[1] Intentando cargar: {enlace}")
    
    try:
        # Abrimos la página
        await page.goto(enlace, wait_until="domcontentloaded", timeout=60000)
        print(f"[2] Página cargada. URL actual: {page.url}")
        
        for i in range(25):
            await asyncio.sleep(12) 
            url_actual = page.url
            print(f"[*] Paso {i+1} - URL: {url_actual}")

            if "hotmart" in url_actual:
                print("[!!!] ¡EXITO TOTAL! Llegamos a Hotmart.")
                return True

            if "ouo.press" in url_actual:
                print("[!] Trampa .press detectada. Volviendo atrás...")
                await page.go_back()
                continue

            try:
                # Intento de clic en el botón principal
                btn = await page.query_selector("#btn-main")
                if btn:
                    print("[+] Botón 'Get Link' encontrado. Clickeando...")
                    await page.evaluate("document.getElementById('btn-main').click();")
                    continue
                
                # Intento de envío de formulario (Captcha)
                form = await page.query_selector("#form-captcha")
                if form:
                    print("[+] Formulario Captcha encontrado. Enviando...")
                    await page.evaluate("document.getElementById('form-captcha').submit();")
                    continue
            except:
                pass
                
    except Exception as e:
        print(f"[X] Error en la navegación: {e}")

async def main():
    print("[START] Iniciando el proceso del Bot...")
    async with async_playwright() as p:
        for i in range(5):
            print(f"\n--- Sesión {i+1} ---")
            try:
                print(f"[*] Conectando al proxy: {WS_SERVER}")
                browser = await p.chromium.launch(
                    headless=True,
                    proxy={"server": PROXY_URL}
                )
                
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                )
                
                page = await context.new_page()
                await saltar_ouo(page)
                await browser.close()
                print(f"[*] Sesión {i+1} terminada.")
            except Exception as e:
                print(f"[X] Error crítico en Sesión {i+1}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
