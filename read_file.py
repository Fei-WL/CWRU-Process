import os
import pdb
from tqdm import tqdm
import json
import torch
import argparse

import numpy as np

from scipy.io import loadmat
from col_name import DATASET_DICT

def split_data(data, train_ratio=0.7, val_ratio=0.2):
    length = data.shape[0]
    train_end = int(length * train_ratio)
    val_end = int(length * (train_ratio + val_ratio))
    
    train_data = data[:train_end]
    val_data = data[train_end:val_end]
    test_data = data[val_end:]
    
    return train_data, val_data, test_data

def get_samples(data, input_len, stride, label, drop_last=True):
    count = 0
    res = []
    while input_len + count * int(stride * input_len) <= data.shape[0]:
        start = count * int(stride * input_len)
        end = start + input_len
        res.append(data[start:end])
        count += 1
    
    samples = np.array(res)
    labels = np.full(samples.shape[0], label)
    return samples, labels

def normalize_data(train_mean, train_std, data, eps=1e-8):
    data_norm = (data - train_mean) / (train_std + eps)
    return data_norm

def save_data(root_path, train_data, train_label, val_data, val_label, test_data, test_label):
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    
    np.save(os.path.join(root_path, 'train_inputs.npy'), train_data)
    np.save(os.path.join(root_path, 'train_label.npy'), train_label)
    np.save(os.path.join(root_path, 'val_inputs.npy'), val_data)
    np.save(os.path.join(root_path, 'val_label.npy'), val_label)
    np.save(os.path.join(root_path, 'test_inputs.npy'), test_data)
    np.save(os.path.join(root_path, 'test_label.npy'), test_label)
    
    print('Train shape: {}, Val shape: {}, Test shape: {}'.format(train_data.shape, val_data.shape, test_data.shape))

def generata_datasets(root_dir: str, datasets_dict: list, input_len: int, stride: float):
    train_data_list = []
    val_data_list = []
    test_data_list = []
    
    train_data_labels = []
    val_data_labels = []
    test_data_labels = []
    
    # Get data from each file according to its label and file path
    for label, dicts in enumerate(datasets_dict):
        for file_path, col_key in dicts.items():
            file_path = os.path.join(root_dir, file_path)
            matdata = loadmat(file_path)[col_key]
            
            train_data, val_data, test_data = split_data(matdata)
            
            train_samples, train_labels = get_samples(train_data, input_len, stride, label)
            val_samples, val_labels = get_samples(val_data, input_len, stride, label)
            test_samples, test_labels = get_samples(test_data, input_len, stride, label)
            
            train_data_list.append(train_samples)
            val_data_list.append(val_samples)
            test_data_list.append(test_samples)
            
            train_data_labels.append(train_labels)
            val_data_labels.append(val_labels)
            test_data_labels.append(test_labels)

    train_data = np.expand_dims(np.concatenate(train_data_list, axis=0), axis=-1)
    val_data = np.expand_dims(np.concatenate(val_data_list, axis=0), axis=-1)
    test_data = np.expand_dims(np.concatenate(test_data_list, axis=0), axis=-1)
    train_labels = np.concatenate(train_data_labels, axis=0)
    val_labels = np.concatenate(val_data_labels, axis=0)
    test_labels = np.concatenate(test_data_labels, axis=0)
    
    # Calculate mean and std from training data for normalization
    train_mean = np.mean(train_data)
    train_std = np.std(train_data)
    norm_train_data = normalize_data(train_mean, train_std, train_data)
    norm_val_data = normalize_data(train_mean, train_std, val_data)
    norm_test_data = normalize_data(train_mean, train_std, test_data)
    
    return norm_train_data, norm_val_data, norm_test_data, train_labels, val_labels, test_labels

def make_description(args):
    name = '{}_{}_{}'.format(args.device, args.freq, args.nclass)
    description = {
        'name': name,
        'num_classes': args.nclass,
        'class_names': [str(i) for i in range(args.nclass)],
        'equal_length': True,
        'seq_len': args.input_len,
        'num_nodes': 1,
        'num_features': 1,
        'shape': '[num_samples, seq_len, num_nodes, num_features]',
        'missing': False,
        'filling_missing': 'NA',
        'norm_each_channel': True
    }
    description_path = os.path.join('./{}'.format(name), 'desc.json')
    with open(description_path, 'w') as f:
        json.dump(description, f, indent=4)
    print(f'{name} is finished.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read MATLAB .mat files for bearing data')
    
    parser.add_argument('--root_dir', type=str, default='./raw_data')
    parser.add_argument('--normal', type=bool, default=True)
    parser.add_argument('--device', type=str, default='DE')
    parser.add_argument('--freq', type=str, default='12k')
    parser.add_argument('--nclass', type=int, default=4)
    parser.add_argument('--input_len', type=int, default=512)
    parser.add_argument('--stride', type=int, default=0.5)
    args = parser.parse_args()

    key = '{}_{}_{}'.format(args.device, args.freq, args.nclass)
    datasets_dict = DATASET_DICT[key]
    
    train_inputs, val_inputs, test_inputs, train_labels, val_labels, test_labels = generata_datasets(args.root_dir, datasets_dict, args.input_len, args.stride)
    
    save_data('./{}'.format(key), train_inputs, train_labels, val_inputs, val_labels, test_inputs, test_labels)
    make_description(args)