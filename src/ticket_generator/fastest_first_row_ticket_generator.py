from src.ticket_generator.ticket_generator_interface import TicketGeneratorInterface
from src.ticket.ticket import Ticket
from src.common import CALL_SEQ_RANGE_LIMITS, CALL_SEQ_RANDOM_LEN_LIMITS, NUM_PLAYERS, MIN_NUM_GAME_PLAYERS, round_game_type, game_claim_player_index, round_player_index, LOWER_INDEX, UPPER_INDEX, ROW_LEN, NUM_ROWS, game_win_claim_types, NUM_TECHNICALLY_INACCURATE_NUMS_IN_ROW, LIST_PENULTIMATE_INDEX, LIST_LAST_INDEX, possible_claiming_player_types, possible_non_claiming_player_types
from random import sample as random_sample, choice as random_choice, shuffle as random_shuffle

class FastestFirstRowTicketGenerator(TicketGeneratorInterface):
    def __init__(self, call_seq, num_players, game_type, claim_player_index, claiming_player_type):
        if len(call_seq) < CALL_SEQ_RANDOM_LEN_LIMITS[LOWER_INDEX]:
            raise ValueError(f"Calling Sequence Length less than permitted lower limit - {CALL_SEQ_RANDOM_LEN_LIMITS[0]}!")
        
        if len(call_seq) > CALL_SEQ_RANDOM_LEN_LIMITS[UPPER_INDEX]:
            raise ValueError(f"Calling Sequence Length greater than permitted upper limit - {CALL_SEQ_RANDOM_LEN_LIMITS[1]}!")

        if num_players < MIN_NUM_GAME_PLAYERS or num_players > NUM_PLAYERS:
            raise ValueError(f"The number of game players needs to be at least {MIN_NUM_GAME_PLAYERS}!")

        if game_type != round_game_type["FASTEST_FIRST_ROW"]:
            raise ValueError("The value provided for Game Type is not permitted!")

        if claim_player_index != game_claim_player_index["FASTEST_FIRST_ROW"]:
            raise ValueError("The value provided for Claim Player Index is not permitted!")

        if claiming_player_type not in [
            possible_claiming_player_types["TECHNICALLY_INACCURATE"],
            possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"],
            possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]]:

            raise ValueError("The Claiming Player Type value provided is not permitted!")

        super().__init__(call_seq, num_players, game_type, claim_player_index, claiming_player_type)

        self.claiming_player_type_ticket_gen_refs_map[self.game_type][possible_claiming_player_types["TECHNICALLY_INACCURATE"]] = self._generate_ticket_with_technically_inaccurate_claim
        self.claiming_player_type_ticket_gen_refs_map[self.game_type][possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"]] = self._generate_ticket_with_technically_accurate_but_invalid_claim
        self.claiming_player_type_ticket_gen_refs_map[self.game_type][possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]] = self._generate_ticket_with_technically_accurate_and_valid_claim

        self.non_claiming_player_type_ticket_gen_refs_map[self.game_type][possible_non_claiming_player_types["TECHNICALLY_INACCURATE"]] = self._generate_ticket_with_technically_inaccurate_claim
        self.non_claiming_player_type_ticket_gen_refs_map[self.game_type][possible_non_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"]] = self._generate_ticket_with_technically_accurate_but_invalid_claim
        self.non_claiming_player_type_ticket_gen_refs_map[self.game_type][possible_non_claiming_player_types["TECHNICALLY_ACCURATE_AND_POTENTIALLY_VALID_BUT_UNRAISED"]] = self._generate_ticket_with_technically_accurate_and_valid_claim

    def generate_ticket_list(self):
        all_players_tickets_list = []
        claiming_player_type_ticket = None
        non_claiming_player_type_tickets_list = []

        for player_index in round_player_index.values():
            if player_index == self.claim_player_index:
                claiming_player_type_ticket = self._generate_ticket_for_claiming_player(player_index)
                all_players_tickets_list.append(claiming_player_type_ticket)
            else:
                self.non_claiming_player_indexes.append(player_index)    
        
        non_claiming_player_type_tickets_list = self._generate_tickets_for_non_claiming_players()
        all_players_tickets_list.extend(non_claiming_player_type_tickets_list)

        return all_players_tickets_list

    def _generate_ticket_for_claiming_player(self, player_index):
        ticket = self.claiming_player_type_ticket_gen_refs_map[self.game_type][self.claiming_player_type](player_index)

        return ticket

    def _generate_tickets_for_non_claiming_players(self):
        tickets_list = []
        ticket = None
         
        for i, non_claiming_player_type_index in enumerate(possible_non_claiming_player_types.values()):
            ticket = self.non_claiming_player_type_ticket_gen_refs_map[self.game_type][non_claiming_player_type_index](self.non_claiming_player_indexes[i])
            tickets_list.append(ticket)

        return tickets_list

    def _generate_ticket_with_technically_inaccurate_claim(self, player_index):
        ticket_arr = []
        ticket_arr_first_row = self._generate_fastest_first_row_arr_for_ticket_technically_inaccurate_claim()
        ticket_arr_second_row = self._generate_fastest_first_row_claim_second_row_arr(ticket_arr_first_row)
        ticket_arr_third_row = self._generate_fastest_first_row_claim_third_row_arr(ticket_arr_first_row, ticket_arr_second_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        return Ticket(ticket_arr, self.game_type, player_index, self.claim_player_index)

    def _generate_ticket_with_technically_accurate_but_invalid_claim(self, player_index):
        ticket_arr = []
        ticket_arr_first_row = self._generate_fastest_first_row_arr_for_ticket_technically_accurate_but_invalid_claim()
        ticket_arr_second_row = self._generate_fastest_first_row_claim_second_row_arr(ticket_arr_first_row)
        ticket_arr_third_row = self._generate_fastest_first_row_claim_third_row_arr(ticket_arr_first_row, ticket_arr_second_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        return Ticket(ticket_arr, self.game_type, player_index, self.claim_player_index)

    def _generate_ticket_with_technically_accurate_and_valid_claim(self, player_index):
        ticket_arr = []
        ticket_arr_first_row = self._generate_fastest_first_row_arr_for_ticket_technically_accurate_and_valid_claim()
        ticket_arr_second_row = self._generate_fastest_first_row_claim_second_row_arr(ticket_arr_first_row)
        ticket_arr_third_row = self._generate_fastest_first_row_claim_third_row_arr(ticket_arr_first_row, ticket_arr_second_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        return Ticket(ticket_arr, self.game_type, player_index, self.claim_player_index)

    def _generate_fastest_first_row_arr_for_ticket_technically_inaccurate_claim(self):
        ticket_arr_first_row = []    
        ticket_arr_first_row_nums = []
        
        first_row_accurate_pop = self.call_seq
        first_row_accurate_subseq = random_sample(first_row_accurate_pop, ROW_LEN - NUM_TECHNICALLY_INACCURATE_NUMS_IN_ROW)
        ticket_arr_first_row_nums.extend(first_row_accurate_subseq)

        calling_seq_range = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX]+1)
        first_row_inaccurate_pop = list(set(calling_seq_range) - set(self.call_seq))
        first_row_inaccurate_subseq = random_sample(first_row_inaccurate_pop, NUM_TECHNICALLY_INACCURATE_NUMS_IN_ROW)
        ticket_arr_first_row_nums.extend(first_row_inaccurate_subseq)
        random_shuffle(ticket_arr_first_row_nums)

        first_row_marks = [True] * ROW_LEN
        ticket_arr_first_row.extend(
            list(
                zip(
                    ticket_arr_first_row_nums, 
                    first_row_marks
                )
            )
        )
        return ticket_arr_first_row

    def _generate_fastest_first_row_arr_for_ticket_technically_accurate_but_invalid_claim(self):
            call_seq_len = len(self.call_seq)
            
            ticket_arr_first_row = []
            ticket_arr_first_row_nums = []

            seq_penultimate_num = self.call_seq[LIST_PENULTIMATE_INDEX]
            first_row_pop = self.call_seq[0:call_seq_len-2]
            first_row_prefix = random_sample(first_row_pop, ROW_LEN-1)
            ticket_arr_first_row_nums.extend(first_row_prefix)
            ticket_arr_first_row_nums.append(seq_penultimate_num)

            first_row_marks = [True] * ROW_LEN
            ticket_arr_first_row.extend(
                list(
                    zip(
                        ticket_arr_first_row_nums, 
                        first_row_marks
                    )
                )
            )
            return ticket_arr_first_row

    def _generate_fastest_first_row_arr_for_ticket_technically_accurate_and_valid_claim(self):
            call_seq_len = len(self.call_seq)
            
            ticket_arr_first_row = []
            ticket_arr_first_row_nums = []
            seq_last_num = self.call_seq[LIST_LAST_INDEX]
            first_row_pop = self.call_seq[0:call_seq_len-1]
            first_row_prefix = random_sample(first_row_pop, ROW_LEN-1)
            ticket_arr_first_row_nums.extend(first_row_prefix)
            ticket_arr_first_row_nums.append(seq_last_num)

            first_row_marks = [True] * ROW_LEN
            ticket_arr_first_row.extend(
                list(
                    zip(
                        ticket_arr_first_row_nums, 
                        first_row_marks
                    )
                )
            )
            return ticket_arr_first_row

    def _generate_fastest_first_row_claim_second_row_arr(self, ticket_arr_first_row):
        ticket_arr_second_row = []
        
        calling_seq_range = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX]+1)
        second_row_pop = list(set(calling_seq_range) - set(ticket_arr_first_row))
        ticket_arr_second_row_nums = random_sample(second_row_pop, ROW_LEN)

        second_row_marks = [random_choice([True, False]) for _ in range(ROW_LEN)]
        ticket_arr_second_row.extend(
            list(
                zip(
                    ticket_arr_second_row_nums, 
                    second_row_marks
                )
            )
        )
        return ticket_arr_second_row

    def _generate_fastest_first_row_claim_third_row_arr(self, ticket_arr_first_row, ticket_arr_second_row):
        ticket_arr_third_row = []
        
        calling_seq_range = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX]+1)
        second_row_pop = list(set(calling_seq_range) - set(ticket_arr_first_row))
        third_row_pop = list(set(second_row_pop) - set(ticket_arr_second_row))
        ticket_arr_third_row_nums = random_sample(third_row_pop, ROW_LEN)
        third_row_marks = [random_choice([True, False]) for _ in range(ROW_LEN)]
        ticket_arr_third_row.extend(
            list(
                zip(
                    ticket_arr_third_row_nums, 
                    third_row_marks
                )
            )
        )
        return ticket_arr_third_row
