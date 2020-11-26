# Project: VUT FIT SUI Project - Dice Wars
# Authors:
#   - Josef Kolář      <xkolar71@stud.fit.vutbr.cz>
#   - Dominik Harmim   <xharmi00@stud.fit.vutbr.cz>
#   - Petr Kapoun      <xkapou04@stud.fit.vutbr.cz>
#   - Jindřich Šesták  <xsesta05@stud.fit.vutbr.cz>
# Year: 2020
# Description: An original implementation of the 'xkolar71' agent.

from typing import List, Dict

from .xkolar71 import AI as NEW_AI
from dicewars.client.game.board import Board


class AI(NEW_AI):
    __LARGEST_REG_HEURISTIC_WEIGHT = 50
    """ weight of a largest region for the heuristic function """
    __REG_HEURISTIC_WEIGHT = 5
    """ weight of a region for the heuristic function """

    def _heuristic(self, players: List[int], board: Board) -> Dict[int, float]:
        """
        Computes the heuristic function for all the given players.

        :param players: Names of players.
        :param board: The game board.
        :return: A dictionary where keys are names of given players and values
                 are values of the heuristic function for these players in a
                 current game board.
        """
        h = {}
        for player in players:
            h[player] = board.get_player_dice(player)

            players_regions = board.get_players_regions(player)
            players_regions_sizes = []
            for region in players_regions:
                region_size = len(region)
                h[player] += self.__REG_HEURISTIC_WEIGHT * region_size
                players_regions_sizes.append(region_size)

            h[player] += \
                self.__LARGEST_REG_HEURISTIC_WEIGHT * max(players_regions_sizes)

        return h
