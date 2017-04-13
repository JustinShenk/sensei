import os
import pickle
import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime


def load_data(data_path):
    '''Return dictionary `data` from string `data_path`
    '''
    os.path.join(data_path, '1.dat')
    data = pickle.load(open(data_path, 'rb'))
    return data


def get_baseline(data):
    '''Get most recent baseline/calibration from subject.
    '''
    baselines = []
    for k, v in data.items():
        if 'baseline' in v:
            print(k, v)
            baselines.append((k, v))
    # Get most recent baseline
    return sorted(baselines)[-1][1].split(' ')[-1]


def get_distances(data):
    '''Get tuple of posture measurements with time stamps.

    Returns:
        Tuple - (time_object, distances)

    '''
    distances = []

    for k, v in data.items():
        if type(v).__module__ == 'numpy':
            # Convert strings to datetime object
            time_object = datetime.strptime(k, '%Y-%m-%d_%H-%M-%S')
            distances.append((time_object, v[0][2]))

    # Sort readings by time to restore order
    time_objects, dists = zip(*sorted(zip(time_objects, widths)))
    return time_object, dists


def plot(time_objects, dists):
    pass
