#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 23:09:39 2021

@author: Hrishikesh Terdalkar
"""

###############################################################################

import argparse

from flask_frozen import Freezer

from server import webapp

###############################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Build static website")
    parser.add_argument("--base-url", default="http://localhost/",
                        help="Full URL of the desired application location")
    parser.add_argument("--relative", action='store_true',
                        help="Build relative URLs")

    args = vars(parser.parse_args())

    # Configure
    webapp.config['FREEZER_BASE_URL'] = args['base_url']
    webapp.config['FREEZER_RELATIVE_URLS'] = args['relative']

    freezer = Freezer(webapp)
    freezer.freeze()
