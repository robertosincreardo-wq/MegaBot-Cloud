import asyncio
from playwright.async_api import async_playwright
import random
import time
import requests
import re

def extraer_proxies_directos():
    print("[*] Extrayendo IPs frescas de fuentes públicas...")
    # Usamos fuentes que entregan el texto limpio para no fallar en GitHub
    urls = [
        "https://proxyscrape.com",
        "https://proxy-list.download",
        "https://githubusercontent.com"
    ]
    ips_encontradas = []
    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            # Buscamos el patrón IP:PUERTO
            ips = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)
            ips_encontradas.extend(ips)
        except: continue
    
    # Eliminamos duplicados y mezclamos
    return list(set(ips_encontradas))

async def saltar_ouo(page, url):
    print(f"[*] Navegando a: {url}")
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=45000)
        
        for i in range(25):
            await asyncio.sleep(15)
            url_actual = page.url
            print(f"[*] Paso {i+1} - URL: {url_actual}")

            if "hotmart" in url_actual:
                print("[!!!] ¡VISTA COMPLETADA! Llegamos a Hotmart.")
                return True

            if "ouo.press" in url_actual:
                print("[!] Detectado ouo.press. Aplicando truco de volver atrás...")
                await page.go_back()
                continue

            try:
                # Intentar Clic o Submit según lo que aparezca
                if await page.query_selector("#btn-main"):
                    await page.evaluate("document.getElementById('btn-main').click();")
                    print("[+] Clic en botón")
                elif await page.query_selector("form[id*='captcha'], form[id*='go']"):
                    await page.evaluate("document.querySelector('form[id*=\"captcha\"], form[id*=\"go\"]').submit();")
                    print("[+] Formulario enviado")
            except: pass
    except:
        print("[!] Tiempo agotado para este proxy.")

async def main():
    # El bot busca sus propias IPs al empezar
    proxies = extraer_proxies_directos()
    if not proxies:
        print("[X] No se hallaron proxies. Usando IPs de respaldo...")
        proxies = ["152.32.190.98:3128", "185.76.240.21:10001"]

    random.shuffle(proxies)

    async with async_playwright() as p:
        # Probaremos con 20 proxies frescos en cada ejecución
        for i in range(20):
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
                
                # TU LINK
                await saltar_ouo(page, "https://ouo.io")
                
                await browser.close()
            except: continue

if __name__ == "__main__":
    asyncio.run(main())
