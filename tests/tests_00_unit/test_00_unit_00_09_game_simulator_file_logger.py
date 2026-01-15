from src.tambola_game_simulator.tambola_game_simulator_interface import TambolaGameSimulatorInterface
from src.game_simulator_logger.game_simulator_file_logger import GameSimulatorFileLogger
import time
from pathlib import Path

class TestGameSimulator(TambolaGameSimulatorInterface):
    simulation_run_count = 0
    def __init__(self, game_simulator_file_logger):
        self._game_simulator_file_logger = game_simulator_file_logger
        self.str_repr = None
        self._log_filename_prefix = self.__class__.__name__
        TestGameSimulator.simulation_run_count += 1
        self._logdir_pathname = self._generate_logdir_pathname()
        self._logfile_pathname = self._generate_logfile_pathname()

    def __str__(self):
        if not self.str_repr:
            pretty_str = f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            pretty_str += f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Inside {self.log_filename_prefix} ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            pretty_str += f"~~~~~~~~~~~~~~~~~~~~~~~Game Simulation Run Number = {TestGameSimulator.simulation_run_count}~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
            pretty_str += f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"

            self.str_repr = f"{pretty_str}"
        return self.str_repr

    @property
    def log_filname_prefix(self):
        return self._log_filename_prefix
    
    @property
    def logdir_pathname(self):
        return self._logdir_pathname
    
    @property
    def log_filename(self):
        return self._log_filename

    @property
    def log_filename_prefix(self):
        return self._log_filename_prefix

    @property 
    def logfile_pathname(self):
        return self._logfile_pathname

    def _generate_logdir_pathname(self):
        pass

    def _generate_logfile_pathname(self):
        pass

    def set_logger_dir_pathname(self):
        # self.game_simulator_file_logger.set_logdir_pathname(self.logdir_pathname)
        pass
    
    def set_logger_file_pathname(self):
        # self.game_simulator_file_logger.set_logfile_pathname(self.logfile_pathname)
        pass

    def log_message_to_file(self):
        with self.game_simulator_file_logger as logger:
            logger.log(self)

    def validate_technically_inaccurate_claim(self):
        print(f"Inside TestGameSimulator::validate_fastest_row_technically_inaccurate_claim()")

    def validate_technically_accurate_but_invalid_claim(self):
        print(f"Inside TestGameSimulator::validate_fastest_row_technically_accurate_but_invalid_claim()")

    def validate_technically_accurate_and_valid_claim(self):
        print(f"Inside TestGameSimulator::validate_fastest_row_technically_accurate_and_valid_claim()")

def _create_logging_directory():
        cwd = Path.cwd()
        logdir_relative_path = Path("logs") / Path("TestGameSimulator")
        logdir_full_pathname = cwd / logdir_relative_path

        try:
            logdir_full_pathname.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            if e.errno == errno.EACCES or e.errno == errno.EPERM:
                print(f"Permission denied: Could not create directory at {str(logdir_full_pathname)}")
                print("Reason: Check file/directory permissions or try running the script with elevated privileges.")
            elif e.errno == errno.ENOSPC:
                print(f"No space left on device: Could not create directory at {str(logdir_full_pathname)}")
            elif e.errno == errno.ENOENT:
                print(f"No such file or directory: The parent directory {str(logdir_full_pathname.parent)} does not exist.")
                print("Reason: Use my_file.parent.mkdir(parents=True, exist_ok=True) to create parent directories automatically.")
            else:
                print(f"An unexpected OS error occurred: {e}")

        return str(logdir_full_pathname)

def _create_log_file(logdir_pathname):
        curr_timestamp = time.strftime("%Y%m%d-%H%M%S")
        log_filename = "TestGameSimulator" + "-" + curr_timestamp
        logfile_full_pathname = Path(logdir_pathname) / Path(log_filename)
        
        try:
            logfile_full_pathname.touch(exist_ok=True)
        except OSError as e:
            if e.errno == errno.EACCES or e.errno == errno.EPERM:
                print(f"Permission denied: Could not create file at {logfile_full_pathname}")
                print("Reason: Check file/directory permissions or try running the script with elevated privileges.")
            elif e.errno == errno.ENOSPC:
                print(f"No space left on device: Could not create file at {str(logdir_full_pathname)}")
            elif e.errno == errno.ENOENT:
                print(f"No such file or directory: The parent directory {str(logfile_full_pathname.parent)} does not exist.")
                print("Reason: Use my_file.parent.mkdir(parents=True, exist_ok=True) to create parent directories automatically.")
            else:
                print(f"An unexpected OS error occurred: {e}")

        return str(logfile_full_pathname)
    
def test_game_simulator_file_logger_init_log_file_created_on_filesystem():
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)
    game_simulator = TestGameSimulator(game_simulator_file_logger)
    game_simulator.log_message_to_file()

    logfile_path = Path(logfile_pathname)

    assert logfile_path.exists() and logfile_path.is_file()

def test_game_simulator_file_logger_init_log_file_created_on_filesystem_inside_unique_directory():
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)
    game_simulator = TestGameSimulator(game_simulator_file_logger)
    game_simulator.log_message_to_file()

    logdir_path = Path(logdir_pathname)

    assert logdir_path.exists() and logdir_path.is_dir()

def test_game_simulator_file_logger_init_log_file_created_in_append_mode():
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)
    game_simulator = TestGameSimulator(game_simulator_file_logger)
    game_simulator.log_message_to_file()

    is_append_mode = False
    is_writable = False

    try:
        with open(logfile_pathname, 'a') as file:
            if file.mode == 'a':
                is_append_mode = True
                
            if file.writable():
                is_writable = True
    except FileNotFoundError:
        print(f"Error: The file '{logfile_pathname}' was not found.")
    except IOError as e:
        print(f"Error reading file: {e}")
    else:
        assert is_append_mode and is_writable

def test_game_simulator_file_logger_init_fresh_log_file_created_for_fresh_simulation_has_unique_name():
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)

    logfile_pathname_one = None
    logfile_pathname_two = None
    logfile_pathname_three = None

    try:
        logfile_pathname_one = _create_log_file(logdir_pathname)
        game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname_one)
        game_simulator_one = TestGameSimulator(game_simulator_file_logger)
    except:
        pass
    else:
        time.sleep(2)

    try:
        logfile_pathname_two = _create_log_file(logdir_pathname)
        game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname_two)
        game_simulator_two = TestGameSimulator(game_simulator_file_logger)
    except:
        pass
    else:
        time.sleep(2)

    try:
        logfile_pathname_three = _create_log_file(logdir_pathname)
        game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname_three)
        game_simulator_three = TestGameSimulator(game_simulator_file_logger)
    except:
        pass
    else:
        assert logfile_pathname_one != logfile_pathname_two and logfile_pathname_two != logfile_pathname_three and logfile_pathname_three != logfile_pathname_one

def test_game_simulator_file_logger_init_current_log_file_available_after_simulation_ends():
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)

    try:
        game_simulator = TestGameSimulator(game_simulator_file_logger)
        game_simulator.log_message_to_file()
    except:
        pass
    else:
        logfile_path = Path(logfile_pathname)
        assert logfile_path.exists() and logfile_path.is_file()

def test_game_simulator_file_logger_log_fresh_log_message_not_none():
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)
    
    try:
        game_simulator = TestGameSimulator(game_simulator_file_logger)
        game_simulator.log_message_to_file()
    except:
        pass
    else:
        logfile_path = Path(logfile_pathname)
        logfile_size = logfile_path.stat().st_size

        assert logfile_path.exists() and logfile_path.is_file() and logfile_size > 0

def test_game_simulator_file_logger_log_fresh_log_message_append_to_log_file_is_success():
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)
    game_simulator = TestGameSimulator(game_simulator_file_logger)
    
    logfile_path = Path(logfile_pathname)

    game_simulator.log_message_to_file()
    logfile_size_one = logfile_path.stat().st_size

    game_simulator.log_message_to_file()
    logfile_size_two = logfile_path.stat().st_size

    assert logfile_size_two - logfile_size_one

def test_game_simulator_file_logger_log_specific_log_message_is_present_in_current_log_file_after_simulation_ends():
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)
    logfile_path = None
    
    try:
        game_simulator = TestGameSimulator(game_simulator_file_logger)
        game_simulator.log_message_to_file()
    except:
        pass
    else:
        is_msg_logged = False
        try:
            with open(logfile_pathname, 'r', encoding='utf-8') as file:
                file_content = file.read()

                if str(game_simulator) in file_content:
                    is_msg_logged = True
        except FileNotFoundError:
            print(f"Error: The file '{logfile_pathname}' was not found.")
            return False
        except IOError as e:
            print(f"Error reading file: {e}")
            return False
        else:
            assert is_msg_logged
