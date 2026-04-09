import asyncio
from playwright.async_api import async_playwright
import random
import time
import os
import re

def extraer_proxies_webshare():
    nombre_archivo = "Webshare 10 proxies.txt"
    lista_final = []
    
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r") as f:
            contenido = f.read()
            # Buscamos el formato: protocolo://usuario:pass@ip:puerto O ip:puerto:user:pass
            # Esta regex es mas potente para capturar lo que copiaste
            patron = re.compile(r'(\d+\.\d+\.\d+\.\d+):(\d+):([^:\s]+):([^:\s]+)')
            lineas = patron.findall(contenido)
            
            if not lineas:
                # Intento 2: Buscar formato con el @ (como el curl que pasaste)
                patron_curl = re.compile(r'([^:\s]+):([^@\s]+)@(\d+\.\d+\.\d+\.\d+):(\d+)')
                lineas_curl = patron_curl.findall(contenido)
                for user, pw, ip, port in lineas_curl:
                    lista_final.append({"server": f"socks5://{ip}:{port}", "user": user, "pass": pw})
            else:
                for ip, port, user, pw in lineas:
                    lista_final.append({"server": f"socks5://{ip}:{port}", "user": user, "pass": pw})
    
    random.shuffle(lista_final)
    print(f"[*] Se cargaron {len(lista_final)} proxies SOCKS5 de Webshare.")
    return lista_final

async def saltar_ouo(page, url_objetivo):
    print(f"[*] Iniciando cadena en: {url_objetivo}")
    try:
        # Cargamos el enlace con tiempo de espera generoso para SOCKS5
        await page.goto(url_objetivo, wait_until="domcontentloaded", timeout=80000)
        
        for i in range(30):
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
                # 1. Botón Get Link
                btn = await page.query_selector("#btn-main")
                if btn:
                    print("[+] Clic en 'Get Link'")
                    await page.evaluate("document.getElementById('btn-main').click();")
                    continue
                
                # 2. Formulario Captcha
                form = await page.query_selector("#form-captcha")
                if form:
                    print("[+] Enviando Formulario")
                    await page.evaluate("document.getElementById('form-captcha').submit();")
                    continue
            except: pass
    except Exception as e:
        print(f"[!] Error de navegación: {e}")

async def main():
    proxies_ws = extraer_proxies_webshare()
    if not proxies_ws:
        print("[X] Revisa tu archivo de proxies. No se detectó el formato IP:PORT:USER:PASS")
        return

    async with async_playwright() as p:
        for i, datos in enumerate(proxies_ws):
            print(f"\n--- SESIÓN {i+1} ---")
            try:
                # SOCKS5 con autenticación inyectada
                browser = await p.chromium.launch(
                    headless=True,
                    proxy={
                        "server": datos["server"],
                        "username": datos["user"],
                        "password": datos["pass"]
                    }
                )
                
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                )
                # Script Stealth para ocultar el bot
                await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                page = await context.new_page()
                await saltar_ouo(page, "https://ouo.io")
                await browser.close()
            except Exception as e:
                print(f"[!] Error: {e}")
                continue

if __name__ == "__main__":
    asyncio.run(main())
