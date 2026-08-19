import requests
import sys
import argparse

# --- Argumentos CLI ---
parser = argparse.ArgumentParser(
    description="HTTP Header Scanner by AleksLabs — Análisis de headers, cookies y tecnologías",
    epilog="Ejemplo: python3 http_header_scanner.py -u example.com google.com -o reporte.txt"
)
parser.add_argument("-u", "--urls", nargs="+", required=True,
    help="URLs a analizar (una o más)")
parser.add_argument("-o", "--output", default=None,
    help="Archivo donde guardar el reporte (opcional)")
args = parser.parse_args()

urls_input = args.urls
output_file = args.output

# --- Autocompletar protocolo ---
urls = []
for url in urls_input:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    urls.append(url)

# --- Función principal ---
def grab_headers(url):
    try:
        r = requests.get(url, timeout=5)
        lines = []
        lines.append(f"\n[+] URL: {url}")
        lines.append(f"[*] Status: {r.status_code}")

        # Cookies
        lines.append("\n--- Cookies ---")
        if r.cookies:
            for cookie in r.cookies:
                if not cookie.secure:
                    lines.append(f"  [!] Sin flag Secure: {cookie.name}")
                if not getattr(cookie, '_rest', {}).get('HttpOnly'):
                    lines.append(f"  [!] Sin flag HttpOnly: {cookie.name}")
                samesite = getattr(cookie, '_rest', {}).get('SameSite')
                if not samesite:
                    lines.append(f"  [!] Sin SameSite: {cookie.name}")
        else:
            lines.append("  [-] No se detectaron cookies")

        # Headers
        lines.append("\n--- Encabezados ---")
        for key, value in r.headers.items():
            lines.append(f"  {key}: {value}")

        # Tecnologías
        lines.append("\n--- Detección de Tecnologías ---")
        server = r.headers.get('Server', '').lower()
        powered = r.headers.get('X-Powered-By', '').lower()
        if 'apache' in server:
            lines.append("  [+] Apache")
        elif 'nginx' in server:
            lines.append("  [+] Nginx")
        elif 'iis' in server or 'microsoft' in server:
            lines.append("  [+] Microsoft IIS")
        elif 'node' in server or 'express' in server:
            lines.append("  [+] Node.js/Express")
        elif 'php' in powered:
            lines.append("  [+] PHP")
        else:
            lines.append("  [*] Tecnología no identificada")

        # Security headers
        lines.append("\n--- Verificación de Seguridad ---")
        security_headers = [
            'X-Frame-Options', 'Content-Security-Policy',
            'Strict-Transport-Security', 'X-Content-Type-Options',
            'X-XSS-Protection', 'Referrer-Policy'
        ]
        faltantes = []
        for h in security_headers:
            if h in r.headers:
                lines.append(f"  [+] Presente: {h}")
            else:
                lines.append(f"  [-] FALTA: {h}")
                faltantes.append(h)

        lines.append(f"\n--- Resumen ---")
        lines.append(f"  [!] {len(faltantes)} headers de seguridad faltantes" if faltantes else "  [+] Todos los headers presentes")

        return "\n".join(lines)

    except Exception as e:
        return f"[-] Error al analizar {url}: {e}"

# --- Bienvenida ---
print("Bienvenido a 'HTTP_HEADER_SCANNER' by AleksLabs")
print(f"[*] URLs a analizar: {len(urls)}")
print(" ")

# --- Ejecutar y guardar ---
resultados = []
for url in urls:
    resultado = grab_headers(url)
    print(resultado)
    print("=" * 60)
    resultados.append(resultado)

if output_file:
    with open(output_file, "w") as f:
        f.write("\n".join(resultados))
    print(f"\n[+] Reporte guardado en: {output_file}")
