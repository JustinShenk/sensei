import os
import pickle
import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from glob import glob


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
    # Get most recent baseline
    return str(sorted(baselines)[-1][1].split(' ')[-1])


def get_distances(data, trimmed=True):
    '''Get tuple of posture measurements with time stamps.

    Returns:
        Tuple - (time_stamp, distances)

    '''
    widths = []
    time_stamps = []
    for k, v in data.items():
        if type(v).__module__ == 'numpy':
            # Convert strings to datetime object
            time_stamp = datetime.datetime.strptime(k, '%Y-%m-%d_%H-%M-%S')
            time_stamps.append(time_stamp)
            widths.append(v[0][2])

    # Sort readings by time to restore order
    time_stamps, widths = zip(*sorted(zip(time_stamps, widths)))

    # Trim data beyond 20 minutes
    if trimmed:
        end = time_stamps[0] + datetime.timedelta(seconds=60 * 21)
        time_stamps = [x for x in time_stamps if x < end]
        widths = widths[:len(time_stamps)]
    return time_stamps, widths


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


def get_subject(data, subject_id='20', trial_number='1'):
    '''Return subject `subject_id`'s data.
    '''
    if type(subject_id) != str:
        subject_id = str(subject_id)
    for d in data:
        if subject_id in d:
            return d[subject_id][trial_number]


def remove_outliers(time_delta, widths, z_threshold=3):
    '''Remove outliers with z-score of `z_threshold` and above
    from `time_delta` and `widths`.
    '''
    mean_y = np.mean(widths)
    stdev_y = np.std(widths)
    z_scores = [(y - mean_y) / stdev_y for y in widths]
    outliers = np.where(np.abs(z_scores) > z_threshold)
    time_keep = np.delete(time_delta, outliers)
    width_keep = np.delete(widths, outliers)
    return time_keep, width_keep


def plot_subjects(data, meta, exclude_outliers=False, z_threshold=3):
    subjects = meta.keys()
    subject_count = len(subjects)
    fig = plt.figure(figsize=(8, subject_count * 3.4))
    for ind, subject in enumerate(subjects):
        conditions = meta[subject]
        ax = fig.add_subplot(subject_count, 1, ind + 1)
        subject_data = get_subject(data, subject_id=subject)
        baseline = get_baseline(subject_data)
        times, widths = get_distances(subject_data)
        time_delta = [(x - times[0]).total_seconds() for x in times]
        if remove_outliers:
            time_delta, widths = remove_outliers(time_delta, widths)
        title = """Head Proximity to Computer over Time
            {}\nSubject ID: {}, Condition: {}, Timepoints: {}
            """.format('Excluding Outliers (z = ' + str(z_threshold) + ') '
                       if exclude_outliers else '', subject, conditions,
                       len(time_delta))

        plot_it(ax, time_delta, widths, baseline=baseline, title=title)
    plt.show()


def draw_warnings(ax, x, y, baseline):
    # Get array of warnings/notifications
    warnings = np.where(np.asarray(y) >= int(baseline) * 1.2)
    warning_x, warning_y = np.asarray(x)[warnings], np.asarray(y)[warnings]
    ax.scatter(
        warning_x, warning_y, color='r', marker='*', label='Notification')


def timeTicks(x, pos):
    minutes, seconds = divmod(int(x), 60)
    return '{}:{:02}'.format(minutes, seconds)


formatter = matplotlib.ticker.FuncFormatter(timeTicks)


def plot_it(ax,
            x,
            y,
            subject_id=None,
            conditions=None,
            baseline=None,
            title=None):
    if title == None:
        title = 'Head Proximity to Computer over Time\n'
        'Subject ID: {} Conditions: {}'.format(subject_id, conditions)
    ax.set_xlabel('Time (minutes)')
    ax.set_ylabel('Proximity')
    ax.set_title(title)
    ax.xaxis.set_major_formatter(formatter)
    ax.set_xlim((0, x[-1]))
    # Plot baseline/calibration
    ax.hlines(int(baseline), 0.0, x[-1], 'g', label='Baseline')
    # Plot warning threshold
    ax.hlines(int(baseline) * 1.2, 0, x[-1], 'r', label='Warning')
    # Draw warning events
    draw_warnings(ax, x, y, baseline)
    ax.plot(x, y, 'b', linewidth=1)
    ax.legend(loc=1, fontsize=8)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=25)
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.show()
