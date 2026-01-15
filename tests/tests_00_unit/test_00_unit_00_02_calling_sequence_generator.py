from src.calling_sequence.calling_sequence_generator import CallingSequenceGenerator
from src.common import CALL_SEQ_RANGE_LIMITS, CALL_SEQ_RANDOMNESS_CHECK_ITERS, LOWER_INDEX, UPPER_INDEX
import pytest

# Choose this RANDOMLY too!
call_seq_len = 21

def test_init_calling_sequence_generator_non_positive_range_start():
    with pytest.raises(ValueError):
        call_seq_gen = CallingSequenceGenerator(-4, 50, 15)

def test_init_calling_sequence_generator_non_positive_range_end():
    with pytest.raises(ValueError):
        call_seq_gen = CallingSequenceGenerator(2, -2, 12)

def test_init_calling_sequence_generator_non_positive_call_seq_len():
    with pytest.raises(ValueError):
        call_seq_gen = CallingSequenceGenerator(15, 75, -5)

def test_init_calling_sequence_generator_range_start_gt_range_end():
    with pytest.raises(ValueError):
        call_seq_gen = CallingSequenceGenerator(55, 45, 15)

def test_init_calling_sequence_generator_call_seq_len_gt_num_unique_integers_in_range():
    with pytest.raises(ValueError):
        call_seq_gen = CallingSequenceGenerator(3, 33, 44)

def test_calling_sequence_generator_get_sequence_is_not_empty():
    call_seq_gen = CallingSequenceGenerator(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX], call_seq_len)
    call_seq = call_seq_gen.generate_calling_sequence()

    assert call_seq

def test_calling_sequence_generator_get_sequence_has_required_len():
    call_seq_gen = CallingSequenceGenerator(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX], call_seq_len)
    call_seq = call_seq_gen.generate_calling_sequence()

    assert len(call_seq) == call_seq_len

def test_calling_sequence_get_sequence_has_elements_within_range():
    call_seq_gen = CallingSequenceGenerator(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX], call_seq_len)
    call_seq = call_seq_gen.generate_calling_sequence()

    all_elems_in_range = True
    for num in call_seq:
        if num < CALL_SEQ_RANGE_LIMITS[LOWER_INDEX] or num > CALL_SEQ_RANGE_LIMITS[UPPER_INDEX]:
            all_elems_in_range = False
            break

    assert all_elems_in_range

def test_calling_sequence_generator_get_sequence_has_unique_elements():
    call_seq_gen = CallingSequenceGenerator(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX], call_seq_len)
    call_seq = call_seq_gen.generate_calling_sequence()

    call_seq_set = set(call_seq)
    call_seq_set_as_list = list(call_seq_set)
    
    assert len(call_seq) == len(call_seq_set_as_list)
