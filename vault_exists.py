from vault_utils import get_file_hash, vault_folder
from pathlib import Path
import os
import sys


def does_hash_exist(file_hash:str):
    file_hash=file_hash.strip().lower()
    return (vault_folder()/file_hash[:2]/file_hash).is_file()

def does_file_exist(file_path:Path):
    assert file_path.is_file()
    file_hash = get_file_hash(file_path)
    return does_hash_exist(file_hash)

if __name__=="__main__":
    check_hash = sys.argv[1] == "-h"
    if check_hash:
        file_hash = sys.argv[2].strip().lower()
        print(does_hash_exist(file_hash))
    else:
        print(does_file_exist(Path(sys.argv[1])))