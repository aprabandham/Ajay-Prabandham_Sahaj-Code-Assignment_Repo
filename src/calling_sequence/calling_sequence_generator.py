from src.common import ZERO
from random import sample as random_sample

class CallingSequenceGenerator:
    def __init__(self, range_start, range_end, call_seq_len):
        if range_start <= ZERO:
            raise ValueError("Sequence Range Start must be a positive integer.")

        if range_end <= ZERO:
            raise ValueError("Sequence Range End must be a positive integer.")
        
        if range_start > range_end:
            raise ValueError("Sequence: Start of range cannot be greater than the end.")
    
        if call_seq_len <= ZERO:
            raise ValueError("Sequence Length must be a positive integer.")

        population = range(range_start, range_end + 1)
    
        if call_seq_len > len(population):
            raise ValueError("Requested Sequence Length is greater than the number of unique integers available in the Range.")

        self.range_start = range_start
        self.range_end = range_end
        self._call_seq_len = call_seq_len
        self.population = population

    @property
    def call_seq_len(self):
        return self._call_seq_len

    def generate_calling_sequence(self):
        return random_sample(self.population, self._call_seq_len)
