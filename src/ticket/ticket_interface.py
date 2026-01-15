from abc import ABC, abstractmethod

class TicketInterface(ABC):
    @abstractmethod
    def get_first_row(self):
        pass

    @abstractmethod
    def get_second_row(self):
        pass

    @abstractmethod
    def get_third_row(self):
        pass

    @abstractmethod
    def get_all_rows(self):
        pass
