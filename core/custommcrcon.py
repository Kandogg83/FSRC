from mcrcon import MCRcon
from core.config import CONFIG
import time
import logging
import atexit

class RCONClient:
    def __init__(self):

        self.event_logger = logging.getLogger("server_logic")
        self.mcr = None
        self.server_online = False

    def check_server_online(self):
        from core.servermanager import server_manager
        self.server_online = server_manager.check_server_online()
        return self.server_online

    def connect(self):

        if self.mcr and  self.server_online:
            return True

        self.mcr = None
        self.check_server_online()

        if not self.check_server_online():
            return False

        attempt = 1
        max_attemps = 4
        while  attempt <= max_attemps:
            try:
                self.mcr = MCRcon(CONFIG["server_ip"], CONFIG["rcon_password"], port=27015)
                self.mcr.connect()
                self.event_logger.info("✅ RCON Connection established")
                return True

            except ConnectionRefusedError as e:
                attempt += 1
                self.event_logger.error(f"❌ MCRcon connection refused. Reason: {e}")
                self.event_logger.info(f"Attempt {attempt}: Retrying in 10 seconds...")
                time.sleep(10)
                if not self.check_server_online():
                    break

            except Exception as e:
                self.event_logger.error(f"Unexpected MCRcom error: {e}")
                break

        self.event_logger.error(f"❌ MCRcon connection failed after {attempt} attempts.")
        self.mcr = None

    def disconnect(self):
        if self.mcr:
            try:
                self.mcr.disconnect()
                self.event_logger.info("🔌 RCON Connection closed")

            except Exception as e:
                self.event_logger.error(f"⚠️ Error closing RCON Connection: {e}")

            finally:
                self.mcr = None

    def send(self, cmd):
        if not self.mcr:
            if not self.connect():
                return None
        if not self.mcr:
            return None

        try:
            response = self.mcr.command(cmd)
            if not cmd.startswith("/"):
                self.event_logger.info(f"💬 {cmd} ")
            return response
        except Exception as e:
            self.event_logger.error(f"❌ Error sending RCON command: {cmd}  | Error: {e}")
            self.disconnect()

        return None

rcon_client = RCONClient()

atexit.register(rcon_client.disconnect)