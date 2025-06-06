###           ###
# Version 1.1.1 #
###           ###

from version import __version__

from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from core.servermanager import server_manager
from core.helpers import get_local_path
from core.config import CONFIG
import logging
import time
from threading import Thread

def setup_logger():

    weblogger_path = get_local_path("../fsrc_weblogger.log")

    file_handler = logging.FileHandler(weblogger_path, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)

setup_logger()      # TODO: noch auf custom_logger umstellen ?!
manager = server_manager
mod_list = manager.mod_handler.mod_list

app = Flask(__name__)
app.config["SECRET_KEY"] = CONFIG["socket_secret"]
socketio = SocketIO(app)

@app.route("/")
def dashboard():
    server_online = manager.web_check_server_online()
    players = manager.get_online_players()
    return render_template("dashboard.html", server_online=server_online, players=players)

@app.route("/version")
def send_current_verison():
    return __version__

@app.route("/start-server", methods={"POST"})
def start_server():
    manager.server_start()
    return "", 204

@app.route("/shutdown-server", methods= {"POST"})
def stop_server():
    manager.server_shutdown()
    return "", 204

@app.route("/start-update", methods={"POST"})
def start_updates():
    manager.run_update(socketio)
    return "", 204

@app.route("/api/server-status", methods={"GET"})
def server_status():
    data = {}
    is_online = manager.web_check_server_online()
    data["server_online"] = is_online
    data["player"] = manager.get_online_players()
    return jsonify(data)

@socketio.on("log_entry")
def send_log(log=None):
    if not log:
        log = manager.event_log.read_log(from_beginning=True)
        new = True
    else:
        new = False
    data = {"log": log, "new": new}
    socketio.emit("log_entry", data)

@socketio.on("mod_list")
def new_mod():
    socketio.emit("mod_list", {"mod_list": manager.mod_handler.mod_list})

def check_log_for_updates():
    current_log = manager.event_log.read_log(return_binary=True)
    while True:
        latest_log = manager.event_log.read_log(return_binary=True)
        if current_log != latest_log:
            current_log = latest_log
            send_log(current_log.decode("utf-8"))
        time.sleep(2)

new_thread = Thread(target=check_log_for_updates, daemon=True)
new_thread.start()

if __name__ == "__main__":
   socketio.run(app, host="0.0.0.0", port=5000, debug=True, allow_unsafe_werkzeug=True)
