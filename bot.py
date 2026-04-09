import asyncio
from playwright.async_api import async_playwright
import random
import time
import os

# --- DATOS DE WEBSHARE ---
WS_USER = "inrjymkc-rotate"
WS_PASS = "kyhwkgls9xnq"
WS_SERVER = "p.webshare.io:80" 
PROXY_URL = f"http://{WS_USER}:{WS_PASS}@{WS_SERVER}"

async def saltar_ouo(page, link_objetivo):
    print(f"[*] Navegando a: {link_objetivo}")
    try:
        # Espera de carga inicial
        await page.goto(link_objetivo, wait_until="domcontentloaded", timeout=60000)
        
        for i in range(20): # 20 pasos es suficiente
            await asyncio.sleep(12) 
            url_actual = page.url
            print(f"   [Paso {i+1}] URL: {url_actual[:50]}")

            if "ouo" not in url_actual.lower() and "http" in url_actual:
                print(f"[!!!] DESTINO ALCANZADO.")
                return True

            if "ouo.press" in url_actual:
                print("[!] Retrocediendo de trampa...")
                await page.go_back()
                continue

            try:
                # Clic o Submit
                await page.evaluate("""
                    let b = document.getElementById('btn-main');
                    if(b) b.click();
                    let f = document.getElementById('form-captcha');
                    if(f) f.submit();
                """)
            except:
                pass
    except Exception as e:
        print(f"[!] Error en link: {e}")
    return False

async def main():
    async with async_playwright() as p:
        # Bajamos a 15 sesiones para evitar el error EPIPE (Broken Pipe)
        for i in range(15):
            print(f"\n--- SESIÓN {i+1}/15 ---")
            browser = None
            try:
                browser = await p.chromium.launch(
                    headless=True,
                    proxy={"server": PROXY_URL}
                )
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                )
                page = await context.new_page()

                # Link principal
                await saltar_ouo(page, "https://ouo.io")
                
                await browser.close()
            except Exception as e:
                print(f"[X] Sesión fallida: {e}")
                if browser:
                    await browser.close()
            
            # Pausa para que el servidor respire
            await asyncio.sleep(3)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error fatal: {e}")
