from connection import ServerConnection
from modinfo import ModInfo
from pathlib import Path
from helpers import create_list_of_installed_mods,run_ps_script
from urllib.parse import urlencode
from sys import argv

username = "KandoLP"
token = "2e85a1bba85b0927f52c0e5fbf1f34"

connection = None
# use_server = "--server" in argv
use_server = True
if use_server:
    connection = ServerConnection()
    factorio_mod_dir = connection.factorio_mod_dir
else:
    default_mod_dir = Path(r"C:\Users\Moritz\AppData\Roaming\Factorio\mods")
    if default_mod_dir.exists():
        factorio_mod_dir = str(default_mod_dir)
    else:
        factorio_mod_dir = input("Please enter the path of the factorio mods folder: ")
        while not Path(factorio_mod_dir).exists():
            factorio_mod_dir = input("Invalid directory! Please enter the path of the factorio mods folder: ")


def download_mod(mod_info, mod_folder):

    # build URL
    base_url = "https://mods.factorio.com"
    query_params = urlencode({"username": username, "token": token})
    download_url = f"{base_url}{mod_info.download_url}?{query_params}"

    # build downloadpath and Filename
    zip_filename = f"{mod_folder}/{mod_info.name}_{mod_info.latest_release_version}.zip"
    out_file = Path(mod_folder) / zip_filename

    ps_script = f"Invoke-WebRequest '{download_url}' -outfile '{out_file}'"
    if not connection:
        download = run_ps_script(ps_script)
        errorcode = download.returncode
        delete_script = run_ps_script
    else:
        download = connection.run_script_on_server(ps_script)
        errorcode = download.status_code
        delete_script = connection.run_script_on_server

    if errorcode == 0:
        ps_script = rf"Remove-item {mod_folder}\{mod_info.installed_version_filename}"
        remove = delete_script(ps_script)

        if not connection:
            success = remove.returncode == 0
        else:
            success = remove.status_code == 0
        if success:
            print(f"Removing of old File for {mod_info.installed_version_filename}")
    else:
        print(f"Download failed for {mod_info.installed_version_filename}")

def check_for_updates(mod_dir):
    mod_list = create_list_of_installed_mods(mod_dir, connection)
    for mod in mod_list:
        mod_info = ModInfo(mod)
        mod_info.installed_version = mod["version"]
        if mod["version"] >= mod_info.latest_release_version:
            print(f"{mod['name']} is up to date")
        else:
            print(f"Download mod here: {mod_info.download_url}")
            download_mod(mod_info, factorio_mod_dir)





if __name__ == "__main__":
    check_for_updates(factorio_mod_dir)

