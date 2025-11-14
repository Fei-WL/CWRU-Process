import os
import pdb
from tqdm import tqdm
import json
import torch
import argparse

import numpy as np

from scipy.io import loadmat
from col_name import DATASET_DICT
from sklearn.preprocessing import StandardScaler

def split_data(data, train_ratio=0.7, val_ratio=0.2):
    length = data.shape[0]
    train_end = int(length * train_ratio)
    val_end = int(length * (train_ratio + val_ratio))
    
    train_data = data[:train_end]
    val_data = data[train_end:val_end]
    test_data = data[val_end:]
    
    return train_data, val_data, test_data

def get_samples(data, input_len, stride, label, id, drop_last=True):
    count = 0
    res = []
    while input_len + count * int(stride * input_len) <= data.shape[0]:
        start = count * int(stride * input_len)
        end = start + input_len
        res.append(data[start:end])
        count += 1
    
    samples = np.array(res)
    labels = np.full(samples.shape[0], label)
    ids = np.full(samples.shape[0], id)
    return samples, labels, ids

def save_data(root_path, inputs, labels, ids, flag):
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    
    np.save(os.path.join(root_path, '{}_inputs.npy'.format(flag)), inputs)
    np.save(os.path.join(root_path, '{}_labels.npy'.format(flag)), labels)
    np.save(os.path.join(root_path, '{}_ids.npy'.format(flag)), ids)
    
    print('{} shape: {}'.format(flag, inputs.shape))

def set_samples(inputs, labels, ids, 
                inputs_list, labels_list, ids_list):
    inputs_list.append(inputs)
    labels_list.append(labels)
    ids_list.append(ids)

def generata_datasets(root_dir: str, 
                      datasets_dict: list, 
                      input_len: int, 
                      stride: float,
                      normalize: bool):
    train_inputs_list = []
    val_inputs_list = []
    test_inputs_list = []
    
    train_labels_list = []
    val_labels_list = []
    test_labels_list = []
    
    train_ids_list = []
    val_ids_list = []
    test_ids_list = []
    
    # Get data from each file according to its label and file path
    for label, dicts in enumerate(datasets_dict):
        for file_path, col_key in dicts.items():
            file_path = os.path.join(root_dir, file_path)
            matdata = loadmat(file_path)[col_key]
            
            train_data, val_data, test_data = split_data(matdata)
            
            train_inputs, train_labels, train_ids = get_samples(train_data, input_len, stride, label, col_key)
            val_inputs, val_labels, val_ids = get_samples(val_data, input_len, stride, label, col_key)
            test_inputs, test_labels, test_ids = get_samples(test_data, input_len, stride, label, col_key)
            
            set_samples(train_inputs, train_labels, train_ids, train_inputs_list, train_labels_list, train_ids_list)
            set_samples(val_inputs, val_labels, val_ids, val_inputs_list, val_labels_list, val_ids_list)
            set_samples(test_inputs, test_labels, test_ids, test_inputs_list, test_labels_list, test_ids_list)
        
    train_inputs = np.concatenate(train_inputs_list, axis=0)
    val_inputs = np.concatenate(val_inputs_list, axis=0)
    test_inputs = np.concatenate(test_inputs_list, axis=0)
    train_labels = np.concatenate(train_labels_list, axis=0)
    val_labels = np.concatenate(val_labels_list, axis=0)
    test_labels = np.concatenate(test_labels_list, axis=0)
    train_ids = np.concatenate(train_ids_list, axis=0)
    val_ids = np.concatenate(val_ids_list, axis=0)
    test_ids = np.concatenate(test_ids_list, axis=0)
    
    # Calculate mean and std from training data for normalization
    if normalize:
        scaler = StandardScaler()
        scaler.fit(train_inputs.squeeze(-1))
        train_inputs = np.expand_dims(scaler.transform(train_inputs.squeeze(-1)), axis=-1)
        val_inputs = np.expand_dims(scaler.transform(val_inputs.squeeze(-1)), axis=-1)
        test_inputs = np.expand_dims(scaler.transform(test_inputs.squeeze(-1)), axis=-1)
    
    return train_inputs, val_inputs, test_inputs, \
            train_labels, val_labels, test_labels, \
            train_ids, val_ids, test_ids

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
        'shape': '[num_samples, seq_len, num_features]',
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
    parser.add_argument('--device', type=str, default='DE')
    parser.add_argument('--freq', type=str, default='12k')
    parser.add_argument('--nclass', type=int, default=4)
    parser.add_argument('--input_len', type=int, default=512)
    parser.add_argument('--stride', type=int, default=0.5)
    parser.add_argument('--normalize', type=bool, default=True)
    args = parser.parse_args()

    key = '{}_{}_{}'.format(args.device, args.freq, args.nclass)
    datasets_dict = DATASET_DICT[key]
    
    train_inputs, val_inputs, test_inputs, \
    train_labels, val_labels, test_labels, \
    train_ids, val_ids, test_ids = generata_datasets(args.root_dir, datasets_dict, args.input_len, args.stride, args.normalize)
    
    save_data('./{}'.format(key), train_inputs, train_labels, train_ids, flag="TRAIN")
    save_data('./{}'.format(key), val_inputs, val_labels, val_ids, flag="VAL")
    save_data('./{}'.format(key), test_inputs, test_labels, test_ids, flag="TEST")
    
    make_description(args)