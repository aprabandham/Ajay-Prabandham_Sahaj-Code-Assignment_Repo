from abc import ABC, abstractmethod

class PlayerGeneratorInterface(ABC):
    @abstractmethod
    def generate_player_list(self):   
        pass
