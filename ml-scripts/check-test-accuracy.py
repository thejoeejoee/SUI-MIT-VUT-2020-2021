#!/usr/bin/env python3
import os

import numpy as np
import tensorflow as tf
PLAYERS_COUNT = 4

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../sui-learning-data-mixed')

TEST_DATA = np.load(os.path.join(DATA_DIR, 'data-test.npy'))
# TEST_DATA = np.load(os.path.join(DATA_DIR, 'learning-data.npy'))

TEST_DATA_COUNT = TEST_DATA.shape[0]

model = tf.keras.models.load_model(os.path.join(os.path.dirname(__file__), 'model-005.h5'))

# TEST_DATA[:, 1:435] = 0

predicted = model.predict(TEST_DATA[:, 1:])

print(np.sum(np.argmax(predicted, axis=1) == TEST_DATA[:, 0]) / TEST_DATA_COUNT)

