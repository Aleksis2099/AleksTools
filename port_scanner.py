import socket
import sys
import argparse

# --- Argumentos CLI ---
parser = argparse.ArgumentParser(
    description="Port Scanner + Banner Grabber by AleksLabs",
    epilog="Ejemplo: python3 port_scanner.py scanme.nmap.org -p 20 150"
)
parser.add_argument("host", help="Host o IP objetivo (ej: scanme.nmap.org)")
parser.add_argument("-p", "--ports", nargs=2, type=int, metavar=("INICIO", "FIN"),
    default=[20, 150],
    help="Rango de puertos a escanear (default: 20 150)")
parser.add_argument("-t", "--timeout", type=float, default=1.0,
    help="Timeout por puerto en segundos (default: 1.0)")
args = parser.parse_args()

host = args.host
puerto_inicio, puerto_fin = args.ports
timeout = args.timeout

# --- Bienvenida ---
print("Bienvenido a 'PORT_SCANNER' — Escaner de puertos + Banner by AleksLabs")
print(f"[*] Host:    {host}")
print(f"[*] Puertos: {puerto_inicio} - {puerto_fin}")
print(f"[*] Timeout: {timeout}s")
print(" ")

# --- Escaneo ---
def scan_with_banner(host, inicio, fin, timeout):
    for port in range(inicio, fin + 1):
        s = socket.socket()
        s.settimeout(timeout)
        if s.connect_ex((host, port)) == 0:
            try:
                banner = s.recv(1024).decode().strip()
            except:
                banner = "sin banner"
            print(f"[+] {port}/tcp abierto | {banner}")
        s.close()

scan_with_banner(host, puerto_inicio, puerto_fin, timeout)
print("\n[*] Escaneo completado.")
