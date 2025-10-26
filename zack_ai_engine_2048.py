from base_ai_engine_2048 import AIEngine2048
from utils import Keys2048


class ZackAIEngine(AIEngine2048):
    def __repr__(self):
        return "v2.2 of Zack's AI Engine"

    def recommend_next_move(self, board) -> Keys2048:
        return Keys2048.LEFT
