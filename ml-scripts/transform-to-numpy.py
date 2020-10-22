#!/usr/bin/env python3

import os
import pickle
import sys
from os import listdir

import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../sui-learning-data-seeded')

winners = listdir(DATA_DIR)

loaded_confs = 0
data = np.empty((0, 499 + 1), dtype=int)

for winner in winners:
    if winner not in '1234':
        continue

    winner_id = int(winner)

    for conf in listdir(os.path.join(DATA_DIR, winner)):
        pth = os.path.join(DATA_DIR, winner, conf)

        with open(pth, 'br') as f:
            one_game_confs = pickle.load(file=f)

        items_count = len(one_game_confs)
        # one_game_confs_with_targets = np.empty((items_count, data.shape[1]))
        #
        # one_game_confs_with_targets[:, 1:] = np.array(list(one_game_confs))
        # one_game_confs_with_targets[:, 0] = winner_id - 1
        #
        # data = np.concatenate(
        #     (one_game_confs_with_targets, data),
        # )
        loaded_confs += items_count

        print(f'Loaded {loaded_confs} (+{items_count}) configurations.', file=sys.stderr)

np.save(os.path.join(DATA_DIR, f'learning-data'), data)
