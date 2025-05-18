import requests
from helpers import compare_mod_versions
class ModInfo:
    def __init__(self, mod):
        self.name = mod["name"]
        self.mod_info_web = requests.get(rf"https://mods.factorio.com/api/mods/{self.name}").json()
        self.latest_release_version = "0.0.0"
        self.latest_release_info = None
        self.download_url = None
        self.installed_version = mod["version"]
        self.installed_version_filename = f"{self.name}_{self.installed_version}.zip"
        for release in self.mod_info_web["releases"]:

            self.latest_release_version = compare_mod_versions(self.latest_release_version, release["version"])
            if self.latest_release_version == release["version"]:
                self.latest_release_info = release
                self.download_url = release["download_url"]
