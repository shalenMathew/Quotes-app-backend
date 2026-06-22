from abc import ABC, abstractmethod


class AIProvider(ABC):

    @abstractmethod
    def generate_quotes(self, count: int):
        pass