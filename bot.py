import asyncio
from playwright.async_api import async_playwright
import random
import time
import os
import re

def extraer_proxies():
    nombre_archivo = "Webshare 10 proxies.txt"
    lista_final = []
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r") as f:
            contenido = f.read()
            # Detecta formato ip:puerto:user:pass O user:pass@ip:puerto
            patron = re.compile(r'(\d+\.\d+\.\d+\.\d+):(\d+):([^:\s]+):([^:\s]+)')
            lineas = patron.findall(contenido)
            if not lineas:
                patron_alt = re.compile(r'([^:\s]+):([^@\s]+)@(\d+\.\d+\.\d+\.\d+):(\d+)')
                lineas_alt = patron_alt.findall(contenido)
                for user, pw, ip, port in lineas_alt:
                    lista_final.append({"server": f"socks5://{ip}:{port}", "user": user, "pass": pw})
            else:
                for ip, port, user, pw in lineas:
                    lista_final.append({"server": f"socks5://{ip}:{port}", "user": user, "pass": pw})
    
    random.shuffle(lista_final)
    print(f"[*] Proxies cargados: {len(lista_final)}")
    return lista_final

async def saltar_ouo(page, url):
    print(f"[*] Navegando a: {url}")
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=80000)
        for i in range(30):
            await asyncio.sleep(15) 
            url_act = page.url
            print(f"[*] Paso {i+1} - URL: {url_act}")

            if "hotmart" in url_act:
                print("[!!!] ¡EXITO TOTAL! Llegamos a Hotmart.")
                return True

            if "ouo.press" in url_act:
                print("[!] Detectado .press. Volviendo atrás...")
                await page.go_back()
                continue

            try:
                # Clic en Get Link
                btn = await page.query_selector("#btn-main")
                if btn:
                    print("[+] Clic en botón")
                    await page.evaluate("document.getElementById('btn-main').click();")
                    continue
                # Enviar Formulario
                form = await page.query_selector("#form-captcha")
                if form:
                    print("[+] Enviando formulario")
                    await page.evaluate("document.getElementById('form-captcha').submit();")
                    continue
            except: pass
    except Exception as e:
        print(f"[!] Error: {e}")

async def main():
    proxies = extraer_proxies()
    if not proxies:
        print("[X] Sin proxies. Revisa Webshare 10 proxies.txt")
        return

    async with async_playwright() as p:
        # Usar los primeros 10 proxies (uno por sesión)
        for i, datos in enumerate(proxies[:10]):
            print(f"\n--- Sesión {i+1} ---")
            try:
                browser = await p.chromium.launch(headless=True, proxy={
                    "server": datos["server"],
                    "username": datos["user"],
                    "password": datos["pass"]
                })
                context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
                await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                page = await context.new_page()
                await saltar_ouo(page, "https://ouo.io")
                await browser.close()
            except: continue

if __name__ == "__main__":
    asyncio.run(main())
