#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author      : Chen Wei
@date        : 2021-12-27
@file        : video.py
@description : video utils
@version     : 1.0
"""

#Note(Chen Wei): to improve futher

import cv2
import numpy as np

def read_and_write_video(src_path, dst_path):
    """read_and_write_video

    Args:
        src_path ([str]): soruce path
        dst_path ([str]): destination path
        
    Note: just code snippet for further modification
        
    """
    
    vidcap = cv2.VideoCapture(src_path)

    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    print("fps: ", fps)

    height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))

    print("width: ", width)
    print("height: ", height)
    
    frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("frame count: ", frame_count)
    
    #NOTE(Chen Wei): opencv not lossless !
    
    # dst_file = cv2.VideoWriter(dst_path, cv2.VideoWriter_fourcc(*'X264'), fps, (width, height))
    dst_file = cv2.VideoWriter(dst_path, cv2.VideoWriter_fourcc(*'MJPG'), fps, (width, height))
    
    # https://www.fourcc.org/codecs.php
    
    while True:
        success, bgr_img = vidcap.read()
        if not success:
            break
        
        # bgr_img = rectify_bgr_img_read_by_OpenCV_for_BT709_video(bgr_img)
        
        dst_file.write(bgr_img)
        
    dst_file.release()
