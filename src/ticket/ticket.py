from src.ticket.ticket_interface import TicketInterface
from src.common import NUM_ROWS, ROW_LEN, round_game_type, round_player_index, game_claim_player_index, row_index, possible_claiming_player_types, possible_claiming_player_technically_inaccurate_sub_types, possible_claiming_player_technically_accurate_but_invalid_sub_types, possible_claiming_player_technically_accurate_and_valid_sub_types
import copy

class Ticket(TicketInterface):
    def __init__(self, ticket_arr, game_type, player_index, claim_player_index, claiming_player_type=None, claiming_player_sub_type=None):
        num_rows = len(ticket_arr)
        if num_rows != NUM_ROWS:
            raise ValueError(f"Each ticket must have {NUM_ROWS} rows")
        
        for row in ticket_arr:
            if len(row) != ROW_LEN:
                raise ValueError(f"Each row in the Ticket must have {ROW_LEN} numbers!")

        if game_type not in [
            round_game_type["FASTEST_FIRST_ROW"], 
            round_game_type["FASTEST_SECOND_ROW"], 
            round_game_type["FASTEST_THIRD_ROW"], 
            round_game_type["FASTEST_FULL_HOUSE"], 
            round_game_type["FASTEST_EARLY_FIVE"]]:
            
            raise ValueError("The value provided for Game Type is not permitted!")

        if player_index not in [
            round_player_index["PLAYER_ONE"], 
            round_player_index["PLAYER_TWO"],
            round_player_index["PLAYER_THREE"],
            round_player_index["PLAYER_FOUR"]]:

            raise ValueError("The value provided for Player Index is not permitted!")

        if claim_player_index not in [
            game_claim_player_index["FASTEST_FIRST_ROW"], 
            game_claim_player_index["FASTEST_SECOND_ROW"], 
            game_claim_player_index["FASTEST_THIRD_ROW"], 
            game_claim_player_index["FASTEST_FULL_HOUSE"], 
            game_claim_player_index["FASTEST_EARLY_FIVE"]]:

            raise ValueError("The value provided for Claim Player Index is not permitted!")

        if claiming_player_type:
            if claiming_player_type not in [
                possible_claiming_player_types["TECHNICALLY_INACCURATE"],
                possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"],
                possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]]:

                raise ValueError("The provided Claiming Player Type is not permitted!")

        if claiming_player_sub_type:
            if ((claiming_player_type == possible_claiming_player_types["TECHNICALLY_INACCURATE"]
                and (claiming_player_sub_type != possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_1"]
                    and claiming_player_sub_type != possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_2"]
                    and claiming_player_sub_type != possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_3"]))
            
            or (claiming_player_type == possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"]
                and (claiming_player_sub_type != possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_1"]
                    and claiming_player_sub_type != possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_2"]
                    and claiming_player_sub_type != possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_3"]))

            or (claiming_player_type == possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
                and (claiming_player_sub_type != possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]
                    and claiming_player_sub_type != possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_2"]
                    and claiming_player_sub_type != possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_3"]))):

                raise ValueError("The provided Claiming Player Sub Type is not permitted for the Claiming Player Type!")

        self.ticket_arr = [[(None, None)] * ROW_LEN] * NUM_ROWS
        for i in range(0, NUM_ROWS):
            for j in range(0, ROW_LEN):
                self.ticket_arr = copy.deepcopy(ticket_arr)

        self.game_type = game_type
        self.claim_player_index = claim_player_index
        self._player_index = player_index
        self._claiming_player_type = claiming_player_type
        self._claiming_player_sub_type = claiming_player_sub_type

    def __str__(self):
        str_repr = ""
        str_repr += "\n----------------------------------------------------------------------------------------\n"
        str_repr += f"\nTicket for GAME TYPE: {self.game_type}\n"
        str_repr += "\n----------------------------------------------------------------------------------------\n"
        str_repr += f"\nFIRST Row: (NUMBER, MARKED) = {self.get_first_row()}\n"
        str_repr += "\n----------------------------------------------------------------------------------------\n"
        str_repr += f"\nSECOND Row: (NUMBER, MARKED) = {self.get_second_row()}\n"
        str_repr += "\n----------------------------------------------------------------------------------------\n"
        str_repr += f"\nTHIRD Row: (NUMBER, MARKED) = {self.get_third_row()}\n"
        str_repr += "\n----------------------------------------------------------------------------------------\n"

        return str_repr

    @property
    def player_index(self):
        return self._player_index

    @property
    def claiming_player_type(self):
        return self._claiming_player_type

    @property
    def claiming_player_sub_type(self):
        return self._claiming_player_sub_type

    def get_first_row(self):
        return self.ticket_arr[row_index["FIRST_ROW"]]

    def get_second_row(self):
        return self.ticket_arr[row_index["SECOND_ROW"]]

    def get_third_row(self):
        return self.ticket_arr[row_index["THIRD_ROW"]]

    def get_all_rows(self):
        return self.ticket_arr
