import numpy as np
import pickle
import os
from pathlib import Path

def ensure_dir(directory):
    Path(directory).mkdir(parents=True, exist_ok=True)

def save_training_data(X, y, filename):
    ensure_dir(os.path.dirname(filename))
    with open(filename, 'wb') as f:
        pickle.dump({'X': X, 'y': y}, f)

def load_training_data(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data['X'], data['y']

def state_to_image(state, num_disks):
    img = np.zeros((num_disks, 3))
    for pole_idx, pole in enumerate(state):
        for disk in pole:
            img[num_disks - disk, pole_idx] = 1
    return img

def preprocess_state(state, num_disks):
    arr = np.zeros((3, num_disks))
    for pole_idx, pole in enumerate(state):
        for disk_idx, disk in enumerate(pole):
            arr[pole_idx, disk_idx] = disk / num_disks
    return arr
