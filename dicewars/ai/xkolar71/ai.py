# Project: VUT FIT SUI Project - Dice Wars
# Authors:
#   - Josef Kolář      <xkolar71@stud.fit.vutbr.cz>
#   - Dominik Harmim   <xharmi00@stud.fit.vutbr.cz>
#   - Petr Kapoun      <xkapou04@stud.fit.vutbr.cz>
#   - Jindřich Šesták  <xsesta05@stud.fit.vutbr.cz>
# Year: 2020
# Description: A definition of a class that represents an AI agent for
#              the Dice Wars game.

from logging import getLogger
from typing import List, Union, Tuple, Iterator
from dicewars.client.ai_driver import BattleCommand, EndTurnCommand
from dicewars.client.game.board import Board
from dicewars.client.game.area import Area
from ..utils import possible_attacks, probability_of_successful_attack, \
    probability_of_holding_area


class AI:
    """ A class that represents an AI agent for the Dice Wars game. """

    __LOGGER_NAME = 'AI xkolar71'  #: name of a logger
    __MAX_DICE = 8  #: maximum number of dice on a single area

    #: weight of a largest region for the heuristic function
    __LARGEST_REG_HEURISTIC_WEIGHT = 50
    __REG_HEURISTIC_WEIGHT = 5  #: weight of a region for the heuristic function

    __MAXN_TURNS_LIMIT = 5  #: limit a number of turns for the Max^n algorithm
    __MAXN_TIME_THRESHOLD = 1.  #: time treshold for the Max^n algorithm

    __ATK_PROB_TRESHOLD = .2  #: atack probability treshold
    #: weight for a preference of attack from a largest region
    __ATK_FROM_LARGEST_REG_WEIGHT = 3
    #: limit for a number of players to use '..._2' parameters
    __ATK_PLAYERS_LIMIT_2 = 2
    __ATK_PROB_TRESHOLD_2 = .4  #: atack probability treshold for more players
    #: weight for a preference of attack from a largest region for more players
    __ATK_FROM_LARGEST_REG_WEIGHT_2 = 2

    def __init__(self, player_name: int, board: Board, players_order: List[int]
                 ) -> None:
        """
        Constructs the AI agent for the Dice Wars game.

        :param player_name: A name (ID) of the associated player.
        :param board: A copy of the game board.
        :param players_order: An order in which the players take turn. (A list
               of players IDs.)
        """
        super().__init__()

        self.__player_name = player_name
        self.__board = board
        self.__players_order = players_order
        self.__loger = getLogger(self.__LOGGER_NAME)

        nb_players = board.nb_players_alive()
        self.__loger.debug(
            f'An AI agent for the {nb_players}-player game is set up.'
            f' player_name: {player_name}; players_order: {players_order}'
        )

    def ai_turn(self, board: Board, nb_moves_this_turn: int,
                nb_turns_this_game: int, time_left: float
                ) -> Union[BattleCommand, EndTurnCommand]:
        """
        A single turn of the AI agent.

        :param board: A copy of the game board.
        :param nb_moves_this_turn: A number of attacks made in this turn.
        :param nb_turns_this_game: A number of turns ended in this game.
        :param time_left: A time (in seconds) left after last turn.
        :return: Either 'BattleCommand' for atacking an enemy or
                 'EndTurnCommand' for ending this turn.
        """
        self.__board = board
        self.__loger.debug(
            f'Looking suitable turns.'
            f' nb_moves_this_turn: {nb_moves_this_turn};'
            f' nb_turns_this_game: {nb_turns_this_game}; time_left: {time_left}'
        )

        if time_left >= self.__MAXN_TIME_THRESHOLD \
                and nb_moves_this_turn < self.__MAXN_TURNS_LIMIT:
            # TODO
            return EndTurnCommand()

        turns = self.__possible_turns(self.__player_name, board)
        if turns:
            turn = turns[0]
            self.__loger.debug(f'Possible turn: {turn[0]} -> {turn[1]}.')

            return BattleCommand(turn[0], turn[1])

        self.__loger.debug('No more suitable turns.')

        return EndTurnCommand()

    def __possible_turns(self, player_name: int, board: Board
                         ) -> List[Tuple[int, int, float]]:
        """
        Returns possible turns with higher hold probability than a trashold.

        :param player_name: A name (ID) of the associated player.
        :param board: The game board.
        :return: Possible turns with higher hold probability than a trashold.
                 (A tuple (atacker area; defender area; weight) sorted
                 by the weight in descending order.)
        """
        if board.nb_players_alive() > self.__ATK_PLAYERS_LIMIT_2:
            atk_prob_treshold = self.__ATK_PROB_TRESHOLD_2
            atk_from_larges_reg_weight = self.__ATK_FROM_LARGEST_REG_WEIGHT_2
        else:
            atk_prob_treshold = self.__ATK_PROB_TRESHOLD
            atk_from_larges_reg_weight = self.__ATK_FROM_LARGEST_REG_WEIGHT

        turns = []
        largest_region = self.__largest_region(player_name, board)

        # noinspection PyTypeChecker
        atks: Iterator[Tuple[Area, Area]] = possible_attacks(board, player_name)
        for a, b in atks:
            a_name = a.get_name()
            b_name = b.get_name()
            atk_power = a.get_dice()

            p = probability_of_successful_attack(board, a_name, b_name)
            p *= probability_of_holding_area(board, b_name, atk_power - 1,
                                             player_name)

            if p >= atk_prob_treshold or atk_power == self.__MAX_DICE:
                if a_name in largest_region:
                    p *= atk_from_larges_reg_weight
                turns.append((a_name, b_name, p))

        return sorted(turns, key=lambda t: t[2], reverse=True)

    @staticmethod
    def __largest_region(player_name: int, board: Board) -> List[int]:
        """
        Returns the largest region of a given player.

        :param player_name: A name (ID) of the associated player.
        :param board: The game board.
        :return: The largest region of a given player. (A list of region
                 names (IDs) in the largest region.)
        """
        players_regions = board.get_players_regions(player_name)
        max_region_size = max(len(region) for region in players_regions)

        return [r for r in players_regions if len(r) == max_region_size][0]

    def __heuristic(self, player_name: int, board: Board) -> int:
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
