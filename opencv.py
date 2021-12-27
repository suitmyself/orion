#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author      : Chen Wei
@date        : 2021-12-27
@file        : opencv.py
@description : opencv utils
@version     : 1.0
"""

import cv2
import numpy as np

def rectify_bgr_img_read_by_opencv_for_bt709_video(bgr_image):
    """rectify_bgr_img_read_by_opencv_for_bt709_video

    Args:
        bgr_image ([np.array]): bgr image

    Returns:
        [type]: corrected bgr image
        
    Note:
    When OpenCV read BT709 limited range video, it would use color matrix (yuv --> rgb) of BT601 limited range,
    so we need rectify this problem.
    It is accomplished by first convert to yuv using color matrix of BT601 limited range, and re-convert to rgb using color matrix of BT709 color matrix.
    These two matrix can be merged.  
    
    mat_709 = np.array([[1.164,  0.000,  1.793],
                        [1.164, -0.213, -0.533],
                        [1.164, 2.112, 0.000]])
    
    mat_601 = np.array([[ 0.257,  0.504,  0.098],
                        [-0.148, -0.291,  0.439],
                        [0.439,  -0.368, -0.071]])
    
    print(np.matmul(mat_709, mat_601))
    
    convert_mat = np.array([[ 1.086275, -0.073168, -0.013231],
                            [ 0.096685,  0.844783,  0.058408],
                            [-0.013428, -0.027936,  1.04124 ]])
    
    print(convert_mat)

    """

    res_bgr_image = np.zeros_like(bgr_image, dtype='float')
    
    #R
    res_bgr_image[:,:,2] =  1.086275 * bgr_image[:,:,2] - 0.073168 * bgr_image[:,:,1] - 0.013231 * bgr_image[:,:,0]

    #G
    res_bgr_image[:,:,1] =  0.096685 * bgr_image[:,:,2] + 0.844783 * bgr_image[:,:,1] + 0.058408 * bgr_image[:,:,0]

    #G
    res_bgr_image[:,:,0] = -0.013428 * bgr_image[:,:,2] - 0.027936 * bgr_image[:,:,1] + 1.04124 * bgr_image[:,:,0]
    
    return np.clip(res_bgr_image, 0, 255).astype(np.uint8)
