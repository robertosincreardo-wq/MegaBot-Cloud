import asyncio
from playwright.async_api import async_playwright
import random
import time
import os

# --- DATOS DE ROTACIÓN WEBSHARE (Puerto 3128) ---
# El puerto 3128 es el más estable para autenticación en servidores
WS_PROXY = "http://webshare.io"
WS_USER = "inrjymkc-rotate"
WS_PASS = "kyhwkgls9xnq"

async def saltar_ouo(page, url_objetivo):
    print(f"[*] Navegando a: {url_objetivo}")
    try:
        # Cargamos el link
        await page.goto(url_objetivo, wait_until="domcontentloaded", timeout=60000)
        
        for i in range(25):
            await asyncio.sleep(15) 
            url_actual = page.url
            print(f"[*] Paso {i+1} - URL: {url_actual}")

            if "hotmart" in url_actual:
                print("[!!!] ¡EXITO TOTAL! Llegamos a Hotmart.")
                return True

            if "ouo.press" in url_actual:
                print("[!] Trampa detectada. Volviendo atrás...")
                await page.go_back()
                continue

            try:
                # Prioridad 1: Botón Get Link
                btn = await page.query_selector("#btn-main")
                if btn:
                    print("[+] Clic en 'Get Link'")
                    await page.evaluate("document.getElementById('btn-main').click();")
                    continue
                
                # Prioridad 2: Formulario Captcha
                form = await page.query_selector("#form-captcha")
                if form:
                    print("[+] Enviando Formulario")
                    await page.evaluate("document.getElementById('form-captcha').submit();")
                    continue
            except:
                pass
    except Exception as e:
        print(f"[!] El proxy no logró conectar: {e}")

async def main():
    async with async_playwright() as p:
        for i in range(15):
            print(f"\n--- Sesión {i+1} ---")
            try:
                browser = await p.chromium.launch(
                    headless=True,
                    proxy={
                        "server": WS_PROXY,
                        "username": WS_USER,
                        "password": WS_PASS
                    }
                )
                
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                )
                page = await context.new_page()

                enlace = "https://ouo.io"
                await saltar_ouo(page, enlace)
                await browser.close()
            except Exception as e:
                print(f"[!] Error de inicio: {e}")
                continue

if __name__ == "__main__":
    asyncio.run(main())
