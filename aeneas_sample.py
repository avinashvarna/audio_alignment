# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 18:43:35 2021

@author: Avinash Varna
"""

import os
import time
import re

from aeneas.executetask import ExecuteTask
from aeneas.task import Task


def is_devanagari(char):
    unicode_val = ord(char)
    return unicode_val >= 0x0900 and unicode_val < 0x0980


def clean_text(input_path, output_path):
    with open(input_path, encoding='utf-8') as f:
        text = f.read()

    # Remove anything within parenthesis
    text = re.sub('\(.*?\)', '', text)
    # Remove + marks
    text = text.replace('+', '')

    lines = []
    for line in text.split('\n'):
        line = line.strip()
        # Remove all lines that don't start with Devanagari
        if line == '' or not is_devanagari(line[0]):
            continue
        # Only retain portion before । or ॥
        index = line.find(u'।')
        index_1 = line.find(u'॥')
        # If both are present retain first
        if index != -1 and index_1 != -1:
            index = min(index, index_1)
        else:
            # Retain the larger one
            index = max(index, index_1)
        # If neither was found, then retain entire line
        if index == -1:
            index = len(line)
        line = line[:index]

        if line != '':
            lines.append(line)

    with open(output_path, mode='w', encoding='utf8') as f:
        f.write('\n'.join(lines))
        f.write('\n')

    return lines


def align(text_path, audio_path, align_path):
    # create Task object
    config_string = u"task_language=hi|is_text_type=plain|os_task_file_format=json"
    task = Task(config_string=config_string)
    task.text_file_path_absolute = text_path
    task.audio_file_path_absolute = audio_path
    task.sync_map_file_path_absolute = align_path

    # process Task
    ExecuteTask(task).execute()

    # output sync map to file
    task.output_sync_map_file()


if __name__ == "__main__":
    start_time = time.time()

    input_path = '001_sanxepa.md'
    audio_path = 'Kanda_1_BK-001-Samksheparamayanam.mp3'

    base, ext = os.path.splitext(input_path)
    output_path = base + '_cleaned' + ext

    align_path = base + '_aligned.json'

    lines = clean_text(input_path, output_path)
    align(output_path, audio_path, align_path)

    print(f'Finished in {time.time()-start_time:0.4f} seconds.')