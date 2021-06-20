# -*- coding: utf-8 -*-
"""
Add shloka numbers to ramayana

Created on Sun Jun 20 12:00:18 2021

@author: Avinash Varna
"""

import time
import json
import re
import glob
from more_itertools import pairwise
from indic_transliteration.sanscript import transliterate, ITRANS, DEVANAGARI
from tqdm import tqdm


def add_shloka_numbers_word_alignment(json_file_path):
    with open(json_file_path, encoding='utf8') as f:
        alignment = json.load(f)

    number = 1
    pattern = re.compile(r"p([\d]*)s([\d]*)w([\d]*)")
    for i, j in pairwise(alignment['fragments']):
        m = pattern.match(i['id'])
        p0, s0, _ = tuple(map(int, m.groups()))
        m = pattern.match(j['id'])
        p1, s1, _ = tuple(map(int, m.groups()))
        if s0 != s1:
            # New sentence
            if 'Kanda_1_BK-001' in json_file_path:
                if s0 == 1:
                    # Sarga title
                    i['lines'][0] = i['lines'][0] + ' ॥'
                else:
                    if s0 & 1 == 0:
                        i['lines'][0] = i['lines'][0] + ' ।'
                    else:
                        number_san = transliterate(str(number), ITRANS, DEVANAGARI)
                        i['lines'][0] = i['lines'][0] + ' ॥ ' + number_san + ' ॥'
                        number += 1
            else:
                if s0 & 1 == 1:
                    i['lines'][0] = i['lines'][0] + ' ।'
                else:
                    number_san = transliterate(str(number), ITRANS, DEVANAGARI)
                    i['lines'][0] = i['lines'][0] + ' ॥ ' + number_san + ' ॥'
                    number += 1

    # For the last one
    number_san = transliterate(str(number), ITRANS, DEVANAGARI)
    j['lines'][0] = j['lines'][0] + ' ॥ ' + number_san + ' ॥'

    with open(json_file_path, 'w', encoding='utf8') as f:
        json.dump(alignment, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    start_time = time.time()

    files = glob.glob('word_alignment/*.json')
    # add_shloka_numbers_word_alignment(files[0])
    for file in tqdm(files):
        add_shloka_numbers_word_alignment(file)

    print(f'Finished in {time.time()-start_time:0.4f} seconds.')