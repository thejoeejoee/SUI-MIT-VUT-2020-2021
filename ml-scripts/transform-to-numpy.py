import os
from os import listdir

import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), '../learning-data')

winners = listdir(DATA_DIR)

data = np.empty((0, 556), dtype=int)

confs_count = 0

for winner in winners:
    winner_id = int(winner)

    for conf in listdir(os.path.join(DATA_DIR, winner))[8000:8000+8000]:
        pth = os.path.join(DATA_DIR, winner, conf)

        line = np.concatenate(([winner_id - 1], np.load(pth, allow_pickle=True)))
        data = np.concatenate(
            ([line], data),
        )
        confs_count += 1

        if not confs_count % 1000:
            print(f'Loaded {confs_count} confs.')

np.save(os.path.join(DATA_DIR, 'learning-data-32k-02'), data)