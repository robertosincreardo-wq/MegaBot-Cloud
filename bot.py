import asyncio
from playwright.async_api import async_playwright
import random
import time

# Usa proxies frescos. El 152.32.190.98 del Intento 4 fue el mejor.
LISTA_PROXIES = [
    "152.32.190.98:3128", 
    "43.159.28.153:23531",
    "152.32.148.118:3128",
    "103.155.22.210:3128",
    "159.89.49.172:3128"
]

async def saltar_ouo(page, url):
    print(f"[*] Iniciando: {url}")
    try:
        # Esperar a que cargue la página inicial
        await page.goto(url, wait_until="load", timeout=90000)
        
        # Intentaremos hasta 20 veces para cubrir las 5 capas de tu cadena
        for i in range(20):
            await asyncio.sleep(12) # Espera obligatoria para el contador de Ouo
            url_actual = page.url
            print(f"[*] Capa {i+1} - URL: {url_actual}")

            if "hotmart" in url_actual:
                print("[!!!] ¡EXITO TOTAL! Llegamos a Hotmart.")
                return True

            # LÓGICA DE CLIC SEGÚN LA PÁGINA
            try:
                # Si estamos en la etapa de "Get Link" (URL contiene /go/ o /xreallcygo/)
                if "/go/" in url_actual or "/xreallcygo/" in url_actual or await page.query_selector("#btn-main"):
                    print("[+] Detectado botón 'Get Link'. Cliqueando...")
                    # Forzamos el clic varias veces para asegurar
                    await page.evaluate("document.getElementById('btn-main').click();")
                    await asyncio.sleep(2)
                
                # Si estamos en la etapa de Captcha (form-captcha)
                elif await page.query_selector("#form-captcha"):
                    print("[+] Detectada etapa de Captcha. Enviando formulario...")
                    await page.evaluate("document.getElementById('form-captcha').submit();")
                
                else:
                    # Si no ve nada, intenta cliquear el botón principal por si acaso
                    print("[?] Intentando clic de emergencia...")
                    await page.evaluate("if(document.getElementById('btn-main')) document.getElementById('btn-main').click();")
            except:
                pass
                
    except Exception as e:
        print(f"[!] Error: {e}")

async def main():
    proxies = LISTA_PROXIES
    random.shuffle(proxies)

    async with async_playwright() as p:
        for i, proxy_actual in enumerate(proxies[:5]):
            print(f"\n--- Intento {i+1} - Proxy: {proxy_actual} ---")
            try:
                # Iniciamos navegador con el proxy
                browser = await p.chromium.launch(headless=True, proxy={'server': f'http://{proxy_actual}'})
                context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
                page = await context.new_page()

                # Tu link principal
                await saltar_ouo(page, "https://ouo.io/8KpMim")
                
                await browser.close()
            except:
                continue

if __name__ == "__main__":
    asyncio.run(main())
