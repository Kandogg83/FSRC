import subprocess
from pathlib import Path
import sys

def compare_mod_versions(number1: str, number2: str):
    v1 = list(map(int, number1.split(".")))
    v2 = list(map(int, number2.split(".")))

    if v1 > v2:
        return number1
    elif v2 > v1:
        return number2
    else:
        return number1


def run_local_ps_script(ps_script):
    ps_script  = f"$ProgressPreference = 'SilentlyContinue'\n " + ps_script
    data = subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return data


def create_list_of_installed_mods(mod_dir, connection=None):

    if connection:
        result = connection.run_script_on_server(f"get-Childitem '{mod_dir}' -Name")
        content = result.std_out.strip().decode()


    else:
        result = run_local_ps_script(f"get-Childitem '{mod_dir}' -Name")
        content = result.stdout.strip()



    mod_list = [entry.strip().removesuffix(".zip") for entry in content.split("\n")
                if entry.strip().endswith(".zip")]
    return_mod_list = []
    for mod in mod_list:
        temp_list = mod.rsplit("_", 1)
        return_mod_list.append({"name": temp_list[0], "version": temp_list[1]})
    return return_mod_list

def get_local_path(filename):
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent / filename
    else:
        return Path(__file__).resolve().parent / filename


