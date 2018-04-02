from pathlib import Path
import datetime, shutil, sys, time
import click

vault_root=Path.home() / 'vault_root'
file_vault_db_file=Path(vault_root)/'file_vault.sqlite'
unrecognized_files_root=Path(vault_root)/'unrecognized'



import sqlite3
from sqlite3 import Error

import hashlib
import os
import json
import sys
import tempfile
import base64

# build the database
# def get_database(file_vault_db_file):
files_table = """
CREATE TABLE IF NOT EXISTS 'files' (
    'file_path'  TEXT UNIQUE,
    'sha_256'    INTEGER
);  """


if(not file_vault_db_file.is_file()):
    print("database file {} not found".format(file_vault_db_file))
    sys.exit()

database_connection = None

try:
    database_connection = sqlite3.connect(str(file_vault_db_file))
except Error as e:
    print('error {}'.format(e))
    sys.exit()
database_cursor = database_connection.cursor()
database_cursor.execute(files_table)
database_connection.commit()


# def list_all_tile_site_codes(database_cursor):
#     sql="""select distinct site_code from map_tiles;"""
#     rows=database_cursor.execute(sql).fetchall()
#     ret_val=[]
#     for row in rows:
#         ret_val.append(row[0])
#     return ret_val
# def list_all_tile_drawings(database_cursor):
#     sql="""select distinct id_drawing from map_tiles;"""
#     rows=database_cursor.execute(sql).fetchall()
#     ret_val=[]
#     for row in rows:
#         ret_val.append(row[0])
#     return ret_val










def sha_256(file_path: Path, block_size=65536) -> str:
    # awh todo: replace this with a call out to the openssl Sha 256 command via the shell.
    #           it's a LOT faster that the python implementation
    sha256 = hashlib.sha256()
    with open(str(file_path), 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()


def get_file_for_hash(sha_256:str)->Path:
    sql="select * from files where sha_256='{}';".format(sha_256)
    rows=database_cursor.execute(sql).fetchall()
    ret_val=[]
    for row in rows:
        return Path(row[0])
    return None


def time_stamp() -> str:
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')


def store_in_vault(sha_256:str, file_path:Path, vault_write_path:Path)->bool:
    # filename = "/foo/bar/baz.txt"¨
    #print(str(file_path.absolute()))
    relative_path:Path = Path(str(file_path.absolute())[1:])
    #print(str(relative_path))
    #print(str(unrecognized_files_path.absolute()))
    new_file_location:Path=Path(vault_write_path.absolute())
    
    #print('>>>>>  ' + str(new_file_location))
    new_file_location = new_file_location.joinpath(relative_path)
    #print('>>>>>  ' + str(new_file_location))
    #os.makedirs(os.path.dirname(str(new_file_location.absolute())), exist_ok=True)
    #print(str(new_file_location.parent))
    new_file_location.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy(str(file_path), str(new_file_location))
    update_database(new_file_location)
    return True

def is_file_in_database(file_path:str)->bool:
    return False

def update_database(file_path:Path)->bool:
    # verify that the file is in the vault
    if(not str(file_path.absolute()).startswith(str(vault_root.absolute()))):
        print('attempting to update the database with a file {} not located in {}'.format(file_path.absolute(), vault_root.absolute() ))
        sys.exit()
    sha:str=sha_256(file_path)
    sql="insert into files ('file_path','sha_256') values (?, ?)"

    #INSERT INTO `files`(`file_path`,`sha_256`) VALUES (NULL,NULL);


    database_cursor.execute(sql, (str(file_path.absolute()), sha))
    database_connection.commit()
    return True


def slow_store(file_path: Path, vault_write_path:Path) -> bool:
    #1. sha the file
    #2. check the database for a match
    #2a-1. if no match, copy the file to the vault at a matching path
    #2b-1. if a match exists, re-run the SHA of the matching file in the vault to confirm the match
    #3. return True
    
    sha:str=sha_256(file_path)
    hashed_file:Path = get_file_for_hash(sha)
    if hashed_file is None:
        #file_path.move()
        store_in_vault(sha, file_path, vault_write_path)
    else:
        print('file {} already in vault'.format(file_path))

    #print(sha)
    return True

def slow_move(file_path: Path, vault_write_path:Path) -> bool:
    #1. slow_store the file
    #2. if slow store returned true, delete the file
    #3. return True
    if slow_store(file_path, vault_write_path):
        file_path.unlink()
        return True
    return False

def build_index()->None:
    return
def check_index()->None:
    return




import click

# @click.group()
# def cli():
#     pass



@click.group()
def store_group():
    pass
@click.group()
def move_group():
    pass
@click.group()
def check_index_group():
    pass

@store_group.command("store", )
@click.argument('files', nargs=-1, type=str)
def store(files):
    vault_write_path:Path=Path(vault_root) / unrecognized_files_root / time_stamp().replace(" ", "_").replace("-", "_").replace(":", "_")
    click.echo('storing ...')
    for fp in files:
        file_path=Path(fp)
        slow_store(file_path, vault_write_path)

@move_group.command("move")
@click.argument('files', nargs=-1, type=str)
def move(files):
    vault_write_path:Path=Path(vault_root) / unrecognized_files_root / time_stamp().replace(" ", "_").replace("-", "_").replace(":", "_")
    click.echo('moving ...')
    for fp in files:
        file_path=Path(fp)
        slow_move(file_path, vault_write_path)

@check_index_group.command("check_index")
def check_index():
    click.echo('checking index ...')





# @click.command("move")
# @click.argument('files', nargs=-1, type=str)
# def move(files):
#     click.echo('saving...')


# cli.add_command(save)
# cli.add_command(move)
cli = click.CommandCollection(sources=[store_group, move_group, check_index_group])

if __name__=="__main__":
    #save()
    cli()


#     vault_write_path:Path=Path(vault_root) / unrecognized_files_root / time_stamp().replace(" ", "_").replace("-", "_").replace(":", "_")
#     file_path:Path = None
#     verb:str = sys.argv[1].strip().lower()
#     if verb=="build_index":
#         build_index()

#     elif verb=="check_index":
#         check_index()

#     elif verb=="move":
#         for fp in sys.argv[2:]:
#             file_path=Path(fp)
#             slow_move(file_path, vault_write_path)
#     elif verb=="store":
#         for fp in sys.argv[2:]:
#             file_path=Path(fp)
#             slow_store(file_path, vault_write_path)
#     else:
#         msg="""file_vault build_index (empties the database and rebuilds it)
# file_vault check_index
# file_vault store [file], [file], ...
# file_vault move [file], [file], ...
# """
#         print(msg)
    
