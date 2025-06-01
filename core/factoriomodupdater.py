from core.modinfo import ModInfo
from pathlib import Path
from core.helpers import create_list_of_installed_mods,run_local_ps_script
from urllib.parse import urlencode
import logging
from core.config import CONFIG


class FactorioModUpdater:
    def __init__(self, connection):
        self.event_logger = logging.getLogger("server_logic")
        self.connection = connection
        self.mod_dir = self._get_mod_directory()
        self.run_script = self._get_run_script()
        self._mod_list = create_list_of_installed_mods(self.mod_dir, self.connection)


    @property
    def mod_list(self):
        return create_list_of_installed_mods(self.mod_dir, self.connection)


    def _get_mod_directory(self):
        if self.connection:
            return self.connection.mod_dir
        else:
            default_path = Path.home() / "AppData" / "Roaming" / "Factorio" / "mods"
            return CONFIG.get("mod_dir", str(default_path))

    def _get_run_script(self):
        if self.connection:
            return self.connection.run_script_on_server
        else:
            return run_local_ps_script

    def _get_returncode(self, data):
        if self.connection:
            return data.status_code
        else:
            return data.returncode

    def check_for_updates(self, socket):

        updated_mods = []
        for mod in self.mod_list:
            mod_info = ModInfo(mod)
            mod_info.installed_version = mod["version"]
            if not mod["version"] >= mod_info.latest_version:

                self.event_logger.info(f"Downloading new Version for mod: {mod_info.name}")
                updated = self.download_mod(mod_info)
                if updated:
                    self.event_logger.info(f"Mod {mod_info.name} has been updated to Version {mod_info.latest_version}")
                    updated_mods.append(updated)
                    if socket:
                        socket.emit("mod_list", {"mod_list": self.mod_list})
        return updated_mods

    def download_mod(self, mod_info):
        auth_params = urlencode({"username": CONFIG["factorio_username"], "token": CONFIG["factorio_token"]})
        download_url = f"{CONFIG['base_mod_url']}{mod_info.download_url}?{auth_params}"
        out_file = Path(self.mod_dir) / mod_info.latest_version_filename
        ps_script = f"Invoke-WebRequest '{download_url}' -outfile '{out_file}'"
        download = self.run_script(ps_script)

        if self._get_returncode(download) == 0:
            if self.delete_mod(mod_info):
                return mod_info
            else:
                return None
        else:
            self.event_logger.warning(f"Download failed for mod: {mod_info.name}")
            return None

    def delete_mod(self,mod_info):

        path = Path(self.mod_dir) / mod_info.installed_version_filename
        ps_script = rf"Remove-Item -Path '{path}' -Force"

        remove = self.run_script(ps_script)
        if self._get_returncode(remove) == 0:
            return True
        else:
            return False

if __name__ == "__main__":
    FactorioModUpdater(None).check_for_updates()