from re import L
import torch
from torch.utils.data import Dataset
import json
import os
from PIL import Image
from utils.Transform import ImageTransforms

 
class SRDataset(Dataset):
    """
    数据集加载器
    """
 
    def __init__(self, H_images, L_images = None, split = 'train', crop_size = 96, scaler = 4):
        """
        :参数 data_folder: # Json数据文件所在文件夹路径
        :参数 split: 'train' 或者 'test'
        :参数 crop_size: 高分辨率图像裁剪尺寸  （实际训练时不会用原图进行放大，而是截取原图的一个子块进行放大）
        """
 
        self.split = split.lower()
        self.crop_size = int(crop_size)
        self.scaler = scaler
        assert self.split in {'train', 'test'}
 
        # 读取图像路径
        self.H_imagefolder = H_images + '/'
        self.L_images = None
        self.images = os.listdir(H_images)
        if L_images:
            self.L_imagefolder = L_images + '/'
            self.L_images = os.listdir(L_images)

        # 数据处理方式
        self.transform = ImageTransforms(scaler = scaler)
 
    def __getitem__(self, i):
        """
        为了使用PyTorch的DataLoader, 必须提供该方法.
        :参数 i: 图像检索号
        :返回: 返回第i个低分辨率和高分辨率的图像对
        """
        # 读取图像
        H_img = Image.open(self.H_imagefolder + self.images[i], mode='r').convert('RGB')
        if self.L_imagefolder:
            L_img = Image.open(self.L_imagefolder + self.L_images[i], mode='r').convert('RGB')
            # L_img = L_img.resize(H_img.size)
        else:
            L_img = None

        if self.split == 'train':
            return self.transform(hr_img = H_img, lr_img = L_img, crop_size=self.crop_size)
        else:
            return self.transform(hr_img = H_img, lr_img = L_img)

        

    def __len__(self):
        """
        为了使用PyTorch的DataLoader, 必须提供该方法.
        :返回: 加载的图像总数
        """
        return len(self.images)