#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author      : Chen Wei
@date        : 2024-1-10
@file        : yuv_writer.py
@description : yuv writer util
@version     : 1.0
"""

import os
import re
import cv2
import numpy as np

#Note(Chen Wei): to improve futher

class YuvWriter:
    
    def __init__(self):
        """init empty reader"""
        pass

    def __init__(self, filename):
        """init reader by filename """
        self.open(filename)

    def open(self, filename):
        self.filename = filename

        size = re.search(r'_(\d+)x(\d+)\.', filename)
        self.width  = int(size.group(1))
        self.height = int(size.group(2))

        self.framesize = int(self.width * self.height * 3 / 2)

        self.file = open(filename, 'wb')

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height
    
    def get_frame_size(self):
        return self.framesize
    
    def write_frame(self, yuv):

        buffer = yuv.tobytes()

        self.file.write(buffer)

    def write_frame_by_bgr(self, bgr):

        #NOTE(Chen Wei): BT601 limited range ?
        yuv = cv2.cvtColor(bgr, cv2.COLOR_BGR2YUV_I420)

        self.write_frame(yuv)