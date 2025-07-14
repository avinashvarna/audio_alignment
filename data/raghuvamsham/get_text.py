# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 15:18:53 2024

@author: kmadh
"""

import datetime
import json
import os


# The json can be obtained from:
# https://raw.githubusercontent.com/sanskritsahitya-com/data/main/raghuvansham/raghuvansham.json


if __name__ == "__main__":
    _start = datetime.datetime.now()

    text_dir = "text"
    num_sargas = 19
    
    with open("raghuvansham.json", encoding="utf8") as f:
        d = json.load(f)
    data = d["data"]
    
    sargas = [dict() for _ in range(num_sargas)]
    
    for item in data:
        sarga_idx = int(item['c']) - 1
        sarga_dict = sargas[sarga_idx]
        sarga_dict[item['i']] = item["v"]

    os.makedirs(text_dir, exist_ok=True)

    for idx, sarga_dict in enumerate(sargas):
        with open(f"{text_dir}/{idx + 1:02d}.txt", "w", encoding="utf8") as f:
            indices = sorted(sarga_dict.keys())
            for i in indices:
                text = sarga_dict[i]
                f.write(text)
                f.write("\n\n")

    
    with open("text_audio_map.csv", "w") as f:
        for idx in range(num_sargas):
            s = f"{idx+1:02d}"
            f.write(f"text/{s}.txt,audio/Raghuvansham-{s}.mp3\n")

    _end = datetime.datetime.now()
    _delta = _end - _start
    print(f'Took {_delta} ({_delta.total_seconds()}s)')
