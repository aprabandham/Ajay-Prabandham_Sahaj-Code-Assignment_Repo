from src.common import round_game_type

class Caller:
    def __init__(self, game_type):
        if game_type not in [
            round_game_type["FASTEST_FIRST_ROW"],
            round_game_type["FASTEST_SECOND_ROW"],
            round_game_type["FASTEST_THIRD_ROW"],
            round_game_type["FASTEST_FULL_HOUSE"],
            round_game_type["FASTEST_EARLY_FIVE"]]:

            raise ValueError("The Game Type provided is not permitted!")

        self.game_type = game_type
        self._call_seq = None

    @property
    def call_seq(self):
        return self._call_seq

    @call_seq.setter
    def call_seq(self, call_seq):
        self._call_seq = call_seq
