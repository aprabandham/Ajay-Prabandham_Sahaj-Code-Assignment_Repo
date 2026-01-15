from src.ticket_generator.ticket_generator_interface import TicketGeneratorInterface
from src.ticket.ticket import Ticket
from src.common import CALL_SEQ_RANGE_LIMITS, CALL_SEQ_RANDOM_LEN_LIMITS, NUM_PLAYERS, MIN_NUM_GAME_PLAYERS, round_game_type, game_claim_player_index, round_player_index, LOWER_INDEX, UPPER_INDEX, ROW_LEN, NUM_ROWS, game_win_claim_types, NUM_TECHNICALLY_INACCURATE_NUMS_IN_ROW, LIST_PENULTIMATE_INDEX, LIST_LAST_INDEX, possible_claiming_player_types, possible_non_claiming_player_types, possible_claiming_player_technically_inaccurate_sub_types, possible_claiming_player_technically_accurate_but_invalid_sub_types, possible_claiming_player_technically_accurate_and_valid_sub_types
from random import sample as random_sample, choice as random_choice, shuffle as random_shuffle

class FastestFullHouseTicketGenerator(TicketGeneratorInterface):
    def __init__(self, call_seq, num_players, game_type, claim_player_index, claiming_player_type, claiming_player_sub_type):
        if len(call_seq) < CALL_SEQ_RANDOM_LEN_LIMITS[LOWER_INDEX]:
            raise ValueError(f"Calling Sequence Length less than permitted lower limit - {CALL_SEQ_RANDOM_LEN_LIMITS[0]}!")
        
        if len(call_seq) > CALL_SEQ_RANDOM_LEN_LIMITS[UPPER_INDEX]:
            raise ValueError(f"Calling Sequence Length greater than permitted upper limit - {CALL_SEQ_RANDOM_LEN_LIMITS[1]}!")

        if num_players < MIN_NUM_GAME_PLAYERS or num_players > NUM_PLAYERS:
            raise ValueError(f"The number of game players needs to be at least {MIN_NUM_GAME_PLAYERS}!")

        if game_type != round_game_type["FASTEST_FULL_HOUSE"]:
            raise ValueError("The value provided for Game Type is not permitted!")

        if claim_player_index != game_claim_player_index["FASTEST_FULL_HOUSE"]:
            raise ValueError("The value provided for Claim Player Index is not permitted!")

        if claiming_player_type not in [
            possible_claiming_player_types["TECHNICALLY_INACCURATE"],
            possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"],
            possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]]:

            raise ValueError("The Claiming Player Type value provided is not permitted!")

        if (claiming_player_type == possible_claiming_player_types["TECHNICALLY_INACCURATE"]
            and claiming_player_sub_type not in [
            possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_1"],
            possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_2"],
            possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_3"]]):

            raise ValueError("The Claiming Player Sub-Type value provided is not permitted!")

        if (claiming_player_type == possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"]
            and claiming_player_sub_type not in [
            possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_1"],
            possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_2"],
            possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_3"]]):

            raise ValueError("The Claiming Player Sub-Type value provided is not permitted!")

        if (claiming_player_type == possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]
            and claiming_player_sub_type not in [
            possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"],
            possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_2"],
            possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_3"]]):

            raise ValueError("The Claiming Player Sub-Type value provided is not permitted!")

        super().__init__(call_seq, num_players, game_type, claim_player_index, claiming_player_type)
        self.claiming_player_sub_type = claiming_player_sub_type

        self.claiming_player_type_ticket_gen_refs_map[self.game_type] = {
            possible_claiming_player_types["TECHNICALLY_INACCURATE"]: {},
            possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"]: {},
            possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]: {}
        }

        self.claiming_player_type_ticket_gen_refs_map[self.game_type][possible_claiming_player_types["TECHNICALLY_INACCURATE"]][possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_1"]] = self._generate_ticket_with_technically_inaccurate_claim_type_1
        self.claiming_player_type_ticket_gen_refs_map[self.game_type][possible_claiming_player_types["TECHNICALLY_INACCURATE"]][possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_2"]] = self._generate_ticket_with_technically_inaccurate_claim_type_2
        self.claiming_player_type_ticket_gen_refs_map[self.game_type][possible_claiming_player_types["TECHNICALLY_INACCURATE"]][possible_claiming_player_technically_inaccurate_sub_types["TECHNICALLY_INACCURATE_TYPE_3"]] = self._generate_ticket_with_technically_inaccurate_claim_type_3
        
        self.claiming_player_type_ticket_gen_refs_map[self.game_type][possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"]][possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_1"]] = self._generate_ticket_with_technically_accurate_but_invalid_claim_type_1
        self.claiming_player_type_ticket_gen_refs_map[self.game_type][possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"]][possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_2"]] = self._generate_ticket_with_technically_accurate_but_invalid_claim_type_2
        self.claiming_player_type_ticket_gen_refs_map[self.game_type][possible_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"]][possible_claiming_player_technically_accurate_but_invalid_sub_types["TECHNICALLY_ACCURATE_BUT_INVALID_TYPE_3"]] = self._generate_ticket_with_technically_accurate_but_invalid_claim_type_3
        
        self.claiming_player_type_ticket_gen_refs_map[self.game_type][possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]][possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_1"]] = self._generate_ticket_with_technically_accurate_and_valid_claim_type_1
        self.claiming_player_type_ticket_gen_refs_map[self.game_type][possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]][possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_2"]] = self._generate_ticket_with_technically_accurate_and_valid_claim_type_2
        self.claiming_player_type_ticket_gen_refs_map[self.game_type][possible_claiming_player_types["TECHNICALLY_ACCURATE_AND_VALID"]][possible_claiming_player_technically_accurate_and_valid_sub_types["TECHNICALLY_ACCURATE_AND_VALID_TYPE_3"]] = self._generate_ticket_with_technically_accurate_and_valid_claim_type_3

        self.non_claiming_player_type_ticket_gen_refs_map[self.game_type][possible_non_claiming_player_types["TECHNICALLY_INACCURATE"]] = self._generate_ticket_with_technically_inaccurate_claim_type_1
        self.non_claiming_player_type_ticket_gen_refs_map[self.game_type][possible_non_claiming_player_types["TECHNICALLY_ACCURATE_BUT_INVALID"]] = self._generate_ticket_with_technically_accurate_but_invalid_claim_type_2
        self.non_claiming_player_type_ticket_gen_refs_map[self.game_type][possible_non_claiming_player_types["TECHNICALLY_ACCURATE_AND_POTENTIALLY_VALID_BUT_UNRAISED"]] = self._generate_ticket_with_technically_accurate_and_valid_claim_type_3

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
        ticket = self.claiming_player_type_ticket_gen_refs_map[self.game_type][self.claiming_player_type][self.claiming_player_sub_type](player_index)

        return ticket

    def _generate_tickets_for_non_claiming_players(self):
        tickets_list = []
        ticket = None
         
        for i, non_claiming_player_type_index in enumerate(possible_non_claiming_player_types.values()):
            ticket = self.non_claiming_player_type_ticket_gen_refs_map[self.game_type][non_claiming_player_type_index](self.non_claiming_player_indexes[i])
            tickets_list.append(ticket)

        return tickets_list

    def _generate_ticket_with_technically_inaccurate_claim_type_1(self, player_index):
        ticket_arr = []
        ticket_arr_first_row = self._generate_row_arr_for_ticket_technically_inaccurate_claim()
        ticket_arr_second_row = self._generate_row_arr_for_ticket_technically_inaccurate_claim_one(ticket_arr_first_row)
        ticket_arr_third_row = self._generate_row_arr_for_ticket_technically_inaccurate_claim_two(ticket_arr_first_row, ticket_arr_second_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        return Ticket(ticket_arr, self.game_type, player_index, self.claim_player_index, self.claiming_player_type, self.claiming_player_sub_type)

    def _generate_ticket_with_technically_inaccurate_claim_type_2(self, player_index):
        ticket_arr = []
        ticket_arr_second_row = self._generate_row_arr_for_ticket_technically_inaccurate_claim()
        ticket_arr_first_row = self._generate_row_arr_for_ticket_technically_inaccurate_claim_one(ticket_arr_second_row)
        ticket_arr_third_row = self._generate_row_arr_for_ticket_technically_inaccurate_claim_two(ticket_arr_second_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        return Ticket(ticket_arr, self.game_type, player_index, self.claim_player_index, self.claiming_player_type, self.claiming_player_sub_type)

    def _generate_ticket_with_technically_inaccurate_claim_type_3(self, player_index):
        ticket_arr = []
        ticket_arr_third_row = self._generate_row_arr_for_ticket_technically_inaccurate_claim()
        ticket_arr_first_row = self._generate_row_arr_for_ticket_technically_inaccurate_claim_one(ticket_arr_third_row)
        ticket_arr_second_row = self._generate_row_arr_for_ticket_technically_inaccurate_claim_two(ticket_arr_third_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        return Ticket(ticket_arr, self.game_type, player_index, self.claim_player_index, self.claiming_player_type, self.claiming_player_sub_type)

    def _generate_ticket_with_technically_accurate_but_invalid_claim_type_1(self, player_index):
        ticket_arr = []
        ticket_arr_first_row = self._generate_row_arr_for_ticket_technically_accurate_but_invalid_claim()
        ticket_arr_second_row = self._generate_row_arr_for_ticket_technically_accurate_but_invalid_claim_one(ticket_arr_first_row)
        ticket_arr_third_row = self._generate_row_arr_for_ticket_technically_accurate_but_invalid_claim_two(ticket_arr_first_row, ticket_arr_second_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        return Ticket(ticket_arr, self.game_type, player_index, self.claim_player_index, self.claiming_player_type, self.claiming_player_sub_type)

    def _generate_ticket_with_technically_accurate_but_invalid_claim_type_2(self, player_index):
        ticket_arr = []
        ticket_arr_second_row = self._generate_row_arr_for_ticket_technically_accurate_but_invalid_claim()
        ticket_arr_first_row = self._generate_row_arr_for_ticket_technically_accurate_but_invalid_claim_one(ticket_arr_second_row)
        ticket_arr_third_row = self._generate_row_arr_for_ticket_technically_accurate_but_invalid_claim_two(ticket_arr_second_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        return Ticket(ticket_arr, self.game_type, player_index, self.claim_player_index, self.claiming_player_type, self.claiming_player_sub_type)

    def _generate_ticket_with_technically_accurate_but_invalid_claim_type_3(self, player_index):
        ticket_arr = []
        ticket_arr_third_row = self._generate_row_arr_for_ticket_technically_accurate_but_invalid_claim()
        ticket_arr_first_row = self._generate_row_arr_for_ticket_technically_accurate_but_invalid_claim_one(ticket_arr_third_row)
        ticket_arr_second_row = self._generate_row_arr_for_ticket_technically_accurate_but_invalid_claim_two(ticket_arr_third_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        return Ticket(ticket_arr, self.game_type, player_index, self.claim_player_index, self.claiming_player_type, self.claiming_player_sub_type)

    def _generate_ticket_with_technically_accurate_and_valid_claim_type_1(self, player_index):
        ticket_arr = []
        ticket_arr_first_row = self._generate_row_arr_for_ticket_technically_accurate_and_valid_claim()
        ticket_arr_second_row = self._generate_row_arr_for_ticket_technically_accurate_and_valid_claim_one(ticket_arr_first_row)
        ticket_arr_third_row = self._generate_row_arr_for_ticket_technically_accurate_and_valid_claim_two(ticket_arr_first_row, ticket_arr_second_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        return Ticket(ticket_arr, self.game_type, player_index, self.claim_player_index, self.claiming_player_type, self.claiming_player_sub_type)

    def _generate_ticket_with_technically_accurate_and_valid_claim_type_2(self, player_index):
        ticket_arr = []
        ticket_arr_second_row = self._generate_row_arr_for_ticket_technically_accurate_and_valid_claim()
        ticket_arr_first_row = self._generate_row_arr_for_ticket_technically_accurate_and_valid_claim_one(ticket_arr_second_row)
        ticket_arr_third_row = self._generate_row_arr_for_ticket_technically_accurate_and_valid_claim_two(ticket_arr_second_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        return Ticket(ticket_arr, self.game_type, player_index, self.claim_player_index, self.claiming_player_type, self.claiming_player_sub_type)

    def _generate_ticket_with_technically_accurate_and_valid_claim_type_3(self, player_index):
        ticket_arr = []
        ticket_arr_third_row = self._generate_row_arr_for_ticket_technically_accurate_and_valid_claim()
        ticket_arr_first_row = self._generate_row_arr_for_ticket_technically_accurate_and_valid_claim_one(ticket_arr_third_row)
        ticket_arr_second_row = self._generate_row_arr_for_ticket_technically_accurate_and_valid_claim_two(ticket_arr_third_row, ticket_arr_first_row)

        ticket_arr.append(ticket_arr_first_row)
        ticket_arr.append(ticket_arr_second_row)
        ticket_arr.append(ticket_arr_third_row)

        return Ticket(ticket_arr, self.game_type, player_index, self.claim_player_index, self.claiming_player_type, self.claiming_player_sub_type)

    def _generate_row_arr_for_ticket_technically_inaccurate_claim(self):
        ticket_arr_row = []    
        ticket_arr_row_nums = []
        
        row_accurate_pop = self.call_seq
        row_accurate_subseq = random_sample(row_accurate_pop, ROW_LEN - NUM_TECHNICALLY_INACCURATE_NUMS_IN_ROW)
        ticket_arr_row_nums.extend(row_accurate_subseq)

        
        calling_seq_range = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX]+1)
        row_inaccurate_pop = list(set(calling_seq_range) - set(self.call_seq))
        row_inaccurate_subseq = random_sample(row_inaccurate_pop, NUM_TECHNICALLY_INACCURATE_NUMS_IN_ROW)
        ticket_arr_row_nums.extend(row_inaccurate_subseq)
        random_shuffle(ticket_arr_row_nums)

        row_marks = [False] * ROW_LEN
        for i, num in enumerate(ticket_arr_row_nums):
            if num in self.call_seq:
                row_marks[i] = True

        ticket_arr_row.extend(
            list(
                zip(
                    ticket_arr_row_nums, 
                    row_marks
                )
            )
        )
        return ticket_arr_row

    def _generate_row_arr_for_ticket_technically_inaccurate_claim_one(self, row_one):
        ticket_arr_row = []
        
        calling_seq_range = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX]+1)
        row_pop = list(set(calling_seq_range) - set(self.call_seq).intersection(set(row_one)))
        ticket_arr_row_nums = random_sample(row_pop, ROW_LEN)

        row_marks = [False] * ROW_LEN
        for i, num in enumerate(ticket_arr_row_nums):
            if num in self.call_seq:
                row_marks[i] = True

        ticket_arr_row.extend(
            list(
                zip(
                    ticket_arr_row_nums, 
                    row_marks
                )
            )
        )
        return ticket_arr_row

    def _generate_row_arr_for_ticket_technically_inaccurate_claim_two(self, row_one, row_two):
        ticket_arr_row = []
        
        calling_seq_range = range(CALL_SEQ_RANGE_LIMITS[LOWER_INDEX], CALL_SEQ_RANGE_LIMITS[UPPER_INDEX]+1)
        first_row_pop = list(set(calling_seq_range) - set(row_one))
        second_row_pop = list(set(first_row_pop) - set(row_two))
        ticket_arr_row_nums = random_sample(second_row_pop, ROW_LEN)

        row_marks = [False] * ROW_LEN
        for i, num in enumerate(ticket_arr_row_nums):
            if num in self.call_seq:
                row_marks[i] = True
        
        ticket_arr_row.extend(
            list(
                zip(
                    ticket_arr_row_nums, 
                    row_marks
                )
            )
        )
        return ticket_arr_row    

    def _generate_row_arr_for_ticket_technically_accurate_but_invalid_claim(self):
            call_seq_len = len(self.call_seq)
            
            ticket_arr_row = []
            ticket_arr_row_nums = []

            seq_penultimate_num = self.call_seq[LIST_PENULTIMATE_INDEX]
            row_pop = self.call_seq[0:call_seq_len-2]
            row_prefix = random_sample(row_pop, ROW_LEN-1)
            ticket_arr_row_nums.extend(row_prefix)
            ticket_arr_row_nums.append(seq_penultimate_num)

            row_marks = [True] * ROW_LEN
            ticket_arr_row.extend(
                list(
                    zip(
                        ticket_arr_row_nums, 
                        row_marks
                    )
                )
            )
            return ticket_arr_row

    def _generate_row_arr_for_ticket_technically_accurate_but_invalid_claim_one(self, row_one):
        ticket_arr_row = []
        call_seq_len = len(self.call_seq)

        row_pop = list(set(self.call_seq[0:call_seq_len-1]) - set(row_one))
        ticket_arr_row_nums = random_sample(row_pop, ROW_LEN)

        row_marks = [True] * ROW_LEN
        ticket_arr_row.extend(
            list(
                zip(
                    ticket_arr_row_nums, 
                    row_marks
                )
            )
        )
        return ticket_arr_row

    def _generate_row_arr_for_ticket_technically_accurate_but_invalid_claim_two(self, row_one, row_two):
        ticket_arr_row = []
        call_seq_len = len(self.call_seq)
        
        first_row_pop = list(set(self.call_seq[0:call_seq_len-1]) - set(row_one))
        second_row_pop = list(set(first_row_pop) - set(row_two))
        ticket_arr_row_nums = random_sample(second_row_pop, ROW_LEN)

        row_marks = [True] * ROW_LEN
        ticket_arr_row.extend(
            list(
                zip(
                    ticket_arr_row_nums, 
                    row_marks
                )
            )
        )
        return ticket_arr_row

    def _generate_row_arr_for_ticket_technically_accurate_and_valid_claim_one(self, row_one):
        ticket_arr_row = []
        
        row_pop = list(set(self.call_seq) - set(row_one))
        ticket_arr_row_nums = random_sample(row_pop, ROW_LEN)

        row_marks = [True] * ROW_LEN
        ticket_arr_row.extend(
            list(
                zip(
                    ticket_arr_row_nums, 
                    row_marks
                )
            )
        )
        return ticket_arr_row

    def _generate_row_arr_for_ticket_technically_accurate_and_valid_claim_two(self, row_one, row_two):
        ticket_arr_row = []
        
        first_row_pop = list(set(self.call_seq) - set(row_one))
        second_row_pop = list(set(first_row_pop) - set(row_two))
        ticket_arr_row_nums = random_sample(second_row_pop, ROW_LEN)
        row_marks = [True] * ROW_LEN
        ticket_arr_row.extend(
            list(
                zip(
                    ticket_arr_row_nums, 
                    row_marks
                )
            )
        )
        return ticket_arr_row

    def _generate_row_arr_for_ticket_technically_accurate_and_valid_claim(self):
            call_seq_len = len(self.call_seq)
            
            ticket_arr_row = []
            ticket_arr_row_nums = []
            seq_last_num = self.call_seq[LIST_LAST_INDEX]
            row_pop = self.call_seq[0:call_seq_len-1]
            row_prefix = random_sample(row_pop, ROW_LEN-1)
            ticket_arr_row_nums.extend(row_prefix)
            ticket_arr_row_nums.append(seq_last_num)

            row_marks = [True] * ROW_LEN
            ticket_arr_row.extend(
                list(
                    zip(
                        ticket_arr_row_nums, 
                        row_marks
                    )
                )
            )
            return ticket_arr_row
