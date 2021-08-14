import os
import sys
import logging

cwd = os.getcwd()
directory_path = os.path.expandvars(f"{cwd}/logs")
log_file_path = os.path.expandvars(f"{cwd}/logs/error.log")

class Log:

    def __init__(self) -> None:
        self.info_log = logging.getLogger("INFO")
        self.error_log = logging.getLogger("ERROR")
        self.settings()

        """
        Default date format is YYYY/MM/DD.
        既定の日付形式は YYYY/MM/DD です.
        """
        self.log_format = logging.Formatter("[%(asctime)s]%(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        self.streamhandler = logging.StreamHandler()
        self.streamhandler.setFormatter(self.log_format)
        self.error_handler = logging.FileHandler("logs/error.log")
        self.error_handler.setFormatter(self.log_format)

        if not self.info_log.hasHandlers():
            self.info_log.setLevel(logging.INFO)
            self.info_log.addHandler(self.streamhandler)

        if not self.error_log.hasHandlers():
            self.error_log.setLevel(logging.ERROR)
            self.error_log.addHandler(self.error_handler)

    def settings(self) -> None:
        if not os.path.exists(directory_path):
            try:
                os.makedirs(directory_path, exist_ok=True)
            except Exception as e:
                self.print_critical_log(e)
                sys.exit(1)
        
        if not os.path.exists(log_file_path):
            try:
                with open(log_file_path, "w") as f:
                    f.write("")
            except Exception as e:
                self.print_critical_log(e)
                sys.exit(1)

    def print_info_log(self, content) -> None:
        self.info_log.info(content)

    def print_error_log(self, content) -> None:
        self.info_log.error(content)
        self.error_log.error(content)

    def print_critical_log(self, content) -> None:
        self.info_log.critical(content)
        self.error_log.critical(content)