# Copyright 2019, Imperial College London
# 
# Tutorial for CO416 - Machine Learning for Imaging
#
# This file: Functions to manage data.

import numpy as np
import torchvision.datasets as dset
import scipy.misc

def get_mnist(data_dir, train, download=False):
    # data_dir: path to local directory where data is, or should be stored.
    # train: if True, return training data. If False, return test data.
    # download: if data not in data_dir, download it.
    data_set = dset.MNIST(root=data_dir, train=train, transform=None, download=False)
    # Students should only deal with numpy arrays, so that it's easy to follow.
    if train:
        data_x = np.asarray(data_set.train_data, dtype='uint8')
        data_y = np.asarray(data_set.train_labels, dtype='int16') # int64 by default
    else:
        data_x = np.asarray(data_set.test_data, dtype='uint8')
        data_y = np.asarray(data_set.test_labels, dtype='int16') # int64 by default
    return data_x, data_y

def make_lbls_onehot(lbls, num_classes):
    # lbls: np.array of shape [N]
    lbls_onehot = np.zeros(shape=(lbls.shape[0], num_classes ) )
    lbls_onehot[ np.arange(lbls_onehot.shape[0]), lbls ] = 1
    return lbls_onehot
    
def normalize_int_whole_database(data):
    # data: shape [num_samples, H, W, C]
    mu = np.mean(data, axis=(0,1,2), keepdims=True) # Mean int of channel C, over samples and pixels.
    std = np.std(data, axis=(0,1,2), keepdims=True) # Returned shape: [1, 1, 1, C]
    norm_data = (data - mu) / std
    return norm_data
    
    
def get_tumor_data(data_dir, train):
    if train:
        paths_to_imgs =[data_dir + "/image_0.png",
                        data_dir + "/image_1.png"]
        paths_to_gts = [data_dir + "/segmentation_0.png",
                        data_dir + "/segmentation_1.png"]
    else: # test
        paths_to_imgs =[data_dir + "/image_2.png"]
        paths_to_gts = [data_dir + "/segmentation_2.png"]

    assert len(paths_to_imgs) == len(paths_to_gts)
    data_x = None
    data_y = None
    for i in range(len(paths_to_imgs)):
        img = scipy.misc.imread(paths_to_imgs[i]) # [H, W]
        img = np.reshape(img, newshape=[1]+list(img.shape)) # [1, H, W]
        gt  = scipy.misc.imread(paths_to_gts[i]) # [H, W]
        gt  = np.reshape(gt, newshape=[1]+list(gt.shape)) # [1, H, W]
        if data_x is None:
            data_x = img.copy()
            data_y = gt.copy()
        else:
            data_x = np.concatenate((data_x, img), axis=0) # [N, H, W]
            data_y = np.concatenate((data_y, gt), axis=0) # [N, H, W]
            
    # When you save imgs as pngs from nii, they are turned to [0,255] values. Turn them back.
    #print('Image intensities in data on disk [min,max]= [', np.min(data_x), np.max(data_x))
    #print('Values in ground truth on disk = ', np.unique(data_y))
    data_x = (data_x - np.mean(data_x, axis=(1,2), keepdims=True))/np.std(data_x, axis=(1,2), keepdims=True)
    data_y[data_y>0] = 1
    #print('Image intensities in data after normalization [min,max]= [', np.min(data_x), np.max(data_x))
    #print('Values in ground truth after normalization = ', np.unique(data_y))
    return data_x, data_y








