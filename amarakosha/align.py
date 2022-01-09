# -*- coding: utf-8 -*-
"""
Very hacky script to clean and align amara text

TODO - Clean up

@author: avinashvarna
"""


import datetime
import os
import sys
import re
import json

from indic_transliteration.sanscript import transliterate, DEVANAGARI, SLP1
from tqdm import trange

base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(base_dir)

try:
    from utils.alignment import align
except ImportError:
    pass


def clean_text():
    ''' Add shloka numbers and clean text'''
    with open('text/amara_mUla.txt', encoding='utf8') as f:
        text = f.read()

    kaandas = re.split('<kANda_\d>\n', text, flags=re.DOTALL)
    # Ignore first '<doc>'
    for k in kaandas[1:]:
        lines = []
        last_varga = 0
        for line in k.split('\n'):
            line = line.strip()
            # line = line.replace('।', ' ।').replace('॥', ' ॥')
            line = line.replace('[','').replace(']','')
            line = re.sub('{[a-z]*}','', line)
            if line.startswith('<'):
                # if line.startswith('</Sloka'):
                #     index = line[8:-1]
                #     kaanda, varga, shloka = index.split(".")
                #     lines[-1] += f' {transliterate(shloka, SLP1, DEVANAGARI)} ॥'
                if line.startswith('<Sloka'):
                    index = line[7:-1]
                    kaanda, varga, shloka = index.split(".")
                    last_varga = f'{kaanda}.{varga}'
                continue
            if line == '' and last_varga != 0:
                with open(f'text/{last_varga}.txt',
                          'w', encoding='utf8') as f:
                    f.write('\n'.join(lines))
                lines = []
                continue
            lines.append(line.replace('/', '').replace('[','').replace(']',''))


def get_num_sargas(k):
    return 10 if k != 3 else 5


def create_kaanda_files():
    for k in range(1, 4):
        text = ''
        num_sargas = get_num_sargas(k)
        for i in range(1, num_sargas + 1):
            with open(f'text/{k}.{i}.txt', encoding='utf8') as f:
                text += f.read() + '\n'
        with open(f'text/{k}.txt', 'w', encoding='utf8') as f:
            f.write(text)


def create_alignment():
    for k in range(1, 4):
        num_sargas = get_num_sargas(k)
        for i in trange(1, num_sargas + 1):
            stem = f'{k}.{i}'
            text_file = f'text/{stem}.txt'
            audio_file = f'audio/{stem}.mp3'
            align_file = f'word_alignment/{stem}.json'
            if (os.path.exists(audio_file) and os.path.exists(text_file)
                and not os.path.exists(align_file)):
                align(text_file, audio_file, align_file, True)
                add_shloka_numbers_word_alignment(align_file)


def create_json():
    desc = dict()
    desc['name'] = 'अमरकोषः'
    desc["description"] = "Text Source: <a href='https://github.com/aupasana/amara-quiz/blob/master/database/amara_mula.utf8'>https://github.com/aupasana/amara-quiz/blob/master/database/amara_mula.utf8</a>\n<br>\nAudio Source: <a href='https://archive.org/details/AmaraKoshahAudio'>https://archive.org/details/AmaraKoshahAudio</a>"
    data = []
    sarga_names = [["स्वर्गवर्गः", "व्योमवर्गः", "दिग्वर्गः", "कालवर्गः", "धीवर्गः", "शब्दादिवर्गः",
                    "नाट्यवर्गः", " पातालभोगिवर्गः", "नरकवर्गः", "वारिवर्गः"],
                    ["भूमिवर्गः", "पुरवर्गः", "शैलवर्गः", "वनौषधिवर्गः", "सिंहादिवर्गः",
                    "मनुष्यवर्गः", "ब्रह्मवर्गः", "क्षत्रियवर्गः", "वैश्यवर्गः", "शूद्रवर्गः"],
                    ["विशेष्यनिघ्नवर्गः", "सङ्कीर्णवर्गः", "नानार्थवर्गः", "अव्ययवर्गः", "लिङ्गादिसंग्रहवर्गः"]
                   ]
    for k in range(1, 4):
        num_sargas = get_num_sargas(k)
        for i in range(1, num_sargas + 1):
            d = {}
            stem = f'{k}.{i}'
            align_file = f'word_alignment/{stem}.json'
            if os.path.exists(align_file):
                d["id"] = stem
                d["name"] = f'{stem}: {sarga_names[k-1][i-1]}'
                d["audio_url"] = f"https://archive.org/download/amarakosha_audio/{stem}.mp3"
                d["word_alignment"] = align_file
                d["sentence_alignment"] = ""
                data.append(d)
    desc["data"] = data
    with open('data.json', 'w', encoding="utf8") as f:
        json.dump(desc, f, ensure_ascii=False, indent=2)


def add_shloka_numbers_word_alignment(json_file_path):
    with open(json_file_path, encoding='utf8') as f:
        alignment = json.load(f)
    shloka_num = 1
    for w in alignment['fragments']:
        line = w["lines"][0]
        line = line.replace('।', ' ।').replace('॥', ' ॥')
        if line[-1] == "॥":
            line += f' {transliterate(str(shloka_num), SLP1, DEVANAGARI)} ॥'
            shloka_num += 1
        w["lines"][0] = line
    with open(json_file_path, 'w', encoding='utf8') as f:
        json.dump(alignment, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    _start_time = datetime.datetime.now()
    # clean_text()

    create_alignment()
    create_json()

    _end_time = datetime.datetime.now()
    delta = _end_time - _start_time
    print(f"Took {delta} ({delta.total_seconds()} s)")