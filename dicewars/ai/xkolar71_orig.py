from .xkolar71 import AI as OriginalAI
from ..client.game.board import Board


class AI(OriginalAI):
    __LARGEST_REG_HEURISTIC_WEIGHT = 50
    """ weight of a largest region for the heuristic function """
    __REG_HEURISTIC_WEIGHT = 5
    """ weight of a region for the heuristic function """

    def _batch_heuristic(self, board: Board) -> dict:
        return {
            i: self._heuristic(player_name=i, board=board)
            for i in self._players_order
        }

    def _heuristic(self, player_name: int, board: Board) -> int:
        """
        Rturns the heuristic evaluation of a given board for a given player.

        :param player_name: A name (ID) of the associated player.
        :param board: The game board.
        :return: The heuristic evaluation of a given board for a given player.
        """
        h = board.get_player_dice(player_name)

        players_regions = board.get_players_regions(player_name)
        players_regions_sizes = []
        for region in players_regions:
            region_size = len(region)
            h += self.__REG_HEURISTIC_WEIGHT * region_size

            players_regions_sizes.append(region_size)

        h += self.__LARGEST_REG_HEURISTIC_WEIGHT * max(players_regions_sizes)

        return h

__all__ = ['AI']