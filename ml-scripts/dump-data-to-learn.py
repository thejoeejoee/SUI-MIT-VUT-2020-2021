#!/usr/bin/env python3
import random
import sys
from argparse import ArgumentParser
from signal import signal, SIGCHLD

from utils import run_ai_only_game, BoardDefinition

parser = ArgumentParser(prog='Dice_Wars')
parser.add_argument('-p', '--port', help="Server port", type=int, default=5005)
parser.add_argument('-a', '--address', help="Server address", default='127.0.0.1')
parser.add_argument('-b', '--board', help="Seed for generating board", type=int, default=random.randint(0, 10 ** 10))
parser.add_argument('-s', '--seed', help="Seed sampling players for a game", type=int)

procs = []


def signal_handler(signum, frame):
    """Handler for SIGCHLD signal that terminates server and clients
    """
    for p in procs:
        try:
            p.kill()
        except ProcessLookupError:
            pass


PLAYING_AIs = [
    'xkolar71_orig',
    'xkolar71_2',
    'xkolar71_3',
    'xkolar71_4',
    # 'dt.rand',
    # 'dt.sdc',
    # 'dt.ste',
    # 'dt.stei',
]
UNIVERSAL_SEED = 42


def board_definitions(initial_board_seed):
    board_seed = initial_board_seed
    while True:
        yield BoardDefinition(board_seed, UNIVERSAL_SEED, UNIVERSAL_SEED)
        if board_seed is not None:
            board_seed += 1


def main():
    args = parser.parse_args()

    random.seed(args.seed)

    signal(SIGCHLD, signal_handler)

    boards_played = 0
    try:
        for board_definition in board_definitions(args.board):
            boards_played += 1

            run_ai_only_game(
                args.port, args.address, procs, PLAYING_AIs,
                board_definition,
                fixed=UNIVERSAL_SEED,
                client_seed=UNIVERSAL_SEED,
                debug=True, logdir='logs',
            )
            print(f'Played {boards_played} games.', file=sys.stderr)

    except (Exception, KeyboardInterrupt) as e:
        sys.stderr.write("Breaking the tournament because of {}\n".format(repr(e)))
        for p in procs:
            p.kill()
        raise


if __name__ == '__main__':
    main()
