from flask import Flask, render_template, jsonify
from core.server_logic import ServerManager

manager = ServerManager()
app = Flask(__name__)

@app.route("/")
def dashboard():
    server_online = manager.web_check_server_online()
    return render_template("dashboard.html", server_online=server_online)

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
    manager.run_update()
    return "", 204

@app.route("/api/server-status", methods={"GET"})
def server_status():
    data = {}
    is_online = manager.web_check_server_online()
    data["server_online"] = is_online
    if is_online is True:
        data["player_count"] = manager.get_player_count()
    print(data)

    return jsonify(data)

if __name__ == "__main__":
   app.run(debug=True)