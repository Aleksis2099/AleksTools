import socket
import sys
import os
import argparse
import threading

# --- Argumentos CLI ---
parser = argparse.ArgumentParser(description="Subdomain Enumerator by AleksLabs")
parser.add_argument("dominio", help="Dominio objetivo (ej: example.com)")
parser.add_argument("-w", "--wordlist", required=True, help="Ruta de la wordlist")
parser.add_argument("-t", "--threads", type=int, default=50, help="Número de threads (default: 50)")
args = parser.parse_args()

dom = args.dominio
wl = args.wordlist
max_threads = args.threads

# --- Bienvenida ---
print("Bienvenido al enumerador de subdominios de AleksLabs.dev")
print(f"[*] Target:   {dom}")
print(f"[*] Wordlist: {wl}")
print(f"[*] Threads:  {max_threads}")
print(" ")

# --- Validar dominio ---
try:
    ip = socket.gethostbyname(dom)
    print(f"[+] Dominio válido → {ip}")
except socket.gaierror:
    print("[-] No se encontró el dominio, pruebe con otro")
    sys.exit()

# --- Validar wordlist ---
if not os.path.exists(wl):
    print("[-] Wordlist no encontrada, verifique la ruta")
    sys.exit()

# --- Variables compartidas entre threads ---
encontrados = 0
probados = 0
lock = threading.Lock()

# --- Función que corre cada thread ---
def probar_subdominio(subd):
    global encontrados, probados
    try:
        ip = socket.gethostbyname(subd)
        with lock:
            encontrados += 1
            probados += 1
            print(f"[+] {subd} ENCONTRADO → {ip}")
    except socket.gaierror:
        with lock:
            probados += 1

# --- Escaneo con threading ---
print(f"\n[*] Escaneando {dom}...\n")

threads = []
semaforo = threading.Semaphore(max_threads)

def worker(subd):
    with semaforo:
        probar_subdominio(subd)

with open(wl, "r") as f:
    for linea in f:
        palabra = linea.strip()
        # ✅ Fix UnicodeError — aquí es donde va la validación
        if not palabra or len(palabra) > 63:
            continue
        subd = palabra + "." + dom
        t = threading.Thread(target=worker, args=(subd,))
        threads.append(t)
        t.start()

# Esperar que terminen todos
for t in threads:
    t.join()

# --- Resumen ---
print("\n" + "=" * 70)
print(f"  Se encontraron {encontrados} subdominios de {probados} probados.")
print("  Gracias por usar el escaneador de subdominios de AleksLabs")
print("=" * 70)
