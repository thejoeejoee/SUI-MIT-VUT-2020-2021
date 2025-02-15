#!/usr/bin/env python3

# Project: VUT FIT SUI Project - Dice Wars
# Authors:
#   - Josef Kolář      <xkolar71@stud.fit.vutbr.cz>
#   - Dominik Harmim   <xharmi00@stud.fit.vutbr.cz>
#   - Petr Kapoun      <xkapou04@stud.fit.vutbr.cz>
#   - Jindřich Šesták  <xsesta05@stud.fit.vutbr.cz>
# Year: 2020
# Description: Shuffles and splits the learning data.

import os

import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../sui-learning-data-mixed')

data = np.load(os.path.join(DATA_DIR, 'learning-data.npy'))
DATA_COUNT = data.shape[0]

np.random.shuffle(data)

TRAIN_RATIO, VALIDATE_RATIO, TEST_RATIO = .7, .2, .1
assert 1 - (TRAIN_RATIO + VALIDATE_RATIO + TEST_RATIO) < 0.01

TRAIN_DATA_COUNT = int(TRAIN_RATIO * DATA_COUNT)
VALIDATE_DATA_COUNT = int(VALIDATE_RATIO * DATA_COUNT)
TEST_DATA_COUNT = int(TEST_RATIO * DATA_COUNT)

np.save(
    os.path.join(DATA_DIR, 'data-train.npy'),
    data[:TRAIN_DATA_COUNT, :]
)

np.save(
    os.path.join(DATA_DIR, 'data-val.npy'),
    data[TRAIN_DATA_COUNT:TRAIN_DATA_COUNT+VALIDATE_DATA_COUNT, :]
)

np.save(
    os.path.join(DATA_DIR, 'data-test.npy'),
    data[TRAIN_DATA_COUNT+VALIDATE_DATA_COUNT:, :]
)
