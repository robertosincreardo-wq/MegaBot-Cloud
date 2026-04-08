import asyncio
from playwright.async_api import async_playwright
import random
import time

# --- MANTÉN TUS PROXIES AQUÍ ---
LISTA_PROXIES = [
    "185.76.240.21:10001",
    "152.32.190.98:3128",
    "182.53.202.208:8080",
    "129.226.81.110:7890",
    "194.102.38.53:80"
]

async def saltar_ouo(page, url):
    print(f"[*] Iniciando cadena: {url}")
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        
        for i in range(25):
            await asyncio.sleep(15)
            url_actual = page.url
            print(f"[*] Paso {i+1} - URL: {url_actual}")

            if "hotmart" in url_actual:
                print("[!!!] ¡EXITO TOTAL! Llegamos a Hotmart.")
                return True

            try:
                # 1. SI ESTAMOS EN OUO.PRESS (Página de dominio/tránsito)
                if "ouo.press" in url_actual:
                    print("[>] Detectado ouo.press. Forzando salto de dominio...")
                    # Intentamos enviar cualquier formulario que esté en esa página
                    await page.evaluate("""
                        let f = document.querySelector('form');
                        if(f) f.submit();
                    """)
                
                # 2. BUSCAR BOTÓN PRINCIPAL (btn-main)
                btn = await page.query_selector("#btn-main")
                if btn:
                    print("[+] Clic en btn-main detectado")
                    await page.evaluate("document.getElementById('btn-main').click();")
                    continue

                # 3. BUSCAR FORMULARIOS DE CAPTCHA O "GO"
                form = await page.query_selector("form[id*='captcha'], form[id*='go'], form[action*='go']")
                if form:
                    print("[+] Enviando formulario de redirección")
                    await page.evaluate("""
                        let f = document.querySelector('form[id*="captcha"], form[id*="go"], form[action*="go"]');
                        f.submit();
                    """)
                    continue

                # 4. CLIC DE EMERGENCIA
                await page.evaluate("""
                    document.querySelectorAll('button, a.btn').forEach(b => {
                        let txt = b.innerText.toLowerCase();
                        if(txt.includes('human') || txt.includes('get') || txt.includes('click') || b.id === 'btn-main') {
                            b.click();
                        }
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
                browser = await p.chromium.launch(
                    headless=True, 
                    proxy={'server': f'http://{proxy_actual}'}
                )
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                )
                page = await context.new_page()
                # Tu link principal
                await saltar_ouo(page, "https://ouo.io")
                await browser.close()
            except:
                continue

if __name__ == "__main__":
    asyncio.run(main())
