import asyncio
from playwright.async_api import async_playwright
import random
import time
import os
import re

# --- AJUSTES DE VELOCIDAD PARA EL PAGO ---
MAX_PASOS = 20 # Suficiente para 5 acortadores
TIEMPO_ESPERA = 10 # Bajamos de 14 a 10 segundos
TIMEOUT_CARGA = 30000 # 30 segundos máximo para cargar la web

def extraer_proxies_maestro():
    lista_final = []
    archivos = ["proxies.txt", "Webshare proxies.txt"]
    for nombre in archivos:
        if os.path.exists(nombre):
            with open(nombre, "r") as f:
                contenido = f.read()
                # Detecta ambos formatos (ip:port:user:pass y user:pass@ip:port)
                p1 = re.findall(r'(\d+\.\d+\.\d+\.\d+):(\d+):([^:\s]+):([^:\s]+)', contenido)
                for ip, port, user, pw in p1:
                    lista_final.append({"server": f"http://{ip}:{port}", "user": user, "pass": pw})
                p2 = re.findall(r'([^:\s"\'@]+):([^@\s"\':]+)@(\d+\.\d+\.\d+\.\d+):(\d+)', contenido)
                for user, pw, ip, port in p2:
                    lista_final.append({"server": f"http://{ip}:{port}", "user": user, "pass": pw})
    random.shuffle(lista_final)
    print(f"[*] {len(lista_final)} IPs listas. Iniciando modo ráfaga...")
    return lista_final

async def saltar_cadena(page, url_inicial):
    try:
        # Si el link no carga en 30s, saltamos la IP
        await page.goto(url_inicial, wait_until="domcontentloaded", timeout=TIMEOUT_CARGA)
        
        for paso in range(MAX_PASOS):
            await asyncio.sleep(TIEMPO_ESPERA)
            url_act = page.url
            print(f"   [Paso {paso+1}] -> {url_act[:50]}...")

            # DETECCIÓN DE ÉXITO (Modo agresivo)
            acortadores = ["ouo.io", "ouo.press", "shrink", "shink", "xreallcygo", "cloudflare", "captcha"]
            if not any(x in url_act.lower() for x in acortadores) and "http" in url_act:
                print(f"   [!!!] DESTINO ALCANZADO: {url_act}")
                return True

            if "ouo.press" in url_act:
                await page.go_back()
                continue

            try:
                # Clic rápido por script
                await page.evaluate("""
                    let b = document.getElementById('btn-main') || document.querySelector('button');
                    if(b) b.click();
                    let f = document.getElementById('form-captcha') || document.getElementById('form-go');
                    if(f) f.submit();
                """)
            except: pass
    except:
        print("   [!] IP demasiado lenta. Saltando...")
    return False

async def main():
    proxies = extraer_proxies_maestro()
    if not proxies: return

    if os.path.exists("links.txt"):
        with open("links.txt", "r") as f:
            links = [l.strip() for l in f if l.strip()]
    else: return

    async with async_playwright() as p:
        # Procesamos en tandas de 10 para ver logs rápido
        for i in range(min(len(proxies), 100)):
            proxy_act = proxies[i]
            link_act = random.choice(links)
            
            print(f"\n--- SESIÓN {i+1}/{len(proxies)} | IP: {proxy_act['server']} ---")
            
            browser = None
            try:
                browser = await p.chromium.launch(headless=True, proxy={
                    "server": proxy_act["server"], "username": proxy_act["user"], "password": proxy_act["pass"]
                })
                context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
                page = await context.new_page()
                # Ponemos un tiempo límite por IP para no estancarnos
                await asyncio.wait_for(saltar_cadena(page, link_act), timeout=200) # 3 min max por IP
            except: pass
            finally:
                if browser: await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
