#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 01 14:43:18 2021

@author: Hrishikesh Terdalkar
"""

import os
import glob

###############################################################################


class Configuration(dict):
    def __init__(self, *args, **kwargs):
        super(Configuration, self).__init__(*args, **kwargs)
        self.__dict__ = self


###############################################################################

CONFIG_PREFIX = 'AA_'
CONFIG = Configuration()

###############################################################################

CONFIG['SECRET_KEY'] = os.environ.get(
    f'{CONFIG_PREFIX}SECRET_KEY', 'audio-alignment'
)

CONFIG['SERVER_DIR'] = os.environ.get(
    f'{CONFIG_PREFIX}SERVER_DIR', os.path.dirname(os.path.realpath(__file__))
)

CONFIG['CORPUS_DIR'] = os.environ.get(
    f'{CONFIG_PREFIX}CORPUS_DIR', os.path.dirname(CONFIG['SERVER_DIR'] + "/../data/")
)
CONFIG['DATA_FILENAME'] = 'data.json'
CONFIG['CORPUS_DATA_FILES'] = os.environ.get(
    f'{CONFIG_PREFIX}CORPUS_DATA_FILES',
    ','.join(glob.glob(
        os.path.join(CONFIG['CORPUS_DIR'], '*', CONFIG['DATA_FILENAME'])
    ))
).split(',')

###############################################################################
