# -*- coding: utf-8 -*-
"""
Very hacky script to clean and align amara text

TODO - Clean up

@author: avinashvarna
"""


import datetime
import os
import sys
import json

from tqdm import trange

base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(base_dir)

try:
    from utils.alignment import align, clean
except ImportError:
    pass

def get_num_sargas(k):
    return 10 if k != 3 else 5

def create_alignment():
    os.makedirs('word_alignment', exist_ok=True)
    os.makedirs('sentence_alignment', exist_ok=True)
    os.makedirs('clean_text', exist_ok=True)

    for k in range(1, 4):
        num_sargas = get_num_sargas(k)
        for i in trange(1, num_sargas + 1):
            stem = f'{k}.{i}'
            text_file = f'text/{stem}.txt'
            clean_text_file = f'clean_text/{stem}.txt'
            audio_file = f'audio/{stem}.mp3'
            clean(text_file, clean_text_file)
            for d, w in [('word_alignment', True), ('sentence_alignment', False)]:
                align_file = f'{d}/{stem}.json'
                if not os.path.exists(align_file):
                    align(clean_text_file, audio_file, align_file, w)


def create_json():
    desc = dict()
    desc['name'] = 'अमरकोषः'
    desc["description"] = "Text Source: <a href='https://github.com/aupasana/amara-quiz/blob/master/database/amara_mula.utf8'>https://github.com/aupasana/amara-quiz/blob/master/database/amara_mula.utf8</a>\n<br>\nAudio Source: <a href='https://archive.org/details/AmaraKoshahAudio'>https://archive.org/details/AmaraKoshahAudio</a>"
    data = []
    sarga_names = [["स्वर्गवर्गः", "व्योमवर्गः", "दिग्वर्गः", "कालवर्गः", "धीवर्गः", "शब्दादिवर्गः",
                    "नाट्यवर्गः", "पातालभोगिवर्गः", "नरकवर्गः", "वारिवर्गः"],
                    ["भूमिवर्गः", "पुरवर्गः", "शैलवर्गः", "वनौषधिवर्गः", "सिंहादिवर्गः",
                    "मनुष्यवर्गः", "ब्रह्मवर्गः", "क्षत्रियवर्गः", "वैश्यवर्गः", "शूद्रवर्गः"],
                    ["विशेष्यनिघ्नवर्गः", "सङ्कीर्णवर्गः", "नानार्थवर्गः", "अव्ययवर्गः", "लिङ्गादिसंग्रहवर्गः"]
                   ]
    for k in range(1, 4):
        num_sargas = get_num_sargas(k)
        for i in range(1, num_sargas + 1):
            d = {}
            stem = f'{k}.{i}'
            d["id"] = stem
            d["name"] = f'{stem}: {sarga_names[k-1][i-1]}'
            d["audio_url"] = f"https://archive.org/download/amarakosha_audio/{stem}.mp3"
            d["word_alignment"] = f'word_alignment/{stem}.json'
            d["sentence_alignment"] = f'sentence_alignment/{stem}.json'
            d["text"] = f'text/{stem}.txt'
            data.append(d)
    desc["data"] = data
    with open('data.json', 'w', encoding="utf8") as f:
        json.dump(desc, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    _start_time = datetime.datetime.now()

    # create_alignment()
    create_json()

    _end_time = datetime.datetime.now()
    delta = _end_time - _start_time
    print(f"Took {delta} ({delta.total_seconds()} s)")
