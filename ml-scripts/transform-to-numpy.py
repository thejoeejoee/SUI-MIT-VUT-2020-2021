import os
import sys
from os import listdir

import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../sui-learning-data')

winners = listdir(DATA_DIR)

PACKAGES = dict(
    train=slice(0, 17),
    val=slice(17, 17 + 5),
    test=slice(17 + 5, 17 + 5 + 3),
)

for name, slc in PACKAGES.items():
    slc = slice(slc.start * 1000, slc.stop * 1000)

    loaded_files = 0
    data = np.empty((0, 556), dtype=int)

    for winner in winners:
        if winner not in '1234':
            continue

        winner_id = int(winner)

        for conf in listdir(os.path.join(DATA_DIR, winner))[slc]:
            pth = os.path.join(DATA_DIR, winner, conf)

            line = np.concatenate((
                [winner_id - 1],
                np.load(pth, allow_pickle=True)
            ))
            data = np.concatenate(
                ([line], data),
            )
            loaded_files += 1

            if not loaded_files % 1000:
                print(f'Loaded {loaded_files} configurations for {name}.', file=sys.stderr)

    np.save(os.path.join(DATA_DIR, f'learning-data-{name}'), data)
