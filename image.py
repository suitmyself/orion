#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author      : Chen Wei
@date        : 2023-03-17
@file        : image.py
@description : image utils
@version     : 1.0
"""

import cv2
import numpy as np

from . import path

def concat_two_image(first_image_file, second_image_file, dst_image_file, axis = 1):
    """
    concat two image

    Args:
        first_image_file (string): first image file
        second_image_file (string): second image file
        dst_image_file (string): dst image file
        axis (int, optional): axis, Defaults to 1.
    """
    
    first_image = cv2.imread(first_image_file)
    second_image = cv2.imread(second_image_file)
    
    dst_image = np.concatenate((first_image, second_image), axis = axis)
    
    cv2.imwrite(dst_image_file, dst_image)

def concat_two_image_folder(first_image_dir, second_image_dir, dst_image_dir, axis = 1):
    """
    concat two image folder, image concatenated for same file name

    Args:
        first_image_folder (string): first image folder
        second_image_folder (string): second image folder
        dst_image_folder (string): dst image folder
        axis (int, optional): axis, Defaults to 1.
    """

    path.make_dirs(dst_image_dir)
    
    first_image_list = path.get_all_files_with_extension(first_image_dir)

    for first_image_file in first_image_list:
        
        image_basename = path.extract_path_basename(first_image_file)
        second_image_file = second_image_dir + "/" + image_basename
        
        if path.check_path_exists(second_image_file):
            dst_image_file = dst_image_dir + "/" + image_basename
            concat_two_image(first_image_file, second_image_file, dst_image_file, axis = axis)

def get_image_dsize(src_image):
    """
    get image dsize

    Args:
        src_image (np.array): source image
        
    Returns: dsize tuple: (width, height), usually used by cv2.resize
    """
    
    if src_image.ndim == 2:
        return src_image.shape[::-1]
    elif src_image.ndim == 3:
        return src_image.shape[-2::-1]
    else:
        raise ValueError(f"error: unsupported ndim = {src_image.ndim}")
    