from src.calling_sequence.calling_sequence_len_generator import CallingSequenceLenGenerator
from src.common import CALL_SEQ_RANDOM_LEN_LIMITS, CALL_SEQ_LEN_RANDOMNESS_CHECK_ITERS, LOWER_INDEX, UPPER_INDEX
import pytest

def test_init_call_seq_len_generator_non_positive_range_start():
    with pytest.raises(ValueError):
        call_seq_len_gen = CallingSequenceLenGenerator(-4, 50)

def test_init_call_seq_len_generator_non_positive_range_end():
    with pytest.raises(ValueError):
        call_seq_len_gen = CallingSequenceLenGenerator(2, -2)

def test_init_call_seq_len_generator_range_start_gt_range_end():
    with pytest.raises(ValueError):
        call_seq_len_gen = CallingSequenceLenGenerator(55, 45)

def test_init_call_seq_len_generator_range_out_of_limits():
    with pytest.raises(ValueError):
        call_seq_len_gen = CallingSequenceLenGenerator(2, 100)

def test_init_call_seq_len_generator_value_within_limits():
    call_seq_len_gen = CallingSequenceLenGenerator(CALL_SEQ_RANDOM_LEN_LIMITS[LOWER_INDEX], CALL_SEQ_RANDOM_LEN_LIMITS[UPPER_INDEX])
    call_seq_len = call_seq_len_gen.generate_calling_sequence_len()

    assert call_seq_len >= CALL_SEQ_RANDOM_LEN_LIMITS[LOWER_INDEX] and call_seq_len <= CALL_SEQ_RANDOM_LEN_LIMITS[UPPER_INDEX]
