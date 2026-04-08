import asyncio
from playwright.async_api import async_playwright
import random
import time

# --- MANTÉN TUS PROXIES AQUÍ ---
LISTA_PROXIES = [
    "185.76.240.21:10001", # El que funcionó
    "152.32.190.98:3128",
    " 207.180.254.198:8080",
    "197.221.249.196:80",
    "203.192.217.6:8080"
]

async def saltar_ouo(page, url):
    print(f"[*] Iniciando: {url}")
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        
        for i in range(25):
            await asyncio.sleep(12) 
            url_actual = page.url
            print(f"[*] Paso {i+1} - URL: {url_actual}")

            if "hotmart" in url_actual:
                print("[!!!] ¡ÉXITO TOTAL EN HOTMART!")
                return True

            try:
                # 1. Intentar cliquear por ID (El método rápido)
                if await page.query_selector("#btn-main"):
                    await page.evaluate("document.getElementById('btn-main').click();")
                    print("[+] Clic por ID btn-main")
                
                # 2. Si falla, intentar enviar cualquier formulario que parezca captcha
                elif await page.query_selector("form"):
                    await page.evaluate("""
                        let f = document.querySelector('form[action*="go"], form[action*="captcha"]');
                        if(f) f.submit();
                    """)
                    print("[+] Formulario enviado por lógica de acción")

                # 3. CLIC DE EMERGENCIA (Busca cualquier botón que sea el de 'Next' o 'Get Link')
                else:
                    print("[?] Buscando botones ocultos...")
                    await page.evaluate("""
                        document.querySelectorAll('button').forEach(b => {
                            if(b.innerText.includes('human') || b.innerText.includes('Get') || b.id == 'btn-main') b.click();
                        });
                    """)
            except:
                pass
                
    except Exception as e:
        print(f"[!] Error: {e}")

async def main():
    proxies = LISTA_PROXIES
    random.shuffle(proxies)

    async with async_playwright() as p:
        for i, proxy_actual in enumerate(proxies):
            print(f"\n--- Intento {i+1} - Proxy: {proxy_actual} ---")
            try:
                browser = await p.chromium.launch(headless=True, proxy={'server': f'http://{proxy_actual}'})
                # Cambiamos a User-Agent de Windows para más estabilidad
                context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
                page = await context.new_page()

                await saltar_ouo(page, "https://ouo.io/8KpMim")
                await browser.close()
            except:
                continue

if __name__ == "__main__":
    asyncio.run(main())
                    print("[+] Detectado botón 'Get Link'. Ejecutando clic...")
                    await page.evaluate("document.getElementById('btn-main').click();")
                    continue

                # Caso B: Etapa de Captcha Invisible (form-captcha)
                form_exists = await page.query_selector("#form-captcha")
                if form_exists:
                    print("[+] Detectada etapa de Captcha. Enviando formulario...")
                    await page.evaluate("document.getElementById('form-captcha').submit();")
                    continue
                
                # Si no detecta nada pero sigue en Ouo, intentamos un clic de emergencia
                if "ouo.io" in url_actual:
                    print("[?] Reintentando forzar botones internos...")
                    await page.evaluate("if(document.getElementById('btn-main')) document.getElementById('btn-main').click();")
                    await page.evaluate("if(document.getElementById('form-captcha')) document.getElementById('form-captcha').submit();")

            except Exception:
                pass
                
    except Exception as e:
        print(f"[!] Error de conexión o tiempo agotado: {e}")

async def main():
    # Mezclamos tus proxies para rotar
    proxies = LISTA_PROXIES
    random.shuffle(proxies)

    async with async_playwright() as p:
        for i, proxy_actual in enumerate(proxies):
            print(f"\n--- Intento {i+1} con tu Proxy: {proxy_actual} ---")
            
            try:
                # Lanzamos el navegador con tu proxy
                browser = await p.chromium.launch(
                    headless=True, 
                    proxy={'server': f'http://{proxy_actual}'}
                )
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                )
                page = await context.new_page()

                # Leemos tu link principal del archivo
                try:
                    with open("links.txt", "r") as f:
                        links = [l.strip() for l in f if l.strip()]
                except:
                    links = ["https://ouo.io"]

                for link in links:
                    await saltar_ouo(page, link)
                
                await browser.close()
            except Exception as e:
                print(f"[!] Falló la conexión con {proxy_actual}")
                continue

if __name__ == "__main__":
    asyncio.run(main())
