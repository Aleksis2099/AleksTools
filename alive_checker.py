import argparse, requests, threading

print("==========================================")
print("=======ALIVE_CHECKER by ALEKSLABS=========")
print("==========================================")
print(" ")

# Arguments
parser = argparse.ArgumentParser(description="Alive Checker, este script recibe una lista de subdominios y verifica cuales responden con HTTP")
parser.add_argument("-d",type=str,required=True,help="Target Domain")
parser.add_argument("-w",type=str,required=False,help="Wordlist for subdomains")
parser.add_argument("-l",type=str,required=False,help="File with a list with already finded subdomains, example: api.example.com")
parser.add_argument("-t",type=int,required=False, default=20, help="Number of threads in order to make a faster scan")
args = parser.parse_args()

max_threads = args.t
semaforo = threading.Semaphore(max_threads)
lock = threading.Lock()
# Argument comprobation

if not args.d:
    print("[!] You need to specify a target domain (-d), example: example.com")
    exit()
if not args.w and not args.l:
    print("[!] You need a Wordlist (-w) or a list of subdomains (-l)")
    exit()
if args.w and args.l:
    print("[-_-] You are using -l, -w will be ignored")

# Target comprobation
url = (f"http://{args.d}")
try:
    response = requests.get(url, timeout=5, allow_redirects=False)
    if response.status_code < 500:
        print (f"[:D] El target,{args.d} está disponible.")
    else:
        print(f"Respuesta rara de {url}")
except requests.ConnectionError:
    print(f"[!] No se pudo realizar una conexión con {args.d}, intente más tarde.")
    exit()

salida = open(f"alive_{args.d}.txt", "w")

# Principal Function
def comp_url(url):
    try: 
        r = requests.get(url,timeout=3,allow_redirects=False)
        if r.status_code < 500:
            vivo = (f"[+] {url} respondío con el código {r.status_code}")
            print (vivo)
            with lock:
                salida.write(vivo + "\n")
    except requests.exceptions.RequestException:
        pass

# Worker
def worker(url):
    with semaforo:
        comp_url(url)

# Recolect URL's
urls = []
if args.l:
    with open(args.l, "r") as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                for protocol in ["https://","http://"]:
                    urls.append(f"{protocol}{linea}")
else:
    with open(args.w, "r") as wl:
        for linea in wl:
            linea = linea.strip()
            if linea:
                for protocol in ["https://","http://"]:
                    urls.append(f"{protocol}{linea}.{args.d}")

# Create and Launch threads
threads = []
for url in urls:
    t = threading.Thread(target=worker, args=(url,))
    threads.append(t)
    t.start()

#  Wait the threads
for t in threads:
    t.join()

# Close the archive
salida.close()

print(" ")
print("====================================================")
print("==================SCAN COMPLETED====================")
print("====================================================")