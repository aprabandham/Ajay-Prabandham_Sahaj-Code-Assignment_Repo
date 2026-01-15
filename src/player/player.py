from src.player.player_interface import PlayerInterface
from src.common import round_game_type, round_player_index, game_claim_player_index, possible_claiming_player_types, possible_claiming_player_technically_inaccurate_sub_types, possible_claiming_player_technically_accurate_but_invalid_sub_types, possible_claiming_player_technically_accurate_and_valid_sub_types

class Player(PlayerInterface):
    def __init__(self, player_index, game_type, claim_validator):
        if player_index not in [
            round_player_index["PLAYER_ONE"],
            round_player_index["PLAYER_TWO"],
            round_player_index["PLAYER_THREE"],
            round_player_index["PLAYER_FOUR"]]:
            
            raise ValueError("The Player Index provided is not listed!")

        if game_type not in [
            round_game_type["FASTEST_FIRST_ROW"],
            round_game_type["FASTEST_SECOND_ROW"],
            round_game_type["FASTEST_THIRD_ROW"],
            round_game_type["FASTEST_FULL_HOUSE"],
            round_game_type["FASTEST_EARLY_FIVE"]]:
            
            raise ValueError("The Game Type provided is not permitted!")

        if not claim_validator:
            raise ValueError("The Game Win Claim Validator Ref provided cannot be None!")
        
        self._ticket = None
        self._player_index = player_index
        self._game_type = game_type
        self.claim_validator = claim_validator
        self._claiming_player_type = None
        self._claiming_player_sub_type = None

    def __str__(self):
        str_repr = ""
        str_repr += "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        str_repr += f"\nGame Type = {self.game_type}\n"
        str_repr += "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        str_repr += f"\nPlayer Index = {self.player_index}\n"
        str_repr += "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"

        return str_repr

    @property
    def game_type(self):
        return self._game_type
    
    @property
    def player_index(self):
        return self._player_index

    @property
    def ticket(self):
        return self._ticket

    @property
    def claiming_player_type(self):
        return self._claiming_player_type

    @property
    def claiming_player_sub_type(self):
        return self._claiming_player_sub_type

    def assign_ticket(self, ticket):
        if not ticket:
            raise ValueError("The Ticket Ref provided cannot be None!")

        self._ticket = ticket

        if ticket.claiming_player_type:
            if ticket.claiming_player_type not in [
                possible_claiming_player_types["TECHNICALLY_INACCURATE"],
                possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"],
                possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]]:

                raise ValueError("The provided Claiming Player Type is not permitted!")

        self._claiming_player_type = ticket.claiming_player_type

        if ticket.claiming_player_sub_type:
            if ((ticket.claiming_player_type == possible_claiming_player_types["TECHNICALLY_INACCURATE"]
                and (ticket.claiming_player_sub_type != possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_1"]
                    and ticket.claiming_player_sub_type != possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_2"]
                    and ticket.claiming_player_sub_type != possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_3"]))
            
            or (ticket.claiming_player_type == possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"]
                and (ticket.claiming_player_sub_type != possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_1"]
                    and ticket.claiming_player_sub_type != possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_2"]
                    and ticket.claiming_player_sub_type != possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_3"]))

            or (ticket.claiming_player_type == possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
                and (ticket.claiming_player_sub_type != possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]
                    and ticket.claiming_player_sub_type != possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_2"]
                    and ticket.claiming_player_sub_type != possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_3"]))):

                raise ValueError("The provided Claiming Player Sub Type is not permitted for the Claiming Player Type!")
        
        self._claiming_player_sub_type = ticket.claiming_player_sub_type

    def raise_game_win_claim(self, call_seq):
        if ((self.game_type == round_game_type["FASTEST_FIRST_ROW"] and self.player_index != game_claim_player_index["FASTEST_FIRST_ROW"])
            or (self.game_type == round_game_type["FASTEST_SECOND_ROW"] and self.player_index != game_claim_player_index["FASTEST_SECOND_ROW"])
            or (self.game_type == round_game_type["FASTEST_THIRD_ROW"] and self.player_index != game_claim_player_index["FASTEST_THIRD_ROW"]) 
            or (self.game_type == round_game_type["FASTEST_FULL_HOUSE"] and self.player_index != game_claim_player_index["FASTEST_FULL_HOUSE"])
            or (self.game_type == round_game_type["FASTEST_EARLY_FIVE"] and self.player_index != game_claim_player_index["FASTEST_EARLY_FIVE"])):
            
            raise ValueError("This Player is not permitted to raise a Game Win Claim, for this Simulation!")

        validation_result = False
        validation_result = self.claim_validator.validate_player_claim(call_seq, self.ticket, self.claiming_player_type, self.claiming_player_sub_type)
        return validation_result
