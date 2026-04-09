import asyncio
from playwright.async_api import async_playwright
import random
import time
import os

# --- DATOS DE ROTACIÓN DE WEBSHARE ---
# Usamos el puerto 80 que es el estándar para rotación
WS_PROXY = "http://webshare.io"
WS_USER = "inrjymkc-rotate"
WS_PASS = "kyhwkgls9xnq"

async def saltar_ouo(page, url_objetivo):
    print(f"[*] Navegando a: {url_objetivo}")
    try:
        # Tiempo de carga inicial
        await page.goto(url_objetivo, wait_until="domcontentloaded", timeout=60000)
        
        # 30 pasos para cubrir toda la cadena de 5 acortadores
        for i in range(30):
            await asyncio.sleep(12) 
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
        print(f"[!] Error: {e}")

async def main():
    async with async_playwright() as p:
        # Haremos 20 sesiones. En cada una, Webshare te dará una IP DISTINTA
        for i in range(20):
            print(f"\n--- Sesión {i+1} - Iniciando con IP Rotativa ---")
            
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

                # Tu enlace
                enlace = "https://ouo.io"
                if os.path.exists("links.txt"):
                    with open("links.txt", "r") as f:
                        enlace = f.read().strip() or enlace

                await saltar_ouo(page, enlace)
                await browser.close()
            except Exception as e:
                print(f"[!] Falló la sesión {i+1}: {e}")
                continue

if __name__ == "__main__":
    asyncio.run(main())
