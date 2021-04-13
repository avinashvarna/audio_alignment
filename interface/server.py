#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 02:52:57 2021

@author: Hrishikesh Terdalkar
"""

###############################################################################

import re
import os
import glob
import json

from flask import Flask, render_template, url_for, redirect

###############################################################################

server_dir = os.path.dirname(os.path.realpath(__file__))

corpora_data = glob.glob(
    os.path.join(os.path.dirname(server_dir), '*', 'data.json')
)

corpora = {}

for corpus_data in corpora_data:
    with open(corpus_data) as f:
        data = json.load(f)

    corpus_path = os.path.dirname(corpus_data)
    corpus_name = os.path.basename(corpus_path)
    corpora[corpus_name] = {
        'path': corpus_path,
        'data': {e['key']: e for e in data['data']}
    }

###############################################################################

webapp = Flask(__name__)
webapp.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'audio-alignment')
webapp.url_map.strict_slashes = False

###############################################################################


@webapp.context_processor
def inject_globals():
    return {
        'title': 'Audio Alignment'
    }


@webapp.route("/corpus/")
@webapp.route("/corpus/<string:corpus>/")
@webapp.route("/corpus/<string:corpus>/<string:key>/")
def show_corpus(corpus=None, key=None):
    data = {}
    data['corpora'] = corpora

    if corpus is not None and corpus not in corpora:
        return redirect(url_for('show_corpus'))

    if key is not None:
        corpus_path = corpora[corpus]['path']
        if key not in corpora[corpus]['data']:
            return redirect(url_for('show_corpus', corpus=corpus))

        info = corpora[corpus]['data'][key]
        audio_url = info['audio_url']

        word_alignment_file = os.path.join(corpus_path, info['word_alignment'])

        with open(word_alignment_file) as f:
            word_alignment = json.load(f)

        lines = []
        current_line = []
        last_s = 1
        for fragment in word_alignment['fragments']:
            fragment_id = fragment['id']
            match = re.match(r'^p(\d+)s(\d+)w(\d+)$', fragment_id)
            if match:
                s = int(match.group(2))
                if s > last_s:
                    lines.append(current_line)
                    current_line = []
                    last_s = s
            current_line.append(fragment)

        lines.append(current_line)

        data['key'] = key
        data['corpus'] = corpus
        data['name'] = info['name']
        data['audio'] = audio_url
        data['lines'] = lines

    return render_template("corpus.html", data=data)


@webapp.route("/")
def home():
    return redirect(url_for('show_corpus'))

###############################################################################


if __name__ == '__main__':
    import socket

    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)
    port = '8484'

    webapp.run(host=host, port=port, debug=True)
