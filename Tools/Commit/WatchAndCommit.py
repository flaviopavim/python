# This script monitors a directory for file changes and automatically commits the changes to a Git repository.
# It uses the 'watchdog' library to monitor file system events and the 'gitpython' library to interact with the Git repository.
# When a file is modified, it is automatically added to the staging area and committed with a message indicating the modified file.
# The script runs continuously, monitoring the directory for any changes.

import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import git

class GitCommitHandler(FileSystemEventHandler):
    def __init__(self, repo_path):
        """
        Initializes the GitCommitHandler with the given repository path.
        
        :param repo_path: Path to the Git repository to monitor and commit changes to.
        """
        self.repo_path = repo_path
        # Initialize the git repository object using GitPython
        self.repo = git.Repo(repo_path)

    def on_modified(self, event):
        """
        This method is called when a file is modified in the monitored directory.
        
        :param event: The event containing information about the modified file.
        """
        if event.is_directory:
            return  # Ignore directory changes

        # Print the modified file path
        print(f'File modified: {event.src_path}')
        # Commit the changes made to the file
        self.commit_changes(event.src_path)

    def commit_changes(self, file_path):
        """
        Adds the modified file to the Git staging area and commits the changes.
        
        :param file_path: The path of the modified file to commit.
        """
        # Add the modified file to the staging area
        self.repo.git.add(file_path)
        
        # Create a commit with a message indicating the modified file
        self.repo.git.commit(m=f'Automated commit for {file_path}')
        print(f'Commit performed for file: {file_path}')
        
        # Uncomment the next line to push changes to a remote repository
        # self.repo.git.push()

def monitor_directory(directory):
    """
    Monitors the given directory for file changes and commits modifications.
    
    :param directory: Path to the directory to monitor.
    """
    event_handler = GitCommitHandler(directory)
    observer = Observer()
    # Schedule the event handler to monitor the directory for changes
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    
    try:
        # Keep the observer running to monitor file changes
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Stop the observer when the script is interrupted
        observer.stop()
    observer.join()

if __name__ == "__main__":
    # Replace with the path to your Git repository
    repo_path = '/path/to/your/repo'
    # Start monitoring the repository for changes
    monitor_directory(repo_path)
