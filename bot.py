import asyncio
from playwright.async_api import async_playwright
import random
import time
import os
import re

def extraer_proxies_webshare():
    # Buscamos el archivo que descargaste
    nombre_archivo = "Webshare 10 proxies.txt"
    lista_final = []
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r") as f:
            for linea in f:
                partes = linea.strip().split(":")
                if len(partes) == 4:
                    # Guardamos los datos ordenados
                    lista_final.append({
                        "server": f"http://{partes[0]}:{partes[1]}",
                        "user": partes[2],
                        "pass": partes[3]
                    })
    print(f"[*] Se cargaron {len(lista_final)} proxies de Webshare.")
    return lista_final

async def saltar_ouo(page, url_objetivo):
    print(f"[*] Navegando a: {url_objetivo}")
    try:
        # Cargamos el link principal
        await page.goto(url_objetivo, wait_until="domcontentloaded", timeout=60000)
        
        # 30 pasos para cubrir toda la cadena de 5 acortadores
        for i in range(30):
            await asyncio.sleep(12) 
            url_actual = page.url
            print(f"[*] Paso {i+1} - URL: {url_actual}")

            if "hotmart" in url_actual:
                print("[!!!] ¡ÉXITO TOTAL! Llegamos a Hotmart.")
                return True

            # Si el proxy falla y sale error de Chrome
            if "chrome-error" in url_actual or "chromewebdata" in url_actual:
                print("[!] Error de conexión. Reintentando...")
                await page.go_back()
                continue

            if "ouo.press" in url_actual:
                print("[!] Detectado ouo.press. Volviendo atrás...")
                await page.go_back()
                continue

            try:
                # Prioridad 1: Botón Get Link
                btn = await page.query_selector("#btn-main")
                if btn:
                    print("[+] Clic en 'Get Link'")
                    await page.evaluate("document.getElementById('btn-main').click();")
                    continue
                
                # Prioridad 2: Formulario Captcha (Turnstile invisible)
                form = await page.query_selector("#form-captcha")
                if form:
                    print("[+] Enviando Formulario Captcha")
                    await page.evaluate("document.getElementById('form-captcha').submit();")
                    continue
            except:
                pass
    except Exception as e:
        print(f"[!] Error de navegación: {e}")

async def main():
    proxies_ws = extraer_proxies_webshare()
    
    if not proxies_ws:
        print("[X] No se encontró el archivo de Webshare o está vacío.")
        return

    async with async_playwright() as p:
        # Vamos a usar cada uno de los 10 proxies en orden
        for i, datos in enumerate(proxies_ws):
            print(f"\n--- Intento {i+1} con Proxy Webshare: {datos['server']} ---")
            
            try:
                # Configuración con Autenticación (Usuario y Pass)
                browser = await p.chromium.launch(
                    headless=True,
                    proxy={
                        "server": datos["server"],
                        "username": datos["user"],
                        "password": datos["pass"]
                    }
                )
                
                # Stealth: Humanizar el navegador
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
                print(f"[!] Error con este proxy: {e}")
                continue

if __name__ == "__main__":
    asyncio.run(main())
