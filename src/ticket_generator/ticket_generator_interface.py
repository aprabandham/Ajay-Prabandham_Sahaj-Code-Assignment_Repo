from abc import ABC, abstractmethod
from src.common import possible_claiming_player_types, possible_non_claiming_player_types

class TicketGeneratorInterface(ABC):
    def __init__(self, call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type=None):
        self.call_seq = call_seq
        self.num_players = num_players
        self.game_type = game_type
        self.claim_player_index = claim_player_index
        self.claiming_player_type = claiming_player_type
        self.claiming_player_sub_type = claiming_player_sub_type

        self.game_iteration_type_of_claiming_player_done = {
            "TECHNICALLY_INACCURATE": False,
            "TECHNICALLY_ACCURATE_BUT_INVALID": False,
            "TECHNICALLY_ACCURATE_AND_VALID": False
        }

        self.claim_player_index = claim_player_index
        self.non_claiming_player_indexes = []

        self.claiming_player_type_ticket_gen_refs_map = {
            self.game_type: {} 
        }

        self.non_claiming_player_type_ticket_gen_refs_map = {
            self.game_type: {} 
        }

    @abstractmethod
    def generate_ticket_list(self):
        pass
