import os
import time
import subprocess
from ftplib import FTP
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Description:
# This script monitors a local directory for changes and uploads files or directories to a remote FTP server.
# It will upload files that are newly created or modified, ensuring that the remote directory structure is properly created if it does not exist.

# FTP connection configurations
ftp_host = "ftp.yoursite.com.br"
ftp_user = "youruser"
ftp_password = "yourpass"

# Local and remote paths
path_to_watch = "your/local/path/here"  # Replace with the path to the folder to monitor
remote_dir = "/your/remote/path/here"  # Base path on the FTP server

# FTP functions
def sanitize_path(path):
    """Converts a path to Unix format (compatible with FTP servers)."""
    return path.replace("\\", "/")

def file_exists(ftp, remote_path):
    """Checks if a file or directory already exists on the FTP server."""
    try:
        ftp.size(remote_path)  # Attempts to get the file size
        return True
    except:
        return False

def ensure_remote_directory_exists(ftp, remote_dir):
    """Ensures the remote directory exists on the FTP server, creating it if necessary."""
    dirs = remote_dir.split("/")
    path = ""
    for directory in dirs:
        if directory:
            path += f"/{directory}"
            try:
                ftp.cwd(path)
            except:
                ftp.mkd(path)
                print(f"Directory {path} created on the FTP server.")

def upload_file_if_different(ftp, local_path, remote_path):
    """Uploads a file if it does not exist or is different from the remote version."""
    local_size = os.path.getsize(local_path)  # Local file size

    # Ensure the remote directory exists
    remote_dir = os.path.dirname(remote_path)
    ensure_remote_directory_exists(ftp, remote_dir)

    if file_exists(ftp, remote_path):
        try:
            remote_size = ftp.size(remote_path)  # Remote file size
            # Uncomment the lines below if you want to skip identical files
            # if local_size == remote_size:
            #     print(f"File {remote_path} already exists and is identical. Skipping upload.")
            #     return
        except Exception as e:
            print(f"Could not check the remote file size: {e}")

    with open(local_path, 'rb') as file:
        ftp.storbinary(f'STOR {remote_path}', file)
        print(f"Upload of file {local_path} to {remote_path} completed.")

def upload_directory(ftp, local_dir, remote_dir):
    """Uploads all files and directories from local_dir to remote_dir on the FTP server."""
    try:
        ftp.cwd(remote_dir)  # Change to the remote directory
    except:
        print(f"Error accessing remote directory {remote_dir}.")
        return
    
    for root, dirs, files in os.walk(local_dir):
        # Skip the '.git' directory and its subdirectories
        if '.git' in root:
            continue

        for dir_name in dirs:
            # Skip '.git' directories
            if '.git' in dir_name:
                continue
            
            remote_path = sanitize_path(os.path.join(remote_dir, os.path.relpath(os.path.join(root, dir_name), local_dir)))
            try:
                ftp.mkd(remote_path)
            except:
                pass  # Suppress errors when creating already existing directories

        for file_name in files:
            # Skip '.git' files
            if '.git' in file_name:
                continue
            
            local_path = os.path.join(root, file_name)
            remote_path = sanitize_path(os.path.join(remote_dir, os.path.relpath(local_path, local_dir)))
            upload_file_if_different(ftp, local_path, remote_path)

# File system monitoring
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
        print(f"Monitoring changes in folder: {self.DIRECTORY_TO_WATCH}")

        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Monitoring stopped.")
        self.observer.join()

class Handler(FileSystemEventHandler):
    def __init__(self, ftp, remote_dir, base_local_dir):
        self.ftp = ftp
        self.remote_dir = remote_dir
        self.base_local_dir = base_local_dir

    def on_any_event(self, event):
        if event.event_type in ('created', 'modified'):
            # Ignore events in the '.git' folder
            if '.git' in event.src_path:
                return
            
            # Upload the modified file or directory
            local_path = event.src_path
            # Construct the remote path correctly by removing the base local directory from the full local path
            relative_path = os.path.relpath(local_path, self.base_local_dir)
            remote_path = sanitize_path(os.path.join(self.remote_dir, relative_path))

            if os.path.isfile(local_path):
                upload_file_if_different(self.ftp, local_path, remote_path)
            else:
                upload_directory(self.ftp, local_path, remote_path)

if __name__ == "__main__":
    # Connect to the FTP server
    ftp = FTP(ftp_host)
    ftp.login(ftp_user, ftp_password)

    # Start the monitoring and uploading process
    watcher = Watcher(path_to_watch, ftp, remote_dir)
    watcher.run()

    # Close the FTP connection
    ftp.quit()
