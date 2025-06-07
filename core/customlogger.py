from core.helpers import get_local_path
from re import match
import logging



class ScriptLogger:
    def __init__(self, name, logfile_name=None, logger_level="INFO"):
        if logfile_name is None:
            logfile_name = f"{name}.log"
        elif not logfile_name.endswith(".log"):
            logfile_name += ".log"
        else:
            pass
        self.logfile = get_local_path(f"../{logfile_name}")
        self._logger = self.setup_logger(name, logger_level)
        self.last_read_position = 0

    @property
    def handler(self):
        return self._logger.handlers[0]

    @property
    def logger(self):
        return self._logger

    def setup_logger(self, name, logger_level):

        level = getattr(logging, logger_level.upper(), logging.INFO)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.handlers.clear()
        file_handler = logging.FileHandler(self.logfile, mode="a", encoding="utf-8")
        file_handler.setLevel(level)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.propagate=False

        return logger

    def read_log(self, from_beginning=False, return_binary=False):
        if not from_beginning:
            start = self.last_read_position
        else:
            start = 0
            self.last_read_position = 0

        if self.logfile.exists():
            with open(self.logfile, "rb") as f:
                f.seek(start)
                new_content = f.read()
                end = f.tell()
                if end != start:
                    self.last_read_position = end
            if return_binary:
                return new_content
            else:
                print(new_content)
                return new_content.decode("utf-8")
        else:
            return ""
