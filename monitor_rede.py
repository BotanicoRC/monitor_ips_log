import os
import time
from datetime import datetime
import threading

# Configurações
base_ip = "192.168.0."  # altere para sua rede
range_inicio = 1
range_fim = 254
intervalo = 30  # segundos entre cada varredura completa
logfile = "ping_rede_log.txt"

# Dicionário para status de cada host
status_hosts = {}

def ping(ip):
    comando = f"ping -n 1 -w 500 {ip}"  # -w 500 = timeout 500ms
    return os.system(comando + " > nul") == 0

def registrar(mensagem):
    with open(logfile, "a", encoding="utf-8") as f:
        f.write(mensagem + "\n")
    print(mensagem)

def checar_host(ip):
    global status_hosts
    resultado = ping(ip)
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    if resultado and status_hosts.get(ip) == False:
        registrar(f"[ONLINE] {ip} voltou em {agora}")
        status_hosts[ip] = True

    elif not resultado and status_hosts.get(ip, True) == True:
        registrar(f"[OFFLINE] {ip} caiu em {agora}")
        status_hosts[ip] = False

    elif ip not in status_hosts:
        status_hosts[ip] = resultado
        estado = "ONLINE" if resultado else "OFFLINE"
        registrar(f"[{estado}] {ip} detectado em {agora}")

while True:
    threads = []
    for i in range(range_inicio, range_fim + 1):
        ip = base_ip + str(i)
        t = threading.Thread(target=checar_host, args=(ip,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"--- Varredura concluída. Aguardando {intervalo}s ---\n")
    time.sleep(intervalo)
