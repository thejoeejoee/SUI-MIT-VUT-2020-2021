import os
import pickle
from os import makedirs
from typing import Dict, Tuple, Iterable

from dicewars.server.area import Area
from dicewars.server.board import Board
from dicewars.server.game import Game
from dicewars.server.player import Player

MAX_AREA_COUNT = 30
MAX_PLAYER_COUNT = 30

GameConfiguration = Tuple[int]

LOG_DIR = os.path.join(os.path.dirname(__file__), '../../learning-data')


def serialize_game_configuration(game: Game) -> GameConfiguration:
    """
    Serializes current game configuration to integer vector of static length:
    435 triangle from matrix of neighbor areas (30x30, but just half)
    30 areas owners
    30 dices counts
    30 biggest regions
    30 reserves
    ==
    555 integers
    """
    board: Board = game.board
    areas: Dict[int, Area] = board.areas
    players: Dict[int, Player] = game.players

    board_state = []
    # generates triangle matrix of neighbor areas
    for column_area_id in range(1, MAX_AREA_COUNT):
        column_area = areas.get(column_area_id)

        neighbors = column_area.get_adjacent_areas_names() if column_area else {}

        board_state.extend([
            int((col_id + 1) in neighbors)
            for col_id in range(column_area_id, MAX_AREA_COUNT)
        ])

    # generates areas owners
    board_state.extend([
        area.owner_name if (area := areas.get(area_id + 1)) else 0
        for area_id in range(MAX_AREA_COUNT)
    ])

    # generates dices counts
    board_state.extend([
        area.dice if (area := areas.get(area_id + 1)) else 0
        for area_id in range(MAX_AREA_COUNT)
    ])

    # size of biggest region of each player
    board_state.extend([
        p.get_largest_region(board) if (p := players.get(player_id + 1)) else 0
        for player_id in range(MAX_PLAYER_COUNT)
    ])

    # dices in reserve of each player
    board_state.extend([
        p.get_reserve() if (p := players.get(player_id + 1)) else 0
        for player_id in range(MAX_PLAYER_COUNT)
    ])

    return tuple(map(int, board_state))


def save_game_configurations(winner_index: int, configurations: Iterable[GameConfiguration]):
    """
    Saves configurations from finished game to folder by index of winner.
    """
    winner_dir = os.path.join(LOG_DIR, f'{winner_index}')
    makedirs(winner_dir, exist_ok=True)

    for conf in configurations:
        conf_hash = str(hash(conf))
        conf_file = os.path.join(winner_dir, conf_hash)
        with open(conf_file, 'wb') as f:
            pickle.dump(conf, f)


def serialize_board_configuration(board: Board) -> GameConfiguration:
    """
    Serializes current game configuration to integer vector of static length:
    435 triangle from matrix of neighbor areas (30x30, but just half)
    30 areas owners
    30 dices counts
    30 biggest regions
    30 reserves
    ==
    555 integers
    """
    areas: Dict[int, Area] = board.areas
    players: Dict[int, Player] = dict()

    board_state = []
    # generates triangle matrix of neighbor areas
    for column_area_id in range(1, MAX_AREA_COUNT):
        column_area = areas.get(column_area_id)

        neighbors = column_area.get_adjacent_areas_names() if column_area else {}

        board_state.extend([
            int((col_id + 1) in neighbors)
            for col_id in range(column_area_id, MAX_AREA_COUNT)
        ])

    # generates areas owners
    board_state.extend([
        area.owner_name if (area := areas.get(area_id + 1)) else 0
        for area_id in range(MAX_AREA_COUNT)
    ])

    # generates dices counts
    board_state.extend([
        area.dice if (area := areas.get(area_id + 1)) else 0
        for area_id in range(MAX_AREA_COUNT)
    ])

    # size of biggest region of each player
    board_state.extend([
        p.get_largest_region(board) if (p := players.get(player_id + 1)) else 0
        for player_id in range(MAX_PLAYER_COUNT)
    ])

    # dices in reserve of each player
    board_state.extend([
        p.get_reserve() if (p := players.get(player_id + 1)) else 0
        for player_id in range(MAX_PLAYER_COUNT)
    ])

    return tuple(map(int, board_state))