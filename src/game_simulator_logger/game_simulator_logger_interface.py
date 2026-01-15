from abc import ABC, abstractmethod

class GameSimulatorLoggerInterface(ABC):
    @abstractmethod
    def log(self, obj):
        pass
