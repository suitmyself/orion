#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author      : Chen Wei
@date        : 2021-12-27
@file        : os.py
@description : os utils
@version     : 1.0
"""

import os

def run_command(cmd):
    """run command

    Args:
        cmd ([str]): command
    """
    os.system(cmd)
    