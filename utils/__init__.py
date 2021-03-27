# -*- coding: utf-8 -*-
"""
Misc utilities

@author: Avinash Varna
"""

import requests
from urllib.parse import urlparse
from pathlib import Path


def download_file(url:str, filepath:str = None):
    ''' Download file from url to specified filepath.
        If filepath is None, then the file is saved in the current directory
        and the path is returned.
    '''
    if filepath is None:
        path = urlparse(url).path
        filepath = Path(path).name
    r = requests.get(url, stream=True)
    with open(filepath, "wb") as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
    return filepath
