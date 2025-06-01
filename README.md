# Factorio Server Manager (FSRC)

A Python-based tool to manage your Factorio dedicated server with features like starting, stopping, automatically updating mods, and sending RCON commands. Supports both local and remote server control.  
As of 1.1 also includes a Web-UI.

---

## Features

- Start and stop the Factorio server
- Graceful shutdown with RCON warning messages
- Automatic mod updates from the official Factorio mod portal
- Remote execution via PowerShell remoting
- Easy configuration using a JSON file
- Web-UI with all features from above

---

## Requirements

- Python 3.8+
- PowerShell (for remote execution)
- Windows OS (tested on Windows 10/11)

---

## Installation

1. Clone this repository or download the latest release.
2. Create and edit your `config.json` with your server settings. (`config_template.json` included as guidance)
3. (Optional) Create a `.env` file for sensitive credentials or put them directly in `config.json`.
4. Run locally using Python or use the provided executable (`fsrc.exe`).  
   Entrypoint for standalone: `core/logic.py`
5. Use `buildforweb.py` for building the Web-UI. Entrypoint for Web-UI: `webserver.py`

---

## Usage

### Without UI

Run the executable or script with the following command-line arguments:

| Argument     | Description                                            |
|--------------|--------------------------------------------------------|
| `--start`    | Start the Factorio server                              |
| `--shutdown` | Gracefully shutdown the server                         |
| `--update`   | Update installed mods and restart the server           |
| `--warn N`   | Send RCON warning messages N minutes before shutdown   |
| `--rc`       | Enable remote server control mode                      |

Example:

```bash
fsrc.exe --start
fsrc.exe --warn 10
fsrc.exe --update
```

### With UI (WebApp)

1. Unzip the included `web-server.zip` on the server
2. Rename and edit `config_template.json` to `config.json` and fill in your settings as described below
3. Build a virtual environment, install dependencies, and run `webserver.py`
4. The Web-UI should now be reachable on its local IP, port 5000

---

## Configuration

Your configuration is stored in `config.json`. Example:

```json
{
  "mod_dir": "AppData/Roaming/Factorio/mods",
  "game_dir": "X:/SteamLibrary/steamapps/common/Factorio",
  "server_ip": "192.168.1.100",                         needs to be set wether it´s local or not
  "rcon_password": "your_rcon_password",                choose one
  "factorio_username": "your_username",
  "factorio_token": "your_api_token",
  "base_mod_url": "https://mods.factorio.com",          do not change
  "api_endpoint": "https://mods.factorio.com/api/mods", do not change
  "server_user": "remote_user",                         <<-- windows-server-user
  "server_password": "remote_password",                 <<-- windows-server-password
  "socket_secret": "<SOCKET_SECRET>"                    choose one
}
```

> 💡 If `mod_dir` is not in `C:/Users/<your_name>/...`, it must be an absolute path like `X:/factorio/mods`.

---

## Example Use Case

Set up for local use on a server, then:

- Start from the Windows Task Scheduler with arguments:
  - `--warn 10`, `--warn 5`, `--warn 1`, `--update`
- Or launch the Web-UI for easy remote access

---

## Dependencies

This project requires the following Python packages:

- `mcrcon`
- `requests`
- `pypsrp`
- `pywinrm`
- `flask`
- `flask-socketio`
- `gevent`

Install them with:

```bash
pip install -r requirements.txt
```

---

## Building the Executable

You can build the standalone executable using PyInstaller:

```bash
python -m PyInstaller --onefile --name fsrc.exe --icon=static/fsrc.ico core/logic.py
```

## Third-Party Libraries and Licenses

This project uses the following third-party libraries:

- **mcrcon** — *zlib License*  
  https://github.com/Tiiffi/mcrcon/blob/master/LICENSE

- **pypsrp** — *MIT License*  
  https://github.com/jborean93/pypsrp/blob/master/LICENSE

- **requests** — *Apache 2.0 License*  
  https://github.com/psf/requests/blob/main/LICENSE

- **pywinrm** — *MIT License*  
  https://github.com/diyan/pywinrm/blob/master/LICENSE

- **flask** — *BSD 3-Clause License*  
  https://github.com/pallets/flask

- **flask-socketio** — *MIT License*  
  https://github.com/miguelgrinberg/flask-socketio

- **gevent** — *MIT License*  
  http://www.gevent.org

---

## License

MIT License — see [LICENSE](LICENSE) file for details.
