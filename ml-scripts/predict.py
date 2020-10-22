#!/usr/bin/env python3
import os

import numpy as np
import tensorflow as tf

PLAYERS_COUNT = 4

DATA_DIR = os.path.join(os.path.dirname(__file__), '../learning-data')

TEST_DATA = np.load(os.path.join(DATA_DIR, 'data-test.npy'))

def reshape_results(results: np.array) -> np.array:
    return np.reshape(
        tf.keras.utils.to_categorical(
            results,
            num_classes=PLAYERS_COUNT
        ),
        newshape=[results.shape[0], PLAYERS_COUNT]
    )

model = tf.keras.models.load_model('./model-002.h5')
def wtf_wtf_foo():
    predicted = model.predict(TEST_DATA[:10, 1:])

def wtf_wtf_bar():
    predicted = model.predict(TEST_DATA[:10, 1:])


wtf_wtf_bar()
wtf_wtf_foo()

