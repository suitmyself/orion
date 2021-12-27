#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author      : Chen Wei
@date        : 2021-12-27
@file        : yuv_reader.py
@description : yuv reader util
@version     : 1.0
"""

import os
import re
import cv2
import numpy as np

#Note(Chen Wei): to improve futher

class YuvReader:
    
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

        self.filesize = os.path.getsize(filename)
        self.framenum = int(self.filesize / self.framesize)

        self.file = open(filename, 'rb')

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_file_size(self):
        return self.filesize

    def get_frame_num(self):
        return self.framenum

    def get_frame(self, idx):
        if idx >= self.framenum:
            raise IndexError("index out of range")

        self.file.seek(idx * self.framesize)

        buffer = self.file.read(self.framesize)

        yuv = np.frombuffer(buffer, np.uint8).reshape(int(self.height * 3 / 2), self.width)

        return yuv

    def get_frame_by_bgr(self, idx):

        yuv = self.getFrame(idx)

        #NOTE(Chen Wei): BT601 limited range ?
        bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)

        return bgr