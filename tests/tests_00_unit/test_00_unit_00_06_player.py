from src.player.player import Player
from src.ticket.ticket import Ticket
from src.common import ROW_LEN, NUM_ROWS, LOWER_INDEX, UPPER_INDEX, NUM_TECHNICALLY_INACCURATE_NUMS_IN_ROW, CALL_SEQ_RANGE_LIMITS, LIST_PENULTIMATE_INDEX, LIST_LAST_INDEX, CALL_SEQ_RANDOM_LEN_LIMITS, round_game_type, round_player_index, possible_claiming_player_types, possible_claiming_player_technically_inaccurate_sub_types, possible_claiming_player_technically_accurate_but_invalid_sub_types, possible_claiming_player_technically_accurate_and_valid_sub_types, game_claim_player_index
from src.claim_validator.claim_validator import ClaimValidator

from random import sample as random_sample, choice as random_choice
import pytest

game_type = round_game_type["FASTEST_FIRST_ROW"]
player_index = round_player_index["PLAYER_ONE"]
claim_player_index = game_claim_player_index["FASTEST_FIRST_ROW"]

claim_validator = ClaimValidator(game_type)

def generate_call_seq_len():
    call_seq_len_population = range(CALL_SEQ_RANDOM_LEN_LIMITS[LOWER_INDEX], CALL_SEQ_RANDOM_LEN_LIMITS[UPPER_INDEX] + 1)
    numbers = random_sample(call_seq_len_population, CALL_SEQ_RANDOM_LEN_LIMITS[UPPER_INDEX] - CALL_SEQ_RANDOM_LEN_LIMITS[LOWER_INDEX] + 1)
    call_seq_len = random_choice(numbers)

    return call_seq_len

def generate_call_seq(call_seq_len):
    call_seq_population = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX] + 1)
    call_seq = random_sample(call_seq_population, call_seq_len)

    return call_seq

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

def generate_fastest_first_row_claim_third_row_arr(call_seq, ticket_arr_first_row, ticket_arr_second_row):
    ticket_arr_third_row = []
    
    calling_seq_range = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX]+1)
    second_row_pop = list(set(calling_seq_range) - set(ticket_arr_first_row))
    third_row_pop = list(set(second_row_pop) - set(ticket_arr_second_row))
    ticket_arr_third_row_nums = random_sample(third_row_pop, ROW_LEN)
    third_row_marks = [random_choice([True, False]) for _ in range(ROW_LEN)]
    ticket_arr_third_row.extend(
        list(
            zip(
                ticket_arr_second_row_nums, 
                second_row_marks
            )
        )
    )
    return ticket_arr_third_row

def generate_fastest_first_row_technically_accurate_and_valid_claim_ticket(call_seq):
        ticket_arr = []

        ticket_arr_first_row = generate_fastest_first_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq)
        ticket_arr_second_row = generate_fastest_first_row_claim_second_row_arr(call_seq, ticket_arr_first_row)
        ticket_arr_third_row = generate_fastest_first_row_claim_second_row_arr(call_seq, ticket_arr_second_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)
        return ticket

def test_init_fastest_first_row_player_player_index_not_lt_lower_limit():
    player_index = 0

    with pytest.raises(ValueError):
        player = Player(player_index, game_type, claim_validator)

def test_init_fastest_first_row_player_player_index_not_gt_upper_limit():
    player_index = 5

    with pytest.raises(ValueError):
        player = Player(player_index, game_type, claim_validator)

def test_init_fastest_first_row_player_game_type_not_lt_lower_limit():
    game_type = 0

    with pytest.raises(ValueError):
        player = Player(player_index, game_type, claim_validator)

def test_init_fastest_first_row_player_game_type_not_gt_upper_limit():
    game_type = 6

    with pytest.raises(ValueError):
        player = Player(player_index, game_type, claim_validator)

def test_fastest_first_row_player_assign_ticket_ticket_not_none():
    player = Player(player_index, game_type, claim_validator)

    call_seq_len = generate_call_seq_len()
    call_seq = generate_call_seq(call_seq_len)
    ticket = generate_fastest_first_row_technically_accurate_and_valid_claim_ticket(call_seq)

    player.assign_ticket(ticket)
    ticket = player.ticket

    assert ticket

def test_fastest_first_row_player_non_claim_player_claim_not_allowed():
    player_index = 2
    player = Player(player_index, game_type, claim_validator)

    call_seq_len = generate_call_seq_len()
    call_seq = generate_call_seq(call_seq_len)
    ticket = generate_fastest_first_row_technically_accurate_and_valid_claim_ticket(call_seq)

    player.assign_ticket(ticket)
    
    with pytest.raises(ValueError):
        player.raise_game_win_claim(call_seq)


game_type = round_game_type["FASTEST_SECOND_ROW"]
player_index = round_player_index["PLAYER_THREE"]
claim_player_index = game_claim_player_index["FASTEST_SECOND_ROW"]
claim_validator = ClaimValidator(game_type)

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

def generate_fastest_second_row_technically_accurate_and_valid_claim_ticket(call_seq):
        ticket_arr = []

        ticket_arr_second_row = generate_fastest_second_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq)
        ticket_arr_first_row = generate_fastest_second_row_claim_first_row_arr(call_seq, ticket_arr_second_row)
        ticket_arr_third_row = generate_fastest_second_row_claim_third_row_arr(call_seq, ticket_arr_second_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        ticket = Ticket(ticket_arr, game_type, player_index, claim_player_index)
        return ticket

def test_init_fastest_second_row_player_player_index_not_lt_lower_limit():
    player_index = 0

    with pytest.raises(ValueError):
        player = Player(player_index, game_type, claim_validator)

def test_init_fastest_second_row_player_player_index_not_gt_upper_limit():
    player_index = 5

    with pytest.raises(ValueError):
        player = Player(player_index, game_type, claim_validator)

def test_init_fastest_second_row_player_game_type_not_lt_lower_limit():
    game_type = 0

    with pytest.raises(ValueError):
        player = Player(player_index, game_type, claim_validator)

def test_init_fastest_second_row_player_game_type_not_gt_upper_limit():
    game_type = 6

    with pytest.raises(ValueError):
        player = Player(player_index, game_type, claim_validator)

def test_fastest_second_row_player_assign_ticket_ticket_not_none():
    player = Player(player_index, game_type, claim_validator)

    call_seq_len = generate_call_seq_len()
    call_seq = generate_call_seq(call_seq_len)
    ticket = generate_fastest_second_row_technically_accurate_and_valid_claim_ticket(call_seq)

    player.assign_ticket(ticket)
    ticket = player.ticket

    assert ticket

def test_fastest_second_row_player_non_claim_player_claim_not_allowed():
    player_index = 2
    player = Player(player_index, game_type, claim_validator)

    call_seq_len = generate_call_seq_len()
    call_seq = generate_call_seq(call_seq_len)
    ticket = generate_fastest_second_row_technically_accurate_and_valid_claim_ticket(call_seq)

    player.assign_ticket(ticket)
    
    with pytest.raises(ValueError):
        player.raise_game_win_claim(call_seq)


game_type = round_game_type["FASTEST_THIRD_ROW"]
player_index = round_player_index["PLAYER_TWO"]
claim_player_index = game_claim_player_index["FASTEST_THIRD_ROW"]

claim_validator = ClaimValidator(game_type)

def generate_call_seq_len():
    call_seq_len_population = range(CALL_SEQ_RANDOM_LEN_LIMITS[LOWER_INDEX], CALL_SEQ_RANDOM_LEN_LIMITS[UPPER_INDEX] + 1)
    numbers = random_sample(call_seq_len_population, CALL_SEQ_RANDOM_LEN_LIMITS[UPPER_INDEX] - CALL_SEQ_RANDOM_LEN_LIMITS[LOWER_INDEX] + 1)
    call_seq_len = random_choice(numbers)

    return call_seq_len

def generate_call_seq(call_seq_len):
    call_seq_population = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX] + 1)
    call_seq = random_sample(call_seq_population, call_seq_len)

    return call_seq

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

def test_init_fastest_third_row_player_player_index_not_lt_lower_limit():
    player_index = 0

    with pytest.raises(ValueError):
        player = Player(player_index, game_type, claim_validator)

def test_init_fastest_third_row_player_player_index_not_gt_upper_limit():
    player_index = 5

    with pytest.raises(ValueError):
        player = Player(player_index, game_type, claim_validator)

def test_init_fastest_third_row_player_game_type_not_lt_lower_limit():
    game_type = 0

    with pytest.raises(ValueError):
        player = Player(player_index, game_type, claim_validator)

def test_init_fastest_third_row_player_game_type_not_gt_upper_limit():
    game_type = 6

    with pytest.raises(ValueError):
        player = Player(player_index, game_type, claim_validator)

def test_fastest_third_row_player_assign_ticket_ticket_not_none():
    player = Player(player_index, game_type, claim_validator)

    call_seq_len = generate_call_seq_len()
    call_seq = generate_call_seq(call_seq_len)
    ticket = generate_fastest_third_row_technically_accurate_and_valid_claim_ticket(call_seq)

    player.assign_ticket(ticket)
    ticket = player.ticket

    assert ticket

def test_fastest_third_row_player_non_claim_player_claim_not_allowed():
    player_index = 1
    player = Player(player_index, game_type, claim_validator)

    call_seq_len = generate_call_seq_len()
    call_seq = generate_call_seq(call_seq_len)
    ticket = generate_fastest_third_row_technically_accurate_and_valid_claim_ticket(call_seq)

    player.assign_ticket(ticket)
    
    with pytest.raises(ValueError):
        player.raise_game_win_claim(call_seq)


game_type = round_game_type["FASTEST_FULL_HOUSE"]
player_index = round_player_index["PLAYER_FOUR"]
claim_player_index = game_claim_player_index["FASTEST_FULL_HOUSE"]

claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]

claim_validator = ClaimValidator(game_type)

def generate_call_seq_len():
    call_seq_len_population = range(CALL_SEQ_RANDOM_LEN_LIMITS[LOWER_INDEX], CALL_SEQ_RANDOM_LEN_LIMITS[UPPER_INDEX] + 1)
    numbers = random_sample(call_seq_len_population, CALL_SEQ_RANDOM_LEN_LIMITS[UPPER_INDEX] - CALL_SEQ_RANDOM_LEN_LIMITS[LOWER_INDEX] + 1)
    call_seq_len = random_choice(numbers)

    return call_seq_len

def generate_call_seq(call_seq_len):
    call_seq_population = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX] + 1)
    call_seq = random_sample(call_seq_population, call_seq_len)

    return call_seq

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

def generate_row_arr_for_ticket_technically_accurate_but_invalid_claim_zero(call_seq):
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
        
        calling_seq_range = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX]+1)
        row_pop = list(set(calling_seq_range) - set(row_one))
        ticket_arr_row_nums = random_sample(row_pop, ROW_LEN)

        row_marks = [random_choice([True, False]) for _ in range(ROW_LEN)]
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
        
        calling_seq_range = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX]+1)
        first_row_pop = list(set(calling_seq_range) - set(row_one))
        second_row_pop = list(set(first_row_pop) - set(row_two))
        ticket_arr_row_nums = random_sample(second_row_pop, ROW_LEN)
        row_marks = [random_choice([True, False]) for _ in range(ROW_LEN)]
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

def generate_ticket_with_technically_accurate_and_valid_claim_type_1(call_seq):
        ticket_arr = []
        ticket_arr_first_row = generate_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq)
        ticket_arr_second_row = generate_row_arr_for_ticket_technically_accurate_but_invalid_claim_one(call_seq, ticket_arr_first_row)
        ticket_arr_third_row = generate_row_arr_for_ticket_technically_accurate_but_invalid_claim_two(call_seq, ticket_arr_first_row, ticket_arr_second_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        return Ticket(ticket_arr, game_type, player_index, claim_player_index)

def generate_ticket_with_technically_accurate_and_valid_claim_type_2(call_seq):
        ticket_arr = []
        ticket_arr_second_row = generate_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq)
        ticket_arr_first_row = generate_row_arr_for_ticket_technically_accurate_but_invalid_claim_one(call_seq, ticket_arr_second_row)
        ticket_arr_third_row = generate_row_arr_for_ticket_technically_accurate_but_invalid_claim_two(call_seq, ticket_arr_second_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        return Ticket(ticket_arr, game_type, player_index, claim_player_index)

def generate_ticket_with_technically_accurate_and_valid_claim_type_3(call_seq):
        ticket_arr = []

        ticket_arr_third_row = generate_row_arr_for_ticket_technically_accurate_and_valid_claim(call_seq)
        ticket_arr_first_row = generate_row_arr_for_ticket_technically_accurate_but_invalid_claim_one(call_seq, ticket_arr_third_row)
        ticket_arr_second_row = generate_row_arr_for_ticket_technically_accurate_but_invalid_claim_two(call_seq, ticket_arr_third_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        return Ticket(ticket_arr, game_type, player_index, claim_player_index)

def test_init_fastest_full_house_player_player_index_not_lt_lower_limit():
    player_index = 0

    with pytest.raises(ValueError):
        player = Player(player_index, game_type, claim_validator)

def test_init_fastest_full_house_player_player_index_not_gt_upper_limit():
    player_index = 5

    with pytest.raises(ValueError):
        player = Player(player_index, game_type, claim_validator)

def test_init_fastest_full_house_player_game_type_not_lt_lower_limit():
    game_type = 0

    with pytest.raises(ValueError):
        player = Player(player_index, game_type, claim_validator)

def test_init_fastest_full_house_player_game_type_not_gt_upper_limit():
    game_type = 6

    with pytest.raises(ValueError):
        player = Player(player_index, game_type, claim_validator)

def test_fastest_full_house_player_assign_ticket_ticket_not_none():
    player = Player(player_index, game_type, claim_validator)

    call_seq_len = generate_call_seq_len()
    call_seq = generate_call_seq(call_seq_len)
    ticket = generate_ticket_with_technically_accurate_and_valid_claim_type_1(call_seq)

    player.assign_ticket(ticket)
    ticket = player.ticket

    assert ticket

def test_fastest_full_house_player_non_claim_player_claim_not_allowed_one():
    player_index = 1
    player = Player(player_index, game_type, claim_validator)

    call_seq_len = generate_call_seq_len()
    call_seq = generate_call_seq(call_seq_len)
    ticket = generate_ticket_with_technically_accurate_and_valid_claim_type_1(call_seq)

    player.assign_ticket(ticket)
    
    with pytest.raises(ValueError):
        player.raise_game_win_claim(call_seq)

def test_fastest_full_house_player_non_claim_player_claim_not_allowed_two():
    player_index = 1
    player = Player(player_index, game_type, claim_validator)

    call_seq_len = generate_call_seq_len()
    call_seq = generate_call_seq(call_seq_len)
    ticket = generate_ticket_with_technically_accurate_and_valid_claim_type_2(call_seq)

    player.assign_ticket(ticket)
    
    with pytest.raises(ValueError):
        player.raise_game_win_claim(call_seq)

def test_fastest_full_house_player_non_claim_player_claim_not_allowed_three():
    player_index = 1
    player = Player(player_index, game_type, claim_validator)

    call_seq_len = generate_call_seq_len()
    call_seq = generate_call_seq(call_seq_len)
    ticket = generate_ticket_with_technically_accurate_and_valid_claim_type_3(call_seq)

    player.assign_ticket(ticket)
    
    with pytest.raises(ValueError):
        player.raise_game_win_claim(call_seq)
