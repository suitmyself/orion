#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author      : Chen Wei
@date        : 2023-03-24
@file        : lut.py
@description : lut utils
@version     : 1.0
"""

from PIL import Image, ImageFilter

import numpy as np

def convert_512x512_lut_to_pillow_3d_lut_filter(lut_image_file):
    """
    convert_512x512_lut_to_pillow_3d_lut_filter
    
    reference:https://github.com/homm/pillow-lut-tools
    file:https://github.com/homm/pillow-lut-tools/blob/master/pillow_lut/loaders.py
    
    """
    
    lut_image = Image.open(lut_image_file).convert('RGB')
    
    if lut_image.size[0] != 512 or lut_image.size[1] != 512:
        raise ValueError(f"Error: lut image size not equal 512x512: {lut_image.size}")
    
    table = np.zeros((512*512, 3), dtype=np.uint8)
    
    for r in range(0, 64):
        for g in range(0, 64):
            for b in range(0, 64):
                
                block_y = b // 8
                block_x = b % 8
                
                cy = 64 * block_y + g
                cx = 64 * block_x + r
                
                idx = r + 64 * g + 64 * 64 * b
                
                table[idx] = lut_image.getpixel((cx, cy))
                
    table = table.astype(np.float32) / 255.0

    return ImageFilter.Color3DLUT((64, 64, 64), table, target_mode=None, _copy_table=False)


def convert_512x512_lut_to_hald8_image(lut_image_file, dst_hdld8_file = None):
    """
    convert_512x512_lut_to_hald8_image
    """

    lut_image = Image.open(lut_image_file).convert('RGB')
    
    if lut_image.size[0] != 512 or lut_image.size[1] != 512:
        raise ValueError(f"Error: lut image size not equal 512x512: {lut_image.size}")
    
    table = np.zeros((512*512, 3), dtype=np.uint8)
    
    for r in range(0, 64):
        for g in range(0, 64):
            for b in range(0, 64):
                
                block_y = b // 8
                block_x = b % 8
                
                cy = 64 * block_y + g
                cx = 64 * block_x + r
                
                idx = r + 64 * g + 64 * 64 * b
                
                table[idx] = lut_image.getpixel((cx, cy))
                
    table = table.reshape((512, 512, -1))
    
    hald8_image =  Image.fromarray(table)
    
    if dst_hdld8_file:
        hald8_image.save(dst_hdld8_file)
        
    return hald8_image


def convert_hald8_image_to_512x512_lut(hald8_image_file, dst_lut_image_file = None):
    """
    convert_hald8_image_to_512x512_lut
    """

    hald8_image = Image.open(hald8_image_file).convert('RGB')
    
    if hald8_image.size[0] != 512 or hald8_image.size[1] != 512:
        raise ValueError(f"Error: lut image size not equal 512x512: {hald8_image.size}")
    
    table = np.zeros((512, 512, 3), dtype=np.uint8)
    
    for r in range(0, 64):
        for g in range(0, 64):
            for b in range(0, 64):
                
                block_y = b // 8
                block_x = b % 8
                
                cy = 64 * block_y + g
                cx = 64 * block_x + r
                
                idx = r + 64 * g + 64 * 64 * b
                hy = idx // 512
                hx = idx % 512
                
                table[cy, cx] = hald8_image.getpixel((hx, hy))
    
    lut_image =  Image.fromarray(table)
    
    if dst_lut_image_file:
        lut_image.save(dst_lut_image_file)
        
    return lut_image


def generate_identity_512x512_lut(dst_lut_image_file = None):
    """
    generate_identity_512x512_lut
    """
    
    table = np.zeros((512, 512, 3), dtype=np.uint8)
    
    for r in range(0, 64):
        for g in range(0, 64):
            for b in range(0, 64):
                
                block_y = b // 8
                block_x = b % 8
                
                cy = 64 * block_y + g
                cx = 64 * block_x + r
                
                table[cy, cx] = (r * 4, g * 4, b * 4)
    
    lut_image =  Image.fromarray(table)
    
    if dst_lut_image_file:
        lut_image.save(dst_lut_image_file)
        
    return lut_image

def generate_identity_hald8_image(dst_hdld8_file = None):
    """
    generate_identity_hald8_image
    """

    table = np.zeros((512*512, 3), dtype=np.uint8)
    
    for r in range(0, 64):
        for g in range(0, 64):
            for b in range(0, 64):
                
                idx = r + 64 * g + 64 * 64 * b
                
                table[idx] = (r * 4, g * 4, b * 4)
                
    table = table.reshape((512, 512, -1))
    
    hald8_image =  Image.fromarray(table)
    
    if dst_hdld8_file:
        hald8_image.save(dst_hdld8_file)
        
    return hald8_image


def apply_3d_lut_for_cv_image(cv_image, cube_lut, factor = 1.0):
    """
    apply_3d_lut_for_cv_image

    Args:
        cv_image (np.array): opencv bgr image
        cube_lut (ImageFilter.Color3DLUT): 3d cube lut filter of pillow 
        factor (float, optional): blend factor. Defaults to 1.0.

    Returns:
        res_image: opencv bgr image
    """
    
    pillow_image = Image.fromarray(cv_image[:,:,::-1]) # bgr --> rgb

    lut_pillow_image = pillow_image.filter(cube_lut)
    
    lut_image = np.asarray(lut_pillow_image)[:,:,::-1] # rgb --> bgr
    
    res_image = cv_image * (1.0 - factor) + lut_image * factor

    return res_image


def apply_3d_lut_for_pillow_image(pillow_image, cube_lut, factor = 1.0):
    """
    apply_3d_lut_for_pillow_image

    Args:
        pillow_image (np.array): pillow rgb image
        cube_lut (ImageFilter.Color3DLUT): 3d cube lut filter of pillow 
        factor (float, optional): blend factor. Defaults to 1.0.

    Returns:
        res_image : pillow rgb image
    """

    lut_pillow_image = pillow_image.filter(cube_lut)
    
    cv_image = np.asarray(pillow_image)
    lut_image = np.asarray(lut_pillow_image)
    
    res_image = cv_image * (1.0 - factor) + lut_image * factor
    
    res_image = Image.fromarray(res_image)

    return res_image