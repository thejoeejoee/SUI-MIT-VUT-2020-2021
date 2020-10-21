from .xkolar71 import AI as OriginalAI
from ..client.game.board import Board


class AI(OriginalAI):
    def _batch_heuristic(self, board: Board) -> dict:
        return {
            i: self._heuristic(player_name=i, board=board)
            for i in self._players_order
        }

__all__ = ['AI']