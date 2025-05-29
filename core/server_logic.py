import argparse
from pathlib import Path
from time import sleep
from turtledemo.sorting_animate import partition

from .config import CONFIG, get_local_path
from .connection import ServerConnection
from .factoriomodupdater import FactorioModUpdater
import logging
from mcrcon import MCRcon
from .helpers import run_local_ps_script
import re


class ServerManager:
    def __init__(self, use_server=False):
        self.start_logging()

        if use_server:
            self.connection = ServerConnection()
        else:
            self.connection = None

        self.run_script = self._get_run_script()
        self.game_dir =  self._get_game_dir()
        self.mod_handler = FactorioModUpdater(connection=self.connection)
        self.update_in_progress = False


    def start_logging(self):
        log_file = get_local_path(
            "../fsrc_eventlog.log")
        logging.basicConfig(format='%(levelname)s: %(asctime)s %(message)s',
                            datefmt='%d.%m.%y  %H:%M:%S',
                            level=logging.INFO,
                            filename=log_file,
                            encoding='utf-8'
                            )


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
            return True
        else:
            return False

    def send_rcon(self, cmd):
        with MCRcon(CONFIG["server_ip"], CONFIG["rcon_password"], port=27015) as mcr:
            return mcr.command(cmd)

    def web_check_server_online(self):
        if self.check_server_online():
            return True
        elif self.update_in_progress:
            return "update"
        else:
            return False

    def get_online_players(self):
        cmd = "/players online"
        players = self.send_rcon(cmd)
        actual_list = re.findall(r"^\s*(\w+)\s+\(online\)", players, re.MULTILINE)
        return actual_list


    def warn_shutdown(self, minutes:int):
        color = "red" if minutes <= 5 else "orange"
        warning = f"[color={color}]⚠️ Warning ⚠️ - {minutes} minute{"s" if minutes != 1 else ""} until server shutdown for maintenance[/color]"
        self.send_rcon(warning)
        logging.info(f"Send {minutes} minute{"s" if minutes != 1 else ""} shutdown warning")


    def server_shutdown(self):
        if self.check_server_online():
            shutdown_message = f"[color=red]Shutting down Server. Goodbye[/color]"
            self.send_rcon(shutdown_message)
            sleep(2)
            self.send_rcon("/quit")
            sleep(2)
            ps_script = "Stop-Process -Name factorio -Force"
            self.run_script(ps_script)
            logging.info(f"Shutdown complete")

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
                logging.info("✅ Factorio Server running.....")
            else:
                logging.warning("❌ Factorio Server not detected after WMI start")

    def run_update(self):
        print("run_update")
        self.update_in_progress = True
        self.server_shutdown()

        for i in range(30):
            if not self.check_server_online():
                logging.info("Server shut down, continuing update process")
                break
            sleep(1)
        else:
            logging.warning("Timeout waiting for server to shut down")

        logging.info(f"🔄 Modupdater starting...")
        updated_modlist = FactorioModUpdater(self.connection).check_for_updates()
        logging.info(f"✅ ModUpdater finished with %s errors", 0)

        if updated_modlist:
            logging.info("The following mods were updated:")
        for mod in updated_modlist:
            logging.info(f"     {mod.name} updated from {mod.installed_version} to {mod.latest_version}")
        logging.info("🏁 ModUpater closing...")
        sleep(5)
        self.server_start()
        self.update_in_progress = False
def main():


    parser = argparse.ArgumentParser()
    parser.add_argument("--warn", type=int, help="Send specified interval Warning in minutes")
    parser.add_argument("--update", action="store_true", help="Saves state, shuts down Server, starts update process, restarts server")
    parser.add_argument("--start", action="store_true", help="Starts the server")
    parser.add_argument("--shutdown", action="store_true", help="Saves state and shuts down server, kills process")
    parser.add_argument("--rc", action="store_true", help="remote control a server")
    args = parser.parse_args()


    #############################
    # for easy testing
    args.rc = True
    #args.start = True
    #args.warn = 1
    #args.shutdown = True
    args.update = True

    #############################

    manager = ServerManager(use_server=args.rc)

    if args.warn:
        manager.warn_shutdown(args.warn)
    if args.shutdown:
        manager.server_shutdown()
    if args.start:
        manager.server_start()
    if args.update:
        manager.run_update()

if __name__ == "__main__":
    main()