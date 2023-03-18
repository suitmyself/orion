#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author      : Chen Wei
@date        : 2023-03-17
@file        : ffmpeg.py
@description : ffmpeg utils
@version     : 1.0
"""

import os

def concat_two_videos(first_video_path, second_video_path, dst_video_path, horizontal = True):
    """"concat two videos"""

    direction = "hstack" if horizontal else "vstack"

    cmd = f'ffmpeg -y -i {first_video_path} -i {second_video_path} -filter_complex {direction}=inputs=2 {dst_video_path}'
    os.system(cmd)

def concat_three_videos(first_video_path, second_video_path, third_video_path, dst_video_path, horizontal = True):
    """"concat three videos"""
    
    direction = "hstack" if horizontal else "vstack"
    
    cmd = f'ffmpeg -y -i {first_video_path} -i {second_video_path} -i {third_video_path} -filter_complex {direction}=inputs=3 {dst_video_path}'
    os.system(cmd)
    
def concat_four_videos(first_video_path, second_video_path, third_video_path, fourth_video_path, dst_video_path, horizontal = True):
    """"concat four videos"""
    
    direction = "hstack" if horizontal else "vstack"
    
    cmd = f'ffmpeg -y -i {first_video_path} -i {second_video_path} -i {third_video_path} -i {fourth_video_path} \
           -filter_complex {direction}=inputs=4 {dst_video_path}'
    os.system(cmd)
    
def concat_four_videos_2x2(first_video_path, second_video_path, third_video_path, fourth_video_path, dst_video_path):
    """"concat four videos in 2x2 mode"""
    
    cmd = f'ffmpeg -y -i {first_video_path} -i {second_video_path} -i {third_video_path} -i {fourth_video_path} \
            -filter_complex "[0:v][1:v][2:v][3:v]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0[v]" -map "[v]" {dst_video_path}'
    os.system(cmd)