from src.ticket_generator.fastest_full_house_ticket_generator import FastestFullHouseTicketGenerator
from src.common import LOWER_INDEX, UPPER_INDEX, CALL_SEQ_RANDOM_LEN_LIMITS, CALL_SEQ_RANGE_LIMITS, NUM_PLAYERS, round_game_type, game_claim_player_index, ZERO, ROW_LEN, NUM_ROWS, possible_claiming_player_types, possible_claiming_player_technically_inaccurate_sub_types, possible_claiming_player_technically_accurate_but_invalid_sub_types, possible_claiming_player_technically_accurate_and_valid_sub_types
from random import randint as random_randint, sample as random_sample
import pytest

call_seq_len = random_randint(CALL_SEQ_RANDOM_LEN_LIMITS[LOWER_INDEX], CALL_SEQ_RANDOM_LEN_LIMITS[UPPER_INDEX])
population = range(CALL_SEQ_RANGE_LIMITS[UPPER_INDEX] - CALL_SEQ_RANGE_LIMITS[LOWER_INDEX] + 1)
call_seq = random_sample(population, call_seq_len)
num_players = NUM_PLAYERS

game_type = round_game_type["FASTEST_FULL_HOUSE"]
claim_player_index = game_claim_player_index["FASTEST_FULL_HOUSE"]
claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]

def test_init_fastest_full_house_ticket_generator_call_seq_len_lt_lower_limit():
    call_seq = [3, 87, 22, 42]
    
    with pytest.raises(ValueError):
        ticket_gen = FastestFullHouseTicketGenerator(call_seq, num_players, game_type, claim_player_index,claiming_player_type, claiming_player_sub_type)

def test_init_fastest_full_house_ticket_generator_call_seq_len_gt_upper_limit():
    call_seq = [i for i in range(1, 100)]
    
    with pytest.raises(ValueError):
        ticket_gen = FastestFullHouseTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)

def test_init_fastest_full_house_ticket_generator_num_players_lt_lower_limit_not_allowed():
    num_players = ZERO

    with pytest.raises(ValueError):
        ticket_gen = FastestFullHouseTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)

def test_init_fastest_full_house_ticket_generator_num_players_gt_upper_limit_not_allowed():
    num_players = 5

    with pytest.raises(ValueError):
        ticket_gen = FastestFullHouseTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)

def test_init_fastest_full_house_ticket_generator_game_type_lt_lower_limit_not_allowed():
    game_type = 0

    with pytest.raises(ValueError):
        ticket_gen = FastestFullHouseTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)

def test_init_fastest_full_house_ticket_generator_game_type_gt_upper_limit_not_allowed():
    game_type = 6

    with pytest.raises(ValueError):
        ticket_gen = FastestFullHouseTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)

def test_init_fastest_full_house_ticket_generator_claim_player_index_lt_lower_bound():
    claim_player_index = ZERO

    with pytest.raises(ValueError):
        ticket_gen = FastestFullHouseTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)

def test_init_fastest_full_house_ticket_generator_claim_player_index_gt_upper_bound():
    claim_player_index = num_players+1

    with pytest.raises(ValueError):
        ticket_gen = FastestFullHouseTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)

def test_fastest_full_house_ticket_generator_generate_ticket_list_ticket_list_not_empty():
    ticket_gen = FastestFullHouseTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    ticket_list = ticket_gen.generate_ticket_list()
    
    assert len(ticket_list) != 0

def test_fastest_full_house_ticket_generator_generate_ticket_list_num_tickets_exactly_matches_num_players():
    ticket_gen = FastestFullHouseTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    ticket_list = ticket_gen.generate_ticket_list()
    
    assert len(ticket_list) == num_players

def test_fastest_full_house_ticket_generator_generate_ticket_list_claiming_ticket_not_accurate_not_empty():
    game_type = round_game_type["FASTEST_FULL_HOUSE"]
    claim_player_index = game_claim_player_index["FASTEST_FULL_HOUSE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_INACCURATE"]
    claiming_player_sub_type = possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_1"]
    
    ticket_gen = FastestFullHouseTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    ticket_list = ticket_gen.generate_ticket_list()

    claiming_player_ticket_not_empty = False
    for ticket in ticket_list:
        if claim_player_index == ticket.player_index:
            claiming_player_ticket_not_empty = True

    assert claiming_player_ticket_not_empty

def test_fastest_full_house_ticket_generator_generate_ticket_list_claiming_ticket_not_accurate_not_empty():
    game_type = round_game_type["FASTEST_FULL_HOUSE"]
    claim_player_index = game_claim_player_index["FASTEST_FULL_HOUSE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_INACCURATE"]
    claiming_player_sub_type = possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_2"]
    
    ticket_gen = FastestFullHouseTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    ticket_list = ticket_gen.generate_ticket_list()

    claiming_player_ticket_not_empty = False
    for ticket in ticket_list:
        if claim_player_index == ticket.player_index:
            claiming_player_ticket_not_empty = True

    assert claiming_player_ticket_not_empty

def test_fastest_full_house_ticket_generator_generate_ticket_list_claiming_ticket_not_accurate_not_empty():
    game_type = round_game_type["FASTEST_FULL_HOUSE"]
    claim_player_index = game_claim_player_index["FASTEST_FULL_HOUSE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_INACCURATE"]
    claiming_player_sub_type = possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_3"]
    
    ticket_gen = FastestFullHouseTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    ticket_list = ticket_gen.generate_ticket_list()

    claiming_player_ticket_not_empty = False
    for ticket in ticket_list:
        if claim_player_index == ticket.player_index:
            claiming_player_ticket_not_empty = True

    assert claiming_player_ticket_not_empty

def test_fastest_full_house_ticket_generator_generate_ticket_list_claiming_ticket_accurate_but_invalid_claim_not_empty():
    game_type = round_game_type["FASTEST_FULL_HOUSE"]
    claim_player_index = game_claim_player_index["FASTEST_FULL_HOUSE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_1"]
    
    ticket_gen = FastestFullHouseTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    ticket_list = ticket_gen.generate_ticket_list()

    claiming_player_ticket_not_empty = False
    for ticket in ticket_list:
        if claim_player_index == ticket.player_index:
            claiming_player_ticket_not_empty = True

    assert claiming_player_ticket_not_empty

def test_fastest_full_house_ticket_generator_generate_ticket_list_claiming_ticket_accurate_but_invalid_claim_not_empty():
    game_type = round_game_type["FASTEST_FULL_HOUSE"]
    claim_player_index = game_claim_player_index["FASTEST_FULL_HOUSE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_2"]
    
    ticket_gen = FastestFullHouseTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    ticket_list = ticket_gen.generate_ticket_list()

    claiming_player_ticket_not_empty = False
    for ticket in ticket_list:
        if claim_player_index == ticket.player_index:
            claiming_player_ticket_not_empty = True

    assert claiming_player_ticket_not_empty

def test_fastest_full_house_ticket_generator_generate_ticket_list_claiming_ticket_accurate_but_invalid_claim_not_empty():
    game_type = round_game_type["FASTEST_FULL_HOUSE"]
    claim_player_index = game_claim_player_index["FASTEST_FULL_HOUSE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_3"]
    
    ticket_gen = FastestFullHouseTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    ticket_list = ticket_gen.generate_ticket_list()

    claiming_player_ticket_not_empty = False
    for ticket in ticket_list:
        if claim_player_index == ticket.player_index:
            claiming_player_ticket_not_empty = True

    assert claiming_player_ticket_not_empty

def test_fastest_full_house_ticket_generator_generate_ticket_list_claiming_ticket_accurate_and_valid_claim_not_empty():
    game_type = round_game_type["FASTEST_FULL_HOUSE"]
    claim_player_index = game_claim_player_index["FASTEST_FULL_HOUSE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]
    
    ticket_gen = FastestFullHouseTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    ticket_list = ticket_gen.generate_ticket_list()

    claiming_player_ticket_not_empty = False
    for ticket in ticket_list:
        if ticket and claim_player_index == ticket.player_index:
            claiming_player_ticket_not_empty = True

    assert claiming_player_ticket_not_empty

def test_fastest_full_house_ticket_generator_generate_ticket_list_claiming_ticket_accurate_and_valid_claim_not_empty():
    game_type = round_game_type["FASTEST_FULL_HOUSE"]
    claim_player_index = game_claim_player_index["FASTEST_FULL_HOUSE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_2"]
    
    ticket_gen = FastestFullHouseTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    ticket_list = ticket_gen.generate_ticket_list()

    claiming_player_ticket_not_empty = False
    for ticket in ticket_list:
        if ticket and claim_player_index == ticket.player_index:
            claiming_player_ticket_not_empty = True

    assert claiming_player_ticket_not_empty

def test_fastest_full_house_ticket_generator_generate_ticket_list_claiming_ticket_accurate_and_valid_claim_not_empty():
    game_type = round_game_type["FASTEST_FULL_HOUSE"]
    claim_player_index = game_claim_player_index["FASTEST_FULL_HOUSE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_3"]
    
    ticket_gen = FastestFullHouseTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    ticket_list = ticket_gen.generate_ticket_list()

    claiming_player_ticket_not_empty = False
    for ticket in ticket_list:
        if ticket and claim_player_index == ticket.player_index:
            claiming_player_ticket_not_empty = True

    assert claiming_player_ticket_not_empty

def test_fastest_full_house_ticket_generator_generate_ticket_list_claiming_ticket_inaccurate_and_non_claiming_tickets_not_empty():
    game_type = round_game_type["FASTEST_FULL_HOUSE"]
    claim_player_index = game_claim_player_index["FASTEST_FULL_HOUSE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_INACCURATE"]
    claiming_player_sub_type = possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_1"]
    
    ticket_gen = FastestFullHouseTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    ticket_list = ticket_gen.generate_ticket_list()

    non_claiming_player_ticket_not_empty = {True: 0}
    for ticket in ticket_list:
        if ticket and claim_player_index != ticket.player_index:
            non_claiming_player_ticket_not_empty[True] += 1

    assert non_claiming_player_ticket_not_empty[True] == 3

def test_fastest_full_house_ticket_generator_generate_ticket_list_claiming_ticket_accurate_but_invalid_and_non_claiming_tickets_not_empty():
    game_type = round_game_type["FASTEST_FULL_HOUSE"]
    claim_player_index = game_claim_player_index["FASTEST_FULL_HOUSE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_2"]
    
    ticket_gen = FastestFullHouseTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    ticket_list = ticket_gen.generate_ticket_list()

    non_claiming_player_ticket_not_empty = {True: 0}
    for ticket in ticket_list:
        if ticket and claim_player_index != ticket.player_index:
            non_claiming_player_ticket_not_empty[True] += 1

    assert non_claiming_player_ticket_not_empty[True] == 3

def test_fastest_full_house_ticket_generator_generate_ticket_list_claiming_ticket_accurate_and_valid_and_non_claiming_tickets_not_empty():
    game_type = round_game_type["FASTEST_FULL_HOUSE"]
    claim_player_index = game_claim_player_index["FASTEST_FULL_HOUSE"]
    claiming_player_type = possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
    claiming_player_sub_type = possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_3"]
    
    ticket_gen = FastestFullHouseTicketGenerator(call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type)
    ticket_list = ticket_gen.generate_ticket_list()

    non_claiming_player_ticket_not_empty = {True: 0}
    for ticket in ticket_list:
        if ticket and claim_player_index != ticket.player_index:
            non_claiming_player_ticket_not_empty[True] += 1

    assert non_claiming_player_ticket_not_empty[True] == 3
