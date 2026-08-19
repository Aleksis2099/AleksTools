# 🔧 AleksTools

Herramientas de **reconocimiento y pentesting** desarrolladas en Python y Bash por **Alexis (Aleksis2099)**, estudiante de ciberseguridad y cazador de bug bounty.

## 📋 Contenido

| Herramienta | Lenguaje | Descripción |
|-------------|----------|-------------|
| `subenum.py` | Python | Enumerador de subdominios con threading (50+ hosts/seg) |
| `dns_resolver.py` | Python | Consulta 9 tipos de registros DNS (A, MX, NS, TXT, AAAA, CNAME, SOA, SRV, CAA) |
| `http_header_scanner.py` | Python | Análisis de headers HTTP, cookies y tecnologías web |
| `port_scanner.py` | Python | Escáner de puertos con captura de banners |
| `dir_scanner.py` | Python | Fuerza bruta de directorios y rutas web |
| `recon.sh` | Bash | Script de automatización de reconocimiento completo |

## 🚀 Uso

### Subdomain Enumerator
```bash
python3 subenum.py example.com -w wordlist.txt -t 100
```
- `-w`: ruta de la wordlist (obligatorio)
- `-t`: número de threads (default: 50)

### DNS Resolver
```bash
uv run dns_resolver.py example.com
# o con registros específicos
uv run dns_resolver.py example.com -r A MX TXT
```

### HTTP Header Scanner
```bash
python3 http_header_scanner.py -u example.com
python3 http_header_scanner.py -u example.com google.com -o reporte.txt
```

### Port Scanner
```bash
python3 port_scanner.py scanme.nmap.org
python3 port_scanner.py scanme.nmap.org -p 1 1000 -t 0.5
```

### Directory Scanner
```bash
python3 dir_scanner.py -d example.com -w wordlist.txt
```

### Recon Automatizado (todo en uno)
```bash
./recon.sh example.com wordlist.txt
```

## 🔧 Requisitos

```bash
pip install requests dnspython
# o con uv
uv run --with requests --with dnspython script.py
```

## ⚠️ Aviso Legal

Estas herramientas son **únicamente para propósitos educativos y pruebas autorizadas**. El uso contra sistemas sin permiso explícito es ilegal. Úselas responsablemente.

---

## 👤 Sobre el autor

- 🌐 [alekslabs.dev](https://alekslabs.dev)
- 🔗 Perfil de GitHub: [Aleksis2099](https://github.com/Aleksis2099)
- 🎓 Estudiante de ciberseguridad (SNHU)
- 🏆 TryHackMe: nivel Hacker

Hecho con 💙 y mucha práctica de room.
