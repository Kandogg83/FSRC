import json
import subprocess

def compare_mod_versions(number1: str, number2: str):
    v1 = list(map(int, number1.split(".")))
    v2 = list(map(int, number2.split(".")))

    if v1 > v2:
        return number1
    elif v2 > v1:
        return number2
    else:
        return False


def run_ps_script(ps_script):
    ps_script  = f"$ProgressPreference = 'SilentlyContinue'\n " + ps_script
    data = subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True)
    return data


def create_list_of_installed_mods(mod_dir, connection=None):
    if not connection:
        mod_directory_content = run_ps_script(f"get-Childitem {mod_dir} -name")
        mod_directory_content = mod_directory_content.stdout.strip()
        print(mod_directory_content)
    else:
        mod_directory_content = connection.run_script_on_server(f"get-Childitem {mod_dir} -name")
        mod_directory_content = mod_directory_content.std_out.strip().decode()
        print(mod_directory_content)
    mod_list = [entry.strip().removesuffix(".zip") for entry in mod_directory_content.split("\n")
                if entry.strip().endswith(".zip")]
    return_mod_list = []
    for mod in mod_list:
        temp_list = mod.rsplit("_", 1)
        return_mod_list.append({"name": temp_list[0], "version": temp_list[1]})
    return return_mod_list

def get_mod_list(self):
    json_string =  self.run_script_on_server(rf"get-content {self.factorio_mod_dir}\mod-list.json -raw")
    mod_list = json.loads(json_string)
    mod_list_3rdparty = []
    for mod in mod_list["mods"]:
        if mod["name"] not in ["base", "elevated-rails", "quality", "space-age"]:
            mod_list_3rdparty.append(mod)
    return mod_list_3rdparty


