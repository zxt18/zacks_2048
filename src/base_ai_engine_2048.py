from abc import ABC, abstractmethod
from src.utils import Keys2048


class AIEngine2048(ABC):
    """
    Abstract Base Class for AI Engine's that could be injected into our 2048 class
    """

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def recommend_next_move(self, board) -> Keys2048:
        pass
