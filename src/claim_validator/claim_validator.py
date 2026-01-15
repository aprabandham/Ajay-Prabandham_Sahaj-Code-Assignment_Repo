from src.claim_validator.claim_validator_interface import ClaimValidatorInterface
from src.common import LOWER_INDEX, UPPER_INDEX, CALL_SEQ_RANDOM_LEN_LIMITS, ROW_LEN, NUM_ROWS, round_game_type, possible_claiming_player_types, possible_claiming_player_technically_inaccurate_sub_types, possible_claiming_player_technically_accurate_but_invalid_sub_types, possible_claiming_player_technically_accurate_and_valid_sub_types

class ClaimValidator(ClaimValidatorInterface):
    def __init__(self, game_type):
        if game_type not in [
            round_game_type["FASTEST_FIRST_ROW"],
            round_game_type["FASTEST_SECOND_ROW"],
            round_game_type["FASTEST_THIRD_ROW"],
            round_game_type["FASTEST_FULL_HOUSE"],
            round_game_type["FASTEST_EARLY_FIVE"]]:
            
            raise ValueError("The value provided for Game Type is not permitted!")

        self.game_type = game_type

    def validate_player_claim(self, call_seq, ticket, claiming_player_type=None, claiming_player_sub_type=None):
        if len(call_seq) < CALL_SEQ_RANDOM_LEN_LIMITS[LOWER_INDEX] or len(call_seq) > CALL_SEQ_RANDOM_LEN_LIMITS[UPPER_INDEX]:
            raise ValueError("The provided Calling Sequence lenght is not within prescribed limits")

        if not ticket:
            raise ValueError("The provided Ticket object is None!")

        call_seq_len = len(call_seq)
        validation_result = False
        match_count = 0

        start_row_elems = []
        other_rows_elems = []
        all_rows_elems_prefix = []

        if self.game_type in [
            round_game_type["FASTEST_FIRST_ROW"], 
            round_game_type["FASTEST_SECOND_ROW"],
            round_game_type["FASTEST_THIRD_ROW"]]:
            if self.game_type == round_game_type["FASTEST_FIRST_ROW"]:
                start_row_elems.extend(ticket.get_first_row())
            elif self.game_type == round_game_type["FASTEST_SECOND_ROW"]:
                start_row_elems.extend(ticket.get_second_row())
            else: 
                start_row_elems.extend(ticket.get_third_row())
        
            # if start_row_elems[-1][LOWER_INDEX] == call_seq[-1]:
            #     match_count += 1

            start_row_prefix = []
            for elem in start_row_elems:
                if elem[LOWER_INDEX] == call_seq[-1]:
                    start_row_prefix = list(set(start_row_elems) - set([elem]))
                    match_count += 1
                    break

            start_row_nums_prefix = [elem[LOWER_INDEX] for elem in start_row_prefix]
            call_seq_prefix = call_seq[0:call_seq_len-1]
                
            for num in start_row_nums_prefix:
                if num in call_seq_prefix:
                    match_count += 1
            
            if match_count == ROW_LEN:
                validation_result = True
        else:
            if self.game_type in [
                round_game_type["FASTEST_FULL_HOUSE"],
                round_game_type["FASTEST_EARLY_FIVE"]]:                
                if not claiming_player_type:                    
                    raise ValueError("The provided Claiming Player Type cannot be None")
            
                if claiming_player_type not in [
                    possible_claiming_player_types["TECHNICALLY_INACCURATE"],
                    possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"],
                    possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]]:

                    raise ValueError("The provided Claiming Player Type is not permitted!")
            
                if not claiming_player_sub_type:
                    raise ValueError("The provided Claiming Player Type cannot be None!")
            
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
            
                if (claiming_player_sub_type == possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_1"]
                    or claiming_player_sub_type == possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_1"]
                    or claiming_player_sub_type == possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]):
                    
                    start_row_elems.extend(ticket.get_first_row())
                    other_rows_elems.extend(ticket.get_second_row())
                    other_rows_elems.extend(ticket.get_third_row())
            
                elif (claiming_player_sub_type == possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_2"]
                    or claiming_player_sub_type == possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_2"]
                    or claiming_player_sub_type == possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_2"]):
                
                    start_row_elems.extend(ticket.get_second_row())
                    other_rows_elems.extend(ticket.get_first_row())
                    other_rows_elems.extend(ticket.get_third_row())
                
                else:
                    start_row_elems.extend(ticket.get_third_row())
                    other_rows_elems.extend(ticket.get_first_row())
                    other_rows_elems.extend(ticket.get_second_row())

                start_row_prefix = []    
                for elem in start_row_elems:
                    if elem[LOWER_INDEX] == call_seq[-1]:
                        start_row_prefix = list(set(start_row_elems) - set([elem]))
                        match_count += 1
                        break

                all_rows_elems_prefix.extend(start_row_prefix)
                all_rows_elems_prefix.extend(other_rows_elems)

                all_rows_nums_prefix = [elem[LOWER_INDEX] for elem in all_rows_elems_prefix]
                call_seq_prefix = call_seq[0:call_seq_len-1]
                    
                for num in all_rows_nums_prefix:
                    if num in call_seq_prefix:
                        match_count += 1
                
                if self.game_type == round_game_type["FASTEST_FULL_HOUSE"]:
                    
                    print("######################################################################################################################################################")
                    print("")
                    print(f"############################################## Inside ClaimValidator::validate_player_claim()########################################################")
                    print("")
                    print(f"FASTEST_FULL_HOUSE: claiming_player_type = {claiming_player_type}, claiming_player_sub_type = {claiming_player_sub_type}, match_count = {match_count}")
                    print("")
                    print("######################################################################################################################################################")
                    print("")

                    if match_count == (ROW_LEN * NUM_ROWS):
                        validation_result = True
                else:
                    if match_count == ROW_LEN:
                        validation_result = True

        return validation_result
