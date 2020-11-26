#!/usr/bin/env python3

# Project: VUT FIT SUI Project - Dice Wars
# Authors:
#   - Josef Kolář      <xkolar71@stud.fit.vutbr.cz>
#   - Dominik Harmim   <xharmi00@stud.fit.vutbr.cz>
#   - Petr Kapoun      <xkapou04@stud.fit.vutbr.cz>
#   - Jindřich Šesták  <xsesta05@stud.fit.vutbr.cz>
# Year: 2020
# Description: Generates game configurations.

import random
import sys
from argparse import ArgumentParser
import time
from signal import signal, SIGCHLD

from utils import run_ai_only_game, BoardDefinition

parser = ArgumentParser(prog='Dice_Wars')
parser.add_argument('-p', '--port', help="Server port", type=int, default=5005)
parser.add_argument('-a', '--address', help="Server address", default='127.0.0.1')

procs = []


def signal_handler():
    """ Handler for SIGCHLD signal that terminates server and clients. """
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
]


def board_definitions():
    while True:
        random.seed(int(time.time()))
        yield BoardDefinition(random.randint(1, 10 ** 10), random.randint(1, 10 ** 10), random.randint(1, 10 ** 10))


def main():
    args = parser.parse_args()

    signal(SIGCHLD, signal_handler)

    boards_played = 0
    try:
        for board_definition in board_definitions():
            boards_played += 1

            run_ai_only_game(
                args.port, args.address, procs, PLAYING_AIs,
                board_definition,
                fixed=random.randint(1, 10 ** 10),
                client_seed=random.randint(1, 10 ** 10),
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
