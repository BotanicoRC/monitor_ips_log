import os
import time
from datetime import datetime

# Lista de hosts para monitorar
hosts = ["192.168.0.1", "192.168.0.120", "192.168.0.45"]  
intervalo = 5  # segundos entre cada rodada de pings
logfile = "ping_log.txt"

# Estado de cada host (online/offline)
status_hosts = {host: True for host in hosts}

def ping(host):
    comando = f"ping -n 1 {host}"
    resposta = os.system(comando + " > nul")
    return resposta == 0

def registrar(mensagem):
    with open(logfile, "a", encoding="utf-8") as f:
        f.write(mensagem + "\n")
    print(mensagem)

print("Monitoramento iniciado...\nRoteador : 192.168.0.1\nServidor : 192.168.0.120\nPortaria : 192.168.0.45\n")
while True:
    for host in hosts:
        resultado = ping(host)
        if resultado and not status_hosts[host]:
            hora_retorno = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            registrar(f"[ONLINE] {host} voltou em {hora_retorno}")
            status_hosts[host] = True

        elif not resultado and status_hosts[host]:
            hora_queda = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            registrar(f"[OFFLINE] {host} caiu em {hora_queda}")
            status_hosts[host] = False

    time.sleep(intervalo)
