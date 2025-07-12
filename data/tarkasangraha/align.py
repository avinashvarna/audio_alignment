# -*- coding: utf-8 -*-
"""
Align tarksangraha text with audio

Text source: https://sanskritdocuments.org/doc_z_misc_major_works/tarka2.html
Audio: https://archive.org/details/Ramayana-recitation-Sriram-harisItArAmamUrti-Ghanapaati-v2/

@author: Avinash Varna
"""

import os
import time
import sys
import json

from indic_transliteration.sanscript import transliterate, ITRANS, DEVANAGARI


base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(base_dir)

try:
    from utils.alignment import align
except ImportError:
    pass


def clean_text(in_file, out_file):
    with open(in_file, 'r', encoding='utf8') as fin, open(
            out_file, 'w', encoding='utf8') as fout:
        for line in fin:
            line = line.rstrip('\n')
            # Only retain portion before । or ॥
            index = line.find(u' ।')
            if index != -1:
                line = line[:index] + u'।'
            index = line.find(u' ॥')
            if index != -1:
                line = line[:index] + u'॥'
            fout.write(line + '\n')


def align_text(text_path, audio_path, align_out_dir, word_align=False):
    audio_basename = os.path.basename(audio_path)
    audio_basename = os.path.splitext(audio_basename)[0]
    align_path = os.path.join(align_out_dir, f'{audio_basename}.json')
    if not os.path.exists(align_path):
        align(text_path, audio_path, align_path, word_align)
    post_process(align_path)


def post_process(json_file):
    with open(json_file, 'r', encoding='utf8') as f:
        alignment_dict = json.load(f)
    index = 1
    index_san = transliterate(str(index), ITRANS, DEVANAGARI)
    for d in alignment_dict['fragments']:
        lines = d['lines']
        for i, line in enumerate(lines):
            line = line.replace('।',' ।')
            if '॥' in line:
                line = line.replace('॥', ' ॥ ' + index_san + ' ॥')
                index += 1
                index_san = transliterate(str(index), ITRANS, DEVANAGARI)
            lines[i] = line
    with open(json_file, 'w', encoding='utf8') as f:
        json.dump(alignment_dict, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    start_time = time.time()

    raw_text_path = 'tarkasaMgrahaH.txt'
    audio_path = 'tarkasaMgrahaH.mp3'

    basename, ext = os.path.splitext(raw_text_path)
    text_path = basename+ '_cleaned' + ext

    clean_text(raw_text_path, text_path)

    align_out_dir = 'sentence_alignment'
    align_text(text_path, audio_path, align_out_dir,
                word_align=False)

    align_out_dir = 'word_alignment'
    align_text(text_path, audio_path, align_out_dir,
                word_align=True)

    print(f'Finished in {time.time()-start_time:0.4f} seconds.')