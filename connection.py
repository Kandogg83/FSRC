import winrm
import getpass

class ServerConnection:
    def __init__(self):
        self.server_ip = "25.51.120.99"
        #password = getpass.getpass("Password:", stream=None)
        password = input("Enter password: ")
        self.auth = ("ServerAdmin", password)
        self.factorio_mod_dir = r"c:\Games\factorio\mods"

        self.session = self.connect_to_server()

    def connect_to_server(self):
        return winrm.Session(f"http://{self.server_ip}:5985", auth=self.auth)

    def run_script_on_server(self, ps_script):
        ps_script = f"$ProgressPreference = 'SilentlyContinue'\n " + ps_script
        data = self.session.run_ps(ps_script)
        self.returncode = data.status_code
        return data
