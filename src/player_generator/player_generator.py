from src.player_generator.player_generator_interface import PlayerGeneratorInterface
from src.player.player import Player
from src.common import CALL_SEQ_RANGE_LIMITS, CALL_SEQ_RANDOM_LEN_LIMITS, NUM_PLAYERS, MIN_NUM_GAME_PLAYERS, round_game_type, game_claim_player_index, round_player_index, LOWER_INDEX, UPPER_INDEX, ROW_LEN, NUM_ROWS, game_win_claim_types, NUM_TECHNICALLY_INACCURATE_NUMS_IN_ROW, LIST_PENULTIMATE_INDEX, LIST_LAST_INDEX, round_player_index, possible_claiming_player_types, possible_claiming_player_technically_inaccurate_sub_types, possible_claiming_player_technically_accurate_but_invalid_sub_types, possible_claiming_player_technically_accurate_and_valid_sub_types

from random import sample as random_sample, choice as random_choice, shuffle as random_shuffle
import copy

class PlayerGenerator(PlayerGeneratorInterface):
    def __init__(self, num_players, game_type, claim_player_index, claim_validator):
        if num_players < MIN_NUM_GAME_PLAYERS or num_players > NUM_PLAYERS:
            raise ValueError(f"The number of game players needs to be at least {MIN_NUM_GAME_PLAYERS}!")

        self.num_players= num_players

        if game_type not in [
            round_game_type["FASTEST_FIRST_ROW"],
            round_game_type["FASTEST_SECOND_ROW"],
            round_game_type["FASTEST_THIRD_ROW"],
            round_game_type["FASTEST_FULL_HOUSE"],
            round_game_type["FASTEST_EARLY_FIVE"]]:
            raise ValueError("The value provided for Game Type is not permitted!")

        self.game_type = game_type

        if ((self.game_type == round_game_type["FASTEST_FIRST_ROW"] and claim_player_index != game_claim_player_index["FASTEST_FIRST_ROW"])
            or (self.game_type == round_game_type["FASTEST_SECOND_ROW"] and claim_player_index != game_claim_player_index["FASTEST_SECOND_ROW"])
            or (self.game_type == round_game_type["FASTEST_THIRD_ROW"] and claim_player_index != game_claim_player_index["FASTEST_THIRD_ROW"])
            or (self.game_type == round_game_type["FASTEST_FULL_HOUSE"] and claim_player_index != game_claim_player_index["FASTEST_FULL_HOUSE"])
            or (self.game_type == round_game_type["FASTEST_EARLY_FIVE"] and claim_player_index != game_claim_player_index["FASTEST_EARLY_FIVE"])):
            raise ValueError("The value provided for Claim Player Index is not permitted!")

        self.claim_player_index = claim_player_index

        if not claim_validator:
            raise ValueError("The Claim Validator ref provided cannot be None!")
        
        self.claim_validator = claim_validator

    @property
    def player_index(self):
        return self._player_index

    def generate_player_list(self):
        player_index_list = round_player_index.values()
        player_list = []
        for index in player_index_list:
            player = Player(index, self.game_type, self.claim_validator)
            player_list.append(player)

        return player_list
