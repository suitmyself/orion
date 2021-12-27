#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author      : Chen Wei
@date        : 2021-12-27
@file        : path.py
@description : path utils
@version     : 1.0
"""

import os
import shutil

def get_all_files_with_extension(path_dir, extensions = None):
    """get_all_files_with_extension

    Args:
        path_dir ([str]): path directory
        extensions ([None/tuple], optional): extensions. Defaults to None.

    Returns:
        [list]: file list
    """
    
    file_list = []
    for path, _, files in os.walk(path_dir):
        for file in files:
            file_list.append(os.path.join(path, file))
    
    if extensions is None:
        return file_list
    
    return [file for file in file_list if file.lower().endswith(extensions)]

def get_immediate_subdirectories(path_dir):
    """get_immediate_subdirectories

    Args:
        path_dir ([str]): path directory

    Returns:
        [list]: subdirectories list
        
    https://stackoverflow.com/questions/800197/how-to-get-all-of-the-immediate-subdirectories-in-python
    """
    return [os.path.join(path_dir, sub_dir) for sub_dir in os.listdir(path_dir)
            if os.path.isdir(os.path.join(path_dir, sub_dir))]


def extract_path_without_extension(path):
    """extract_file_path_without_extension

    Args:
        path ([str]): path

    Returns:
        [str]: path without extension, e.g., a/b/c.png --> a/b/c
    """
    return os.path.splitext(path)[0]

def extract_path_basename(path):
    """extract_path_basename

    Args:
        path ([str]): path

    Returns:
        [str]: path basebame, e.g., a/b/c.png --> c.png
    """

    return os.path.basename(path)

def extract_path_dirname(path):
    """extract_path_dirname

    Args:
        path ([str]): path

    Returns:
        [str]: path dirname, e.g., a/b/c.png --> a/b/
    """
    return  os.path.dirname(path)

def split_path_components(path):
    """split_path_components

    Args:
        path ([str]): path

    Returns:
        [list]: path components list, e.g., a/b/c.png --> ['a', 'b', 'c.png']
    """
    
    return os.path.normpath(path).split(os.sep)

def check_path_exists(path):
    """
        check_path_exists
    Args:
        path ([str]): path

    Returns:
        [bool]: True if exists, false otherwise
    """
    return os.path.exists(path)

def make_dirs(path_dir, exist_ok=True):
    """make_dirs

    Args:
        path_dir ([str]): path
        exist_ok (bool, optional): whether legal if path exists. Defaults to True.
    """
    
    os.makedirs(path_dir, exist_ok=exist_ok)
    
def rename_path(src_path, dst_path):
    """rename path

    Args:
        src_path ([str]): source path
        dst_path ([str]): destination path
    """
    os.rename(src_path, dst_path)
    
def copy_file(src_path, dst_path, create_dir=True):
    """copy file

    Args:
        src_path ([str]): source path
        dst_path ([str]): destination path
        create_dir (bool, optional): whether create dirs if not exists. Defaults to True.
    """
    
    if create_dir:
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    shutil.copyfile(src_path, dst_path)

def remove_path(path):
    """remove path

    Args:
        path ([str]): path
    """
    try:
        shutil.rmtree(path)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

if __name__ == '__main__':
    
    print(get_all_files_with_extension(".", (".py")))
    print(get_immediate_subdirectories("."))
    print(extract_path_without_extension("a/b/c.png"))
    print(extract_path_basename("a/b/c.png"))
    print(split_path_components("a/b/c.png"))
    print(check_path_exists("."))
