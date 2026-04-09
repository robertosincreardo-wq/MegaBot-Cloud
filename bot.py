import asyncio
from playwright.async_api import async_playwright
import random
import time
import os

# --- DATOS DE ROTACIÓN WEBSHARE (Protocolo SOCKS5) ---
# Cambiamos a SOCKS5 en el puerto 1080
WS_PROXY = "socks5://p.webshare.io:1080"
WS_USER = "inrjymkc-rotate"
WS_PASS = "kyhwkgls9xnq"

async def saltar_ouo(page, url_objetivo):
    print(f"[*] Navegando a: {url_objetivo}")
    try:
        # Aumentamos a 90 segundos para dar tiempo al túnel SOCKS5
        await page.goto(url_objetivo, wait_until="load", timeout=90000)
        
        for i in range(25):
            await asyncio.sleep(15) 
            url_actual = page.url
            print(f"[*] Paso {i+1} - URL: {url_actual}")

            if "hotmart" in url_actual:
                print("[!!!] ¡EXITO TOTAL! Llegamos a Hotmart.")
                return True

            if "ouo.press" in url_actual:
                print("[!] Trampa ouo.press. Volviendo atrás...")
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
        print(f"[!] Error dentro de la navegación: {e}")

async def main():
    async with async_playwright() as p:
        # Haremos 15 intentos. Cada uno tendrá una IP distinta gracias a la rotación.
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

                # Enlace directo
                enlace = "https://ouo.io/8KpMim"
                await saltar_ouo(page, enlace)
                await browser.close()
            except Exception as e:
                print(f"[!] Error al iniciar el túnel SOCKS5: {e}")
                continue

if __name__ == "__main__":
    asyncio.run(main())
