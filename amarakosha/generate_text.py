# -*- coding: utf-8 -*-
"""
Use ashtadhyayi amara data

@author: avinashvarna
"""


import datetime
import json
from natsort import natsorted
from collections import defaultdict

from indic_transliteration.sanscript import transliterate, DEVANAGARI, SLP1


if __name__ == "__main__":
    _start_time = datetime.datetime.now()

    sarga_names = [["स्वर्गवर्गः", "व्योमवर्गः", "दिग्वर्गः", "कालवर्गः", "धीवर्गः", "शब्दादिवर्गः",
                    "नाट्यवर्गः", "पातालभोगिवर्गः", "नरकवर्गः", "वारिवर्गः"],
                    ["भूमिवर्गः", "पुरवर्गः", "शैलवर्गः", "वनौषधिवर्गः", "सिंहादिवर्गः",
                    "मनुष्यवर्गः", "ब्रह्मवर्गः", "क्षत्रियवर्गः", "वैश्यवर्गः", "शूद्रवर्गः"],
                    ["विशेष्यनिघ्नवर्गः", "सङ्कीर्णवर्गः", "नानार्थवर्गः", "अव्ययवर्गः", "लिङ्गादिसंग्रहवर्गः"]
                   ]

    with open('amara_data.txt', encoding='utf8') as f:
        data = json.load(f)['data']

    vargas = defaultdict(lambda : defaultdict(dict))
    for shloka in data:
        num = shloka['num']
        text = shloka['text']
        text = text.replace('। ', '[।]\n')
        num_dev = transliterate(num, SLP1, DEVANAGARI).replace('।', '.')
        text = text.replace('॥', f'[॥{num_dev}॥]\n')


        kaanda, varga, shloka_num = num.split('.')
        k_v = f'{kaanda}.{varga}'
        vargas[k_v][num] = text


    for varga_num, shlokas in vargas.items():
        kaanda, varga = varga_num.split('.')
        kaanda, varga = int(kaanda), int(varga)
        keys = natsorted(shlokas.keys())
        texts = [shlokas[k] for k in keys]
        with open(f'text/{varga_num}.txt', 'w', encoding='utf8') as f:
            name = sarga_names[kaanda-1][varga-1]
            if varga_num == '1.1':
                s = 'नामलिङ्गानुशासनं नाम अमरकोषः [।]\n\nप्रथमकाण्डम् [।]\n\n'
            elif varga_num == '2.1':
                s = 'श्री-अमरसिंहविरचितं नामलिङ्गानुशासनम् [।]\n\nद्वितीयं काण्डम् [।]\n\nवर्गभेदाः [।]\n\n'
            elif varga_num == '3.1':
                s = 'श्री-अमरसिंहविरचितं नामलिङ्गानुशासनम् [।]\n\nतृतीयं काण्डम् [।]\n\nवर्गभेदाः [।]\n\n'
            else:
                s = f'अथ {name} [।]\n\n'
            s += '\n'.join(texts)
            s += f'\nइति {name} [।]\n'
            f.write(s)



    _end_time = datetime.datetime.now()
    delta = _end_time - _start_time
    print(f"Took {delta} ({delta.total_seconds()} s)")