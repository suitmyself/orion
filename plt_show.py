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
import numpy as np

from matplotlib import pyplot as plt

def show_bgr_img(img: np.ndarray):
    """show np.ndarray BGR image using matplotlib.pyplot
    
    Args:
        img (np.ndarray): BGR image
    """
    img = np.uint8(img)

    plt.figure(figsize=(10, 12))
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()


def show_bgr_imgs(img_list: list):
    """show np.ndarray BGR image using matplotlib.pyplot
    
    Args:
        img_list (list[cv2.Mat]): BGR image list that concated to show
    """
    img_list = [np.uint8(img) for img in img_list]
    imgs = np.hstack(img_list)

    plt.figure(figsize=(10, 12))
    plt.imshow(cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()


def show_gray_img(img: np.ndarray):
    """show np.ndarray gray image using matplotlib.pyplot
    
    Args:
        img (np.ndarray): gray image
    """
    gray = np.uint8(img) if img.max() > 1 else np.uint8(img * 255)

    plt.figure(figsize=(10, 12))
    plt.imshow(gray, cmap='gray')
    plt.axis('off')
    plt.show()


def show_gray_imgs(img_list: list):
    """show np.ndarray gray image using matplotlib.pyplot
    
    Args:
        img_list (list[np.ndarray]): gray image list that concated to show
    """
    res_list = []

    for img in img_list:
        res_img = np.uint8(img) if img.max() > 1 else np.uint8(img * 255)
        res_list.append(res_img)

    res = np.concatenate(tuple(res_list), axis=1)

    plt.figure(figsize=(10, 12))
    plt.imshow(res, cmap='gray')
    plt.axis('off')
    plt.show()


def show_histogram(img: np.ndarray):
    """show histogram of np.ndarray gray image using matplotlib.pyplot
    
    Args:
        img (np.ndarray): [H, W] gray image or [B, G, R] image
    """
    gray = img.copy()
    if len(img.shape) > 2:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plt.figure()
    plt.hist(gray.ravel(), bins=256, range=[0, 256])
    plt.show()


def show_img_with_hist(img: np.ndarray):
    """show histogram of np.ndarray gray image using matplotlib.pyplot
    
    Args:
        img (np.ndarray): [H, W] gray image or [B, G, R] image
    """
    gray = img.copy()
    if len(img.shape) > 2:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    fig, axs = plt.subplots(2, 1, figsize=(6, 8))
    axs[0].imshow(gray, cmap='gray')
    axs[0].axis('off')

    axs[1].hist(gray.ravel(), bins=256, range=[0, 256])

    plt.tight_layout()
    plt.show()
