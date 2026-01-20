import os
import time
from ftplib import FTP, error_perm
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ============================================================
# CONFIGURAÇÕES
# ============================================================
FTP_HOST = ""
FTP_USER = ""
FTP_PASS = ""
FTP_DIR  = "/public_html/"       # Pasta no servidor
LOCAL_DIR = r"D:\my-folder"  # Pasta local a monitorar

IGNORAR_PASTAS = {".git", "__pycache__"}
IGNORAR_ARQUIVOS = {"index.lock"}

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================
def caminho_ignorado(path):
    partes = path.replace("\\", "/").split("/")
    return (
        any(p in IGNORAR_PASTAS for p in partes) or
        os.path.basename(path) in IGNORAR_ARQUIVOS
    )

# ============================================================
# FUNÇÕES FTP
# ============================================================
def conectar_ftp():
    ftp = FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)
    return ftp


def ftp_mkdirs(ftp, path):
    """
    Cria diretórios recursivamente no FTP (mkdir -p)
    """
    dirs = path.strip("/").split("/")
    current = ""

    for d in dirs:
        current += "/" + d
        try:
            ftp.mkd(current)
        except error_perm:
            pass


def criar_diretorio_remoto(caminho_local):
    if caminho_ignorado(caminho_local):
        return

    ftp = None
    try:
        ftp = conectar_ftp()

        rel_path = os.path.relpath(caminho_local, LOCAL_DIR)
        remote_dir = f"{FTP_DIR}/{rel_path}".replace("\\", "/")

        ftp_mkdirs(ftp, remote_dir)
        print(f"[MKDIR] {rel_path}")

    except Exception as e:
        print(f"[ERRO] ao criar pasta {caminho_local}: {e}")
    finally:
        if ftp:
            ftp.quit()


def enviar_arquivo(caminho_local):
    if caminho_ignorado(caminho_local):
        return

    if not os.path.exists(caminho_local):
        return

    ftp = None
    try:
        ftp = conectar_ftp()

        rel_path = os.path.relpath(caminho_local, LOCAL_DIR)
        remote_path = f"{FTP_DIR}/{rel_path}".replace("\\", "/")
        remote_dir = os.path.dirname(remote_path)

        ftp_mkdirs(ftp, remote_dir)

        print(f"[UPLOAD] {rel_path}")

        with open(caminho_local, "rb") as f:
            ftp.storbinary(f"STOR {remote_path}", f)

    except Exception as e:
        print(f"[ERRO] ao enviar {caminho_local}: {e}")
    finally:
        if ftp:
            ftp.quit()


def deletar_arquivo(caminho_local):
    if caminho_ignorado(caminho_local):
        return

    ftp = None
    try:
        ftp = conectar_ftp()

        rel_path = os.path.relpath(caminho_local, LOCAL_DIR)
        remote_path = f"{FTP_DIR}/{rel_path}".replace("\\", "/")

        print(f"[DELETE] {rel_path}")
        ftp.delete(remote_path)

    except Exception as e:
        print(f"[ERRO] ao deletar {remote_path}: {e}")
    finally:
        if ftp:
            ftp.quit()

# ============================================================
# MONITORAMENTO
# ============================================================
class MonitorHandler(FileSystemEventHandler):

    def on_created(self, event):
        if caminho_ignorado(event.src_path):
            return

        if event.is_directory:
            criar_diretorio_remoto(event.src_path)
        else:
            enviar_arquivo(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            enviar_arquivo(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            """IGNORAR DELETES POR ENQUANTO"""
            #deletar_arquivo(event.src_path)

# ============================================================
# LOOP PRINCIPAL
# ============================================================
if __name__ == "__main__":
    print(f"Monitorando: {LOCAL_DIR}")
    print("Pressione CTRL+C para sair...\n")

    observer = Observer()
    observer.schedule(MonitorHandler(), LOCAL_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()