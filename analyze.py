import os
import pickle
import numpy as np
import matplotlib.pyplot as plt

from glob import glob
from datetime import datetime


def dat_to_dict(data_path):
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
            baselines.append((k, v))
    print(baselines)
    # Get most recent baseline
    return sorted(baselines)[-1][1].split(' ')[-1]


def get_distances(data):
    '''Get tuple of posture measurements with time stamps.

    Returns:
        Tuple - (time_object, distances)

    '''
    widths = []

    for k, v in data.items():
        if type(v).__module__ == 'numpy':
            # Convert strings to datetime object
            time_object = datetime.strptime(k, '%Y-%m-%d_%H-%M-%S')
            widths.append(v[0][2])

    # Sort readings by time to restore order
    time_objects, dists = zip(*sorted(zip(time_objects, widths)))
    return time_object, dists


def get_data_files(data_folder_path='data'):
    data_folder = os.path.join(os.getcwd(), data_folder_path)
    files = []
    for file in glob(data_folder + "/*/*"):
        if '.dat' in file:
            files.append(file)
    return files


def load_all_data(data_folder_path='data'):
    '''Return dictionary with all data in `data_folder_path` folder.
    '''
    files = get_data_files('data')
    data = [dat_to_dict(x) for x in files]
    return data


def get_subject(data, subject_number='20', trial_number='1'):
    '''Return subject's data.
    '''
    for d in data:
        if subject_number in d:
            return d[subject_number][trial_number]


def plot(time_objects, dists):
    pass
