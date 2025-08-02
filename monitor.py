import time
import threading
import subprocess
from datetime import datetime
import requests
import base64
from PIL import Image, ImageDraw
import pystray

# Configurações
hosts = ["192.168.0.1", "192.168.0.120", "192.168.0.45"]
intervalo = 5
logfile = "ping_log.txt"

# GitHub
GITHUB_USER = "BotanicoRC"
REPO = "monitor_ips_log"
FILE_PATH = "ping_log.txt"
TOKEN = "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"

status_hosts = {host: True for host in hosts}
executando = True
icone = None  # será definido depois

def salvar_no_github():
    url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO}/contents/{FILE_PATH}"
    try:
        with open(logfile, "rb") as f:
            conteudo = f.read()
        conteudo_b64 = base64.b64encode(conteudo).decode("utf-8")
        r = requests.get(url, headers={"Authorization": f"token {TOKEN}"})
        sha = r.json()["sha"] if r.status_code == 200 else None
        data = {
            "message": f"Atualização {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            "content": conteudo_b64,
            "branch": "main"
        }
        if sha:
            data["sha"] = sha
        requests.put(url, json=data, headers={"Authorization": f"token {TOKEN}"})
    except:
        pass  # ignora erro para não travar

def ping(host):
    try:
        comando = ["ping", "-n", "1", host]
        resultado = subprocess.run(
            comando,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW  # impede CMD de abrir
        )
        return resultado.returncode == 0
    except Exception:
        return False

def registrar(mensagem):
    with open(logfile, "a", encoding="utf-8") as f:
        f.write(mensagem + "\n")
    salvar_no_github()

def monitorar():
    global icone
    while executando:
        for host in hosts:
            resultado = ping(host)
            if resultado and not status_hosts[host]:
                registrar(f"[ONLINE] {host} voltou em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                status_hosts[host] = True
            elif not resultado and status_hosts[host]:
                registrar(f"[OFFLINE] {host} caiu em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                status_hosts[host] = False
        if icone:
            atualizar_icone(icone)  # atualiza cor do ícone
        time.sleep(intervalo)

# Função para criar ícone
def criar_icone(cor="green"):
    img = Image.new('RGB', (64, 64), color="white")
    d = ImageDraw.Draw(img)
    d.ellipse((8, 8, 56, 56), fill=cor)
    return img

def atualizar_icone(icone):
    cor = "green" if all(status_hosts.values()) else "red"
    icone.icon = criar_icone(cor)
    icone.visible = True

# Encerrar monitoramento
def sair(icon, item):
    global executando
    executando = False
    icon.stop()

# Início
if __name__ == "__main__":
    thread = threading.Thread(target=monitorar, daemon=True)
    thread.start()

    menu = pystray.Menu(pystray.MenuItem("Sair", sair))
    icone = pystray.Icon("Monitor Ping", criar_icone(), menu=menu)
    icone.run()
