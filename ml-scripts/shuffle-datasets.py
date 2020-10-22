#!/usr/bin/env python3

import os

import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../sui-learning-data')

TRAIN_DATA = np.load(os.path.join(DATA_DIR, 'learning-data-train.npy'))
TRAIN_DATA_COUNT = TRAIN_DATA.shape[0]

VALIDATE_DATA = np.load(os.path.join(DATA_DIR, 'learning-data-val.npy'))
VALIDATE_DATA_COUNT = VALIDATE_DATA.shape[0]

TEST_DATA = np.load(os.path.join(DATA_DIR, 'learning-data-test.npy'))
TEST_DATA_COUNT = TEST_DATA.shape[0]

data = np.concatenate((
    TRAIN_DATA, VALIDATE_DATA, TEST_DATA,
))

np.random.shuffle(data)

np.save(
    os.path.join(DATA_DIR, 'data-train.npy'),
    data[:TRAIN_DATA_COUNT,]
)

np.save(
    os.path.join(DATA_DIR, 'data-val.npy'),
    data[TRAIN_DATA_COUNT:TRAIN_DATA_COUNT+VALIDATE_DATA_COUNT,]
)

np.save(
    os.path.join(DATA_DIR, 'data-test.npy'),
    data[TRAIN_DATA_COUNT+VALIDATE_DATA_COUNT:,]
)

