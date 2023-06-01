#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author      : Gao Jie
@date        : 2023-06-01
@file        : plt_show.py
@description : matplot.pyplot utils
@version     : 1.0
"""

import cv2
from matplotlib import pyplot as plt

import numpy as np


def show_bgr_imgs(img_list: list):
    """show cv2.Mat BGR image using matplotlib.pyplot
    
    Args:
        img_list (list[cv2.Mat]): BGR image list that concated to show
    """
    imgs = np.hstack(img_list)
    plt.imshow(cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()


def show_gray_img(img: np.ndarray):
    """show cv2.Mat gray image using matplotlib.pyplot
    
    Args:
        img (np.ndarray): gray image
    """
    gray = img.copy()
    gray = np.uint8(img) if img.max() > 1 else np.uint8(img * 255)

    plt.imshow(gray, cmap='gray')
    plt.axis('off')
    plt.show()


def show_gray_imgs(img_list: list):
    """show cv2.Mat gray image using matplotlib.pyplot
    
    Args:
        img_list (list[np.ndarray]): gray image list that concated to show
    """
    res_list = []

    for img in img_list:
        res_img = np.uint8(img) if img.max() > 1 else np.uint8(img * 255)
        res_list.append(res_img)

    res = np.concatenate(tuple(res_list), axis=1)

    plt.imshow(res, cmap='gray')
    plt.axis('off')
    plt.show()