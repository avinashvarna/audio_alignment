#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 23:09:39 2021

@author: Hrishikesh Terdalkar
"""

###############################################################################

from flask_frozen import Freezer
from server import webapp

freezer = Freezer(webapp)

###############################################################################

if __name__ == '__main__':
    freezer.freeze()
