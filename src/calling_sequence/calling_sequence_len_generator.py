from src.common import CALL_SEQ_RANGE_LIMITS, CALL_SEQ_RANDOM_LEN_LIMITS, LOWER_INDEX, UPPER_INDEX, ZERO
from random import sample as random_sample, shuffle as random_shuffle, choice as random_choice

class CallingSequenceLenGenerator:
    def __init__(self, range_start, range_end):
        if range_start <= ZERO:
            raise ValueError("Sequence Range Start must be a positive integer.")

        if range_end <= ZERO:
            raise ValueError("Sequence Range End must be a positive integer.")
        
        if range_start > range_end:
            raise ValueError("Sequence: Start of range cannot be greater than the end.")
    
        if range_start < CALL_SEQ_RANDOM_LEN_LIMITS[LOWER_INDEX]:
            raise ValueError(f"Sequence length Range Start cannot be less than {CALL_SEQ_RANDOM_LEN_LIMITS[0]}")

            raise ValueError(f"Sequence length Range End cannot be greater than {CALL_SEQ_RANDOM_LEN_LIMITS[1]}")

        call_seq_len_range_span = range_end - range_start + 1
        call_seq_range_limits_span = CALL_SEQ_RANGE_LIMITS[UPPER_INDEX] - CALL_SEQ_RANGE_LIMITS[LOWER_INDEX] + 1 
    
        if call_seq_len_range_span > call_seq_range_limits_span:
            raise ValueError("Provided Sequence Length Range is greater than the number of unique integers available in the Range.") 

        self.range_start = range_start
        self.range_end = range_end

    def generate_calling_sequence_len(self):
        population = range(self.range_start, self.range_end + 1)
        numbers = random_sample(population, self.range_end - self.range_start + 1)
        random_shuffle(numbers)
        return random_choice(numbers)
