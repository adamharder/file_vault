#


## Storage locations

must export a variable called FILE_VAULT that contains the root of the file vault.

file vault locations:


./file_vault.sqlite
./unrecognized/[timestamps]/mirror_of_orifinal_file_path


links will not be stored


actions:
* `build_index` (empties the database and rebuilds it)
* `check_index` (verifies that all files in the vault are accounted for in the database)
* `store [file]`
* `move [file]`  store the file and erase the source file