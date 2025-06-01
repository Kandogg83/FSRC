import json
import sys
from pathlib import Path
from .helpers import get_local_path


CONFIG_PATH = get_local_path("../config.json")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config_import = json.load(f)

mod_dir_path = Path(config_import["mod_dir"])
if not mod_dir_path.is_absolute():
    mod_dir_path = Path.home() / mod_dir_path
CONFIG = {
    "mod_dir": mod_dir_path,
    "game_dir": Path(config_import["game_dir"]),
    "server_ip": config_import["server_ip"],
    "rcon_password": config_import["rcon_password"],
    "factorio_username": config_import["factorio_username"],
    "factorio_token": config_import["factorio_token"],
    "base_mod_url": config_import["base_mod_url"],
    "api_endpoint": config_import["api_endpoint"],
    "server_user": config_import["server_user"],
    "server_password": config_import["server_password"],
    "socket_secret": config_import["socket_secret"]
}

