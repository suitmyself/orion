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

def convert_yuv_420_to_444(yuv_420_image):
    """convert yuv 420 to 444

    Args:
        yuv_image (np.array): yuv 420 image of size (height * 3 / 2) * width

    Returns:
        [type]: yuv 444 image of size height * width * 3
    """

    image_height = int(yuv_420_image.shape[0] * 2 / 3)
    image_width  = yuv_420_image.shape[1]

    yuv_444_image = np.zeros((image_height, image_width, 3), dtype = yuv_420_image.dtype)

    #---------

    yuv_444_image[:, :, 0] = yuv_420_image[0:image_height]

    #---------

    u_end_height = v_start_height = int(image_height * 5 / 4)

    uv_height = int(image_height / 2)
    uv_width  = int(image_width / 2)

    u_420_image = yuv_420_image[image_height : u_end_height].reshape(uv_height, uv_width)
    yuv_444_image[:, :, 1] = np.repeat(np.repeat(u_420_image, repeats=2, axis=0), repeats=2, axis=1)

    v_420_image = yuv_420_image[v_start_height: ].reshape(uv_height, uv_width)
    yuv_444_image[:, :, 2] = np.repeat(np.repeat(v_420_image, repeats=2, axis=0), repeats=2, axis=1)

    return yuv_444_image


def convert_yuv_444_to_420(yuv_444_image):
    """convert yuv 444 to 420

    Args:
        yuv_image (np.array): yuv 444 image of height * width * 3

    Returns:
        [type]: yuv 420 image of size size (height * 3 / 2) * width
    """

    image_height = yuv_444_image.shape[0]
    image_width  = yuv_444_image.shape[1]

    yuv_height = int(image_height * 3 / 2)

    yuv_420_image = np.zeros((yuv_height, image_width), dtype = yuv_444_image.dtype)

    #---------

    yuv_420_image[0:image_height] = yuv_444_image[:,:,0]

    #---------

    u_end_height = v_start_height = int(image_height * 5 / 4)

    uv_plane_height = int(image_height / 4)

    yuv_444_image = yuv_444_image.astype(np.float32) # to avoid overflow

    u_420_image = (yuv_444_image[0::2, 0::2, 1] + yuv_444_image[0::2, 1::2, 1] + yuv_444_image[1::2, 0::2, 1] + yuv_444_image[1::2, 1::2, 1]) / 4.0 + 0.5
    yuv_420_image[image_height: u_end_height] = u_420_image.reshape((uv_plane_height, -1))

    v_420_image = (yuv_444_image[0::2, 0::2, 2] + yuv_444_image[0::2, 1::2, 2] + yuv_444_image[1::2, 0::2, 2] + yuv_444_image[1::2, 1::2, 2]) / 4.0 + 0.5
    yuv_420_image[v_start_height: ] = v_420_image.reshape((uv_plane_height, -1))

    # print(yuv_420_image.dtype)

    return yuv_420_image


def convert_bgr_to_709_limited_yuv(bgr_image):
    """convert_bgr_to_709_limited_yuv

    Args:
        bgr_image (np.array): bgr image

    Returns:
        [type]: yuv 444 BT709 limited image
    """
    yuv_image = np.zeros_like(bgr_image, dtype='float')

    bgr_image = bgr_image.astype(np.float32)

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

def convert_709_limited_yuv_to_bgr(yuv_image):
    """convert_709_limited_yuv_to_bgr

    Args:
        bgr_image (np.array): yuv 444 BT709 limited image

    Returns:
        [type]: bgr image
    """

    bgr_image = np.zeros_like(yuv_image, dtype='float')

    yuv_image = yuv_image.astype(np.float32)

    yuv_image_by_offset = np.zeros_like(yuv_image)

    yuv_image_by_offset[:,:,0] = yuv_image[:,:,0] / 255.0 - 16.0 /255.0
    yuv_image_by_offset[:,:,1] = yuv_image[:,:,1] / 255.0 - 0.5
    yuv_image_by_offset[:,:,2] = yuv_image[:,:,2] / 255.0 - 0.5

    #B
    bgr_image[:,:,0] = 1.164 * yuv_image_by_offset[:,:,0] + 2.112 * yuv_image_by_offset[:,:,1] + 0.000 * yuv_image_by_offset[:,:,2]

    #G
    bgr_image[:,:,1] = 1.164 * yuv_image_by_offset[:,:,0] - 0.213 * yuv_image_by_offset[:,:,1] - 0.533 * yuv_image_by_offset[:,:,2]

    #R
    bgr_image[:,:,2] = 1.164 * yuv_image_by_offset[:,:,0] + 0.000 * yuv_image_by_offset[:,:,1] + 1.793 * yuv_image_by_offset[:,:,2]

    bgr_image *= 255.0

    return np.clip(bgr_image, 0, 255).astype(np.uint8)

def convert_bgr_to_709_full_yuv(bgr_image):
    """convert_bgr_to_709_full_yuv

    Args:
        bgr_image (np.array): bgr image

    Returns:
        [type]: yuv 444 BT709 full image
    """
    yuv_image = np.zeros_like(bgr_image, dtype='float')

    bgr_image = bgr_image.astype(np.float32)

    #Y
    yuv_image[:,:,0] = 0   + 0.213 * bgr_image[:,:,2] + 0.715 * bgr_image[:,:,1] + 0.072 * bgr_image[:,:,0]

    #Cb
    yuv_image[:,:,1] = 128 - 0.115 * bgr_image[:,:,2] - 0.385 * bgr_image[:,:,1] + 0.500 * bgr_image[:,:,0]

    #Cr
    yuv_image[:,:,2] = 128 + 0.500 * bgr_image[:,:,2] - 0.454 * bgr_image[:,:,1] - 0.046 * bgr_image[:,:,0]

    yuv_image[:,:,0] = np.clip(yuv_image[:,:,0], 0, 255)
    yuv_image[:,:,1] = np.clip(yuv_image[:,:,1], 0, 255)
    yuv_image[:,:,2] = np.clip(yuv_image[:,:,2], 0, 255)

    return yuv_image

def convert_709_full_yuv_to_bgr(yuv_image):
    """convert_709_full_yuv_to_bgr

    Args:
        bgr_image (np.array): yuv 444 BT709 full image

    Returns:
        [type]: bgr image
    """

    bgr_image = np.zeros_like(yuv_image, dtype='float')

    yuv_image = yuv_image.astype(np.float32)

    yuv_image_by_offset = np.zeros_like(yuv_image)

    yuv_image_by_offset[:,:,0] = yuv_image[:,:,0] / 255.0
    yuv_image_by_offset[:,:,1] = yuv_image[:,:,1] / 255.0 - 0.5
    yuv_image_by_offset[:,:,2] = yuv_image[:,:,2] / 255.0 - 0.5

    #B
    bgr_image[:,:,0] = 1.000 * yuv_image_by_offset[:,:,0] + 1.856 * yuv_image_by_offset[:,:,1] + 0.000 * yuv_image_by_offset[:,:,2]

    #G
    bgr_image[:,:,1] = 1.000 * yuv_image_by_offset[:,:,0] - 0.187 * yuv_image_by_offset[:,:,1] - 0.468 * yuv_image_by_offset[:,:,2]

    #R
    bgr_image[:,:,2] = 1.000 * yuv_image_by_offset[:,:,0] + 0.000 * yuv_image_by_offset[:,:,1] + 1.575 * yuv_image_by_offset[:,:,2]

    bgr_image *= 255.0

    return np.clip(bgr_image, 0, 255).astype(np.uint8)

def convert_bgr_to_601_limited_yuv(bgr_image):
    """convert_bgr_to_601_limited_yuv

    Args:
        bgr_image (np.array): bgr image

    Returns:
        [type]: yuv 444 BT601 limited image
    """
    yuv_image = np.zeros_like(bgr_image, dtype='float')

    bgr_image = bgr_image.astype(np.float32)

    #Y
    yuv_image[:,:,0] = 16  + 0.257 * bgr_image[:,:,2] + 0.504 * bgr_image[:,:,1] + 0.098 * bgr_image[:,:,0]

    #Cb
    yuv_image[:,:,1] = 128 - 0.148 * bgr_image[:,:,2] - 0.291 * bgr_image[:,:,1] + 0.439 * bgr_image[:,:,0]

    #Cr
    yuv_image[:,:,2] = 128 + 0.439 * bgr_image[:,:,2] - 0.368 * bgr_image[:,:,1] - 0.071 * bgr_image[:,:,0]

    yuv_image[:,:,0] = np.clip(yuv_image[:,:,0], 16, 235)
    yuv_image[:,:,1] = np.clip(yuv_image[:,:,1], 16, 240)
    yuv_image[:,:,2] = np.clip(yuv_image[:,:,2], 16, 240)

    return yuv_image

def convert_601_limited_yuv_to_bgr(yuv_image):
    """convert_601_limited_yuv_to_bgr

    Args:
        bgr_image (np.array): yuv 444 BT601 limited image

    Returns:
        [type]: bgr image
    """

    bgr_image = np.zeros_like(yuv_image, dtype='float')

    yuv_image = yuv_image.astype(np.float32)

    yuv_image_by_offset = np.zeros_like(yuv_image)

    yuv_image_by_offset[:,:,0] = yuv_image[:,:,0] / 255.0 - 16.0 /255.0
    yuv_image_by_offset[:,:,1] = yuv_image[:,:,1] / 255.0 - 0.5
    yuv_image_by_offset[:,:,2] = yuv_image[:,:,2] / 255.0 - 0.5

    #B
    bgr_image[:,:,0] = 1.164 * yuv_image_by_offset[:,:,0] + 2.017 * yuv_image_by_offset[:,:,1] + 0.000 * yuv_image_by_offset[:,:,2]

    #G
    bgr_image[:,:,1] = 1.164 * yuv_image_by_offset[:,:,0] - 0.392 * yuv_image_by_offset[:,:,1] - 0.813 * yuv_image_by_offset[:,:,2]

    #R
    bgr_image[:,:,2] = 1.164 * yuv_image_by_offset[:,:,0] + 0.000 * yuv_image_by_offset[:,:,1] + 1.596 * yuv_image_by_offset[:,:,2]

    bgr_image *= 255.0

    return np.clip(bgr_image, 0, 255).astype(np.uint8)

def convert_bgr_to_601_full_yuv(bgr_image):
    """convert_bgr_to_601_full_yuv

    Args:
        bgr_image (np.array): bgr image

    Returns:
        [type]: yuv 444 BT601 full image
    """
    yuv_image = np.zeros_like(bgr_image, dtype='float')

    bgr_image = bgr_image.astype(np.float32)

    #Y
    yuv_image[:,:,0] = 0   + 0.299 * bgr_image[:,:,2] + 0.587 * bgr_image[:,:,1] + 0.114 * bgr_image[:,:,0]

    #Cb
    yuv_image[:,:,1] = 128 - 0.169 * bgr_image[:,:,2] - 0.331 * bgr_image[:,:,1] + 0.500 * bgr_image[:,:,0]

    #Cr
    yuv_image[:,:,2] = 128 + 0.500 * bgr_image[:,:,2] - 0.419 * bgr_image[:,:,1] - 0.081 * bgr_image[:,:,0]

    return np.clip(yuv_image, 0, 255).astype(np.uint8)

def convert_601_full_yuv_to_bgr(yuv_image):
    """convert_601_full_yuv_to_bgr

    Args:
        bgr_image (np.array): yuv 444 BT601 full image

    Returns:
        [type]: bgr image
    """

    bgr_image = np.zeros_like(yuv_image, dtype='float')

    yuv_image = yuv_image.astype(np.float32)

    yuv_image_by_offset = np.zeros_like(yuv_image)

    yuv_image_by_offset[:,:,0] = yuv_image[:,:,0] / 255.0
    yuv_image_by_offset[:,:,1] = yuv_image[:,:,1] / 255.0 - 0.5
    yuv_image_by_offset[:,:,2] = yuv_image[:,:,2] / 255.0 - 0.5

    #B
    bgr_image[:,:,0] = 1.000 * yuv_image_by_offset[:,:,0] + 1.772 * yuv_image_by_offset[:,:,1] + 0.000 * yuv_image_by_offset[:,:,2]

    #G
    bgr_image[:,:,1] = 1.000 * yuv_image_by_offset[:,:,0] - 0.344 * yuv_image_by_offset[:,:,1] - 0.714 * yuv_image_by_offset[:,:,2]

    #R
    bgr_image[:,:,2] = 1.000 * yuv_image_by_offset[:,:,0] + 0.000 * yuv_image_by_offset[:,:,1] + 1.402 * yuv_image_by_offset[:,:,2]

    bgr_image *= 255.0

    return np.clip(bgr_image, 0, 255).astype(np.uint8)

#TODO(Chen Wei): add other versions