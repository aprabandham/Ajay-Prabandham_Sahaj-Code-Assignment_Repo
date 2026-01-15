from src.game_simulator_logger.game_simulator_logger_interface import GameSimulatorLoggerInterface
from contextlib import contextmanager

class GameSimulatorFileLogger(GameSimulatorLoggerInterface):
    def __init__(self, logfile_pathname):
        self.logfile_pathname = logfile_pathname
        self.logfile_handle = None

    def set_logdir_pathname(self, logdir_pathname):
        # self.logdir_pathname = logdir_pathname
        pass

    def set_logfile_pathname(self, logfile_pathname):
        # self.logfile_pathname = logfile_pathname
        pass

    # Open file in append mode
    def __enter__(self):
        try:
            self.logfile_handle = open(self.logfile_pathname, 'a', encoding='utf-8')
        except FileNotFoundError:
            print(f"Error: The file with handle '{self.logfile_pathname}' was not found.")
        else:
            return self

    # You can handle exceptions here if needed
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if(self.logfile_handle):
                self.logfile_handle.close()
        except FileNotFoundError:
            print(f"Error: The file with handle {self.logfile_handle} was not found.")
        else:
            pass

    def log(self, obj):
        if self.logfile_handle:
            try:
                write_str = ""
                write_str += "\n##########################################################################################################\n"
                write_str += "\n" + str(obj) + "\n"
                write_str += "\n##########################################################################################################\n"
                
                self.logfile_handle.write(write_str)
            except FileNotFoundError:
                print(f"Error: The file with handle '{self.logfile_handle}' was not found.")
            except IOError as e:
                print(f"Error writing to file: {e}")
        else:
            print("Error: File handle not open!")
