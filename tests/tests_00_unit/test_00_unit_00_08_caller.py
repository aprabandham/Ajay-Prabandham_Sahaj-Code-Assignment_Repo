from src.caller.caller import Caller
from src.common import round_game_type, CALL_SEQ_RANDOM_LEN_LIMITS, CALL_SEQ_RANGE_LIMITS, LOWER_INDEX, UPPER_INDEX
from random import randint as random_randint, sample as random_sample
import pytest

game_type = round_game_type["FASTEST_FIRST_ROW"]
call_seq_len = random_randint(CALL_SEQ_RANDOM_LEN_LIMITS[LOWER_INDEX], CALL_SEQ_RANDOM_LEN_LIMITS[UPPER_INDEX])

population = range(CALL_SEQ_RANGE_LIMITS[UPPER_INDEX] - CALL_SEQ_RANGE_LIMITS[LOWER_INDEX] + 1)
call_seq = random_sample(population, call_seq_len)


def test_caller_init_game_type_lt_lower_limit_not_allowed():
    game_type = 0

    with pytest.raises(ValueError):
        caller = Caller(game_type)

def test_caller_init_game_type_gt_upper_limit_not_allowed():
    game_type = 6

    with pytest.raises(ValueError):
        caller = Caller(game_type)

def test_caller_call_seq_setter_getter_not_none():
    caller = Caller(game_type)
    caller.call_seq = call_seq

    assert caller.call_seq == call_seq