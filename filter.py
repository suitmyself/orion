#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author      : Gao Jie
@date        : 2023-05-31
@file        : filter.py
@description : filter related algorithm
@version     : 1.0
"""

import numpy as np
import cv2

def homomorphic_filter(src: np.ndarray, cutoff_freq: int=200, gamma_low: float=0.5, gamma_high: float=2.0, sharp_factor: float=0.1, use_yuv: bool=False) -> np.ndarray:
    """apply Histogram Equalization to image
    
    homomorphic_filter(src[, cutoff_freq, gamma_low, gamma_high, sharp_factor, use_yuv])

    Args:
        src (np.ndarray): origin BGR image or gray image
        cutoff_freq (int): cut-off frequency, controlling the truncation of the high frequency part
        gamma_low (float): gamma value of low frequency part, used to enhance or attenuate the low frequency part
        gamma_high (float): gamma value of high frequency part, used to enhance or attenuate the high frequency part
        sharp_factor (float): sharpening factor, controlling the enhancement degree of the high frequency part
        use_yuv (bool): use yuv or use hsv when input BGR image, default to use hsv

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

    gray = np.float64(gray)
    log_gray = np.log(gray + 1)
    rows, cols = gray.shape

    # fft
    gray_fft = np.fft.fft2(log_gray)
    gray_fftshift = np.fft.fftshift(gray_fft)

    result_fftshift = np.zeros_like(gray_fftshift)
    M, N = np.meshgrid(np.arange(-cols // 2, cols // 2), np.arange(-rows//2, rows//2))

    # filter
    D = np.sqrt(M ** 2 + N ** 2)
    Z = (gamma_high - gamma_low) * (1 - np.exp(-sharp_factor * (D ** 2 / cutoff_freq ** 2))) + gamma_low
    result_fftshift = Z * gray_fftshift

    # inverse fft
    result_ifftshift = np.fft.ifftshift(result_fftshift)
    result_ifft = np.fft.ifft2(result_ifftshift)

    dst_gray = np.abs(np.exp(result_ifft) -1)
    dmax, dmin = np.max(dst_gray), np.min(dst_gray)
    drange = dmax - dmin
    dst_gray_max = min(255, max(dmax, np.max(gray)))
    dst_gray_min = min(dmin, np.min(gray))

    # stretch to the same dynamic range as original
    for i in range(rows):
        for j in range(cols):
            dst_gray[i, j] = (dst_gray_max - dst_gray_min) * (dst_gray[i, j] - dmin) / drange + dst_gray_min

    dst = np.uint8(np.clip(dst_gray, 0, 255))

    if len(src.shape) > 2:
        if use_yuv:
            yuv = cv2.merge([dst, u, v])
            dst = cv2.cvtColor(yuv, cv2.COLOR_YCrCb2BGR)
        else:
            hsv = cv2.merge([h, s, dst])
            dst = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    return dst