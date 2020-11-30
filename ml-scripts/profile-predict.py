#!/usr/bin/env python3

# Project: VUT FIT SUI Project - Dice Wars
# Authors:
#   - Josef Kolář      <xkolar71@stud.fit.vutbr.cz>
#   - Dominik Harmim   <xharmi00@stud.fit.vutbr.cz>
#   - Petr Kapoun      <xkapou04@stud.fit.vutbr.cz>
#   - Jindřich Šesták  <xsesta05@stud.fit.vutbr.cz>
# Year: 2020
# Description: Predicts test part of dataset for profiling the predict performance.


import os

import numpy as np
import tensorflow as tf

PLAYERS_COUNT = 4

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../sui-learning-data-mixed')

TEST_DATA = np.load(os.path.join(DATA_DIR, 'data-test.npy'))


def reshape_results(results: np.array) -> np.array:
    return np.reshape(
        tf.keras.utils.to_categorical(
            results,
            num_classes=PLAYERS_COUNT
        ),
        newshape=[results.shape[0], PLAYERS_COUNT]
    )


model = tf.keras.models.load_model(os.path.join(os.path.dirname(__file__), 'model.h5'))


def predict_profiled_first():
    model.predict(TEST_DATA[:, 1:])


def predict_profiled_second():
    model.predict(TEST_DATA[:, 1:])


if __name__ == '__main__':
    predict_profiled_first()
    predict_profiled_second()
