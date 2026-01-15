from src.tambola_game_simulator.tambola_fastest_early_five_game_simulator import TambolaFastestEarlyFiveGameSimulator
from src.calling_sequence.calling_sequence_generator import CallingSequenceGenerator
from src.calling_sequence.calling_sequence_len_generator import CallingSequenceLenGenerator
from src.ticket_generator.fastest_early_five_ticket_generator import FastestEarlyFiveTicketGenerator
from src.player_generator.player_generator import PlayerGenerator
from src.player.player import Player
from src.caller.caller import Caller
from src.claim_validator.claim_validator import ClaimValidator
from src.game_simulator_logger.game_simulator_file_logger import GameSimulatorFileLogger

from src.common import round_game_type, round_player_index, game_claim_player_index, CALL_SEQ_RANGE_LIMITS, CALL_SEQ_RANDOM_LEN_LIMITS, LOWER_INDEX, UPPER_INDEX, NUM_PLAYERS, possible_claiming_player_types, possible_claiming_player_technically_inaccurate_sub_types, possible_claiming_player_technically_accurate_but_invalid_sub_types, possible_claiming_player_technically_accurate_and_valid_sub_types
import pytest
import time
from pathlib import Path

num_players = NUM_PLAYERS
game_type = round_game_type["FASTEST_EARLY_FIVE"]
claim_player_index = game_claim_player_index["FASTEST_EARLY_FIVE"]
claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]

call_seq_len_gen = CallingSequenceLenGenerator(CALL_SEQ_RANDOM_LEN_LIMITS[LOWER_INDEX], CALL_SEQ_RANDOM_LEN_LIMITS[UPPER_INDEX])
call_seq_len = call_seq_len_gen.generate_calling_sequence_len()

call_seq_gen = CallingSequenceGenerator(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX], call_seq_len)
call_seq = call_seq_gen.generate_calling_sequence()

claim_validator = ClaimValidator(game_type)
player_gen = PlayerGenerator(num_players, game_type, claim_player_index, claim_validator)
player_index_list = round_player_index.values()

caller = Caller(game_type)
caller.call_seq = call_seq

def _create_logging_directory():
        cwd = Path.cwd()
        logdir_relative_path = Path("logs") / Path("TambolaFastestFirstRowGameSimulator")
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


def test_init_tambola_fastest_early_five_game_simulator_game_type_lt_lower_limit_is_not_permitted():
    game_type = 0
    claim_player_index = game_claim_player_index["FASTEST_EARLY_FIVE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]
    
    with pytest.raises(ValueError):
        logdir_pathname = _create_logging_directory()
        logfile_pathname = _create_log_file(logdir_pathname)
        game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)

        ticket_gen = FastestEarlyFiveTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
        tambola_game_simulator = TambolaFastestEarlyFiveGameSimulator(game_type, call_seq_len_gen, call_seq_gen, player_gen, ticket_gen, claim_validator, caller, player_index_list, game_simulator_file_logger)

def test_init_tambola_fastest_early_five_game_simulator_game_type_gt_upper_limit_is_not_permitted():
    game_type = 6    
    claim_player_index = game_claim_player_index["FASTEST_EARLY_FIVE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]

    with pytest.raises(ValueError):
        logdir_pathname = _create_logging_directory()
        logfile_pathname = _create_log_file(logdir_pathname)
        game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)

        ticket_gen = FastestEarlyFiveTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type) 
        tambola_game_simulator = TambolaFastestEarlyFiveGameSimulator(game_type, call_seq_len_gen, call_seq_gen, player_gen, ticket_gen, claim_validator, caller, player_index_list, game_simulator_file_logger)

def test_init_tambola_fastest_early_five_game_simulator_calling_sequence_generator_not_none():
    game_type = round_game_type["FASTEST_EARLY_FIVE"]
    claim_player_index = game_claim_player_index["FASTEST_EARLY_FIVE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]
    
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)

    ticket_gen = FastestEarlyFiveTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    tambola_game_simulator = TambolaFastestEarlyFiveGameSimulator(game_type, call_seq_len_gen, call_seq_gen, player_gen, ticket_gen, claim_validator, caller, player_index_list, game_simulator_file_logger)
    assert tambola_game_simulator.call_seq_gen

def test_init_tambola_fastest_early_five_game_simulator_calling_sequence_len_generator_not_none():
    game_type = round_game_type["FASTEST_EARLY_FIVE"]
    claim_player_index = game_claim_player_index["FASTEST_EARLY_FIVE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]
    
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)

    ticket_gen = FastestEarlyFiveTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    tambola_game_simulator = TambolaFastestEarlyFiveGameSimulator(game_type, call_seq_len_gen, call_seq_gen, player_gen, ticket_gen, claim_validator, caller, player_index_list, game_simulator_file_logger)
    assert tambola_game_simulator.call_seq_len_gen

def test_init_tambola_fastest_early_five_game_simulator_ticket_generator_not_none():
    game_type = round_game_type["FASTEST_EARLY_FIVE"]
    claim_player_index = game_claim_player_index["FASTEST_EARLY_FIVE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]
    
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)

    ticket_gen = FastestEarlyFiveTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    tambola_game_simulator = TambolaFastestEarlyFiveGameSimulator(game_type, call_seq_len_gen, call_seq_gen, player_gen, ticket_gen, claim_validator, caller, player_index_list, game_simulator_file_logger)
    assert tambola_game_simulator.ticket_gen

def test_init_tambola_fastest_early_five_game_simulator_player_generator_not_none():
    game_type = round_game_type["FASTEST_EARLY_FIVE"]
    claim_player_index = game_claim_player_index["FASTEST_EARLY_FIVE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]
    
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)

    ticket_gen = FastestEarlyFiveTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    tambola_game_simulator = TambolaFastestEarlyFiveGameSimulator(game_type, call_seq_len_gen, call_seq_gen, player_gen, ticket_gen, claim_validator, caller, player_index_list, game_simulator_file_logger)
    assert tambola_game_simulator.player_gen

def test_init_tambola_fastest_early_five_game_simulator_claim_validator_not_none():
    game_type = round_game_type["FASTEST_EARLY_FIVE"]
    claim_player_index = game_claim_player_index["FASTEST_EARLY_FIVE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]
    
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)

    ticket_gen = FastestEarlyFiveTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    tambola_game_simulator = TambolaFastestEarlyFiveGameSimulator(game_type, call_seq_len_gen, call_seq_gen, player_gen, ticket_gen, claim_validator, caller, player_index_list, game_simulator_file_logger)
    assert tambola_game_simulator.claim_validator

def test_init_tambola_fastest_early_five_game_simulator_caller_not_none():
    game_type = round_game_type["FASTEST_EARLY_FIVE"]
    claim_player_index = game_claim_player_index["FASTEST_EARLY_FIVE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]
    
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)

    ticket_gen = FastestEarlyFiveTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    tambola_game_simulator = TambolaFastestEarlyFiveGameSimulator(game_type, call_seq_len_gen, call_seq_gen, player_gen, ticket_gen, claim_validator, caller, player_index_list, game_simulator_file_logger)
    assert tambola_game_simulator.claim_validator

def test_init_tambola_fastest_early_five_game_simulator_player_index_list_not_empty():
    game_type = round_game_type["FASTEST_EARLY_FIVE"]
    claim_player_index = game_claim_player_index["FASTEST_EARLY_FIVE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]
    
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)

    ticket_gen = FastestEarlyFiveTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    tambola_game_simulator = TambolaFastestEarlyFiveGameSimulator(game_type, call_seq_len_gen, call_seq_gen, player_gen, ticket_gen, claim_validator, caller, player_index_list, game_simulator_file_logger)
    assert tambola_game_simulator.player_index_list

def test_init_tambola_fastest_early_five_game_simulator_player_index_list_of_expected_len():
    game_type = round_game_type["FASTEST_EARLY_FIVE"]
    claim_player_index = game_claim_player_index["FASTEST_EARLY_FIVE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]
    
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)

    ticket_gen = FastestEarlyFiveTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    tambola_game_simulator = TambolaFastestEarlyFiveGameSimulator(game_type, call_seq_len_gen, call_seq_gen, player_gen, ticket_gen, claim_validator, caller, player_index_list, game_simulator_file_logger)
    assert len(tambola_game_simulator.player_index_list) == NUM_PLAYERS

def test_tambola_fastest_early_five_game_simulator_fastest_third_row_technically_inaccurate_claim_is_rejected_one():
    game_type = round_game_type["FASTEST_EARLY_FIVE"]
    claim_player_index = game_claim_player_index["FASTEST_EARLY_FIVE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_INACCURATE"]
    claiming_player_sub_type = possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_1"]
    
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)

    ticket_gen = FastestEarlyFiveTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    tambola_game_simulator = TambolaFastestEarlyFiveGameSimulator(game_type, call_seq_len_gen, call_seq_gen, player_gen, ticket_gen, claim_validator, caller, player_index_list, game_simulator_file_logger)
    validation_result = tambola_game_simulator.validate_technically_inaccurate_claim()

    assert not validation_result

def test_tambola_fastest_early_five_game_simulator_fastest_third_row_technically_inaccurate_claim_is_rejected_two():
    game_type = round_game_type["FASTEST_EARLY_FIVE"]
    claim_player_index = game_claim_player_index["FASTEST_EARLY_FIVE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_INACCURATE"]
    claiming_player_sub_type = possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_2"]
    
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)

    ticket_gen = FastestEarlyFiveTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    tambola_game_simulator = TambolaFastestEarlyFiveGameSimulator(game_type, call_seq_len_gen, call_seq_gen, player_gen, ticket_gen, claim_validator, caller, player_index_list, game_simulator_file_logger)
    validation_result = tambola_game_simulator.validate_technically_inaccurate_claim()

    assert not validation_result

def test_tambola_fastest_early_five_game_simulator_fastest_third_row_technically_inaccurate_claim_is_rejected_three():
    game_type = round_game_type["FASTEST_EARLY_FIVE"]
    claim_player_index = game_claim_player_index["FASTEST_EARLY_FIVE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_INACCURATE"]
    claiming_player_sub_type = possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_3"]
    
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)

    ticket_gen = FastestEarlyFiveTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    tambola_game_simulator = TambolaFastestEarlyFiveGameSimulator(game_type, call_seq_len_gen, call_seq_gen, player_gen, ticket_gen, claim_validator, caller, player_index_list, game_simulator_file_logger)
    validation_result = tambola_game_simulator.validate_technically_inaccurate_claim()

    assert not validation_result

def test_tambola_fastest_early_five_game_simulator_fastest_third_row_technically_accurate_but_invalid_claim_is_rejected_one():
    game_type = round_game_type["FASTEST_EARLY_FIVE"]
    claim_player_index = game_claim_player_index["FASTEST_EARLY_FIVE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_1"]
    
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)

    ticket_gen = FastestEarlyFiveTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    tambola_game_simulator = TambolaFastestEarlyFiveGameSimulator(game_type, call_seq_len_gen, call_seq_gen, player_gen, ticket_gen, claim_validator, caller, player_index_list, game_simulator_file_logger)
    validation_result = tambola_game_simulator.validate_technically_accurate_but_invalid_claim()

    assert not validation_result

def test_tambola_fastest_early_five_game_simulator_fastest_third_row_technically_accurate_but_invalid_claim_is_rejected_two():
    game_type = round_game_type["FASTEST_EARLY_FIVE"]
    claim_player_index = game_claim_player_index["FASTEST_EARLY_FIVE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_2"]
    
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)

    ticket_gen = FastestEarlyFiveTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    tambola_game_simulator = TambolaFastestEarlyFiveGameSimulator(game_type, call_seq_len_gen, call_seq_gen, player_gen, ticket_gen, claim_validator, caller, player_index_list, game_simulator_file_logger)
    validation_result = tambola_game_simulator.validate_technically_accurate_but_invalid_claim()

    assert not validation_result

def test_tambola_fastest_early_five_game_simulator_fastest_third_row_technically_accurate_but_invalid_claim_is_rejected_three():
    game_type = round_game_type["FASTEST_EARLY_FIVE"]
    claim_player_index = game_claim_player_index["FASTEST_EARLY_FIVE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_3"]
    
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)

    ticket_gen = FastestEarlyFiveTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    tambola_game_simulator = TambolaFastestEarlyFiveGameSimulator(game_type, call_seq_len_gen, call_seq_gen, player_gen, ticket_gen, claim_validator, caller, player_index_list, game_simulator_file_logger)
    validation_result = tambola_game_simulator.validate_technically_accurate_but_invalid_claim()

    assert not validation_result

def test_tambola_fastest_early_five_game_simulator_fastest_third_row_technically_accurate_and_valid_claim_is_accepted_one():
    game_type = round_game_type["FASTEST_EARLY_FIVE"]
    claim_player_index = game_claim_player_index["FASTEST_EARLY_FIVE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]
    
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)

    ticket_gen = FastestEarlyFiveTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    tambola_game_simulator = TambolaFastestEarlyFiveGameSimulator(game_type, call_seq_len_gen, call_seq_gen, player_gen, ticket_gen, claim_validator, caller, player_index_list, game_simulator_file_logger)
    validation_result = tambola_game_simulator.validate_technically_accurate_and_valid_claim()

    assert validation_result

def test_tambola_fastest_early_five_game_simulator_fastest_third_row_technically_accurate_and_valid_claim_is_accepted_two():
    game_type = round_game_type["FASTEST_EARLY_FIVE"]
    claim_player_index = game_claim_player_index["FASTEST_EARLY_FIVE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_2"]
    
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)

    ticket_gen = FastestEarlyFiveTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    tambola_game_simulator = TambolaFastestEarlyFiveGameSimulator(game_type, call_seq_len_gen, call_seq_gen, player_gen, ticket_gen, claim_validator, caller, player_index_list, game_simulator_file_logger)
    validation_result = tambola_game_simulator.validate_technically_accurate_and_valid_claim()

    assert validation_result

def test_tambola_fastest_early_five_game_simulator_fastest_third_row_technically_accurate_and_valid_claim_is_accepted_three():
    game_type = round_game_type["FASTEST_EARLY_FIVE"]
    claim_player_index = game_claim_player_index["FASTEST_EARLY_FIVE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_3"]
    
    logdir_pathname = _create_logging_directory()
    logfile_pathname = _create_log_file(logdir_pathname)
    game_simulator_file_logger = GameSimulatorFileLogger(logfile_pathname)

    ticket_gen = FastestEarlyFiveTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    tambola_game_simulator = TambolaFastestEarlyFiveGameSimulator(game_type, call_seq_len_gen, call_seq_gen, player_gen, ticket_gen, claim_validator, caller, player_index_list, game_simulator_file_logger)
    validation_result = tambola_game_simulator.validate_technically_accurate_and_valid_claim()

    assert validation_result
