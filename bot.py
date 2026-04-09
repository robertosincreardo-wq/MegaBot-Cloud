import asyncio
from playwright.async_api import async_playwright
import random
import time
import os

def extraer_proxies_webshare():
    nombre_archivo = "Webshare 10 proxies.txt"
    lista_final = []
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r") as f:
            for linea in f:
                partes = linea.strip().split(":")
                if len(partes) == 4:
                    lista_final.append({
                        "server": f"http://{partes[0]}:{partes[1]}",
                        "user": partes[2],
                        "pass": partes[3]
                    })
    # MEZCLAMOS los proxies para que no se usen siempre en el mismo orden
    random.shuffle(lista_final)
    print(f"[*] Se cargaron {len(lista_final)} proxies de Webshare en orden aleatorio.")
    return lista_final

async def saltar_ouo(page, url_objetivo):
    print(f"[*] Navegando a: {url_objetivo}")
    try:
        await page.goto(url_objetivo, wait_until="domcontentloaded", timeout=60000)
        
        for i in range(30):
            await asyncio.sleep(13) # Un poco más de tiempo para asegurar la vista
            url_actual = page.url
            print(f"[*] Paso {i+1} - URL: {url_actual}")

            if "hotmart" in url_actual:
                print("[!!!] ¡EXITO TOTAL! Vista completada y llegada a Hotmart.")
                return True

            if "ouo.press" in url_actual:
                print("[!] Trampa detectada. Volviendo atrás para resetear IP...")
                await page.go_back()
                continue

            try:
                # Intentamos Clic en el botón principal
                btn = await page.query_selector("#btn-main")
                if btn:
                    print("[+] Clic en 'Get Link'")
                    await page.evaluate("document.getElementById('btn-main').click();")
                    continue
                
                # Intentamos enviar el formulario de Captcha
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
    proxies_ws = extraer_proxies_webshare()
    
    if not proxies_ws:
        print("[X] El archivo de Webshare no existe.")
        return

    async with async_playwright() as p:
        # Probamos cada proxy de tu lista de 10
        for i, datos in enumerate(proxies_ws):
            print(f"\n--- SESIÓN ÚNICA {i+1} - IP: {datos['server']} ---")
            
            try:
                # Creamos una instancia de navegador TOTALMENTE LIMPIA
                browser = await p.chromium.launch(
                    headless=True,
                    proxy={
                        "server": datos["server"],
                        "username": datos["user"],
                        "password": datos["pass"]
                    }
                )
                
                # Fingerprint nueva para cada sesión
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/12" + str(random.randint(0,9)) + ".0.0.0 Safari/537.36"
                )
                page = await context.new_page()

                # Tu link real
                await saltar_ouo(page, "https://ouo.io")
                
                # Cerramos todo para asegurar que la siguiente IP empiece de cero
                await browser.close()
                print(f"[*] Sesión {i+1} finalizada y cookies borradas.")
            except:
                continue

if __name__ == "__main__":
    asyncio.run(main())
