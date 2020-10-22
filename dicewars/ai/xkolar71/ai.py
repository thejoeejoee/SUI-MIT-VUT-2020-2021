# Project: VUT FIT SUI Project - Dice Wars
# Authors:
#   - Josef Kolář      <xkolar71@stud.fit.vutbr.cz>
#   - Dominik Harmim   <xharmi00@stud.fit.vutbr.cz>
#   - Petr Kapoun      <xkapou04@stud.fit.vutbr.cz>
#   - Jindřich Šesták  <xsesta05@stud.fit.vutbr.cz>
# Year: 2020
# Description: A definition of a class that represents an AI agent for
#              the Dice Wars game.
import os
from logging import getLogger
from typing import List, Union, Tuple, Deque, Dict
from copy import deepcopy
from collections import deque
from dicewars.client.ai_driver import BattleCommand, EndTurnCommand
from dicewars.client.game.board import Board
from ..utils import possible_attacks, probability_of_successful_attack, \
    probability_of_holding_area
import tensorflow as tf

from ...ml.game import serialize_game_configuration

LOCAL_DIR = os.path.dirname(__file__)


class AI:
    """ A class that represents an AI agent for the Dice Wars game. """

    __LOGGER_NAME = 'AI xkolar71'
    """ name of a logger """
    __MAX_DICE = 8
    """ maximum number of dice on a single area """

    __MAXN_TURNS_LIMIT = 5
    """ limit a number of turns for the Max^n algorithm """
    __MAXN_TOTAL_TURNS_LIMIT = 1000
    """ limit the total number of turns for the Max^n algorithm to ensure 
        termination """
    __MAXN_TIME_THRESHOLD = 1.
    """ time treshold (in seconds) for the Max^n algorithm """
    __MAXN_DEPTH = 5
    """ depth of the Max^n algorithm """
    __MAXN_ITERS = 1
    """ number of iterations of the Max^n algorithm """

    __ATK_PROB_TRESHOLD = .2
    """ atack probability treshold """
    __ATK_FROM_LARGEST_REG_WEIGHT = 3
    """ weight for a preference of attack from a largest region """
    __ATK_PLAYERS_LIMIT_2 = 2
    """ limit for a number of players to use '..._2' parameters """
    __ATK_PROB_TRESHOLD_2 = .4
    """ atack probability treshold for more players """
    __ATK_FROM_LARGEST_REG_WEIGHT_2 = 2
    """ weight for a preference of attack from a largest region for more 
        players """

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
        self._players_order = players_order
        self.__loger = getLogger(self.__LOGGER_NAME)

        self.__model = tf.keras.models.load_model(os.path.join(LOCAL_DIR, 'model.h5'))

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
        :return: Either 'BattleCommand(a, b)' for atacking an enemy area 'b'
                 from an area 'a' or 'EndTurnCommand()' for ending this turn.
        """
        self.__board = board
        self.__loger.debug(
            f'Looking for suitable turns.'
            f' nb_moves_this_turn: {nb_moves_this_turn};'
            f' nb_turns_this_game: {nb_turns_this_game}; time_left: {time_left}'
        )

        # use the Max^n algorithm if possible
        if time_left >= self.__MAXN_TIME_THRESHOLD \
                and nb_moves_this_turn < self.__MAXN_TURNS_LIMIT \
                and nb_turns_this_game < self.__MAXN_TOTAL_TURNS_LIMIT:
            turn = self.__maxn(self.__player_name, board)
            if turn is None:
                return EndTurnCommand()

            a, b = turn
            self.__loger.debug(f'Max^n turn: {a} -> {b}.')

            return BattleCommand(a, b)

        # use the single turn expectiminimax if there are feasible turns
        turns = self.__possible_turns(self.__player_name, board)
        if turns:
            a, b = turns[0]
            self.__loger.debug(f'Possible turn: {a} -> {b}.')

            return BattleCommand(a, b)

        self.__loger.debug('No more suitable turns.')

        return EndTurnCommand()

    def __possible_turns(self, player_name: int, board: Board
                         ) -> List[Tuple[int, int]]:
        """
        Returns possible turns with higher hold probability than a trashold.
        (The single turn expectiminimax.)

        :param player_name: A name (ID) of the associated player.
        :param board: The game board.
        :return: Possible turns with higher hold probability than a trashold.
                 (A list of tuples (atacker area; defender area) sorted by
                 a weight in descending order.)
        """
        if board.nb_players_alive() > self.__ATK_PLAYERS_LIMIT_2:
            atk_prob_treshold = self.__ATK_PROB_TRESHOLD_2
            atk_from_larges_reg_weight = self.__ATK_FROM_LARGEST_REG_WEIGHT_2
        else:
            atk_prob_treshold = self.__ATK_PROB_TRESHOLD
            atk_from_larges_reg_weight = self.__ATK_FROM_LARGEST_REG_WEIGHT

        turns = []
        largest_region = self.__largest_region(player_name, board)

        for a, b in possible_attacks(board, player_name):
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

        turns = sorted(turns, key=lambda t: t[2], reverse=True)
        turns = list(map(lambda t: t[:2], turns))

        return turns

    @staticmethod
    def __largest_region(player_name: int, board: Board) -> List[int]:
        """
        Returns the largest region of a given player.

        :param player_name: A name (ID) of the associated player.
        :param board: The game board.
        :return: The largest region of a given player. (A list of area
                 names (IDs) in the largest region.)
        """
        players_regions = board.get_players_regions(player_name)
        max_region_size = max(len(r) for r in players_regions)

        return [r for r in players_regions if len(r) == max_region_size][0]

    @staticmethod
    def __perform_atack(board: Board, a_name: int, b_name: int) -> None:
        """
        Performes a successful atack.

        :param board: The game board.
        :param a_name: A name of an atacker area.
        :param b_name: A name of a defender area.
        """
        a = board.get_area(a_name)
        b = board.get_area(b_name)

        b.set_dice(a.get_dice() - 1)
        a.set_dice(1)
        b.set_owner(a_name)

    def __maxn(self, player_name: int, board: Board,
               ) -> Union[Tuple[int, int], None]:
        """
        An interface for the Max^n recursive algorithm.

        :param player_name: A name (ID) of the associated player.
        :param board: The game board.
        :return: A result of the Max^n algorithm (method '__maxn_rec').
                 I.e., a tuple (atacker area, defender area) with the
                 best turn, or None in case there is no suitable turn.
        """
        # construct a queue of players to be considered (in appropriate order)
        players = deque(self._players_order)
        players.reverse()
        while players[-1] != player_name:
            players.rotate(1)
        players_copy = deepcopy(players)
        for _ in range(self.__MAXN_ITERS - 1):
            players.extend(players_copy)

        # ignore values of the heuristic function
        turn, _ = self.__maxn_rec(deepcopy(board), players, self.__MAXN_DEPTH)

        return turn

    def __maxn_rec(self, board: Board, players_names: Deque[int], depth: int,
                   ) -> Tuple[Union[Tuple[int, int], None], Dict[int, int]]:
        """
        The Max^n recursive algorithm. It uses the single turn expectiminimax
        for the computation of the best moves in the individual turns.

        :param board: A copy of the game board.
        :param players_names: A queue of players (names of players, i.e., IDs)
               to be considered in this algorithm. The player on the top of the
               queue is a currently associated player. After a player is
               processed, he is removed from the queue.
        :param depth: A depth of the algorithm. It declinines with recursive
               calls of this method.
        :return: A tuple where the first item is a tuple (atacker area,
                 defender area) with the best turn, or None in case there is
                 no suitable turn. And the second item of the tuple is
                 a dictionary where keys are names of players and values
                 are values of the heuristic function for these players in
                 a current game board.
        """
        # there are no more players
        if not players_names:
            # just evaluate the heuristic function for the AI's player
            return None, self._batch_heuristic(board=board)

        player_name = players_names[-1]
        # current player is not alive => skip him
        if not board.get_player_areas(player_name):
            players_names.pop()
            board_copy = deepcopy(board)

            return self.__maxn_rec(board_copy, players_names, depth)

        # depth is not 0 => expand lower nodes
        if depth:
            # expand some lower suitable nodes, according to the single turn
            # expectiminimax, the number of nodes to be expanded is decreasing
            # with a depth
            turns = self.__possible_turns(player_name, board)[:depth]
            if not turns:
                # no further moves possible => return just the heuristic
                # in a leaf node
                _, h = self.__maxn_rec(deepcopy(board), players_names, 0)

                return None, h

            h = {}
            turn = 0, 0
            for a, b in turns:
                board_copy = deepcopy(board)
                self.__perform_atack(board_copy, a, b)  # simulate an atack
                _, new_h = self.__maxn_rec(board_copy, players_names, depth - 1)

                # maximise the heuristic for a current player
                if player_name in new_h:
                    if player_name not in h \
                            or new_h[player_name] > h[player_name]:
                        h = deepcopy(new_h)
                        turn = a, b

            return turn if h else None, h

        # depth is 0 => advance to further players or compute the heuristic

        players_names.pop()
        # there are furthe players
        if players_names:
            return self.__maxn_rec(
                deepcopy(board), players_names, self.__MAXN_DEPTH
            )

        evaluated = self._batch_heuristic(board=board)
        # compute the heuristic function for all living players
        living_players = set(a.get_owner_name() for a in board.areas.values())
        h = {}
        for player_name in living_players:
            h[player_name] = evaluated.get(player_name)

        return None, h

    def _batch_heuristic(self, board: Board) -> dict:
        # TODO: doc
        serialized = serialize_game_configuration(board=board)

        prediction = self.__model.predict([serialized])[0]

        return {i: v for i, v in enumerate(prediction, start=1)}