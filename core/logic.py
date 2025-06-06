import version
import argparse
from core.servermanager import server_manager

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
    #args.rc = True
    #args.start = True
    #args.warn = 1
    #args.shutdown = True
    #args.update = True

    #############################

    manager = server_manager

    if args.warn:
        manager.warn_shutdown(args.warn)
    if args.shutdown:
        manager.server_shutdown()
    if args.start:
        manager.server_start()
    if args.update:
        manager.run_update()
    if  args.rc:
        manager.use_server_connection()

if __name__ == "__main__":
    main()