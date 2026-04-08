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
            ips = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', contenido)
            print(f"[!] Se encontraron {len(ips)} IPs válidas.")
            return ips
    except Exception as e:
        print(f"[X] Error leyendo proxies.txt: {e}")
    return []

async def saltar_ouo(page, url_objetivo):
    # Forzamos que use el enlace con el código
    print(f"[*] Navegando a destino real: {url_objetivo}")
    
    try:
        # Aumentamos el tiempo de espera por los proxies lentos
        await page.goto(url_objetivo, wait_until="domcontentloaded", timeout=60000)
        
        for i in range(25):
            await asyncio.sleep(15) # Tiempo para que cargue el botón y Cloudflare
            url_actual = page.url
            print(f"[*] Paso {i+1} - URL: {url_actual}")

            if "hotmart" in url_actual:
                print("[!!!] ¡VISTA COMPLETADA! Llegamos a Hotmart.")
                return True

            if "ouo.press" in url_actual:
                print("[!] Trampa detectada. Volviendo atrás...")
                await page.go_back()
                continue

            try:
                # Intentamos Clic o enviar formulario
                btn = await page.query_selector("#btn-main")
                if btn:
                    print("[+] Botón 'Get Link' detectado. Clickeando...")
                    await page.evaluate("document.getElementById('btn-main').click();")
                    continue
                
                form = await page.query_selector("form[id*='captcha']")
                if form:
                    print("[+] Captcha detectado. Enviando formulario...")
                    await page.evaluate("document.getElementById('form-captcha').submit();")
                    continue
            except:
                pass
    except Exception as e:
        print(f"[!] Error de carga: {e}")

async def main():
    proxies = extraer_ips_locales()
    if not proxies:
        print("[X] No hay proxies. Abortando.")
        return

    random.shuffle(proxies)

    async with async_playwright() as p:
        # Probaremos con las primeras 20 IPs de tu lista
        for i in range(min(len(proxies), 20)):
            proxy_actual = proxies[i]
            print(f"\n--- Intento {i+1} - IP: {proxy_actual} ---")
            
            try:
                browser = await p.chromium.launch(
                    headless=True, 
                    proxy={'server': f'http://{proxy_actual}'}
                )
                
                # --- MODO STEALTH (Humanización) ---
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                    viewport={'width': 1920, 'height': 1080}
                )
                
                # Ocultar que es un bot a nivel de sistema
                await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                page = await context.new_page()

                # LEER TU ENLACE DEL ARCHIVO links.txt
                enlace_final = ""
                if os.path.exists("links.txt"):
                    with open("links.txt", "r") as f:
                        enlace_final = f.read().strip()
                
                # Si el archivo está vacío, usa este por defecto
                if not enlace_final:
                    enlace_final = "https://ouo.io"

                await saltar_ouo(page, enlace_final)
                await browser.close()
            except:
                continue

if __name__ == "__main__":
    asyncio.run(main())
