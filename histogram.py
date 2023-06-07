#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author      : Gao Jie
@date        : 2023-05-31
@file        : histogram.py
@description : histogram related algorithm
@version     : 1.0
"""

import numpy as np
import cv2


def he(src: np.ndarray, use_yuv: bool=True) -> np.ndarray:
    """apply Histogram Equalization to image
    
    he(src[, use_yuv]) -> dst

    Args:
        src (np.ndarray): origin BGR image or gray image
        use_yuv (bool): use yuv or use hsv when input BGR image, default to use yuv

    Returns:
        np.ndarray: result BGR image or gray image with Histogram Equalization
    """
    gray = src.copy()

    if len(src.shape) > 2:
        if use_yuv:
            yuv = cv2.cvtColor(src, cv2.COLOR_BGR2YCrCb)
            gray, u, v = cv2.split(yuv)
        else:
            hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
            h, s, gray = cv2.split(hsv)

    dst = cv2.equalizeHist(gray)

    if len(src.shape) > 2:
        if use_yuv:
            yuv = cv2.merge([dst, u, v])
            dst = cv2.cvtColor(yuv, cv2.COLOR_YCrCb2BGR)
        else:
            hsv = cv2.merge([h, s, dst])
            dst = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    return dst


def clahe(src: np.ndarray, limit: float=0.8, grid: tuple=(33, 33), use_yuv: bool=True) -> np.ndarray:
    """apply Contrast Limited Adaptive Histogram Equalization to image
    
    clahe(src[, limit, grid, use_yuv]) -> dst

    Args:
        src (np.ndarray): origin BGR image or gray image
        limit (float): contrast limiting threshold
        grid (tuple): grid size for histogram equalization
        use_yuv (bool): use yuv or use hsv when input BGR image, default to use yuv

    Returns:
        np.ndarray: result BGR image or gray image with histogram equalization
    """
    gray = src.copy()

    if len(src.shape) > 2:
        if use_yuv:
            yuv = cv2.cvtColor(src, cv2.COLOR_BGR2YCrCb)
            gray, u, v = cv2.split(yuv)
        else:
            hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
            h, s, gray = cv2.split(hsv)

    clahe = cv2.createCLAHE(clipLimit=limit, tileGridSize=grid)
    dst = clahe.apply(gray)

    if len(src.shape) > 2:
        if use_yuv:
            yuv = cv2.merge([gray, u, v])
            dst = cv2.cvtColor(yuv, cv2.COLOR_YCrCb2BGR)
        else:
            hsv = cv2.merge([h, s, gray])
            dst = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    return dst


def calculate_mean_and_variance(src: np.ndarray) -> tuple:
    """Calculate Mean and Variance of gray image.

    Args:
        src (np.ndarray): gray image with [H, W]

    Returns:
        tuple: mean and variance of source gray image
    """
    # NOTE(Gao Jie): cv2.calcHist is faster than np.histogram
    # hist, bins = np.histogram(src.ravel(), bins=256, range=[0, 256])
    hist = cv2.calcHist([src], [0], None, [256], [0, 256]).ravel()
    bins = list(range(257))

    mean = np.sum(hist * bins[:-1]) / np.sum(hist)
    variance = np.sum(hist * (bins[:-1] - mean) ** 2) / np.sum(hist)

    return mean, variance
