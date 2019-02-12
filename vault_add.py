from vault_exists import does_hash_exist, does_file_exist
from vault_utils import get_file_hash, vault_folder
import hashlib
from pathlib import Path
import os
import sys
import json

def add_file_to_vault(file_path:Path):
    assert(file_path.exists())
    if not does_file_exist(file_path):
        hash = get_file_hash(file_path)
        metadata = dict(file_path=[str(file_path.absolute())], extension=file_path.suffix.lower())
        print(json.dumps(metadata, indent=2))

if __name__=="__main__":
    file_to_add = Path(sys.argv[1])
    print(add_file_to_vault(file_to_add))