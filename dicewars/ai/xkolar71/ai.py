from typing import List, Union

from dicewars.client.ai_driver import BattleCommand, EndTurnCommand
from dicewars.client.game.board import Board


class AI:
    def __init__(
            self,
            player_name: int,
            board: Board,
            players_order: List[int]
    ) -> None:
        ...

    def ai_turn(
            self,
            board: Board,
            nb_moves_this_turn: int,
            nb_turns_this_game: int,
            time_left: float
    ) -> Union[BattleCommand, EndTurnCommand]:
        return EndTurnCommand()
