# -*- coding: utf-8 -*-
"""
Align text with audio

"""

import os
import sys
import csv
import time

from tqdm import tqdm

base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(base_dir)

from utils.alignment import align, clean
#except ImportError:
#    pass


def get_text_audio_map():
    map_file = 'text_audio_map.csv'

    text_audio_map = []
    with open(map_file, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            text_audio_map.append(row)

    return text_audio_map


def align_text(text_audio_map, align_out_dir, word_align=False):
    os.makedirs(align_out_dir, exist_ok=True)

    for text_path, audio_path in tqdm(text_audio_map):
        clean_text_path = f"{text_path}.clean"
        clean(text_path, clean_text_path)
        audio_basename = os.path.basename(audio_path)
        audio_basename = os.path.splitext(audio_basename)[0]
        align_path = os.path.join(align_out_dir, f'{audio_basename}.json')
        if not os.path.exists(align_path):
            align(clean_text_path, audio_path, align_path, word_align)


if __name__ == "__main__":
    start_time = time.time()

    text_audio_map = get_text_audio_map()

    # align_out_dir = 'sentence_alignment'
    # align_text(text_audio_map, align_out_dir, word_align=False)

    align_out_dir = 'word_alignment'
    align_text(text_audio_map, align_out_dir, word_align=True)

    print(f'Finished in {time.time()-start_time:0.4f} seconds.')
