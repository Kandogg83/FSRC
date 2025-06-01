# CHANGELOG FSRC

---
## [1.1] - 2025-06.01
### Added / Changed / Improved
- introduced web ui
  - buttons for start-server, stop-server and update-mods
  - automatically refreshing eventlog on dashboard
  - list of mods with versions on dashboard
- enhanced logging in seperate files (webserver backend and gameserver)
- restructured filebase
- introduced builder for webui deployment


## [1.01] - 2025-05-23
### Fixed / Added
- Logging: Fixed path issue for the log file (using get_local_path)
- Mod Path: Fixed wrong path handling for absolute paths in config.json ["mod_dir"]
- Minor bug fixes and stability improvements
- ICO for the .exe
- Added CHANGELOG.txt


## [1.00] - 2025-05-20
### Added
- Initial release of the EXE (fsrc.exe)
- Basic server start, shutdown, and update functions
- Configuration file in JSON format integrated
- Support for RCON commands and warnings
- Task Scheduler integration with BAT files
