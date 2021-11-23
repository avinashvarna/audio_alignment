# -*- coding: utf-8 -*-
"""
Align audio to text

@author: Avinash Varna
"""

import re
import json
from functools import partial

from aeneas.executetask import ExecuteTask
from aeneas.task import Task
from aeneas.runtimeconfiguration import RuntimeConfiguration


def clean(text_path, clean_text_path):
    "Prepare text for alignment (Ignore text written in [square-brackets])"
    with open(text_path, encoding="utf-8") as f:
        content = f.read()

    clean_content = re.sub(r"\[.*?\]", "", content)
    with open(clean_text_path, mode="w", encoding="utf-8") as f:
        f.write(clean_content)


def align(text_path, audio_path, align_out_path, word_align=True):
    # create Task object
    config_string = u"task_language=hi"
    config_string += "|os_task_file_format=json"
    rconf = None
    if word_align:
        config_string += "|os_task_file_levels=3"
        config_string += "|is_text_type=mplain"
        rconf = RuntimeConfiguration()
        rconf[RuntimeConfiguration.MFCC_MASK_NONSPEECH] = True
        rconf[RuntimeConfiguration.MFCC_MASK_NONSPEECH_L3] = True
    else:
        config_string += "|is_text_type=plain"

    task = Task(config_string=config_string)
    task.text_file_path_absolute = text_path
    task.audio_file_path_absolute = audio_path
    task.sync_map_file_path_absolute = align_out_path

    # process Task
    ExecuteTask(task, rconf=rconf).execute()

    # output sync map to file
    task.output_sync_map_file()

    # Remove annoying unicode characters
    with open(align_out_path, 'r', encoding='utf8') as f:
        alignment = json.load(f)
    with open(align_out_path, 'w', encoding='utf8') as f:
        json.dump(alignment, f, ensure_ascii=False, indent=2)


sentence_align = partial(align, word_align=False)
word_align = partial(align, word_align=True)
