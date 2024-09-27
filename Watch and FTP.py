import os
import time
import subprocess
from ftplib import FTP
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configurações de conexão FTP
ftp_host = "ftp.yoursite.com.br"
ftp_user = "youruser"
ftp_password = "yourpass"

# Caminhos locais e remotos
path_to_watch = "your/local/path/here"  # Substitua pelo caminho da pasta a ser monitorada
remote_dir = "/your/remote/path/here"  # Caminho base no servidor FTP

# Funções FTP
def sanitize_path(path):
    """Converte um caminho para o formato Unix (compatível com servidores FTP)."""
    return path.replace("\\", "/")

def file_exists(ftp, remote_path):
    """Verifica se um arquivo ou diretório já existe no servidor FTP."""
    try:
        ftp.size(remote_path)  # Tenta obter o tamanho do arquivo
        return True
    except:
        return False

def ensure_remote_directory_exists(ftp, remote_dir):
    """Garante que o diretório remoto exista no servidor FTP, criando-o se necessário."""
    dirs = remote_dir.split("/")
    path = ""
    for directory in dirs:
        if directory:
            path += f"/{directory}"
            try:
                ftp.cwd(path)
            except:
                ftp.mkd(path)
                print(f"Diretório {path} criado no servidor FTP.")

def upload_file_if_different(ftp, local_path, remote_path):
    """Faz o upload de um arquivo se ele não existir ou for diferente do remoto."""
    local_size = os.path.getsize(local_path)  # Tamanho do arquivo local

    # Garante que o diretório remoto existe
    remote_dir = os.path.dirname(remote_path)
    ensure_remote_directory_exists(ftp, remote_dir)

    if file_exists(ftp, remote_path):
        try:
            remote_size = ftp.size(remote_path)  # Tamanho do arquivo remoto
            #if local_size == remote_size:
            #    print(f"Arquivo {remote_path} já existe e é idêntico. Não será feito upload.")
            #    return
        except Exception as e:
            print(f"Não foi possível verificar o tamanho do arquivo remoto: {e}")

    with open(local_path, 'rb') as file:
        ftp.storbinary(f'STOR {remote_path}', file)
        print(f"Upload do arquivo {local_path} para {remote_path} concluído.")

def upload_directory(ftp, local_dir, remote_dir):
    """Faz o upload de todos os arquivos e diretórios de local_dir para remote_dir no servidor FTP."""
    try:
        ftp.cwd(remote_dir)  # Muda para o diretório remoto
    except:
        print(f"Erro ao acessar o diretório remoto {remote_dir}.")
        return
    
    for root, dirs, files in os.walk(local_dir):
        # Ignora o diretório '.git' e seus subdiretórios
        if '.git' in root:
            continue

        for dir_name in dirs:
            # Ignora diretórios '.git'
            if '.git' in dir_name:
                continue
            
            remote_path = sanitize_path(os.path.join(remote_dir, os.path.relpath(os.path.join(root, dir_name), local_dir)))
            try:
                ftp.mkd(remote_path)
            except:
                pass  # Suprime mensagens de erro ao criar diretórios já existentes

        for file_name in files:
            # Ignora arquivos '.git'
            if '.git' in file_name:
                continue
            
            local_path = os.path.join(root, file_name)
            remote_path = sanitize_path(os.path.join(remote_dir, os.path.relpath(local_path, local_dir)))
            upload_file_if_different(ftp, local_path, remote_path)

# Monitoramento de Arquivos
class Watcher:
    def __init__(self, directory_to_watch, ftp, remote_dir):
        self.DIRECTORY_TO_WATCH = directory_to_watch
        self.ftp = ftp
        self.remote_dir = remote_dir
        self.observer = Observer()

    def run(self):
        event_handler = Handler(self.ftp, self.remote_dir, self.DIRECTORY_TO_WATCH)
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        print(f"Monitorando alterações na pasta: {self.DIRECTORY_TO_WATCH}")

        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Monitoramento encerrado.")
        self.observer.join()

class Handler(FileSystemEventHandler):
    def __init__(self, ftp, remote_dir, base_local_dir):
        self.ftp = ftp
        self.remote_dir = remote_dir
        self.base_local_dir = base_local_dir

    def on_any_event(self, event):
        if event.event_type in ('created', 'modified'):
            # Ignora eventos na pasta '.git'
            if '.git' in event.src_path:
                return
            
            # Faz o upload do arquivo ou diretório alterado
            local_path = event.src_path
            # Constrói o caminho remoto corretamente removendo a base local do caminho local completo
            relative_path = os.path.relpath(local_path, self.base_local_dir)
            remote_path = sanitize_path(os.path.join(self.remote_dir, relative_path))

            if os.path.isfile(local_path):
                upload_file_if_different(self.ftp, local_path, remote_path)
            else:
                upload_directory(self.ftp, local_path, remote_path)

if __name__ == "__main__":
    # Conectando ao servidor FTP
    ftp = FTP(ftp_host)
    ftp.login(ftp_user, ftp_password)

    # Inicia o monitoramento e upload
    watcher = Watcher(path_to_watch, ftp, remote_dir)
    watcher.run()

    # Fechando a conexão FTP
    ftp.quit()
