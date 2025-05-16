import os
import shutil
import tempfile
import subprocess
from pathlib import Path
from urllib.parse import urlparse

# Configurable blacklists
FOLDER_BLACKLIST = {'.git', '.vscode', '__pycache__', '.idea', 'node_modules', '.github'}
EXTENSION_BLACKLIST = {'.xml', '.exe', '.bin', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.tar', '.gz', '.pdf'}
FILE_BLACKLIST = {'LICENSE', '__init__.py'}

# Destination base folder
os.makedirs(os.path.expanduser('~/Documents/Flattened'), exist_ok=True)
DEST_BASE = os.path.expanduser('~/Documents/Flattened')

def clone_repo(repo_url):
    repo_name = urlparse(repo_url).path.strip('/').split('/')[-1].replace('.git', '')
    temp_dir = tempfile.mkdtemp()
    dest_dir = os.path.join(DEST_BASE, repo_name)
    print(f"Cloning {repo_url} to {temp_dir}...")

    try:
        subprocess.run(['git', 'clone', '--depth', '1', repo_url, temp_dir], check=True)
    except subprocess.CalledProcessError:
        print(f"Error cloning {repo_url}")
        return

    os.makedirs(dest_dir, exist_ok=True)
    process_repo_files(temp_dir, dest_dir, repo_name)
    shutil.rmtree(temp_dir)

def process_repo_files(source_root, dest_root, repo_name):
    for root, dirs, files in os.walk(source_root):
        # Remove blacklisted folders from traversal
        dirs[:] = [d for d in dirs if d not in FOLDER_BLACKLIST]

        for file in files:
            file_path = Path(root) / file
            rel_path = file_path.relative_to(source_root)

            # Skip file if its extension is blacklisted
            if file_path.suffix.lower() in EXTENSION_BLACKLIST:
                continue
            
            if file in FILE_BLACKLIST:
                continue
            
            # Skips empty files
            if file_path.stat().st_size == 0:
                continue

            # Build new flat filename
            flat_parts = [repo_name] + list(rel_path.with_suffix('').parts)
            new_filename = ".".join(flat_parts) + file_path.suffix + ".txt"
            new_file_path = os.path.join(dest_root, new_filename)

            try:
                with open(file_path, 'r', errors='ignore') as f_in, open(new_file_path, 'w') as f_out:
                    f_out.write(f_in.read())
            except Exception as e:
                print(f"Skipping file {file_path}: {e}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Flatten GitHub repos into .txt files for LLM ingestion.")
    parser.add_argument("urls", nargs="+", help="One or more GitHub repo URLs.")
    args = parser.parse_args()

    for url in args.urls:
        clone_repo(url)

if __name__ == "__main__":
    main()

