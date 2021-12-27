#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author      : Chen Wei
@date        : 2021-12-27
@file        : yuv.py
@description : yuv utils
@version     : 1.0
"""

import numpy as np

def convert_bgr_to_709_limited_yuv(bgr_image):
    """convert_bgr_to_709_limited_yuv

    Args:
        bgr_image (np.array): bgr image

    Returns:
        [type]: yuv 444 BT709 limited image
    """
    yuv_image = np.zeros_like(bgr_image, dtype='float')

    bgr_image = bgr_image.astype(np.float)

    #Y
    yuv_image[:,:,0] = 16  + 0.183 * bgr_image[:,:,2] + 0.614 * bgr_image[:,:,1] + 0.062 * bgr_image[:,:,0]

    #Cb
    yuv_image[:,:,1] = 128 - 0.101 * bgr_image[:,:,2] - 0.339 * bgr_image[:,:,1] + 0.439 * bgr_image[:,:,0]

    #Cr
    yuv_image[:,:,2] = 128 + 0.439 * bgr_image[:,:,2] - 0.399 * bgr_image[:,:,1] - 0.040 * bgr_image[:,:,0]

    yuv_image[:,:,0] = np.clip(yuv_image[:,:,0], 16, 235)
    yuv_image[:,:,1] = np.clip(yuv_image[:,:,1], 16, 240)
    yuv_image[:,:,2] = np.clip(yuv_image[:,:,2], 16, 240)

    return yuv_image


#TODO(Chen Wei): add other versions