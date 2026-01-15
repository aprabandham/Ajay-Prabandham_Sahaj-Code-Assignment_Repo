from abc import ABC, abstractmethod

class PlayerInterface(ABC):
    @abstractmethod
    def assign_ticket(self, ticket):
        pass

    @abstractmethod
    def raise_game_win_claim(self, call_seq):
        pass
