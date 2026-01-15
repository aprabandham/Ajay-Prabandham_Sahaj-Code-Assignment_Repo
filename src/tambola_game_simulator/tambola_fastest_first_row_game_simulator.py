from src.tambola_game_simulator.tambola_game_simulator_interface import TambolaGameSimulatorInterface
from src.calling_sequence.calling_sequence_generator import CallingSequenceGenerator
from src.calling_sequence.calling_sequence_len_generator import CallingSequenceLenGenerator
from src.ticket_generator.fastest_first_row_ticket_generator import FastestFirstRowTicketGenerator
from src.player_generator.player_generator import PlayerGenerator
from src.player.player import Player
from src.ticket.ticket import Ticket
from src.caller.caller import Caller
from src.claim_validator.claim_validator import ClaimValidator
from src.game_simulator_logger import game_simulator_file_logger
from src.common import NUM_PLAYERS, round_game_type, round_player_index, game_claim_player_index, possible_claiming_player_types, round_game_name

class TambolaFastestFirstRowGameSimulator(TambolaGameSimulatorInterface):
    def __init__(self, game_type, call_seq_len_gen, call_seq_gen, player_gen, ticket_gen, claim_validator, caller, player_index_list, game_simulator_file_logger):
        if game_type !=  round_game_type["FASTEST_FIRST_ROW"]:
            raise ValueError("the provided Game Type value is not permitted!")

        if not call_seq_len_gen:
            raise ValueError("The Call Sequence Length generator Ref cannot be None!")

        if not call_seq_gen:
            raise ValueError("The Call Sequence Length Generator Ref cannot be None!")

        if not ticket_gen:
            raise ValueError("The Ticket Generator Ref cannot be None!")

        if not claim_validator:
            raise ValueError("The Claim Validator Ref cannot be None!")

        if player_index_list == []:
            raise ValueError("The Player List cannot be empty!")

        if len(player_index_list) > NUM_PLAYERS:
            raise ValueError(f"The number of Game Players cannot exceed {NUM_PLAYERS}!")

        super().__init__(game_type, call_seq_len_gen, call_seq_gen, player_gen, ticket_gen, claim_validator, caller, player_index_list, game_simulator_file_logger)

    def validate_fastest_row_technically_inaccurate_claim(self):
        self.log_message_to_file(f"Tambola Game Simulator INACCURATE Claim Validation - for Game {self.game_type} - {round_game_name[self.game_type]}")
        player_list = self.player_gen.generate_player_list()
        ticket_list = self.ticket_gen.generate_ticket_list()

        for ticket in ticket_list:
            self.log_message_to_file(ticket)
            for player in player_list:
                if ticket.player_index == player.player_index:
                    self.log_message_to_file(player)
                    player.assign_ticket(ticket)

        validation_result = False
        for player in player_list:
            if player.player_index == game_claim_player_index["FASTEST_FIRST_ROW"]:

                self.log_message_to_file("Claiming Player is raising a claim for their Ticket")
                self.log_message_to_file(f"Claiming Player Index for Game = {game_claim_player_index["FASTEST_FIRST_ROW"]}")
                self.log_message_to_file(player)
                self.log_message_to_file(ticket)
                self.log_message_to_file("Vlaidation of Claim involves Comparing this ticket to the generated Calling Sequence:")
                self.log_message_to_file(f"Calling Sequence now = {self.caller.call_seq}")
                self.log_message_to_file(f"SORTED Calling Sequence (to help verify) = {sorted(self.caller.call_seq)}")

                validation_result = player.raise_game_win_claim(self.caller.call_seq)

        return validation_result

    def validate_fastest_row_technically_accurate_but_invalid_claim(self):
        self.log_message_to_file(f"Tambola Game Simulator ACCURATE-BUT-INVALID Claim Validation - for Game {self.game_type} - {round_game_name[self.game_type]}")
        player_list = self._player_gen.generate_player_list()
        ticket_list = self.ticket_gen.generate_ticket_list()

        for ticket in ticket_list:
            self.log_message_to_file(ticket)
            for player in player_list:
                if ticket.player_index == player.player_index:
                    self.log_message_to_file(player)
                    player.assign_ticket(ticket)

        validation_result = False
        for player in player_list:
            if player.player_index == game_claim_player_index["FASTEST_FIRST_ROW"]:

                self.log_message_to_file("Claiming Player is raising a claim for their Ticket")
                self.log_message_to_file(f"Claiming Player Index for Game = {game_claim_player_index["FASTEST_FIRST_ROW"]}")
                self.log_message_to_file(player)
                self.log_message_to_file(ticket)
                self.log_message_to_file("Vlaidation of Claim involves Comparing this ticket to the generated Calling Sequence:")
                self.log_message_to_file(f"Calling Sequence now = {self.caller.call_seq}")
                self.log_message_to_file(f"SORTED Calling Sequence (to help verify) = {sorted(self.caller.call_seq)}")

                validation_result = player.raise_game_win_claim(self.caller.call_seq)

        return validation_result

    def validate_fastest_row_technically_accurate_and_valid_claim(self):
        self.log_message_to_file(f"Tambola Game Simulator ACCURATE-AND-VALID Claim Validation - for Game {self.game_type} - {round_game_name[self.game_type]}")
        player_list = self._player_gen.generate_player_list()
        ticket_list = self.ticket_gen.generate_ticket_list()

        for ticket in ticket_list:
            self.log_message_to_file(ticket)
            for player in player_list:
                if ticket.player_index == player.player_index:
                    self.log_message_to_file(player)
                    player.assign_ticket(ticket)

        validation_result = False
        for player in player_list:
            if player.player_index == game_claim_player_index["FASTEST_FIRST_ROW"]:

                self.log_message_to_file("Claiming Player is raising a claim for their Ticket")
                self.log_message_to_file(f"Claiming Player Index for Game = {game_claim_player_index["FASTEST_FIRST_ROW"]}")
                self.log_message_to_file(player)
                self.log_message_to_file(ticket)
                self.log_message_to_file("Vlaidation of Claim involves Comparing this ticket to the generated Calling Sequence:")
                self.log_message_to_file(f"Calling Sequence now = {self.caller.call_seq}")
                self.log_message_to_file(f"SORTED Calling Sequence (to help verify) = {sorted(self.caller.call_seq)}")

                validation_result = player.raise_game_win_claim(self.caller.call_seq)

        return validation_result
