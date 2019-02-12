import hashlib
from pathlib import Path
import os
import sys

def vault_folder()->Path:
    return Path("./vault/archive")

if not vault_folder().is_dir():
    os.makedirs(vault_folder())

def get_file_hash(file_path:Path):
    file_hash = hashlib.sha1()
    sha1 = hashlib.sha1()

    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

