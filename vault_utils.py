import hashlib
from pathlib import Path
import os
import sys

def vault_folder()->Path:
    return Path.home()/"vault"/"archive"

if not vault_folder().is_dir():
    os.makedirs(vault_folder())

_file_hashes={}

def get_file_hash(file_path:Path):
    path_str = str(file_path.absolute())
    if not path_str in _file_hashes:
        file_hash = hashlib.sha1()
        sha1 = hashlib.sha1()

        BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                sha1.update(data)
            _file_hashes[path_str]=sha1.hexdigest() 
    return _file_hashes[path_str]

