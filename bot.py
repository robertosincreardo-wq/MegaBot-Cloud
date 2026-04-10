import os

# Verificamos si hay archivos cargados para leer los enlaces y los proxies
files = os.listdir('.')
print(f"Archivos disponibles: {files}")

# Intentamos leer 'Webshare 10 proxies.txt' y 'links.txt' si existen
def read_file(name):
    try:
        with open(name, 'r') as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return None

proxies = read_file('Webshare 10 proxies.txt')
links = read_file('links.txt')

print(f"Proxies encontrados: {len(proxies) if proxies else 0}")
print(f"Links encontrados: {len(links) if links else 0}")
