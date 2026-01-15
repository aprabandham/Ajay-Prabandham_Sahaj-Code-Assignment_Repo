from src.claim_validator.claim_validator import ClaimValidator
from src.ticket.ticket import Ticket
from src.common import ROW_LEN, NUM_ROWS, LOWER_INDEX, UPPER_INDEX, NUM_TECHNICALLY_INACCURATE_NUMS_IN_ROW, CALL_SEQ_RANGE_LIMITS, LIST_PENULTIMATE_INDEX, LIST_LAST_INDEX, CALL_SEQ_RANDOM_LEN_LIMITS, round_game_type, round_player_index, possible_claiming_player_types, possible_claiming_player_technically_inaccurate_sub_types, possible_claiming_player_technically_accurate_but_invalid_sub_types, possible_claiming_player_technically_accurate_and_valid_sub_types

from random import sample as random_sample, choice as random_choice, shuffle as random_shuffle
import pytest

def generate_call_seq_len():
    call_seq_len_population = range(CALL_SEQ_RANDOM_LEN_LIMITS[LOWER_INDEX], CALL_SEQ_RANDOM_LEN_LIMITS[UPPER_INDEX] + 1)
    numbers = random_sample(call_seq_len_population, CALL_SEQ_RANDOM_LEN_LIMITS[UPPER_INDEX] - CALL_SEQ_RANDOM_LEN_LIMITS[LOWER_INDEX] + 1)
    call_seq_len = random_choice(numbers)

    return call_seq_len

def generate_call_seq(call_seq_len):
    call_seq_population = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX] + 1)
    call_seq = random_sample(call_seq_population, call_seq_len)

    return call_seq

def generate_fastest_first_row_arr_for_ticket_technically_inaccurate_claim(call_seq):
        ticket_arr_first_row = []    
        ticket_arr_first_row_nums = []
        
        first_row_accurate_pop = call_seq
        first_row_accurate_subseq = random_sample(first_row_accurate_pop, ROW_LEN - NUM_TECHNICALLY_INACCURATE_NUMS_IN_ROW)
        ticket_arr_first_row_nums.extend(first_row_accurate_subseq)

        calling_seq_range = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX]+1)
        first_row_inaccurate_pop = list(set(calling_seq_range) - set(call_seq))
        first_row_inaccurate_subseq = random_sample(first_row_inaccurate_pop, NUM_TECHNICALLY_INACCURATE_NUMS_IN_ROW)
        ticket_arr_first_row_nums.extend(first_row_inaccurate_subseq)
        random_shuffle(ticket_arr_first_row_nums)

        first_row_marks = [True] * ROW_LEN
        ticket_arr_first_row.extend(
            list(
                zip(
                    ticket_arr_first_row_nums, 
                    first_row_marks
                )
            )
        )
        return ticket_arr_first_row

def generate_fastest_first_row_arr_for_ticket_technically_accurate_but_invalid_claim(call_seq):
        call_seq_len = len(call_seq)
        
        ticket_arr_first_row = []
        ticket_arr_first_row_nums = []

        seq_penultimate_num = call_seq[LIST_PENULTIMATE_INDEX]
        first_row_pop = call_seq[0:call_seq_len-2]
        first_row_prefix = random_sample(first_row_pop, ROW_LEN-1)
        ticket_arr_first_row_nums.extend(first_row_prefix)
        ticket_arr_first_row_nums.append(seq_penultimate_num)

        first_row_marks = [True] * ROW_LEN
        ticket_arr_first_row.extend(
            list(
                zip(
                    ticket_arr_first_row_nums, 
                    first_row_marks
                )
            )
        )
        return ticket_arr_first_row

def generate_fastest_first_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq):
        call_seq_len = len(call_seq)
        
        ticket_arr_first_row = []
        ticket_arr_first_row_nums = []
        seq_last_num = call_seq[LIST_LAST_INDEX]
        first_row_pop = call_seq[0:call_seq_len-1]
        first_row_prefix = random_sample(first_row_pop, ROW_LEN-1)
        ticket_arr_first_row_nums.extend(first_row_prefix)
        ticket_arr_first_row_nums.append(seq_last_num)

        first_row_marks = [True] * ROW_LEN
        ticket_arr_first_row.extend(
            list(
                zip(
                    ticket_arr_first_row_nums, 
                    first_row_marks
                )
            )
        )
        return ticket_arr_first_row

def generate_fastest_first_row_claim_second_row_arr(call_seq, ticket_arr_first_row):
        ticket_arr_second_row = []
        
        calling_seq_range = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX]+1)
        second_row_pop = list(set(calling_seq_range) - set(ticket_arr_first_row))
        ticket_arr_second_row_nums = random_sample(second_row_pop, ROW_LEN)

        second_row_marks = [random_choice([True, False]) for _ in range(ROW_LEN)]
        ticket_arr_second_row.extend(
            list(
                zip(
                    ticket_arr_second_row_nums, 
                    second_row_marks
                )
            )
        )
        return ticket_arr_second_row

def test_fastest_first_row_claim_validator_init_game_type_not_allowed_one():
    game_type = 0

    with pytest.raises(ValueError):
        game_win_claim_validator = ClaimValidator(game_type)

def test_fastest_first_row_claim_validator_init_game_type_not_allowed_two():
    game_type = 6

    with pytest.raises(ValueError):
        game_win_claim_validator = ClaimValidator(game_type)

def test_fastest_first_row_claim_validator_fastest_first_row_validate_claim_call_seq_len_lt_lower_limit():
    call_seq = [3, 87, 22, 42]
    ticket_arr = []

    game_type = round_game_type["FASTEST_FIRST_ROW"]
    player_index = round_player_index["PLAYER_ONE"]
    claim_player_index = round_player_index["PLAYER_ONE"]

    with pytest.raises(ValueError):
        ticket_arr_first_row = generate_fastest_first_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq)
        ticket_arr_second_row = generate_fastest_first_row_claim_second_row_arr(call_seq, ticket_arr_first_row)
        ticket_arr_third_row = generate_fastest_first_row_claim_second_row_arr(call_seq, ticket_arr_second_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

        game_win_claim_validator = ClaimValidator(game_type)
        validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket)

def test_fastest_first_row_claim_validator_fastest_first_row_validate_claim_call_seq_len_gt_upper_limit():
    call_seq = [i for i in range(1, 100)]
    ticket_arr = []

    game_type = round_game_type["FASTEST_FIRST_ROW"]
    player_index = round_player_index["PLAYER_ONE"]
    claim_player_index = round_player_index["PLAYER_ONE"]
        
    ticket_arr_first_row = generate_fastest_first_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq)
    ticket_arr_second_row = generate_fastest_first_row_claim_second_row_arr(call_seq, ticket_arr_first_row)
    ticket_arr_third_row = generate_fastest_first_row_claim_second_row_arr(call_seq, ticket_arr_second_row)

    ticket_arr.append(ticket_arr_first_row)
    ticket_arr.append(ticket_arr_second_row)
    ticket_arr.append(ticket_arr_third_row)
    ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

    game_win_claim_validator = ClaimValidator(game_type)
    
    with pytest.raises(ValueError):
        validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket)

def test_fastest_first_row_claim_validator_fastest_first_row_validate_claim_ticket_is_none():
    ticket = None

    game_type = round_game_type["FASTEST_FIRST_ROW"]
    player_index = round_player_index["PLAYER_ONE"]
    claim_player_index = round_player_index["PLAYER_ONE"]

    call_seq_len = generate_call_seq_len()
    call_seq = generate_call_seq(call_seq_len)

    game_win_claim_validator = ClaimValidator(game_type)
    
    with pytest.raises(ValueError):
        validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket)

def test_fastest_first_row_claim_validator_fastest_first_row_technically_inaccurate_claim_is_rejected():
        call_seq_len = generate_call_seq_len()
        call_seq = generate_call_seq(call_seq_len)

        game_type = round_game_type["FASTEST_FIRST_ROW"]
        player_index = round_player_index["PLAYER_ONE"]
        claim_player_index = round_player_index["PLAYER_ONE"]

        ticket_arr = []
        
        ticket_arr_first_row = generate_fastest_first_row_arr_for_ticket_technically_inaccurate_claim(call_seq)
        ticket_arr_second_row = generate_fastest_first_row_claim_second_row_arr(call_seq, ticket_arr_first_row)
        ticket_arr_third_row = generate_fastest_first_row_claim_second_row_arr(call_seq, ticket_arr_second_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)        
        game_win_claim_validator = ClaimValidator(game_type)
        validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket)

        assert not validation_result

def test_fastest_first_row_claim_validator_fastest_first_row_technically_accurate_but_invalid_claim_is_rejected():
        call_seq_len = generate_call_seq_len()
        call_seq = generate_call_seq(call_seq_len)

        game_type = round_game_type["FASTEST_FIRST_ROW"]
        player_index = round_player_index["PLAYER_ONE"]
        claim_player_index = round_player_index["PLAYER_ONE"]

        ticket_arr = []
        
        ticket_arr_first_row = generate_fastest_first_row_arr_for_ticket_technically_accurate_but_invalid_claim(call_seq)
        ticket_arr_second_row = generate_fastest_first_row_claim_second_row_arr(call_seq, ticket_arr_first_row)
        ticket_arr_third_row = generate_fastest_first_row_claim_second_row_arr(call_seq, ticket_arr_second_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

        game_win_claim_validator = ClaimValidator(game_type)
        validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket)

        assert not validation_result

def test_fastest_first_row_claim_validator_fastest_first_row_technically_accurate_and_valid_claim_is_accepted():
        call_seq_len = generate_call_seq_len()
        call_seq = generate_call_seq(call_seq_len)

        game_type = round_game_type["FASTEST_FIRST_ROW"]
        player_index = round_player_index["PLAYER_ONE"]
        claim_player_index = round_player_index["PLAYER_ONE"]

        ticket_arr = []
        
        ticket_arr_first_row = generate_fastest_first_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq)
        ticket_arr_second_row = generate_fastest_first_row_claim_second_row_arr(call_seq, ticket_arr_first_row)
        ticket_arr_third_row = generate_fastest_first_row_claim_second_row_arr(call_seq, ticket_arr_second_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

        game_win_claim_validator = ClaimValidator(game_type)
        validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket)

        assert validation_result


def generate_fastest_second_row_arr_for_ticket_technically_accurate_but_invalid_claim(call_seq):
            call_seq_len = len(call_seq)
            
            ticket_arr_second_row = []
            ticket_arr_second_row_nums = []

            seq_penultimate_num = call_seq[LIST_PENULTIMATE_INDEX]
            second_row_pop = call_seq[0:call_seq_len-2]
            second_row_prefix = random_sample(second_row_pop, ROW_LEN-1)
            ticket_arr_second_row_nums.extend(second_row_prefix)
            ticket_arr_second_row_nums.append(seq_penultimate_num)

            second_row_marks = [True] * ROW_LEN
            ticket_arr_second_row.extend(
                list(
                    zip(
                        ticket_arr_second_row_nums, 
                        second_row_marks
                    )
                )
            )
            return ticket_arr_second_row

def generate_fastest_second_row_arr_for_ticket_technically_inaccurate_claim(call_seq):
        ticket_arr_second_row = []    
        ticket_arr_second_row_nums = []
        
        second_row_accurate_pop = call_seq
        second_row_accurate_subseq = random_sample(second_row_accurate_pop, ROW_LEN - NUM_TECHNICALLY_INACCURATE_NUMS_IN_ROW)
        ticket_arr_second_row_nums.extend(second_row_accurate_subseq)

        calling_seq_range = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX]+1)
        second_row_inaccurate_pop = list(set(calling_seq_range) - set(call_seq))
        second_row_inaccurate_subseq = random_sample(second_row_inaccurate_pop, NUM_TECHNICALLY_INACCURATE_NUMS_IN_ROW)
        ticket_arr_second_row_nums.extend(second_row_inaccurate_subseq)
        random_shuffle(ticket_arr_second_row_nums)

        second_row_marks = [True] * ROW_LEN
        ticket_arr_second_row.extend(
            list(
                zip(
                    ticket_arr_second_row_nums, 
                    second_row_marks
                )
            )
        )
        return ticket_arr_second_row

def generate_fastest_second_row_arr_for_ticket_technically_accurate_but_invalid_claim(call_seq):
            call_seq_len = len(call_seq)
            
            ticket_arr_second_row = []
            ticket_arr_second_row_nums = []

            seq_penultimate_num = call_seq[LIST_PENULTIMATE_INDEX]
            second_row_pop = call_seq[0:call_seq_len-2]
            second_row_prefix = random_sample(second_row_pop, ROW_LEN-1)
            ticket_arr_second_row_nums.extend(second_row_prefix)
            ticket_arr_second_row_nums.append(seq_penultimate_num)

            second_row_marks = [True] * ROW_LEN
            ticket_arr_second_row.extend(
                list(
                    zip(
                        ticket_arr_second_row_nums, 
                        second_row_marks
                    )
                )
            )
            return ticket_arr_second_row

def generate_fastest_second_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq):
            call_seq_len = len(call_seq)
            
            ticket_arr_second_row = []
            ticket_arr_second_row_nums = []
            seq_last_num = call_seq[LIST_LAST_INDEX]
            second_row_pop = call_seq[0:call_seq_len-1]
            second_row_prefix = random_sample(second_row_pop, ROW_LEN-1)
            ticket_arr_second_row_nums.extend(second_row_prefix)
            ticket_arr_second_row_nums.append(seq_last_num)

            second_row_marks = [True] * ROW_LEN
            ticket_arr_second_row.extend(
                list(
                    zip(
                        ticket_arr_second_row_nums, 
                        second_row_marks
                    )
                )
            )
            return ticket_arr_second_row

def generate_fastest_second_row_claim_first_row_arr(call_seq, ticket_arr_second_row):
        ticket_arr_first_row = []
        
        calling_seq_range = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX]+1)
        first_row_pop = list(set(calling_seq_range) - set(ticket_arr_second_row))
        ticket_arr_first_row_nums = random_sample(first_row_pop, ROW_LEN)

        first_row_marks = [random_choice([True, False]) for _ in range(ROW_LEN)]
        ticket_arr_first_row.extend(
            list(
                zip(
                    ticket_arr_first_row_nums, 
                    first_row_marks
                )
            )
        )
        return ticket_arr_first_row

def generate_fastest_second_row_claim_third_row_arr(call_seq, ticket_arr_second_row, ticket_arr_first_row):
        ticket_arr_third_row = []
        
        calling_seq_range = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX]+1)
        first_row_pop = list(set(calling_seq_range) - set(ticket_arr_second_row))
        third_row_pop = list(set(first_row_pop) - set(ticket_arr_first_row))
        ticket_arr_third_row_nums = random_sample(third_row_pop, ROW_LEN)
        third_row_marks = [random_choice([True, False]) for _ in range(ROW_LEN)]
        ticket_arr_third_row.extend(
            list(
                zip(
                    ticket_arr_third_row_nums, 
                    third_row_marks
                )
            )
        )
        return ticket_arr_third_row

def test_fastest_second_row_claim_validator_init_game_type_not_allowed_one():
    game_type = 0

    with pytest.raises(ValueError):
        game_win_claim_validator = ClaimValidator(game_type)

def test_fastest_second_row_claim_validator_init_game_type_not_allowed_two():
    game_type = 6

    with pytest.raises(ValueError):
        game_win_claim_validator = ClaimValidator(game_type)

def test_fastest_second_row_claim_validator_fastest_second_row_validate_claim_call_seq_len_lt_lower_limit():
    call_seq = [3, 87, 22, 42]
    ticket_arr = []

    game_type = round_game_type["FASTEST_SECOND_ROW"]
    player_index = round_player_index["PLAYER_THREE"]
    claim_player_index = round_player_index["PLAYER_THREE"]
    
    with pytest.raises(ValueError):
        ticket_arr_second_row = generate_fastest_second_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq)
        ticket_arr_first_row = generate_fastest_second_row_claim_first_row_arr(call_seq, ticket_arr_second_row)
        ticket_arr_third_row = generate_fastest_second_row_claim_third_row_arr(call_seq, ticket_arr_second_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

        game_win_claim_validator = ClaimValidator(game_type)
        validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket)

def test_fastest_second_row_claim_validator_fastest_second_row_validate_claim_call_seq_len_gt_upper_limit():
    call_seq = [i for i in range(1, 100)]
    ticket_arr = []

    game_type = round_game_type["FASTEST_SECOND_ROW"]
    player_index = round_player_index["PLAYER_THREE"]
    claim_player_index = round_player_index["PLAYER_THREE"]
        
    ticket_arr_second_row = generate_fastest_second_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq)
    ticket_arr_first_row = generate_fastest_second_row_claim_first_row_arr(call_seq, ticket_arr_second_row)
    ticket_arr_third_row = generate_fastest_second_row_claim_third_row_arr(call_seq, ticket_arr_second_row, ticket_arr_first_row)

    ticket_arr.append(ticket_arr_first_row)
    ticket_arr.append(ticket_arr_second_row)
    ticket_arr.append(ticket_arr_third_row)
    ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

    game_win_claim_validator = ClaimValidator(game_type)
    
    with pytest.raises(ValueError):
        validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket)

def test_fastest_second_row_claim_validator_fastest_second_row_validate_claim_ticket_is_none():
    ticket = None
    call_seq_len = generate_call_seq_len()
    call_seq = generate_call_seq(call_seq_len)

    game_type = round_game_type["FASTEST_SECOND_ROW"]
    player_index = round_player_index["PLAYER_THREE"]
    claim_player_index = round_player_index["PLAYER_THREE"]

    game_win_claim_validator = ClaimValidator(game_type)
    
    with pytest.raises(ValueError):
        validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket)

def test_fastest_second_row_claim_validator_fastest_second_row_technically_inaccurate_claim_is_rejected():
        call_seq_len = generate_call_seq_len()
        call_seq = generate_call_seq(call_seq_len)

        game_type = round_game_type["FASTEST_SECOND_ROW"]
        player_index = round_player_index["PLAYER_THREE"]
        claim_player_index = round_player_index["PLAYER_THREE"]

        ticket_arr = []
        
        ticket_arr_second_row = generate_fastest_second_row_arr_for_ticket_technically_inaccurate_claim(call_seq)
        ticket_arr_first_row = generate_fastest_second_row_claim_first_row_arr(call_seq, ticket_arr_second_row)
        ticket_arr_third_row = generate_fastest_second_row_claim_third_row_arr(call_seq, ticket_arr_second_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

        game_win_claim_validator = ClaimValidator(game_type)
        validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket)

        assert not validation_result

def test_fastest_second_row_claim_validator_fastest_second_row_technically_accurate_but_invalid_claim_is_rejected():
        call_seq_len = generate_call_seq_len()
        call_seq = generate_call_seq(call_seq_len)

        game_type = round_game_type["FASTEST_SECOND_ROW"]
        player_index = round_player_index["PLAYER_THREE"]
        claim_player_index = round_player_index["PLAYER_THREE"]

        ticket_arr = []
        
        ticket_arr_second_row = generate_fastest_second_row_arr_for_ticket_technically_accurate_but_invalid_claim(call_seq)
        ticket_arr_first_row = generate_fastest_second_row_claim_first_row_arr(call_seq, ticket_arr_second_row)
        ticket_arr_third_row = generate_fastest_second_row_claim_third_row_arr(call_seq, ticket_arr_second_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

        game_win_claim_validator = ClaimValidator(game_type)
        validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket)

        assert not validation_result

def test_fastest_second_row_claim_validator_fastest_second_row_technically_accurate_and_valid_claim_is_accepted():
        call_seq_len = generate_call_seq_len()
        call_seq = generate_call_seq(call_seq_len)

        game_type = round_game_type["FASTEST_SECOND_ROW"]
        player_index = round_player_index["PLAYER_THREE"]
        claim_player_index = round_player_index["PLAYER_THREE"]

        ticket_arr = []
        
        ticket_arr_second_row = generate_fastest_second_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq)
        ticket_arr_first_row = generate_fastest_second_row_claim_first_row_arr(call_seq, ticket_arr_second_row)
        ticket_arr_third_row = generate_fastest_second_row_claim_third_row_arr(call_seq, ticket_arr_second_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

        game_win_claim_validator = ClaimValidator(game_type)
        validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket)

        assert validation_result


def generate_fastest_third_row_arr_for_ticket_technically_inaccurate_claim(call_seq):
        ticket_arr_third_row = []    
        ticket_arr_third_row_nums = []
        
        third_row_accurate_pop = call_seq
        third_row_accurate_subseq = random_sample(third_row_accurate_pop, ROW_LEN - NUM_TECHNICALLY_INACCURATE_NUMS_IN_ROW)
        ticket_arr_third_row_nums.extend(third_row_accurate_subseq)

        calling_seq_range = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX]+1)
        third_row_inaccurate_pop = list(set(calling_seq_range) - set(call_seq))
        third_row_inaccurate_subseq = random_sample(third_row_inaccurate_pop, NUM_TECHNICALLY_INACCURATE_NUMS_IN_ROW)
        ticket_arr_third_row_nums.extend(third_row_inaccurate_subseq)
        random_shuffle(ticket_arr_third_row_nums)

        third_row_marks = [True] * ROW_LEN
        ticket_arr_third_row.extend(
            list(
                zip(
                    ticket_arr_third_row_nums, 
                    third_row_marks
                )
            )
        )
        return ticket_arr_third_row

def generate_fastest_third_row_arr_for_ticket_technically_accurate_but_invalid_claim(call_seq):
        call_seq_len = len(call_seq)
        
        ticket_arr_third_row = []
        ticket_arr_third_row_nums = []

        seq_penultimate_num = call_seq[LIST_PENULTIMATE_INDEX]
        third_row_pop = call_seq[0:call_seq_len-2]
        third_row_prefix = random_sample(third_row_pop, ROW_LEN-1)
        ticket_arr_third_row_nums.extend(third_row_prefix)
        ticket_arr_third_row_nums.append(seq_penultimate_num)

        third_row_marks = [True] * ROW_LEN
        ticket_arr_third_row.extend(
            list(
                zip(
                    ticket_arr_third_row_nums, 
                    third_row_marks
                )
            )
        )
        return ticket_arr_third_row

def generate_fastest_third_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq):
    call_seq_len = len(call_seq)
        
    ticket_arr_third_row = []
    ticket_arr_third_row_nums = []
    seq_last_num = call_seq[LIST_LAST_INDEX]
    third_row_pop = call_seq[0:call_seq_len-1]
    third_row_prefix = random_sample(third_row_pop, ROW_LEN-1)
    ticket_arr_third_row_nums.extend(third_row_prefix)
    ticket_arr_third_row_nums.append(seq_last_num)

    third_row_marks = [True] * ROW_LEN
    ticket_arr_third_row.extend(
        list(
            zip(
                ticket_arr_third_row_nums, 
                third_row_marks
            )
        )
    )
    return ticket_arr_third_row

def generate_fastest_third_row_claim_first_row_arr(call_seq, ticket_arr_third_row):
    ticket_arr_first_row = []
    
    calling_seq_range = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX]+1)
    first_row_pop = list(set(calling_seq_range) - set(ticket_arr_third_row))
    ticket_arr_first_row_nums = random_sample(first_row_pop, ROW_LEN)

    first_row_marks = [random_choice([True, False]) for _ in range(ROW_LEN)]
    ticket_arr_first_row.extend(
        list(
            zip(
                ticket_arr_first_row_nums, 
                first_row_marks
            )
        )
    )
    return ticket_arr_first_row

def generate_fastest_third_row_claim_second_row_arr(call_seq, ticket_arr_third_row, ticket_arr_first_row):
    ticket_arr_second_row = []
    
    calling_seq_range = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX]+1)
    first_row_pop = list(set(calling_seq_range) - set(ticket_arr_third_row))
    second_row_pop = list(set(first_row_pop) - set(ticket_arr_first_row))
    ticket_arr_second_row_nums = random_sample(second_row_pop, ROW_LEN)
    second_row_marks = [random_choice([True, False]) for _ in range(ROW_LEN)]
    ticket_arr_second_row.extend(
        list(
            zip(
                ticket_arr_second_row_nums, 
                second_row_marks
            )
        )
    )
    return ticket_arr_second_row

def generate_fastest_third_row_technically_accurate_and_valid_claim_ticket(call_seq):
        ticket_arr = []

        ticket_arr_third_row = generate_fastest_third_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq)
        ticket_arr_first_row = generate_fastest_third_row_claim_first_row_arr(call_seq, ticket_arr_third_row)
        ticket_arr_second_row = generate_fastest_third_row_claim_second_row_arr(call_seq, ticket_arr_third_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)
        return ticket

def test_fastest_third_row_claim_validator_init_game_type_not_allowed_one():
    game_type = 0

    with pytest.raises(ValueError):
        game_win_claim_validator = ClaimValidator(game_type)

def test_fastest_third_row_claim_validator_init_game_type_not_allowed_two():
    game_type = 6

    with pytest.raises(ValueError):
        game_win_claim_validator = ClaimValidator(game_type)

def test_fastest_third_row_claim_validator_fastest_third_row_validate_claim_call_seq_len_lt_lower_limit():
    call_seq = [3, 87, 22, 42]
    ticket_arr = []

    game_type = round_game_type["FASTEST_THIRD_ROW"]
    player_index = round_player_index["PLAYER_TWO"]
    claim_player_index = round_player_index["PLAYER_TWO"]
    
    with pytest.raises(ValueError):
        ticket_arr_third_row = generate_fastest_third_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq)
        ticket_arr_first_row = generate_fastest_third_row_claim_first_row_arr(call_seq, ticket_arr_third_row)
        ticket_arr_second_row = generate_fastest_third_row_claim_second_row_arr(call_seq, ticket_arr_third_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

        game_win_claim_validator = ClaimValidator(game_type)
        validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket)

def test_fastest_third_row_claim_validator_fastest_third_row_validate_claim_call_seq_len_gt_upper_limit():
    call_seq = [i for i in range(1, 100)]
    ticket_arr = []

    game_type = round_game_type["FASTEST_THIRD_ROW"]
    player_index = round_player_index["PLAYER_TWO"]
    claim_player_index = round_player_index["PLAYER_TWO"]
        
    ticket_arr_third_row = generate_fastest_third_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq)
    ticket_arr_first_row = generate_fastest_third_row_claim_first_row_arr(call_seq, ticket_arr_third_row)
    ticket_arr_second_row = generate_fastest_third_row_claim_second_row_arr(call_seq, ticket_arr_third_row, ticket_arr_first_row)

    ticket_arr.append(ticket_arr_first_row)
    ticket_arr.append(ticket_arr_second_row)
    ticket_arr.append(ticket_arr_third_row)
    ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

    game_win_claim_validator = ClaimValidator(game_type)
    
    with pytest.raises(ValueError):
        validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket)

def test_fastest_third_row_claim_validator_fastest_third_row_validate_claim_ticket_is_none():
    ticket = None
    call_seq_len = generate_call_seq_len()
    call_seq = generate_call_seq(call_seq_len)

    game_type = round_game_type["FASTEST_THIRD_ROW"]
    player_index = round_player_index["PLAYER_TWO"]
    claim_player_index = round_player_index["PLAYER_TWO"]

    game_win_claim_validator = ClaimValidator(game_type)
    
    with pytest.raises(ValueError):
        validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket)

def test_fastest_third_row_claim_validator_fastest_third_row_technically_inaccurate_claim_is_rejected():
        call_seq_len = generate_call_seq_len()
        call_seq = generate_call_seq(call_seq_len)

        game_type = round_game_type["FASTEST_THIRD_ROW"]
        player_index = round_player_index["PLAYER_TWO"]
        claim_player_index = round_player_index["PLAYER_TWO"]

        ticket_arr = []
        
        ticket_arr_third_row = generate_fastest_third_row_arr_for_ticket_technically_inaccurate_claim(call_seq)
        ticket_arr_first_row = generate_fastest_third_row_claim_first_row_arr(call_seq, ticket_arr_third_row)
        ticket_arr_second_row = generate_fastest_third_row_claim_second_row_arr(call_seq, ticket_arr_third_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

        game_win_claim_validator = ClaimValidator(game_type)
        validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket)

        assert not validation_result

def test_fastest_third_row_claim_validator_fastest_third_row_technically_accurate_but_invalid_claim_is_rejected():
        call_seq_len = generate_call_seq_len()
        call_seq = generate_call_seq(call_seq_len)

        game_type = round_game_type["FASTEST_THIRD_ROW"]
        player_index = round_player_index["PLAYER_TWO"]
        claim_player_index = round_player_index["PLAYER_TWO"]

        ticket_arr = []
        
        ticket_arr_third_row = generate_fastest_third_row_arr_for_ticket_technically_accurate_but_invalid_claim(call_seq)
        ticket_arr_first_row = generate_fastest_third_row_claim_first_row_arr(call_seq, ticket_arr_third_row)
        ticket_arr_second_row = generate_fastest_third_row_claim_second_row_arr(call_seq, ticket_arr_third_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

        game_win_claim_validator = ClaimValidator(game_type)
        validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket)

        assert not validation_result

def test_fastest_third_row_claim_validator_fastest_third_row_technically_accurate_and_valid_claim_is_accepted():
        call_seq_len = generate_call_seq_len()
        call_seq = generate_call_seq(call_seq_len)

        game_type = round_game_type["FASTEST_THIRD_ROW"]
        player_index = round_player_index["PLAYER_TWO"]
        claim_player_index = round_player_index["PLAYER_TWO"]

        ticket_arr = []
        
        ticket_arr_third_row = generate_fastest_third_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq)
        ticket_arr_first_row = generate_fastest_third_row_claim_first_row_arr(call_seq, ticket_arr_third_row)
        ticket_arr_second_row = generate_fastest_third_row_claim_second_row_arr(call_seq, ticket_arr_third_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

        game_win_claim_validator = ClaimValidator(game_type)
        validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket)

        assert validation_result


def generate_row_arr_for_ticket_technically_inaccurate_claim(call_seq):
        ticket_arr_row = []    
        ticket_arr_row_nums = []
        
        row_accurate_pop = call_seq
        row_accurate_subseq = random_sample(row_accurate_pop, ROW_LEN - NUM_TECHNICALLY_INACCURATE_NUMS_IN_ROW)
        ticket_arr_row_nums.extend(row_accurate_subseq)

        
        calling_seq_range = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX]+1)
        row_inaccurate_pop = list(set(calling_seq_range) - set(call_seq))
        row_inaccurate_subseq = random_sample(row_inaccurate_pop, NUM_TECHNICALLY_INACCURATE_NUMS_IN_ROW)
        ticket_arr_row_nums.extend(row_inaccurate_subseq)
        random_shuffle(ticket_arr_row_nums)

        row_marks = [False] * ROW_LEN
        for i, num in enumerate(ticket_arr_row_nums):
            if num in call_seq:
                row_marks[i] = True

        ticket_arr_row.extend(
            list(
                zip(
                    ticket_arr_row_nums, 
                    row_marks
                )
            )
        )
        return ticket_arr_row

def generate_row_arr_for_ticket_technically_inaccurate_claim_one(call_seq, row_one):
        ticket_arr_row = []
        
        calling_seq_range = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX]+1)
        row_pop = list(set(calling_seq_range) - set(call_seq).intersection(set(row_one)))
        ticket_arr_row_nums = random_sample(row_pop, ROW_LEN)

        row_marks = [False] * ROW_LEN
        for i, num in enumerate(ticket_arr_row_nums):
            if num in call_seq:
                row_marks[i] = True

        ticket_arr_row.extend(
            list(
                zip(
                    ticket_arr_row_nums, 
                    row_marks
                )
            )
        )
        return ticket_arr_row

def generate_row_arr_for_ticket_technically_inaccurate_claim_two(call_seq, row_one, row_two):
        ticket_arr_row = []
        
        calling_seq_range = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX]+1)
        first_row_pop = list(set(calling_seq_range) - set(row_one))
        second_row_pop = list(set(first_row_pop) - set(row_two))
        ticket_arr_row_nums = random_sample(second_row_pop, ROW_LEN)

        row_marks = [False] * ROW_LEN
        for i, num in enumerate(ticket_arr_row_nums):
            if num in call_seq:
                row_marks[i] = True
        
        ticket_arr_row.extend(
            list(
                zip(
                    ticket_arr_row_nums, 
                    row_marks
                )
            )
        )
        return ticket_arr_row    

def generate_row_arr_for_ticket_technically_accurate_but_invalid_claim(call_seq):
            call_seq_len = len(call_seq)
            
            ticket_arr_row = []
            ticket_arr_row_nums = []

            seq_penultimate_num = call_seq[LIST_PENULTIMATE_INDEX]
            row_pop = call_seq[0:call_seq_len-2]
            row_prefix = random_sample(row_pop, ROW_LEN-1)
            ticket_arr_row_nums.extend(row_prefix)
            ticket_arr_row_nums.append(seq_penultimate_num)

            row_marks = [True] * ROW_LEN
            ticket_arr_row.extend(
                list(
                    zip(
                        ticket_arr_row_nums, 
                        row_marks
                    )
                )
            )
            return ticket_arr_row

def generate_row_arr_for_ticket_technically_accurate_but_invalid_claim_one(call_seq, row_one):
        ticket_arr_row = []
        call_seq_len = len(call_seq)

        row_pop = list(set(call_seq[0:call_seq_len-1]) - set(row_one))
        ticket_arr_row_nums = random_sample(row_pop, ROW_LEN)

        row_marks = [True] * ROW_LEN
        ticket_arr_row.extend(
            list(
                zip(
                    ticket_arr_row_nums, 
                    row_marks
                )
            )
        )
        return ticket_arr_row

def generate_row_arr_for_ticket_technically_accurate_but_invalid_claim_two(call_seq, row_one, row_two):
        ticket_arr_row = []
        call_seq_len = len(call_seq)
        
        first_row_pop = list(set(call_seq[0:call_seq_len-1]) - set(row_one))
        second_row_pop = list(set(first_row_pop) - set(row_two))
        ticket_arr_row_nums = random_sample(second_row_pop, ROW_LEN)

        row_marks = [True] * ROW_LEN
        ticket_arr_row.extend(
            list(
                zip(
                    ticket_arr_row_nums, 
                    row_marks
                )
            )
        )
        return ticket_arr_row

def generate_row_arr_for_ticket_technically_accurate_and_valid_claim_one(call_seq, row_one):
        ticket_arr_row = []
        
        row_pop = list(set(call_seq) - set(row_one))
        ticket_arr_row_nums = random_sample(row_pop, ROW_LEN)

        row_marks = [True] * ROW_LEN
        ticket_arr_row.extend(
            list(
                zip(
                    ticket_arr_row_nums, 
                    row_marks
                )
            )
        )
        return ticket_arr_row

def generate_row_arr_for_ticket_technically_accurate_and_valid_claim_two(call_seq, row_one, row_two):
        ticket_arr_row = []
        
        first_row_pop = list(set(call_seq) - set(row_one))
        second_row_pop = list(set(first_row_pop) - set(row_two))
        ticket_arr_row_nums = random_sample(second_row_pop, ROW_LEN)
        row_marks = [True] * ROW_LEN
        ticket_arr_row.extend(
            list(
                zip(
                    ticket_arr_row_nums, 
                    row_marks
                )
            )
        )
        return ticket_arr_row

def generate_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq):
            call_seq_len = len(call_seq)
            
            ticket_arr_row = []
            ticket_arr_row_nums = []
            seq_last_num = call_seq[LIST_LAST_INDEX]
            row_pop = call_seq[0:call_seq_len-1]
            row_prefix = random_sample(row_pop, ROW_LEN-1)
            ticket_arr_row_nums.extend(row_prefix)
            ticket_arr_row_nums.append(seq_last_num)

            row_marks = [True] * ROW_LEN
            ticket_arr_row.extend(
                list(
                    zip(
                        ticket_arr_row_nums, 
                        row_marks
                    )
                )
            )
            return ticket_arr_row

def test_fastest_full_house_claim_validator_init_game_type_not_allowed_one():
    game_type = 0

    with pytest.raises(ValueError):
        game_win_claim_validator = ClaimValidator(game_type)

def test_fastest_full_house_claim_validator_init_game_type_not_allowed_two():
    game_type = 6

    with pytest.raises(ValueError):
        game_win_claim_validator = ClaimValidator(game_type)

def test_fastest_full_house_claim_validator_fastest_full_house_validate_claim_call_seq_len_lt_lower_limit():
    call_seq = [3, 87, 22, 42]
    ticket_arr = []

    game_type = round_game_type["FASTEST_FULL_HOUSE"]
    player_index = round_player_index["PLAYER_FOUR"]
    claim_player_index = round_player_index["PLAYER_FOUR"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]
    
    with pytest.raises(ValueError):
        ticket_arr_first_row = generate_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq)
        ticket_arr_second_row = generate_row_arr_for_ticket_technically_accurate_and_valid_claim_one(call_seq, ticket_arr_first_row)
        ticket_arr_third_row = generate_row_arr_for_ticket_technically_accurate_and_valid_claim_two(call_seq, ticket_arr_first_row, ticket_arr_second_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

        game_win_claim_validator = ClaimValidator(game_type)
        
        validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket, claiming_player_type, claiming_player_sub_type)

def test_fastest_full_house_claim_validator_fastest_full_house_validate_claim_call_seq_len_gt_upper_limit():
    call_seq = [i for i in range(1, 100)]
    ticket_arr = []

    game_type = round_game_type["FASTEST_FULL_HOUSE"]
    player_index = round_player_index["PLAYER_FOUR"]
    claim_player_index = round_player_index["PLAYER_FOUR"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]
        
    ticket_arr_first_row = generate_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq)
    ticket_arr_second_row = generate_row_arr_for_ticket_technically_accurate_and_valid_claim_one(call_seq, ticket_arr_first_row)
    ticket_arr_third_row = generate_row_arr_for_ticket_technically_accurate_and_valid_claim_two(call_seq, ticket_arr_first_row, ticket_arr_second_row)

    ticket_arr.append(ticket_arr_first_row)
    ticket_arr.append(ticket_arr_second_row)
    ticket_arr.append(ticket_arr_third_row)
    ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

    game_win_claim_validator = ClaimValidator(game_type)
    
    with pytest.raises(ValueError):
        validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket, claiming_player_type, claiming_player_sub_type)

def test_fastest_full_house_claim_validator_fastest_full_house_validate_claim_ticket_is_none():
    ticket = None
    call_seq_len = generate_call_seq_len()
    call_seq = generate_call_seq(call_seq_len)

    game_type = round_game_type["FASTEST_FULL_HOUSE"]
    player_index = round_player_index["PLAYER_FOUR"]
    claim_player_index = round_player_index["PLAYER_FOUR"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]

    game_win_claim_validator = ClaimValidator(game_type)
    
    with pytest.raises(ValueError):
        validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket, claiming_player_type, claiming_player_sub_type)

def test_fastest_full_house_claim_validator_fastest_full_house_technically_inaccurate_claim_is_rejected_one():
        call_seq_len = generate_call_seq_len()
        call_seq = generate_call_seq(call_seq_len)

        game_type = round_game_type["FASTEST_FULL_HOUSE"]
        player_index = round_player_index["PLAYER_FOUR"]
        claim_player_index = round_player_index["PLAYER_FOUR"]
        claiming_player_type = possible_claiming_player_types["TECHNICALLY_INACCURATE"]
        claiming_player_sub_type = possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_1"]

        ticket_arr = []
        
        ticket_arr_first_row = generate_row_arr_for_ticket_technically_inaccurate_claim(call_seq)
        ticket_arr_second_row = generate_row_arr_for_ticket_technically_inaccurate_claim_one(call_seq, ticket_arr_first_row)
        ticket_arr_third_row = generate_row_arr_for_ticket_technically_inaccurate_claim_two(call_seq, ticket_arr_first_row, ticket_arr_second_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

        game_win_claim_validator = ClaimValidator(game_type)

        try:
            validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket, claiming_player_type, claiming_player_sub_type)
        except ValueError as e:
            print(f"Original Error Message: {e}")
        except Exception as err:
            print(f"Original Error Message: {err}")
        else:
            assert not validation_result

def test_fastest_full_house_claim_validator_fastest_full_house_technically_inaccurate_claim_is_rejected_two():
        call_seq_len = generate_call_seq_len()
        call_seq = generate_call_seq(call_seq_len)

        game_type = round_game_type["FASTEST_FULL_HOUSE"]
        player_index = round_player_index["PLAYER_FOUR"]
        claim_player_index = round_player_index["PLAYER_FOUR"]
        claiming_player_type = possible_claiming_player_types["TECHNICALLY_INACCURATE"]
        claiming_player_sub_type = possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_2"]
        
        ticket_arr = []
        
        ticket_arr_second_row = generate_row_arr_for_ticket_technically_inaccurate_claim(call_seq)
        ticket_arr_first_row = generate_row_arr_for_ticket_technically_inaccurate_claim_one(call_seq, ticket_arr_second_row)
        ticket_arr_third_row = generate_row_arr_for_ticket_technically_inaccurate_claim_two(call_seq, ticket_arr_second_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

        game_win_claim_validator = ClaimValidator(game_type)
        
        try:
            validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket, claiming_player_type, claiming_player_sub_type)
        except ValueError as e:
            print(f"Original Error Message: {e}")
        except Exception as err:
            print(f"Original Error Message: {err}")
        else:
            assert not validation_result

def test_fastest_full_house_claim_validator_fastest_full_house_technically_inaccurate_claim_is_rejected_three():
        call_seq_len = generate_call_seq_len()
        call_seq = generate_call_seq(call_seq_len)

        game_type = round_game_type["FASTEST_FULL_HOUSE"]
        player_index = round_player_index["PLAYER_FOUR"]
        claim_player_index = round_player_index["PLAYER_FOUR"]
        claiming_player_type = possible_claiming_player_types["TECHNICALLY_INACCURATE"]
        claiming_player_sub_type = possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_3"]

        ticket_arr = []
        
        ticket_arr_third_row = generate_row_arr_for_ticket_technically_inaccurate_claim(call_seq)
        ticket_arr_first_row = generate_row_arr_for_ticket_technically_inaccurate_claim_one(call_seq, ticket_arr_third_row)
        ticket_arr_second_row = generate_row_arr_for_ticket_technically_inaccurate_claim_two(call_seq, ticket_arr_third_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

        game_win_claim_validator = ClaimValidator(game_type)
        
        try:
            validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket, claiming_player_type, claiming_player_sub_type)
        except ValueError as e:
            print(f"Original Error Message: {e}")
        except Exception as err:
            print(f"Original Error Message: {err}")
        else:
            assert not validation_result

def test_fastest_full_house_claim_validator_fastest_full_house_technically_accurate_but_invalid_claim_is_rejected_one():
        call_seq_len = generate_call_seq_len()
        call_seq = generate_call_seq(call_seq_len)

        game_type = round_game_type["FASTEST_FULL_HOUSE"]
        player_index = round_player_index["PLAYER_FOUR"]
        claim_player_index = round_player_index["PLAYER_FOUR"]
        claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"]
        claiming_player_sub_type = possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_1"]

        ticket_arr = []
        
        ticket_arr_first_row = generate_row_arr_for_ticket_technically_accurate_but_invalid_claim(call_seq)
        ticket_arr_second_row = generate_row_arr_for_ticket_technically_accurate_but_invalid_claim_one(call_seq, ticket_arr_first_row)
        ticket_arr_third_row = generate_row_arr_for_ticket_technically_accurate_but_invalid_claim_two(call_seq, ticket_arr_first_row, ticket_arr_second_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

        game_win_claim_validator = ClaimValidator(game_type)
        
        try:
            validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket, claiming_player_type, claiming_player_sub_type)
        except ValueError as e:
            print(f"Original Error Message: {e}")
        except Exception as err:
            print(f"Original Error Message: {err}")
        else:
            assert not validation_result

def test_fastest_full_house_claim_validator_fastest_full_house_technically_accurate_but_invalid_claim_is_rejected_two():
        call_seq_len = generate_call_seq_len()
        call_seq = generate_call_seq(call_seq_len)

        game_type = round_game_type["FASTEST_FULL_HOUSE"]
        player_index = round_player_index["PLAYER_FOUR"]
        claim_player_index = round_player_index["PLAYER_FOUR"]
        claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"]
        claiming_player_sub_type = possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_2"]

        ticket_arr = []
        
        ticket_arr_second_row = generate_row_arr_for_ticket_technically_accurate_but_invalid_claim(call_seq)
        ticket_arr_first_row = generate_row_arr_for_ticket_technically_accurate_but_invalid_claim_one(call_seq, ticket_arr_second_row)
        ticket_arr_third_row = generate_row_arr_for_ticket_technically_accurate_but_invalid_claim_two(call_seq, ticket_arr_second_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

        game_win_claim_validator = ClaimValidator(game_type)
        
        try:
            validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket, claiming_player_type, claiming_player_sub_type)
        except ValueError as e:
            print(f"Original Error Message: {e}")
        except Exception as err:
            print(f"Original Error Message: {err}")
        else:
            assert not validation_result

def test_fastest_full_house_claim_validator_fastest_full_house_technically_accurate_but_invalid_claim_is_rejected_three():
        call_seq_len = generate_call_seq_len()
        call_seq = generate_call_seq(call_seq_len)

        game_type = round_game_type["FASTEST_FULL_HOUSE"]
        player_index = round_player_index["PLAYER_FOUR"]
        claim_player_index = round_player_index["PLAYER_FOUR"]
        claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"]
        claiming_player_sub_type = possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_3"]

        ticket_arr = []
        
        ticket_arr_third_row = generate_row_arr_for_ticket_technically_accurate_but_invalid_claim(call_seq)
        ticket_arr_first_row = generate_row_arr_for_ticket_technically_accurate_but_invalid_claim_one(call_seq, ticket_arr_third_row)
        ticket_arr_second_row = generate_row_arr_for_ticket_technically_accurate_but_invalid_claim_two(call_seq, ticket_arr_third_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

        game_win_claim_validator = ClaimValidator(game_type)
        
        try:
            validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket, claiming_player_type, claiming_player_sub_type)
        except ValueError as e:
            print(f"Original Error Message: {e}")
        except Exception as err:
            print(f"Original Error Message: {err}")
        else:
            assert not validation_result

def test_fastest_full_house_claim_validator_fastest_full_house_technically_accurate_and_valid_claim_is_accepted_one():
        call_seq_len = generate_call_seq_len()
        call_seq = generate_call_seq(call_seq_len)

        game_type = round_game_type["FASTEST_FULL_HOUSE"]
        player_index = round_player_index["PLAYER_FOUR"]
        claim_player_index = round_player_index["PLAYER_FOUR"]
        claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
        claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]

        ticket_arr = []
        
        ticket_arr_first_row = generate_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq)
        ticket_arr_second_row = generate_row_arr_for_ticket_technically_accurate_and_valid_claim_one(call_seq, ticket_arr_first_row)
        ticket_arr_third_row = generate_row_arr_for_ticket_technically_accurate_and_valid_claim_two(call_seq, ticket_arr_first_row, ticket_arr_second_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

        game_win_claim_validator = ClaimValidator(game_type)
        
        try:
            validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket, claiming_player_type, claiming_player_sub_type)
        except ValueError as e:
            print(f"Original Error Message: {e}")
        except Exception as err:
            print(f"Original Error Message: {err}")
        else:
            assert validation_result

def test_fastest_full_house_claim_validator_fastest_full_house_technically_accurate_and_valid_claim_is_accepted_two():
        call_seq_len = generate_call_seq_len()
        call_seq = generate_call_seq(call_seq_len)

        game_type = round_game_type["FASTEST_FULL_HOUSE"]
        player_index = round_player_index["PLAYER_FOUR"]
        claim_player_index = round_player_index["PLAYER_FOUR"]
        claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
        claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_2"]

        ticket_arr = []
        
        ticket_arr_second_row = generate_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq)
        ticket_arr_first_row = generate_row_arr_for_ticket_technically_accurate_and_valid_claim_one(call_seq, ticket_arr_second_row)
        ticket_arr_third_row = generate_row_arr_for_ticket_technically_accurate_and_valid_claim_two(call_seq, ticket_arr_second_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

        game_win_claim_validator = ClaimValidator(game_type)
        
        try:
            validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket, claiming_player_type, claiming_player_sub_type)
        except ValueError as e:
            print(f"Original Error Message: {e}")
        except Exception as err:
            print(f"Original Error Message: {err}")
        else:
            assert validation_result

def test_fastest_full_house_claim_validator_fastest_full_house_technically_accurate_and_valid_claim_is_accepted_three():
        call_seq_len = generate_call_seq_len()
        call_seq = generate_call_seq(call_seq_len)

        game_type = round_game_type["FASTEST_FULL_HOUSE"]
        player_index = round_player_index["PLAYER_FOUR"]
        claim_player_index = round_player_index["PLAYER_FOUR"]
        claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
        claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_3"]

        ticket_arr = []
        
        ticket_arr_third_row = generate_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq)
        ticket_arr_first_row = generate_row_arr_for_ticket_technically_accurate_and_valid_claim_one(call_seq, ticket_arr_third_row)
        ticket_arr_second_row = generate_row_arr_for_ticket_technically_accurate_and_valid_claim_two(call_seq, ticket_arr_third_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)

        game_win_claim_validator = ClaimValidator(game_type)
        
        try:
            validation_result = game_win_claim_validator.validate_player_claim(call_seq, ticket, claiming_player_type, claiming_player_sub_type)
        except ValueError as e:
            print(f"Original Error Message: {e}")
        except Exception as err:
            print(f"Original Error Message: {err}")
        else:
            assert validation_result
