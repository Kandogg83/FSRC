# Factorio Server Manager (FSRC)

A Python-based tool to manage your Factorio dedicated server with features like starting, stopping, automaticly updating mods, and sending RCON commands. Supports both local and remote server control.

---

## Features

- Start and stop the Factorio server
- Graceful shutdown with RCON warning messages
- Automatic mod updates from the official Factorio mod portal
- Remote execution via PowerShell remoting
- Easy configuration using a JSON file

---

## Requirements

- Python 3.8+
- PowerShell (for remote execution)
- Windows OS (tested on Windows 10/11)
- [MCRcon](https://github.com/Tiiffi/mcrcon) Python library for RCON commands

---

## Installation

1. Clone this repository or download the latest release.
2. Create and edit your `config.json` with your server settings.
3. (Optional) Create `.env` file for sensitive credentials or put them directly in `config.json`.
4. Run locally using Python or use the provided executable (`fsrc.exe`).

---

## Usage

Run the executable or script with the following command-line arguments:

| Argument     | Description                                       |
|--------------|-------------------------------------------------|
| `--start`    | Start the Factorio server                         |
| `--shutdown` | Gracefully shutdown the server                    |
| `--update`   | Update installed mods and restart the server     |
| `--warn N`   | Send RCON warning messages N minutes before shutdown |
| `--rc`       | Enable remote server control mode                 |

Example:

```bash
fsrc.exe --start
fsrc.exe --warn 10
fsrc.exe --update
````

---

## Configuration
Your configuration is stored in config.json. Example:

````bash
{
  "mod_dir": "AppData/Roaming/Factorio/mods",
  "game_dir": "G:/SteamLibrary/steamapps/common/Factorio", 
  "server_ip": "192.168.1.100",              <---- needs to be set also in local mode for rcon to work
  "rcon_password": "your_rcon_password",     <---- will be set at server start and used for sending messages
  "factorio_username": "your_username",
  "factorio_token": "your_api_token",
  "base_mod_url": "https://mods.factorio.com",    <<-- don't change
  "api_endpoint": "https://mods.factorio.com/api/mods",    <<-- don't change
  "server_user": "remote_user",              <---- windows user on server (only for --rc)
  "server_password": "remote_password"       <---- windows password on server (only for --rc)
}
````
---

## Possible usecase :

- Set up for local use on server
- start from windows taskplanner with  arguments ( --warn 10, --warn 5, --warn 1, --update )

---

## Dependencies

This project requires the following Python packages:

- `mcrcon`
- `requests`
- `pypsrp`  <!-- für WinRM-Remoteausführung -->
- `pywinrm` 

To install all dependencies, run:

```bash
pip install -r requirements.txt
````
For more details about the dependencies and their licenses, see DEPENDENCIES.md.

## Building the Executable
You can build the executable with PyInstaller:

---

````bash
pyinstaller --onefile --icon=resources/fsrc.ico main.py
````

---

## Third-Party Libraries and Licenses

This project uses the following third-party libraries:

- **mcrcon** — licensed under the *zlib License*  
  Source: https://github.com/Tiiffi/mcrcon/blob/master/LICENSE

- **pypsrp** — licensed under the *MIT License*  
  Source: https://github.com/jborean93/pypsrp/blob/master/LICENSE

- **requests** — licensed under the *Apache 2.0 License*  
  Source: https://github.com/psf/requests/blob/main/LICENSE

- **pywinrm** — licensed under the *MIT License*  
  Source: https://github.com/diyan/pywinrm/blob/master/LICENSE

---

## Acknowledgments / Third-Party Libraries
This project uses mcrcon by Tiiffi, which is licensed under the zlib License.
You can find mcrcon here: https://github.com/Tiiffi/mcrcon

Thank you to the original author for providing this useful library.

---

## License
MIT License — see LICENSE file for details.








