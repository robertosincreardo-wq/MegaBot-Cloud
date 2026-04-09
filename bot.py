import asyncio
from playwright.async_api import async_playwright
import random
import time
import os
import re

# --- CONFIGURACIÓN ---
MAX_PASOS = 30 
TIEMPO_ESPERA = 14 # Un segundo extra para asegurar el contador

def extraer_proxies_maestro():
    """Extrae proxies de cualquier formato (incluyendo comandos curl o listas puras)"""
    lista_final = []
    # Archivos a buscar
    archivos = ["proxies.txt", "Webshare proxies.txt"]
    
    for nombre in archivos:
        if os.path.exists(nombre):
            print(f"[*] Leyendo proxies de: {nombre}")
            with open(nombre, "r") as f:
                contenido = f.read()
                # Patron 1: ip:puerto:user:pass
                p1 = re.findall(r'(\d+\.\d+\.\d+\.\d+):(\d+):([^:\s]+):([^:\s]+)', contenido)
                for ip, port, user, pw in p1:
                    lista_final.append({"server": f"http://{ip}:{port}", "user": user, "pass": pw})
                
                # Patron 2: user:pass@ip:puerto (Como el comando curl que pasaste)
                p2 = re.findall(r'([^:\s"\'@]+):([^@\s"\':]+)@(\d+\.\d+\.\d+\.\d+):(\d+)', contenido)
                for user, pw, ip, port in p2:
                    lista_final.append({"server": f"http://{ip}:{port}", "user": user, "pass": pw})
                    
    # Eliminar duplicados y mezclar
    random.shuffle(lista_final)
    print(f"[*] Sistema cargó {len(lista_final)} IPs únicas.")
    return lista_final

async def saltar_cadena(page, url_inicial):
    print(f"[*] Iniciando navegación: {url_inicial}")
    try:
        # Tiempo de carga inicial generoso
        await page.goto(url_inicial, wait_until="domcontentloaded", timeout=60000)
        
        for paso in range(MAX_PASOS):
            await asyncio.sleep(TIEMPO_ESPERA)
            url_act = page.url
            print(f"[*] Paso {paso+1} - URL actual: {url_act}")

            # DETECTAR SI LLEGAMOS AL DESTINO FINAL
            # Si la URL ya no contiene acortadores conocidos, es que llegamos
            acortadores = ["ouo.io", "ouo.press", "shrink", "shink", "bitly", "xreallcygo", "cloudflare"]
            if not any(x in url_act.lower() for x in acortadores):
                print(f"[!!!] ¡DESTINO ALCANZADO! URL Final: {url_act}")
                return True

            # SALIR DE LA TRAMPA .PRESS
            if "ouo.press" in url_act:
                print("[!] Trampa ouo.press detectada. Retrocediendo...")
                await page.go_back()
                continue

            try:
                # 1. Intentar Clic en botón 'Get Link' o 'Continue'
                btn = await page.query_selector("#btn-main, button:has-text('Get Link'), button:has-text('Continue')")
                if btn:
                    print("[+] Clic en botón detectado.")
                    await page.evaluate("document.getElementById('btn-main').click();")
                    continue
                
                # 2. Intentar Enviar Formulario Captcha
                form = await page.query_selector("#form-captcha, #form-go")
                if form:
                    print("[+] Enviando formulario interno.")
                    await page.evaluate("document.querySelector('form[id*=\"captcha\"], form[id*=\"go\"]').submit();")
                    continue
            except:
                pass
    except Exception as e:
        print(f"[X] Proxy falló o link caído: {e}")
    return False

async def main():
    proxies = extraer_proxies_maestro()
    if not proxies:
        print("[X] No hay proxies en los archivos .txt. Abortando.")
        return

    # Cargar tus links (los 6 o 10 que tengas)
    if os.path.exists("links.txt"):
        with open("links.txt", "r") as f:
            links = [l.strip() for l in f if l.strip()]
    else:
        print("[X] No se encontró links.txt")
        return

    async with async_playwright() as p:
        # En cada ejecución de GitHub, el bot intentará usar todas las IPs que pusiste
        # pero para no exceder los límites de tiempo, procesará 50 por vez.
        for i in range(min(len(proxies), 50)):
            proxy_act = proxies[i]
            # Elegimos uno de tus links al azar en cada intento
            link_act = random.choice(links)
            
            print(f"\n--- SESIÓN {i+1} | IP Proxy: {proxy_act['server']} ---")
            
            browser = None
            try:
                browser = await p.chromium.launch(
                    headless=True,
                    proxy={
                        "server": proxy_act["server"],
                        "username": proxy_act["user"],
                        "password": proxy_act["pass"]
                    }
                )
                
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                    viewport={'width': 1280, 'height': 720}
                )
                # Ocultar huella de bot
                await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                page = await context.new_page()
                await saltar_cadena(page, link_act)
                
            except:
                pass
            finally:
                if browser:
                    await browser.close()
            
            await asyncio.sleep(2) # Pausa entre cambios de IP

if __name__ == "__main__":
    asyncio.run(main())
