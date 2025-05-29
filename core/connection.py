import winrm
from  pathlib import Path
from .config import CONFIG
import warnings

# Nur winrm warnings filtern ##
warnings.filterwarnings(
    "ignore",
    message="There was a problem converting the Powershell error message.*",
    module="winrm"
)

class ServerConnection:
    def __init__(self):
        self.server_ip = "25.51.120.99"
        self.auth = (CONFIG["server_user"], CONFIG["server_password"])
        self.mod_dir = Path(r"c:\Games\factorio\mods")
        self.game_dir = Path(r"c:\Games\factorio")

        self.session = self.connect_to_server()

    def connect_to_server(self):
        return winrm.Session(f"http://{self.server_ip}:5985", auth=self.auth)

    def run_script_on_server(self, ps_script):
        ps_script = f"$ProgressPreference = 'SilentlyContinue'\n " + ps_script
        data = self.session.run_ps(ps_script)
        self.returncode = data.status_code
        return data
