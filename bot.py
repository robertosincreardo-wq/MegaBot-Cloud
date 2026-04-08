import asyncio
from playwright.async_api import async_playwright
import random
import time
import re
import os

def extraer_ips_locales():
    print("[*] Leyendo IPs del archivo proxies.txt...")
    try:
        if os.path.exists("proxies.txt"):
            with open("proxies.txt", "r") as f:
                contenido = f.read()
            # Esta línea limpia todo el texto basura y saca solo las IPs
            ips = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', contenido)
            print(f"[!] Se encontraron {len(ips)} IPs válidas en tu archivo.")
            return ips
    except Exception as e:
        print(f"[X] Error leyendo proxies.txt: {e}")
    return []

async def saltar_ouo(page, url):
    # CORRECCIÓN: Aseguramos que el link sea el tuyo completo
    mi_enlace = "https://ouo.io" 
    print(f"[*] Navegando a: {mi_enlace}")
    
    try:
        await page.goto(mi_enlace, wait_until="domcontentloaded", timeout=45000)
        
        for i in range(25):
            await asyncio.sleep(15)
            url_actual = page.url
            print(f"[*] Paso {i+1} - URL: {url_actual}")

            if "hotmart" in url_actual:
                print("[!!!] ¡VISTA COMPLETADA! Llegamos a Hotmart.")
                return True

            if "ouo.press" in url_actual:
                print("[!] Detectado ouo.press. Volviendo atrás...")
                await page.go_back()
                continue

            try:
                # Intentar Clic o Submit
                if await page.query_selector("#btn-main"):
                    await page.evaluate("document.getElementById('btn-main').click();")
                    print("[+] Clic en botón")
                elif await page.query_selector("form[id*='captcha'], form[id*='go']"):
                    await page.evaluate("document.querySelector('form[id*=\"captcha\"], form[id*=\"go\"]').submit();")
                    print("[+] Formulario enviado")
            except: pass
    except:
        print("[!] Tiempo agotado o error de carga.")

async def main():
    proxies = extraer_ips_locales()
    
    if not proxies:
        print("[X] No hay proxies en proxies.txt. Abortando.")
        return

    random.shuffle(proxies)

    async with async_playwright() as p:
        # Probaremos con las IPs que encontraste (hasta 20)
        max_intentos = min(len(proxies), 20)
        for i in range(max_intentos):
            proxy_actual = proxies[i]
            print(f"\n--- Intento {i+1} - IP: {proxy_actual} ---")
            
            try:
                browser = await p.chromium.launch(
                    headless=True, 
                    proxy={'server': f'http://{proxy_actual}'}
                )
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                )
                page = await context.new_page()
                
                await saltar_ouo(page, "")
                await browser.close()
            except: 
                print("[!] Error de conexión con este proxy.")
                continue

if __name__ == "__main__":
    asyncio.run(main())
