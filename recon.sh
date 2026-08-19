#!/bin/bash
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo "Uso: ./recon.sh <TARGET> <WORDLIST>"
    echo " "
    echo "Argumentos:"
    echo "  TARGET    Dominio objetivo (ej: example.com)"
    echo "  WORDLIST  Ruta de la wordlist (ej: /usr/share/wordlists/dirb/common.txt)"
    echo " "
    echo "Ejemplo:"
    echo "  ./recon.sh example.com /usr/share/wordlists/dirb/common.txt"
    exit 0
fi
echo "Herramienta de reconocimiento automatica by ALEKSLABS"
echo " "
#Variables
TARGET=$1
WL=$2
#Validación de Variables
if [ -z "$TARGET" ]; then
    echo "[!] No se recibió ningún TARGET"
    echo "USO: ./recon.sh <TARGET> <WORDLIST>"
    exit 1
else
    echo "TARGET recibido"
fi

if [ -z "$WL" ]; then
    echo "[!] No se recibió ninguna WORDLIST"
    echo "USO: ./recon.sh <TARGET> <WORDLIST>"
    exit 1
else
    echo "WORDLIST recibido"
fi
    
#Buscar las herramientas
echo " "
echo "[X] Buscando herramientas necesarias..."
RUTA_DNS=$(find "$HOME" -name "dns_resolver.py" 2>/dev/null | head -1)
RUTA_SUB=$(find "$HOME" -name "subenum.py" 2>/dev/null | head -1)

if [ -z "$RUTA_DNS" ]; then
    echo "[!] No se encontró 'dns_resolver.py' VERIFICAR QUE ESTÉ INSTALADA"
    exit 1
else
    echo "[:D] Se encontró 'dns_resolver.py'"
fi

if [ -z "$RUTA_SUB" ]; then
    echo "[!] No se encontró 'subenum.py' VERIFICAR QUE ESTÉ INSTALADA"
    exit 1
else
    echo "[:D] Se encontró 'subenum.py'"
fi
    
#Creación de carpeta

mkdir -p $TARGET
echo "=== === === === === === === === === ==="
echo "=== Se creo la carpeta para $TARGET ==="
echo "=== === === === === === === === === ==="
echo " "
echo "Escaneando $TARGET"

#Ejecución del DNS_RESOVER
echo " "
echo "[X] Ejecutando DNS_RESOLVER..."
uv run "$RUTA_DNS" $TARGET > $TARGET/dns_resolver.txt
echo " "

#Ejecución del Enumerador de subdominios
echo "[X] Ejecutando SUB_ENUM..."
python3 "$RUTA_SUB" $TARGET -w $WL -t 200 > $TARGET/subenum.txt

# Despedida
echo " "
echo "=== === === === === === === === === ==="
echo "=== Escaneo completado ==="
echo "=== Resultados guardados en: $TARGET/ ==="
echo "=== === === === === === === === === ==="
echo " "
echo "Archivos generados:"
ls $TARGET/
