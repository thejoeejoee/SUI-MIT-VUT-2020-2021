#!/usr/bin/env python
import os

import numpy as np
import tensorflow as tf

PLAYERS_COUNT = 4

DATA_DIR = os.path.join(os.path.dirname(__file__), '../learning-data')

TEST_DATA = np.load(os.path.join(DATA_DIR, 'data-test.npy'))

TEST_DATA_COUNT = TEST_DATA.shape[0]

def reshape_results(results: np.array) -> np.array:
    return np.reshape(
        tf.keras.utils.to_categorical(
            results,
            num_classes=PLAYERS_COUNT
        ),
        newshape=[results.shape[0], PLAYERS_COUNT]
    )

model = tf.keras.models.load_model('./model-002.h5')

TEST_DATA[:, 435:] = 0

predicted = model.predict(TEST_DATA[:, 1:])

print(np.sum(np.argmax(predicted, axis=1) == TEST_DATA[:, 0]) / TEST_DATA_COUNT)

