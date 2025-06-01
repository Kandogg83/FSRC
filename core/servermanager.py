from pathlib import Path
from time import sleep
from .config import CONFIG
from .connection import ServerConnection
from .factoriomodupdater import FactorioModUpdater
from .customlogger import ScriptLogger
from .custommcrcon import rcon_client
import logging
from .helpers import run_local_ps_script
import re




class ServerManager:
    def __init__(self):
        self.event_log = ScriptLogger("server_logic", "fsrc_eventlog", logger_level="INFO")
        self.event_logger = self.event_log.logger
        self.connection = None

        self.run_script = self._get_run_script()
        self.game_dir =  self._get_game_dir()
        self.mod_handler = FactorioModUpdater(connection=self.connection)
        self.mod_list = self.mod_handler.mod_list
        self.server_online = self.check_server_online()
        self.update_in_progress = False

    def use_server_connection(self):
        self.connection = ServerConnection()

    def _get_run_script(self):
        if self.connection:
            return self.connection.run_script_on_server
        else:
            return run_local_ps_script

    def _get_game_dir(self):
        if self.connection:
            return self.connection.game_dir
        else:
            return CONFIG["game_dir"]

    def _get_stdout(self, result):
        if self.connection:
            return result.std_out.decode("cp1252", errors="replace").strip()
        else:
            return result.stdout.strip()

    def check_server_online(self):
        ps_script = r"get-process -name factorio"
        result = self.run_script(ps_script)
        if bool(self._get_stdout(result)):
            self.server_online = True
            return True
        else:
            self.server_online = False
            return False



    def web_check_server_online(self):
        if self.check_server_online():
            return True
        elif self.update_in_progress:
            return "update"
        else:
            return False

    def get_online_players(self):
        cmd = "/players online"
        if self.server_online:
            players = rcon_client.send(cmd)
            if players:
                actual_list = re.findall(r"^\s*([^\s]+)\s+\(online\)", players, re.MULTILINE)
                return actual_list
            else:
                return []
        else:
            return []

    def warn_shutdown(self, minutes:int):
        color = "red" if minutes <= 5 else "orange"
        warning = f"[color={color}]⚠️ Warning ⚠️ - {minutes} minute{'s' if minutes != 1 else ''} until server shutdown for maintenance[/color]"
        rcon_client.send(warning)
        self.event_logger.info(f"Send {minutes} minute{'s' if minutes != 1 else ''} shutdown warning")

    def server_shutdown(self):
        if self.check_server_online():
            shutdown_message = f"[color=red]Shutting down Server. Goodbye[/color]"
            rcon_client.send(shutdown_message)
            sleep(2)
            rcon_client.send("/quit")
            sleep(2)
            rcon_client.disconnect()
            ps_script = "Stop-Process -Name factorio -Force"
            self.run_script(ps_script)
            self.event_logger.info(f"Shutdown complete")

    def server_start(self):
        if not self.check_server_online():
            factorio_path = Path(self.game_dir) / "bin" / "x64" / "factorio.exe"
            settings_path = Path(self.game_dir) / "server-settings.json"
            rcon_args = f"--rcon-password {CONFIG['rcon_password']} --rcon-port 27015"
            server_args = f"--start-server-load-latest --server-settings {settings_path} {rcon_args}"

            ps_script = rf"""
                ([wmiclass]"Win32_Process").Create('"{factorio_path}" {server_args}')
                """
            self.run_script(ps_script)

            sleep(5)
            if self.check_server_online():
                self.event_logger.info("✅ Factorio Server running.....")
            else:
                self.event_logger.warning("❌ Factorio Server not detected after WMI start")

    def run_update(self, socket=None):
        self.update_in_progress = True
        self.server_shutdown()

        for i in range(30):
            if not self.check_server_online():
                self.event_logger.info("Server shut down, continuing update process")
                break
            sleep(1)
        else:
            logging.warning("Timeout waiting for server to shut down")

        self.event_logger.info(f"🔄 Modupdater starting...")
        updated_modlist = self.mod_handler.check_for_updates(socket)
        self.event_logger.info(f"✅ ModUpdater finished with %s errors", 0)

        if updated_modlist:
            self.event_logger.info("The following mods were updated:")
        for mod in updated_modlist:
            self.event_logger.info(f"     {mod.name} updated from {mod.installed_version} to {mod.latest_version}")
        self.event_logger.info("🏁 ModUpater closing...")
        sleep(5)
        self.server_start()
        self.update_in_progress = False

server_manager = ServerManager()