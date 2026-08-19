import argparse
import requests

parser = argparse.ArgumentParser(description="DIR_SCANNER by ALEKSLABS")
parser.add_argument("-d", required=True, help="Dominio objetivo")
parser.add_argument("-w", required=True, help="Wordlist")
args = parser.parse_args()

print("============================================")
print("=========DIR_SCANNER by ALEKSLABS===========")
print("============================================")
print("")

encontrados = 0
with open(args.w, "r") as f:
    for linea in f:
        ruta = linea.strip()
        if not ruta:
            continue
        url = f"https://{args.d}/{ruta}"

        try:
            r = requests.get(url, timeout=5)
        except requests.exceptions.RequestException:
            print(f"[!] Error al conectar con {url}")
            continue

        if r.status_code != 404:
            print(f"[+] [{r.status_code}] /{ruta}")
            encontrados += 1

print(f"\n[*] Escaneo completado. {encontrados} rutas encontradas.")
