from abc import ABC, abstractmethod

class ClaimValidatorInterface(ABC):
    @abstractmethod
    def validate_player_claim(self, call_seq, ticket, claiming_player_type=None, claiming_player_sub_type=None):
        pass
