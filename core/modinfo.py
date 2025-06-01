import requests
from core.helpers import compare_mod_versions

class ModInfo:
    def __init__(self, mod):
        self.name = mod["name"]
        self.mod_info_web = requests.get(rf"https://mods.factorio.com/api/mods/{self.name}").json()

        self.installed_version = mod["version"]
        self.installed_version_filename = f"{self.name}_{self.installed_version}.zip"
        self.latest_release_info = None
        self.download_url = None

        self.latest_version = self._get_latest_version()
        self.latest_version_filename = f"{self.name}_{self.latest_version}.zip"


    def _get_latest_version(self):
        for release in self.mod_info_web["releases"]:

            highest_version = compare_mod_versions(self.installed_version, release["version"])
            if highest_version == release["version"]:
                self.latest_release_info = release
                self.download_url = release["download_url"]
        return highest_version