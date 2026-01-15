from abc import ABC, abstractmethod

class TambolaGameSimulatorInterface(ABC):
    def __init__(self, game_type, call_seq_len_gen, call_seq_gen, player_gen, ticket_gen, claim_validator, caller, player_index_list, game_simulator_file_logger):
        self._game_type = game_type
        self._call_seq_len_gen = call_seq_len_gen
        self._call_seq_gen = call_seq_gen
        self._player_gen = player_gen
        self._ticket_gen = ticket_gen
        self._claim_validator = claim_validator
        self._caller = caller
        self._player_index_list = player_index_list
        self._game_simulator_file_logger = game_simulator_file_logger

    @property
    def game_type(self):
        return self._game_type

    @property
    def call_seq_len_gen(self):
        return self._call_seq_len_gen

    @property
    def call_seq_gen(self):
        return self._call_seq_gen

    @property
    def player_gen(self):
        return self._player_gen

    @property
    def ticket_gen(self):
        return self._ticket_gen

    @property
    def claim_validator(self):
        return self._claim_validator

    @property
    def caller(self):
        return self._caller

    @property
    def player_index_list(self):
        return self._player_index_list

    @property
    def game_simulator_file_logger(self):
        return self._game_simulator_file_logger

    def log_message_to_file(self, obj):
        with self.game_simulator_file_logger as logger:
            logger.log(obj)
    
    @abstractmethod
    def validate_fastest_row_technically_inaccurate_claim(self):
        pass

    @abstractmethod
    def validate_fastest_row_technically_accurate_but_invalid_claim(self):
        pass

    @abstractmethod
    def validate_fastest_row_technically_accurate_and_valid_claim(self):
        pass
