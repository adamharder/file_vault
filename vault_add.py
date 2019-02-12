from vault_exists import does_hash_exist, does_file_exist
from vault_utils import get_file_hash, vault_folder
import hashlib
from pathlib import Path
import os
import sys
import json



def get_file_metadata(file_path:Path):
    return dict(sha1=get_file_hash(file_path), file_path=[str(file_path.absolute())], extension=file_path.suffix.lower(), file_size=os.path.getsize(file_path))

def add_file_to_vault(file_path:Path):
    assert(file_path.exists())
    if not does_file_exist(file_path):
        hash = get_file_hash(file_path)
        metadata = get_file_metadata(file_path)
        print(json.dumps(metadata, indent=2))
        if not (vault_folder()/hash[:2]).is_dir():
            os.makedirs(vault_folder()/hash[:2])
        (vault_folder()/hash[:2]/hash).write_bytes(file_path.read_bytes())
        (vault_folder()/hash[:2]/f"{hash}_metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True))


if __name__=="__main__":
    
    for file_to_add in sys.argv[1:]:
        file_to_add=Path(file_to_add)
        print(add_file_to_vault(file_to_add))