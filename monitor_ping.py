import os
import time
from datetime import datetime

# Configurações
host = "192.168.0.1"   # Altere para o IP ou hostname que deseja monitorar
intervalo = 5          # Segundos entre cada ping
logfile = "ping_log.txt"

def ping(host):
    comando = f"ping -n 1 {host}"  # -n 1 = 1 pacote (no Windows)
    resposta = os.system(comando + " > nul")
    return resposta == 0

def registrar(mensagem):
    with open(logfile, "a", encoding="utf-8") as f:
        f.write(mensagem + "\n")
    print(mensagem)

print(f"Iniciando monitoramento de {host}...")
offline = False

while True:
    if ping(host):
        if offline:
            hora_retorno = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            registrar(f"[ONLINE] Retorno detectado em {hora_retorno}")
            offline = False
    else:
        if not offline:
            hora_queda = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            registrar(f"[OFFLINE] Queda detectada em {hora_queda}")
            offline = True
    
    time.sleep(intervalo)
