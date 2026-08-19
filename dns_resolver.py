# /// script
# dependencies = ["dnspython"]
# ///
import dns.resolver
import sys
import argparse

# --- Argumentos CLI ---
parser = argparse.ArgumentParser(
    description="DNS Resolver by AleksLabs — Enumeración de registros DNS",
    epilog="Ejemplo: uv run dns_resolver.py example.com"
)
parser.add_argument("dominio", help="Dominio objetivo (ej: example.com)")
parser.add_argument("-r", "--registros", nargs="+",
    default=["A", "MX", "NS", "TXT", "AAAA", "CNAME", "SOA", "SRV", "CAA"],
    help="Registros a consultar (default: todos)")
args = parser.parse_args()

dom = args.dominio
registros = args.registros

# --- Bienvenida ---
print("Bienvenido a 'DNS_RESOLVER' — Enumeración de registros DNS by AleksLabs")
print(f"[*] Target:    {dom}")
print(f"[*] Registros: {', '.join(registros)}")
print(" ")

# --- Código Principal ---
for reg in registros:
    try:
        respuesta = dns.resolver.resolve(dom, reg)
        for registro in respuesta:
            print(f"[{reg}] {registro}")
    except dns.resolver.NoAnswer:
        print(f"[-] No se encontró registro {reg}")
    except dns.resolver.LifetimeTimeout:
        print(f"[!] Timeout al consultar registro {reg}")
    except dns.resolver.NXDOMAIN:
        print(f"[-] Dominio no encontrado: {dom}")
        sys.exit()
    except dns.exception.DNSException as e:
        print(f"[!] Error DNS en {reg}: {e}")
