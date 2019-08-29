import os
import glob
from sklearn.model_selection import train_test_split
import json
import random
import os
from PIL import Image, ImageFilter, ImageDraw
import numpy as np
import h5py
from PIL import ImageStat
import cv2
import os
import random
import torch
import numpy as np
from torch.utils.data import Dataset
from PIL import Image
import torchvision.transforms.functional as F
from torchvision import datasets, transforms

"""
create a list of file (full directory)
"""

def create_training_image_list(data_path):
    """
    create a list of absolutely path of jpg file
    :param data_path: must contain subfolder "images" with *.jpg  (example ShanghaiTech/part_A/train_data/)
    :return:
    """
    DATA_PATH = data_path
    image_path_list = glob.glob(os.path.join(DATA_PATH, "images", "*.jpg"))
    return image_path_list


def get_train_val_list(data_path, test_size=0.1):
    DATA_PATH = data_path
    image_path_list = glob.glob(os.path.join(DATA_PATH, "images", "*.jpg"))
    if len(image_path_list) is 0:
        image_path_list = glob.glob(os.path.join(DATA_PATH, "*.jpg"))
    train, val = train_test_split(image_path_list, test_size=test_size)

    print("train size ", len(train))
    print("val size ", len(val))
    return train, val


def load_data(img_path, train=True):
    gt_path = img_path.replace('.jpg', '.h5').replace('images', 'ground-truth-h5')
    img = Image.open(img_path).convert('RGB')
    gt_file = h5py.File(gt_path, 'r')
    target = np.asarray(gt_file['density'])

    target = cv2.resize(target, (int(target.shape[1] / 8), int(target.shape[0] / 8)),
                        interpolation=cv2.INTER_CUBIC) * 64

    return img, target


def load_data_ucf_cc50(img_path, train=True):
    gt_path = img_path.replace('.jpg', '.h5')
    img = Image.open(img_path).convert('RGB')
    gt_file = h5py.File(gt_path, 'r')
    target = np.asarray(gt_file['density'])

    target = cv2.resize(target, (int(target.shape[1] / 8), int(target.shape[0] / 8)),
                        interpolation=cv2.INTER_CUBIC) * 64

    return img, target

def load_data_ucf_cc50_pancnn(img_path, train=True):
    gt_path = img_path.replace('.jpg', '.h5')
    img = Image.open(img_path).convert('RGB')
    gt_file = h5py.File(gt_path, 'r')
    target = np.asarray(gt_file['density'])

    if train:
        crop_size = (int(img.size[0] / 2), int(img.size[1] / 2))
        if random.randint(0, 9) <= -1:

            dx = int(random.randint(0, 1) * img.size[0] * 1. / 2)
            dy = int(random.randint(0, 1) * img.size[1] * 1. / 2)
        else:
            dx = int(random.random() * img.size[0] * 1. / 2)
            dy = int(random.random() * img.size[1] * 1. / 2)

        img = img.crop((dx, dy, crop_size[0] + dx, crop_size[1] + dy))
        target = target[dy:crop_size[1] + dy, dx:crop_size[0] + dx]

        if random.random() > 0.8:
            target = np.fliplr(target)
            img = img.transpose(Image.FLIP_LEFT_RIGHT)

    target1 = cv2.resize(target, (int(target.shape[1] / 8), int(target.shape[0] / 8)),
                        interpolation=cv2.INTER_CUBIC) * 64
    target2 = cv2.resize(target, (int(target.shape[1] / 16), int(target.shape[0] / 16)),
                        interpolation=cv2.INTER_CUBIC) * 64 #*2
    target3 = cv2.resize(target, (int(target.shape[1] / 32), int(target.shape[0] / 32)),
                        interpolation=cv2.INTER_CUBIC) * 64 #*4

    return img, (target1, target2, target3)

class ListDataset(Dataset):
    def __init__(self, root, shape=None, shuffle=True, transform=None, train=False, seen=0, batch_size=1,
                 num_workers=4, dataset_name="shanghaitech"):
        """
        if you have different image size, then batch_size must be 1
        :param root:
        :param shape:
        :param shuffle:
        :param transform:
        :param train:
        :param seen:
        :param batch_size:
        :param num_workers:
        """
        if train:
            root = root * 4
        if shuffle:
            random.shuffle(root)

        self.nSamples = len(root)
        self.lines = root
        self.transform = transform
        self.train = train
        self.shape = shape
        self.seen = seen
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.dataset_name = dataset_name
        # load data fn
        if dataset_name is "shanghaitech":
            self.load_data_fn = load_data
        elif dataset_name is "ucf_cc_50":
            self.load_data_fn = load_data_ucf_cc50
        elif dataset_name is "ucf_cc_50_pacnn":
            self.load_data_fn = load_data_ucf_cc50_pancnn

    def __len__(self):
        return self.nSamples

    def __getitem__(self, index):
        assert index <= len(self), 'index range error'
        img_path = self.lines[index]
        img, target = self.load_data_fn(img_path, self.train)
        if self.transform is not None:
            img = self.transform(img)
        return img, target


def get_dataloader(train_list, val_list, test_list, dataset_name="shanghaitech"):
    train_loader = torch.utils.data.DataLoader(
        ListDataset(train_list,
                            shuffle=True,
                            transform=transforms.Compose([
                                transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                                            std=[0.229, 0.224, 0.225]),
                            ]),
                            train=True,
                            batch_size=1,
                            num_workers=4, dataset_name=dataset_name),
        batch_size=1, num_workers=4)

    val_loader = torch.utils.data.DataLoader(
        ListDataset(val_list,
                            shuffle=False,
                            transform=transforms.Compose([
                                transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                                            std=[0.229, 0.224, 0.225]),
                            ]), train=False, dataset_name=dataset_name),
        batch_size=1)
    if test_list is not None:
        test_loader = torch.utils.data.DataLoader(
            ListDataset(test_list,
                        shuffle=False,
                        transform=transforms.Compose([
                            transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                                        std=[0.229, 0.224, 0.225]),
                        ]), train=False, dataset_name=dataset_name),
            batch_size=1)
    else:
        test_loader = None

    return train_loader, val_loader, test_loader
